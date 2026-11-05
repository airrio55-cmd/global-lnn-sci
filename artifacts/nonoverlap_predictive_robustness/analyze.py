"""Fixed phase-zero H20 subset; saved predictions only, no fitting or selection."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,recall_score,precision_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
MARKETS={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
SEEDS=[42,52,62,72,82];inputs={}
FILES=['nonoverlap_protocol.json','selected_dates.csv','nonoverlap_metrics.csv','nonoverlap_mcnemar.csv','primary_vs_nonoverlap.csv','results_report.md','methodology_notes.md','analysis_manifest.json','completion_check.json','nonoverlap_delta_ba.png']
assert not any((OUT/name).exists() for name in FILES),'Preserve existing robustness outputs; no overwrites'
def read(p,**kw):
 p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,**kw)
def text(name,value):
 with (OUT/name).open('x') as f:f.write(value)
def js(name,value):text(name,json.dumps(value,indent=2)+'\n')
def save(name,rows):pd.DataFrame(rows).to_csv(OUT/name,index=False,float_format='%.17g',mode='x')
def metrics(y,p):return {'Accuracy':accuracy_score(y,p),'Balanced_Accuracy':balanced_accuracy_score(y,p),'Macro_F1':f1_score(y,p,labels=[0,1],average='macro',zero_division=0),'Recall':recall_score(y,p,zero_division=0),'Precision':precision_score(y,p,zero_division=0),'F1':f1_score(y,p,zero_division=0),'Pred_Pos_Rate':p.mean()}
def holm(p):
 p=np.array(p,float);ix=np.argsort(p);a=np.empty(len(p));a[ix]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[ix]));return a
js('nonoverlap_protocol.json',{'scope':'Final explanatory robustness to overlapping H=20 labels; not model selection or a replacement for main results','markets':MARKETS,'frozen_best_source':'artifacts/cross_market_statistics/market_best_models.csv','representative_prediction':'Each original seed probability > original saved threshold, then >=3 positive votes among all five seeds; never probability averaging','sampling':{'sort':'chronological existing frozen test prediction rows','phase':0,'step':20,'offsets_evaluated':[0],'alternative_phase_search':False},'Persistence':'Exact saved full-test Persistence predictions, independently matched to original Close(t)>Close(t-20) definition','McNemar':{'two_sided':True,'alpha':.05,'primary_p':'max(exact binomial p, continuity-corrected chi-square p)','Holm_family':'Exactly five market-level p-values','tests':'Accuracy/correctness, not Balanced Accuracy'},'training':False,'model_or_feature_or_threshold_changes':False,'HMM_or_economic_changes':False,'independence_limit':'Reduced label overlap does not guarantee complete serial independence; smaller N reduces power'})
best=read(ROOT/'artifacts/cross_market_statistics/market_best_models.csv',float_precision='round_trip').set_index('Market');primary=read(ROOT/'artifacts/cross_market_statistics/mcnemar_results.csv',float_precision='round_trip').set_index('Market')
selected=[];metricrows=[];mcnemar=[];comparisons=[];checks=[]
for market,folder in MARKETS.items():
 b=best.loc[market];model,loss=b.Best_Model,b.Loss
 full=read(ROOT/f'artifacts/cross_market_statistics/{market}_majority_predictions.csv',float_precision='round_trip')
 dates=pd.DatetimeIndex(pd.to_datetime(full.Date));assert dates.is_unique and dates.is_monotonic_increasing
 y=full.Y_true.to_numpy(int);saved_majority=full.Majority_prediction.to_numpy(int);persistence=full.Persistence_prediction.to_numpy(int)
 source=ROOT/folder;seedtable=read(source/'seed_results.csv',float_precision='round_trip');votes=[]
 for seed in SEEDS:
  p=read(source/'predictions'/f'{model}_{loss}_{seed}.csv',float_precision='round_trip')
  assert np.array_equal(pd.to_datetime(p.Date).to_numpy(),dates.to_numpy()) and np.array_equal(p.Y_true,y)
  row=seedtable[(seedtable.Model==model)&(seedtable.Loss==loss)&(seedtable.Seed.astype(str)==str(seed))].iloc[0]
  assert np.allclose(p.Threshold,row.Threshold,rtol=0,atol=1e-14)
  pred=(p.Probability.to_numpy()>row.Threshold).astype(int);assert np.array_equal(pred,full[f'Seed_{seed}_prediction'])
  assert np.isclose(balanced_accuracy_score(y,pred),row.Balanced_Accuracy,rtol=0,atol=1e-12)
  votes.append(pred)
 assert np.array_equal((np.array(votes).sum(axis=0)>=3).astype(int),saved_majority)
 raw=read(source/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');loc=raw.index.get_indexer(dates);close=raw.Close.to_numpy()
 assert (loc>=20).all() and (loc+20<len(raw)).all()
 assert np.array_equal((close[loc]>close[loc-20]).astype(int),persistence)
 assert np.array_equal((close[loc+20]>close[loc]).astype(int),y)
 full_b=metrics(y,saved_majority);full_p=metrics(y,persistence)
 assert np.isclose(full_b['Balanced_Accuracy'],primary.loc[market,'Majority_BA'],atol=1e-12,rtol=0)
 assert np.isclose(full_b['Accuracy']-full_p['Accuracy'],primary.loc[market,'Delta_Accuracy'],atol=1e-12,rtol=0)
 ix=np.arange(0,len(full),20);assert ix[0]==0 and np.array_equal(ix,np.arange(0,len(full),20))
 assert (np.diff(loc[ix])>=20).all(),'Observed prediction row spacing must not be shorter than 20 frozen market observations'
 for k,i in enumerate(ix):
  selected.append({'Market':market,'Model':model,'Loss':loss,'Selection_number':k,'Original_prediction_row':int(i),'Date':str(dates[i].date()),'Frozen_market_row':int(loc[i]),'Horizon_end_date':str(raw.index[loc[i]+20].date()),'Market_observations_since_previous':int(loc[i]-loc[ix[k-1]]) if k else np.nan,'Y_true':int(y[i]),'Best_majority_prediction':int(saved_majority[i]),'Persistence_prediction':int(persistence[i]),**{f'Seed_{s}_prediction':int(votes[j][i]) for j,s in enumerate(SEEDS)}})
 yy=y[ix];bm=saved_majority[ix];pp=persistence[ix]
 assert len(np.unique(yy))==2
 mb=metrics(yy,bm);mp=metrics(yy,pp)
 for name,m in [('Frozen_Best_Majority',mb),('Persistence',mp)]:metricrows.append({'Market':market,'Model':model if name!='Persistence' else 'Persistence','Loss':loss if name!='Persistence' else 'BASELINE','Prediction':name,'N':len(ix),'Positive_label_rate':yy.mean(),**m,**{'Delta_'+key:mb[key]-mp[key] for key in ['Accuracy','Balanced_Accuracy','Macro_F1']}})
 a=bm==yy;c=pp==yy;n00=int((~a&~c).sum());n01=int((~a&c).sum());n10=int((a&~c).sum());n11=int((a&c).sum());n=n01+n10
 exact=stats.binomtest(n10,n,.5,alternative='two-sided').pvalue if n else 1.;stat=max(abs(n01-n10)-1,0)**2/n if n else 0.;cc=stats.chi2.sf(stat,1) if n else 1.
 mcnemar.append({'Market':market,'N':len(ix),'n00':n00,'n01':n01,'n10':n10,'n11':n11,'McNemar_statistic_CC':stat,'exact_binomial_p':exact,'continuity_corrected_p':cc,'primary_p':max(exact,cc),'Delta_Accuracy':mb['Accuracy']-mp['Accuracy']})
 dbfull=full_b['Balanced_Accuracy']-full_p['Balanced_Accuracy'];dbnon=mb['Balanced_Accuracy']-mp['Balanced_Accuracy'];dafull=full_b['Accuracy']-full_p['Accuracy'];danon=mb['Accuracy']-mp['Accuracy']
 comparisons.append({'Market':market,'Model':model,'Loss':loss,'Full_N':len(y),'Nonoverlap_N':len(ix),'Full_Delta_BA':dbfull,'Nonoverlap_Delta_BA':dbnon,'Full_Delta_Accuracy':dafull,'Nonoverlap_Delta_Accuracy':danon,'Delta_BA_sign_preserved':bool(np.sign(dbfull)==np.sign(dbnon)),'Delta_Accuracy_sign_preserved':bool(np.sign(dafull)==np.sign(danon)),'Full_Delta_Macro_F1':full_b['Macro_F1']-full_p['Macro_F1'],'Nonoverlap_Delta_Macro_F1':mb['Macro_F1']-mp['Macro_F1']})
 checks.append({'Market':market,'selected_N':len(ix),'first_date':str(dates[0].date()),'selected_dates_exact_original_rows':True,'exact_every20_prediction_rows':True,'minimum_actual_market_spacing':int(np.diff(loc[ix]).min()),'Persistence_matches_saved_and_original_definition':True,'thresholds_and_best_unchanged':True})
mc=pd.DataFrame(mcnemar);assert len(mc)==5;mc['Holm_p']=holm(mc.primary_p);mc['significant_at_0_05']=mc.Holm_p<.05
save('selected_dates.csv',selected);save('nonoverlap_metrics.csv',metricrows);save('nonoverlap_mcnemar.csv',mc);save('primary_vs_nonoverlap.csv',comparisons)
co=pd.DataFrame(comparisons);x=np.arange(5);fig,ax=plt.subplots(figsize=(10,5));ax.bar(x-.18,co.Full_Delta_BA,.36,label='Primary full test',color='#999999');ax.bar(x+.18,co.Nonoverlap_Delta_BA,.36,label='Fixed phase 0, every 20th row',color='#2166ac');ax.axhline(0,color='black',lw=.8);ax.set_xticks(x,co.Market);ax.set_ylabel('Majority-vote BA minus Persistence BA');ax.set_title('Predictive robustness to H=20 label overlap; no phase search');ax.legend();fig.tight_layout();fig.savefig(OUT/'nonoverlap_delta_ba.png',dpi=180);plt.close(fig)
notes='''# Methodology

This analysis addresses robustness to overlapping H=20 forecast labels using a prespecified every-20-observation subset beginning with the first existing test observation (zero-based rows0,20,40,...). No alternative offset was evaluated. It is not a new model-selection exercise and does not replace the main full-test results.

Frozen Best selections come only from cross_market_statistics/market_best_models.csv. SP500 uses sp500_rerun exclusively; no archived SP500 or failed reconstruction is used. Original saved thresholds, seed votes, majority votes, labels and Persistence from the primary analysis are verified exactly. Probabilities are not averaged and no model is run, trained or retuned. Thresholds are cross-checked against unchanged seed result tables. Source inputs are hashed before/after.

Selected_dates.csv stores original row indices, dates, 20-observation label end dates, labels, all seed votes, majority votes and Persistence. Dates are sorted/unique, the first row is selected, and source market observation gaps between selected dates are at least20. This audits the requested observed-prediction-row sampling rather than substituting calendar-day spacing. Forecasts at t and t+20 share an endpoint price but not an intervening daily return interval. Missing prediction rows could create wider gaps; the actual spacing is recorded, not inferred.

Metrics use the binary labels0/1. Macro F1 explicitly uses both classes and zero_division0; Recall/Precision/F1 are positive-class metrics. Both classes exist in every selected market subset. Delta=Best majority minus Persistence. Delta columns in nonoverlap_metrics.csv are the same pair-level contrast on both benchmark/model rows, not separate benchmark self-differences. Full-test contrasts are majority-vote metrics, not five-seed mean BA, and match saved primary McNemar outputs.

McNemar table: n00=both wrong; n01=Persistence correct/Best wrong; n10=Best correct/Persistence wrong; n11=both correct. Exact p is a two-sided binomial discordance test; continuity-corrected statistic=max(abs(n01−n10)−1,0)^2/(n01+n10). With no discordance p=1. Primary p is the larger of the exact and continuity-corrected p-values. Holm adjusts exactly five market p-values, alpha0.05. McNemar tests Accuracy/correctness, NOT Balanced Accuracy.

Reduced overlap does not guarantee complete serial independence. Remaining market dependence, regime persistence and shared training history remain. Small non-overlapping samples reduce statistical power; a nonsignificant result does not establish equivalence. Original frozen Best configurations were selected from test BA in earlier exploratory analyses, and this check does not remove post-selection uncertainty. Negative and nonsignificant results are retained unchanged. Sign preservation is exact numerical sign agreement; zero is a distinct sign. No HMM, economic or primary experimental artifact is changed.
'''
text('methodology_notes.md',notes)
lines=['# Final non-overlapping predictive robustness','','This analysis addresses robustness to overlapping H=20 forecast labels. The prespecified subset starts at the first frozen test observation and selects every20th observed prediction row. No model selection, phase search, training, new prediction or threshold change. Main full-test results remain unchanged.','','|Market|N full / subset|Full delta BA|Subset delta BA|BA sign preserved|Full delta accuracy|Subset delta accuracy|Holm p|','|---|---:|---:|---:|---|---:|---:|---:|']
for r in co.itertuples():
 p=mc[mc.Market==r.Market].iloc[0];lines.append(f'|{r.Market}|{r.Full_N} / {r.Nonoverlap_N}|{r.Full_Delta_BA:+.6f}|{r.Nonoverlap_Delta_BA:+.6f}|{r.Delta_BA_sign_preserved}|{r.Full_Delta_Accuracy:+.6f}|{r.Nonoverlap_Delta_Accuracy:+.6f}|{p.Holm_p:.6g}|')
lines+=['','Full contrasts use the same frozen majority vote as the primary cross-market analysis, not means of seed metrics. McNemar concerns accuracy, not BA. It is exploratory: reduced label overlap does not guarantee complete serial independence, and small subset N reduces power. Prior test-based Best selection remains a limitation. Negative and nonsignificant results are retained.','','## Paired McNemar details','','|Market|n00|n01|n10|n11|Exact p|Continuity-corrected p|Primary p|Holm p|','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in mc.itertuples():lines.append(f'|{r.Market}|{r.n00}|{r.n01}|{r.n10}|{r.n11}|{r.exact_binomial_p:.6g}|{r.continuity_corrected_p:.6g}|{r.primary_p:.6g}|{r.Holm_p:.6g}|')
lines+=['','## Findings','','BA sign preserved in '+str(int(co.Delta_BA_sign_preserved.sum()))+'/5 markets; accuracy sign preserved in '+str(int(co.Delta_Accuracy_sign_preserved.sum()))+'/5. Holm-significant market-level McNemar tests: '+str(int(mc.significant_at_0_05.sum()))+'/5. This is a robustness check only, not a replacement for main results or evidence of equivalence. See selected_dates.csv and methodology_notes.md for exact phase, spacing and integrity checks.']
text('results_report.md','\n'.join(lines)+'\n')
# Independent saved-row, contingency, exact-p and Holm verification before validation status.
sd=pd.read_csv(OUT/'selected_dates.csv');assert len(sd)==sum(r['selected_N'] for r in checks)
for market in MARKETS:
 s=sd[sd.Market==market];src=pd.read_csv(ROOT/f'artifacts/cross_market_statistics/{market}_majority_predictions.csv');ix=s.Original_prediction_row.to_numpy(int);assert np.array_equal(ix,np.arange(0,len(src),20))
 for left,right in [('Y_true','Y_true'),('Best_majority_prediction','Majority_prediction'),('Persistence_prediction','Persistence_prediction')]:assert np.array_equal(s[left],src.iloc[ix][right])
 r=mc[mc.Market==market].iloc[0];assert r.n00+r.n01+r.n10+r.n11==len(s);n=int(r.n01+r.n10);exact=min(1.,2*stats.binom.cdf(min(r.n01,r.n10),n,.5)) if n else 1.;assert np.isclose(exact,r.exact_binomial_p,atol=1e-14,rtol=0)
ordered=mc.sort_values('primary_p');prior=0
for i,r in enumerate(ordered.itertuples()):prior=max(prior,min(1,(5-i)*r.primary_p));assert np.isclose(prior,r.Holm_p,atol=1e-14,rtol=0)
for p,digest in inputs.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest
js('analysis_manifest.json',{'status':'completed','completed_at_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':inputs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn','matplotlib']},'market_sources':MARKETS,'source_artifacts_unchanged':True,'training_performed':False,'existing_predictions_replaced':False})
js('completion_check.json',{'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'market_checks':checks,'no_model_training':True,'source_prediction_hashes_unchanged':True,'thresholds_unchanged':True,'best_configurations_unchanged':True,'first_date_phase_fixed':True,'exact_every20_frozen_prediction_rows':True,'phase_search':False,'selected_labels_predictions_exact_saved_rows':True,'Persistence_exact_reproduction':True,'Holm_exactly_five_markets':True,'independent_saved_row_and_p_value_checks':True,'existing_HMM_economic_and_primary_results_unchanged':True})
print(co[['Market','Full_N','Nonoverlap_N','Full_Delta_BA','Nonoverlap_Delta_BA','Delta_BA_sign_preserved']].to_string(index=False));print(mc[['Market','primary_p','Holm_p','significant_at_0_05']].to_string(index=False))
