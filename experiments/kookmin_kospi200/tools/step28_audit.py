"""STEP2.8 data sensitivity and preparation only. NEVER executes smoke/training/HMM."""
from pathlib import Path
import sys,json,hashlib,copy,datetime
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.data import Calendar
from kospi200.reconciliation import sha256,full_excel_comparison,validate_prices
from kospi200.price_sensitivity import compare_candidates,CONFLICT_DATES
CHECKED='2026-11-16'
def save(path,data):
 (ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def run():
 m=ROOT/'manifests';local=ROOT/'data/derived';sup=ROOT/'data/user_supplied';sp=m/'krx_sessions_2010_2025.csv'
 cp=json.loads((ROOT/'provenance/krx_calendar_provenance.json').read_text());assert sha256(sp)==cp['session_csv_sha256']
 s=pd.DatetimeIndex(pd.read_csv(sp,parse_dates=['Date']).Date,name='Date');cal=Calendar(s,cp['source_url'],sha256(sp),True)
 prior=json.loads((m/'step27_data_validation.json').read_text());full=sup/'KOSPI 200 종가.xlsx';assert sha256(full)==prior['full_excel_sha256']
 a=pd.read_csv(local/'kospi200_close_completed_2010_2025.csv',parse_dates=['Date'],float_precision='round_trip')[['Date','Close']]
 b=pd.read_excel(full,sheet_name='Sheet1',skiprows=16,header=None,names=['Date','Close','unused'])[['Date','Close']]
 b,_=validate_prices(b)
 original_file=ROOT/'originals/KOSPI_200.csv';original=pd.read_csv(original_file,parse_dates=['Date'],float_precision='round_trip')
 compare=full_excel_comparison(original[['Date','종가']].rename(columns={'종가':'Close'}),b,calendar=cal)
 material=compare[~compare.rounded_2dp_match];assert set(material.Date)==set(CONFLICT_DATES)
 # Reconcile to the preserved STEP2.7 private table before writing new audit files.
 old=pd.read_csv(local/'step27_price_conflicts_private.csv',parse_dates=['Date'],float_precision='round_trip')
 old2=old[old.Date.isin(CONFLICT_DATES)].set_index('Date')
 assert np.array_equal(old2.reindex(material.Date).Close_original.to_numpy(),material.Close_original.to_numpy())
 assert np.array_equal(old2.reindex(material.Date).Close_excel.to_numpy(),material.Close_excel.to_numpy())
 focused=material[['Date','Close_original','Close_excel']].copy()
 focused['absolute_difference']=(focused.Close_excel-focused.Close_original).abs()
 focused['relative_difference_original_denominator']=focused.absolute_difference/focused.Close_original.abs()
 focused['relative_difference_percent']=focused.relative_difference_original_denominator*100
 focused['rounded_2dp_absolute_difference']=(focused.Close_excel.round(2)-focused.Close_original.round(2)).abs()
 focused['excel_claimed_index_code']='I.101 / I31000040F';focused['unit']='index points (Excel claim; original upstream unverified)'
 focused['confirmed_supplier']='UNKNOWN';focused['official_price_match']='UNKNOWN_BLOCKED_HTTP_403'
 focused['original_sha256']=sha256(original_file);focused['excel_sha256']=sha256(full)
 focused['original_source']='user KOSPI_200.csv';focused['excel_source']='user KOSPI 200 종가.xlsx'
 focused.to_csv(local/'step28_two_price_conflicts_private.csv',index=False,float_format='%.17g')
 remaining=compare[compare.rounded_2dp_match].copy()
 roundtrip=remaining.Close_original.to_numpy()==remaining.Close_excel.to_numpy(dtype=np.float32).astype(np.float64)
 assert roundtrip.all()
 sensitivity,sa,sb=compare_candidates(a,b,cal)
 # Attribution diagnostics only; neither scenario is selected for analysis.
 two=a.copy();two.loc[two.Date.isin(CONFLICT_DATES),'Close']=b.set_index('Date').Close.reindex(two.loc[two.Date.isin(CONFLICT_DATES),'Date']).to_numpy()
 precision=a.copy();mask=~precision.Date.isin(CONFLICT_DATES);precision.loc[mask,'Close']=b.set_index('Date').Close.reindex(precision.loc[mask,'Date']).to_numpy()
 two_effect,_,_=compare_candidates(a,two,cal);precision_effect,_,_=compare_candidates(a,precision,cal)
 sensitivity['attribution']={'two_conflict_dates_only':two_effect,'other_dates_precision_only':precision_effect,
   'warning':'Effects may interact; do not assume arithmetic additivity of thresholds/labels. No source choice from model performance.'}
 sensitivity['price_comparison']={'common_dates':3894,'exact_matches':int(compare.exact_match.sum()),
  'within_1e_minus9_matches':int(compare.within_1e_minus9.sum()),'rounded_2dp_matches':3892,
  'remaining_dates_float32_roundtrip_matches':int(roundtrip.sum()),'remaining_exact_matches':int(remaining.exact_match.sum()),
  'remaining_precision_only_differences':int((~remaining.exact_match).sum()),'material_conflict_dates':['2021-04-23','2021-05-06'],
  'precision_interpretation':'All other common values equal float64(float32(Excel)); compatible with float32 representation, not proof of original processing history',
  'material_cause':'UNKNOWN; not explained by float32 roundtrip; source/revision/misrecording not distinguished'}
 # Explicitly separate and retain candidates locally; never overwrite prior series.
 artifacts=[]
 for name,frame,state in [('A',a,sa),('B',b,sb)]:
  for kind,data in [('close',frame),('targets',state['labels'].drop(columns='Close').reset_index()),('features',state['features'].reset_index())]:
   path=local/f'step28_candidate_{name}_{kind}_private.csv';data.to_csv(path,index=False,na_rep='UNKNOWN',float_format='%.17g');artifacts.append({'candidate':name,'kind':kind,'file':str(path.relative_to(ROOT)),'sha256':sha256(path),'publication':'LOCAL_ONLY'})
 sensitivity.update({'checked_date':CHECKED,'period':['2010-01-01','2025-12-31'],'candidate_definitions':{'A':'Preserved original 3894 closes + supplied missing 45 once','B':'Full Excel 3939 closes'},'source_hashes':prior['source_hashes'],
                     'candidate_artifacts':artifacts,'private_detail_file':'data/derived/step28_two_price_conflicts_private.csv',
                     'private_report_file':'data/derived/STEP28_PRICE_CONFLICT_PRIVATE_KO.md','raw_prices_published':False,'final_data_status':'BLOCKED_PRICE_SOURCE_NOT_SELECTED',
                     'cause_of_label_differences_step26_vs_original':'47 horizon-correction changes, distinct from current A-vs-B comparison',
                     'last_valid_base':'2025-12-01','last_label_end':'2025-12-30','training_enabled':False,'hmm_fit_enabled':False})
 save('manifests/step28_price_sensitivity.json',sensitivity)
 # Official access is evidence of failure only, never an official-price match.
 attempts=json.loads(Path('/workspace/work/step28/official_access.json').read_text())
 for row in attempts:row.pop('body_preview',None)
 timing={'url':'https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp','checked_date':CHECKED,'access_method':'web tool page open',
  'web_snapshot_sha256':sha256(Path('/workspace/work/step28/web_evidence_private.json')),
  'snapshot_hash_scope':'Local saved web tool result bundle, NOT origin HTML bytes',
  'current_page_summary':'KRX EOD first distribution 16:00, second 18:10',
  'limitation':'Current product-level schedule cannot certify either unidentified supplier historical availability at 18:00. No zero provider delay assumed.',
  'direct_http_snapshot_attempt':json.loads(Path('/workspace/work/step28/timing_evidence.json').read_text())}
 save('provenance/step28_source_checks.json',{'checked_date':CHECKED,'official_price_attempts':attempts,'official_prices_retrieved':0,
  'verified_supplier_for_A':None,'verified_supplier_for_B':None,'timing_evidence':timing,'official_crosscheck_status':'BLOCKED',
  'alternative_access':'Authorized KRX price export / approved KRX OpenAPI access; authenticated supplier vintage/revision documentation',
  'search_check':'Public searches of both exact dates and values found no usable authenticated closing-price evidence; search snippets were not accepted as price verification'})
 base=json.loads((ROOT/'configs/experiment_config.json').read_text())
 defs=json.loads((ROOT/'provenance/step27_notebook_source_references.json').read_text())['definition_bundles']
 source=next(d for d in defs if '10개' in d['notebook'])
 cfg={'stage':'STEP2.8_PREPARED_NOT_EXECUTED','training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,'device':'cpu',
      'origin':'O1','seed':2,'feature_spec':'F1','models':base['models'],'channels':['RAW','LOG'],'features':{'RAW':['Log_Ret','Disparity'],'LOG':['Log_Ret','Disparity']},
      'model_settings':base['model'],'seed_offsets':base['seed_offsets'],'prediction_contract':{'time':'18:00','timezone':'Asia/Seoul','include_t':True},
      'eligibility_policy':'STEP27 common local-feature 20-window mask; F1 inputs remain two domestic features only',
      'train_batches':1,'validation_batches':1,'reproducibility_repetitions':2,'planned_model_channel_cases':10,'planned_training_batch_steps_including_repetition':20,
      'test_access':False,'selected_candidate':None,'selected_price_sha256':None,'calendar_sha256':sha256(sp),'source_notebook_sha256':source['notebook_sha256'],
      'original_definition_hashes':{k:v['sha256'] for k,v in source['definitions'].items() if k in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']},
      'runtime_versions':{'torch':'2.10.0+cpu','ncps':'1.0.1'},'optional_hmm_runtime_reference':{'hmmlearn':'0.3.3'},
      'approval_required':{'scope':'STEP3_F1_O1_SEED2_CPU_SMOKE_ONLY','approved_by':'user','bind':['config_sha256','gates_sha256']},
      'checkpoint_policy':'New ignored local derived directory; weights_only load; exact model/optimizer/scheduler and validation-logit roundtrip',
      'manual_regime':{'variable':'Vol_Regime','definition':'Log_Ret.rolling(40).std(ddof=1)','quantiles':[30,70],'method':'linear','reference':'retained Train dates, STEP27 common local-feature-window policy','validation_test_refit':False,'single_class_BA_MacroF1':None},
      'hmm_plan':base['hmm'],'external_feature_blocks_are_F1_prerequisites':False,'historical_checkpoint_compatibility_required_for_new_F1_training':False,
      'original_loss_semantics':'alpha globally multiplies Focal CE, not alpha_t class weighting','protocol_change_requires_new_version':True}
 save('configs/step28_smoke_config.json',cfg)
 gates={'checked_date':CHECKED,'F1_overall_status':'BLOCKED','STEP3_smoke_status':'BLOCKED','training_enabled':False,'hmm_fit_enabled':False,
  'mandatory_A':{'final_price_source':{'status':'BLOCKED','selected_candidate':None,'reason':'A/B have same labels but unverified source/revisions; source must be selected before training'},
   'calendar_labels':{'status':'PASS','reason':'Both 3939 sessions,3919known/20UNKNOWN,20-session labels,purging,Train-only scaler verified as diagnostics'},
   'domestic_input_time_contract':{'status':'BLOCKED','reason':'Neither unidentified supplier has historical 18:00 availability/revision evidence'},
   'model_library_compatibility':{'status':'PARTIAL','reason':'Installation/import/source signatures PASS; construction/forward/backward/checkpoint smoke never executed'},
   'protocol_frozen':{'status':'PASS','reason':'STEP2.8 versioned specification and implementation hash snapshot; price choice pending, flags false'}},
  'extensions_B':{'Foreign_Net_source':{'status':'BLOCKED'},'Nasdaq_SOX_PIT':{'status':'BLOCKED'},'full_5feature_experiment':{'status':'BLOCKED'},'full_feature_ablation':{'status':'BLOCKED'},'LTC_tau_actual_forward':{'status':'BLOCKED'},
                  'historical_ncps_hmmlearn_checkpoint_reproduction':{'status':'BLOCKED','reason':'Not required to claim a separately preregistered new F1 candidate-environment experiment; historical equivalence cannot be claimed'}},
  'separate_execution_approval':{'status':'BLOCKED','scope':'STEP3_F1_O1_SEED2_CPU_SMOKE_ONLY','reason':'STEP2.8 authorizes code/data audit only'},
  'F1_does_not_require_extension_B':True,'HMM_fit_executed':False,'model_forward_executed':False,'checkpoint_loaded':False,
  'GPU_executed':False,'models_trained':0,'new_model_performance_generated':False,'2026_market_observations_used':0}
 save('manifests/step28_gate_results.json',gates)
 freeze_paths=['runtime/step28_smoke_runtime.py','src/kospi200/price_sensitivity.py','src/kospi200/paired_regime_evaluation.py','src/kospi200/manual_evaluation.py','src/kospi200/regimes.py','tools/step28_smoke.py']
 save('manifests/step28_protocol_freeze.json',{'checked_date':CHECKED,'status':'PASS_VERSIONED_SPECIFICATION_ONLY','parent_protocol':'reports/PROTOCOL_KO.md','parent_protocol_sha256':sha256(ROOT/'reports/PROTOCOL_KO.md'),
  'config_file':'configs/step28_smoke_config.json','config_sha256':sha256(ROOT/'configs/step28_smoke_config.json'),
  'implementation_artifacts':[{'file':p,'sha256':sha256(ROOT/p)} for p in freeze_paths],'final_price_selected':False,'execution_authorized':False})
 before=json.loads(Path('/workspace/work/step28/before.json').read_text());protected=[]
 for name,oldhash in before.items():
  if name in ['README.md','CHANGELOG.md']:continue
  newhash=sha256(ROOT/name);protected.append({'file':name,'before_sha256':oldhash,'after_sha256':newhash,'status':'PASS' if oldhash==newhash else 'FAIL'})
 assert all(p['status']=='PASS' for p in protected)
 save('provenance/step28_preservation.json',{'checked_date':CHECKED,'all_unchanged':True,'artifacts':protected,'reviewed_reports':json.loads(Path('/workspace/work/step28/review.json').read_text())})
 # Actual two-date numbers go only to this ignored local report.
 lines=['# STEP2.8 비공개 종가 충돌 수치','확인일2026-11-16. 라이선스 미확인: 공개 GitHub 게시 금지.',
  '|Date|기존 종가|신규 종가|절대 차이|상대 차이(기존분모)|상대 차이 %|소수2자리 절대 차이|',
  '|---|---:|---:|---:|---:|---:|---:|']
 for _,row in focused.iterrows():lines.append('|'+str(row.Date.date())+'|'+'|'.join(format(float(row[k]),'.17g') for k in ['Close_original','Close_excel','absolute_difference','relative_difference_original_denominator','relative_difference_percent','rounded_2dp_absolute_difference'])+'|')
 lines+=['','Excel 식별자 I.101/I31000040F, 단위 종가지수(포인트)는 파일 내 주장. 기존 CSV의 원천코드는 UNKNOWN. 공급처 양쪽 UNKNOWN. 공식가격 일치 UNKNOWN(BLOCKED_HTTP_403). 두 건은float32표현만으로 설명되지 않으며 기록오류/공급처개정/다른지수정의를 판별할 증거가 없다.','기존SHA256 '+sha256(original_file),'ExcelSHA256 '+sha256(full),'공식조회URL https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd','공개 집계 보고서 reports/STEP28_PRICE_CONFLICT_KO.md 참조.']
 (local/'STEP28_PRICE_CONFLICT_PRIVATE_KO.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'known_labels_A_B':[sensitivity['known_labels_A'],sensitivity['known_labels_B']],'label_differences':sensitivity['known_label_differences'],'label_end_differences':sensitivity['label_end_differences'],'features':sensitivity['features'],'thresholds':sensitivity['manual_thresholds'],'prior_artifacts_unchanged':len(protected)},ensure_ascii=False,indent=2))
if __name__=='__main__':run()
