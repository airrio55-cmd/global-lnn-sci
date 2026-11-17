"""Prepared STEP3C worker (disabled until a separately approved release); immutable identities, own-Origin data barrier, CPU only."""
from pathlib import Path
import datetime,fcntl,hashlib,importlib.metadata,json,os,platform,random,sys,time,traceback
from zoneinfo import ZoneInfo
MODELS=['RNN','LSTM','GRU','LTC','CfC']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
def write(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
def validate_scope(c,a,g,job,config_sha,worker_sha,preflight_sha):
 from kospi200.step4b_scope import require_scope
 return require_scope(c,a,g,job,config_sha,worker_sha,preflight_sha)

def barrier(root,run,jobdir,origin,notebook):
 allowed=run/'inputs'/origin;state={'forbidden_access_attempts':0,'original_source_reads':0,'origin_input_opens':0}
 def hook(event,args):
  if event!='open' or not args or isinstance(args[0],int):return
  try:p=Path(os.fsdecode(args[0])).resolve()
  except (TypeError,ValueError):return
  if p==notebook:state['original_source_reads']+=1;return
  if p.is_relative_to(jobdir):return
  if p.is_relative_to(allowed):state['origin_input_opens']+=1;return
  if p.is_relative_to(root/'data') or p.is_relative_to(root/'originals') or p.is_relative_to('/workspace/attachments'):
   state['forbidden_access_attempts']+=1;raise PermissionError('Worker may access its own Origin prefix only: '+str(p))
 sys.addaudithook(hook);return state

def execute_job(*,root,config_path,approval_path,preflight_path,job_id,resume=False):
 root=Path(root).resolve();c=json.loads(Path(config_path).read_text());a=json.loads(Path(approval_path).read_text());g=json.loads(Path(preflight_path).read_text())
 job=next((j for j in g['jobs'] if j['run_id']==job_id),None)
 if job is None:raise ValueError('Unapproved fit identity')
 validate_scope(c,a,g,job,sha(config_path),sha(__file__),sha(preflight_path))
 base=json.loads((root/'configs/step3a_pilot_config.json').read_text());prod=json.loads((root/'configs/experiment_config.json').read_text())
 if c['model_settings']!=base['model_settings'] or c['model_seed_offsets']!=base['model_seed_offsets'] or prod['training_enabled'] is not False or prod['hmm_fit_enabled'] is not False:raise ValueError('Settings or production flag changed')
 for row in c['implementation_artifacts']:
  if sha(root/row['file'])!=row['sha256']:raise ValueError('Frozen code changed')
 if {n:importlib.metadata.version(n) for n in c['environment_versions']}!=c['environment_versions']:raise ValueError('Environment changed')
 run=(root/c['run_directory']).resolve();jobdir=run/'jobs'/job_id;permit=json.loads((jobdir/'reservation.json').read_text())
 if permit['job']!=job or permit['config_sha256']!=sha(config_path):raise ValueError('Fit reservation invalid')
 lock=(jobdir/'fit.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 ltc_resource_lock=None
 if job['model']=='LTC':
  ltc_resource_lock=(run/'ltc_resource.lock').open('a');fcntl.flock(ltc_resource_lock,fcntl.LOCK_EX)
 resultpath=jobdir/'result.json'
 if resultpath.exists():
  old=json.loads(resultpath.read_text())
  if old['status'] in ['COMPLETED','FAILED_DIVERGENCE','FAILED_EXCEPTION','BLOCKED']:return old
  if not resume:raise ValueError('Existing fit requires explicit resume')
 info=g['datasets'][job['origin']][job['candidate']]
 for file,hkey in [('array_file','array_sha256'),('date_file','date_sha256'),('metadata_file','metadata_sha256')]:
  if not (root/info[file]).resolve().is_relative_to(run/'inputs'/job['origin']) or sha(root/info[file])!=info[hkey]:raise ValueError('Staged data hash or Origin mismatch')
 notebook=(root/c['source_notebook_file']).resolve()
 if sha(notebook)!=c['source_notebook_sha256']:raise ValueError('Original Notebook changed')
 access=barrier(root,run,jobdir,job['origin'],notebook)
 import numpy as np
 import torch
 from torch import nn
 from ncps.torch import LTC,CfC
 from kospi200.pilot_data import validation_metrics
 from kospi200.smoke_preparation import static_parameter_count
 from runtime.step29_synthetic_smoke import verified_definition_sources
 if str(torch.__version__)!='2.10.0+cpu' or torch.version.cuda is not None or os.environ.get('PYTHONHASHSEED')!='2':raise ValueError('CPU process policy mismatch')
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 if torch.is_autocast_enabled('cpu') or torch.is_autocast_enabled():raise ValueError('AMP forbidden')
 sources=verified_definition_sources(json.loads(notebook.read_text()),c);ns={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':.2}
 for name in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']:exec(compile(sources[name]['source'],'<verified-original-model>','exec'),ns)
 with np.load(root/info['array_file'],allow_pickle=False) as z:arrays={k:z[k].copy() for k in ['train_x','train_y','validation_x','validation_y']}
 meta=json.loads((root/info['metadata_file']).read_text());dates=json.loads((root/info['date_file']).read_text());cutoff=f"{info['validation_year']}-12-31"
 if any(d>cutoff for part in dates.values() for key in ['dates','label_end'] for d in part[key]):raise ValueError('Independent Test endpoint/input violation')
 if arrays['train_x'].shape!=(meta['train_samples'],20,2) or arrays['validation_x'].shape!=(meta['validation_samples'],20,2) or any(not np.isfinite(v).all() for v in arrays.values()):raise ValueError('Invalid array shape/finite')
 if any(arrays[k].dtype!=np.float32 for k in ['train_x','validation_x']) or any(arrays[k].dtype!=np.int64 for k in ['train_y','validation_y']):raise ValueError('Dtype changed')
 tx,ty,vx,vy=[torch.from_numpy(arrays[k]) for k in ['train_x','train_y','validation_x','validation_y']]
 record={**job,'source_stage':'STEP4B_NEW100','status':'RUNNING','started_at_kst':now(),'epochs_completed':0,'best_validation_epoch':None,'train_samples':len(ty),'validation_samples':len(vy),'input_data_sha256':info['array_sha256'],'worker_sha256':sha(__file__),'config_sha256':sha(config_path),'checkpoint_restore':False,'epoch1_resume_roundtrip':False,'RNG_restore_exact':False,'independent_Test_rows_used':0,'2026_used':0}
 write(resultpath,record)
 def equal(x,y):
  if isinstance(x,torch.Tensor):return isinstance(y,torch.Tensor) and torch.equal(x,y)
  if isinstance(x,dict):return x.keys()==y.keys() and all(equal(x[k],y[k]) for k in x)
  if isinstance(x,(list,tuple)):return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
  return x==y
 def rng_state(gen):
  s=np.random.get_state();return {'Python':random.getstate(),'NumPy':{'kind':s[0],'keys':s[1].tolist(),'pos':s[2],'has_gauss':s[3],'cached_gaussian':s[4]},'Torch_CPU':torch.get_rng_state(),'DataLoader':gen.get_state()}
 def restore_rng(s,gen):
  random.setstate(s['Python']);n=s['NumPy'];np.random.set_state((n['kind'],np.array(n['keys'],dtype=np.uint32),n['pos'],n['has_gauss'],n['cached_gaussian']));torch.set_rng_state(s['Torch_CPU']);gen.set_state(s['DataLoader'])
 def save_checkpoint(p,x):
  tmp=p.with_suffix('.pt.tmp');torch.save(x,tmp);os.replace(tmp,p)
 def bundle(steps):
  name=job['model'];model=(ns['RecurrentModel'](2,128,name,1,dropout=.2) if name in ['RNN','LSTM','GRU'] else ns['LNNModel' if name=='LTC' else 'CfCModel'](2,128,dropout=.2)).to(device='cpu',dtype=torch.float32)
  if sum(p.numel() for p in model.parameters() if p.requires_grad)!=static_parameter_count(name,2)['trainable']:raise ValueError('Parameter mismatch')
  if name=='LTC' and model.ltc.rnn_cell._implicit_param_constraints is not True:raise ValueError('LTC constraint mismatch')
  opt=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=1e-4);sch=torch.optim.lr_scheduler.OneCycleLR(opt,max_lr=.005,epochs=100,steps_per_epoch=steps);return model,opt,sch
 def load_bundle(p,steps,gen):
  x=torch.load(p,map_location='cpu',weights_only=True)
  if x['config_sha256']!=sha(config_path) or x['worker_sha256']!=sha(__file__) or x['input_data_sha256']!=info['array_sha256'] or x['job']!=job:raise ValueError('Resume identity mismatch')
  model,opt,sch=bundle(steps);model.load_state_dict(x['model']);opt.load_state_dict(x['optimizer']);sch.load_state_dict(x['scheduler']);restore_rng(x['RNG'],gen);return model,opt,sch,x
 latest=jobdir/'latest.pt';bestpath=jobdir/'best.pt';historypath=jobdir/'history.json'
 try:
  seed=job['effective_seed'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed);gen=torch.Generator().manual_seed(seed)
  loader=torch.utils.data.DataLoader(torch.utils.data.TensorDataset(tx,ty),batch_size=64,shuffle=True,generator=gen,num_workers=0,pin_memory=False)
  criterion=ns['FocalLoss'](gamma=2,alpha=.25);model,opt,sch=bundle(len(loader));history=[];best=-1.;best_epoch=None;counter=0;start=1
  if latest.exists():
   model,opt,sch,x=load_bundle(latest,len(loader),gen);history=x['history'];best=x['early_stopping']['best_score'];best_epoch=x['early_stopping']['best_epoch'];counter=x['early_stopping']['counter'];start=x['completed_epoch']+1;record['resume_from_committed_epoch']=x['completed_epoch']
  print('START',job_id,'seed',seed,'batches',len(loader),flush=True)
  for epoch in range(start,101):
   if counter>=10:break
   then=time.perf_counter();model.train();loss_sum=0.;n=0;steps=0
   for bx,by in loader:
    opt.zero_grad(set_to_none=True);logits=model(bx);loss=criterion(logits,by)
    if logits.shape!=(len(by),2) or not torch.isfinite(loss):raise FloatingPointError('Nonfinite training loss/output')
    loss.backward();grads=[p.grad for p in model.parameters() if p.requires_grad]
    if any(x is None or not torch.isfinite(x).all() for x in grads):raise FloatingPointError('Missing/nonfinite gradients')
    norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
    if not torch.isfinite(norm):raise FloatingPointError('Nonfinite gradient norm')
    opt.step();sch.step();loss_sum+=float(loss.detach())*len(by);n+=len(by);steps+=1
   model.eval()
   with torch.no_grad():vlogits=model(vx);vloss=criterion(vlogits,vy);prob=torch.softmax(vlogits,dim=1)[:,1]
   if not torch.isfinite(vloss) or not torch.isfinite(prob).all():raise FloatingPointError('Nonfinite validation')
   metrics=validation_metrics(arrays['validation_y'],prob.numpy());improved=metrics['validation_BA']>best
   if improved:best=metrics['validation_BA'];best_epoch=epoch;counter=0
   else:counter+=1
   row={'epoch':epoch,'train_loss':loss_sum/n,'validation_loss':float(vloss),**metrics,'optimizer_steps_this_epoch':steps,'scheduler_steps_total':int(sch.last_epoch),'learning_rate':float(opt.param_groups[0]['lr']),'improved_validation_BA':improved,'early_stopping_counter':counter,'epoch_seconds':time.perf_counter()-then};history.append(row)
   payload={'scope':c['execution_mode'],'job':job,'completed_epoch':epoch,'batch_position':0,'resume_granularity':'committed epoch boundary','model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':sch.state_dict(),'early_stopping':{'best_score':best,'best_epoch':best_epoch,'counter':counter,'patience':10,'comparison':'strict greater; ties no improvement'},'RNG':rng_state(gen),'history':history,'feature_order':['Log_Ret','Disparity'],'scaler_metadata':meta['scaler'],'input_data_sha256':info['array_sha256'],'price_data_sha256':info['price_sha256'],'config_sha256':sha(config_path),'worker_sha256':sha(__file__),'environment':{'python':platform.python_version(),'versions':c['environment_versions'],'cpu_threads':1,'dtype':'float32','AMP':False},'environment_sha256':c['environment_sha256'],'code_artifacts':c['implementation_artifacts'],'original_definition_hashes':c['original_definition_hashes'],'independent_Test_access':False}
   save_checkpoint(latest,payload)
   if improved:save_checkpoint(bestpath,payload)
   write(historypath,history);record.update({'epochs_completed':epoch,'best_validation_epoch':best_epoch,'last_validation_BA':metrics['validation_BA'],'elapsed_training_seconds':sum(x['epoch_seconds'] for x in history)})
   if epoch==1:
    state=model.state_dict();opts=opt.state_dict();sched=sch.state_dict();saved_rng=payload['RNG'];new,no,nsch,x=load_bundle(latest,len(loader),gen);new.eval()
    exact=equal(rng_state(gen),saved_rng)
    with torch.no_grad():replay=new(vx)
    if not equal(state,new.state_dict()) or not equal(opts,no.state_dict()) or not equal(sched,nsch.state_dict()) or not torch.equal(vlogits,replay) or not exact:raise RuntimeError('Checkpoint/RNG exact continuation failed')
    model,opt,sch=new,no,nsch;record['epoch1_resume_roundtrip']=True;record['RNG_restore_exact']=True
   write(resultpath,record);print(f'EPOCH {job_id} {epoch:03d} BA={metrics["validation_BA"]:.6f} best={best:.6f}@{best_epoch} wait={counter} pred_pos={metrics["prediction_positive_rate"]:.4f} seconds={row["epoch_seconds"]:.3f}',flush=True)
   if counter>=10:break
  selected,_,_,x=load_bundle(bestpath,len(loader),gen);selected.eval()
  with torch.no_grad():selected_probs=torch.softmax(selected(vx),dim=1)[:,1].numpy()
  measured=validation_metrics(arrays['validation_y'],selected_probs);expected=next(h for h in history if h['epoch']==best_epoch)
  if any(measured[k]!=expected[k] for k in measured):raise RuntimeError('Best checkpoint validation mismatch')
  np.savez(jobdir/'validation_predictions_private.npz',dates=np.array(dates['validation']['dates']),y_true=arrays['validation_y'],probability=selected_probs)
  record.update({'status':'COMPLETED','finished_at_kst':now(),'metrics':measured,'prediction_status':measured['prediction_status'],'checkpoint_restore':True,'best_checkpoint_sha256':sha(bestpath),'latest_checkpoint_sha256':sha(latest),'history_sha256':sha(historypath),'validation_predictions_sha256':sha(jobdir/'validation_predictions_private.npz'),'epochs_with_degenerate_prediction':sum(h['prediction_status']=='DEGENERATE_PREDICTION' for h in history),'degenerate_epoch_ratio':sum(h['prediction_status']=='DEGENERATE_PREDICTION' for h in history)/len(history),'stopped_early':len(history)<100,'full_fresh_retrain_repeated':False})
  print('DONE',job_id,'epochs',len(history),'best',best_epoch,'BA',measured['validation_BA'],measured['prediction_status'],flush=True)
 except KeyboardInterrupt:
  record.update({'status':'INTERRUPTED','error':'Resume same fit at last committed epoch'});record['file_access_barrier']=access;write(resultpath,record);raise
 except Exception as exc:
  record.update({'status':'FAILED_DIVERGENCE' if isinstance(exc,FloatingPointError) else 'FAILED_EXCEPTION','error':str(exc),'error_type':type(exc).__name__,'finished_at_kst':now()});(jobdir/'error.log').write_text(traceback.format_exc());print('FAIL',job_id,type(exc).__name__,str(exc),flush=True)
 record['file_access_barrier']=access;write(resultpath,record);return record
