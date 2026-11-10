"""Temporary synthetic artifact fixtures only: no optimization,backward,AUC or training."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,tempfile,datetime,hashlib
from unittest.mock import patch
import numpy as np,pandas as pd,torch
spec=importlib.util.spec_from_file_location('operations','/operations/run-v15-container.py');ops=importlib.util.module_from_spec(spec);spec.loader.exec_module(ops)
sys.path.insert(0,str(ops.FROZEN));import v15_locked_runner as frozen
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier

def forbidden(*a,**kw):raise AssertionError('No training,backward,AUC or estimator fit allowed in launcher test')
with patch.object(torch.Tensor,'backward',side_effect=forbidden),patch.object(LogisticRegression,'fit',side_effect=forbidden),patch.object(LGBMClassifier,'fit',side_effect=forbidden),patch('sklearn.metrics.roc_auc_score',side_effect=forbidden):
 with patch.object(ops.subprocess,'Popen',side_effect=forbidden):
  # Lock checking itself uses subprocess,so do not call main while globally patching subprocess.Popen.
  pass
 v14=frozen.v14_module(ops.ROOT);job=json.loads((ops.FROZEN/'step4/job_manifest.json').read_text())['jobs'][0]
 raw,frame,cols,_=v14.load_market(ops.ROOT,job['Market']);train=v14.records(frame,raw,cols,'2010-01-01',job['Train_end']);ev=v14.records(frame,raw,cols,'2013-01-01','2013-12-31');xtr,xev,scaler,used=frozen.window_tensors(train,ev,frame,cols)
 frozen.configure_seed(42);model=frozen.build_model('LSTM',len(cols)).eval();torch.set_num_threads(2)
 # Constructor/scheduler import test only,no optimizer step or gradients.
 optimizer=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=.0001);scheduler=torch.optim.lr_scheduler.OneCycleLR(optimizer,max_lr=.005,steps_per_epoch=1,epochs=60)
 with torch.inference_mode():prob=torch.softmax(model(torch.from_numpy(xev)),1)[:,1]
 with tempfile.TemporaryDirectory(prefix='v15-ops-synthetic-',dir='/tmp') as tmp:
  base=Path(tmp);d=base/'fits'/job['fit_id'];d.mkdir(parents=True);torch.save({'state_dict':model.state_dict(),'architecture':'LSTM','input_size':len(cols),'seed':42,'epochs':60,'loss':'CE','probabilities':prob},d/'checkpoint.pt')
  #60 is a schema fixture,not a claim of training. All files are removed on exit.
  pd.DataFrame({'epoch':range(1,61),'train_loss':np.ones(60)}).to_csv(d/'training_loss.csv',index=False)
  pd.DataFrame({'Date':[r['Date'] for r in ev],'Y_true':[r['y'] for r in ev],'Probability':prob.numpy(),'Y_pred':(prob.numpy()>.5).astype(int)}).to_csv(d/'predictions.csv',index=False,float_format='%.17g')
  meta={'columns':cols,'scaler_mean':scaler.mean_.tolist(),'scaler_scale':scaler.scale_.tolist(),'scaler_var':scaler.var_.tolist(),'scaler_used_rows':used.tolist(),'train_dates':[r['Date'] for r in train],'evaluation_dates':[r['Date'] for r in ev],'input_tensor_sha256':hashlib.sha256(xtr.tobytes()).hexdigest(),'eval_tensor_sha256':hashlib.sha256(xev.tobytes()).hexdigest(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};(d/'fit_metadata.json').write_text(json.dumps(meta))
  result=ops.check_job(job,base,frozen,v14,{});assert result['checkpoint_replay']=='PASS'
  bad=pd.read_csv(d/'predictions.csv');bad.loc[0,'Probability']=float('nan');bad.to_csv(d/'predictions.csv',index=False)
  try:ops.check_job(job,base,frozen,v14,{})
  except AssertionError:pass
  else:raise AssertionError('Corruption not rejected')
ops.main(execute=False)
Path('/runs/launcher_no_fit_test.json').write_text(json.dumps({'status':'PASS','synthetic_completed_artifact_validation':True,'corrupt_probability_rejected':True,'read_only_image_optimizer_constructor_only':True,'training_steps':0,'backward_calls':0,'AUC_calls':0,'temporary_synthetic_fixtures_removed':True},indent=2)+'\n')
print('LAUNCHER_NO_FIT_TEST_PASS',flush=True)
