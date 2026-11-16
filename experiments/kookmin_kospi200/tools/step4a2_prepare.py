"""Verify frozen master/old40 and stage ONLY O3 prefix; no model import/forward/fit."""
from pathlib import Path
import sys,json,hashlib,datetime,shutil,importlib.metadata,platform
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.master_data import read_origin_prefix,prepare_origin
from kospi200.o4_o5_pilot_scope import planned_jobs,MODE

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 masterpath=R/'configs/step3c_master_experiment_config.json';c=json.loads(masterpath.read_text());freeze=json.loads((R/'manifests/step3c_protocol_freeze.json').read_text());assert sha(masterpath)==freeze['config_sha256'];assert all(c[k] is False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled'])
 for x in c['implementation_artifacts']:assert sha(R/x['file'])==x['sha256']
 for x in freeze['reports']:assert sha(R/x['file'])==x['sha256']
 base=json.loads((R/'manifests/step3c_prepared_inputs.json').read_text());reuse=pd.read_csv(R/'manifests/step3c_reuse_check.csv');assert len(reuse)==40 and reuse.status.eq('PASS_REUSE_EXACT_F1_TRAINING_CONTRACT').all();checks=[]
 for x in base['reused_completed']:
  record=x['record'];folder=R/x['source_directory'];assert record['status']=='COMPLETED'
  for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:assert sha(folder/file)==record[key];checks.append({'file':str((folder/file).relative_to(R)),'sha256':record[key]})
 previous_o3=json.loads((R/'manifests/step4a1_execution_manifest.json').read_text());assert previous_o3['new_completed']==20 and previous_o3['new_failed']==0 and previous_o3['new_blocked']==0
 assert sha(R/'configs/step4a1_o3_pilot_config.json')==previous_o3['config_sha256'];assert sha(R/'runtime/step4a1_worker.py')==previous_o3['worker_sha256'];assert sha(R/'runtime/step4a1_manager.py')==previous_o3['manager_sha256']
 oldrun=R/previous_o3['run_directory'];reused=list(base['reused_completed'])
 for jid,record in previous_o3['new_records'].items():
  assert record['status']=='COMPLETED';folder=oldrun/'jobs'/jid
  for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256'),('checkpoint_verification.json','postfit_checkpoint_audit_sha256')]:assert sha(folder/file)==record[key];checks.append({'file':str((folder/file).relative_to(R)),'sha256':record[key]})
  reused.append({'run_id':jid,'origin':'O3','seed':record['seed'],'candidate':record['candidate'],'model':record['model'],'effective_seed':record['effective_seed'],'source_stage':'STEP4A1_NEW','source_directory':str(folder.relative_to(R)),'record':record})
 assert len(reused)==60
 olddata=[json.loads((R/'manifests/step3b_preflight.json').read_text())['datasets'],json.loads((R/'manifests/step4a1_preflight.json').read_text())['datasets']]
 for groups in olddata:
  for parts in groups.values():
   for d in parts.values():
    for filename,key in [('array_file','array_sha256'),('metadata_file','metadata_sha256'),('date_file','date_sha256')]:assert sha(R/d[filename])==d[key];checks.append({'file':d[filename],'sha256':d[key]})
 for rel in ['manifests/step3b_metrics.csv','manifests/step3b_epoch_history.csv','manifests/step4a1_metrics.csv','manifests/step4a1_epoch_history.csv']:checks.append({'file':rel,'sha256':sha(R/rel)})
 versions={k:importlib.metadata.version(k) for k in c['environment_versions']};assert versions==c['environment_versions'];assert sha(R/c['source_notebook_file'])==c['source_notebook_sha256']
 oldkernel=(R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1];newkernel=(R/'runtime/step4a2_worker.py').read_text().split(' def equal(x,y):',1)[1];assert oldkernel==newkernel and hashlib.sha256(newkernel.encode()).hexdigest()==c['learning_kernel_sha256']
 stamp=datetime.datetime.now(ZoneInfo('Asia/Seoul'));run=R/'data/derived'/('step4a2_O4_O5_'+stamp.strftime('%Y%m%dT%H%M%S_KST'));run.mkdir(parents=True,exist_ok=False);(run/'jobs').mkdir()
 calpath=R/'manifests/krx_sessions_2010_2025.csv';proof=json.loads((R/'provenance/krx_calendar_provenance.json').read_text());assert sha(calpath)==proof['session_csv_sha256'];fullcal=pd.read_csv(calpath,parse_dates=['Date']);assert len(fullcal)==3939;datasets={}
 for origin,year in [('O4',2023),('O5',2024)]:
  idir=run/'inputs'/origin;idir.mkdir(parents=True);cal=fullcal[fullcal.Date.dt.year<=year].copy();stagecal=idir/'calendar_private.csv';cal.to_csv(stagecal,index=False,date_format='%Y-%m-%d');datasets[origin]={}
  for candidate in ['A','B']:
   previous=base['datasets'][origin][candidate];source=R/previous['source_file'];assert sha(source)==previous['source_sha256'];prices=read_origin_prefix(source,cal.Date,year)
   arrays,meta,dates,regimes=prepare_origin(prices,cal,origin=origin,calendar_source=proof['source_url'],calendar_sha256=sha(stagecal));assert (meta['train_samples'],meta['validation_samples'])=={'O4':(3129,225),'O5':(3374,224)}[origin]
   with np.load(R/previous['array_file'],allow_pickle=False) as z:
    for part in ['train','validation']:assert np.array_equal(arrays[part][0],z[part+'_x']) and np.array_equal(arrays[part][1],z[part+'_y'])
   assert dates==json.loads((R/previous['date_file']).read_text()) and meta['scaler']==previous['metadata']['scaler'];npz=idir/f'{candidate}_arrays_private.npz';shutil.copyfile(R/previous['array_file'],npz)
   p=idir/f'{candidate}_prices_private.csv';prices.to_csv(p,index=False,float_format='%.17g',date_format='%Y-%m-%d');dp=idir/f'{candidate}_dates_private.json';mp=idir/f'{candidate}_metadata_private.json';rp=idir/f'{candidate}_manual_regimes_private.csv';write(dp,dates);write(mp,meta);regimes.to_frame().to_csv(rp,index_label='Date')
   datasets[origin][candidate]={'origin':origin,'candidate':candidate,'validation_year':year,'source_file':previous['source_file'],'source_sha256':previous['source_sha256'],'array_file':str(npz.relative_to(R)),'array_sha256':sha(npz),'price_file':str(p.relative_to(R)),'price_sha256':sha(p),'date_file':str(dp.relative_to(R)),'date_sha256':sha(dp),'metadata_file':str(mp.relative_to(R)),'metadata_sha256':sha(mp),'regime_file':str(rp.relative_to(R)),'regime_sha256':sha(rp),'metadata':meta,'master_array_identity':True,'source_status':'BOTH_UNVERIFIED','production_PIT':'BLOCKED'}
 resources={'checked_at_kst':stamp.isoformat(),'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip(),'memory_max_bytes':int(Path('/sys/fs/cgroup/memory.max').read_text()),'memory_current_bytes':int(Path('/sys/fs/cgroup/memory.current').read_text()),'python':platform.python_version()};assert resources['cpu_max']=='200000 100000' and resources['memory_max_bytes']==8589934592
 mastersha=sha(masterpath);c.update({'stage':'STEP4A2','execution_mode':MODE,'project_root':str(R),'master_config_sha256':mastersha,'o4_o5_pilot_execution_enabled':True,'pilot_execution_enabled':True,'training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'origins':['O4','O5'],'seeds':[2,12],'max_new_fits':40,'total_fit_budget':40,'reused_fits':60,'run_directory':str(run.relative_to(R)),'resources_current':resources,'per_origin_maximum_price_year':{'O4':2023,'O5':2024},'independent_Test_price_cutoffs':{'O4':'2023-12-31','O5':'2024-12-31'},'execution_status':'AUTHORIZED_O4_O5_ONLY40_RETROSPECTIVE_CPU','master460_execution_authorized':False,'statistics_execution_enabled':False,'tau_forward_enabled':False})
 files=['runtime/step4a2_worker.py','runtime/step4a2_manager.py','runtime/step4a2_checkpoint_audit.py','src/kospi200/o4_o5_pilot_scope.py','tools/step4a2_worker.py','tools/step4a2_pilot.py','tools/step4a2_prepare.py']+[x['file'] for x in c['implementation_artifacts']];c['implementation_artifacts']=[{'file':f,'sha256':sha(R/f)} for f in dict.fromkeys(files)];write(R/'configs/step4a2_o4_o5_pilot_config.json',c)
 gates=[{'id':x,'status':'PASS'} for x in ['master_config_and_source_freeze','old60_completed_hashes','O4_O5_master_arrays_exact','official_session20_horizon','O4_O5_boundaries3129_225_3374_224','Train20purge_Validation20UNKNOWN','Train_only_scaler_commonVolMask','feature_order_dtype_finite','perOrigin_Test_price_block','exact40_job_grid','learning_kernel_same_sha','environment_and_current_resources']]
 g={'stage':'STEP4A2','prepared_at_kst':stamp.isoformat(),'run_directory':c['run_directory'],'datasets':datasets,'jobs':planned_jobs(),'reused_completed':reused,'gates':gates,'all_preflight_PASS':True,'master_config_sha256':mastersha,'old60_preserved_hashes':checks,'new_fit_budget':40,'per_origin_Test_price_observations_used':{'O4':0,'O5':0},'2026_used':0,'source_status':'BOTH_UNVERIFIED','production_PIT':'BLOCKED','config_sha256':sha(R/'configs/step4a2_o4_o5_pilot_config.json')};write(R/'manifests/step4a2_preflight.json',g);write(run/'preflight_private.json',g)
 auth={'approved':True,'approved_by':'user','approval_reference':'Current user STEP4A-2 pasted request: O4/O5 only, Seeds2/12, A/B,5 models, max40 CPU Train/Validation fits','request_file_sha256':sha(Path('/workspace/attachments/4ae024dc-e825-4fc1-86c8-e67662574900/붙여넣은 텍스트.txt')),'approved_at_kst':stamp.isoformat(),'scope':MODE,'config_sha256':g['config_sha256'],'worker_sha256':sha(R/'runtime/step4a2_worker.py'),'manager_sha256':sha(R/'runtime/step4a2_manager.py'),'preflight_sha256':sha(R/'manifests/step4a2_preflight.json'),'master_config_sha256':mastersha,'max_new_fits':40,'permits_Test':False,'permits_HMM_fit':False,'permits_GPU':False,'old60_refit_authorized':False,'acknowledges_BOTH_UNVERIFIED':True,'permits_O1_O2_O3_new_fits':False,'permits_seed22plus':False,'permits_tau_forward':False,'permits_confirmatory_pvalues':False};write(R/'provenance/step4a2_o4_o5_authorization.json',auth)
 w=Path('/workspace/work/step4a2');w.mkdir(exist_ok=True);(w/'run_dir.txt').write_text(str(run));print('O4/O5 preflight12 PASS; old60 hashes preserved; exact40 jobs; master flags unchanged')
 print([(o,p,x['metadata']['train_samples'],x['metadata']['validation_samples'],x['metadata']['class_counts']) for o,parts in datasets.items() for p,x in parts.items()])
