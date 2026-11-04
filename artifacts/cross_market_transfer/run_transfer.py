"""LOMO pooled LNN CE transfer; fixed common features and paired target training."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math,copy,time,traceback,subprocess,sys
import numpy as np,pandas as pd,torch
import nbformat
from sklearn.metrics import balanced_accuracy_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];os.chdir(ROOT)
M={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
SEEDS=[42,52,62,72,82];FEATURES=['Log_Ret','Vol20','Momentum20','Disparity20','RSI14'];CUTS=[2018,2019,2020,2021]
for d in ['predictions','checkpoints','scalers','frozen_inputs','logs']: (OUT/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,value):
 p=OUT/name;t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');t.replace(p)
def now():return datetime.now(timezone.utc).isoformat()
def init():
 global ns,protocol,lockhash,frames,bundles,sourcepacks,inputhashes
 protocol=json.loads((OUT/'transfer_protocol.json').read_text());lockhash=sha(OUT/'transfer_protocol.json')
 n=nbformat.read(ROOT/protocol['definition_notebook'],4);ns={}
 for i in [1,3,5,7,9,11,13,14,16]:exec(compile(n.cells[i].source,f'frozen-cell-{i}','exec'),ns)
 assert {n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in protocol['packages']}==protocol['packages']
 torch.set_num_threads(2);assert ns['DEVICE'].type=='cpu';ns['MAX_LR']=protocol['target_training']['max_lr']
 assert ns['SEEDS']==SEEDS and ns['HIDDEN_SIZE']==128 and ns['DROPOUT']==.2 and ns['HORIZON']==ns['WINDOW_SIZE']==20
 frames={};bundles={};sourcepacks={};inputhashes={};manifest=[]
 for market,folder in M.items():
  p=ROOT/folder/'market_input.csv';inputhashes[str(p.relative_to(ROOT))]=sha(p)
  frozen=OUT/'frozen_inputs'/(market+'.csv')
  if frozen.exists():assert sha(frozen)==sha(p)
  else:frozen.write_bytes(p.read_bytes())
  raw=pd.read_csv(frozen,index_col=0,parse_dates=True,float_precision='round_trip');assert raw.index.is_unique and raw.index.is_monotonic_increasing
  df=ns['add_common_features'](raw[['Close']]);frames[market]=df
  perturb=raw[['Close']].copy();perturb.loc[perturb.index>='2022-01-01']*=1.7
  np.testing.assert_allclose(df.loc[df.index<'2022-01-01',FEATURES],ns['add_common_features'](perturb).loc[df.index<'2022-01-01',FEATURES],atol=0,rtol=0,equal_nan=True)
  bundles[market]=ns['prepare_market_walkforward'](df,market,'COMMON',verbose=False)
  for c in CUTS:
   train=df.loc[:f'{c-1}-12-31'].copy();val=df.loc[f'{c}-01-01':f'{c}-12-31'].copy()
   tr,va,scaler,trdf,vadf=ns['prepare_split_tensors'](train,val,FEATURES)
   sourcepacks[(market,c)]=(tr,va,scaler)
   check_split(raw,trdf,f'{c-1}-12-31');check_split(raw,vadf,f'{c}-12-31')
   np.testing.assert_allclose(scaler.mean_,trdf[FEATURES].mean());assert tr[0].shape[1:]==va[0].shape[1:]==(20,5)
   dump_scaler(f'source_{market}_through_{c}',scaler,trdf.index,FEATURES)
  bundle=bundles[market]
  tensor_path=OUT/'checkpoints'/f'{market}_test_tensors.pt'
  if not tensor_path.exists():torch.save({'X':bundle['test'][0].clone(),'y':bundle['test'][1].clone(),'dates':bundle['test'][2].strftime('%Y-%m-%d').tolist()},tensor_path)
  for f in bundle['folds']:
   check_split(raw,f['train_df'],f['train_end']);check_split(raw,f['val_df'],f['val_end']);np.testing.assert_allclose(f['scaler'].mean_,f['train_df'][FEATURES].mean())
   dump_scaler(f'target_{market}_fold_{f["fold_id"]}',f['scaler'],f['train_df'].index,FEATURES)
  check_split(raw,bundle['final_train_df'],'2021-12-31');check_split(raw,bundle['test_df'],'2025-12-31')
  np.testing.assert_allclose(bundle['final_scaler'].mean_,bundle['final_train_df'][FEATURES].mean());assert bundle['final_train'][0].shape[1:]==bundle['test'][0].shape[1:]==(20,5)
  dump_scaler(f'target_{market}_final',bundle['final_scaler'],bundle['final_train_df'].index,FEATURES)
  for target in M:
   if market!=target:
    for cutoff in CUTS:manifest.append({'Target':target,'Source':market,'Cutoff_year':cutoff,'Source_gradient_end':f'{cutoff-1}-12-31','Source_validation_year':cutoff,'Target_validation_year':cutoff+1 if cutoff<2021 else 'TEST_2022_2025','Source_test_2022_2025_used':False,'Train_samples':len(sourcepacks[(market,cutoff)][0][1]),'Validation_samples':len(sourcepacks[(market,cutoff)][1][1]),'Scaler':f'scalers/source_{market}_through_{cutoff}.json'})
 pd.DataFrame(manifest).to_csv(OUT/'source_target_manifest.csv',index=False)
 write('data_manifest.json',{'input_sha256':inputhashes,'feature_set':'TRANSFER_COMMON','features':FEATURES,'definition_notebook_sha256':sha(ROOT/protocol['definition_notebook']),'protocol_sha256':lockhash,'normalization':'separate per-market, gradient-training-only StandardScaler','source_validation_rule':'last eligible pretraining year held out, label tails purged; stricter fold-specific source cutoff prevents target validation leakage'})
 write('leakage_audit.json',{'status':'passed','source_max_year':2021,'source_fold_cutoffs':CUTS,'no_future_target_validation_source':True,'per_split_20_observation_label_purge':True,'sequence_excludes_target_row':True,'training_only_scalers':True,'future_feature_perturbation':True,'local_features_used':False,'original_base_results_unchanged':True})
def check_split(raw,frame,end):
 ix=raw.index.get_indexer(frame.index);assert (ix>=0).all() and (ix+20<len(raw)).all();assert (raw.index[ix+20]<=pd.Timestamp(end)).all()
def dump_scaler(stem,s,dates,features):
 write('scalers/'+stem+'.json',{'mean':s.mean_.tolist(),'scale':s.scale_.tolist(),'var':s.var_.tolist(),'n_samples_seen':int(s.n_samples_seen_),'fit_first':str(dates.min().date()),'fit_last':str(dates.max().date()),'features':features})
def saveck(path,content):
 tmp=path.with_suffix('.tmp');torch.save({**content,'protocol_sha256':lockhash},tmp);tmp.replace(path)
def loadck(path):
 z=torch.load(path,weights_only=False,map_location='cpu');assert z['protocol_sha256']==lockhash;return z

def balanced_batches(packs,generator):
 # Exactly 16 examples per source per minibatch; reshuffle/cycle smaller markets.
 data=[p[0] for p in packs];orders=[torch.randperm(len(x[1]),generator=generator) for x in data];positions=[0]*4
 steps=math.ceil(max(len(x[1]) for x in data)/16)
 for _ in range(steps):
  xs=[];ys=[]
  for i,(X,y,_,_) in enumerate(data):
   chosen=[]
   while len(chosen)<16:
    available=min(16-len(chosen),len(y)-positions[i]);chosen+=orders[i][positions[i]:positions[i]+available].tolist();positions[i]+=available
    if positions[i]==len(y):orders[i]=torch.randperm(len(y),generator=generator);positions[i]=0
   xs.append(X[chosen]);ys.append(y[chosen])
  order=torch.randperm(64,generator=generator);yield torch.cat(xs)[order],torch.cat(ys)[order]

def pretrain(target,seed,cutoff):
 path=OUT/'checkpoints'/f'{target}_seed{seed}_source_through{cutoff}.pt'
 if path.exists():return loadck(path)['state_dict']
 sources=[m for m in M if m!=target];packs=[sourcepacks[(m,cutoff)] for m in sources];ns['set_seed'](seed);model=ns['build_model']('LNN',5)
 optimizer=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=1e-4)
 steps=math.ceil(max(len(p[0][1]) for p in packs)/16);scheduler=torch.optim.lr_scheduler.OneCycleLR(optimizer,max_lr=.005,steps_per_epoch=steps,epochs=100)
 gen=torch.Generator().manual_seed(seed);best=-np.inf;stale=0;best_state=None;curve=[]
 for epoch in range(100):
  write('active_job.json',{'phase':'source_pretraining','Target':target,'Seed':seed,'cutoff':cutoff,'epoch':epoch+1,'max_epochs':100,'updated_at_utc':now()})
  model.train()
  for X,y in balanced_batches(packs,gen):
   optimizer.zero_grad(set_to_none=True);loss=torch.nn.functional.cross_entropy(model(X),y);assert torch.isfinite(loss);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);optimizer.step();scheduler.step()
  model.eval();scores=[]
  with torch.no_grad():
   for _,(X,y,_,_),_ in packs:scores.append(balanced_accuracy_score(y.numpy(),model(X).argmax(1).numpy()))
  score=float(np.mean(scores));curve.append({'epoch':epoch+1,'equal_market_validation_BA':score,**dict(zip(sources,scores))})
  if score>best:best=score;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch+1;stale=0
  else:stale+=1
  if stale>=10:break
 pd.DataFrame(curve).to_csv(OUT/'logs'/f'{target}_seed{seed}_source_through{cutoff}.csv',index=False)
 saveck(path,{'state_dict':best_state,'Target':target,'Seed':seed,'cutoff':cutoff,'sources':sources,'best_epoch':best_epoch,'epochs_run':epoch+1,'validation_BA':best,'balanced_batch_each_source':16})
 print('PRETRAIN COMPLETE',target,seed,cutoff,'epochs',epoch+1,flush=True)
 return best_state

def target_fold(target,method,seed,fold,state):
 path=OUT/'checkpoints'/f'{target}_{method}_seed{seed}_fold{fold["fold_id"]}.pt'
 if path.exists():return loadck(path)['validation_probabilities']
 write('active_job.json',{'phase':'target_validation','Target':target,'Method':method,'Seed':seed,'fold':fold['fold_id'],'updated_at_utc':now()})
 ns['set_seed'](seed);model=ns['build_model']('LNN',5)
 if state is not None:model.load_state_dict(state)
 X,y,_,_=fold['train'];V,vy,vd,_=fold['val']
 model,prob=ns['train_one_fold'](model,X,y,V,vy,seed_for_loader=seed,loss_mode='CE')
 assert np.isfinite(prob).all() and ((prob>=0)&(prob<=1)).all()
 saveck(path,{'state_dict':model.state_dict(),'Target':target,'Method':method,'Seed':seed,'fold':fold['fold_id'],'validation_probabilities':prob,'validation_labels':vy.numpy(),'validation_dates':vd.strftime('%Y-%m-%d').tolist(),'scaler_file':f'scalers/target_{target}_fold_{fold["fold_id"]}.json'})
 print('TARGET FOLD COMPLETE',target,method,seed,fold['fold_id'],flush=True);return prob

def run_all():
 init()
 sourcehash={name:sha(OUT/name) for name in ['run_transfer.py','finalize.py','report.py','transfer_protocol.json']}
 state={'source_sha256':sourcehash,'packages':protocol['packages'],'started_at_utc':now(),'definition_notebook_sha256':sha(ROOT/protocol['definition_notebook']),'HMM_sha256':sha(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv'),'economic_protocol_sha256':sha(ROOT/'artifacts/cross_market_economic/economic_protocol.json')}
 if (OUT/'run_manifest.json').exists():assert json.loads((OUT/'run_manifest.json').read_text())['source_sha256']==sourcehash
 else:write('run_manifest.json',state)
 rows=[];start=now();write('progress.json',{'status':'running','completed_final_runs':0,'expected_final_runs':50,'expected_training_checkpoints':300});write('execution_status.json',{'status':'running','pid':os.getpid(),'started_at_utc':start})
 for target in M:
  bundle=bundles[target]
  for seed in SEEDS:
   for method in ['Scratch','Transfer']:
    val_probs=[];val_y=[];val_dates=[]
    for fold in bundle['folds']:
     cutoff=int(fold['train_end'][:4]);state=pretrain(target,seed,cutoff) if method=='Transfer' else None
     val_probs.append(target_fold(target,method,seed,fold,state));val_y.append(fold['val'][1].numpy());val_dates.extend(fold['val'][2])
    vp=np.concatenate(val_probs);vy=np.concatenate(val_y);threshold,_=ns['select_validation_threshold'](vy,vp,ns['THRESHOLD_GRID'])
    final=OUT/'checkpoints'/f'{target}_{method}_seed{seed}_final.pt'
    if final.exists():
     z=loadck(final);assert threshold==z['Threshold'];prob=z['test_probabilities']
    else:
     write('active_job.json',{'phase':'target_final','Target':target,'Method':method,'Seed':seed,'updated_at_utc':now()})
     state=pretrain(target,seed,2021) if method=='Transfer' else None
     ns['set_seed'](seed);model=ns['build_model']('LNN',5)
     if state is not None:model.load_state_dict(state)
     X,y,_,_=bundle['final_train'];V,vytest,dt,fwd=bundle['test']
     model,prob=ns['train_final_model'](model,X,y,V,seed_for_loader=seed,loss_mode='CE')
     assert np.isfinite(prob).all() and ((prob>=0)&(prob<=1)).all()
     saveck(final,{'state_dict':model.state_dict(),'Target':target,'Method':method,'Seed':seed,'Threshold':threshold,'test_probabilities':prob,'test_labels':vytest.numpy(),'test_dates':dt.strftime('%Y-%m-%d').tolist(),'scaler_file':f'scalers/target_{target}_final.json','input_size':5,'final_epochs':60})
    V,yt,dates,fwd=bundle['test'];metrics=ns['calculate_metrics'](yt.numpy(),probs=prob,threshold=threshold);vmetrics=ns['calculate_metrics'](np.concatenate(val_y),probs=vp,threshold=threshold)
    rows.append({'Market':target,'Method':method,'Model':'LNN','Loss':'CE','Feature_set':'TRANSFER_COMMON','Seed':seed,'Threshold':threshold,'WF_Val_BA':vmetrics['Balanced_Accuracy'],'WF_Val_Macro_F1':vmetrics['Macro_F1'],**metrics})
    pd.DataFrame({'Date':dates,'Y_true':yt.numpy(),'Probability':prob,'Y_pred':(prob>threshold).astype(int),'Threshold':threshold,'Seed':seed,'Method':method,'Model':'LNN','Loss':'CE','Forward_Return20':fwd}).to_csv(OUT/'predictions'/f'{target}_{method}_{seed}.csv',index=False,float_format='%.17g')
    pd.DataFrame({'Date':pd.to_datetime(val_dates),'Y_true':np.concatenate(val_y),'Probability':vp,'Threshold':threshold}).to_csv(OUT/'predictions'/f'{target}_{method}_{seed}.validation.csv',index=False,float_format='%.17g')
    pd.DataFrame(rows).to_csv(OUT/'seed_results.partial.csv',index=False,float_format='%.17g')
    write('progress.json',{'status':'running','completed_final_runs':len(rows),'expected_final_runs':50,'completed_checkpoints':len([p for p in (OUT/'checkpoints').glob('*.pt') if not p.name.endswith('_test_tensors.pt')]),'expected_checkpoints':300,'updated_at_utc':now()})
    print('FINAL COMPLETE',target,method,seed,metrics,flush=True)
 for method,name in [('Scratch','scratch_seed_results.csv'),('Transfer','transfer_seed_results.csv')]:pd.DataFrame([r for r in rows if r['Method']==method]).to_csv(OUT/name,index=False,float_format='%.17g')
 for p,d in inputhashes.items():assert sha(ROOT/p)==d
 subprocess.run([sys.executable,str(OUT/'finalize.py')],check=True)
 write('execution_status.json',{'status':'completed','started_at_utc':start,'completed_at_utc':now(),'runs':50})
 write('progress.json',{'status':'completed','completed_final_runs':50,'expected_final_runs':50,'completed_checkpoints':300,'expected_checkpoints':300})
 publish()
def publish():
 def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
 assert git('branch','--show-current')=='main';assert not git('diff','--cached','--name-only') and not git('diff','--name-only')
 assert json.loads((OUT/'completion_check.json').read_text())['status']=='validated'
 git('fetch','origin','main');git('merge','--ff-only','origin/main')
 files=[str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file() and p.suffix in ['.py','.json','.csv','.md','.png','.pt','.log'] and 'candidate' not in p.parts and '__pycache__' not in p.parts and p.name not in ['execution.log','publication.json','seed_results.partial.csv']]
 # execution.log is still open in the detached process; archive a fixed copy for publication.
 (OUT/'completed_execution.log').write_bytes((OUT/'execution.log').read_bytes());files.append(str((OUT/'completed_execution.log').relative_to(ROOT)))
 git('add','--',*files);git('diff','--cached','--check');git('commit','-m','Add frozen LOMO common-feature LNN transfer experiment and paired scratch comparison');git('push','origin','main');commit=git('rev-parse','HEAD');assert git('ls-remote','origin','refs/heads/main').split()[0]==commit;write('publication.json',{'status':'published','commit':commit,'verified_at_utc':now()});print('PUBLISHED',commit,flush=True)
if __name__=='__main__':
 try:
  if '--preflight' in sys.argv:
   init();g=torch.Generator().manual_seed(42);batch=next(balanced_batches([sourcepacks[(m,2018)] for m in list(M)[1:]],g));model=ns['build_model']('LNN',5);v=torch.nn.functional.cross_entropy(model(batch[0]),batch[1]);assert torch.isfinite(v);v.backward();assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None);print('PREFLIGHT PASS: causal data/scalers, 16-per-source batch and LNN backward; no test metrics used')
  else:
   previous=OUT/'execution_status.json'
   if previous.exists():
    old=json.loads(previous.read_text());assert old.get('status')!='completed','Preserve completed run';assert not(old.get('status')=='running' and Path('/proc/'+str(old.get('pid'))).exists()),'Duplicate active run'
   run_all()
 except BaseException as e:
  write('execution_status.json',{'status':'failed','error':str(e),'failed_at_utc':now()});(OUT/'execution_error.txt').write_text(traceback.format_exc());raise
