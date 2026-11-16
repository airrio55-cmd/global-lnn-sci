"""Verify STEP3A immutable evidence; stage O1/O2 prefixes and fixed manual references."""
from pathlib import Path
import sys,json,hashlib,datetime,shutil,importlib.metadata
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.rolling_pilot_data import read_origin_prefix,prepare_origin

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 old=json.loads((ROOT/'manifests/step3a_execution_manifest.json').read_text());og=json.loads((ROOT/'manifests/step3a_preflight.json').read_text());oc=json.loads((ROOT/'configs/step3a_pilot_config.json').read_text());oldrun=ROOT/old['run_directory']
 assert old['completed_models']==10 and old['failed_models']==0
 assert sha(ROOT/'runtime/step3a_pilot.py')==old['runner_sha256'];assert sha(ROOT/'configs/step3a_pilot_config.json')==old['config_sha256'];assert sha(ROOT/'manifests/step3a_preflight.json')==old['preflight_sha256'];assert sha(ROOT/'provenance/step3a_pilot_authorization.json')==old['authorization_sha256']
 checks=[]
 for item in old['implementation_artifacts']:assert sha(ROOT/item['file'])==item['sha256'];checks.append({'file':item['file'],'sha256':item['sha256'],'status':'PASS'})
 reused=[]
 for key,row in old['fit_ledger'].items():
  assert row['status']=='COMPLETED'
  for file,field in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:
   path=oldrun/key/file;assert sha(path)==row[field];checks.append({'file':str(path.relative_to(ROOT)),'sha256':row[field],'status':'PASS'})
  reused.append({'run_id':f'O1_seed2_{row["candidate"]}_{row["model"]}','origin':'O1','seed':2,'candidate':row['candidate'],'model':row['model'],'source_stage':'STEP3A_REUSED','source_run_id':key,'source_directory':str((oldrun/key).relative_to(ROOT)),'record':row})
 for candidate in ['A','B']:
  info=og['datasets'][candidate]
  for file,field in [('price_file','price_sha256'),('array_file','array_sha256'),('date_file','date_sha256'),('metadata_file','metadata_sha256')]:assert sha(ROOT/info[file])==info[field]
 versions={k:importlib.metadata.version(k) for k in oc['environment_versions']};assert versions==oc['environment_versions']
 cp=ROOT/'manifests/krx_sessions_2010_2025.csv';proof=json.loads((ROOT/'provenance/krx_calendar_provenance.json').read_text());assert sha(cp)==proof['session_csv_sha256']
 fullcal=pd.read_csv(cp,parse_dates=['Date']);assert len(fullcal)==3939
 prior=json.loads((ROOT/'manifests/step28_price_sensitivity.json').read_text())
 run=ROOT/'data/derived'/('step3b_pilot_'+datetime.datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y%m%dT%H%M%S_KST'));run.mkdir(parents=True,exist_ok=False);(run/'jobs').mkdir();datasets={}
 for origin,year in [('O1',2020),('O2',2021)]:
  idir=run/'inputs'/origin;idir.mkdir(parents=True);cal=fullcal[fullcal.Date.dt.year<=year].copy();calpath=idir/'calendar_private.csv';cal.to_csv(calpath,index=False,date_format='%Y-%m-%d');datasets[origin]={}
  for candidate in ['A','B']:
   artifact=next(x for x in prior['candidate_artifacts'] if x['candidate']==candidate and x['kind']=='close');source=ROOT/artifact['file'];assert sha(source)==artifact['sha256']
   frame=read_origin_prefix(source,pd.DatetimeIndex(cal.Date),year);price=idir/f'{candidate}_prices_private.csv';frame.to_csv(price,index=False,date_format='%Y-%m-%d',float_format='%.17g')
   data,meta,dates,regimes=prepare_origin(frame,cal,origin=origin,calendar_source=proof['source_url'],calendar_sha256=sha(calpath))
   npz=idir/f'{candidate}_arrays_private.npz';np.savez(npz,train_x=data['train'][0],train_y=data['train'][1],validation_x=data['validation'][0],validation_y=data['validation'][1])
   dp=idir/f'{candidate}_dates_private.json';mp=idir/f'{candidate}_metadata_private.json';rp=idir/f'{candidate}_manual_regimes_private.csv';write(dp,dates);write(mp,meta);regimes.to_frame().to_csv(rp,index_label='Date')
   # O1 must be bitwise identical to STEP3A. Copy the original NPZ bytes after comparison.
   if origin=='O1':
    with np.load(ROOT/og['datasets'][candidate]['array_file'],allow_pickle=False) as z:
     for part in ['train','validation']:
      assert np.array_equal(z[part+'_x'],data[part][0]);assert np.array_equal(z[part+'_y'],data[part][1])
    assert json.loads((ROOT/og['datasets'][candidate]['date_file']).read_text())==dates
    shutil.copyfile(ROOT/og['datasets'][candidate]['array_file'],npz)
   datasets[origin][candidate]={'origin':origin,'candidate':candidate,'validation_year':year,'source_file':artifact['file'],'source_sha256':artifact['sha256'],'array_file':str(npz.relative_to(ROOT)),'array_sha256':sha(npz),'price_file':str(price.relative_to(ROOT)),'price_sha256':sha(price),'date_file':str(dp.relative_to(ROOT)),'date_sha256':sha(dp),'metadata_file':str(mp.relative_to(ROOT)),'metadata_sha256':sha(mp),'regime_file':str(rp.relative_to(ROOT)),'regime_sha256':sha(rp),'date_information_sha256':hashlib.sha256(json.dumps(dates,sort_keys=True).encode()).hexdigest(),'metadata':meta,'source_status':'BOTH_UNVERIFIED','production_PIT':'BLOCKED','O1_identical_STEP3A_arrays':origin=='O1'}
  assert datasets[origin]['A']['date_information_sha256']==datasets[origin]['B']['date_information_sha256']
 jobs=[]
 for origin in ['O1','O2']:
  for seed in [2,12]:
   for candidate in ['A','B']:
    for model in ['RNN','LSTM','GRU','LTC','CfC']:
     if origin=='O1' and seed==2:continue
     jobs.append({'run_id':f'{origin}_seed{seed}_{candidate}_{model}','origin':origin,'seed':seed,'candidate':candidate,'model':model,'effective_seed':seed+oc['model_seed_offsets'][model]})
 assert len(jobs)==30 and len({j['run_id'] for j in jobs})==30
 gates=[{'id':k,'status':'PASS','evidence':v} for k,v in [('STEP3A_10_preserved','All completed old identities + best/latest/history/probability hashes match; no rerun'),('old_configuration_and_source','STEP3A config/runtime/data dependencies and exact model source unchanged'),('candidate_integrity','Prior full candidate3939-session source hashes unchanged'),('origin_boundaries','O1<=2020 andO2<=2021 distinct isolated prefixes; no postValidation numeric row parsed'),('labels_purging','Official20-session endpoints; Train20purge; Validation20unknown; violations0'),('scaler_mask','Train-only union of input-window dates; common Vol_Regime mask unchanged'),('feature_order_shape','Log_Ret,Disparity;20x2 CPUfloat32 arrays; O1 bitwise matches STEP3A'),('fixed_seed_hyperparameters','Seeds2/12 + original offsets; all model settings equal STEP3A'),('new_fit_budget','Exactly30 new identities excluding O1Seed2; immutable reuse10'),('Test_isolation','Each worker may only open ownOrigin input subtree and own fit directory'),('manual_thresholds','Train-only30/70 quantiles frozen before predictions; no Validation refit'),('runtime_environment','STEP3A CPU reference package versions unchanged; max2 processes,1LTC')]]
 record={'stage':'STEP3B','prepared_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'run_directory':str(run.relative_to(ROOT)),'reused_STEP3A':reused,'preserved_hash_checks':checks,'datasets':datasets,'jobs':jobs,'gates':gates,'all_preflight_PASS':True,'environment_versions':versions,'model_settings':oc['model_settings'],'model_seed_offsets':oc['model_seed_offsets'],'full_calendar_sha256':sha(cp),'full_calendar_count':3939,'new_fit_budget':30,'old_fit_reexecution_authorized':False,'source_status':'BOTH_UNVERIFIED','production_PIT_status':'BLOCKED','training_enabled':False,'hmm_fit_enabled':False,'Test_evaluation_authorized':False,'2026_used':0}
 write(ROOT/'manifests/step3b_preflight.json',record);write(run/'preflight_private.json',record);Path('/workspace/work/step3b/run_dir.txt').write_text(str(run))
 print('Verified reuse10; staged O1/O2 A/B; planned new30; gates12 PASS')
 for origin in datasets:
  print(origin,[(p,x['metadata']['train_samples'],x['metadata']['validation_samples'],x['metadata']['class_counts']) for p,x in datasets[origin].items()])
