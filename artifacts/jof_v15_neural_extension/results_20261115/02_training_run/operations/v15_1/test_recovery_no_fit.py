"""Temporary synthetic source-run fixture; no predictive fit/backward/AUC."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import tempfile,tarfile,json,hashlib,importlib.util,random
from unittest.mock import patch
import numpy as np,pandas as pd,torch
sys.path.insert(0,'/repo/artifacts/jof_v15_neural_extension');sys.path.insert(0,str(Path(__file__).parent))
import prepare,worker,base_v15_0_ops as ops
import v15_locked_runner as runner
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier

def forbidden(*a,**kw):raise AssertionError('Forbidden learning/backward/AUC in recovery test')
with patch.object(runner,'fit_predict',side_effect=forbidden),patch.object(torch.Tensor,'backward',side_effect=forbidden),patch.object(LogisticRegression,'fit',side_effect=forbidden),patch.object(LGBMClassifier,'fit',side_effect=forbidden),patch('sklearn.metrics.roc_auc_score',side_effect=forbidden):
 runner.check_lock('/repo','/repo/artifacts/jof_v15_neural_extension/V15_CONFIG_LOCKED.json','/authorization/record.json',require_execution=True)
 jobs=json.loads((prepare.FROZEN/'step4/job_manifest.json').read_text())['jobs'];job=jobs[0];v14=runner.v14_module(Path('/repo'));raw,frame,cols,_=v14.load_market(Path('/repo'),job['Market']);train=v14.records(frame,raw,cols,'2010-01-01',job['Train_end']);ev=v14.records(frame,raw,cols,'2013-01-01','2013-12-31');xtr,xev,scaler,used=runner.window_tensors(train,ev,frame,cols)
 runner.configure_seed(42);model=runner.build_model('LSTM',len(cols)).eval()
 with torch.inference_mode():prob=torch.softmax(model(torch.from_numpy(xev)),1)[:,1]
 with tempfile.TemporaryDirectory(prefix='v15-1-untrained-fixture-',dir='/tmp') as temp:
  t=Path(temp);source=t/'synthetic_source';source.mkdir();d=source/'results/fits'/job['fit_id'];d.mkdir(parents=True)
  torch.save({'state_dict':model.state_dict(),'architecture':'LSTM','input_size':len(cols),'seed':42,'epochs':60,'loss':'CE','probabilities':prob},d/'checkpoint.pt')
  pd.DataFrame({'epoch':range(1,61),'train_loss':np.ones(60)}).to_csv(d/'training_loss.csv',index=False)
  pd.DataFrame({'Date':[r['Date'] for r in ev],'Y_true':[r['y'] for r in ev],'Probability':prob.numpy(),'Y_pred':(prob.numpy()>.5).astype(int)}).to_csv(d/'predictions.csv',index=False,float_format='%.17g')
  meta={'columns':cols,'scaler_mean':scaler.mean_.tolist(),'scaler_scale':scaler.scale_.tolist(),'scaler_var':scaler.var_.tolist(),'scaler_used_rows':used.tolist(),'train_dates':[r['Date'] for r in train],'evaluation_dates':[r['Date'] for r in ev],'input_tensor_sha256':hashlib.sha256(xtr.tobytes()).hexdigest(),'eval_tensor_sha256':hashlib.sha256(xev.tobytes()).hexdigest(),'started_at_utc':ops.now(),'ended_at_utc':ops.now()};(d/'fit_metadata.json').write_text(json.dumps(meta))
  verified=ops.check_job(job,source/'results',runner,v14,{});(source/'operations').mkdir();(source/'operations/fixture.py').write_text('# Synthetic test,no learning\n');(source/'operations_sha256.json').write_text(json.dumps({'fixture.py':ops.sha(source/'operations/fixture.py')}))
  state={'states':{j['fit_id']:'PENDING' for j in jobs},'completed_artifacts':{job['fit_id']:verified}};state['states'][job['fit_id']]='COMPLETE';state['states'][jobs[1]['fit_id']]='FAILED';(source/'job_status.json').write_text(json.dumps(state));partial=source/'results/fits'/jobs[1]['fit_id'];partial.mkdir();(partial/'training_loss.csv').write_text('epoch,train_loss\n1,1.0\n')
  sourceauth=json.loads(Path('/authorization/record.json').read_text());sourceauth['run_id']=source.name;(source/'authorization.json').write_text(json.dumps(sourceauth))
  def make_backup(path):
   with tarfile.open(path,'w:gz') as a:a.add(source,arcname=source.name)
  backup=t/'backup.tar.gz';make_backup(backup);auth=t/'new_auth.json';auth.write_text(json.dumps({**sourceauth,'source_backup_sha256':ops.sha(backup)}));out=t/'prepared';out.mkdir();before={str(p.relative_to(source)):ops.sha(p) for p in source.rglob('*') if p.is_file()}
  prepare.SOURCE=source;prepare.BACKUP=backup;prepare.AUTH=auth;prepare.OUT=out;prepare.main()
  plan=json.loads((out/'recovery_plan.json').read_text());assert plan['reused_count']==1 and plan['new_fit_count']==1079 and len(plan['quarantined_incomplete_jobs'])==1
  assert before=={str(p.relative_to(source)):ops.sha(p) for p in source.rglob('*') if p.is_file()}
  assert (d/'checkpoint.pt').stat().st_ino!=(out/'results/fits'/job['fit_id']/'checkpoint.pt').stat().st_ino,'Must not hardlink preserved source'
  ledger=[];called=[]
  def original(*args,**kwargs):called.append((args,kwargs));return 'fresh-fit-sentinel'
  adapter=worker.make_adapter(original,jobs,plan['reused_jobs'],out/'results',ledger.append)
  torchstate=torch.get_rng_state().clone();randstate=random.getstate();npstate=np.random.get_state()
  cached=adapter('LSTM',train,ev,frame,cols,42,60,'cpu',cfg={},artifact_dir=out/'results/fits'/job['fit_id'],execution_authorized=True)
  np.testing.assert_array_equal(cached,prob.numpy());assert cached.dtype==prob.numpy().dtype and not called;assert torch.equal(torchstate,torch.get_rng_state()) and randstate==random.getstate();np.testing.assert_array_equal(npstate[1],np.random.get_state()[1])
  fresh=jobs[1];sentinel=adapter('LTC',train,ev,frame,cols,42,60,'cpu',cfg={},artifact_dir=out/'results/fits'/fresh['fit_id'],execution_authorized=True)
  assert sentinel=='fresh-fit-sentinel' and called[0][0][1] is train and called[0][0][2] is ev and called[0][0][3] is frame and called[0][0][4] is cols
  # Corrupt an explicitly recorded checksum while maintaining a valid backup/source mirror.
  state['completed_artifacts'][job['fit_id']]['files_sha256']['predictions.csv']='0'*64;(source/'job_status.json').write_text(json.dumps(state));make_backup(backup);auth.write_text(json.dumps({**sourceauth,'source_backup_sha256':ops.sha(backup)}));prepare.OUT=t/'reject';prepare.OUT.mkdir()
  try:prepare.main()
  except ValueError:pass
  else:raise AssertionError('Recorded complete hash corruption accepted')
import controller
controller.main(execute=False)
Path('/runs/recovery_no_fit_test.json').write_text(json.dumps({'status':'PASS','synthetic_only':True,'backup_and_source_inventory_verified':True,'source_files_unchanged':True,'byte_copies_not_hardlinks':True,'partial_job_excluded_for_full_restart':True,'cache_reuse_no_fitting_no_RNG_consumption':True,'cache_miss_arguments_forwarded_unchanged_to_mock':True,'recorded_complete_checksum_corruption_rejected':True,'real_predictive_fits':0,'AUC_calls':0,'backward_calls':0,'temporary_fixtures_removed':True},indent=2)+'\n');print('V15_1_RECOVERY_NO_FIT_TEST_PASS',flush=True)
