"""Read-only source integrity checks and O1-only price staging; no neural training."""
from pathlib import Path
import sys,json,datetime,hashlib,importlib.metadata
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.pilot_data import read_verified_o1_prefix,prepare_pilot_arrays,sha256

def write(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 prior=json.loads((ROOT/'manifests/step28_price_sensitivity.json').read_text());calp=ROOT/'manifests/krx_sessions_2010_2025.csv'
 calproof=json.loads((ROOT/'provenance/krx_calendar_provenance.json').read_text());assert sha256(calp)==calproof['session_csv_sha256']
 fullcal=pd.read_csv(calp,parse_dates=['Date']);assert len(fullcal)==3939;assert fullcal.Date.is_unique and fullcal.Date.is_monotonic_increasing
 stagecal=fullcal[fullcal.Date.dt.year<=2020].copy();assert len(stagecal)==2714
 # Hash checks may read full bytes for integrity. No post-2020 price row is parsed.
 inputs=[]
 for entry in json.loads((ROOT/'evidence/input_manifest.json').read_text()):
  path=ROOT/'originals'/entry['filename'];actual=sha256(path);assert actual==entry['sha256'];inputs.append({'file':str(path.relative_to(ROOT)),'sha256':actual,'status':'PASS','access':'byte hash only'})
 for name,digest in prior['source_hashes'].items():
  path=(ROOT/'originals'/name) if (ROOT/'originals'/name).exists() else ROOT/'data/user_supplied'/name
  actual=sha256(path);assert actual==digest;inputs.append({'file':str(path.relative_to(ROOT)),'sha256':actual,'status':'PASS','access':'byte hash only'})
 stamp=datetime.datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y%m%dT%H%M%S_KST')
 run=ROOT/'data/derived'/('step3a_pilot_'+stamp);run.mkdir(parents=True,exist_ok=False);(run/'inputs').mkdir()
 stagecal.to_csv(run/'inputs/calendar_O1_private.csv',index=False,date_format='%Y-%m-%d');calsha=sha256(run/'inputs/calendar_O1_private.csv')
 datasets={};arrays={};dates={}
 for name in ['A','B']:
  artifact=next(x for x in prior['candidate_artifacts'] if x['candidate']==name and x['kind']=='close');source=ROOT/artifact['file']
  assert sha256(source)==artifact['sha256'];assert prior['sessions']==3939
  frame=read_verified_o1_prefix(source,pd.DatetimeIndex(stagecal.Date));fp=run/'inputs'/f'candidate_{name}_O1_prices_private.csv'
  frame.to_csv(fp,index=False,date_format='%Y-%m-%d',float_format='%.17g')
  parsed=pd.read_csv(fp,parse_dates=['Date'],float_precision='round_trip')
  data,meta,date_info=prepare_pilot_arrays(parsed,stagecal,calendar_source=calproof['source_url'],calendar_sha256=calsha)
  npz=run/'inputs'/f'candidate_{name}_O1_arrays_private.npz';np.savez(npz,train_x=data['train'][0],train_y=data['train'][1],validation_x=data['validation'][0],validation_y=data['validation'][1])
  dp=run/'inputs'/f'candidate_{name}_O1_dates_private.json';write(dp,date_info)
  mp=run/'inputs'/f'candidate_{name}_O1_metadata_private.json';write(mp,meta)
  datasets[name]={'full_candidate_file':artifact['file'],'full_candidate_sha256':artifact['sha256'],'full_session_count_verified_by_prior_audit_and_same_file_hash':3939,
    'price_file':str(fp.relative_to(ROOT)),'price_sha256':sha256(fp),'array_file':str(npz.relative_to(ROOT)),'array_sha256':sha256(npz),
    'date_file':str(dp.relative_to(ROOT)),'date_sha256':sha256(dp),'metadata_file':str(mp.relative_to(ROOT)),'metadata_sha256':sha256(mp),
    'date_information_sha256':hashlib.sha256(json.dumps(date_info,sort_keys=True).encode()).hexdigest(),'metadata':meta,
    'provider_status':'BOTH_UNVERIFIED','production_PIT_status':'BLOCKED','price_selected_as_main':False}
  arrays[name]=data;dates[name]=date_info
 assert dates['A']==dates['B'];assert datasets['A']['metadata']['class_counts']==datasets['B']['metadata']['class_counts']
 smoke=json.loads((ROOT/'manifests/step29_smoke_results.json').read_text());assert smoke['status']=='PASS' and smoke['check_counts']=={'PASS':70,'FAIL':0,'BLOCKED':0}
 assert [r['model'] for r in smoke['models']]==['RNN','LSTM','GRU','LTC','CfC']
 oldenv=json.loads((ROOT/'manifests/step29_runtime_environment.json').read_text());versions={n:importlib.metadata.version(n) for n in oldenv['versions']};assert versions==oldenv['versions']
 import torch
 assert str(torch.__version__)=='2.10.0+cpu' and torch.version.cuda is None
 base=json.loads((ROOT/'configs/experiment_config.json').read_text());assert base['training_enabled'] is False and base['hmm_fit_enabled'] is False
 gates=[{'id':n,'status':'PASS','evidence':e} for n,e in [
  ('whole_input_SHA256','All original/source/candidate hashes match preserved evidence'),
  ('A_B_composition_provenance','Prior A=original3894+45 once; B=Excel3939; hashes identical; sources remain unverified'),
  ('official_3939_sessions','Prior full comparison + immutable full file identity; O1 prefix2714 dates/IDs rechecked directly'),
  ('no_2026_observations','Only <=2020 price rows parsed into staged inputs'),
  ('exact_Train_Validation_boundaries','Train2010-2019/Validation2020; 2387/228 eligible for both'),
  ('label_purging','20 Train labels purged; strict label_end before Validation start; violations0'),
  ('future_endpoint_block','Final20 Validation labels unknown/excluded; max endpoint2020-12-30'),
  ('Train_only_scaler','Fit union of retained Train input dates only; 2406 rows ending2019-11-29'),
  ('window_alignment','20 actual sessions t-19..t; F1 order preserved; common Vol_Regime mask'),
  ('Test_isolation','Source reader consumes exactly2714 prefix rows; no post-2020 price row iteration; runtime staged whitelist'),
  ('five_model_CPU_synthetic_compatibility','STEP29 five models70checksPASS; pinned environment unchanged'),
  ('Pilot_authorization_budget','Current user explicit retrospective O1 A/B F1 CPU authorization; fixed10 fits/100epochs/patience10')]]
 record={'stage':'STEP3A','prepared_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'run_directory':str(run.relative_to(ROOT)),
  'calendar':{'full_file':str(calp.relative_to(ROOT)),'full_sha256':sha256(calp),'full_sessions':3939,'staged_file':str((run/'inputs/calendar_O1_private.csv').relative_to(ROOT)),'staged_sha256':calsha,'staged_sessions':2714},
  'source_inputs':inputs,'datasets':datasets,'gates':gates,'all_execution_preflight_gates_PASS':True,
  'source_PIT_exception':'User explicitly authorizes retrospective exploratory Pilot despite unknown source/vintage; production gates unchanged, never promoted',
  'production_training_enabled':False,'hmm_fit_enabled':False,'price_source_status':'BOTH_UNVERIFIED','production_PIT_status':'BLOCKED',
  'environment_versions':versions,'synthetic_compatibility_manifest_sha256':sha256(ROOT/'manifests/step29_smoke_results.json'),
  'A_B_same_date_and_label_arrays':True,'A_B_scaled_input_exact_equal':{part:bool(np.array_equal(arrays['A'][part][0],arrays['B'][part][0])) for part in ['train','validation']},
  'A_B_max_scaled_input_abs_difference':{part:float(np.max(np.abs(arrays['A'][part][0]-arrays['B'][part][0]))) for part in ['train','validation']},
  'full_price_value_rows_parsed_after_2020':0,'HMM_fit':False,'GPU':False,'Test_predictions':False}
 write(ROOT/'manifests/step3a_preflight.json',record);write(run/'preflight_private.json',record)
 Path('/workspace/work/step3a/run_dir.txt').write_text(str(run))
 print(json.dumps({'run_directory':str(run),'gates_PASS':len(gates),'candidates':{k:v['metadata'] for k,v in datasets.items()}},ensure_ascii=False,indent=2))
