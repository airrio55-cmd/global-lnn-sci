"""Exactly ten authorized Train-only GaussianHMM candidates for one cohort."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.metadata,json,os,sys,traceback
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from kospi200.step6b_scope import require_scope
from kospi200.step6a_hmm import HMM_KWARGS,candidate_eligibility,filter_sessions,validate_parameters

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def clean(x):
 import numpy as np
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,np.generic):x=x.item()
 if isinstance(x,float) and not np.isfinite(x):return None
 return x

def write(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n');os.replace(tmp,p)
def validate(config_path,approval_path):
 c=read(config_path);a=read(approval_path);run=R/c['output_root'];inputs=read(run/'inputs_manifest_private.json');jobs=read(run/'job_roster_private.json');hashes={p:sha(R/p) for p in c['source_hashes']};require_scope(c,a,config_sha=sha(config_path),inputs_sha=sha(run/'inputs_manifest_private.json'),roster_sha=sha(run/'job_roster_private.json'),source_hashes=hashes,job=jobs[0],roster=jobs)
 master=read(R/'configs/step3c_master_experiment_config.json')
 if sha(R/'configs/step3c_master_experiment_config.json')!=c['master_sha256'] or any(master[k] is not False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']):raise ValueError('Master changed')
 if sha(R/'configs/step6a_hmm_protocol.json')!=c['HMM_protocol_sha256'] or sha(R/'src/kospi200/step6a_hmm.py')!=c['HMM_adapter_sha256']:raise ValueError('Frozen HMM contract changed')
 if {k:importlib.metadata.version(k) for k in c['versions']}!=c['versions'] or Path('/sys/fs/cgroup/cpu.max').read_text().strip()!=c['resources']['cpu_max'] or int(Path('/sys/fs/cgroup/memory.max').read_text())!=c['resources']['memory_max']:raise ValueError('Environment/resources changed')
 return c,a,run,inputs,jobs

def execute(config_path,approval_path,origin,candidate):
 c,a,run,inputs,jobs=validate(config_path,approval_path);info=inputs['groups'][origin][candidate]
 if sha(R/info['Train_file'])!=info['Train_sha256'] or sha(R/info['scaler_file'])!=info['scaler_sha256']:raise ValueError('Train-only input changed')
 import numpy as np
 from hmmlearn.hmm import GaussianHMM
 meta_allowed={(R/info[k]).resolve() for k in ['Train_file','scaler_file']}|{Path(config_path).resolve(),Path(approval_path).resolve()};active={'out':None,'denied':0}
 def barrier(event,args):
  if event!='open' or not args or isinstance(args[0],int):return
  try:p=Path(os.fsdecode(args[0])).resolve()
  except (TypeError,ValueError):return
  if p in meta_allowed or active['out'] is not None and p.is_relative_to(active['out']):return
  if p.is_relative_to(R/'data') or p.is_relative_to(R/'originals') or p.is_relative_to('/workspace/attachments'):active['denied']+=1;raise PermissionError('Train cohort/own output only; no Validation/Test/results')
 sys.addaudithook(barrier)
 with np.load(R/info['Train_file'],allow_pickle=False) as z:x=z['x'].copy();raw=z['raw'].copy();ids=z['session_id'].copy()
 if x.dtype!=np.float64 or x.shape!=(info['expected_Train_rows'],1) or not np.isfinite(x).all():raise ValueError('Invalid Train-only observation')
 for job in [j for j in jobs if j['origin']==origin and j['candidate']==candidate]:
  folder=run/'candidates'/job['job_id'];folder.mkdir(exist_ok=True);active['out']=folder.resolve();lock=(folder/'fit.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (folder/'result.json').exists():print('SKIP_EXISTING',job['job_id'],flush=True);lock.close();continue
  record={**job,'status':'RESERVED','fit_calls':0,'iterations':None,'monitor_converged':False,'train_log_likelihood':None,'likelihood_history':[],'train_hard_states':[],'parameters':{},'Train_sha256':info['Train_sha256'],'Train_date_SHA':info['Train_date_file_sha256'],'scaler_sha256':info['scaler_sha256'],'source_hashes':c['source_hashes'],'reproducibility_evidence':{'synthetic_repeat_PASS':True,'deterministic_settings':True,'fixed_seed':job['seed'],'data_sha256':info['Train_sha256'],'source_sha256':c['source_hashes']['runtime/step6b_fit.py'],'environment_sha256':c['environment_sha256']},'Train_filter_calls':0,'forbidden_access_attempts':0};write(folder/'result.json',record)
  try:
   require_scope(c,a,config_sha=a['config_sha256'],inputs_sha=a['input_manifest_sha256'],roster_sha=a['roster_sha256'],source_hashes=c['source_hashes'],job=job,roster=jobs)
   model=GaussianHMM(random_state=job['seed'],**HMM_KWARGS);record.update(status='FIT_STARTED',fit_calls=1);write(folder/'result.json',record);model.fit(x)
   p={'startprob':model.startprob_.copy(),'transmat':model.transmat_.copy(),'means':model.means_.copy(),'covars':model.covars_.copy()};ll=float(model.score(x));history=list(model.monitor_.history);record.update(parameters=p,train_log_likelihood=ll,iterations=int(model.monitor_.iter),monitor_converged=bool(model.monitor_.converged),likelihood_history=history,last_LL_delta=float(history[-1]-history[-2]) if len(history)>1 else None)
   try:
    validate_parameters(p);record['covariance_positive_definite']=True;posterior=filter_sessions(x,ids,parameters=p,expected_session_ids=ids);hard=posterior.argmax(1);record.update(train_hard_states=hard.tolist(),Train_state_occupancy=[float((hard==i).mean()) for i in [0,1]],Train_filter_calls=1);np.savez(folder/'Train_posterior_private.npz',posterior=posterior,session_id=ids)
   except Exception as e:record.update(covariance_positive_definite=False,parameter_filter_error=str(e))
   eligible=candidate_eligibility(record);record.update(status='ELIGIBLE' if eligible['eligible'] else 'INELIGIBLE',eligibility=eligible,forbidden_access_attempts=active['denied']);np.savez(folder/'parameters_private.npz',**p);record['parameter_sha256']=sha(folder/'parameters_private.npz')
  except Exception as e:
   record.update(status='FAILED',error=str(e),error_type=type(e).__name__,forbidden_access_attempts=active['denied']);(folder/'error.log').write_text(traceback.format_exc())
  finally:
   write(folder/'result.json',record);lock.close();print('CANDIDATE',job['job_id'],record['status'],'iterations',record.get('iterations'),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--approval',required=True);p.add_argument('--origin',required=True);p.add_argument('--candidate',required=True);a=p.parse_args();execute(a.config,a.approval,a.origin,a.candidate)
