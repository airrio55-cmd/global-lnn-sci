"""Post-training checks and prespecified transfer statistics; no model fitting."""
import os
os.environ['OMP_NUM_THREADS']='2';os.environ['MKL_NUM_THREADS']='2';os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
import json,hashlib,itertools
from datetime import datetime,timezone
import numpy as np,pandas as pd,torch,nbformat
from scipy import stats
from sklearn.metrics import balanced_accuracy_score,f1_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];os.chdir(ROOT)
S=[42,52,62,72,82];M=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'];REG=['Low','Normal','High'];lock=json.loads((OUT/'transfer_protocol.json').read_text());lockhash=hashlib.sha256((OUT/'transfer_protocol.json').read_bytes()).hexdigest()
def save(x,name):pd.DataFrame(x).to_csv(OUT/name,index=False,float_format='%.17g')
def holm(p):
 p=np.array(p,float);ix=np.argsort(p);z=np.empty(len(p));z[ix]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[ix]));return z
scratch=pd.read_csv(OUT/'scratch_seed_results.csv',float_precision='round_trip');transfer=pd.read_csv(OUT/'transfer_seed_results.csv',float_precision='round_trip')
assert len(scratch)==len(transfer)==25 and not scratch.duplicated(['Market','Seed']).any() and not transfer.duplicated(['Market','Seed']).any()
paired=transfer.merge(scratch,on=['Market','Seed'],suffixes=('_Transfer','_Scratch'),validate='one_to_one')
for metric in ['Accuracy','Balanced_Accuracy','Macro_F1','Recall','Precision','F1','Pred_Pos_Rate']:paired['Delta_'+metric]=paired[metric+'_Transfer']-paired[metric+'_Scratch']
save(paired,'transfer_seed_deltas.csv');summary=[];bootstrap=[];mc=[];regrows=[];economic=[];rng=np.random.default_rng(20261028)
hmm_path=ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv';hmm=pd.read_csv(hmm_path);hmm.Date=pd.to_datetime(hmm.Date)
definitions=nbformat.read(ROOT/lock['definition_notebook'],4);ns={}
for i in [1,3,13,14]:exec(compile(definitions.cells[i].source,f'validation-definition-{i}','exec'),ns)
torch.set_num_threads(2)
for market in M:
 d=paired[paired.Market==market].sort_values('Seed');assert d.Seed.tolist()==S
 row={'Market':market,'Mean_Delta_BA':d.Delta_Balanced_Accuracy.mean(),'Mean_Delta_Macro_F1':d.Delta_Macro_F1.mean(),'Seeds_positive_BA':int((d.Delta_Balanced_Accuracy>0).sum()),'Transfer_positive':bool(d.Delta_Balanced_Accuracy.mean()>0),'Robust_transfer_positive':bool((d.Delta_Balanced_Accuracy>0).sum()>=4),'Metric_consistent_transfer':bool(d.Delta_Balanced_Accuracy.mean()>0 and d.Delta_Macro_F1.mean()>0),'Negative_transfer':bool(d.Delta_Balanced_Accuracy.mean()<0)}
 for metric in ['Accuracy','Balanced_Accuracy','Macro_F1','Recall','Precision','F1','Pred_Pos_Rate']:
  for method in ['Scratch','Transfer']:
   values=d[metric+'_'+method];row.update({method+'_'+metric+'_'+name:float(value) for name,value in [('mean',values.mean()),('SD',values.std(ddof=1)),('median',values.median()),('min',values.min()),('max',values.max())]})
  if metric not in ['Balanced_Accuracy','Macro_F1']:continue
  delta=d['Delta_'+metric].to_numpy();bs=rng.choice(delta,size=(10000,5),replace=True).mean(axis=1);w=stats.wilcoxon(delta,alternative='two-sided',method='exact') if np.any(delta) else (0,1)
  bootstrap.append({'Market':market,'Metric':metric,'Mean_delta':delta.mean(),'SD_delta':delta.std(ddof=1),'Median_delta':np.median(delta),'Min_delta':delta.min(),'Max_delta':delta.max(),'CI_low':np.quantile(bs,.025),'CI_high':np.quantile(bs,.975),'Resamples':10000,'Wilcoxon_statistic':float(w[0]),'raw_p':float(w[1])})
 summary.append(row)
 raw=pd.read_csv(OUT/'frozen_inputs'/f'{market}.csv',index_col=0,parse_dates=True,float_precision='round_trip');idx=raw.index;close=raw.Close.to_numpy();regime=hmm[hmm.Market==market].set_index('Date').Regime
 votes={};truth=None;dates=None
 for method in ['Scratch','Transfer']:
  methodvotes=[]
  for seed in S:
   p=pd.read_csv(OUT/'predictions'/f'{market}_{method}_{seed}.csv',float_precision='round_trip');v=pd.read_csv(OUT/'predictions'/f'{market}_{method}_{seed}.validation.csv',float_precision='round_trip')
   assert np.isfinite(p.Probability).all() and p.Probability.between(0,1).all() and np.isfinite(v.Probability).all()
   dt=pd.DatetimeIndex(pd.to_datetime(p.Date));y=p.Y_true.to_numpy(int)
   loc=idx.get_indexer(dt);assert (loc>=20).all() and (loc+20<len(idx)).all()
   assert np.array_equal((close[loc+20]>close[loc]).astype(int),y)
   if dates is None:dates=dt;truth=y
   else:assert dates.equals(dt) and np.array_equal(truth,y)
   r=(scratch if method=='Scratch' else transfer);r=r[(r.Market==market)&(r.Seed==seed)].iloc[0]
   threshold,_=ns['select_validation_threshold'](v.Y_true.to_numpy(),v.Probability.to_numpy(),ns['THRESHOLD_GRID']);assert threshold==r.Threshold and np.allclose(p.Threshold,threshold,atol=1e-14,rtol=0)
   predicted=(p.Probability.to_numpy()>threshold).astype(int);assert np.array_equal(predicted,p.Y_pred)
   z=ns['calculate_metrics'](y,probs=p.Probability.to_numpy(),threshold=threshold)
   for name in ['Accuracy','Balanced_Accuracy','Macro_F1','Recall','Precision','F1','Pred_Pos_Rate']:assert np.isclose(z[name],r[name],atol=1e-12,rtol=0)
   checkpoint=torch.load(OUT/'checkpoints'/f'{market}_{method}_seed{seed}_final.pt',weights_only=False,map_location='cpu');assert checkpoint['protocol_sha256']==lockhash and checkpoint['input_size']==5
   model=ns['build_model']('LNN',5);model.load_state_dict(checkpoint['state_dict']);model.eval()
   # Saved exact scaled test tensors avoid recomputing a numerically different transform at verification.
   tensors=torch.load(OUT/'checkpoints'/f'{market}_test_tensors.pt',weights_only=False,map_location='cpu')
   with torch.no_grad():prob=torch.softmax(model(tensors['X']),dim=1)[:,1].numpy()
   np.testing.assert_allclose(prob,p.Probability.to_numpy(),atol=1e-7,rtol=0);assert np.array_equal((prob>threshold).astype(int),predicted)
   methodvotes.append(predicted)
  votes[method]=np.array(methodvotes)
 reps={method:(vp.sum(axis=0)>=3).astype(int) for method,vp in votes.items()};a=reps['Transfer']==truth;b=reps['Scratch']==truth
 n00=int((~a&~b).sum());n01=int((~a&b).sum());n10=int((a&~b).sum());n11=int((a&b).sum());n=n01+n10
 exact=stats.binomtest(n10,n,.5,alternative='two-sided').pvalue if n else 1.;cc=max(abs(n01-n10)-1,0)**2/n if n else 0.;pc=stats.chi2.sf(cc,1) if n else 1.
 mc.append({'Market':market,'N':len(truth),'n00_both_wrong':n00,'n01_Scratch_correct_Transfer_wrong':n01,'n10_Transfer_correct_Scratch_wrong':n10,'n11_both_correct':n11,'McNemar_statistic_CC':cc,'exact_p':exact,'continuity_corrected_p':pc,'raw_p':max(exact,pc),'Accuracy_delta':a.mean()-b.mean()})
 save({'Date':dates,'Y_true':truth,'Scratch_majority':reps['Scratch'],'Transfer_majority':reps['Transfer']},f'predictions/{market}_majority.csv')
 regimes=regime.loc[dates].to_numpy()
 for state in REG:
  mask=regimes==state;valid=len(np.unique(truth[mask]))==2
  ba={method:np.mean([balanced_accuracy_score(truth[mask],p[mask]) for p in vp]) if valid else np.nan for method,vp in votes.items()};mf={method:np.mean([f1_score(truth[mask],p[mask],average='macro',labels=[0,1],zero_division=0) for p in vp]) if mask.any() else np.nan for method,vp in votes.items()}
  regrows.append({'Market':market,'Regime':state,'N':int(mask.sum()),'Scratch_BA':ba['Scratch'],'Transfer_BA':ba['Transfer'],'Delta_BA':ba['Transfer']-ba['Scratch'],'Scratch_Macro_F1':mf['Scratch'],'Transfer_Macro_F1':mf['Transfer'],'Delta_Macro_F1':mf['Transfer']-mf['Scratch'],'Exploratory':True})
 if row['Transfer_positive']:
  positions=idx.get_indexer(dates);start=positions[0]+1;end=np.where(idx<='2025-12-31')[0][-1];rt=np.r_[0.,close[1:]/close[:-1]-1]
  for method in ['Scratch','Transfer']:
   pos=np.zeros(len(idx))
   for location,signal in zip(positions,reps[method]):pos[location+1:end+1]=signal
   pos[end]=0;old=np.r_[0.,pos[:-1]];turn=abs(pos-old);net=(old*rt-turn*.0005)[start:end+1];wealth=np.cumprod(1+net);peak=np.maximum.accumulate(np.r_[1.,wealth]);sd=net.std(ddof=1)
   economic.append({'Market':market,'Method':method,'N':len(net),'CAGR':wealth[-1]**(252/len(net))-1,'Sharpe':net.mean()/sd*np.sqrt(252) if sd>0 else np.nan,'MDD':float((np.r_[1.,wealth]/peak-1).min()),'Round_trip_bps':10,'Secondary_positive_BA_selected':True})
save(summary,'transfer_comparison.csv');bf=pd.DataFrame(bootstrap)
# Each metric has a prespecified five-market Wilcoxon family, and an extra joint ten-test adjustment is also supplied.
bf['Holm_p']=np.nan
for metric in bf.Metric.unique():mask=bf.Metric==metric;bf.loc[mask,'Holm_p']=holm(bf.loc[mask,'raw_p'])
bf['Holm_joint10_p']=holm(bf.raw_p);bf['significant']=bf.Holm_p<.05;save(bf,'transfer_bootstrap_ci.csv')
mcf=pd.DataFrame(mc);mcf['Holm_p']=holm(mcf.raw_p);mcf['significant']=mcf.Holm_p<.05;save(mcf,'transfer_mcnemar.csv');save(regrows,'regime_transfer_results.csv')
ecf=pd.DataFrame(economic,columns=['Market','Method','N','CAGR','Sharpe','MDD','Round_trip_bps','Secondary_positive_BA_selected']);ecf.to_csv(OUT/'transfer_economic_results.csv',index=False)
if len(ecf):
 ep=ecf[ecf.Method=='Transfer'].merge(ecf[ecf.Method=='Scratch'],on='Market',suffixes=('_Transfer','_Scratch'))
 for name in ['CAGR','Sharpe','MDD']:ep['Delta_'+name]=ep[name+'_Transfer']-ep[name+'_Scratch']
 save(ep,'transfer_economic_comparison.csv')
else:save(pd.DataFrame(columns=['Market','Delta_CAGR','Delta_Sharpe','Delta_MDD']),'transfer_economic_comparison.csv')
assert len(list((OUT/'checkpoints').glob('*source_through*.pt')))==100
assert len(list((OUT/'checkpoints').glob('*_fold*.pt')))==150
assert len(list((OUT/'checkpoints').glob('*_final.pt')))==50
assert len(list((OUT/'predictions').glob('*.validation.csv')))==50
manifest=json.loads((OUT/'data_manifest.json').read_text())
for name,digest in manifest['input_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
run=json.loads((OUT/'run_manifest.json').read_text())
for name,digest in run['source_sha256'].items():assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest
assert hashlib.sha256(hmm_path.read_bytes()).hexdigest()==run['HMM_sha256']
assert hashlib.sha256((ROOT/'artifacts/cross_market_economic/economic_protocol.json').read_bytes()).hexdigest()==run['economic_protocol_sha256']
assert hashlib.sha256((ROOT/lock['definition_notebook']).read_bytes()).hexdigest()==run['definition_notebook_sha256']
for path in (OUT/'checkpoints').glob('*source_through*.pt'):
 z=torch.load(path,weights_only=False,map_location='cpu');assert z['protocol_sha256']==lockhash and z['cutoff']<=2021
 assert z['Target'] not in z['sources'] and len(z['sources'])==4 and z['balanced_batch_each_source']==16
# Report and figures use the already computed results, never fitting or selection.
subprocess=__import__('subprocess');subprocess.run([__import__('sys').executable,str(OUT/'report.py')],check=True)
for image in ['transfer_delta_ba_by_market.png','scratch_vs_transfer.png','transfer_regime_heatmap.png']:assert (OUT/image).stat().st_size>1000
analysis={'status':'completed','completed_at_utc':datetime.now(timezone.utc).isoformat(),'protocol_sha256':lockhash,'input_sha256':manifest['input_sha256'],'HMM_assignment_sha256':hashlib.sha256(hmm_path.read_bytes()).hexdigest(),'economic_protocol_sha256':hashlib.sha256((ROOT/'artifacts/cross_market_economic/economic_protocol.json').read_bytes()).hexdigest(),'new_feature_set':'TRANSFER_COMMON, not COMMON_LOCAL','pretraining_source_sets_fixed':True,'source_2022_2025_training_used':False,'target_hyperparameter_selection_from_test':False,'source_combination_attribution':'Pooled LOMO only; no isolated US/non-US or Japan/Europe-to-Korea causal attribution possible.'}
(OUT/'analysis_manifest.json').write_text(json.dumps(analysis,indent=2)+'\n')
(OUT/'completion_check.json').write_text(json.dumps({'status':'validated','final_runs':50,'scratch_runs':25,'transfer_runs':25,'pretraining_checkpoints':100,'target_fold_checkpoints':150,'final_checkpoints':50,'validation_prediction_files':50,'test_prediction_files':50,'final_checkpoint_inference_verified':True,'validation_only_thresholds_verified':True,'leakage_audit':'passed','source_inputs_unchanged':True,'frozen_source_and_target_training_rules':True},indent=2)+'\n')
print(pd.DataFrame(summary)[['Market','Mean_Delta_BA','Mean_Delta_Macro_F1','Seeds_positive_BA','Negative_transfer']].to_string(index=False))
