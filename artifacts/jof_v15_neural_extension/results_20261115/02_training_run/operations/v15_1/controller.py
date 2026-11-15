"""Observability/integrity wrapper; delegates every fit and statistic to frozen V15 code.
V15.1: complete-job reuse only; no optimizer/epoch resume; no automatic retry.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import os,json,csv,hashlib,subprocess,time,signal,traceback,datetime,collections
ROOT=Path('/repo');OUT=Path('/runs');FROZEN=ROOT/'artifacts/jof_v15_neural_extension';AUTH=Path('/authorization/record.json')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  for chunk in iter(lambda:stream.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def js(path,value):
 path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,default=str)+'\n');tmp.replace(path)
def check_job(job,base,runner,v14,context):
 import numpy as np,pandas as pd,torch
 folder=base/'fits'/job['fit_id'];names=['checkpoint.pt','predictions.csv','fit_metadata.json','training_loss.csv'];assert all((folder/n).is_file() for n in names),'Missing completed-job artifacts'
 history=pd.read_csv(folder/'training_loss.csv');assert history.epoch.tolist()==list(range(1,61)) and np.isfinite(history.train_loss).all()
 meta=json.loads((folder/'fit_metadata.json').read_text());pred=pd.read_csv(folder/'predictions.csv',float_precision='round_trip');ck=torch.load(folder/'checkpoint.pt',map_location='cpu',weights_only=True)
 assert (ck['architecture'],ck['input_size'],ck['seed'],ck['epochs'],ck['loss'])==(job['Architecture'],job['Input_dim'],job['Seed'],60,'CE')
 assert ck['state_dict'] and all(torch.isfinite(t).all() for t in ck['state_dict'].values())
 key=(job['Market'],job['Stage'],job['Eval_end_year'],job['Representation'])
 if key not in context:
  # Only keep current fold RAW/LOG tensor contexts; no predictive model is fit here.
  if len(context)>=2:context.clear()
  raw,frame,rawcols,_=v14.load_market(ROOT,job['Market']);cols=rawcols if job['Representation']=='RAW' else runner.LOGCOLS
  train=v14.records(frame,raw,rawcols,'2010-01-01',job['Train_end'])
  ev=v14.records(frame,raw,rawcols,f"{job['Stage']}-01-01",f"{job['Eval_end_year']}-12-31")
  xtr,xev,scaler,used=runner.window_tensors(train,ev,frame,cols);context[key]=(train,ev,xtr,xev,scaler,used,list(cols))
 train,ev,xtr,xev,scaler,used,cols=context[key]
 assert len(train)==job['TrainN'] and len(ev)==len(pred)==job['EvalN']
 dates=[r['Date'] for r in ev];truth=np.array([r['y'] for r in ev]);assert pred.Date.tolist()==dates and meta['evaluation_dates']==dates and meta['train_dates']==[r['Date'] for r in train]
 assert hashlib.sha256('\n'.join(dates).encode()).hexdigest()==job['Evaluation_dates_sha256']
 np.testing.assert_array_equal(pred.Y_true,truth);assert not pred.Date.duplicated().any()
 probability=pred.Probability.to_numpy();assert np.isfinite(probability).all() and ((probability>=0)&(probability<=1)).all()
 np.testing.assert_array_equal(ck['probabilities'].numpy(),probability);np.testing.assert_array_equal(pred.Y_pred,(probability>.5).astype(int))
 assert meta['columns']==cols and meta['scaler_used_rows']==used.tolist()
 for field,value in [('scaler_mean',scaler.mean_),('scaler_scale',scaler.scale_),('scaler_var',scaler.var_)]:np.testing.assert_allclose(meta[field],value,atol=1e-12,rtol=0)
 assert meta['input_tensor_sha256']==hashlib.sha256(xtr.tobytes()).hexdigest() and meta['eval_tensor_sha256']==hashlib.sha256(xev.tobytes()).hexdigest()
 runner.replay_checkpoint(folder/'checkpoint.pt',xev)
 return {'files_sha256':{n:sha(folder/n) for n in names},'started_at_utc':meta['started_at_utc'],'ended_at_utc':meta['ended_at_utc'],'rows':len(pred),'state':'COMPLETE','checkpoint_replay':'PASS'}
def final_validation(base,jobs,completed):
 import numpy as np,pandas as pd
 assert len(completed)==len(jobs)==1080
 for j in jobs:
  for name,digest in completed[j['fit_id']]['files_sha256'].items():assert sha(base/'fits'/j['fit_id']/name)==digest
 completion=json.loads((base/'completion_manifest.json').read_text());source=base/'v15_predictions.csv';assert completion['fit_count']==1080 and completion['prediction_sha256']==sha(source) and completion['protocol_config_sha256']==sha(FROZEN/'V15_CONFIG_LOCKED.json')
 p=pd.read_csv(source,float_precision='round_trip');key=['Market','Origin','Period','Date','Model','Seed'];assert not p.duplicated(key).any() and not p[key+['Probability','Y_true']].isna().any().any()
 # Frozen structural validator checks all exact scoring dates,seeds and50/50 ensemble; no AUC.
 import v15_analysis_draft as frozen_analysis
 frozen_analysis.validate_predictions(ROOT,p)
 for job in jobs:
  saved=pd.read_csv(base/'fits'/job['fit_id']/'predictions.csv',float_precision='round_trip')
  actual=p[(p.Market==job['Market'])&(p.Origin==job['Origin'])&(p.Period==job['Period'])&(p.Model==job['Model'])&(p.Seed==job['Seed'])]
  actual=actual[actual.Date.isin(saved.Date)]
  assert actual.Date.tolist()==saved.Date.tolist();np.testing.assert_array_equal(actual.Probability,saved.Probability);np.testing.assert_array_equal(actual.Y_true,saved.Y_true)
 js(OUT/'result_manifest.json',{'status':'ALL1080_FITS_INTEGRITY_VALIDATED','locked_commit':json.loads(AUTH.read_text())['locked_commit'],'jobs':completed,'combined_predictions_sha256':sha(source),'completed_at_utc':now(),'AUC_computed_by_validation':False})
def main(execute=False):
 sys.path.insert(0,str(FROZEN));import v15_locked_runner as runner
 from prepare import verify_code
 verify_code()
 cfg,anchor=runner.check_lock(ROOT,FROZEN/'V15_CONFIG_LOCKED.json',AUTH,require_execution=True)
 jobs=json.loads((FROZEN/'step4/job_manifest.json').read_text())['jobs'];assert len(jobs)==1080 and len({j['fit_id'] for j in jobs})==1080
 if not execute:print('LAUNCHER_VERIFY_ONLY_PASS;0fits/0AUC',flush=True);return
 plan=json.loads((OUT/'recovery_plan.json').read_text());ready=json.loads((OUT/'preparation_complete.json').read_text())
 if ready['recovery_plan_sha256']!=sha(OUT/'recovery_plan.json') or plan['code_manifest_sha256']!=sha(Path(__file__).with_name('version_manifest.json')):raise ValueError('Recovery plan drift')
 if (OUT/'process.json').exists():raise ValueError('Recovery attempt already launched;no in-place restart')
 if {p.name for p in (OUT/'results/fits').iterdir() if p.is_dir()}!=set(plan['reused_jobs']):raise ValueError('Unplanned existing fit directories')
 v14=runner.v14_module(ROOT);completed=plan['reused_jobs'].copy();states={j['fit_id']:('COMPLETE' if j['fit_id'] in completed else 'PENDING') for j in jobs};context={};child=None;first=None;status='STARTING';last_hash=0;started=now();active=None
 def snapshot():
  counts=collections.Counter(states.values());js(OUT/'progress.json',{'state':status,'planned':1080,'completed':counts['COMPLETE'],'failed':counts['FAILED'],'running':counts['RUNNING'],'pending':counts['PENDING'],'active_job':active,'first_epoch_observed_at_utc':first,'wrapper_started_at_utc':started,'updated_at_utc':now(),'analysis':('RUNNING' if status=='ANALYSIS_RUNNING' else 'COMPLETE' if status=='ALL_COMPLETE_WITH_ANALYSIS' else 'NOT_STARTED_OR_FAILED'),'resume_supported':True,'resume_mode':'verified_complete_jobs_only;incomplete_job_restarts_epoch1','recovery_version':'V15.1','reused_jobs':plan['reused_count'],'new_completed':counts['COMPLETE']-plan['reused_count'],'locked_commit':anchor})
  js(OUT/'job_status.json',{'states':states,'completed_artifacts':completed,'updated_at_utc':now()})
  tmp=OUT/'job_status.csv.tmp'
  with tmp.open('w',newline='') as stream:
   writer=csv.DictWriter(stream,fieldnames=['fit_id','Market','Origin','Stage','Model','Seed','status']);writer.writeheader();writer.writerows({**{k:j[k] for k in ['fit_id','Market','Origin','Stage','Model','Seed']},'status':states[j['fit_id']]} for j in jobs)
  tmp.replace(OUT/'job_status.csv')
 def interrupted(signum,frame):raise KeyboardInterrupt(f'Signal{signum};no automatic resume')
 signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
 try:
  snapshot();print('PREFLIGHT_VALIDATED; STARTING_FROZEN_RUNNER',anchor,flush=True)
  log=(OUT/'training.log').open('a',buffering=1);child=subprocess.Popen([sys.executable,'-u',str(Path(__file__).with_name('worker.py')),'--execute'],stdout=log,stderr=subprocess.STDOUT)
  status='RUNNING';js(OUT/'process.json',{'pid':child.pid,'started_at_utc':now(),'command':'V15.1 worker dispatch;original fitting function on cache misses;no automatic retry'});snapshot()
  while True:
   code=child.poll();existing=[i for i,j in enumerate(jobs) if (OUT/'results/fits'/j['fit_id']).exists()];latest=max(existing,default=-1);active=jobs[latest]['fit_id'] if latest>=0 and jobs[latest]['fit_id'] not in completed else None
   for i in existing:
    job=jobs[i];jid=job['fit_id']
    if jid in completed:continue
    states[jid]='RUNNING'
    loss=OUT/'results/fits'/jid/'training_loss.csv'
    if loss.is_file() and first is None:
     try:
      history=list(csv.DictReader(loss.open()));valid=[r for r in history if r.get('epoch') and r.get('train_loss') and __import__('math').isfinite(float(r['train_loss']))]
      if valid:first=now();print('TRAINING_CONFIRMED',first,jid,'epoch',valid[-1]['epoch'],'loss',valid[-1]['train_loss'],flush=True)
     except (ValueError,OSError):pass
    # Wait until next fit exists or training child exits; do not read a CSV still being written.
    if i<latest or code is not None:
     try:completed[jid]=check_job(job,OUT/'results',runner,v14,context);completed[jid].update({'provenance':'new_V15.1_fit','attempt_run_id':json.loads(AUTH.read_text())['run_id']});states[jid]='COMPLETE';print('JOB_COMPLETE',len(completed),'/1080',jid,flush=True)
     except Exception:
      states[jid]='FAILED';raise
   if time.monotonic()-last_hash>300:
    for rel,digest in json.loads((FROZEN/'V15_LOCK_PAYLOAD.json').read_text())['sha256'].items():assert sha(ROOT/rel)==digest,'Frozen file drift:'+rel
    last_hash=time.monotonic()
   snapshot()
   if code is not None:
    if code!=0:raise RuntimeError(f'Frozen runner exited{code};preserve all artifacts;no resume/retry permitted')
    break
   time.sleep(5)
  status='VALIDATING_ALL_RESULTS';snapshot();final_validation(OUT/'results',jobs,completed)
  print('ALL1080_FITS_AND_INTEGRITY_COMPLETE',now(),flush=True);status='TRAINING_COMPLETE_ANALYSIS_PENDING';snapshot()
  auth=json.loads(AUTH.read_text())
  if auth.get('analysis_authorized') is True:
   runner.check_lock(ROOT,FROZEN/'V15_CONFIG_LOCKED.json',AUTH,require_analysis=True)
   status='ANALYSIS_RUNNING';snapshot()
   with (OUT/'analysis.log').open('a') as log:
    subprocess.run([sys.executable,'-u',str(FROZEN/'v15_analysis_draft.py'),'--repo',str(ROOT),'--predictions',str(OUT/'results/v15_predictions.csv'),'--out',str(OUT/'analysis'),'--config',str(FROZEN/'V15_CONFIG_LOCKED.json'),'--lock',str(AUTH),'--acknowledge-analysis'],stdout=log,stderr=subprocess.STDOUT,check=True)
   js(OUT/'analysis_manifest.json',{'status':'COMPLETED','files_sha256':{str(p.relative_to(OUT/'analysis')):sha(p) for p in (OUT/'analysis').rglob('*') if p.is_file()},'completed_at_utc':now()});status='ALL_COMPLETE_WITH_ANALYSIS'
  else:status='ALL_FITS_VALIDATED_ANALYSIS_NOT_AUTHORIZED'
  js(OUT/'completion.json',{'status':status,'learned_jobs_complete':1080,'reused_jobs':plan['reused_count'],'new_fits_complete':1080-plan['reused_count'],'recovery_version':'V15.1','failed_jobs':0,'locked_commit':anchor,'actual_first_fit_started_at_utc':min(v['started_at_utc'] for v in completed.values()),'actual_last_fit_ended_at_utc':max(v['ended_at_utc'] for v in completed.values()),'completed_at_utc':now()});snapshot();print(status,flush=True)
 except BaseException as error:
  if child is not None and child.poll() is None:
   child.terminate()
   try:child.wait(timeout=30)
   except subprocess.TimeoutExpired:child.kill();child.wait()
  for jid,state in states.items():
   if state=='RUNNING':states[jid]='FAILED'
  status='RECOVERY_ATTEMPT_FAILED_PRESERVE_AND_REPREPARE';js(OUT/'error.json',{'error_type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'time_utc':now(),'completed_jobs_retained':len(completed),'resume_supported':True,'resume_requires_new_prepared_attempt':True});snapshot();print(status,str(error),flush=True);raise
if __name__=='__main__':main(execute='--execute' in sys.argv)
