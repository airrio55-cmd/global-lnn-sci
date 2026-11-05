"""Frozen validation-selected statistical/overlap/regime sensitivity; no fitting."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,itertools
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,recall_score,precision_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
MARKETS={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
ARCH=['LNN','LSTM','Transformer'];SEEDS=[42,52,62,72,82];SEED=20261028;B=10000;H=20
EXPECTED={'SP500':['MILD_FOCAL']*3,'NASDAQ100':['MILD_FOCAL','MILD_FOCAL','MILD_WCE'],'NIKKEI225':['MILD_WCE','MILD_FOCAL','MILD_FOCAL'],'EUROSTOXX50':['MILD_FOCAL','CE','CE'],'KOSPI200':['CE','CE','MILD_FOCAL']}
METRICS=['Accuracy','Balanced_Accuracy','Macro_F1','Recall','Precision','F1','Pred_Pos_Rate'];inputs={}
assert not (OUT/'completion_check.json').exists(),'Do not overwrite a completed analysis'
protected={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['artifacts/cross_market_statistics','artifacts/nonoverlap_predictive_robustness','artifacts/cross_market_hmm','artifacts/validation_selected_lnn_economic'] for p in (ROOT/folder).rglob('*') if p.is_file()}
def read(p,**kw):
 p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,**kw)
def save(rows,name):pd.DataFrame(rows).to_csv(OUT/name,index=False,float_format='%.17g')
def js(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def metric(y,p):
 assert len(y)>0
 return {'Accuracy':accuracy_score(y,p),'Balanced_Accuracy':balanced_accuracy_score(y,p) if len(np.unique(y))==2 else np.nan,'Macro_F1':f1_score(y,p,labels=[0,1],average='macro',zero_division=0),'Recall':recall_score(y,p,zero_division=0),'Precision':precision_score(y,p,zero_division=0),'F1':f1_score(y,p,zero_division=0),'Pred_Pos_Rate':float(np.mean(p))}
def holm(p):
 p=np.asarray(p,float);ix=np.argsort(p);a=np.empty(len(p));a[ix]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[ix]));return a
def exact_wilcoxon(delta):
 nonzero=delta[delta!=0];n=len(nonzero)
 if not n:return 0.,1.,0,False
 ranks=stats.rankdata(abs(nonzero),method='average');wplus=float(ranks[nonzero>0].sum());total=float(ranks.sum());obs=abs(wplus-total/2)
 enumeration=np.asarray(list(itertools.product([0,1],repeat=n)))@ranks
 p=np.mean(abs(enumeration-total/2)>=obs-1e-14)
 return min(wplus,total-wplus),float(p),n,len(np.unique(abs(nonzero)))<n
def mcnemar(y,p,b):
 a=p==y;c=b==y;n00=int((~a&~c).sum());n01=int((~a&c).sum());n10=int((a&~c).sum());n11=int((a&c).sum());n=n01+n10
 exact=stats.binomtest(n10,n,.5,alternative='two-sided').pvalue if n else 1.;stat=max(abs(n01-n10)-1,0)**2/n if n else 0.;cc=stats.chi2.sf(stat,1) if n else 1.
 mp=metric(y,p);mb=metric(y,b)
 return {'N':len(y),'LNN_Accuracy':mp['Accuracy'],'Persistence_Accuracy':mb['Accuracy'],'LNN_BA':mp['Balanced_Accuracy'],'Persistence_BA':mb['Balanced_Accuracy'],'Delta_Accuracy':mp['Accuracy']-mb['Accuracy'],'Delta_BA':mp['Balanced_Accuracy']-mb['Balanced_Accuracy'],'n00':n00,'n01':n01,'n10':n10,'n11':n11,'statistic_CC':stat,'exact_p':exact,'continuity_corrected_p':cc,'raw_p':max(exact,cc)}
# Selection is completed using only validation columns before opening test predictions.
selection=[];SELECT={}
for market,folder in MARKETS.items():
 f=read(ROOT/folder/'summary.csv',usecols=['Model','Loss','WF_Val_BA_mean'],float_precision='round_trip')
 for arch,expected in zip(ARCH,EXPECTED[market]):
  z=f[f.Model==arch].sort_values(['WF_Val_BA_mean','Loss'],ascending=[False,True]);assert len(z)==3
  r=z.iloc[0];assert r.Loss==expected,f'STOP selection mismatch {market} {arch}: {r.Loss}'
  SELECT[(market,arch)]=r.Loss;selection.append({'Market':market,'Architecture':arch,'Loss':r.Loss,'WF_Val_BA_mean':r.WF_Val_BA_mean,'Test_used_for_selection':False,'Summary_source':folder+'/summary.csv'})
save(selection,'selected_primary_configs.csv')
protocol={'states_refit':False,'predictive_training':False,'selection':'Per market/architecture argmax WF_Val_BA_mean only; expected15 verified before test reading','seed_bootstrap':{'resamples':B,'seed':SEED,'scope':'algorithmic seed variability, not independent market history'},'Wilcoxon':'exact conditional sign enumeration of nonzero signed ranks; ties use midranks; two-sided; zeros discarded','Holm_families':{'seed_primary':15,'seed_LNN_specific':5,'full_majority_McNemar':5,'nonoverlap_McNemar':5,'Friedman_primary_and_secondary':2},'nonoverlap':'first saved test row, every20 observed prediction rows, phase0 only','Nikkei_primary':'LNN MILD_WCE five-seed metric mean vs deterministic Persistence, High labels reused; majority sensitivity also reported','Nikkei_bootstrap':{'type':'noncircular moving blocks of20 on full chronological test observation sequence, THEN select resampled High rows; never concatenate High episodes before block sampling','resamples':B,'seed':SEED,'paired':'same indices for truth, all five LNN seed predictions, Persistence and fixed regimes','invalid':'BA invalid if sampled High subset lacks either class; exclude and count; no imputation','conditional':'fixed HMM sequence, no refit/regime uncertainty/model-selection uncertainty/multiplicity adjustment'},'Nikkei_permutation':{'method':'within each contiguous original-observation High episode split consecutive chunks of maximum20, retaining shorter final blocks; independent whole-block model/baseline swaps shared across all five seeds','resamples':10000,'seed':SEED,'statistic':'mean five-seed Delta BA vs Persistence, consistent with descriptive0.2468','p':'two-sided (1+count(abs(permuted delta)>=abs(observed delta)))/(B+1)','exploratory':True,'post_hoc':True,'preregistered':False,'confirmatory':False},'interpretation':'Conservative Outcome A only if absolute BA>0.5, positive block-CI lower bound, nonoverlap direction nonnegative and exploratory permutation p<=0.05; otherwise Outcome B. No model/signal/settings changed by interpretation.'}
js('analysis_protocol.json',protocol)
seedrows=[];tests=[];majority_rows=[];fullmc=[];nonrows=[];noncomp=[];nonmc=[];non_dates=[];arrays={};rng=np.random.default_rng(SEED)
for market,folder in MARKETS.items():
 directory=ROOT/folder;results=read(directory/'seed_results.csv',float_precision='round_trip');baseline=results[results.Model=='Persistence'].iloc[0];raw=read(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');ref=None
 for arch in ARCH:
  loss=SELECT[(market,arch)];votes=[];ys=None;dates=None;deltas=[]
  for seed in SEEDS:
   p=read(directory/'predictions'/f'{arch}_{loss}_{seed}.csv',float_precision='round_trip');dt=pd.DatetimeIndex(pd.to_datetime(p.Date));y=p.Y_true.to_numpy(int)
   if ref is None:ref=(dt,y)
   else:assert dt.equals(ref[0]) and np.array_equal(y,ref[1])
   row=results[(results.Model==arch)&(results.Loss==loss)&(results.Seed.astype(str)==str(seed))].iloc[0]
   assert np.isfinite(p.Probability).all() and p.Probability.between(0,1).all();assert np.allclose(p.Threshold,row.Threshold,atol=1e-14,rtol=0)
   pred=(p.Probability.to_numpy()>row.Threshold).astype(int)
   if 'Y_pred' in p:assert np.array_equal(pred,p.Y_pred)
   met=metric(y,pred)
   for name in METRICS:assert np.isclose(met[name],row[name],atol=1e-12,rtol=0)
   votes.append(pred);deltas.append(met['Balanced_Accuracy']-baseline.Balanced_Accuracy)
   seedrows.append({'Market':market,'Architecture':arch,'Loss':loss,'Seed':seed,'N':len(y),'Positive_label_rate':y.mean(),**met,'Persistence_Accuracy':baseline.Accuracy,'Persistence_BA':baseline.Balanced_Accuracy,'Persistence_Macro_F1':baseline.Macro_F1,'Delta_Accuracy':met['Accuracy']-baseline.Accuracy,'Delta_BA':met['Balanced_Accuracy']-baseline.Balanced_Accuracy,'Delta_Macro_F1':met['Macro_F1']-baseline.Macro_F1,'Seed_BA_above_Persistence':bool(met['Balanced_Accuracy']>baseline.Balanced_Accuracy)})
   dates=dt;ys=y
  votes=np.array(votes);delta=np.array(deltas);w,pval,eff,ties=exact_wilcoxon(delta);bs=rng.choice(delta,size=(B,5),replace=True).mean(axis=1)
  tests.append({'Market':market,'Architecture':arch,'Loss':loss,'N_seeds':5,'Effective_nonzero_seed_differences':eff,'Absolute_difference_ties':ties,'Mean_Test_BA':np.mean([metric(ys,v)['Balanced_Accuracy'] for v in votes]),'Persistence_BA':baseline.Balanced_Accuracy,'Mean_Delta_BA':delta.mean(),'SD_Delta_BA':delta.std(ddof=1),'Seed_CI_low':np.quantile(bs,.025),'Seed_CI_high':np.quantile(bs,.975),'Seeds_above_Persistence':int((delta>0).sum()),'Wilcoxon_statistic':w,'raw_p':pval})
  loc=raw.index.get_indexer(dates);assert (loc>=20).all() and (loc+20<len(raw)).all();close=raw.Close.to_numpy();persist=(close[loc]>close[loc-20]).astype(int);assert np.array_equal((close[loc+20]>close[loc]).astype(int),ys)
  bm=metric(ys,persist)
  for name,col in [('Accuracy','Accuracy'),('Balanced_Accuracy','Balanced_Accuracy'),('Macro_F1','Macro_F1')]:assert np.isclose(bm[name],baseline[col],atol=1e-12,rtol=0)
  representative=(votes.sum(axis=0)>=3).astype(int)
  for i,d in enumerate(dates):majority_rows.append({'Market':market,'Architecture':arch,'Loss':loss,'Date':str(d.date()),'Y_true':int(ys[i]),'Majority_prediction':int(representative[i]),'Persistence_prediction':int(persist[i]),**{f'Seed_{s}_prediction':int(votes[j,i]) for j,s in enumerate(SEEDS)}})
  arrays[(market,arch)]={'dates':dates,'y':ys,'votes':votes,'majority':representative,'persistence':persist,'raw_positions':loc,'raw':raw}
  if arch=='LNN':
   prior=read(ROOT/'artifacts/validation_selected_lnn_economic'/f'{market}_operational_predictions.csv')
   assert np.array_equal(pd.to_datetime(prior.Date),dates) and np.array_equal(prior.Y_true,ys) and np.array_equal(prior.LNN_majority_prediction,representative) and np.array_equal(prior.Persistence_prediction,persist)
   fullmc.append({'Market':market,'Loss':loss,**mcnemar(ys,representative,persist)})
   ix=np.arange(0,len(ys),20);assert (np.diff(loc[ix])>=20).all()
   for i in ix:non_dates.append({'Market':market,'Loss':loss,'Original_prediction_row':int(i),'Date':str(dates[i].date()),'Y_true':int(ys[i]),'LNN_majority':int(representative[i]),'Persistence':int(persist[i])})
   yy=ys[ix];mm=metric(yy,representative[ix]);bb=metric(yy,persist[ix]);fmm=metric(ys,representative);fbb=metric(ys,persist)
   for name,met in [('LNN_majority',mm),('Persistence',bb)]:nonrows.append({'Market':market,'Loss':loss,'Prediction':name,'N':len(ix),'Positive_label_rate':yy.mean(),**met,'Delta_Accuracy':mm['Accuracy']-bb['Accuracy'],'Delta_BA':mm['Balanced_Accuracy']-bb['Balanced_Accuracy'],'Delta_Macro_F1':mm['Macro_F1']-bb['Macro_F1']})
   db=mm['Balanced_Accuracy']-bb['Balanced_Accuracy'];df=fmm['Balanced_Accuracy']-fbb['Balanced_Accuracy'];da=mm['Accuracy']-bb['Accuracy'];daf=fmm['Accuracy']-fbb['Accuracy']
   noncomp.append({'Market':market,'Loss':loss,'Full_N':len(ys),'Nonoverlap_N':len(ix),'Full_majority_Delta_BA':df,'Nonoverlap_LNN_BA':mm['Balanced_Accuracy'],'Nonoverlap_Persistence_BA':bb['Balanced_Accuracy'],'Nonoverlap_Delta_BA':db,'Full_Delta_BA_sign':int(np.sign(df)),'Nonoverlap_Delta_BA_sign':int(np.sign(db)),'BA_sign_preserved':bool(np.sign(df)==np.sign(db)),'Full_majority_Delta_Accuracy':daf,'Nonoverlap_Delta_Accuracy':da,'Accuracy_sign_preserved':bool(np.sign(daf)==np.sign(da))})
   nonmc.append({'Market':market,'Loss':loss,**mcnemar(yy,representative[ix],persist[ix])})
sf=pd.DataFrame(seedrows);save(sf,'seed_level_primary_metrics.csv')
cols=METRICS+['Persistence_Accuracy','Persistence_BA','Persistence_Macro_F1','Delta_Accuracy','Delta_BA','Delta_Macro_F1']
ag=sf.groupby(['Market','Architecture','Loss'])[cols].agg(['mean','std']);ag.columns=['_'.join(c) for c in ag.columns];ag.reset_index().to_csv(OUT/'seed_level_primary_summary.csv',index=False,float_format='%.17g')
tf=pd.DataFrame(tests);tf['Holm15_p']=holm(tf.raw_p);tf['Holm_LNN5_p']=np.nan;ln=tf.Architecture=='LNN';tf.loc[ln,'Holm_LNN5_p']=holm(tf.loc[ln,'raw_p']);tf['significant_Holm15']=tf.Holm15_p<.05;save(tf,'validation_selected_statistical_tests.csv')
fr=[]
for name in ['Balanced_Accuracy','Macro_F1']:
 matrix=sf.groupby(['Market','Architecture'])[name].mean().unstack().loc[list(MARKETS),ARCH].to_numpy();z,p=stats.friedmanchisquare(*matrix.T);fr.append({'Metric':name,'Market_blocks':5,'Architectures':3,'Friedman_statistic':z,'raw_p':p,'Kendall_W':z/(5*2),'Secondary':name=='Macro_F1'})
ff=pd.DataFrame(fr);ff['Holm2_p']=holm(ff.raw_p);save(ff,'architecture_friedman_tests.csv')
for rows,name in [(fullmc,'majority_vote_mcnemar.csv'),(nonmc,'nonoverlap_mcnemar.csv')]:
 f=pd.DataFrame(rows);f['Holm5_p']=holm(f.raw_p);f['significant_Holm5']=f.Holm5_p<.05;save(f,name)
save(nonrows,'nonoverlap_metrics.csv');save(noncomp,'nonoverlap_comparison_full.csv');save(non_dates,'nonoverlap_selected_dates.csv');save(majority_rows,'majority_predictions_all_architectures.csv')
# Nikkei High: fixed MILD_WCE and same seed-mean statistic as expected descriptive values.
hmm_path=ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv';hmm=read(hmm_path);hmm.Date=pd.to_datetime(hmm.Date)
z=arrays[('NIKKEI225','LNN')];assert SELECT[('NIKKEI225','LNN')]=='MILD_WCE';labels=hmm[hmm.Market=='NIKKEI225'].set_index('Date').loc[z['dates'],'Regime'].to_numpy();high=labels=='High';y=z['y'];votes=z['votes'];baseline=z['persistence'];n=int(high.sum());assert n==117
seed_high=[metric(y[high],v[high]) for v in votes];mean_high={name:float(np.mean([v[name] for v in seed_high])) for name in METRICS};persist_high=metric(y[high],baseline[high]);majority_high=metric(y[high],z['majority'][high]);observed=mean_high['Balanced_Accuracy']-persist_high['Balanced_Accuracy']
assert abs(mean_high['Balanced_Accuracy']-.5392)<.0005 and abs(persist_high['Balanced_Accuracy']-.2923)<.0005 and abs(observed-.2468)<.0005
highrows=[]
for name,met in [('LNN_five_seed_metric_mean',mean_high),('LNN_majority_sensitivity',majority_high),('Persistence',persist_high)]:highrows.append({'Market':'NIKKEI225','Model':'LNN' if name!='Persistence' else 'Persistence','Loss':'MILD_WCE' if name!='Persistence' else 'BASELINE','Aggregation':name,'Regime':'High','N':n,'Positive_label_rate':y[high].mean(),**met,'Delta_BA':met['Balanced_Accuracy']-persist_high['Balanced_Accuracy'],'Delta_Macro_F1':met['Macro_F1']-persist_high['Macro_F1'],'Delta_Accuracy':met['Accuracy']-persist_high['Accuracy']})
save(highrows,'nikkei_high_primary_metrics.csv');save([{'Seed':s,**met} for s,met in zip(SEEDS,seed_high)],'nikkei_high_seed_metrics.csv')
# Efficient class-conditional metrics for the paired full-time-block bootstrap.
def multi_metrics(yy,p):
 p=np.atleast_2d(p);positive=yy==1;negative=~positive
 tp=(p[:,positive]==1).sum(axis=1);fn=positive.sum()-tp;tn=(p[:,negative]==0).sum(axis=1);fp=negative.sum()-tn
 ba=.5*(tp/positive.sum()+tn/negative.sum()) if positive.any() and negative.any() else np.full(len(p),np.nan)
 den1=2*tp+fp+fn;den0=2*tn+fp+fn
 mf=.5*(np.divide(2*tp,den1,out=np.zeros(len(p)),where=den1!=0)+np.divide(2*tn,den0,out=np.zeros(len(p)),where=den0!=0));acc=(tp+tn)/len(yy)
 return np.array([np.mean(ba),np.mean(mf),np.mean(acc)])
rng=np.random.default_rng(SEED);boot=[];invalid=0;T=len(y)
for iteration in range(B):
 starts=rng.integers(0,T-H+1,size=int(np.ceil(T/H)));ix=(starts[:,None]+np.arange(H)).ravel()[:T];ix=ix[high[ix]]
 if len(ix)==0 or len(np.unique(y[ix]))<2:invalid+=1;continue
 value=multi_metrics(y[ix],votes[:,ix])-multi_metrics(y[ix],baseline[ix]);boot.append({'Resample':iteration,'N_High':len(ix),'Delta_BA':value[0],'Delta_Macro_F1':value[1],'Delta_Accuracy':value[2]})
bs=pd.DataFrame(boot);save(bs,'nikkei_high_bootstrap_samples.csv');br=[]
for metric_name,estimate in [('Delta_BA',observed),('Delta_Macro_F1',mean_high['Macro_F1']-persist_high['Macro_F1']),('Delta_Accuracy',mean_high['Accuracy']-persist_high['Accuracy'])]:br.append({'Metric':metric_name,'Estimate':estimate,'CI_low':bs[metric_name].quantile(.025),'CI_high':bs[metric_name].quantile(.975),'Requested_resamples':B,'Valid_resamples':len(bs),'Invalid_resamples':invalid,'Block_length':H,'Seed':SEED,'HMM_refit':False,'Conditional_on_fixed_regimes':True})
save(br,'nikkei_high_block_bootstrap.csv')
# Split only at genuinely consecutive original-market High observations, never concatenate interruptions.
high_ix=np.flatnonzero(high);high_positions=z['raw_positions'][high_ix];episodes=np.cumsum(np.r_[True,np.diff(high_positions)>1]);blocks=[];block_manifest=[]
for episode in np.unique(episodes):
 members=high_ix[episodes==episode]
 for start in range(0,len(members),H):
  block=members[start:start+H];assert (np.diff(z['raw_positions'][block])==1).all();assert high[block].all();blocks.append(block)
  block_manifest.append({'Episode':int(episode),'Block':len(blocks),'N':len(block),'First_date':str(z['dates'][block[0]].date()),'Last_date':str(z['dates'][block[-1]].date()),'Raw_first_position':int(z['raw_positions'][block[0]]),'Raw_last_position':int(z['raw_positions'][block[-1]])})
save(block_manifest,'nikkei_high_permutation_blocks.csv')
positives=int(y[high].sum());negatives=n-positives;contribution=(votes==y).mean(axis=0)-(baseline==y);weights=np.where(y==1,.5/positives,.5/negatives);block_contributions=np.array([(contribution[b]*weights[b]).sum() for b in blocks]);assert np.isclose(block_contributions.sum(),observed,atol=1e-12,rtol=0)
rng=np.random.default_rng(SEED);signs=rng.choice([-1,1],size=(B,len(blocks)));permuted=signs@block_contributions
# Independently verify literal paired prediction swaps for initial sampled block-sign patterns.
for pattern,expected in zip(signs[:10],permuted[:10]):
 a=votes.copy();b=np.tile(baseline,(5,1))
 for sign,block in zip(pattern,blocks):
  if sign<0:a[:,block]=baseline[block];b[:,block]=votes[:,block]
 actual=multi_metrics(y[high],a[:,high])[0]-multi_metrics(y[high],b[:,high])[0];assert np.isclose(actual,expected,atol=1e-12,rtol=0)
p_perm=(1+int((abs(permuted)>=abs(observed)-1e-12).sum()))/(B+1)
save([{'Market':'NIKKEI225','Loss':'MILD_WCE','Regime':'High','Statistic':'mean five-seed Delta BA vs Persistence','Observed_delta_BA':observed,'Two_sided_p':p_perm,'Permutations':B,'Seed':SEED,'High_N':n,'Episodes':int(episodes.max()),'Blocks':len(blocks),'Block_max_length':H,'Short_blocks':sum(len(b)<H for b in blocks),'Blocks_cross_regime_interruptions':False,'Exploratory':True,'Post_hoc':True,'Preregistered':False,'Confirmatory':False}],'nikkei_high_block_permutation.csv')
save({'Permutation':np.arange(B),'Delta_BA':permuted},'nikkei_high_permutation_samples.csv')
# Manuscript tables keep correction families and aggregate/majority distinctions explicit.
lnn=tf[tf.Architecture=='LNN'].merge(pd.read_csv(OUT/'majority_vote_mcnemar.csv')[['Market','Delta_Accuracy','raw_p','Holm5_p']],on='Market',suffixes=('_Wilcoxon','_McNemar'),validate='one_to_one')
lnn=lnn.rename(columns={'Loss':'Selected_LNN_Loss','raw_p_Wilcoxon':'Wilcoxon_raw_p','raw_p_McNemar':'McNemar_raw_p','Holm15_p':'Wilcoxon_Holm15_p','Holm_LNN5_p':'Wilcoxon_LNN_Holm5_p','Holm5_p':'McNemar_Holm5_p','Delta_Accuracy':'Majority_Delta_Accuracy'});save(lnn,'manuscript_lnn_statistical_table.csv')
nt=pd.DataFrame(noncomp).merge(pd.read_csv(OUT/'nonoverlap_mcnemar.csv')[['Market','Holm5_p']],on='Market',validate='one_to_one');save(nt,'manuscript_nonoverlap_table.csv')
save([{'Metric':name,'LNN_MILD_WCE_seed_mean':mean_high[name],'Persistence':persist_high[name],'Difference':mean_high[name]-persist_high[name]} for name in METRICS],'manuscript_nikkei_high_panel.csv')
# Prespecified cautious interpretation, not a fitting/selection decision.
ni_non=nt[nt.Market=='NIKKEI225'].iloc[0];ba_ci=br[0]
outcome='A' if mean_high['Balanced_Accuracy']>.5 and ba_ci['CI_low']>0 and ni_non.Nonoverlap_Delta_BA>=0 and p_perm<=.05 else 'B'
interpretation={'Outcome':outcome,'Nikkei_High_BA':mean_high['Balanced_Accuracy'],'Persistence_High_BA':persist_high['Balanced_Accuracy'],'Delta_BA':observed,'Block_CI_low':ba_ci['CI_low'],'Block_CI_high':ba_ci['CI_high'],'Exploratory_block_permutation_p':p_perm,'Nonoverlap_Nikkei_Delta_BA':ni_non.Nonoverlap_Delta_BA,'BA_sign_preserved_markets':int(nt.BA_sign_preserved.sum()),'Accuracy_sign_preserved_markets':int(nt.Accuracy_sign_preserved.sum()),'Effective_independent_N_estimated':False}
js('interpretation_summary.json',interpretation)
for name,digest in inputs.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
for name,digest in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
js('analysis_manifest.json',{'status':'analysis_completed_pending_report_validation','completed_at_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':inputs,'protected_artifact_sha256':protected,'selection_test_columns_read':False,'no_training':True,'thresholds_unchanged':True,'HMM_regime_labels_unchanged':True,'packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn']}})
print(tf[['Market','Architecture','Loss','Mean_Delta_BA','raw_p','Holm15_p']].to_string(index=False));print(json.dumps(interpretation,indent=2))
