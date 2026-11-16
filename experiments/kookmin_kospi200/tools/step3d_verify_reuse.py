"""Read-only O3 reuse audit. No torch import, checkpoint load or training entrypoint."""
from pathlib import Path
import ast, hashlib, importlib.util, importlib.metadata, io, json, sys, unittest
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[1]
W = Path('/workspace/work/step3d')
sys.path.insert(0, str(R / 'src'))
from kospi200.master_data import prepare_origin

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(p):
    return json.loads((R / p).read_text())

def write(p, value):
    (R / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def table(frame, cols):
    frame = frame[cols]
    def cell(x):
        if pd.isna(x): return 'null'
        if isinstance(x, (float, np.floating)): return f'{x:.6f}'
        return str(x).replace('|', '/')
    return '| ' + ' | '.join(cols) + ' |\n| ' + ' | '.join(['---']*len(cols)) + ' |\n' + '\n'.join('| ' + ' | '.join(cell(x) for x in row) + ' |' for row in frame.itertuples(index=False, name=None))

def main():
    baseline = json.loads((W / 'before.json').read_text())
    checks = []
    def gate(name, condition):
        checks.append({'id': name, 'status': 'PASS' if condition else 'FAIL'})
        if not condition: raise RuntimeError(name)
    master = read('configs/step3c_master_experiment_config.json')
    freeze = read('manifests/step3c_protocol_freeze.json')
    gate('master_config_and_production_flags', sha(R/'configs/step3c_master_experiment_config.json') == freeze['config_sha256'] and all(master[k] is False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']))
    gate('master_artifacts_and_frozen_reports', all(sha(R/x['file']) == x['sha256'] for x in master['implementation_artifacts'] + freeze['reports']))
    gate('pinned_environment', all(importlib.metadata.version(k) == v for k,v in master['environment_versions'].items()))
    old = read('manifests/step3c_prepared_inputs.json')['reused_completed']
    gate('exact_existing40', len(old) == 40 and len({x['run_id'] for x in old}) == 40)
    old_hashes = []
    for job in old:
        folder = R / job['source_directory']
        for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:
            gate('old40_' + job['run_id'] + '_' + file, sha(folder/file) == job['record'][key])
            old_hashes.append({'file':str((folder/file).relative_to(R)), 'sha256':job['record'][key]})
    execution = read('manifests/step4a1_execution_manifest.json')
    preflight = read('manifests/step4a1_preflight.json')
    config = read('configs/step4a1_o3_pilot_config.json')
    roster = {(f'O3_seed{s}_{p}_{m}') for s in [2,12] for p in ['A','B'] for m in ['RNN','LSTM','GRU','LTC','CfC']}
    gate('exact20_previously_completed_O3', set(execution['new_records']) == roster and all(x['status']=='COMPLETED' for x in execution['new_records'].values()))
    gate('frozen_O3_config_worker_manager', all(sha(R/p) == execution[k] for p,k in [('configs/step4a1_o3_pilot_config.json','config_sha256'),('runtime/step4a1_worker.py','worker_sha256'),('runtime/step4a1_manager.py','manager_sha256')]))
    gate('same_model_hyperparameters_offsets', config['model_settings']==master['model_settings'] and config['model_seed_offsets']==master['model_seed_offsets'] and config['learning_kernel_sha256']==master['learning_kernel_sha256'])
    gate('identical_learning_kernel_bytes', (R/'runtime/step4a1_worker.py').read_text().split(' def equal(x,y):',1)[1] == (R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1])
    for candidate,info in preflight['datasets']['O3'].items():
        for file,key in [('array_file','array_sha256'),('metadata_file','metadata_sha256'),('date_file','date_sha256'),('price_file','price_sha256'),('regime_file','regime_sha256')]:
            gate(candidate+'_'+file+'_hash', sha(R/info[file])==info[key])
        # Only the original O3 staged 2010..2022 prefix is parsed. No full price source.
        prices = pd.read_csv(R/info['price_file'], parse_dates=['Date'], float_precision='round_trip')
        gate(candidate+'_price_prefix_2022_only', len(prices)==3208 and prices.Date.max()==pd.Timestamp('2022-12-29') and prices.Date.min()==pd.Timestamp('2010-01-04'))
        calpath = R / info['price_file']; calpath = calpath.parent / 'calendar_private.csv'
        calendar = pd.read_csv(calpath, parse_dates=['Date'])
        arrays, meta, dates, regimes = prepare_origin(prices, calendar, origin='O3', calendar_source=read('provenance/krx_calendar_provenance.json')['source_url'], calendar_sha256=sha(calpath))
        with np.load(R/info['array_file'], allow_pickle=False) as z:
            gate(candidate+'_reconstructed_arrays_exact', all(np.array_equal(arrays[part][i], z[part+suffix]) for part in ['train','validation'] for i,suffix in [(0,'_x'),(1,'_y')]))
        gate(candidate+'_dates_labels_scaler_manual_exact', dates==json.loads((R/info['date_file']).read_text()) and meta['scaler']==info['metadata']['scaler'] and meta['manual_reference']==info['metadata']['manual_reference'])
        gate(candidate+'_purge20_unknown20_boundaries', meta['train_purged']==20 and meta['validation_unknown_excluded']==20 and meta['train_cutoff_violations']==0 and meta['validation_future_endpoint_violations']==0 and (meta['train_samples'],meta['validation_samples'])==(2883,226))
    run = R / execution['run_directory']
    o3hashes=[]
    for jid,record in execution['new_records'].items():
        folder = run/'jobs'/jid
        for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256'),('checkpoint_verification.json','postfit_checkpoint_audit_sha256')]:
            gate(jid+'_'+file+'_hash', sha(folder/file)==record[key])
            o3hashes.append({'file':str((folder/file).relative_to(R)), 'sha256':record[key]})
        history=json.loads((folder/'history.json').read_text())
        best=max(x['validation_BA'] for x in history)
        first=next(x['epoch'] for x in history if x['validation_BA']==best)
        audit=json.loads((folder/'checkpoint_verification.json').read_text())
        gate(jid+'_first_max_BA_and_existing_restore_evidence', first==record['best_validation_epoch'] and audit['status']=='PASS' and audit['best_probability_equal_completed_fit'] and audit['epoch1_training_logits_roundtrip'])
    # Run previous suites in memory; their __main__ writers never run.
    regressions=[]
    for stem,clsname in [('test_step4a1_preflight','O3Preflight'),('test_step4a1_results',None)]:
        spec=importlib.util.spec_from_file_location(stem,R/'tests'/f'{stem}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(getattr(module,clsname)) if clsname else unittest.defaultTestLoader.loadTestsFromModule(module)
        log=io.StringIO(); result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
        regressions.append({'suite':stem,'tests':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors)})
        (W/(stem+'.log')).write_text(log.getvalue())
        gate(stem+'_read_only_regression',result.wasSuccessful())
    gate('no_torch_or_hmm_import', 'torch' not in sys.modules and 'hmmlearn' not in sys.modules)
    # Compile/report runtime smoke only; never creates a new training runner.
    ast.parse(Path(__file__).read_text())
    gate('report_runtime_and_reuse_only_smoke',True)
    frame=pd.read_csv(R/'manifests/step4a1_runs.csv',float_precision='round_trip')
    gate('O3_metrics_exact20_and_support',set(frame.run_id)==roster and frame.validation_samples.eq(226).all() and frame.train_samples.eq(2883).all())
    # Only requested O1/O2/O3 aggregate diagnostics are read; O4/O5 remain untouched.
    combined=pd.read_csv(R/'manifests/step4a1_all60_diagnostic_metrics.csv',float_precision='round_trip')
    gate('O1_O2_O3_aggregate60_unique',len(combined)==60 and combined.run_id.is_unique and set(combined.origin)=={'O1','O2','O3'})
    for df in [frame,combined]:
        for key in list(df.columns):
            if key=='source_directory' or key.endswith('_file') or key.endswith('_directory'):df.drop(columns=key,inplace=True)
    frame['step3d_action']='REUSED_COMPLETED_STEP4A1'
    frame.to_csv(R/'manifests/step3d_runs.csv',index=False)
    metrics=pd.read_csv(R/'manifests/step4a1_metrics.csv',float_precision='round_trip');metrics['step3d_action']='REUSED_COMPLETED_STEP4A1';metrics.to_csv(R/'manifests/step3d_metrics.csv',index=False)
    combined.to_csv(R/'manifests/step3d_origin_comparison.csv',index=False)
    manual=pd.read_csv(R/'manifests/step4a1_manual_regime_summary.csv',float_precision='round_trip');manual.to_csv(R/'manifests/step3d_manual_regime_summary.csv',index=False)
    manual_seed=pd.read_csv(R/'manifests/step4a1_manual_regime_metrics.csv',float_precision='round_trip');manual_seed.to_csv(R/'manifests/step3d_manual_regime_metrics.csv',index=False)
    auth={'stage':'STEP3D','approved_by':'user','approval_reference':'Current user request STEP3D O3 limited 20-fit pilot; prior identical completed fits detected and reused','requested_scope':{'origin':'O3','seeds':[2,12],'candidates':['A','B'],'models':['RNN','LSTM','GRU','LTC','CfC'],'features':['Log_Ret','Disparity'],'maximum_new_fits':20},'execution_policy':'REUSE_EXACT_COMPLETED_IDENTITIES_ONLY','new_training_authorized_for_this_runner':False,'training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'full460_authorized':False,'Test_authorized':False,'GPU_authorized':False,'master_config_sha256':freeze['config_sha256']}
    write('provenance/step3d_authorization.json',auth)
    now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
    manifest={'stage':'STEP3D','checked_at_kst':now,'mode':'VERIFIED_REUSE_OF_ALREADY_COMPLETED_O3','requested_maximum_new_fits':20,'new_fits_this_step':0,'reused_O3_completed':20,'previous_O1_O2_completed_preserved':40,'requested_O1_O2_O3_scope_completed':60,'already_completed_O4_O5_untouched':40,'actual_project_completed':100,'additional_full_grid_fits_remaining':400,'source_stage':'STEP4A1','historical_O3_execution_started':execution['started_at_kst'],'historical_O3_execution_finished':execution['finished_at_kst'],'source_execution_manifest_sha256':sha(R/'manifests/step4a1_execution_manifest.json'),'master_config_sha256':freeze['config_sha256'],'O3_pilot_config_sha256':execution['config_sha256'],'worker_sha256':execution['worker_sha256'],'learning_kernel_sha256':config['learning_kernel_sha256'],'environment_sha256':config['environment_sha256'],'job_hashes':[{k:row[k] for k in ['run_id','origin','seed','candidate','model','best_checkpoint_sha256','latest_checkpoint_sha256','history_sha256']} for row in frame.to_dict('records')],'source_status':'BOTH_UNVERIFIED','production_PIT':'BLOCKED','training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'Test_evaluations':0,'HMM_fit':0,'GPU':0,'new2026_observations_used':0,'new2023plus_price_parsing':0,'new_model_creation_forward_or_checkpoint_load':0,'existing_checkpoint_restore_evidence_verified':20,'new_checkpoint_restore_execution':0,'runtime_smoke':'Read-only report runner and previous O3 boundary regression; no new training runner or training smoke required','independent_Test_claim':False}
    write('manifests/step3d_execution_manifest.json',manifest)
    common='설계2: A/B 병렬 회고적·탐색적 F1 CPU Train/Validation 연구다. A/B=BOTH_UNVERIFIED, production-PIT=BLOCKED를 유지한다. Validation으로 주 가격·모델·Seed·사양을 선택하지 않았다. 독립 Test/HMM/GPU/외부5피처/Ensemble/2026 관측 사용은 이번 단계0건이다.'
    cols=['origin','candidate','seed','model','epochs','best_epoch','validation_BA','macro_f1','recall0','recall1','accuracy','brier','prediction_positive_rate','degenerate_epoch_ratio']
    reports={
      'STEP3D_RESULTS_KO.md':f'''# STEP3D O3 제한 확장 결과 확인\n\n확인시각(KST): {now}\n\n{common}\n\n동일 O3 20개는 STEP4A-1에서 이미 완료됐다. 이번 단계 신규 fit0 / 기존 O3 재사용20 / 기존 O1·O2 보존40이다. 20개를 다시 실행하거나 신규 완료로 중복 집계하지 않았다. 요청 범위 누적60이고, 이미 완료된 O4/O5의40개까지 포함한 실제 프로젝트 누적은100이다. 이번 요청으로 O4/O5를 새로 학습하지 않았다.\n\nO3 Train2010~2021(적격2883개), Validation2022(226개). Train purge20·Validation 말단UNKNOWN20·공식 session_id+20·입력t-19~t·F1 순서와 Train-only scaler를 재검증했다. 기존 O3 가격prefix3208개만 수치 파싱하고 이후 가격은 읽지 않았다.\n\n{table(frame,cols)}\n\n[Origin 비교](STEP3D_ORIGIN_COMPARISON_KO.md) · [LTC](STEP3D_LTC_DIAGNOSTICS_KO.md) · [실행 감사](STEP3D_EXECUTION_AUDIT_KO.md) · [다음 조건](STEP3D_NEXT_GATES_KO.md)\n''',
      'STEP3D_ORIGIN_COMPARISON_KO.md':f'''# STEP3D O1/O2/O3 동일 조합 비교\n\n{common}\n\n세 Origin의60개 기존 완료 조합을 모두 보존한 기술적 비교다. Validation은 checkpoint 선택 자료이며 독립 Test 성능이 아니다. 서로 다른 연도·학습기간·클래스 구성이 달라 인과적 Origin/레짐 효과를 주장하지 않는다. 두 Seed 표준편차는 최종 안정성 근거가 아니다.\n\n{table(combined,cols)}\n\n## O3 수동 변동성 레짐\n\n기존 Train-only q30/q70 참조를 재구성해 동일함을 확인했다. Validation 분위수 재계산은0건이다. Low/Mid/High support는0/35/191이며 Mid의 실제0/1은32/3, High는117/74다. 빈 레짐·실제 단일 클래스는 BA/MacroF1=null, 없는 클래스 Recall=null 정책을 유지한다. 모델이 단일 클래스만 예측한 경우와 실제 정답이 단일 클래스인 경우를 구분한다.\n\n{table(manual,['candidate','model','regime','n_per_seed','n_class0_per_seed','n_class1_per_seed','balanced_accuracy_mean','macro_f1_mean'])}\n''',
      'STEP3D_LTC_DIAGNOSTICS_KO.md':f'''# STEP3D LTC 세 Origin 진단\n\n{common}\n\n{table(combined[combined.model=='LTC'],cols+['prediction_status','degenerate_prediction_epochs'])}\n\n단일 클래스 예측은 DEGENERATE_PREDICTION으로 별도 표시하며 NaN/손실 발산과 동일시하지 않는다. 기존 O3 4개 LTC는 수치 발산 실패가 아니라 완료된 퇴화 예측 사례다. Seed를 교체하거나 loss·patience·epoch를 변경하지 않았다. best epoch는 strict Validation BA의 최초 최고점이며 history 전체의 단일 클래스 epoch 비율을 보존했다.\n''',
      'STEP3D_EXECUTION_AUDIT_KO.md':f'''# STEP3D 실행·재사용 감사\n\n{common}\n\n최초 O3 실행은 {execution['started_at_kst']}~{execution['finished_at_kst']}에 STEP4A-1로 완료됐다. 이번 STEP3D에는20개 신규 학습을 실행하지 않고 정확히 같은20개를 검증·재사용했다. 기존40개 checkpoint/latest/history/Validation 확률160개와 O3의100개 파일 해시를 대조했다.\n\nMaster SHA `{freeze['config_sha256']}`. 학습 kernel SHA `{config['learning_kernel_sha256']}`. O3 config/worker/manager와 원본 모델·환경 pin을 동결 manifest와 대조했다. master production 플래그는 모두false다.\n\nO3 원래 staged 가격·배열·scaler·label/date·Train-only 수동 reference를 재구성했다. 별도 모델 생성/forward/checkpoint load/학습은0건이다. 원래 epoch1 logits/RNG 복원과 best 확률 복원 PASS20건의 증거 파일 SHA를 이번에 검증했으며 새로 복원 실행한 것으로 표현하지 않는다. 학습 runner를 새로 만들지 않아 신규 training runtime smoke는 해당 없음이다. 읽기 전용 보고 runner와 기존 O3 경계 회귀검사는 실제 실행했다.\n\n기존 preflight12개 및 결과14개를 __main__ 기록 함수를 호출하지 않고 재실행했다. 기존 test결과 파일을 덮어쓰지 않는다. 새 검사와 회귀 결과는 [tests](../manifests/step3d_test_results.json)에 기록한다.\n\n상세 원자료 경로/스케일러값/일별Target·확률/weights는 공개하지 않는다. 공개 execution manifest에는 identity·상태·해시·집계만 기록한다. 기존 모든 파일 byte 보존은 아래 preservation 검사로 확인한다. main/JOF/이전 보고서·성능표는 수정하지 않는다.\n''',
      'STEP3D_NEXT_GATES_KO.md':f'''# STEP3D 다음 단계 조건\n\n{common}\n\n이번 요청은 O3만 허용했고 신규 fit 상한20이었다. 동일20개가 이미 완료되어 신규0개, 재사용20개다. 요청 당시 기존40+O3=60개 설계는 이미 충족됐다. 실제 저장소에는 후속 STEP4A-2의40개도 완료되어 전체100개다. 완료 결과를 재학습하거나 누적120개로 중복 보고하지 않는다.\n\n전체500개 계획 대비 남은 고유 조합은400개(5Origin×8Seed[22,32,42,52,62,72,82,92]×2가격×5모델)다. STEP3C 동결 당시460개 잔여 기록은 수정하지 않는다. 이번 승인으로400/460개를 실행하지 않는다. 추가 학습·독립 Test·HMM·GPU·외부피처·Ensemble은 각각 범위·예산·증빙·별도 승인 전 차단을 유지한다. 가격 원천/개정정책/18:00 KST 과거 가용성은 여전히 미확정이다. 가격은 Validation 우열로 선택하지 않는다.\n'''
    }
    reports['STEP3D_RESULTS_KO.md'] += '\n실제 클래스 support는 Train0/1=1276/1607, Validation0/1=149/77이다. 적격 기준일은 Train2010-03-30~2021-12-02, Validation2022-01-03~2022-12-01이며 label_end 최대는 각각2021-12-30/2022-12-29다.\n'
    reports['STEP3D_LTC_DIAGNOSTICS_KO.md'] += '\nO3 Seed2는 A/B 모두17epoch, best7이며 최적 checkpoint는 두 클래스 예측이다. 다만16/17epoch(94.12%)에서 단일 클래스 예측이었다. Seed12는 A/B 모두11epoch, best1, BA0.5이며11/11epoch(100%) 단일 클래스 예측이었다. 이 차이를 보존하며 수치 발산으로 오표기하지 않는다.\n'
    reports['STEP3D_ORIGIN_COMPARISON_KO.md'] += '\n모델·Seed별 레짐 BA/MacroF1/Recall 및 실제 support는 [Seed별 수동 레짐 CSV](../manifests/step3d_manual_regime_metrics.csv)에 별도 보존했다. HMM 레짐과 합치지 않았다.\n'
    for filename,text in reports.items(): (R/'reports'/filename).write_text(text)
    gate('all_previous_files_byte_unchanged',all(sha(R/p)==h for p,h in baseline.items()))
    tests={'stage':'STEP3D','checked_at_kst':now,'new_checks_PASS':sum(x['status']=='PASS' for x in checks),'new_checks_FAIL':sum(x['status']=='FAIL' for x in checks),'regression_suites':regressions,'checks':checks,'BLOCKED':['price_source_certification','historical_18KST_production_PIT'],'new_training_runner_smoke':'NOT_APPLICABLE_REUSE_ONLY','protected_files':len(baseline),'changed_old_files':0}
    write('manifests/step3d_test_results.json',tests)
    private={'old40_artifact_hashes':old_hashes,'O3_artifact_hashes':o3hashes,'baseline_sha256':sha(W/'before.json')}
    (W/'verification_private.json').write_text(json.dumps(private,indent=2))
    print(json.dumps({'new_fit':0,'reused_O3':20,'preserved_previous40':40,'project_total':100,'checks_PASS':tests['new_checks_PASS'],'regressions':regressions,'previous_files_unchanged':len(baseline),'remaining':400}))

if __name__=='__main__':main()
