"""No-model preflight checks; preserves all old files and writes new evidence only."""
from pathlib import Path
import copy, hashlib, json, subprocess, sys
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from runtime.step4b_worker import validate_scope
from kospi200.step4b_scope import planned_jobs
from kospi200.data import BlockedError,local_features
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 cp=R/'configs/step4b_pilot_config.json';ap=R/'manifests/step4b_authorization.json';gp=R/'manifests/step4b_preflight_private.json'
 c,a,g=[json.loads(p.read_text()) for p in [cp,ap,gp]];checks=[]
 def check(key,condition):
  checks.append({'id':key,'status':'PASS' if condition else 'FAIL'})
  if not condition:raise RuntimeError(key)
 check('exact_new100_roster',g['jobs']==planned_jobs() and len({j['run_id'] for j in g['jobs']})==100)
 check('approval_scope',validate_scope(c,a,g,g['jobs'][0],sha(cp),sha(R/'runtime/step4b_worker.py'),sha(gp)))
 for key,value in [('seeds',[42]),('max_new_fits',400),('gpu_enabled',True),('training_enabled',True),('models',['LTC'])]:
  d=copy.deepcopy(c);d[key]=value
  try:validate_scope(d,a,g,g['jobs'][0],sha(cp),sha(R/'runtime/step4b_worker.py'),sha(gp))
  except BlockedError:check('reject_'+key,True)
  else:check('reject_'+key,False)
 for row in c['implementation_artifacts']:check('frozen_'+row['file'],sha(R/row['file'])==row['sha256'])
 for origin,parts in g['datasets'].items():
  year=2019+int(origin[1]);info=parts['A']
  code="from pathlib import Path; from runtime.step4b_worker import barrier; import json; root=Path("+repr(str(R))+"); c=json.loads((root/'configs/step4b_pilot_config.json').read_text()); g=json.loads((root/'manifests/step4b_preflight_private.json').read_text()); run=root/c['run_directory']; state=barrier(root,run,run/'barrier_probe',"+repr(origin)+",(root/c['source_notebook_file']).resolve()); p=root/g['datasets']["+repr(origin)+"]['A']['date_file']; assert p.open().read(1); denied=0\nfor o in g['datasets']:\n if o=="+repr(origin)+":continue\n try:(root/g['datasets'][o]['A']['array_file']).open('rb')\n except PermissionError:denied+=1\n else:raise RuntimeError('Origin barrier bypass')\nassert denied==4\n"
  p=subprocess.run([sys.executable,'-c',code],cwd=R,env={**__import__('os').environ,'PYTHONPATH':str(R)+':'+str(R/'src')},capture_output=True,text=True);check(origin+'_actual_worker_barrier',p.returncode==0)
  for candidate,d in parts.items():
   m=d['metadata'];dates=json.loads((R/d['date_file']).read_text())
   check(origin+candidate+'_cutoffs',m['price_end']<=f'{year}-12-31' and m['train_purged']==20 and m['validation_unknown_excluded']==20 and m['train_max_label_end']<m['validation_boundary_start'] and m['validation_future_endpoint_violations']==0)
   check(origin+candidate+'_train_scaler',m['scaler']['fit_end']==m['train_last_sample'] and m['scaler']['fit_rows']==m['train_samples']+19 and m['scaler']['source_partition']=='train')
   with np.load(R/d['array_file'],allow_pickle=False) as z:
    check(origin+candidate+'_input_shape_dtype_finite',all(z[k+'_x'].shape==(m[k+'_samples'],20,2) and z[k+'_x'].dtype==np.float32 and np.isfinite(z[k+'_x']).all() for k in ['train','validation']))
   price=pd.read_csv(R/d['price_file'],parse_dates=['Date'],float_precision='round_trip').set_index('Date').Close;cut=pd.Timestamp(f'{year}-06-30');perturbed=price.copy();perturbed.loc[perturbed.index>cut]*=1.7
   check(origin+candidate+'_future_feature_perturbation',local_features(price).loc[:cut].equals(local_features(perturbed).loc[:cut]))
   cal=pd.read_csv((R/d['price_file']).parent/'calendar_private.csv',parse_dates=['Date']);ids=pd.Series(cal.session_id.to_numpy(),index=cal.Date)
   check(origin+candidate+'_exact20_label_end',all((ids.reindex(pd.to_datetime(part['label_end'])).to_numpy()-ids.reindex(pd.to_datetime(part['dates'])).to_numpy()==20).all() for part in dates.values()))
 smoke=json.loads((R/'manifests/step4b_runner_smoke.json').read_text());check('new_runner_actual_synthetic_smoke',smoke['status']=='PASS' and smoke['config_sha256']==sha(cp) and smoke['worker_sha256']==sha(R/'runtime/step4b_worker.py'))
 baseline=json.loads(Path('/workspace/work/step4b/before.json').read_text());check('existing_all_files_unchanged',all(sha(R/p)==h for p,h in baseline.items()))
 # Publication candidates only: operational manifests and datasets are private.
 public=['configs/step4b_pilot_config.json','manifests/step4b_authorization.json','manifests/step4b_job_roster.csv','manifests/step4b_baseline100_metrics.csv']
 for name in public:
  if name.endswith('.csv'):
   frame=pd.read_csv(R/name);check('public_schema_'+name,not {'Date','Close','Target','probability','y_true','y_pred','source_directory'} & set(frame.columns) and '/workspace/' not in (R/name).read_text())
 summary={'stage':'STEP4B','status':'PASS','passed':len(checks),'failed':0,'checks':checks,'config_sha256':sha(cp),'worker_sha256':sha(R/'runtime/step4b_worker.py'),'runner_smoke_sha256':sha(R/'manifests/step4b_runner_smoke.json'),'old100_preserved':True,'new_fit_budget':100,'price_PIT_status':'BLOCKED','source_status':'BOTH_UNVERIFIED','independent_Test_evaluation_enabled':False}
 (R/'manifests/step4b_preflight_results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
if __name__=='__main__':main()
