"""Bounded two-process CPU coordinator; at most one memory-heavy LTC at a time."""
from pathlib import Path
import concurrent.futures,fcntl,hashlib,json,os,subprocess,sys,time
from .step4a2_worker import validate_scope,sha,write,now

def execute_expansion(*,root,config_path,approval_path,preflight_path,resume=False):
 root=Path(root).resolve();c=json.loads(Path(config_path).read_text());a=json.loads(Path(approval_path).read_text());g=json.loads(Path(preflight_path).read_text())
 validate_scope(c,a,g,g['jobs'][0],sha(config_path),sha(root/'runtime/step4a2_worker.py'),sha(preflight_path))
 if a['manager_sha256']!=sha(__file__) or c['scheduling']!={'maximum_worker_processes':2,'maximum_concurrent_LTC':1,'torch_threads_per_worker':1}:raise ValueError('Frozen coordinator/resource policy changed')
 for row in c['implementation_artifacts']:
  if sha(root/row['file'])!=row['sha256']:raise ValueError('Implementation artifact changed')
 run=(root/c['run_directory']).resolve();ledgerpath=run/'manager_ledger.json'
 manager_lock=(run/'manager.lock').open('a');fcntl.flock(manager_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 if ledgerpath.exists():
  if not resume:raise ValueError('Expansion already started; explicit --resume only for unfinished identities')
  ledger=json.loads(ledgerpath.read_text())
  if ledger['config_sha256']!=sha(config_path):raise ValueError('Cannot resume changed configuration')
 else:
  if resume:raise ValueError('No expansion ledger exists')
  ledger={'scope':c['execution_mode'],'started_at_kst':now(),'config_sha256':sha(config_path),'worker_sha256':sha(root/'runtime/step4a2_worker.py'),'manager_sha256':sha(__file__),'authorization_sha256':sha(approval_path),'fit_budget':40,'jobs':{j['run_id']:{**j,'status':'PENDING'} for j in g['jobs']},'reused60_trained_again':False,'completed':False}
  write(ledgerpath,ledger)
 if len(ledger['jobs'])!=40 or set(ledger['jobs'])!={j['run_id'] for j in g['jobs']}:raise ValueError('Job plan drift')
 # A worker cannot begin without its own immutable reservation. Completed or
 # failed cases are never replaced by another seed or retrained on resume.
 terminal={'COMPLETED','FAILED_EXCEPTION','FAILED_DIVERGENCE','FAILED_CHECKPOINT_VERIFICATION','BLOCKED'}
 pending=[j for j in g['jobs'] if ledger['jobs'][j['run_id']]['status'] not in terminal]
 def run_job(job):
  jid=job['run_id'];dest=run/'jobs'/jid;dest.mkdir(exist_ok=True)
  reservation=dest/'reservation.json'
  if reservation.exists():
   if json.loads(reservation.read_text())!={'job':job,'config_sha256':sha(config_path),'budget_scope':'O4_O5_ONLY40_EXCLUDES_COMPLETED60'}:raise ValueError('Reservation drift')
  else:write(reservation,{'job':job,'config_sha256':sha(config_path),'budget_scope':'O4_O5_ONLY40_EXCLUDES_COMPLETED60'})
  # On resume attach to a surviving worker instead of launching a duplicate.
  while True:
   probe=(dest/'fit.lock').open('a')
   try:fcntl.flock(probe,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(probe,fcntl.LOCK_UN);probe.close();break
   except BlockingIOError:probe.close()
   rp=dest/'result.json'
   if rp.exists():
    current=json.loads(rp.read_text())
    if current['status'] in terminal:return current
   time.sleep(5)
  cmd=[sys.executable,str(root/'tools/step4a2_worker.py'),'--config-path',str(config_path),'--approval-path',str(approval_path),'--preflight-path',str(preflight_path),'--job-id',jid]
  if resume:cmd.append('--resume')
  env=os.environ.copy();env.update({'PYTHONHASHSEED':'2','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
  with (dest/'execution.log').open('a') as log:result=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
  rp=dest/'result.json'
  if rp.exists():record=json.loads(rp.read_text())
  else:record={**job,'source_stage':'STEP4A2_NEW','status':'BLOCKED','error':'Worker failed before constructing a model; see private execution.log','returncode':result.returncode}
  if result.returncode<0 or record.get('status')=='RUNNING':record.update({'status':'INTERRUPTED','error':'Worker terminated; resume same identity only','returncode':result.returncode});write(rp,record)
  return record
 running={};last_heartbeat=0.
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  while pending or running:
   active_ltc=any(j['model']=='LTC' for j in running.values())
   while len(running)<2:
    index=next((i for i,j in enumerate(pending) if j['model']=='LTC'),None) if not active_ltc else None
    if index is None:index=next((i for i,j in enumerate(pending) if j['model']!='LTC'),None)
    if index is None:break
    job=pending.pop(index);ledger['jobs'][job['run_id']]['status']='RUNNING';ledger['jobs'][job['run_id']]['launched_at_kst']=now();write(ledgerpath,ledger)
    running[pool.submit(run_job,job)]=job;active_ltc=active_ltc or job['model']=='LTC';print('LAUNCH',job['run_id'],'active',len(running),flush=True)
   done,_=concurrent.futures.wait(running,timeout=10,return_when=concurrent.futures.FIRST_COMPLETED)
   for future in done:
    job=running.pop(future)
    try:result=future.result()
    except Exception as exc:result={**job,'source_stage':'STEP4A2_NEW','status':'BLOCKED','error':str(exc)}
    ledger['jobs'][job['run_id']]=result;write(ledgerpath,ledger);print('FINISHED',job['run_id'],result['status'],'epochs',result.get('epochs_completed'),'best',result.get('best_validation_epoch'),flush=True)
   if time.monotonic()-last_heartbeat>=30:
    states=[]
    for job in running.values():
     rp=run/'jobs'/job['run_id']/'result.json'
     if rp.exists():
      r=json.loads(rp.read_text());states.append((job['run_id'],r.get('epochs_completed',0),r.get('best_validation_epoch')))
     else:states.append((job['run_id'],'initializing'))
    print('HEARTBEAT',now(),'completed',sum(r['status']=='COMPLETED' for r in ledger['jobs'].values()),'pending',len(pending),'running',states,flush=True);last_heartbeat=time.monotonic()
 ledger['completed']=all(x['status'] in terminal for x in ledger['jobs'].values());ledger['finished_at_kst']=now();write(ledgerpath,ledger)
 summary={'stage':'STEP4A2','scope':c['execution_mode'],'run_directory':c['run_directory'],'started_at_kst':ledger['started_at_kst'],'finished_at_kst':ledger['finished_at_kst'],'new_fit_budget':40,'planned_new_jobs':40,'new_completed':sum(r['status']=='COMPLETED' for r in ledger['jobs'].values()),'new_failed':sum(r['status'].startswith('FAILED') for r in ledger['jobs'].values()),'new_blocked':sum(r['status']=='BLOCKED' for r in ledger['jobs'].values()),'new_interrupted':sum(r['status']=='INTERRUPTED' for r in ledger['jobs'].values()),'new_records':ledger['jobs'],'reused60':g['reused_completed'],'old60_reexecuted':False,'source_status':'BOTH_UNVERIFIED','production_PIT_status':'BLOCKED','main_price_candidate_selected':None,'training_enabled':False,'hmm_fit_enabled':False,'pilot_execution_enabled':True,'Test_evaluation':False,'GPU':False,'HMM_fit':False,'full_5Origin10Seed':False,'Ablation':False,'2026_used':0,'per_origin_maximum_price_year':c['per_origin_maximum_price_year'],'scheduling':c['scheduling'],'environment_versions':c['environment_versions'],'config_sha256':sha(config_path),'authorization_sha256':sha(approval_path),'preflight_sha256':sha(preflight_path),'worker_sha256':sha(root/'runtime/step4a2_worker.py'),'manager_sha256':sha(__file__),'implementation_artifacts':c['implementation_artifacts'],'data_provenance':g['datasets'],'model_hyperparameters_changed_after_results':False,'source_model_seed_selected_using_validation':False,'checkpoints_raw_prices_daily_targets_probabilities_publication_allowed':False}
 write(root/'manifests/step4a2_execution_manifest.json',summary);write(run/'execution_manifest_private.json',summary);return summary
