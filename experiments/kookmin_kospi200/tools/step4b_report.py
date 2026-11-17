"""Aggregate stored Validation diagnostics; never executes any model or fit."""
from pathlib import Path
import datetime,hashlib,json
from zoneinfo import ZoneInfo
import pandas as pd
R=Path(__file__).resolve().parents[1];W=Path('/workspace/work/step4b')
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def table(frame,cols):
 def cell(v):
  if pd.isna(v):return 'null'
  if isinstance(v,float):return f'{v:.6f}'
  return str(v).replace('|','/')
 return '| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'+'\n'.join('| '+' | '.join(cell(v) for v in x)+' |' for x in frame[cols].itertuples(index=False,name=None))
def main():
 m=read('manifests/step4b_execution_manifest.json');c=read('configs/step4b_pilot_config.json');s=read('manifests/step4b_analysis_summary.json');pre=read('manifests/step4b_preflight_results.json');post=read('manifests/step4b_postrun_tests.json');g=read('manifests/step4b_preflight_private.json')
 new=pd.read_csv(R/'manifests/step4b_runs.csv',float_precision='round_trip');allrows=pd.read_csv(R/'manifests/step4b_all200_diagnostic_metrics.csv',float_precision='round_trip');seeds=pd.read_csv(R/'manifests/step4b_seed_stability.csv');price=pd.read_csv(R/'manifests/step4b_price_sensitivity.csv');ltc=allrows[allrows.model=='LTC'];manual=pd.read_csv(R/'manifests/step4b_manual_regime_summary.csv');now=datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
 common='국민대학교 BIT전문대학원 박사학위논문 KOSPI200 LNN 연구의 회고적·탐색적 F1 CPU Train/Validation Pilot이다. A/B는 BOTH_UNVERIFIED, historical18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. Validation은 EarlyStopping과 checkpoint 선택에 쓰였으므로 독립 일반화 성능이 아니다. Seed를 날짜에 연결해 독립 시장 표본 수를 늘리지 않았다. A/B·모델·Seed·날짜·설정을 결과로 선택하지 않았다.'
 cohorts=[]
 for o,parts in g['datasets'].items():
  for p,d in parts.items():
   z=d['metadata'];cohorts.append({'origin':o,'candidate':p,'train_start':z['train_first_sample'],'train_end':z['train_last_sample'],'train_n':z['train_samples'],'train0':z['class_counts']['train']['0'],'train1':z['class_counts']['train']['1'],'validation_start':z['validation_first_sample'],'validation_end':z['validation_last_sample'],'validation_n':z['validation_samples'],'validation0':z['class_counts']['validation']['0'],'validation1':z['class_counts']['validation']['1'],'train_q30':z['manual_reference']['low'],'train_q70':z['manual_reference']['high']})
 cohorts=pd.DataFrame(cohorts);cohorts.to_csv(R/'manifests/step4b_origin_cohorts.csv',index=False)
 instability=[]
 for (o,p,model),t in allrows.groupby(['origin','candidate','model']):
  v=t[t.status=='COMPLETED'];instability.append({'origin':o,'candidate':p,'model':model,'completed':len(v),'best_degenerate':int(v.prediction_status.eq('DEGENERATE_PREDICTION').sum()),'any_degenerate_epochs':int(v.degenerate_prediction_epochs.gt(0).sum()),'total_degenerate_epochs':int(v.degenerate_prediction_epochs.sum()),'total_epochs':int(v.epochs.sum()),'mean_epoch_degenerate_ratio':float(v.degenerate_epoch_ratio.mean()) if len(v) else None})
 instability=pd.DataFrame(instability);instability.to_csv(R/'manifests/step4b_model_instability.csv',index=False)
 def put(name,text):(R/'reports'/name).write_text(text.strip()+'\n')
 metriccols=['source_stage','origin','candidate','seed','model','status','train_samples','validation_samples','epochs','best_epoch','validation_BA','macro_f1','recall0','recall1','accuracy','brier','prediction_positive_rate','degenerate_epoch_ratio']
 put('STEP4B_200FIT_RESULTS_KO.md',f'''# STEP4B 누적 고유 fit 진단

확인시각(KST): {now}

{common}

기존 OLD100_REUSED100개 보존, 승인된 신규100개 중 실제 완료{s['new_completed']} / 실패{s['new_failed']} / BLOCKED{s['new_blocked']} / 중단미완료{s['new_interrupted']}이다. 실제 누적 완료는{s['total_actual_completed']}개이며, 계획200행과 완료 수를 구분한다. STEP3D의 O3는 STEP4A1과 동일하여 추가 집계하지 않았다. 신규{s['new_epochs']}epoch/{s['new_optimizer_updates']}optimizer updates다.

## 날짜 및 클래스 support

{table(cohorts,list(cohorts.columns[:12]))}

20KRX세션 label_end, Train20purge·Validation 말단20UNKNOWN 제외, 입력t-19~t, F1=[Log_Ret,Disparity] 및 공통 Vol_Regime 유한window 마스크를 유지했다. Scaler는 유지된 Train window 날짜 합집합에만 fit했다. Vol_Regime은 모델 입력이 아니다.

## 신규100 identity 실제 결과

{table(new,metriccols)}

[누적200개 원값](../manifests/step4b_all200_diagnostic_metrics.csv), [학습 이력 집계](../manifests/step4b_training_summary.csv), [Seed 진단](STEP4B_SEED_STABILITY_KO.md), [LTC 진단](STEP4B_LTC_DIAGNOSTICS_KO.md)에 OLD100_REUSED/STEP4B_NEW100을 구분했다. 실패·결측을0으로 채우거나 나쁜 Seed를 제거하지 않았다. HMM/Test/GPU/Ensemble/외부피처/τactual/p값/2026은0건이다.

## 수동 레짐

각 Origin의 유지된 Train q30/q70을 새 학습 전에 고정했다. Validation 분위수 재계산이나 임계값 선택은 하지 않았다. 동일 best Validation 확률의 Low/Mid/High 층화이며 HMM과 분리한다. 빈 레짐·실제 한 클래스 레짐의 BA/MacroF1=null이고 없는 클래스 Recall=null이다. 모델이 한 클래스만 예측해도 실제 두 클래스가 있으면 지표를 계산하고 퇴화 flag를 별도 기록한다.

[모델·Seed별 레짐 support 및 지표](../manifests/step4b_manual_regime_metrics.csv), [집계](../manifests/step4b_manual_regime_summary.csv), [Train-only 임계값](../manifests/step4b_origin_cohorts.csv)을 함께 보존했다. 레짐 결과로 모델·경계를 선택하지 않았다.
''')
 seedcols=['origin','candidate','model','completed_seeds','validation_BA_seed2','validation_BA_seed12','validation_BA_seed22','validation_BA_seed32','validation_BA_mean','validation_BA_std','validation_BA_min','validation_BA_max','macro_f1_mean','macro_f1_std','macro_f1_min','macro_f1_max','brier_mean','brier_std','brier_min','brier_max']
 put('STEP4B_SEED_STABILITY_KO.md',f'''# STEP4B 네 Seed 안정성

{common}

각 Origin×가격×모델에서 Seed[2,12,22,32]의 원값·평균·표본표준편차(ddof1)·범위를 모두 보고한다. 실패/미완료는null이며 completed_seeds/지표별 valid_seeds를 함께 기록한다. 네 Seed만으로 확증적 유의성이나 일반화 우위를 주장하지 않는다. 같은 Validation 날짜의 반복이므로 표본 수를4배로 늘리지 않는다.

{table(seeds,seedcols)}

MacroF1/Brier 및 모든 지표의 Seed별 원값, Recall0/1,Accuracy,positive rate,best/total epoch,퇴화 epoch비율도 [전체 Seed CSV](../manifests/step4b_seed_stability.csv)에 있다. 기존 Seed2/12 짝지은 차이는 [baseline pairs](../manifests/step4b_baseline_seed_pairs.csv)에 고정 보존했다.
''')
 put('STEP4B_LTC_DIAGNOSTICS_KO.md',f'''# STEP4B LTC 반복 불안정성

{common}

## LTC 네 Seed 전수

{table(ltc,['source_stage','origin','candidate','seed','status','epochs','best_epoch','validation_BA','macro_f1','prediction_status','prediction_positive_rate','degenerate_prediction_epochs','degenerate_epoch_ratio'])}

Seed12와 신규Seed22/32의 Origin별 반복 여부, bestepoch·종료epoch 및 A/B차이를 모두 보존한다. 단일 클래스 예측은 수치 발산과 구분한다. 신규 LTC best 단일클래스 checkpoint는 {int(new[new.model=='LTC'].prediction_status.eq('DEGENERATE_PREDICTION').sum())}개다. 실패를 다른 Seed나 설정으로 대체하지 않았다.

## 다른 네 모델을 포함한 동일 진단

{table(instability,list(instability.columns))}

best_degenerate는 최적 checkpoint가 단일 클래스인 완료fit 수이고 any_degenerate_epochs는 학습 중 한번이라도 발생한fit 수다. 퇴화epoch 원값·분모 및 완료fit 수를 함께 해석한다. τactual forward, HMM 및 확증 p값은 실행하지 않았다.
''')
 put('STEP4B_PRICE_SENSITIVITY_KO.md',f'''# STEP4B A/B 가격 민감도

{common}

A=기존3894종가+누락45보완, B=사용자 전체Excel3939종가 후보를 유지했다. 기존 가격 충돌2건에 관한 출처 미확정 상태를 바꾸지 않았다. 같은 Origin/Seed/모델의 A/B Validation 차이는 수치 민감도 진단이며 우열에 따른 주 가격 선정이 아니다.

{table(price,['origin','seed','model','completed_candidates','validation_BA_A','validation_BA_B','validation_BA_delta_B_minus_A','macro_f1_A','macro_f1_B','macro_f1_delta_B_minus_A','brier_A','brier_B','brier_delta_B_minus_A','best_epoch_A','best_epoch_B'])}

다른 Recall/Accuracy/positive rate/학습epoch/퇴화비율 차이는 [전체CSV](../manifests/step4b_price_sensitivity.csv)에 있다. 공급처·개정정책·historical18:00 KST 가용성 증빙 전까지 BOTH_UNVERIFIED/PIT BLOCKED를 유지한다.
''')
 baseline=json.loads((W/'before.json').read_text());changed=[p for p,h in baseline.items() if sha(R/p)!=h];assert not changed,changed
 resume=[j['run_id'] for j in m['new_records'].values() if j.get('resume_from_committed_epoch')]
 put('STEP4B_EXECUTION_AUDIT_KO.md',f'''# STEP4B 실행 감사

{common}

사용자 승인: 5Origin×2가격×Seed22/32×5모델=정확히100 신규fit. Seed42~92/전체잔여400은 승인되지 않았고 실행하지 않았다. 별도 [승인](../manifests/step4b_authorization.json), [로스터](../manifests/step4b_job_roster.csv), scoped config/manager/worker로 제한했다. master training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false를 유지했다.

실행시각 {m['started_at_kst']}~{m['finished_at_kst']}. 완료{s['new_completed']}, 실패{s['new_failed']}, BLOCKED{s['new_blocked']}, 중단{s['new_interrupted']}, 확정epoch재개 {len(resume)}개다. 기존100개 재학습0, STEP3D중복집계0. 기존 {len(baseline)}파일 SHA 변경0. 사전검사{pre['passed']}PASS/{pre['failed']}FAIL, 사후{post['passed']}PASS/{post['failed']}FAIL, 신규checkpoint복원감사{s['new_checkpoint_audits_PASS']}/{s['new_completed']}PASS다.

새 worker 실제 helper AST 및 원본 정의를 사용한 합성CPU smoke: 5모델 constructor/forward/backward/gradient clipping/AdamW·OneCycle step/checkpoint·RNG 복원, 모델당 합성1update만 실행했다. 금융 입력은 사용하지 않았다. 실제 worker의 미승인identity entrypoint/변경scope 거절, 5Origin별 실제filebarrier를 별도 subprocess로 검증했다. 합성smoke는 전체실험이나 실증성능이 아니다.

각 worker는 자기 Origin input subtree와 자기job출력만 금융 파일 접근을 허용했다. O1~O5 각각2020/2021/2022/2023/2024년까지만 가격prefix를 수치로 사용했다. Origin간 Validation/Test연도 중첩은 사용자 승인 범위의 해당Origin에만 허용하며 다른Origin 배열을 전달하지 않았다. 공식달력의 날짜/전체원천byte SHA와 가격 관측값 파싱을 구분한다. 독립 Test가격·Target·확률/2026은 사용0건이다.

CPU2core/8GiB, worker≤2/LTC≤1/Torch thread1, CPUFP32/AMP OFF. 버전 Torch{c['environment_versions']['torch']}/ncps{c['environment_versions']['ncps']}/hmmlearn{c['environment_versions']['hmmlearn']}를 바꾸지 않았다. 원본 모델·seedoffset·Focal전역alpha·고정 하이퍼파라미터와 학습kernel은 STEP3C와 바이트 동일하다. Validation BA strict 개선만 best 선택, 동률은 최초 최고 유지다.

모든checkpoint는 model/optimizer/scheduler/EarlyStopping/Python·NumPy·Torch·DataLoader RNG, committed epoch/batch0, Origin/가격/Seed/모델,feature/scaler/data/source/config/environment SHA를 보존한다. 최초epoch 원래logits/state/RNG 복원 일치와 best확률·두독립복원logits·전체payload roundtrip을 검사했다. 감사 중 추가optimizer update0이다. 원래best epoch의 rawlogits 자체는 저장하지 않아 그tensor직접비교라고 주장하지 않는다. 중간batch복원이 아닌 마지막확정epoch부터 동일identity로만 재개 가능하다. 실패나완료identity를 자동재학습하지 않았다.

Master SHA `{c['master_config_sha256']}`\n\nPilot SHA `{m['config_sha256']}`\n\nWorker SHA `{m['worker_sha256']}`\n\nLearning kernel SHA `{c['learning_kernel_sha256']}`\n\nEnvironment SHA `{c['environment_sha256']}`

신규runs/sidecar는 위hash와 best/latest/history해시를 연결한다. 가격·일별Target·확률·weights/checkpoint·스케일러상세/개인경로는 ignored로컬에만 보존한다. 공개본은 코드·집계·비민감hash·축약실행manifest이며 전체operationalmanifest는 로컬전용이다. main/JOF V14/V15·원본Notebook/CSV·기존논문표·기존100checkpoint는 보존했다. 독립Test/HMM/GPU/Ensemble/외부피처/τactual/확증p값/전체Notebook 실행은 모두0이다.
''')
 put('STEP4B_NEXT_GATES_KO.md',f'''# STEP4B 종료 및 다음 실행 조건

{common}

실제누적완료 {s['total_actual_completed']}개, 전체500개중 남은고유미완료 {500-s['total_actual_completed']}개다. 성공100개를 가정하지 않고 실제{s['new_completed']}개만 더했다. 신규100개가 모두성공하면 누적200/잔여300이다. Seed42/52/62/72/82/92의 미실행 조합은5Origin×6Seed×2가격×5모델=300개이며 이번에자동실행하지 않는다. 만일실패가있으면 그identity와 재개·재시도예산을 별도구분해야 한다.

다음학습은 범위·예산·독립승인·동결검증 후에만 가능하다. 가격소스는 공급처신뢰성·정의·개정정책·historical가용성증빙으로 결정해야 하고 Validation성능을 근거로 고르지 않는다. production-PIT,독립Test,Ensemble,RAW5/LOG2재현,외부피처Ablation,HMM,τactual,확증통계는 각각미승인/증빙미해결 상태다. 실제4개Seed 진단으로 통계적유의성·일반화우위를 주장하지 않는다. STEP4B 종료후추가학습0이다.
''')
 audit_path=R/'reports/STEP4B_EXECUTION_AUDIT_KO.md'
 audit_path.write_text(audit_path.read_text()+'\n세부 epoch별 학습·검증 이력 공개는 연구 산출물 노출 위험으로 자동 승인 검토에서 거부됐다. 원본 이력은 로컬에 그대로 보존하고 공개본에서 제외했다. 공개 학습 이력 집계는 Origin·가격·모델·실행 단계별 epoch 수와 퇴화 사례의 집계만 담으며 개별 epoch의 loss/검증 지표를 포함하지 않는다.\n')
 for filename,asset,caption in [('STEP4B_200FIT_RESULTS_KO.md','step4b_seed_validation.svg','Seed별 Validation BA와 평균±표본표준편차: 확증적 신뢰구간이 아님'),('STEP4B_LTC_DIAGNOSTICS_KO.md','step4b_LTC_degenerate.svg','LTC의 단일 클래스 예측 epoch 비율과 best checkpoint 상태')]:
  report=R/'reports'/filename;report.write_text(report.read_text()+f'\n![{caption}](assets/{asset})\n')
 next_path=R/'reports/STEP4B_NEXT_GATES_KO.md'
 next_path.write_text(next_path.read_text()+'\n과거 Origin의 Test 연도가 후속 Origin의 Validation으로 이미 관찰되는 역사적 구조와 기존 논문 결과 노출을 유지해 설명한다. 이번에 독립 Test 예측을 새로 실행하지 않았다는 사실은 해당 역사적 연도가 전혀 관찰되지 않은 전향적 holdout이라는 뜻이 아니다. 이 구조를 결과 기반 사양 변경이나 독립 일반화 우위 주장에 사용하지 않는다.\n')
 audit_path.write_text(audit_path.read_text()+'\n전체 config 공개는 로컬 경로와 상세 운영 메타데이터 때문에 자동 승인 검토에서 거부됐다. 실행 중인 원본 config를 수정하지 않고 로컬에 보존했으며, 공개 config는 승인 범위·고정 학습 설정·차단 상태·해시만 포함한 축약본이다. 공개 config의 private_operational_config_sha256가 실제 실행 config를 연결한다.\n')
 evidence=W/'resume_evidence.json'
 if evidence.exists():
  e=json.loads(evidence.read_text());(R/'manifests/step4b_resume_audit.json').write_text(json.dumps(e,indent=2)+'\n')
  audit_path.write_text(audit_path.read_text()+f"\n실행 중 모니터링 도구의 abort 이후 manager/worker 프로세스 종료를 확인했다. 중단 원인을 사용자 직접 취소로 단정하지 않는다. 완료83개는 해시 검증 후 skip했고 {e['job_id']}는 확정epoch{e['committed_epoch']} checkpoint에서 동일 identity·동결 코드로 재개했다. 중단 전 result와 checkpoint snapshot의 해시를 보존했다. 동결 worker가 재개 시 record-level epoch1/RNG flags를 false로 초기화하는 메타데이터 한계가 있어, 과거 최초epoch 복원 PASS는 중단 전 실제 증거로 검증했다. 해당 flag를 조용히 true로 교체하거나 학습 코드를 수정하지 않았다. 재개 후 best checkpoint·payload·RNG 감사는 별도 실행된다. history의 optimizer update 수는 확정epoch 기준이며 중단된 미확정batch 작업량을 임의로 추정하지 않는다. 모니터링과 학습 실행 세션을 분리해 재개했다.\n")
 verification={**s,'preflight_tests_PASS':pre['passed'],'postrun_tests_PASS':post['passed'],'postrun_tests_FAIL':post['failed'],'old_files_preserved':len(baseline),'old_files_changed':0,'remaining_unique_fits':500-s['total_actual_completed'],'training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'resumed_identities':len(resume)}
 (R/'manifests/step4b_verification_summary.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification))

if __name__=='__main__':main()
