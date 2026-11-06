"""Frozen Phase1: validation-first GRU/logistic/LightGBM, then untouched test."""
import os
for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[key]='2'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,time,traceback,warnings,copy
import numpy as np,pandas as pd,torch,nbformat,joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from lightgbm import LGBMClassifier
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];os.chdir(ROOT)
M={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
S=[42,52,62,72,82];LOSSES=['CE','MILD_WCE','MILD_FOCAL'];NEW=['GRU','LogisticRegression','LightGBM'];ACTIVE={}
for d in ['all_predictions','checkpoints','scalers','frozen_features','diagnostics','figures']: (OUT/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def js(name,x):
 p=OUT/name;t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n');t.replace(p)
def activity(**fields):
 global ACTIVE
 ACTIVE=fields;js('active_job.json',{**ACTIVE,'updated_at_utc':now()})
def savept(p,x):
 tmp=p.with_suffix('.tmp');torch.save({**x,'protocol_sha256':LOCKHASH},tmp);tmp.replace(p)
def loadpt(p):
 x=torch.load(p,weights_only=False,map_location='cpu');assert x['protocol_sha256']==LOCKHASH;return x

def setup():
 global LOCK,LOCKHASH,NS,BUNDLES,FRAMES,RAW,INPUTHASH
 LOCK=json.loads((OUT/'protocol_lock.json').read_text());LOCKHASH=sha(OUT/'protocol_lock.json')
 import importlib.metadata
 assert {n:importlib.metadata.version(n) for n in LOCK['packages']}==LOCK['packages']
 NS={};BUNDLES={};FRAMES={};RAW={};INPUTHASH={};columns=[];data=[]
 existing=pd.read_csv(ROOT/'artifacts/validation_selected_statistical_robustness/selected_primary_configs.csv')
 for market,folder in M.items():
  directory=ROOT/folder;name=LOCK['notebooks'][market];assert sha(directory/name)==LOCK['notebook_sha256'][market];notebook=nbformat.read(directory/name,4);ns={}
  for i in [1,3,5,7,9,11,13,14]:exec(compile(notebook.cells[i].source,f'{market}-frozen-cell-{i}','exec'),ns)
  torch.set_num_threads(2);assert ns['DEVICE'].type=='cpu';assert ns['HORIZON']==ns['WINDOW_SIZE']==20
  assert (ns['HIDDEN_SIZE'],ns['NUM_LAYERS'],ns['DROPOUT'],ns['MAX_LR'],ns['EPOCHS'],ns['PATIENCE'],ns['BATCH_SIZE'],ns['FOCAL_GAMMA'])==(128,1,.2,.005,100,10,64,1.)
  path=directory/'market_input.csv';INPUTHASH[str(path.relative_to(ROOT))]=sha(path);raw=pd.read_csv(path,index_col=0,parse_dates=True,float_precision='round_trip');RAW[market]=raw
  assert raw.index.is_unique and raw.index.is_monotonic_increasing and raw.Close.gt(0).all()
  processed=directory/'feature_input.csv';frozen=OUT/'frozen_features'/f'{market}.csv'
  if processed.exists():
   INPUTHASH[str(processed.relative_to(ROOT))]=sha(processed)
   if frozen.exists():assert sha(frozen)==sha(processed)
   else:frozen.write_bytes(processed.read_bytes())
   how='Exact existing processed feature_input.csv, byte-preserved'
  else:
   if not frozen.exists():ns['add_common_features'](raw).to_csv(frozen,float_format='%.17g')
   how='No processed file exists: original market-specific feature cell applied to original frozen market_input.csv; saved once with17digit precision'
  df=pd.read_csv(frozen,index_col=0,parse_dates=True,float_precision='round_trip');FRAMES[market]=df
  assert df.index.equals(raw.index);np.testing.assert_allclose(df.Close,raw.Close,atol=0,rtol=0)
  features=ns['get_feature_columns'](df,market,'COMMON_LOCAL')
  source_audit=directory/'leakage_audit.json';INPUTHASH[str(source_audit.relative_to(ROOT))]=sha(source_audit);assert features==json.loads(source_audit.read_text())['features']
  candidate=raw.copy();candidate.loc[candidate.index>='2022-01-01']*=1.7
  before=ns['add_common_features'](raw);changed=ns['add_common_features'](candidate);np.testing.assert_allclose(before.loc[before.index<'2022-01-01',features],changed.loc[changed.index<'2022-01-01',features],equal_nan=True,atol=0,rtol=0)
  bundle=ns['prepare_market_walkforward'](df,market,'COMMON_LOCAL',verbose=False);BUNDLES[market]=bundle
  for fold in bundle['folds']:
   audit_split(raw,fold['train_df'],fold['train_end'],fold['train'],len(features));audit_split(raw,fold['val_df'],fold['val_end'],fold['val'],len(features));np.testing.assert_allclose(fold['scaler'].mean_,fold['train_df'][features].mean())
   scaler_json(f'{market}_fold{fold["fold_id"]}',fold['scaler'],features,fold['train_df'].index)
  audit_split(raw,bundle['final_train_df'],'2021-12-31',bundle['final_train'],len(features));audit_split(raw,bundle['test_df'],'2025-12-31',bundle['test'],len(features));np.testing.assert_allclose(bundle['final_scaler'].mean_,bundle['final_train_df'][features].mean())
  scaler_json(f'{market}_final',bundle['final_scaler'],features,bundle['final_train_df'].index)
  # Labels/dates only: identity audit, never a selection score.
  ref=directory/'predictions/LSTM_CE_42.csv';INPUTHASH[str(ref.relative_to(ROOT))]=sha(ref);ref=pd.read_csv(ref,usecols=['Date','Y_true']);assert np.array_equal(pd.to_datetime(ref.Date),bundle['test'][2]) and np.array_equal(ref.Y_true,bundle['test'][1].numpy())
  for r in existing[existing.Market==market].itertuples():
   summary_path=directory/'summary.csv';INPUTHASH[str(summary_path.relative_to(ROOT))]=sha(summary_path);summary=pd.read_csv(summary_path,usecols=['Model','Loss','WF_Val_BA_mean']);selected=summary[summary.Model==r.Architecture].sort_values(['WF_Val_BA_mean','Loss'],ascending=[False,True]).iloc[0];assert selected.Loss==r.Loss
  probe=ns['build_model']('GRU',len(features));assert isinstance(probe.rnn,torch.nn.GRU) and probe.rnn.hidden_size==128 and probe.rnn.num_layers==1 and probe.rnn.batch_first and probe.rnn.dropout==0.;assert probe.dropout.p==.2 and probe.fc.in_features==128 and probe.fc.out_features==2
  # Same EarlyStopping implementation, with logging-only side effects after its update.
  parent=ns['EarlyStopping']
  class LoggedStopping(parent):
   def __call__(self,score,model):
    super().__call__(score,model);self.report_epoch=getattr(self,'report_epoch',0)+1;js('active_job.json',{**ACTIVE,'epoch':self.report_epoch,'validation_BA_at_fixed_0_5':float(score),'updated_at_utc':now()})
  ns['EarlyStopping']=LoggedStopping;NS[market]=ns
  for lag in range(20,0,-1):
   for feature in features:columns.append({'Market':market,'Column_index':len([c for c in columns if c['Market']==market]),'Lag_observations':lag,'Feature':feature})
  pack=OUT/'checkpoints'/f'{market}_input_tensors.pt'
  if not pack.exists():savept(pack,{'folds':[{k:f[k] for k in ['fold_id','train','val']} for f in bundle['folds']],'final_train':bundle['final_train'],'test':bundle['test'],'features':features})
  data.append({'Market':market,'Feature_source':how,'Feature_names':features,'Feature_input_sha256':sha(frozen),'Market_input_sha256':INPUTHASH[str(path.relative_to(ROOT))],'Feature_definition_cell_sha256':hashlib.sha256(notebook.cells[9].source.encode()).hexdigest(),'split_definition_cell_sha256':hashlib.sha256(notebook.cells[11].source.encode()).hexdigest(),'Neural_input_shape':[20,len(features)],'Tabular_columns':20*len(features),'Feature_scaling':'Original per-feature train-only StandardScaler, shared across all20 lags; flatten the same scaled tensor without a second scaler','Test_dates_labels_match_frozen_LSTM':True})
 pd.DataFrame(columns).to_csv(OUT/'diagnostics/tabular_column_order.csv',index=False)
 js('data_manifest.json',{'markets':data,'input_sha256':INPUTHASH,'feature_set':'exact market-specific COMMON_LOCAL','no_network_refresh':True,'label_horizon':20})
 js('leakage_audit.json',{'status':'passed','same_features_as_LSTM':True,'same_W20_tensors_for_tabular':True,'training_only_scalers':True,'label_boundaries_purged':True,'input_window_excludes_target':True,'future_feature_perturbation':True,'original_frozen_source_availability_rules_preserved':True,'rule_P_t_information_difference_documented':True,'no_HMM_refit':True})
def scaler_json(stem,s,features,dates):js('scalers/'+stem+'.json',{'type':'StandardScaler','mean':s.mean_.tolist(),'scale':s.scale_.tolist(),'var':s.var_.tolist(),'n_samples_seen':int(s.n_samples_seen_),'fit_first':str(dates.min().date()),'fit_last':str(dates.max().date()),'features':features,'flattening':'C-order chronological sequence, oldest timestep first'})
def audit_split(raw,df,end,pack,d):
 pos=raw.index.get_indexer(df.index);assert (pos>=0).all() and (pos+20<len(raw)).all();assert (raw.index[pos+20]<=pd.Timestamp(end)).all();assert pack[0].shape[1:]==(20,d);assert pack[2].equals(pd.DatetimeIndex(df.index[20:]));assert torch.isfinite(pack[0]).all()
def tabular(model,seed):
 if model=='LogisticRegression':return LogisticRegression(penalty='l2',solver='lbfgs',max_iter=5000,class_weight=None,C=1.,fit_intercept=True,random_state=seed,tol=1e-4)
 assert model=='LightGBM'
 return LGBMClassifier(objective='binary',n_estimators=300,learning_rate=.03,num_leaves=31,max_depth=-1,min_child_samples=20,subsample=1.,colsample_bytree=1.,reg_alpha=0.,reg_lambda=0.,class_weight=None,verbosity=-1,random_state=seed,data_random_seed=seed,feature_fraction_seed=seed,bagging_seed=seed,drop_seed=seed,extra_seed=seed,deterministic=True,force_col_wise=True,n_jobs=2)
def fit_job(market,model,loss,seed,fold=None):
 stage=f'fold{fold["fold_id"]}' if fold is not None else 'final';stem=f'{market}_{model}_{loss}_{seed}_{stage}';ck=OUT/'checkpoints'/(stem+'.pt')
 if ck.exists():return loadpt(ck)['probabilities']
 activity(phase='validation' if fold else 'final_test',Market=market,Model=model,Loss=loss,Seed=seed,Stage=stage)
 if fold is None:
  selection=json.loads((OUT/'selection_lock.json').read_text());assert selection['status']=='frozen_before_new_test_evaluation' and sha(OUT/'selected_configs.csv')==selection['selection_sha256'] and sha(OUT/'frozen_thresholds.csv')==selection['thresholds_sha256']
 ns=NS[market];bundle=BUNDLES[market];tr,ev=(fold['train'],fold['val']) if fold else (bundle['final_train'],bundle['test']);X,y=tr[:2];V,vy,dates,fwd=ev
 ns['set_seed'](seed);start=time.monotonic()
 if model=='GRU':
  estimator=ns['build_model']('GRU',X.shape[-1])
  if fold:estimator,prob=ns['train_one_fold'](estimator,X,y,V,vy,seed_for_loader=seed,loss_mode=loss)
  else:estimator,prob=ns['train_final_model'](estimator,X,y,V,seed_for_loader=seed,loss_mode=loss)
  state={'state_dict':estimator.state_dict(),'input_size':X.shape[-1],'epochs_max':100 if fold else 60}
 else:
  estimator=tabular(model,seed)
  with warnings.catch_warnings(record=True) as messages:
   warnings.simplefilter('always');estimator.fit(X.numpy().reshape(len(X),-1),y.numpy());prob=estimator.predict_proba(V.numpy().reshape(len(V),-1))[:,1]
  path=OUT/'checkpoints'/(stem+'.joblib');joblib.dump(estimator,path,compress=3)
  diagnostic={'Market':market,'Model':model,'Loss':loss,'Seed':seed,'Stage':stage,'Warnings':[str(w.message) for w in messages],'n_iter':np.asarray(getattr(estimator,'n_iter_',[])).tolist(),'Logistic_converged':bool(np.max(estimator.n_iter_)<5000) if model=='LogisticRegression' else None,'LightGBM_requested_estimators':300 if model=='LightGBM' else None,'LightGBM_actual_trees':int(estimator.booster_.num_trees()) if model=='LightGBM' else None,'fit_seconds':time.monotonic()-start}
  js('diagnostics/'+stem+'.json',diagnostic);state={'estimator_file':str(path.relative_to(OUT))}
 prob=np.asarray(prob);assert np.isfinite(prob).all() and ((prob>=0)&(prob<=1)).all()
 savept(ck,{**state,'Market':market,'Model':model,'Loss':loss,'Seed':seed,'Stage':stage,'probabilities':prob,'Y_true':vy.numpy(),'dates':dates.strftime('%Y-%m-%d').tolist(),'scaler_file':f'scalers/{market}_{stage}.json','selection_lock_sha256':sha(OUT/'selection_lock.json') if fold is None else None})
 print('FIT COMPLETE',stem,'seconds',round(time.monotonic()-start,1),flush=True);return prob

def validation_phase():
 records=[];candidates=[]
 for market in M:
  ns=NS[market]
  for model in NEW:
   for loss in LOSSES if model=='GRU' else ['L2' if model=='LogisticRegression' else 'Binary_logloss']:
    for seed in S:
     probabilities=[];truth=[];dates=[]
     for fold in BUNDLES[market]['folds']:
      probabilities.append(fit_job(market,model,loss,seed,fold));truth.append(fold['val'][1].numpy());dates.extend(fold['val'][2])
     p=np.concatenate(probabilities);y=np.concatenate(truth);threshold,grid=ns['select_validation_threshold'](y,p,ns['THRESHOLD_GRID']);met=ns['calculate_metrics'](y,probs=p,threshold=threshold)
     records.append({'Market':market,'Model':model,'Loss':loss,'Seed':seed,'Threshold':threshold,'WF_Val_BA':met['Balanced_Accuracy'],'WF_Val_Macro_F1':met['Macro_F1'],'Abs_threshold_distance':abs(threshold-.5)})
     pd.DataFrame({'Date':pd.to_datetime(dates),'Y_true':y,'Probability':p,'Y_pred':(p>threshold).astype(int),'Threshold':threshold,'Seed':seed,'Model':model,'Loss':loss}).to_csv(OUT/'all_predictions'/f'{market}_{model}_{loss}_{seed}.validation.csv',index=False,float_format='%.17g')
     grid.to_csv(OUT/'diagnostics'/f'{market}_{model}_{loss}_{seed}_threshold_grid.csv',index=False,float_format='%.17g')
     pd.DataFrame(records).to_csv(OUT/'validation_selection_results.partial.csv',index=False,float_format='%.17g');js('progress.json',{'phase':'validation','completed_validation_candidate_seed_runs':len(records),'expected_validation_candidate_seed_runs':125,'completed_final_test_runs':0,'expected_final_test_runs':75,'completed_fit_checkpoints':len(list((OUT/'checkpoints').glob('*_fold*.pt'))),'updated_at_utc':now()})
 f=pd.DataFrame(records);assert len(f)==125;f.to_csv(OUT/'validation_selection_results.csv',index=False,float_format='%.17g')
 selected=[]
 for (market,model),g in f.groupby(['Market','Model'],sort=False):
  agg=g.groupby('Loss').agg(WF_Val_BA_mean=('WF_Val_BA','mean'),WF_Val_Macro_F1_mean=('WF_Val_Macro_F1','mean'),Mean_threshold_distance=('Abs_threshold_distance','mean')).reset_index().sort_values(['WF_Val_BA_mean','WF_Val_Macro_F1_mean','Mean_threshold_distance','Loss'],ascending=[False,False,True,True])
  for r in agg.to_dict('records'):candidates.append({'Market':market,'Model':model,**r})
  r=agg.iloc[0];selected.append({'Market':market,'Model':model,'Loss':r.Loss,'WF_Val_BA_mean':r.WF_Val_BA_mean,'WF_Val_Macro_F1_mean':r.WF_Val_Macro_F1_mean,'Mean_threshold_distance':r.Mean_threshold_distance,'Origin':'New_Phase1','Selection':'Validation only; no test evaluation yet'})
 old=pd.read_csv(ROOT/'artifacts/validation_selected_statistical_robustness/selected_primary_configs.csv')
 for r in old.itertuples():selected.append({'Market':r.Market,'Model':r.Architecture,'Loss':r.Loss,'WF_Val_BA_mean':r.WF_Val_BA_mean,'Origin':'Existing_frozen','Selection':'Copied unchanged validated architecture selection'})
 selected=pd.DataFrame(selected);destination=OUT/'selected_configs.csv'
 if destination.exists():
  previous=pd.read_csv(destination,float_precision='round_trip');assert previous[['Market','Model','Loss']].equals(selected[['Market','Model','Loss']])
 else:selected.to_csv(destination,index=False,float_format='%.17g')
 pd.DataFrame(candidates).to_csv(OUT/'validation_candidate_summary.csv',index=False,float_format='%.17g')
 thresholds=[]
 for r in selected[selected.Origin=='New_Phase1'].itertuples():
  for row in f[(f.Market==r.Market)&(f.Model==r.Model)&(f.Loss==r.Loss)].to_dict('records'):thresholds.append(row)
 td=OUT/'frozen_thresholds.csv';current=pd.DataFrame(thresholds)
 if td.exists():
  previous=pd.read_csv(td,float_precision='round_trip');assert np.array_equal(previous.Threshold,current.Threshold) and previous[['Market','Model','Loss','Seed']].equals(current[['Market','Model','Loss','Seed']])
 else:current.to_csv(td,index=False,float_format='%.17g')
 newlock={'status':'frozen_before_new_test_evaluation','all_new_validation_jobs_complete':375,'validation_candidate_seed_runs':125,'new_selected_configs':15,'existing_configs_retained':15,'selection_sha256':sha(destination),'thresholds_sha256':sha(td),'created_at_utc':now()}
 if (OUT/'selection_lock.json').exists():
  previous=json.loads((OUT/'selection_lock.json').read_text());assert previous['selection_sha256']==newlock['selection_sha256'] and previous['thresholds_sha256']==newlock['thresholds_sha256']
 else:js('selection_lock.json',newlock)
 return selected,f

def run():
 setup();sourcehash={name:sha(OUT/name) for name in ['run_phase1.py','finalize.py','report.py','protocol_lock.json']}
 if (OUT/'run_manifest.json').exists():assert json.loads((OUT/'run_manifest.json').read_text())['source_sha256']==sourcehash
 else:
  paths=subprocess.check_output(['git','ls-files','artifacts'],text=True).splitlines();protected={p:sha(ROOT/p) for p in paths if (ROOT/p).is_file()}
  js('run_manifest.json',{'started_at_utc':now(),'source_sha256':sourcehash,'protected_original_artifact_sha256':protected,'input_sha256':INPUTHASH,'packages':LOCK['packages'],'source_existing_PT_sha256':sha(ROOT/'artifacts/validation_selected_pt_tests/analyze.py'),'source_economic_protocol_sha256':sha(ROOT/'artifacts/cross_market_economic/economic_protocol.json')})
 js('execution_status.json',{'status':'running','pid':os.getpid(),'started_at_utc':now(),'phase':'validation_only'})
 selected,validation=validation_phase();assert json.loads((OUT/'selection_lock.json').read_text())['status']=='frozen_before_new_test_evaluation';rows=[]
 for r in selected[selected.Origin=='New_Phase1'].itertuples():
  for seed in S:
   score=validation[(validation.Market==r.Market)&(validation.Model==r.Model)&(validation.Loss==r.Loss)&(validation.Seed==seed)].iloc[0];prob=fit_job(r.Market,r.Model,r.Loss,seed);threshold=float(score.Threshold);pack=BUNDLES[r.Market]['test'];y=pack[1].numpy();met=NS[r.Market]['calculate_metrics'](y,probs=prob,threshold=threshold)
   rows.append({'Market':r.Market,'Model':r.Model,'Loss':r.Loss,'Seed':seed,'Threshold':threshold,'WF_Val_BA':score.WF_Val_BA,'WF_Val_Macro_F1':score.WF_Val_Macro_F1,'Actual_Up_Rate':y.mean(),**met})
   pd.DataFrame({'Date':pack[2],'Y_true':y,'Probability':prob,'Y_pred':(prob>threshold).astype(int),'Threshold':threshold,'Seed':seed,'Model':r.Model,'Loss':r.Loss,'Forward_Return20':pack[3]}).to_csv(OUT/'all_predictions'/f'{r.Market}_{r.Model}_{r.Loss}_{seed}.test.csv',index=False,float_format='%.17g')
   pd.DataFrame(rows).to_csv(OUT/'test_results.partial.csv',index=False,float_format='%.17g');js('progress.json',{'phase':'test_after_validation_lock','completed_validation_candidate_seed_runs':125,'completed_final_test_runs':len(rows),'expected_final_test_runs':75,'updated_at_utc':now()});print('FINAL COMPLETE',r.Market,r.Model,seed,flush=True)
 df=pd.DataFrame(rows);df.to_csv(OUT/'test_results_all_new_models.csv',index=False,float_format='%.17g')
 for model,name in [('GRU','gru_seed_results.csv'),('LogisticRegression','logistic_seed_results.csv'),('LightGBM','lightgbm_seed_results.csv')]:df[df.Model==model].to_csv(OUT/name,index=False,float_format='%.17g')
 subprocess.run([sys.executable,str(OUT/'finalize.py')],check=True)
 js('execution_status.json',{'status':'completed','completed_at_utc':now(),'new_final_runs':75});js('progress.json',{'status':'completed','validation_candidate_seed_runs':125,'final_test_runs':75,'model_fit_checkpoints':450})
 publish()
def publish():
 def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
 assert json.loads((OUT/'completion_check.json').read_text())['status']=='validated';assert not git('diff','--name-only') and not git('diff','--cached','--name-only');assert git('branch','--show-current')=='main'
 git('fetch','origin','main');git('merge','--ff-only','origin/main');(OUT/'completed_execution.log').write_bytes((OUT/'execution.log').read_bytes())
 files=[str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.py','.json','.csv','.md','.png','.pt','.joblib','.log','.gz'] and p.name not in ['execution.log','publication.json','validation_selection_results.partial.csv','test_results.partial.csv']]
 git('add','--',*files);git('diff','--cached','--check');git('commit','-m','Add frozen JOF Phase1 GRU logistic LightGBM and rule benchmark expansion');git('push','origin','main');commit=git('rev-parse','HEAD');assert git('ls-remote','origin','refs/heads/main').split()[0]==commit;js('publication.json',{'status':'published','commit':commit,'verified_at_utc':now()});print('PUBLISHED',commit,flush=True)
if __name__=='__main__':
 try:
  if '--preflight' in sys.argv:
   setup()
   for market in M:
    ns=NS[market];X,y=BUNDLES[market]['folds'][0]['train'][:2]
    for loss in LOSSES:
     ns['set_seed'](42);g=ns['build_model']('GRU',X.shape[-1]);v=ns['build_criterion'](loss,y)(g(X[:64]),y[:64]);assert torch.isfinite(v);v.backward();assert all(torch.isfinite(p.grad).all() for p in g.parameters() if p.grad is not None)
    for name in ['LogisticRegression','LightGBM']:
     model=tabular(name,42);model.fit(X[:128].numpy().reshape(128,-1),y[:128].numpy());prob=model.predict_proba(X[:64].numpy().reshape(64,-1))[:,1];assert np.isfinite(prob).all()
    print('PREFLIGHT PASS',market,'GRU3 losses; Logistic/LightGBM locked-parameter fit on real training-only smoke subset',flush=True)
  else:
   p=OUT/'execution_status.json'
   if p.exists():
    old=json.loads(p.read_text());assert old.get('status')!='completed','Preserve completed run';assert not(old.get('status')=='running' and Path('/proc/'+str(old.get('pid'))).exists()),'Duplicate active run'
   run()
 except BaseException as exc:
  js('execution_status.json',{'status':'failed','error':str(exc),'failed_at_utc':now()});(OUT/'execution_error.txt').write_text(traceback.format_exc());raise
