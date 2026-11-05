from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,itertools
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import balanced_accuracy_score,f1_score,accuracy_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
manifest=json.loads((OUT/'analysis_manifest.json').read_text());protocol=json.loads((OUT/'analysis_protocol.json').read_text())
for group in ['input_sha256','protected_artifact_sha256']:
 for name,digest in manifest[group].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
selection=pd.read_csv(OUT/'selected_primary_configs.csv');sf=pd.read_csv(OUT/'seed_level_primary_metrics.csv');tf=pd.read_csv(OUT/'validation_selected_statistical_tests.csv');nf=pd.read_csv(OUT/'nonoverlap_comparison_full.csv');mr=pd.read_csv(OUT/'majority_predictions_all_architectures.csv');dates=pd.read_csv(OUT/'nonoverlap_selected_dates.csv')
assert len(selection)==15 and len(sf)==75 and len(tf)==15
assert not sf.duplicated(['Market','Architecture','Seed']).any()
assert all(sorted(g.Seed)==[42,52,62,72,82] for _,g in sf.groupby(['Market','Architecture']))
for r in selection.itertuples():
 f=pd.read_csv(ROOT/r.Summary_source,usecols=['Model','Loss','WF_Val_BA_mean']);f=f[f.Model==r.Architecture].sort_values(['WF_Val_BA_mean','Loss'],ascending=[False,True]);assert f.iloc[0].Loss==r.Loss
for market,g in dates.groupby('Market'):
 source=mr[(mr.Market==market)&(mr.Architecture=='LNN')].reset_index(drop=True);ix=np.arange(0,len(source),20);assert np.array_equal(g.Original_prediction_row,ix)
 for a,b in [('Y_true','Y_true'),('LNN_majority','Majority_prediction'),('Persistence','Persistence_prediction')]:assert np.array_equal(g[a],source.iloc[ix][b])
 assert np.array_equal(pd.to_datetime(g.Date),pd.to_datetime(source.iloc[ix].Date))
for _,g in mr.groupby(['Market','Architecture']):
 votes=g[[f'Seed_{s}_prediction' for s in [42,52,62,72,82]]].to_numpy();assert np.array_equal((votes.sum(axis=1)>=3).astype(int),g.Majority_prediction)
def verify_holm(frame,pcol,outcol):
 prior=0
 for i,r in enumerate(frame.sort_values(pcol).to_dict('records')):
  prior=max(prior,min(1,(len(frame)-i)*r[pcol]));assert np.isclose(prior,r[outcol],atol=1e-12,rtol=0)
verify_holm(tf,'raw_p','Holm15_p');verify_holm(tf[tf.Architecture=='LNN'],'raw_p','Holm_LNN5_p')
for filename in ['majority_vote_mcnemar.csv','nonoverlap_mcnemar.csv']:
 f=pd.read_csv(OUT/filename);assert len(f)==5;verify_holm(f,'raw_p','Holm5_p')
 for r in f.itertuples():
  assert r.n00+r.n01+r.n10+r.n11==r.N;n=int(r.n01+r.n10);exact=min(1,2*stats.binom.cdf(min(r.n01,r.n10),n,.5)) if n else 1
  assert np.isclose(exact,r.exact_p,atol=1e-12,rtol=0) and np.isclose(max(r.exact_p,r.continuity_corrected_p),r.raw_p,atol=1e-12,rtol=0)
ff=pd.read_csv(OUT/'architecture_friedman_tests.csv');verify_holm(ff,'raw_p','Holm2_p')
for r in ff.itertuples():
 a=sf.groupby(['Market','Architecture'])[r.Metric].mean().unstack().loc[['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'],['LNN','LSTM','Transformer']];z,p=stats.friedmanchisquare(*a.to_numpy().T);assert np.isclose(z,r.Friedman_statistic) and np.isclose(p,r.raw_p)
# Independently replay block resampling indices; verify invalid count and initial metric samples with sklearn.
g=mr[(mr.Market=='NIKKEI225')&(mr.Architecture=='LNN')].reset_index(drop=True);assert g.Loss.eq('MILD_WCE').all()
hmm=pd.read_csv(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv');hmm.Date=pd.to_datetime(hmm.Date);h=hmm[hmm.Market=='NIKKEI225'].set_index('Date').loc[pd.to_datetime(g.Date),'Regime'].eq('High').to_numpy();assert h.sum()==117
y=g.Y_true.to_numpy(int);votes=g[[f'Seed_{s}_prediction' for s in [42,52,62,72,82]]].to_numpy().T;baseline=g.Persistence_prediction.to_numpy(int)
bs=pd.read_csv(OUT/'nikkei_high_bootstrap_samples.csv');ci=pd.read_csv(OUT/'nikkei_high_block_bootstrap.csv');rng=np.random.default_rng(20261028);bad=0;verified=0
for iteration in range(10000):
 starts=rng.integers(0,len(y)-20+1,size=int(np.ceil(len(y)/20)));ix=(starts[:,None]+np.arange(20)).ravel()[:len(y)];ix=ix[h[ix]]
 if len(ix)==0 or len(np.unique(y[ix]))<2:bad+=1;continue
 if verified<10:
  saved=bs[bs.Resample==iteration].iloc[0]
  for name,fn in [('Delta_BA',balanced_accuracy_score),('Delta_Macro_F1',lambda yy,p:f1_score(yy,p,labels=[0,1],average='macro',zero_division=0)),('Delta_Accuracy',accuracy_score)]:
   actual=np.mean([fn(y[ix],p[ix]) for p in votes])-fn(y[ix],baseline[ix]);assert np.isclose(actual,saved[name],atol=1e-12,rtol=0)
  verified+=1
assert len(bs)+bad==10000 and (ci.Invalid_resamples==bad).all() and (ci.Valid_resamples==len(bs)).all()
for r in ci.itertuples():np.testing.assert_allclose([r.CI_low,r.CI_high],bs[r.Metric].quantile([.025,.975]),atol=1e-12,rtol=0)
# Every permutation block must stay within a single consecutive High episode in original frozen calendar.
blocks=pd.read_csv(OUT/'nikkei_high_permutation_blocks.csv');raw=pd.read_csv(ROOT/'artifacts/nikkei225/market_input.csv',index_col=0,parse_dates=True);rawloc=raw.index.get_indexer(pd.to_datetime(g.Date));covered=[];scores=[]
pos=(y[h]==1).sum();neg=(y[h]==0).sum();weights=np.where(y==1,.5/pos,.5/neg)
for r in blocks.itertuples():
 ix=np.where((rawloc>=r.Raw_first_position)&(rawloc<=r.Raw_last_position))[0]
 assert len(ix)==r.N and r.N<=20 and h[ix].all() and (np.diff(rawloc[ix])==1).all()
 assert g.Date.iloc[ix[0]]==r.First_date and g.Date.iloc[ix[-1]]==r.Last_date
 covered.extend(ix.tolist());delta=np.mean(votes[:,ix]==y[ix],axis=0)-(baseline[ix]==y[ix]);scores.append((delta*weights[ix]).sum())
assert sorted(covered)==np.flatnonzero(h).tolist()
perm=pd.read_csv(OUT/'nikkei_high_block_permutation.csv').iloc[0];samples=pd.read_csv(OUT/'nikkei_high_permutation_samples.csv');assert len(samples)==10000
observed=np.mean([balanced_accuracy_score(y[h],p[h]) for p in votes])-balanced_accuracy_score(y[h],baseline[h]);assert np.isclose(observed,perm.Observed_delta_BA)
expected=(1+int((abs(samples.Delta_BA)>=abs(observed)-1e-12).sum()))/10001;assert np.isclose(expected,perm.Two_sided_p)
signs=np.random.default_rng(20261028).choice([-1,1],size=(10000,len(scores)));np.testing.assert_allclose(signs@np.array(scores),samples.Delta_BA,atol=1e-12,rtol=0)
# Exact enumeration is a diagnostic check only, never a replacement for the requested Monte Carlo p.
if len(scores)<=20:
 exact=np.asarray(list(itertools.product([-1,1],repeat=len(scores))))@np.array(scores);p_exact=float(np.mean(abs(exact)>=abs(observed)-1e-12))
 (OUT/'nikkei_high_permutation_exact_check.json').write_text(json.dumps({'status':'diagnostic_only','patterns':len(exact),'exact_block_sign_p':p_exact,'Monte_Carlo_primary_p_retained':float(perm.Two_sided_p),'not_effective_independent_sample_size':True},indent=2)+'\n')
required=['selected_primary_configs.csv','seed_level_primary_metrics.csv','validation_selected_statistical_tests.csv','architecture_friedman_tests.csv','majority_vote_mcnemar.csv','nonoverlap_metrics.csv','nonoverlap_comparison_full.csv','nonoverlap_mcnemar.csv','nikkei_high_primary_metrics.csv','nikkei_high_block_bootstrap.csv','nikkei_high_block_permutation.csv','results_report.md','methodology_notes.md','analysis_manifest.json']
assert all((OUT/name).is_file() for name in required)
manifest['status']='validated';manifest['script_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.py')};manifest['protocol_sha256']=hashlib.sha256((OUT/'analysis_protocol.json').read_bytes()).hexdigest();(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
check={'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'architecture_market_selections':15,'seed_runs':75,'no_training':True,'no_test_based_loss_selection':True,'validation_selection_matches_expected':True,'thresholds_unchanged':True,'HMM_refit':False,'prediction_and_regime_hashes_unchanged':True,'original_statistical_nonoverlap_HMM_economic_artifacts_unchanged':True,'full_test_predictions_and_labels_exact':True,'nonoverlap_phase':0,'nonoverlap_step':20,'phase_search':False,'Nikkei_High_loss':'MILD_WCE','Nikkei_High_N':117,'bootstrap_paired_and_jointly_aligned':True,'bootstrap_valid':len(bs),'bootstrap_invalid':bad,'permutation_blocks_cross_regime_interruptions':False,'permutation_episodes':int(perm.Episodes),'permutation_blocks':int(perm.Blocks),'independent_Friedman_Holm_binomial_and_bootstrap_checks':True,'effective_independent_sample_size_claimed':False}
(OUT/'completion_check.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check,indent=2))
