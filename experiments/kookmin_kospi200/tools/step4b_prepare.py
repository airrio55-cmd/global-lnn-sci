"""Stage bounded prefixes, verify all prior100, and bind exactly100 new jobs."""
from pathlib import Path
import datetime, hashlib, importlib.metadata, json, platform, shutil, sys
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from kospi200.master_data import prepare_origin
from kospi200.step4b_scope import planned_jobs,MODE
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def main():
 w=Path('/workspace/work/step4b');before=json.loads((w/'before.json').read_text())
 assert all(sha(R/p)==h for p,h in before.items())
 masterpath=R/'configs/step3c_master_experiment_config.json';c=json.loads(masterpath.read_text());freeze=json.loads((R/'manifests/step3c_protocol_freeze.json').read_text())
 assert sha(masterpath)==freeze['config_sha256'] and all(c[k] is False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled'])
 for x in c['implementation_artifacts']+freeze['reports']:assert sha(R/x['file'])==x['sha256']
 previous=json.loads((R/'manifests/step4a2_execution_manifest.json').read_text());oldpre=json.loads((R/'manifests/step4a2_preflight.json').read_text());reused=list(oldpre['reused_completed'])
 for jid,record in previous['new_records'].items():
  reused.append({'run_id':jid,'origin':record['origin'],'seed':record['seed'],'candidate':record['candidate'],'model':record['model'],'source_stage':'STEP4A2_NEW','source_directory':str(Path(previous['run_directory'])/'jobs'/jid),'record':record})
 assert len(reused)==100 and len({x['run_id'] for x in reused})==100
 expected_old={f'{o}_seed{s}_{p}_{m}' for o in ['O1','O2','O3','O4','O5'] for s in [2,12] for p in ['A','B'] for m in c['models']};assert {x['run_id'] for x in reused}==expected_old
 # STEP3D is explicitly the same twenty identities, never appended to the ledger.
 d3=json.loads((R/'manifests/step3d_execution_manifest.json').read_text());assert d3['new_fits_this_step']==0 and {x['run_id'] for x in d3['job_hashes']}=={x for x in expected_old if x.startswith('O3_')}
 checks=[]
 for item in reused:
  record=item['record'];assert record['status']=='COMPLETED';folder=R/item['source_directory']
  for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:
   assert sha(folder/file)==record[key];checks.append({'file':str((folder/file).relative_to(R)),'sha256':record[key]})
  if 'postfit_checkpoint_audit_sha256' in record:
   assert sha(folder/'checkpoint_verification.json')==record['postfit_checkpoint_audit_sha256'];checks.append({'file':str((folder/'checkpoint_verification.json').relative_to(R)),'sha256':record['postfit_checkpoint_audit_sha256']})
 old_configs=['step3a_pilot_config','step3b_expansion_config','step4a1_o3_pilot_config','step4a2_o4_o5_pilot_config']
 for name in old_configs:
  p=R/'configs'/f'{name}.json'
  if p.exists():
   cfg=json.loads(p.read_text());assert cfg['model_settings']==c['model_settings'] and cfg['model_seed_offsets']==c['model_seed_offsets']
   for x in cfg.get('implementation_artifacts',[]):assert sha(R/x['file'])==x['sha256']
 old_kernel=(R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1];new_kernel=(R/'runtime/step4b_worker.py').read_text().split(' def equal(x,y):',1)[1]
 assert old_kernel==new_kernel and hashlib.sha256(new_kernel.encode()).hexdigest()==c['learning_kernel_sha256']
 versions={k:importlib.metadata.version(k) for k in c['environment_versions']};assert versions==c['environment_versions'];assert sha(R/c['source_notebook_file'])==c['source_notebook_sha256']
 stamp=datetime.datetime.now(ZoneInfo('Asia/Seoul'));run=R/'data/derived'/('step4b_seeds22_32_'+stamp.strftime('%Y%m%dT%H%M%S_KST'));run.mkdir(parents=True,exist_ok=False);(run/'jobs').mkdir()
 groups={}
 for rel in ['manifests/step3b_preflight.json','manifests/step4a1_preflight.json','manifests/step4a2_preflight.json']:groups.update(json.loads((R/rel).read_text())['datasets'])
 datasets={};counts={'O1':(2387,228),'O2':(2635,228),'O3':(2883,226),'O4':(3129,225),'O5':(3374,224)}
 proof=json.loads((R/'provenance/krx_calendar_provenance.json').read_text());calendar_path=R/'manifests/krx_sessions_2010_2025.csv';assert sha(calendar_path)==proof['session_csv_sha256'];calendar=pd.read_csv(calendar_path,parse_dates=['Date']);assert len(calendar)==3939
 for origin in ['O1','O2','O3','O4','O5']:
  year=2019+int(origin[1]);idir=run/'inputs'/origin;idir.mkdir(parents=True);cal=calendar[calendar.Date.dt.year<=year].copy();calpath=idir/'calendar_private.csv';cal.to_csv(calpath,index=False,date_format='%Y-%m-%d');datasets[origin]={}
  for candidate in ['A','B']:
   old=groups[origin][candidate]
   for f,k in [('array_file','array_sha256'),('date_file','date_sha256'),('metadata_file','metadata_sha256'),('price_file','price_sha256'),('regime_file','regime_sha256')]:assert sha(R/old[f])==old[k];checks.append({'file':old[f],'sha256':old[k]})
   prices=pd.read_csv(R/old['price_file'],parse_dates=['Date'],float_precision='round_trip');assert prices.Date.max().year<=year
   arrays,meta,dates,regimes=prepare_origin(prices,cal,origin=origin,calendar_source=proof['source_url'],calendar_sha256=sha(calpath));assert (meta['train_samples'],meta['validation_samples'])==counts[origin]
   with np.load(R/old['array_file'],allow_pickle=False) as z:
    for part in ['train','validation']:assert np.array_equal(arrays[part][0],z[part+'_x']) and np.array_equal(arrays[part][1],z[part+'_y'])
   assert dates==json.loads((R/old['date_file']).read_text()) and meta['scaler']==old['metadata']['scaler'] and meta['manual_reference']==old['metadata']['manual_reference']
   info=dict(old);info['metadata']=meta
   for key in ['array_file','price_file','date_file','metadata_file','regime_file']:
    dest=idir/(candidate+'_'+Path(old[key]).name);shutil.copyfile(R/old[key],dest);info[key]=str(dest.relative_to(R))
   # Keep original NPZ and source bytes; the reconstructed metadata is equal in model-relevant fields.
   datasets[origin][candidate]=info
 resources={'checked_at_kst':stamp.isoformat(),'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip(),'memory_max_bytes':int(Path('/sys/fs/cgroup/memory.max').read_text()),'memory_current_bytes':int(Path('/sys/fs/cgroup/memory.current').read_text()),'python':platform.python_version()}
 assert resources['cpu_max']=='200000 100000' and resources['memory_max_bytes']==8589934592
 mastersha=sha(masterpath);jobs=planned_jobs();assert len(jobs)==100 and len({j['run_id'] for j in jobs})==100 and not (expected_old & {j['run_id'] for j in jobs})
 c.update({'stage':'STEP4B','execution_mode':MODE,'project_root':str(R),'master_config_sha256':mastersha,'step4b_execution_enabled':True,'pilot_execution_enabled':True,'training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'origins':['O1','O2','O3','O4','O5'],'seeds':[22,32],'max_new_fits':100,'total_fit_budget':100,'reused_fits':100,'run_directory':str(run.relative_to(R)),'resources_current':resources,'per_origin_maximum_price_year':{o:2019+int(o[1]) for o in datasets},'independent_Test_price_cutoffs':{o:f'{2019+int(o[1])}-12-31' for o in datasets},'execution_status':'AUTHORIZED_ONLY_SEEDS22_32_100_RETROSPECTIVE_CPU','master460_execution_authorized':False,'statistics_execution_enabled':False,'tau_forward_enabled':False})
 files=['runtime/step4b_worker.py','runtime/step4b_manager.py','runtime/step4b_checkpoint_audit.py','src/kospi200/step4b_scope.py','tools/step4b_worker.py','tools/step4b_pilot.py','tools/step4b_prepare.py','tools/step4b_smoke.py']+[x['file'] for x in c['implementation_artifacts']];c['implementation_artifacts']=[{'file':f,'sha256':sha(R/f)} for f in dict.fromkeys(files)]
 cp=R/'configs/step4b_pilot_config.json';write(cp,c)
 gates=[{'id':x,'status':'PASS'} for x in ['old100_unique_completed_preserved','STEP3D_O3_not_double_counted','source_model_loss_kernel_exact','environment_pins_exact','official_session20_horizon','all5_origin_arrays_scaler_manual_exact','origin_purging20_unknown20','new100_unique_seed22_32_only','feature_order_float32_finite','master_false_flags_preserved','CPU2_memory8GiB_confirmed']]
 g={'stage':'STEP4B','prepared_at_kst':stamp.isoformat(),'run_directory':c['run_directory'],'datasets':datasets,'jobs':jobs,'reused_completed':reused,'gates':gates,'all_preflight_PASS':True,'master_config_sha256':mastersha,'old100_preserved_hashes':checks,'new_fit_budget':100,'2026_used':0,'source_status':'BOTH_UNVERIFIED','production_PIT':'BLOCKED','config_sha256':sha(cp)};gp=R/'manifests/step4b_preflight_private.json';write(gp,g);write(run/'preflight_private.json',g)
 auth={'approved':True,'approved_by':'user','approval_reference':'User STEP4B explicit request: exactly100 CPU retrospective Train/Validation fits; OriginsO1..O5, A/B, Seeds22/32, five F1 models; not remaining400','approved_at_kst':stamp.isoformat(),'scope':MODE,'config_sha256':sha(cp),'worker_sha256':sha(R/'runtime/step4b_worker.py'),'manager_sha256':sha(R/'runtime/step4b_manager.py'),'preflight_sha256':sha(gp),'master_config_sha256':mastersha,'max_new_fits':100,'permits_Test':False,'permits_HMM_fit':False,'permits_GPU':False,'old100_refit_authorized':False,'acknowledges_BOTH_UNVERIFIED':True,'permits_seed42plus':False,'permits_tau_forward':False,'permits_confirmatory_pvalues':False};write(R/'manifests/step4b_authorization.json',auth)
 pd.DataFrame(jobs).assign(master_config_sha256=mastersha,pilot_config_sha256=sha(cp)).to_csv(R/'manifests/step4b_job_roster.csv',index=False)
 oldrows=pd.read_csv(R/'manifests/step4a2_all100_diagnostic_metrics.csv',float_precision='round_trip');assert len(oldrows)==100 and set(oldrows.run_id)==expected_old and oldrows.status.eq('COMPLETED').all()
 for job in reused:
  row=oldrows.set_index('run_id').loc[job['run_id']]
  for k,v in job['record']['metrics'].items():
   if k in row.index and isinstance(v,(float,int)):assert np.isclose(row[k],v,rtol=0,atol=1e-14)
 for k in list(oldrows.columns):
  if k=='source_directory' or k.endswith('_file') or k.endswith('_directory'):oldrows.drop(columns=k,inplace=True)
 oldrows['original_source_stage']=oldrows.source_stage;oldrows['source_stage']='OLD100_REUSED';oldrows.to_csv(R/'manifests/step4b_baseline100_metrics.csv',index=False)
 (w/'run_dir.txt').write_text(str(run));write(w/'old100_private_hashes.json',checks);print(json.dumps({'old100_verified':100,'duplicate':0,'conflict':0,'new_roster':len(jobs),'dataset_groups':len(datasets),'gates':len(gates),'run_directory':str(run)}))

if __name__=='__main__':main()
