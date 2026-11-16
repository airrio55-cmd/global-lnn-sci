"""Post-fit same-Validation checkpoint roundtrip; no optimizer updates or Test inputs."""
from pathlib import Path
import hashlib,json,random,platform

def audit_checkpoint(root,config,preflight,job_id,record):
 import numpy as np
 import torch
 from torch import nn
 from ncps.torch import LTC,CfC
 from runtime.step29_synthetic_smoke import verified_definition_sources
 from kospi200.pilot_data import validation_metrics
 root=Path(root);c=json.loads(Path(config).read_text());g=json.loads(Path(preflight).read_text());job=next(x for x in g['jobs'] if x['run_id']==job_id);dest=root/c['run_directory']/'jobs'/job_id;info=g['datasets']['O3'][job['candidate']]
 def eq(a,b):
  if isinstance(a,torch.Tensor):return isinstance(b,torch.Tensor) and torch.equal(a,b)
  if isinstance(a,dict):return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
  if isinstance(a,(list,tuple)):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
  return a==b
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 ns={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':.2};sources=verified_definition_sources(json.loads((root/c['source_notebook_file']).read_text()),c)
 for name in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']:exec(compile(sources[name]['source'],'<verified-original-model-checkpoint-only>','exec'),ns)
 with np.load(root/info['array_file'],allow_pickle=False) as z:vx=torch.from_numpy(z['validation_x'].copy());vy=z['validation_y'].copy()
 payload=torch.load(dest/'best.pt',map_location='cpu',weights_only=True)
 if payload['job']!=job or payload['feature_order']!=['Log_Ret','Disparity'] or payload['input_data_sha256']!=info['array_sha256']:raise ValueError('Checkpoint identity/feature/data mismatch')
 if payload['config_sha256']!=sha(Path(config)) or payload['scaler_metadata']!=info['metadata']['scaler']:raise ValueError('Checkpoint config/scaler mismatch')
 tmp=dest/'checkpoint_roundtrip_private.pt';torch.save(payload,tmp);reload=torch.load(tmp,map_location='cpu',weights_only=True)
 if not eq(payload,reload):raise ValueError('Full payload model/optimizer/scheduler/EarlyStopping/RNG roundtrip failed')
 def restore(p):
  model=(ns['RecurrentModel'](2,128,job['model'],1,dropout=.2) if job['model'] in ['RNN','LSTM','GRU'] else ns['LNNModel' if job['model']=='LTC' else 'CfCModel'](2,128,dropout=.2)).to(device='cpu',dtype=torch.float32);model.load_state_dict(p['model']);model.eval();return model
 a,b=restore(payload),restore(reload)
 with torch.no_grad():la=a(vx);lb=b(vx);prob=torch.softmax(la,dim=1)[:,1].numpy()
 if not torch.equal(la,lb):raise ValueError('Independent best checkpoint reload logits differ')
 with np.load(dest/'validation_predictions_private.npz',allow_pickle=False) as z:
  if not np.array_equal(prob,z['probability']):raise ValueError('Best restored probability differs from completed fit')
 # Rebuild and restore optimizer/scheduler states without stepping either.
 opt=torch.optim.AdamW(b.parameters(),lr=.005,weight_decay=1e-4);sch=torch.optim.lr_scheduler.OneCycleLR(opt,max_lr=.005,epochs=100,steps_per_epoch=(info['metadata']['train_samples']+63)//64);opt.load_state_dict(reload['optimizer']);sch.load_state_dict(reload['scheduler'])
 if not eq(opt.state_dict(),payload['optimizer']) or not eq(sch.state_dict(),payload['scheduler']):raise ValueError('Optimizer/scheduler restoration failed')
 state=payload['RNG'];random.setstate(state['Python']);n=state['NumPy'];np.random.set_state((n['kind'],np.asarray(n['keys'],dtype=np.uint32),n['pos'],n['has_gauss'],n['cached_gaussian']));torch.set_rng_state(state['Torch_CPU']);gen=torch.Generator();gen.set_state(state['DataLoader'])
 now_np=np.random.get_state();numpy_exact=now_np[0]==n['kind'] and np.array_equal(now_np[1],np.asarray(n['keys'],dtype=np.uint32)) and now_np[2:]==(n['pos'],n['has_gauss'],n['cached_gaussian'])
 if not numpy_exact or random.getstate()!=state['Python'] or not torch.equal(torch.get_rng_state(),state['Torch_CPU']) or not torch.equal(gen.get_state(),state['DataLoader']):raise ValueError('RNG restore failed')
 check={'status':'PASS','best_checkpoint_logits_equal_two_independent_restores':True,'best_probability_equal_completed_fit':True,'full_model_optimizer_scheduler_earlystop_RNG_roundtrip':True,'feature_scaler_data_config_hashes_verified':True,'epoch1_training_logits_roundtrip':record['epoch1_resume_roundtrip'],'original_best_epoch_logits_stored':False,'comparison_limit':'Best reload logits compare two payload restores and completed best probability; epoch1 compares original training logits exactly','additional_optimizer_updates':0,'Test_rows_used':0,'best_checkpoint_sha256':sha(dest/'best.pt'),'roundtrip_sha256':sha(tmp),'logits_shape':list(la.shape),'early_stopping':payload['early_stopping']}
 p=dest/'checkpoint_verification.json';p.write_text(json.dumps(check,indent=2)+'\n');return check,sha(p)
