"""One approved Origin/Candidate cohort, frozen best weights, exactly one no-grad forward/job."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.metadata,json,os,platform,sys,traceback
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from kospi200.step5b_scope import require_scope
from kospi200.step5b_policy import test_metrics

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
def now():return datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
def execute(config_path,approval_path,origin,candidate):
 c=read(config_path);a=read(approval_path);run=R/c['output_root'];inputs=read(run/'inputs_manifest_private.json');jobs=read(run/'jobs_private.json');info=inputs['groups'][origin][candidate];master=read(R/'configs/step3c_master_experiment_config.json')
 if sha(R/'configs/step3c_master_experiment_config.json')!=c['master_sha256'] or any(master[k] is not False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']):raise ValueError('Master changed')
 sources={p:sha(R/p) for p in c['source_hashes']}
 versions={k:importlib.metadata.version(k) for k in master['environment_versions']}
 env={'python':platform.python_version(),'versions':versions,'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip(),'device':'cpu','dtype':'float32','AMP':False}
 if versions!=master['environment_versions'] or hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest()!=c['execution_environment_sha256']:raise ValueError('Environment changed')
 require_scope(c,a,config_sha=sha(config_path),inputs_sha=sha(run/'inputs_manifest_private.json'),jobs_sha=sha(run/'jobs_private.json'),policy_sha=sha(R/'src/kospi200/step5b_policy.py'),source_hashes=sources,job=next(j for j in jobs if j['origin']==origin and j['candidate']==candidate),roster=jobs)
 if sha(R/info['array_file'])!=info['array_sha256'] or sha(R/info['metadata_file'])!=info['metadata_sha256']:raise ValueError('Staged cohort hash changed')
 import numpy as np
 import torch
 from torch import nn
 from ncps.torch import LTC,CfC
 from runtime.step29_synthetic_smoke import verified_definition_sources
 if torch.version.cuda is not None or str(torch.__version__)!='2.10.0+cpu':raise ValueError('CPU only')
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 if torch.is_autocast_enabled('cpu') or torch.is_autocast_enabled():raise ValueError('AMP forbidden')
 notebook=R/master['source_notebook_file']
 if sha(notebook)!=master['source_notebook_sha256']:raise ValueError('Notebook source changed')
 src=verified_definition_sources(read(notebook),master);ns={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':.2}
 for name in ['init_weights','RecurrentModel','LNNModel','CfCModel']:exec(compile(src[name]['source'],'<verified-original-STEP5B-inference>','exec'),ns)
 ltc_lock=(run/'LTC_resource.lock').open('a')
 active={'checkpoint':None,'output':None,'attempts':0}
 def barrier(event,args):
  if event!='open' or not args or isinstance(args[0],int):return
  try:p=Path(os.fsdecode(args[0])).resolve()
  except (TypeError,ValueError):return
  if p in [(R/info['array_file']).resolve(),(R/info['metadata_file']).resolve(),Path(config_path).resolve(),Path(approval_path).resolve()]:return
  if active['checkpoint'] is not None and p==active['checkpoint']:return
  if active['output'] is not None and p.is_relative_to(active['output']):return
  if p.is_relative_to(R/'data') or p.is_relative_to(R/'originals') or p.is_relative_to('/workspace/attachments'):active['attempts']+=1;raise PermissionError('Own cohort array/current best/output only')
 sys.addaudithook(barrier)
 with np.load(R/info['array_file'],allow_pickle=False) as z:arr={k:z[k].copy() for k in z.files}
 vx=torch.from_numpy(arr['x']);vy=arr['y'];total=0
 for job in [j for j in jobs if j['origin']==origin and j['candidate']==candidate]:
  out=run/'jobs'/job['run_id'];out.mkdir(exist_ok=True);active['output']=out.resolve();active['checkpoint']=(R/job['checkpoint_file']).resolve();lock=(out/'evaluation.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (out/'result.json').exists():print('SKIP_EXISTING',job['run_id'],flush=True);lock.close();continue
  record={'run_id':job['run_id'],'origin':origin,'candidate':candidate,'seed':job['seed'],'model':job['model'],'evaluation_identity':job['evaluation_identity'],'status':'RESERVED','started_at_kst':now(),'forward_calls':0,'checkpoint_loads':0,'new_fits':0,'Test_updates':0,'policy_sha256':a['policy_sha256'],'best_checkpoint_sha256':job['best_checkpoint_sha256'],'Test_array_sha256':info['array_sha256'],'source_hashes':sources,'training_environment_sha256':master['environment_sha256'],'execution_environment_sha256':c['execution_environment_sha256']};write(out/'result.json',record)
  try:
   if job['model']=='LTC':fcntl.flock(ltc_lock,fcntl.LOCK_EX)
   require_scope(c,a,config_sha=sha(config_path),inputs_sha=a['inputs_manifest_sha256'],jobs_sha=a['job_roster_sha256'],policy_sha=sha(R/'src/kospi200/step5b_policy.py'),source_hashes=sources,job=job,roster=jobs)
   if sha(active['checkpoint'])!=job['best_checkpoint_sha256'] or sha(R/job['training_config_file'])!=job['training_config_sha256'] or sha(R/job['source_file'])!=job['source_sha256']:raise ValueError('Frozen checkpoint/config/model source changed')
   payload=torch.load(active['checkpoint'],map_location='cpu',weights_only=True);record['checkpoint_loads']=1
   ident=payload.get('job',{'origin':payload.get('Origin'),'model':payload.get('Model'),'candidate':payload.get('candidate'),'seed':payload.get('Seed'),'effective_seed':payload.get('effective_seed')})
   if any(ident.get(k)!=job[k] for k in ['origin','candidate','seed','model','effective_seed']):raise ValueError('Checkpoint identity mismatch')
   if payload['feature_order']!=['Log_Ret','Disparity'] or payload['scaler_metadata']!=info['scaler'] or payload['input_data_sha256']!=job['input_data_sha256'] or payload['config_sha256']!=job['training_config_sha256']:raise ValueError('Checkpoint input/scaler/config mismatch')
   if payload['environment']['versions']!=master['environment_versions'] or payload.get('worker_sha256',payload.get('runner_sha256'))!=job['source_sha256']:raise ValueError('Checkpoint source/environment mismatch')
   if payload['early_stopping']['best_epoch']!=payload['completed_epoch'] or payload['completed_epoch']!=job['original_record']['best_validation_epoch']:raise ValueError('Not selected frozen best epoch')
   name=job['model'];model=(ns['RecurrentModel'](2,128,name,1,dropout=.2) if name in ['RNN','LSTM','GRU'] else ns['LNNModel' if name=='LTC' else 'CfCModel'](2,128,dropout=.2)).to(device='cpu',dtype=torch.float32);model.load_state_dict(payload['model'],strict=True);model.eval()
   if name=='LTC' and model.ltc.rnn_cell._implicit_param_constraints is not True:raise ValueError('LTC constraint mismatch')
   # Single invocation over the complete fixed cohort. No optimizer/loss/backward.
   record['status']='INFERENCE_STARTED';record['forward_calls']=1;write(out/'result.json',record)
   weights_before={k:v.detach().clone() for k,v in model.state_dict().items()}
   with torch.no_grad():logits=model(vx);prob=torch.softmax(logits,dim=1)[:,1].numpy()
   if logits.shape!=(len(vy),2) or not np.isfinite(prob).all():raise FloatingPointError('Invalid Test logits/probability')
   if not all(torch.equal(v,model.state_dict()[k]) for k,v in weights_before.items()):raise ValueError('Model weights changed during inference')
   measured=test_metrics(vy,prob);manual=[]
   for reg in ['Low_Vol','Mid_Vol','High_Vol']:
    mask=arr['regime']==reg;manual.append({'regime':reg,**test_metrics(vy[mask],prob[mask])})
   np.savez(out/'test_predictions_private.npz',**{k:v for k,v in arr.items() if k not in ['x','volatility']},probability=prob,prediction=(prob>.5).astype(np.int64))
   record.update(status='COMPLETED',finished_at_kst=now(),metrics=measured,manual=manual,probability_sha256=sha(out/'test_predictions_private.npz'),forbidden_access_attempts=active['attempts'],model_state_unchanged=True,model_eval=True,no_grad=True,AMP=False,dtype='float32',checkpoint_preserved=sha(active['checkpoint'])==job['best_checkpoint_sha256']);write(out/'result.json',record);print('DONE',job['run_id'],flush=True);total+=1
  except Exception as e:
   record.update(status='FAILED' if record['forward_calls'] else 'BLOCKED',finished_at_kst=now(),error_type=type(e).__name__,error=str(e),forbidden_access_attempts=active['attempts']);write(out/'result.json',record);(out/'error.log').write_text(traceback.format_exc());print('FAIL',job['run_id'],type(e).__name__,str(e),flush=True);raise RuntimeError('Cohort stopped; no retry after failed identity') from e
  finally:
   if job['model']=='LTC':fcntl.flock(ltc_lock,fcntl.LOCK_UN)
   lock.close()
 return total
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--approval',required=True);p.add_argument('--origin',required=True,choices=['O1','O2','O3','O4','O5']);p.add_argument('--candidate',required=True,choices=['A','B']);a=p.parse_args();execute(a.config,a.approval,a.origin,a.candidate)
