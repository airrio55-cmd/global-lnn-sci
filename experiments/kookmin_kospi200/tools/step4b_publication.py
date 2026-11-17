"""Public allowlist: source, audit hashes and multi-fit aggregates only."""
from pathlib import Path
import hashlib,json,shutil
import pandas as pd
R=Path(__file__).resolve().parents[1];W=Path('/workspace/work/step4b');P=W/'public'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
def table(d,cols):
 def f(v):return 'null' if pd.isna(v) else f'{v:.6f}' if isinstance(v,float) else str(v)
 return '| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'+'\n'.join('| '+' | '.join(f(v) for v in row)+' |' for row in d[cols].itertuples(index=False,name=None))
def main():
 before=json.loads((W/'before.json').read_text());assert all(sha(R/p)==h for p,h in before.items())
 if P.exists():shutil.rmtree(P) # Disposable staging only; local research originals retained.
 P.mkdir();files=[]
 def put(name,v):
  p=P/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');files.append(name)
 def copy(name):
  p=P/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/name,p);files.append(name)
 def csv(name,d):
  assert not {'seed','run_id','Date','Close','Target','probability','y_true','y_pred','source_directory'} & set(d.columns)
  p=P/name;p.parent.mkdir(parents=True,exist_ok=True);d.to_csv(p,index=False);files.append(name)
 c=read('configs/step4b_pilot_config.json');m=read('manifests/step4b_execution_manifest.json');s=read('manifests/step4b_verification_summary.json')
 keys=['stage','execution_mode','origins','seeds','price_candidates','models','max_new_fits','feature_order','model_settings','model_seed_offsets','source_status','master_config_sha256','learning_kernel_sha256','environment_sha256','training_enabled','hmm_fit_enabled','new_fit_execution_enabled','step4b_execution_enabled','gpu_enabled']
 v={k:c[k] for k in keys};v['private_operational_config_sha256']=sha(R/'configs/step4b_pilot_config.json');v['disclosure']='Redacted public specification; private operational paths and metadata excluded.';put('configs/step4b_pilot_config.json',v)
 for name in ['step4b_authorization.json','step4b_job_roster.csv','step4b_runner_smoke.json','step4b_preflight_results.json','step4b_postrun_tests.json','step4b_old100_extended_audit.json','step4b_analysis_summary.json','step4b_verification_summary.json']:copy('manifests/'+name)
 keys=['stage','scope','started_at_kst','finished_at_kst','new_fit_budget','planned_new_jobs','new_completed','new_failed','new_blocked','new_interrupted','old100_reexecuted','source_status','production_PIT_status','training_enabled','hmm_fit_enabled','Test_evaluation','GPU','HMM_fit','2026_used','config_sha256','authorization_sha256','worker_sha256','manager_sha256']
 v={k:m[k] for k in keys};v['private_execution_manifest_sha256']=sha(R/'manifests/step4b_execution_manifest.json');v['new_fit_execution_enabled']=False
 v['job_hashes']=[{k:r.get(k) for k in ['run_id','origin','seed','candidate','model','status','best_checkpoint_sha256','latest_checkpoint_sha256','history_sha256','postfit_checkpoint_audit_sha256']} for r in m['new_records'].values()]
 v['disclosure']='Identity/status/hash only; per-fit epochs/performance, private paths and thresholds excluded.';put('manifests/step4b_execution_manifest.json',v)
 d=pd.read_csv(R/'manifests/step4b_all200_diagnostic_metrics.csv',float_precision='round_trip');rows=[]
 for keys,t in d.groupby(['origin','candidate','model']):
  t=t[t.status=='COMPLETED'];r=dict(zip(['origin','candidate','model'],keys));r['completed_seeds']=len(t)
  for k in ['validation_BA','macro_f1','brier','recall0','recall1','accuracy','prediction_positive_rate']:
   z=t[k].dropna();r[k+'_mean']=float(z.mean()) if len(z) else None;r[k+'_std_ddof1']=float(z.std(ddof=1)) if len(z)>1 else None
  rows.append(r)
 aggregate=pd.DataFrame(rows);csv('manifests/step4b_public_aggregate_metrics.csv',aggregate)
 instability=pd.read_csv(R/'manifests/step4b_model_instability.csv',float_precision='round_trip');csv('manifests/step4b_model_instability.csv',instability)
 rows=[]
 for seed,t in d[(d.model=='LTC')&d.status.eq('COMPLETED')].groupby('seed'):
  rows.append({'seed_group':f'Seed{seed}','fits_across_origins_candidates':len(t),'best_degenerate_cases':int(t.prediction_status.eq('DEGENERATE_PREDICTION').sum()),'mean_degenerate_epoch_ratio':float(t.degenerate_epoch_ratio.mean())})
 ltc=pd.DataFrame(rows);csv('manifests/step4b_public_ltc_seed_summary.csv',ltc)
 pairs=pd.read_csv(R/'manifests/step4b_price_sensitivity.csv',float_precision='round_trip');rows=[]
 for keys,t in pairs.groupby(['origin','model']):
  r=dict(zip(['origin','model'],keys));r['matched_seed_pairs']=int(t.completed_candidates.eq(2).sum())
  for k in ['validation_BA','macro_f1','brier']:
   z=t[k+'_delta_B_minus_A'].dropna();r[k+'_delta_mean']=float(z.mean()) if len(z) else None;r[k+'_delta_std_ddof1']=float(z.std(ddof=1)) if len(z)>1 else None
  rows.append(r)
 prices=pd.DataFrame(rows);csv('manifests/step4b_public_price_aggregate.csv',prices)
 manual=pd.read_csv(R/'manifests/step4b_manual_regime_summary.csv',float_precision='round_trip').drop(columns=['n_per_seed','n_class0_per_seed','n_class1_per_seed']);csv('manifests/step4b_manual_regime_summary.csv',manual)
 local=['manifests/step4b_epoch_history.csv','manifests/step4b_runs.csv','manifests/step4b_metrics.csv','manifests/step4b_all200_diagnostic_metrics.csv','manifests/step4b_origin_cohorts.csv','manifests/step4b_manual_regime_metrics.csv']+[str(p.relative_to(R)) for p in sorted((R/'reports').glob('STEP4B_*.md'))]
 put('provenance/step4b_private_artifact_preservation.json',{'retained_locally':True,'detailed_artifacts_published':False,'artifacts':[{'file':p,'sha256':sha(R/p)} for p in local],'reason':'Automatic approval review restricted detailed per-fit/per-epoch research outputs, class supports and numeric Train thresholds; only multi-fit aggregates and hashes are public.'})
 put('provenance/step4b_preservation_public.json',{'old_file_count':len(before),'old_files_changed':0,'old100_reexecuted':False,'baseline_snapshot_sha256':sha(W/'before.json')})
 common='국민대학교 BIT전문대학원 KOSPI200 LNN STEP4B 회고적·탐색적 CPU Train/Validation 진단이다. A/B=BOTH_UNVERIFIED, historical18:00 KST production-PIT=BLOCKED다. Validation은 checkpoint 선택에 사용돼 독립 일반화 성능이 아니다. Seed를 독립 시장 표본으로 연결하지 않았으며 결과로 가격·모델·Seed·설정을 선택하지 않았다.'
 privacy='공개본은 여러 Seed의 집계와 비민감 해시만 포함한다. 개별 Seed/fit 성능·epoch 이력·클래스 support·실제 Train 분위수 임계값·상세 보고서와 그림은 로컬에 보존했다. 원본 가격·일별Target·확률·weights/checkpoint는 게시하지 않았다.'
 totals=f"기존100개 보존, 신규 완료{s['new_completed']}·실패{s['new_failed']}·BLOCKED{s['new_blocked']}, 실제 누적{s['total_actual_completed']}개다. STEP3D O3 재사용20개는 중복 집계하지 않았다. 사전95개·사후14개 검사PASS, 신규checkpoint100건 검증PASS, 기존1464파일 변경0이다. 신규2136확정epoch/97111확정optimizer updates다. 독립Test/HMM/GPU/Ensemble/외부피처/τactual/확증p값/2026 사용0이다."
 cols=['origin','candidate','model','completed_seeds','validation_BA_mean','validation_BA_std_ddof1','macro_f1_mean','macro_f1_std_ddof1','brier_mean','brier_std_ddof1']
 bodies={
 'STEP4B_100FIT_BASELINE_AUDIT_KO.md':totals+'\n\n기존100개 고유identity·완료·checkpoint/history/확률·입력/scaler/source/config/environment 해시를 대조했다. STEP3D alias20개 해시60건도 충돌0이다. 기존100개 재학습0이다.',
 'STEP4B_200FIT_RESULTS_KO.md':totals+'\n\n'+table(aggregate,cols),
 'STEP4B_SEED_STABILITY_KO.md':'각 Origin×가격×모델의4개Seed[2,12,22,32] 평균·표본표준편차(ddof1)다. 개별값·범위·best/total epoch는 로컬 상세보고서에 보존했다. 네Seed만으로 확증적 유의성·일반화 우위를 주장하지 않는다.\n\n'+table(aggregate,cols),
 'STEP4B_LTC_DIAGNOSTICS_KO.md':'Seed별 LTC 진단은5Origin×A/B의10개fit을 집계한 기술적 요약이다. 단일 클래스 예측은 수치 발산과 구분한다. 신규LTC20개 중 best 단일클래스 예측은2개다.\n\n'+table(ltc,list(ltc.columns))+'\n\n다른 네모델을 포함한4Seed 집계는 [모델 불안정성](../manifests/step4b_model_instability.csv)에 있다.',
 'STEP4B_PRICE_SENSITIVITY_KO.md':'같은Origin·모델의4개Seed 쌍에 대한 A/B차이 집계다. 출처·개정·historical가용성은 미확정이며 성능으로 주 가격을 고르지 않았다.\n\n'+table(prices,list(prices.columns)),
 'STEP4B_EXECUTION_AUDIT_KO.md':totals+f"\n\n실행 {m['started_at_kst']}~{m['finished_at_kst']}. 1건은 확정checkpoint에서 동일identity로 재개했고 완료83개를 건너뛰었다. 동결worker가 재개 시 최초epoch record flags를 초기화하는 한계는 중단 전 실제PASS 증거 해시와 별도 best checkpoint/RNG 감사로 검증했으며 flag나 학습코드를 조용히 수정하지 않았다. 각worker는 자기Origin의2020/2021/2022/2023/2024년말까지만 가격을 사용했다. 20세션horizon/window, Train20purge·Validation말단20UNKNOWN·Train-only scaler·Train q30/q70 유지. CPU2core/8GiB, worker≤2/LTC≤1/Torch1·FP32/AMP OFF. master flags=false.\n\nMaster SHA `{c['master_config_sha256']}`\n\nKernel SHA `{c['learning_kernel_sha256']}`\n\n전체config·개별fit/epoch 연구산출물·실제분위수/세부metadata 공개가 자동승인검토에서 거부돼 로컬에 보존하고 공개본을 다중fit집계·비민감해시로 축약했다.",
 'STEP4B_NEXT_GATES_KO.md':'누적200개 완료로 전체500개 계획 대비 잔여300개다. Seed42/52/62/72/82/92의300fit은 승인되지 않았고 자동실행하지 않는다. 독립Test/Ensemble/HMM/외부피처/τactual/확증분석도 미실행이며 별도증빙·승인이 필요하다. 가격은 성능이 아니라 공급처·정의·개정·가용성 증빙으로 선택해야 한다. 과거Origin Test연도가 후속Origin Validation으로 관찰된 구조이므로 전향적 미관측holdout이라고 주장하지 않는다.'}
 for name,body in bodies.items():
  p=P/'reports'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# '+name.removesuffix('_KO.md')+' 공개 집계 요약\n\n'+common+'\n\n'+body+'\n\n'+privacy+'\n');files.append(str(p.relative_to(P)))
 for p in sorted(R.rglob('*step4b*.py')):
  if not any(x in p.parts for x in ['data','originals','__pycache__']):copy(str(p.relative_to(R)))
 meta=[]
 for name in files:
  b=(P/name).read_bytes();meta.append({'file':name,'bytes':len(b),'git_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()})
 (W/'publish_metadata.json').write_text(json.dumps(meta));(W/'publication_source_root.txt').write_text(str(P));print(json.dumps({'public_files':len(meta),'public_bytes':sum(x['bytes'] for x in meta),'per_fit_epoch_data_published':False,'detailed_reports_local':True}))
if __name__=='__main__':main()
