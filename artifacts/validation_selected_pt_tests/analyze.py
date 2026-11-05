"""Conventional Pesaran–Timmermann 1992, existing binary forecasts only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
M={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
A=['LNN','LSTM','Transformer'];S=[42,52,62,72,82]
EXPECTED={'SP500':['MILD_FOCAL']*3,'NASDAQ100':['MILD_FOCAL','MILD_FOCAL','MILD_WCE'],'NIKKEI225':['MILD_WCE','MILD_FOCAL','MILD_FOCAL'],'EUROSTOXX50':['MILD_FOCAL','CE','CE'],'KOSPI200':['CE','CE','MILD_FOCAL']}
assert not (OUT/'pt_seed_level_results.csv').exists(),'Do not overwrite existing outputs'
inputs={};tracked=subprocess.check_output(['git','ls-files','artifacts'],cwd=ROOT,text=True).splitlines();protected={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked if (ROOT/p).is_file()}
def read(p,**kwargs):
 p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,**kwargs)
def save(rows,name):pd.DataFrame(rows).to_csv(OUT/name,index=False,float_format='%.17g')
def js(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def pt(y,f):
 y=np.asarray(y);f=np.asarray(f);assert len(y)==len(f) and set(y)<={0,1} and set(f)<={0,1};n=len(y);py=float(y.mean());pf=float(f.mean());ph=float(np.mean(y==f));ps=py*pf+(1-py)*(1-pf)
 vp=ps*(1-ps)/n;vps=((2*py-1)**2*pf*(1-pf)+(2*pf-1)**2*py*(1-py))/n+4*py*(1-py)*pf*(1-pf)/(n*n);var=vp-vps;simple=4*py*(1-py)*pf*(1-pf)*(n-1)/(n*n)
 row={'N':n,'Actual_Up_Rate':py,'Forecast_Up_Rate':pf,'Accuracy':ph,'Balanced_Accuracy':balanced_accuracy_score(y,f) if len(np.unique(y))==2 else np.nan,'Macro_F1':f1_score(y,f,labels=[0,1],average='macro',zero_division=0),'Observed_hit_rate':ph,'Expected_independent_hit_rate':ps,'Hit_rate_excess':ph-ps,'Var_hit':vp,'Var_expected_hit':vps,'Var_hat':var,'Var_algebraic_check':simple,'PT_statistic':np.nan,'PT_two_sided_p':np.nan,'PT_positive_one_sided_p':np.nan}
 if n<=1:status='PT not defined: insufficient observations'
 elif len(np.unique(f))==1:status='PT not defined for constant forecast'
 elif len(np.unique(y))==1:status='PT not defined for constant actual direction'
 elif not np.isfinite(var) or var<=0:status='PT not defined: nonpositive/nonfinite variance'
 else:
  assert np.isclose(var,simple,atol=1e-15,rtol=1e-10)
  z=(ph-ps)/np.sqrt(var);row.update(PT_statistic=z,PT_two_sided_p=2*stats.norm.sf(abs(z)),PT_positive_one_sided_p=stats.norm.sf(z));status='defined'
 expected_counts=n*np.outer([1-py,py],[1-pf,pf]);row['Min_expected_cell_count']=expected_counts.min();row['Small_cell_warning']=bool(expected_counts.min()<5);row['PT_status']=status
 return row
def adjust(frame,mask,outcol,pcol):
 # All planned hypotheses stay in the family; undefined PT is reserved as p=1 but displayed NA.
 f=frame.loc[mask,pcol];p=f.fillna(1.).to_numpy();ix=np.argsort(p);adj=np.empty(len(p));adj[ix]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[ix]));frame.loc[mask,outcol]=adj;frame.loc[mask & frame[pcol].isna(),outcol]=np.nan
selection=[];config={}
for market,folder in M.items():
 f=read(ROOT/folder/'summary.csv',usecols=['Model','Loss','WF_Val_BA_mean'],float_precision='round_trip')
 for arch,expected in zip(A,EXPECTED[market]):
  r=f[f.Model==arch].sort_values(['WF_Val_BA_mean','Loss'],ascending=[False,True]).iloc[0];assert r.Loss==expected,f'STOP {market} {arch} mismatch'
  config[(market,arch)]=r.Loss;selection.append({'Market':market,'Architecture':arch,'Selected_Loss':r.Loss,'WF_Val_BA_mean':r.WF_Val_BA_mean,'Test_used_for_selection':False})
save(selection,'selected_primary_configs.csv')
seedrows=[];majority=[];non=[];bench=[];high=[];predictionrows=[];subsets=[];cache={}
prior=read(ROOT/'artifacts/validation_selected_statistical_robustness/majority_predictions_all_architectures.csv')
for market,folder in M.items():
 directory=ROOT/folder;result=read(directory/'seed_results.csv',float_precision='round_trip');raw=read(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');reference=None
 for arch in A:
  loss=config[(market,arch)];votes=[]
  for seed in S:
   p=read(directory/'predictions'/f'{arch}_{loss}_{seed}.csv',float_precision='round_trip');dates=pd.DatetimeIndex(pd.to_datetime(p.Date));y=p.Y_true.to_numpy(int);assert dates.is_unique and dates.is_monotonic_increasing
   if reference is None:reference=(dates,y)
   else:assert dates.equals(reference[0]) and np.array_equal(y,reference[1])
   r=result[(result.Model==arch)&(result.Loss==loss)&(result.Seed.astype(str)==str(seed))].iloc[0];assert np.allclose(p.Threshold,r.Threshold,atol=1e-14,rtol=0);assert np.isfinite(p.Probability).all() and p.Probability.between(0,1).all()
   f=(p.Probability.to_numpy()>r.Threshold).astype(int)
   if 'Y_pred' in p:assert np.array_equal(f,p.Y_pred)
   test=pt(y,f)
   for metric in ['Accuracy','Balanced_Accuracy','Macro_F1']:assert np.isclose(test[metric],r[metric],atol=1e-12,rtol=0)
   seedrows.append({'Market':market,'Architecture':arch,'Selected_Loss':loss,'Seed':seed,'Threshold':r.Threshold,**test});votes.append(f)
  votes=np.array(votes);f=(votes.sum(axis=0)>=3).astype(int);saved=prior[(prior.Market==market)&(prior.Architecture==arch)]
  assert np.array_equal(pd.to_datetime(saved.Date),dates) and np.array_equal(saved.Y_true,y) and np.array_equal(saved.Majority_prediction,f)
  loc=raw.index.get_indexer(dates);close=raw.Close.to_numpy();assert (loc>=20).all() and (loc+20<len(raw)).all();persist=(close[loc]>close[loc-20]).astype(int);assert np.array_equal((close[loc+20]>close[loc]).astype(int),y);assert np.array_equal(saved.Persistence_prediction,persist)
  majority.append({'Market':market,'Architecture':arch,'Selected_Loss':loss,'Aggregation':'five-seed majority >=3','Dependence_note':'PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially.',**pt(y,f)})
  for i,date in enumerate(dates):predictionrows.append({'Market':market,'Architecture':arch,'Selected_Loss':loss,'Date':str(date.date()),'Y_true':int(y[i]),'Majority_forecast':int(f[i]),'Persistence':int(persist[i]),**{f'Seed_{seed}_forecast':int(votes[j,i]) for j,seed in enumerate(S)}})
  cache[(market,arch)]={'dates':dates,'y':y,'votes':votes,'majority':f,'persistence':persist}
  if arch=='LNN':
   ix=np.arange(0,len(y),20);assert (np.diff(loc[ix])>=20).all();oldsubset=read(ROOT/'artifacts/validation_selected_statistical_robustness/nonoverlap_selected_dates.csv');oldsubset=oldsubset[oldsubset.Market==market]
   assert np.array_equal(oldsubset.Original_prediction_row,ix) and np.array_equal(oldsubset.LNN_majority,f[ix]) and np.array_equal(oldsubset.Persistence,persist[ix])
   non.append({'Market':market,'Architecture':'LNN','Selected_Loss':loss,'Phase':0,'Step':20,'Dependence_note':'The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence.',**pt(y[ix],f[ix])})
   for i in ix:subsets.append({'Market':market,'Original_prediction_row':int(i),'Date':str(dates[i].date()),'Y_true':int(y[i]),'LNN_majority':int(f[i]),'Persistence':int(persist[i])})
 for name,f in [('Always_Up',np.ones(len(y),int)),('Always_Down',np.zeros(len(y),int)),('Persistence',persist)]:bench.append({'Market':market,'Benchmark':name,**pt(y,f)})
sf=pd.DataFrame(seedrows);assert len(sf)==75;save(sf,'pt_seed_level_results.csv');mf=pd.DataFrame(majority);assert len(mf)==15
adjust(mf,pd.Series(True,index=mf.index),'Holm15_p','PT_two_sided_p');adjust(mf,pd.Series(True,index=mf.index),'Holm15_positive_p','PT_positive_one_sided_p');ln=mf.Architecture=='LNN';adjust(mf,ln,'Holm5_LNN_p','PT_two_sided_p');adjust(mf,ln,'Holm5_LNN_positive_p','PT_positive_one_sided_p')
mf['Significant_Holm15']=(mf.Holm15_p<.05)&mf.PT_two_sided_p.notna();mf['Positive_direction_supported_Holm15']=mf.Significant_Holm15&(mf.PT_statistic>0);mf['Significant_negative_association_Holm15']=mf.Significant_Holm15&(mf.PT_statistic<0)
mf['Directional_Accuracy_Supported_Holm5']=ln&(mf.Holm5_LNN_p<.05)&(mf.PT_statistic>0)
save(mf,'pt_holm_adjusted_results.csv');save(mf[ln],'pt_lnn_majority_results.csv');save(mf,'pt_majority_results_all_architectures.csv')
summary=[]
for (market,arch),g in sf.groupby(['Market','Architecture'],sort=False):
 summary.append({'Market':market,'Architecture':arch,'Selected_Loss':g.Selected_Loss.iloc[0],'N_seeds':5,'Mean_BA':g.Balanced_Accuracy.mean(),'Mean_Accuracy':g.Accuracy.mean(),'Mean_PT_statistic':g.PT_statistic.mean(),'Median_PT_statistic':g.PT_statistic.median(),'Defined_PT_seeds':int(g.PT_statistic.notna().sum()),'Undefined_PT_seeds':int(g.PT_statistic.isna().sum()),'Seeds_PT_positive':int((g.PT_statistic>0).sum()),'Seeds_two_sided_p_below_0_05':int((g.PT_two_sided_p<.05).sum()),'Seeds_positive_one_sided_p_below_0_05':int((g.PT_positive_one_sided_p<.05).sum()),'Counts_are_descriptive_only':True})
save(summary,'pt_architecture_summary.csv');save(bench,'pt_benchmark_context.csv')
nf=pd.DataFrame(non);adjust(nf,pd.Series(True,index=nf.index),'Exploratory_Holm5_p','PT_two_sided_p');nf['Positive_direction_supported_exploratory']=nf.Exploratory_Holm5_p.lt(.05)&nf.PT_statistic.gt(0);save(nf,'pt_nonoverlap_results.csv');save(subsets,'pt_nonoverlap_selected_dates.csv');save(predictionrows,'majority_forecasts_audit.csv')
hmm=read(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv');hmm.Date=pd.to_datetime(hmm.Date);z=cache[('NIKKEI225','LNN')];assert config[('NIKKEI225','LNN')]=='MILD_WCE';mask=hmm[hmm.Market=='NIKKEI225'].set_index('Date').loc[z['dates'],'Regime'].eq('High').to_numpy();assert int(mask.sum())==117
for label,f,seed in [(f'Seed_{s}',v,s) for s,v in zip(S,z['votes'])]+[('Majority',z['majority'],'MAJORITY'),('Persistence',z['persistence'],'BASELINE'),('Always_Up',np.ones(len(mask),int),'CONSTANT')]:
 row={'Market':'NIKKEI225','Architecture':'LNN' if label not in ['Persistence','Always_Up'] else label,'Selected_Loss':'MILD_WCE' if label not in ['Persistence','Always_Up'] else 'BASELINE','Aggregation':label,'Seed':seed,'Regime':'High','Exploratory':True,**pt(z['y'][mask],f[mask])};row['Always_Up_Accuracy']=z['y'][mask].mean();row['Accuracy_minus_Always_Up']=row['Accuracy']-row['Always_Up_Accuracy'];high.append(row)
save(high,'pt_nikkei_high_results.csv')
# Manuscript tables retain explicit dependence notes and undefined tests.
columns=['Market','Architecture','Selected_Loss','N','Accuracy','Balanced_Accuracy','Actual_Up_Rate','Forecast_Up_Rate','PT_statistic','PT_two_sided_p','Holm15_p','Significant_Holm15','Positive_direction_supported_Holm15','PT_status','Dependence_note']
save(mf[columns],'manuscript_pt_table.csv');save(mf[ln][columns+['Holm5_LNN_p','Directional_Accuracy_Supported_Holm5']],'manuscript_lnn_pt_table.csv')
# Reference metadata: no external observations or model outputs used.
reference=Path('/tmp/rugarch-tests-pt.R');docs=Path('/tmp/DACTest-pt.Rd');assert reference.exists() and 'p_hat_var - p_star_var' in reference.read_text()
js('pt_reference.json',{'original':'Pesaran, M.H. and Timmermann, A. (1992), A Simple Nonparametric Test of Predictive Performance, Journal of Business & Economic Statistics10(4),461–465','independent_implementation':'rugarch::DACTest, test=PT, R/rugarch-tests.R, lines384–400','source_url':'https://raw.githubusercontent.com/alexiosg/rugarch/master/R/rugarch-tests.R','source_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'documentation_url':'https://raw.githubusercontent.com/alexiosg/rugarch/master/man/DACTest.Rd','documentation_sha256':hashlib.sha256(docs.read_bytes()).hexdigest(),'binary_mapping_for_reference':'Reference sign-based implementation requires mapping binary directions to -1/+1; passing0/1 directly would incorrectly omit Down/Down hits','variance':'Var(P_hat)-Var(P_star), exactly as original formula; no alternative test substituted','p_primary':'two-sided normal; one-sided positive normal tail supplemental','constant_forecast':'PT not defined for constant forecast; never assign p=1 as an observed PT result','planned_Holm':'reserve undefined hypotheses as p=1 internally for correction, report their adjusted p as NA; exactly15 and5 planned hypotheses'})
protocol={'alpha':.05,'primary_tail':'two-sided','supplemental_tail':'one-sided positive association, prespecified, not chosen after observing sign','families':{'A':15,'B_LNN':5,'nonoverlap_exploratory':5},'support_rule':'primary directional support requires positive PT and two-sided Holm p<0.05; significant negative association is not positive forecasting skill','undefined':'retain rows with NA test/p; count them and reserve planned Holm slots, not silently drop','selection':'existing validation WF BA only; all15 expected verified','source_models_unchanged':True,'nonoverlap_phase':0,'nonoverlap_step':20,'phase_search':False,'HMM_refit':False,'standard_PT_not_dependence_robust':True}
js('pt_protocol.json',protocol)
for name,digest in inputs.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
for name,digest in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
js('analysis_manifest.json',{'status':'computed_pending_independent_validation','completed_at_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':inputs,'protected_original_artifact_sha256':protected,'source_prediction_and_artifact_files_unchanged':True,'model_training':False,'threshold_tuning':False,'features_or_targets_changed':False,'HMM_refit':False,'packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn']}})
print(mf[['Market','Architecture','Selected_Loss','PT_statistic','PT_two_sided_p','Holm15_p','Positive_direction_supported_Holm15']].to_string(index=False));print('Undefined seed PT:',int(sf.PT_statistic.isna().sum()),'; primary majority PT:',int(mf.PT_statistic.isna().sum()))
