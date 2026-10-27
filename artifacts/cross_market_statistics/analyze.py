"""Read-only post-hoc statistics; no fitting, prediction generation or threshold search."""
from pathlib import Path
import hashlib,json,itertools
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import balanced_accuracy_score,f1_score,accuracy_score
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
ALPHA=.05; RNG_SEED=20261026; RESAMPLES=10000
MARKETS={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
SEEDS=[42,52,62,72,82]
CONFIGS=list(itertools.product(['LNN','LSTM','Transformer'],['CE','MILD_FOCAL','MILD_WCE']))
inputs={}
def read(p,**kwargs):
 p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,**kwargs)
def holm(p):
 p=np.asarray(p,float);order=np.argsort(p);a=np.empty(len(p));a[order]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[order]));return a
def save(rows,name):
 f=pd.DataFrame(rows);f.to_csv(OUT/name,index=False,float_format='%.17g');return f
best=[];boots=[];mc=[];deltas=[];mat=[];audit=[]
rng=np.random.default_rng(RNG_SEED)
for market,d in MARKETS.items():
 directory=ROOT/d
 f=read(directory/'seed_results.csv');learn=f[f.Seed.astype(str)!='BASELINE'].copy();learn.Seed=learn.Seed.astype(int)
 assert len(learn)==45 and not learn.duplicated(['Model','Loss','Seed']).any()
 assert set(learn[['Model','Loss','Seed']].itertuples(index=False,name=None))==set((m,l,s) for m,l in CONFIGS for s in SEEDS)
 p=f[f.Model=='Persistence'].iloc[0]
 g=learn.groupby(['Model','Loss']).agg(Mean_BA=('Balanced_Accuracy','mean'),SD_BA=('Balanced_Accuracy','std'),Macro_F1=('Macro_F1','mean'))
 b=g.sort_values(['Mean_BA','Model','Loss'],ascending=[False,True,True]).iloc[0];model,loss=b.name
 selected=learn[(learn.Model==model)&(learn.Loss==loss)].sort_values('Seed')
 delta=selected.Balanced_Accuracy.to_numpy()-p.Balanced_Accuracy
 row={'Market':market,'Best_Model':model,'Loss':loss,**b.to_dict(),'Persistence_BA':p.Balanced_Accuracy,'Delta_BA':float(delta.mean()),'Seeds_above_Persistence':int((delta>0).sum()),'Delta_vs_neutral_0_5':b.Mean_BA-.5,'Persistence_below_0_5':bool(p.Balanced_Accuracy<.5),'Persistence_Macro_F1':p.Macro_F1,'Delta_Macro_F1':b.Macro_F1-p.Macro_F1,'BA_improves_F1_worsens':bool(delta.mean()>0 and b.Macro_F1<p.Macro_F1),'Selection':'post-hoc highest five-seed mean TEST BA; exploratory'}
 best.append(row)
 for s,x in zip(SEEDS,delta):deltas.append({'Market':market,'Seed':s,'Delta_BA':x})
 samples=rng.choice(delta,size=(RESAMPLES,5),replace=True).mean(axis=1)
 w=stats.wilcoxon(delta,alternative='two-sided',method='exact') if np.any(delta) else (0,1)
 boots.append({'Market':market,'Mean_Delta_BA':delta.mean(),'Median_Delta_BA':np.median(delta),'SD_Delta_BA':delta.std(ddof=1),'Min':delta.min(),'Max':delta.max(),'Bootstrap_CI_low':np.quantile(samples,.025),'Bootstrap_CI_high':np.quantile(samples,.975),'Resamples':RESAMPLES,'RNG_seed':RNG_SEED,'Wilcoxon_statistic':float(w[0]),'raw_p':float(w[1]),'N_seeds':5})
 mat.append([g.loc[c,'Mean_BA'] for c in CONFIGS])
 source_summary=read(directory/'summary.csv')
 selected_summary=source_summary[(source_summary.Model==model)&(source_summary.Loss==loss)].iloc[0]
 assert np.isclose(selected_summary.Balanced_Accuracy_mean,b.Mean_BA,atol=1e-12,rtol=0)
 assert np.isclose(selected_summary.Balanced_Accuracy_std,b.SD_BA,atol=1e-12,rtol=0)
 prediction_dir=directory/'predictions'
 paths=[prediction_dir/f'{model}_{loss}_{s}.csv' for s in SEEDS]
 assert all(x.exists() for x in paths),f'{market}: missing required prediction file'
 raw=read(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');px=raw.Close.dropna()
 reference=None;votes=[]
 for seed,path in zip(SEEDS,paths):
  pred=read(path,float_precision='round_trip').rename(columns={'y_true':'Y_true','probability':'Probability'});dates=pd.DatetimeIndex(pd.to_datetime(pred.Date));assert dates.is_unique and dates.is_monotonic_increasing
  y=pred.Y_true.to_numpy(int);assert set(y)<={0,1}
  positions=px.index.get_indexer(dates);assert (positions>=20).all() and (positions+20<len(px)).all()
  # Identical deterministic baseline definition from completed notebook, not a new model.
  baseline=(px.to_numpy()[positions]>px.to_numpy()[positions-20]).astype(int)
  expected_y=(px.to_numpy()[positions+20]>px.to_numpy()[positions]).astype(int);assert np.array_equal(y,expected_y)
  threshold=selected[selected.Seed==seed].iloc[0].Threshold
  assert np.allclose(pred.Threshold,threshold,rtol=0,atol=1e-14)
  assert pred.Probability.between(0,1).all() and pred.Probability.notna().all()
  model_pred=(pred.Probability.to_numpy()>threshold).astype(int)
  if 'Y_pred' in pred:assert np.array_equal(model_pred,pred.Y_pred.to_numpy(int))
  if market=='SP500':
   persisted=read(directory/'baseline_predictions.csv')
   assert np.array_equal(pd.to_datetime(persisted.Date).to_numpy(),dates.to_numpy())
   assert np.array_equal(persisted.Y_true,y) and np.array_equal(persisted.Persistence,baseline)
  if reference is None:reference=(dates,y,baseline)
  else:
   assert dates.equals(reference[0]) and np.array_equal(y,reference[1]) and np.array_equal(baseline,reference[2])
  sr=selected[selected.Seed==seed].iloc[0]
  for actual,expected in [(balanced_accuracy_score(y,model_pred),sr.Balanced_Accuracy),(f1_score(y,model_pred,average='macro'),sr.Macro_F1),(balanced_accuracy_score(y,baseline),p.Balanced_Accuracy),(f1_score(y,baseline,average='macro'),p.Macro_F1),(accuracy_score(y,baseline),p.Accuracy)]:assert np.isclose(actual,expected,atol=1e-12,rtol=0)
  votes.append(model_pred)
 # Primary market-level test: majority of five existing thresholded seed predictions.
 majority=(np.asarray(votes).sum(axis=0)>=3).astype(int)
 a=majority==y;b0=baseline==y
 n00=int((~a&~b0).sum());n01=int((~a&b0).sum());n10=int((a&~b0).sum());n11=int((a&b0).sum());discord=n01+n10
 exact=stats.binomtest(n10,discord,.5,alternative='two-sided').pvalue if discord else 1.
 statistic=max(abs(n01-n10)-1,0)**2/discord if discord else 0.
 cc=stats.chi2.sf(statistic,1) if discord else 1.
 mc.append({'Market':market,'Prediction_rule':'five-seed majority vote (at least 3/5); original per-seed thresholds','status':'computed','Model':model,'Loss':loss,'N':len(y),'n00':n00,'n01':n01,'n10':n10,'n11':n11,'McNemar_statistic_CC':statistic,'exact_p':exact,'continuity_corrected_p':cc,'raw_p':max(exact,cc),'Model_Accuracy':float(a.mean()),'Persistence_Accuracy':float(b0.mean()),'Delta_Accuracy':float(a.mean()-b0.mean()),'Majority_BA':balanced_accuracy_score(y,majority),'Majority_Macro_F1':f1_score(y,majority,average='macro')})
 save(pd.DataFrame({'Date':dates,'Y_true':y,'Persistence_prediction':baseline,'Seed_42_prediction':votes[0],'Seed_52_prediction':votes[1],'Seed_62_prediction':votes[2],'Seed_72_prediction':votes[3],'Seed_82_prediction':votes[4],'Majority_prediction':majority}),market+'_majority_predictions.csv')
 audit.append({'Market':market,'status':'paired_integrity_passed','N':len(reference[1]),'baseline':'Reproduced original deterministic Close(t)>Close(t-20) on frozen input; BA/F1/accuracy match saved baseline','labels':'Verified against frozen 20-observation target; identical across all five seeds'})
bestf=save(best,'market_best_models.csv');bootf=pd.DataFrame(boots);bootf['Holm_p']=holm(bootf.raw_p);bootf['significant']=bootf.Holm_p<ALPHA;bootf.to_csv(OUT/'seed_bootstrap_results.csv',index=False)
save(deltas,'seed_deltas.csv')
mcf=pd.DataFrame(mc);valid=mcf.raw_p.notna();assert len(mcf)==5 and valid.all()
mcf['Holm_p']=holm(mcf.raw_p);mcf['significant']=mcf.Holm_p<ALPHA;mcf.to_csv(OUT/'mcnemar_results.csv',index=False)
save(audit,'prediction_integrity_audit.csv')
mat=np.asarray(mat);posthoc=[]
fr=[]
for name,indices in [('ce_only',[i for i,c in enumerate(CONFIGS) if c[1]=='CE']),('all_configs',list(range(9)))]:
 data=mat[:,indices];stat,pval=stats.friedmanchisquare(*data.T)
 fr.append({'Comparison':name,'N_markets':5,'N_configurations':len(indices),'Friedman_statistic':stat,'raw_p':pval,'Kendall_W':stat/(5*(len(indices)-1))})
frf=pd.DataFrame(fr);frf['Holm_p']=holm(frf.raw_p);frf['significant']=frf.Holm_p<ALPHA
for row in frf.to_dict('records'):
 save([row],'friedman_'+row['Comparison']+'.csv')
 if row['significant']:
  ix=[i for i,c in enumerate(CONFIGS) if c[1]=='CE'] if row['Comparison']=='ce_only' else list(range(9))
  for a,b in itertools.combinations(ix,2):
   diff=mat[:,a]-mat[:,b];w=stats.wilcoxon(diff,alternative='two-sided',method='exact') if np.any(diff) else (0,1)
   posthoc.append({'Family':row['Comparison'],'Config_A':' '.join(CONFIGS[a]),'Config_B':' '.join(CONFIGS[b]),'statistic':float(w[0]),'raw_p':float(w[1])})
post=pd.DataFrame(posthoc,columns=['Family','Config_A','Config_B','statistic','raw_p'])
post['Holm_p']=pd.Series(dtype=float);post['significant']=pd.Series(dtype=bool)
if len(post):
 # One joint family across every triggered pairwise test.
 post['Holm_p']=holm(post.raw_p);post['significant']=post.Holm_p<ALPHA
post.to_csv(OUT/'posthoc_wilcoxon.csv',index=False)
for name,indices in [('all_configs',list(range(9))),('ce_only',[i for i,c in enumerate(CONFIGS) if c[1]=='CE'])]:
 ranks=np.array([stats.rankdata(-row[indices],method='average') for row in mat]);rows=[]
 for j,i in enumerate(indices):
  rows.append({'Model':CONFIGS[i][0],'Loss':CONFIGS[i][1],'Mean_rank':ranks[:,j].mean(),'Median_rank':np.median(ranks[:,j]),**{m:ranks[k,j] for k,m in enumerate(MARKETS)}})
 save(rows,'rankings_'+name+'.csv')
save([{'Market':m,'Model':c[0],'Loss':c[1],'Mean_BA':mat[k,j]} for k,m in enumerate(MARKETS) for j,c in enumerate(CONFIGS)],'fixed_configuration_means.csv')
bestf[['Market','Best_Model','Loss','Macro_F1','Persistence_Macro_F1','Delta_Macro_F1','BA_improves_F1_worsens']].to_csv(OUT/'macro_f1_robustness.csv',index=False)
for path,digest in inputs.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
(OUT/'analysis_manifest.json').write_text(json.dumps({'alpha':ALPHA,'two_sided':True,'resamples':RESAMPLES,'rng_seed':RNG_SEED,'training_performed':False,'source_files_unchanged':True,'status':'completed' if all(r['status']=='computed' for r in mc) else 'completed_with_missing_SP500_sample_predictions','packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn']},'market_directories':MARKETS,'input_sha256':inputs,'mcnemar_policy':'User-requested five-seed majority votes of original thresholded predictions, no seed selection or threshold changes. Holm over exactly five available market-level tests. S&P500 uses only artifacts/sp500_rerun (archived SP500 and failed reconstruction excluded). No seed-specific McNemar tests are performed. Primary raw p=max(exact,continuity-corrected).','families':'McNemar 5; seed Wilcoxon 5; Friedman 2; all triggered posthoc pairs jointly.','bootstrap':'Percentile resampling of five training seeds, conditional on fixed test history. Not a time-series or population uncertainty CI.'},indent=2))
lines=['# Five-market exploratory statistics','', 'No retraining, tuning, threshold search or prediction replacement. Best model/loss selected post hoc by highest five-seed mean TEST BA, as requested. This selection introduces optimism; p-values are descriptive/exploratory and Holm does not correct the prior test-based winner selection.','', '## Best configurations','', '|Market|Model|Loss|Mean BA|Delta Persistence|Delta 0.5|Delta Macro F1|','|---|---|---|---:|---:|---:|---:|']
for r in best:lines.append(f"|{r['Market']}|{r['Best_Model']}|{r['Loss']}|{r['Mean_BA']:.6f}|{r['Delta_BA']:+.6f}|{r['Delta_vs_neutral_0_5']:+.6f}|{r['Delta_Macro_F1']:+.6f}|")
lines+=['','## McNemar','', 'Primary McNemar uses user-requested five-seed majority votes: threshold each seed using its original validation-selected threshold, then predict positive if at least three of five vote positive. No threshold search or probability averaging. S&P500 uses the completed reproducible rerun in artifacts/sp500_rerun; archived SP500 and failed replay outputs are excluded. Holm adjusts exactly five computed market p-values. No seed-specific McNemar tests are performed or included. Ensemble metrics differ from the five-seed mean metrics in market_best_models.csv and are labeled separately.', '', 'Persistence labels were reproduced from frozen Close data using the unchanged original deterministic baseline definition and verified against stored metrics. All computed pairs have identical dates and y_true; model BA/F1 and persistence BA/F1/accuracy reproduce saved rows.', '', 'McNemar tests equality of error probability/accuracy, NOT Balanced Accuracy. The primary p-value is the larger of exact binomial and continuity-corrected asymptotic p-values. Overlapping 20-observation targets and serial dependence violate the independent-pair assumption of ordinary McNemar; exact means exact under its model, not dependence-robust. No confirmatory time-series significance claim is justified by these p-values.', '', '## Seed bootstrap and Wilcoxon','', '10,000 percentile bootstrap samples of five seed deltas, RNG seed 20261026. This captures conditional training-seed variation, not uncertainty across independent market histories. Seeds share the same test set. With five nonzero differences, the smallest two-sided exact Wilcoxon p is 0.0625; alpha=0.05 significance is unattainable even before Holm. Ties/zero differences may alter exactness.', '', '## Friedman and post-hoc','']
for r in frf.to_dict('records'):lines.append(f"- {r['Comparison']}: statistic={r['Friedman_statistic']:.6f}, raw p={r['raw_p']:.6g}, Holm p={r['Holm_p']:.6g}, significant={r['significant']}.")
lines+=['','Friedman uses five market blocks of five-seed mean BA, not 25 independent blocks. CE-only and fixed nine-configuration comparisons remain separate; no architecture-specific best-loss selection. Holm corrects the two omnibus tests. Pairwise Wilcoxon runs only for a Holm-significant omnibus, with joint Holm across all triggered pairs. Five markets yield low power and chi-square Friedman p-values are asymptotic. Markets are economically correlated; block independence is an approximation.', '', 'Ranks use 1=highest BA and average ranks for ties. A lower-than-0.5 Persistence baseline makes a positive delta insufficient evidence of useful predictive superiority. BA improvements alongside worse Macro F1 are explicitly flagged. KOSPI200 uses its user-authorized empirical observation calendar; 45 XKRX date discrepancies are not confirmed missing KRX observations.', '', '## Scope','', 'All five market-level McNemar tests are available. SP500 data source: artifacts/sp500_rerun only. All input prediction and seed files remain unchanged, verified by SHA256. The five-seed representative is a majority vote of separately thresholded predictions, not a new tuned model. Architecture ranking is CE-only; fixed-configuration ranking is separately reported for all nine configurations.']
lines += ['', '## Majority-vote McNemar results', '', '|Market|N|Delta Accuracy|Majority BA|Primary raw p|Holm p|Significant|', '|---|---:|---:|---:|---:|---:|---|']
for r in mcf.itertuples():
 lines.append(f'|{r.Market}|{r.N}|{r.Delta_Accuracy:+.6f}|{r.Majority_BA:.6f}|{r.raw_p:.6g}|{r.Holm_p:.6g}|{r.significant}|')
lines += ['', 'These significance flags concern accuracy equality under ordinary McNemar assumptions; the sign of Delta Accuracy indicates improvement versus deterioration. They do not test BA directly. Majority-vote metrics are distinct from five-seed means.', '', '## Seed-delta bootstrap', '', '|Market|Mean delta BA|95% percentile CI|Wilcoxon raw p|Holm p|', '|---|---:|---|---:|---:|']
for r in bootf.itertuples():
 lines.append(f'|{r.Market}|{r.Mean_Delta_BA:+.6f}|[{r.Bootstrap_CI_low:+.6f}, {r.Bootstrap_CI_high:+.6f}]|{r.raw_p:.6g}|{r.Holm_p:.6g}|')
lines += ['', 'Five-seed CIs describe conditional seed variability; they are not independence-corrected market-history confidence intervals. All five selected configurations have lower mean Macro F1 than Persistence; BA increases with Macro F1 deterioration are flagged for Nikkei225, EURO STOXX 50 and KOSPI200.', '', 'Post-hoc status: not performed because neither Holm-corrected omnibus test is significant. posthoc_wilcoxon.csv contains headers and no comparisons. See rankings_ce_only.csv for architecture ranks without best-loss selection and rankings_all_configs.csv for fixed model/loss ranks.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n')
print(bestf[['Market','Best_Model','Loss','Mean_BA','Delta_BA']].to_string(index=False));print(frf.to_string(index=False));print('Computed McNemar:',int(valid.sum()),'unavailable:',int((~valid).sum()))

(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
