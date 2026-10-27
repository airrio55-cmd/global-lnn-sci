"""Monthly causal 3-state HMM; read-only predictive artifacts; no tuning."""
import os
os.environ['OMP_NUM_THREADS']='2';os.environ['MKL_NUM_THREADS']='2';os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
import json,hashlib,itertools,warnings
from datetime import datetime,timezone
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,recall_score,precision_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
MARKETS={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
SEEDS=[42,52,62,72,82];REGIMES=['Low','Normal','High'];CONFIGS=list(itertools.product(['LNN','LSTM','Transformer'],['CE','MILD_FOCAL','MILD_WCE']))
SEED=20261028;B=2000;BLOCK=20;inputs={}
def read(path,**kwargs):
 path=Path(path);inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();return pd.read_csv(path,**kwargs)
def save(rows,name):pd.DataFrame(rows).to_csv(OUT/name,index=False,float_format='%.17g')
def metric(y,p):
 if not len(y):return {k:np.nan for k in ['Accuracy','Balanced_Accuracy','Macro_F1','Recall','Precision','F1','Pred_Pos_Rate']}
 return {'Accuracy':accuracy_score(y,p),'Balanced_Accuracy':balanced_accuracy_score(y,p) if len(np.unique(y))==2 else np.nan,'Macro_F1':f1_score(y,p,labels=[0,1],average='macro',zero_division=0),'Recall':recall_score(y,p,zero_division=0),'Precision':precision_score(y,p,zero_division=0),'F1':f1_score(y,p,zero_division=0),'Pred_Pos_Rate':np.mean(p)}
def forward(emissions,start,trans):
 result=[];a=np.log(np.maximum(start,1e-300));lt=np.log(np.maximum(trans,1e-300))
 for i,e in enumerate(emissions):
  a=(a if i==0 else logsumexp(a[:,None]+lt,axis=0))+e;a-=logsumexp(a);result.append(a.copy())
 return np.array(result)
protocol={'states':3,'inputs':['Log_Ret','Vol20'],'classifier':'GaussianHMM, diagonal covariance','n_iter':300,'tol':1e-4,'min_covar':1e-4,'random_seed':SEED,'refit':'monthly expanding; fit rows strictly before first frozen-market observation in each test month','initial_history':'2010–2021','assignment':'target-date t uses filtered state at latest frozen observation strictly before t (t-1 observation). No same-target close or future observation. Forward filtering only, never full-month Viterbi/smoothing.','state_order':'Sort training-history posterior-weighted mean original Vol20 ascending; Low/Normal/High; relearned per market/month using training history only','bootstrap':{'resamples':B,'block_length_observations':BLOCK,'method':'circular date-block bootstrap over full test chronology; apply original regime mask after resampling; mean five seed BAs minus Persistence BA','seed':SEED,'ci':'95% percentile; require two classes and >=20 regime samples in resample'},'small_regime_flag':'N<50 or minority-label count<10; CIs exploratory, no formal significance claims','predictive_training':False,'best_selection':'Read fixed cross_market_statistics/market_best_models.csv; never reselect using regimes','no_tuning':True}
(OUT/'hmm_protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
best=read(ROOT/'artifacts/cross_market_statistics/market_best_models.csv').set_index('Market')
assignments=[];convergence=[];distributions=[];seedmetrics=[];summaries=[];bestrows=[];cis=[]
rng=np.random.default_rng(SEED)
for market,folder in MARKETS.items():
 directory=ROOT/folder
 raw=read(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');assert raw.index.is_unique and raw.index.is_monotonic_increasing
 features=pd.DataFrame({'Log_Ret':np.log(raw.Close).diff()});features['Vol20']=features.Log_Ret.rolling(20).std()*np.sqrt(252);features=features.dropna()
 results=read(directory/'seed_results.csv');learn=results[results.Seed.astype(str)!='BASELINE'].copy();learn.Seed=learn.Seed.astype(int)
 predmap={};dates=None;y=None
 for model,loss in CONFIGS:
  for seed in SEEDS:
   f=read(directory/'predictions'/f'{model}_{loss}_{seed}.csv',float_precision='round_trip')
   dt=pd.DatetimeIndex(pd.to_datetime(f.Date));yy=f.Y_true.to_numpy(int)
   if dates is None:dates=dt;y=yy
   else:assert dt.equals(dates) and np.array_equal(yy,y)
   assert dt.is_unique and dt.is_monotonic_increasing
   row=learn[(learn.Model==model)&(learn.Loss==loss)&(learn.Seed==seed)].iloc[0]
   assert np.allclose(f.Threshold,row.Threshold,atol=1e-14,rtol=0)
   p=(f.Probability.to_numpy()>row.Threshold).astype(int)
   assert np.isclose(balanced_accuracy_score(y,p),row.Balanced_Accuracy,atol=1e-12,rtol=0)
   assert np.isclose(f1_score(y,p,average='macro'),row.Macro_F1,atol=1e-12,rtol=0)
   predmap[(model,loss,seed)]=p
 positions=raw.index.get_indexer(dates);assert (positions>=20).all() and (positions+20<len(raw)).all()
 persistence=(raw.Close.to_numpy()[positions]>raw.Close.to_numpy()[positions-20]).astype(int)
 assert np.array_equal((raw.Close.to_numpy()[positions+20]>raw.Close.to_numpy()[positions]).astype(int),y)
 baseline=results[results.Model=='Persistence'].iloc[0];assert np.isclose(balanced_accuracy_score(y,persistence),baseline.Balanced_Accuracy,atol=1e-12,rtol=0)
 # Regimes for every frozen target-market observation in test years, not only prediction rows.
 all_test=raw.index[(raw.index>='2022-01-01')&(raw.index<='2025-12-31')]
 market_assign=[]
 for month in all_test.to_period('M').unique():
  targets=all_test[all_test.to_period('M')==month];cutoff=targets.min();history=features[features.index<cutoff]
  assert len(history)>1000 and history.index.max()<cutoff
  scaler=StandardScaler().fit(history);X=scaler.transform(history)
  model=GaussianHMM(n_components=3,covariance_type='diag',n_iter=300,tol=1e-4,min_covar=1e-4,random_state=SEED)
  with warnings.catch_warnings(record=True) as captured:
   warnings.simplefilter('always');model.fit(X)
  assert np.isfinite(model.monitor_.history[-1]) and np.isfinite(model.means_).all()
  weights=model.predict_proba(X);means=(weights*history.Vol20.to_numpy()[:,None]).sum(axis=0)/weights.sum(axis=0)
  order=np.argsort(means);mapping={int(s):REGIMES[j] for j,s in enumerate(order)}
  source_dates=raw.index[raw.index.get_indexer(targets)-1]
  prefix=features[features.index<=source_dates.max()]
  emissions=model._compute_log_likelihood(scaler.transform(prefix))
  filtered=forward(emissions,model.startprob_,model.transmat_)
  # Prefix-invariance: later emissions cannot change already-filtered states.
  check=len(history);np.testing.assert_allclose(filtered[:check],forward(emissions[:check],model.startprob_,model.transmat_),atol=1e-12,rtol=0)
  for date,source in zip(targets,source_dates):
   ix=prefix.index.get_loc(source);state=int(filtered[ix].argmax());assert source<date
   r={'Market':market,'Date':str(date.date()),'Regime':mapping[state],'Raw_state':state,'Feature_date':str(source.date()),'Fit_cutoff':str(cutoff.date()),'Fit_last_date':str(history.index.max().date()),'Fit_month':str(month),'Log_Ret':float(prefix.loc[source,'Log_Ret']),'Vol20':float(prefix.loc[source,'Vol20']),'Filtered_probability':float(np.exp(filtered[ix,state]))}
   assert pd.Timestamp(r['Fit_last_date'])<pd.Timestamp(r['Fit_cutoff'])<=date
   market_assign.append(r)
  hist=list(model.monitor_.history);gain=hist[-1]-hist[-2] if len(hist)>1 else np.nan
  convergence.append({'Market':market,'Month':str(month),'Fit_first':str(history.index.min().date()),'Fit_last':str(history.index.max().date()),'Fit_N':len(history),'Iterations':model.monitor_.iter,'Monitor_converged':bool(model.monitor_.converged),'Hit_iteration_limit':model.monitor_.iter>=300,'Last_log_likelihood':hist[-1],'Last_gain':gain,'Numerical_decrease':bool(gain<0),'Training_state_mean_Vol20':json.dumps({str(i):float(v) for i,v in enumerate(means)}),'State_mapping':json.dumps(mapping),'Warnings':' | '.join(str(w.message) for w in captured)})
 assignments+=market_assign
 a=pd.DataFrame(market_assign).set_index('Date');a.index=pd.to_datetime(a.index);matched=a.loc[dates];reg=matched.Regime.to_numpy()
 best_model=best.loc[market,'Best_Model'];best_loss=best.loc[market,'Loss'];bp=np.array([predmap[(best_model,best_loss,s)] for s in SEEDS])
 for regime in REGIMES:
  mask=reg==regime;n=int(mask.sum());positives=int(y[mask].sum());small=n<50 or min(positives,n-positives)<10
  distributions.append({'Market':market,'Regime':regime,'N':n,'Share':n/len(y),'All_test_calendar_N':int((a.Regime==regime).sum()),'Mean_Log_Ret':matched.loc[mask,'Log_Ret'].mean(),'Mean_Vol20':matched.loc[mask,'Vol20'].mean(),'Positive_label_rate':y[mask].mean() if n else np.nan,'N_positive':positives,'N_negative':n-positives,'Small_sample':small})
  base_metrics=metric(y[mask],persistence[mask])
  summaries.append({'Market':market,'Regime':regime,'Model':'Persistence','Loss':'BASELINE','N':n,'Seeds':0,**base_metrics,'Delta_BA_vs_Persistence':0.,'Delta_Macro_F1_vs_Persistence':0.})
  for arch,loss in CONFIGS:
   mm=[]
   for seed in SEEDS:
    m=metric(y[mask],predmap[(arch,loss,seed)][mask]);mm.append(m)
    seedmetrics.append({'Market':market,'Regime':regime,'Model':arch,'Loss':loss,'Seed':seed,'N':n,**m})
   mean={k:np.mean([v[k] for v in mm]) for k in base_metrics};sd={k+'_SD':np.std([v[k] for v in mm],ddof=1) for k in base_metrics}
   row={'Market':market,'Regime':regime,'Model':arch,'Loss':loss,'N':n,'Seeds':5,**mean,**sd,'Delta_BA_vs_Persistence':mean['Balanced_Accuracy']-base_metrics['Balanced_Accuracy'],'Delta_Macro_F1_vs_Persistence':mean['Macro_F1']-base_metrics['Macro_F1']}
   summaries.append(row)
   if arch==best_model and loss==best_loss:bestrows.append({**row,'Persistence_BA':base_metrics['Balanced_Accuracy'],'Persistence_Macro_F1':base_metrics['Macro_F1'],'Positive_label_rate':positives/n if n else np.nan,'Small_sample':small})
 # Resample full chronology first, then condition on the fixed regime, preserving within-block dependence.
 counts={r:[] for r in REGIMES};T=len(y)
 for _ in range(B):
  starts=rng.integers(0,T,size=int(np.ceil(T/BLOCK)));idx=((starts[:,None]+np.arange(BLOCK))%T).ravel()[:T]
  for regime in REGIMES:
   ix=idx[reg[idx]==regime];yy=y[ix];positive=yy==1;negative=~positive
   if len(ix)<20 or not positive.any() or not negative.any():continue
   base=.5*(persistence[ix][positive].mean()+(1-persistence[ix][negative]).mean())
   modelba=.5*(bp[:,ix][:,positive].mean(axis=1)+(1-bp[:,ix][:,negative]).mean(axis=1))
   counts[regime].append(float(modelba.mean()-base))
 for regime,values in counts.items():
  mask=reg==regime;n=int(mask.sum());small=n<50 or min(int(y[mask].sum()),n-int(y[mask].sum()))<10
  cis.append({'Market':market,'Regime':regime,'Model':best_model,'Loss':best_loss,'N':n,'Resamples':B,'Valid_resamples':len(values),'Block_length':BLOCK,'CI_low':np.quantile(values,.025) if values else np.nan,'CI_high':np.quantile(values,.975) if values else np.nan,'Small_sample':small,'Interpretation':'exploratory conditional fixed-regime CI; not refitting HMM or accounting for model-selection uncertainty'})
 print('FINISHED',market,'monthly fits',len(all_test.to_period('M').unique()),flush=True)
 save(convergence,'hmm_convergence_log.csv');save(assignments,'regime_assignments_all_markets.csv')
save(distributions,'regime_distribution.csv');save(seedmetrics,'regime_metrics_seed_level.csv');save(summaries,'regime_metrics_all_configs.csv');save(bestrows,'regime_best_model_comparison.csv');save(cis,'regime_bootstrap_ci.csv')
for path,digest in inputs.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
manifest={'status':'completed','completed_at_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':inputs,'predictive_training':False,'predictive_threshold_changes':False,'monthly_fits':len(convergence),'causality':'fit before month, train-only standardization/state mapping; forward-only filter at strictly previous observation; prefix-invariance verified','regime_metrics':'five-seed metric mean per configuration, not majority-vote metrics; Persistence once per regime','source_unchanged':True,'packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn','hmmlearn']}}
(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
