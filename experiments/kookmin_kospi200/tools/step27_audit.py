"""STEP2.7 data-only audit. No notebook execution, model import, fit or GPU."""
from pathlib import Path
import sys,json,hashlib,ast,re,importlib.metadata as metadata,platform
import pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.data import Calendar
from kospi200.reconciliation import validate_prices,reconcile_close,full_excel_comparison,label_audit,sha256
from kospi200.folds import rolling_origins,window_dates
from kospi200.smoke_preparation import extract_original_definitions,static_parameter_count,smoke_plan
CHECKED='2026-11-16'
def save(path,value):
 (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def run():
 m=ROOT/'manifests';private=ROOT/'data/derived';sup=ROOT/'data/user_supplied'
 full=sup/'KOSPI 200 종가.xlsx'
 if not full.is_file():raise RuntimeError('BLOCKED_FULL_EXCEL_MISSING')
 import openpyxl
 w=openpyxl.load_workbook(full,read_only=True,data_only=False);s=w['Sheet1']
 metadata_claims={str(s.cell(i,1).value):s.cell(i,2).value for i in range(3,17)}
 if s.cell(12,2).value!='코스피 200' or s.cell(15,2).value!='종가지수(포인트)':raise RuntimeError('Unexpected index/item')
 raw=pd.DataFrame(s.iter_rows(min_row=17,max_col=2,values_only=True),columns=['Date','Close']);w.close()
 new,quality=validate_prices(raw)
 sp=m/'krx_sessions_2010_2025.csv';cp=json.loads((ROOT/'provenance/krx_calendar_provenance.json').read_text());assert sha256(sp)==cp['session_csv_sha256']
 sessions=pd.DatetimeIndex(pd.read_csv(sp,parse_dates=['Date']).Date,name='Date');cal=Calendar(sessions,cp['source_url'],sha256(sp),True)
 original_path=ROOT/'originals/KOSPI_200.csv';original=pd.read_csv(original_path,float_precision='round_trip').rename(columns={'종가':'Close'})[['Date','Close']]
 csv=sup/'KOSPI200_누락45일_종가_보완.csv';xlsx=sup/'KOSPI200_누락45일_종가_보완.xlsx';supp=pd.read_csv(csv,float_precision='round_trip');sx=pd.read_excel(xlsx,sheet_name='누락 45일').rename(columns={'날짜 (Date)':'Date','KOSPI 200 종가':'Close'})[['Date','Close']]
 expected=pd.read_csv(m/'kospi_missing_dates_audit.csv',parse_dates=['date']).date
 completed,integrity=reconcile_close(original,supp,sx,calendar=cal,expected_missing=expected,original_file=original_path.name,supplement_file=csv.name,original_sha256=sha256(original_path),supplement_sha256=sha256(csv))
 cmp=full_excel_comparison(original,raw,calendar=cal);conflicts=cmp[~cmp.exact_match].copy()
 conflicts['original_source_file']=original_path.name;conflicts['new_source_file']=full.name
 conflicts['original_source_sha256']=sha256(original_path);conflicts['new_source_sha256']=sha256(full)
 conflicts['source_url']='UNKNOWN_USER_ATTACHMENT';conflicts['verification_level']='USER_SUPPLIED_CONFLICT_UNRESOLVED'
 conflicts.to_csv(private/'step27_price_conflicts_private.csv',index=False,float_format='%.17g')
 public=conflicts.drop(columns=['Close_original','Close_excel','difference']).copy()
 public.to_csv(m/'step27_price_conflicts.csv',index=False)
 supplement_match=validate_prices(supp)[0].set_index('Date').Close.eq(new.set_index('Date').Close.reindex(pd.to_datetime(supp.Date))).sum()
 # Diagnose preserved STEP2.6 candidate values only; unresolved conflicts prevent finalization.
 labels,features,window,differences,summary=label_audit(original,completed,cal)
 changed=differences[differences.Target_changed.fillna(False)].copy()
 assert len(changed)==47 and changed.horizon_date_changed.all()
 changed.to_csv(private/'step27_label_change_causes_private.csv',index=False,na_rep='UNKNOWN')
 folds,selected=rolling_origins(labels,cal,window)
 for i,row in folds.iterrows():
  dates=selected[row.origin][row.partition];y=labels.loc[dates,'Target'].astype(int);rows=labels.loc[row.boundary_start:row.boundary_end];eligible=rows.Target.notna()&window.reindex(rows.index)
  ws=window_dates(sessions,dates,window=20,include_t=True)
  violations=sum(int(v.max()>t or len(v)!=20) for t,v in ws.items())
  folds.loc[i,'window_eligible_before_purge']=int(eligible.sum());folds.loc[i,'up_samples']=int(y.eq(1).sum());folds.loc[i,'down_or_equal_samples']=int(y.eq(0).sum());folds.loc[i,'up_ratio']=float(y.mean())
  folds.loc[i,'min_label_end']=str(labels.loc[dates,'label_end'].min().date());folds.loc[i,'max_label_end']=str(labels.loc[dates,'label_end'].max().date())
  folds.loc[i,'window_future_or_length_violations']=violations
  folds.loc[i,'label_end_cutoff_violations']=int(labels.loc[dates,'label_end'].ge(pd.Timestamp(row.next_cutoff)).sum()) if row.next_cutoff else 0
 folds=folds.rename(columns={'eligible_samples':'provisional_structural_samples'})
 for col in ['final_confirmed_samples','domestic_PIT_verified_samples','external_5feature_PIT_verified_samples']:folds[col]=None
 f1ready=features[['Log_Ret','Disparity']].notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20)
 f1folds,_=rolling_origins(labels,cal,f1ready)
 folds['F1_input_only_provisional_samples']=f1folds.eligible_samples
 folds['status']='BLOCKED_UNRESOLVED_PRICE_CONFLICT_AND_PIT';folds.to_csv(m/'step27_origin_manifest.csv',index=False)
 # Static notebook extraction and historical output preservation.
 history=[];perseed=[];source_refs=[];bundles=[]
 for path in sorted((ROOT/'originals').glob('*.ipynb')):
  tag='10seed' if '10개' in path.name else '5seed' if '5개' in path.name else 'single';nb=json.loads(path.read_text());seeds=None
  for node in ast.parse(''.join(nb['cells'][4]['source'])).body:
   if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEEDS' for t in node.targets):seeds=ast.literal_eval(node.value)
  defs=extract_original_definitions(nb)
  (private/f'step27_{tag}_original_definitions_private.py').write_text('\n\n'.join(v['source'] for v in defs.values()))
  bundles.append({'notebook':path.name,'notebook_sha256':sha256(path),'definitions':{k:{a:b for a,b in v.items() if a!='source'} for k,v in defs.items()}})
  for cellno in [6,8,9,11,12,14,15,16,17]:
   text=''.join(nb['cells'][cellno-1]['source']);matches=[]
   for lineno,line in enumerate(text.splitlines(),1):
    if any(k in line for k in ['test_vol =','low_threshold =','high_threshold =','manual_mask_','calculate_metrics(','balanced_accuracy_score(','mean_mets =','seed_metrics =','regime_agg[','REGIME_NAMES','Vol_Regime\'] =']):matches.append({'line':lineno,'text':line.strip()})
   source_refs.append({'notebook':tag,'cell':cellno,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'selected_lines':matches})
  for cellno,kind in [(16,'manual'),(17,'hmm')]:
   cell=nb['cells'][cellno-1];out=''
   for o in cell.get('outputs',[]):
    v=o.get('text',o.get('data',{}).get('text/plain',[]));out+=''.join(v) if isinstance(v,list) else v
   regime=None
   for line in out.splitlines():
    hit=re.search(r'\[Regime: (\w+)\]',line) if kind=='manual' else re.search(r'\[HMM State (\d+)\]',line)
    if hit:regime=hit.group(1) if kind=='manual' else 'HMM_'+hit.group(1)
    parts=line.split()
    if regime and len(parts)>=7:
     try:values=[float(x) for x in parts[-6:]]
     except ValueError:continue
     model=' '.join(parts[:-6]);rec={'notebook':tag,'source_notebook_sha256':sha256(path),'source_cell':cellno,'regime_type':kind,'regime':regime,'model':model,'seed_scope':str(seeds[0]) if len(seeds)==1 else 'MEAN_OF_'+str(len(seeds))+'_SEEDS',**dict(zip(['accuracy','balanced_accuracy','recall_positive','precision_positive','macro_f1','f1_positive'],values)),'status':'HISTORICAL_STORED_OUTPUT_ONLY','source_output_sha256':hashlib.sha256(out.encode()).hexdigest()}
     history.append(rec)
     for seed in seeds:
      perseed.append({'notebook':tag,'regime_type':kind,'regime':regime,'model':model,'seed':seed,'balanced_accuracy':values[1] if len(seeds)==1 else None,'status':'HISTORICAL_STORED_SINGLE_SEED' if len(seeds)==1 else 'BLOCKED_PER_SEED_OUTPUT_NOT_STORED'})
 hist=pd.DataFrame(history);ps=pd.DataFrame(perseed)
 for kind in ['manual','hmm']:
  hist[hist.regime_type==kind].to_csv(m/f'step27_historical_{kind}_metrics.csv',index=False)
  ps[ps.regime_type==kind].to_csv(m/f'step27_historical_{kind}_per_seed.csv',index=False)
 save('provenance/step27_notebook_source_references.json',{'checked_date':CHECKED,'cell_numbering':'actual notebook cells 1-based, not comment numbers','references':source_refs,'definition_bundles':bundles,'historical_outputs_executed':False})
 config=json.loads((ROOT/'configs/experiment_config.json').read_text());packages={}
 for name in ['torch','ncps','hmmlearn','numpy','pandas','scikit-learn']:
  try:packages[name]=metadata.version(name)
  except metadata.PackageNotFoundError:packages[name]=None
 params=[]
 for model in config['models']:
  for channel,n in [('F0_RAW',5),('LOG',2),('F1_RAW',2)]:params.append({'model':model,'channel':channel,'input_size':n,**static_parameter_count(model,n)})
 env_path=ROOT/'provenance/step27_isolated_environment.json'
 isolated=json.loads(env_path.read_text()) if env_path.exists() else None
 runtime={'isolated_environment':isolated,'checked_date':CHECKED,'python':platform.python_version(),'installed_metadata_only':packages,'model_imports':False,'model_construction':False,'GPU_query':False,'status':'BLOCKED','reason':'Original ncps/hmmlearn versions and checkpoint compatibility unknown; runtime model validation not executed. See isolated_environment for installation/import evidence','static_parameter_counts':params,'ncps_reference_version':'1.0.1','ncps_reference_wheel_sha256':'249b2a62c38608df62d454fe20f4e880f74c27ef97ea3a45e101d47b1b273fb5','parameter_count_limitation':'LTC/CfC counts are reference formulas, not original runtime proof. LTC total includes fixed registered masks.','source_urls':['https://pytorch.org/docs/stable/generated/torch.nn.RNN.html','https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html','https://pytorch.org/docs/stable/generated/torch.nn.GRU.html','https://pypi.org/pypi/ncps/1.0.1/json','https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py'],'wrapper_implicit_positive_constraints':True,'direct_cell_default':False,'physical_dt_unit':None,'solver_substeps':6}
 save('manifests/step27_model_environment.json',runtime)
 gates={'data_validation':'BLOCKED','input_time_contract':'BLOCKED','label_purging':'PASS','full_excel_comparison':'PASS','model_environment':'BLOCKED','protocol_frozen':'PASS','explicit_step3_execution_approval':'BLOCKED'}
 plan=smoke_plan(config,gates);plan['manual_regime']={'reference_partition':'train','quantiles':[30,70],'method':'linear','test_recalculation_allowed':False,'single_class_metrics':'BA/MacroF1 null; support and available-class recall reported','HMM_table_separate':True};plan['source_notebook_sha256']=next(b['notebook_sha256'] for b in bundles if '10개' in b['notebook']);plan['original_definition_manifest']='provenance/step27_notebook_source_references.json';plan['seed_offsets']=config['seed_offsets'];plan['original_focal_loss_semantics']='alpha globally multiplies focal CE, not class-dependent alpha_t';plan['future_gpu_conditions']=['Separate explicit execution approval','All mandatory evidence gates PASS','Pinned torch/CUDA/ncps versions and device identity','FP32 AMP disabled; no silent CPU/GPU substitution','Record determinism and CUBLAS setup before process launch'];save('configs/step27_smoke_config.json',plan)
 freeze_files=['configs/experiment_config.json','configs/step27_smoke_config.json','reports/PROTOCOL_KO.md','src/kospi200/manual_evaluation.py','src/kospi200/smoke_preparation.py']
 save('manifests/step27_protocol_freeze.json',{'checked_date':CHECKED,'status':'PASS_SPECIFICATION_SNAPSHOT_ONLY','execution_permission':False,'artifacts':[{'file':p,'sha256':sha256(ROOT/p)} for p in freeze_files],'change_policy':'Any future specification change gets a new version and reason; no Test-outcome tuning'})
 out={'stage':'STEP2.7','checked_date':CHECKED,'baseline_commit':'f38f8a45ce2f60a2cc7fbecc80d9ab76464d597e','full_excel_exists':True,'full_excel_sha256':sha256(full),'full_excel_quality':quality,'full_excel_metadata_claims':metadata_claims,'column_mapping':'Sheet1 A17:A3955 Date, B17:B3955 Close; index name is metadata B12, item B15','official_sessions':len(sessions),'full_calendar_exact_match':pd.DatetimeIndex(new.Date).equals(sessions),'calendar_provenance':'provenance/krx_calendar_provenance.json','comparison':{'common_dates':len(cmp),'exact_matches':int(cmp.exact_match.sum()),'within_1e_minus9_matches':int(cmp.within_1e_minus9.sum()),'rounded_2dp_matches':int(cmp.rounded_2dp_match.sum()),'numeric_difference_rows':len(conflicts),'rounded_2dp_conflict_dates':cmp.loc[~cmp.rounded_2dp_match,'Date'].dt.strftime('%Y-%m-%d').tolist(),'max_absolute_difference':float(cmp.difference.abs().max()),'status':'PASS_COMPARISON_EXECUTED_CONFLICTS_UNRESOLVED'},'supplement_45_exact_matches_full_excel':int(supplement_match),'integrity':integrity,'provisional_label_audit':summary,'label_change_cause':{'changes':47,'all_have_different_horizon_end':True,'down_to_up':21,'up_to_down':26,'original_common_prices_modified':0,'cause':'Missing sessions restored, shifting endpoints from observed-row+20 to official session_id+20; no price substitution','comparison_scope':'Cutoff-first diagnostic; not reexecution of historical results'},'final_data_status':'BLOCKED_UNRESOLVED_PRICE_CONFLICT','confirmed_final_samples':None,'provisional_derived_written':False,'prior_candidate_series_preserved':True,'F1_input_only_provisional_known_windows':int((f1ready&labels.Target.notna()).sum()),'F1_with_manual_volatility_provisional_known_windows':int((window&labels.Target.notna()).sum()),'external_feature_PIT_status':'BLOCKED','F1_domestic_only_status':'BLOCKED_PRICE_PROVENANCE_AND_18KST_AVAILABILITY','smoke_gates':gates,'STEP3_smoke_ready':False,'training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,'source_url':None,'source':'User attachments; supplier/extraction/revision policy unverified','price_verification_level':'USER_SUPPLIED_NOT_KRX_OFFICIAL_VERIFIED','price_conflict_policy':'No predeclared authorized tie-breaker; no source selected as truth; preserve prior candidate values; never finalize unresolved data','source_hashes':{p.name:sha256(p) for p in [original_path,full,csv,xlsx]},'raw_private_publication_allowed':False,'2026_prices_used':0,'historical_manual_metric_rows':int((hist.regime_type=='manual').sum()),'historical_hmm_metric_rows':int((hist.regime_type=='hmm').sum()),'manual_per_seed_missing_rows':int(((ps.regime_type=='manual')&ps.status.str.startswith('BLOCKED')).sum())}
 save('manifests/step27_data_validation.json',out)
 # Prior reports, code, original inputs and derived candidate series are immutable.
 before=json.loads(Path('/workspace/work/step27/before.json').read_text());preserved=[]
 for name,digest in before.items():
  if name in ['README.md','CHANGELOG.md']:continue
  p=ROOT/name;actual=sha256(p) if p.exists() else None
  preserved.append({'file':name,'before_sha256':digest,'after_sha256':actual,'status':'PASS' if actual==digest else 'FAIL'})
 assert all(p['status']=='PASS' for p in preserved),'Prior artifact changed'
 save('provenance/step27_preservation.json',{'checked_date':CHECKED,'prior_artifacts':preserved,'all_unchanged':True,'raw_prices_and_source_bundles':'LOCAL_ONLY','license_status':'BLOCKED','no_new_model_performance_generated':True})
 print(json.dumps({'excel_rows':len(new),'numeric_conflicts':len(conflicts),'two_decimal_conflicts':out['comparison']['rounded_2dp_conflict_dates'],'manual_rows':out['historical_manual_metric_rows'],'hmm_rows':out['historical_hmm_metric_rows'],'missing_manual_seed_rows':out['manual_per_seed_missing_rows'],'preserved_artifacts':len(preserved)},ensure_ascii=False))
if __name__=='__main__':run()
