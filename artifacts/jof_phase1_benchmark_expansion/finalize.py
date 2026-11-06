"""Phase1 fixed comparisons/diagnostics only; no new model/threshold selection."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast,subprocess,sys
import numpy as np,pandas as pd,torch,joblib,nbformat
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,recall_score,precision_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];os.chdir(ROOT)
M={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'};NEW=['GRU','LogisticRegression','LightGBM'];ARCH=['LNN','LSTM','Transformer','GRU'];SEEDS=[42,52,62,72,82]
lock=json.loads((OUT/'protocol_lock.json').read_text());lockhash=hashlib.sha256((OUT/'protocol_lock.json').read_bytes()).hexdigest();run=json.loads((OUT/'run_manifest.json').read_text());selection_lock=json.loads((OUT/'selection_lock.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(x,name):pd.DataFrame(x).to_csv(OUT/name,index=False,float_format='%.17g')
def metric(y,p):return {'Accuracy':accuracy_score(y,p),'Balanced_Accuracy':balanced_accuracy_score(y,p) if len(np.unique(y))==2 else np.nan,'Macro_F1':f1_score(y,p,labels=[0,1],average='macro',zero_division=0),'Recall':recall_score(y,p,zero_division=0),'Precision':precision_score(y,p,zero_division=0),'F1':f1_score(y,p,zero_division=0),'Pred_Pos_Rate':float(np.mean(p)),'Actual_Up_Rate':float(np.mean(y))}
def extract(path,function,space):
 tree=ast.parse(Path(path).read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function);exec(compile(ast.Module(body=[node],type_ignores=[]),str(path)+'-function-only','exec'),space);return space[function]
pt=extract(ROOT/'artifacts/validation_selected_pt_tests/analyze.py','pt',{'np':np,'pd':pd,'stats':stats,'balanced_accuracy_score':balanced_accuracy_score,'f1_score':f1_score})
economic_metrics=extract(ROOT/'artifacts/cross_market_economic/analyze.py','metrics',{'np':np,'pd':pd})
selected=pd.read_csv(OUT/'selected_configs.csv',float_precision='round_trip');validation=pd.read_csv(OUT/'validation_selection_results.csv',float_precision='round_trip');new_results=pd.read_csv(OUT/'test_results_all_new_models.csv',float_precision='round_trip');thresholds=pd.read_csv(OUT/'frozen_thresholds.csv',float_precision='round_trip')
assert len(selected)==30 and len(new_results)==75 and len(validation)==125 and len(thresholds)==75
assert sha(OUT/'selected_configs.csv')==selection_lock['selection_sha256'] and sha(OUT/'frozen_thresholds.csv')==selection_lock['thresholds_sha256']
# Independently reconstruct validation threshold/loss decisions from saved validation probabilities.
base=nbformat.read(ROOT/'artifacts/sp500_rerun/SCI_v1_4_WALKFORWARD_SP500.ipynb',4);ns={}
for i in [1,3,13,14]:exec(compile(base.cells[i].source,f'validation-{i}','exec'),ns)
torch.set_num_threads(2)
for r in validation.itertuples():
 v=pd.read_csv(OUT/'all_predictions'/f'{r.Market}_{r.Model}_{r.Loss}_{r.Seed}.validation.csv',float_precision='round_trip');thr,_=ns['select_validation_threshold'](v.Y_true,v.Probability,ns['THRESHOLD_GRID']);assert thr==r.Threshold
 met=metric(v.Y_true.to_numpy(int),(v.Probability.to_numpy()>thr).astype(int));assert np.isclose(met['Balanced_Accuracy'],r.WF_Val_BA,atol=1e-12,rtol=0) and np.isclose(met['Macro_F1'],r.WF_Val_Macro_F1,atol=1e-12,rtol=0)
for market in M:
 v=validation[(validation.Market==market)&(validation.Model=='GRU')];a=v.groupby('Loss').agg(BA=('WF_Val_BA','mean'),MF=('WF_Val_Macro_F1','mean'),Dist=('Abs_threshold_distance','mean')).reset_index().sort_values(['BA','MF','Dist','Loss'],ascending=[False,False,True,True]);assert selected[(selected.Market==market)&(selected.Model=='GRU')].Loss.iloc[0]==a.Loss.iloc[0]
representatives=[];rules=[];ptrows=[];non=[];econ=[];econpaths=[];primary=[];freq=[];seedfreq=[];equivalence=[];seedmeans=[];determinism=[];alignment=[]
for market,folder in M.items():
 directory=ROOT/folder;raw=pd.read_csv(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');index=raw.index;close=raw.Close.to_numpy();pack=torch.load(OUT/'checkpoints'/f'{market}_input_tensors.pt',weights_only=False,map_location='cpu');assert pack['protocol_sha256']==lockhash
 test=pack['test'];dates=pd.DatetimeIndex(test[2]);y=test[1].numpy();locations=index.get_indexer(dates);assert (locations>=200).all() and (locations+20<len(raw)).all();assert np.array_equal((close[locations+20]>close[locations]).astype(int),y)
 source_results=pd.read_csv(directory/'seed_results.csv',float_precision='round_trip');pred={};meta={}
 for r in selected[selected.Market==market].itertuples():
  probs=[];votes=[];rows=[]
  for seed in SEEDS:
   if r.Model in NEW:
    p=pd.read_csv(OUT/'all_predictions'/f'{market}_{r.Model}_{r.Loss}_{seed}.test.csv',float_precision='round_trip');row=new_results[(new_results.Market==market)&(new_results.Model==r.Model)&(new_results.Seed==seed)].iloc[0]
    ck=torch.load(OUT/'checkpoints'/f'{market}_{r.Model}_{r.Loss}_{seed}_final.pt',weights_only=False,map_location='cpu');assert ck['protocol_sha256']==lockhash and ck['selection_lock_sha256']==sha(OUT/'selection_lock.json')
    if r.Model=='GRU':
     ns['set_seed'](seed)  # Same deterministic execution settings as the original training job.
     estimator=ns['build_model']('GRU',test[0].shape[-1]);estimator.load_state_dict(ck['state_dict']);estimator.eval()
     with torch.no_grad():replay=torch.softmax(estimator(test[0]),dim=1)[:,1].numpy()
    else:
     estimator=joblib.load(OUT/ck['estimator_file']);replay=estimator.predict_proba(test[0].numpy().reshape(len(y),-1))[:,1]
     if r.Model=='LogisticRegression':assert estimator.solver=='lbfgs' and estimator.C==1. and estimator.max_iter==5000 and estimator.class_weight is None
     else:assert estimator.n_estimators==300 and estimator.learning_rate==.03 and estimator.num_leaves==31
    np.testing.assert_allclose(replay,p.Probability,atol=1e-7 if r.Model=='GRU' else 1e-12,rtol=0)
   else:
    p=pd.read_csv(directory/'predictions'/f'{r.Model}_{r.Loss}_{seed}.csv',float_precision='round_trip');row=source_results[(source_results.Model==r.Model)&(source_results.Loss==r.Loss)&(source_results.Seed.astype(str)==str(seed))].iloc[0]
   assert np.array_equal(pd.to_datetime(p.Date),dates) and np.array_equal(p.Y_true,y);assert np.allclose(p.Threshold,row.Threshold,atol=1e-14,rtol=0)
   prob=p.Probability.to_numpy();vote=(prob>row.Threshold).astype(int);assert np.isfinite(prob).all()
   if 'Y_pred' in p:assert np.array_equal(vote,p.Y_pred)
   if r.Model in NEW:assert np.array_equal((replay>row.Threshold).astype(int),vote)
   met=metric(y,vote)
   for name in ['Accuracy','Balanced_Accuracy','Macro_F1']:assert np.isclose(met[name],row[name],atol=1e-12,rtol=0)
   probs.append(prob);votes.append(vote);rows.append(met);seedfreq.append({'Market':market,'Model':r.Model,'Loss':r.Loss,'Seed':seed,'Actual_Up_Rate':y.mean(),'Forecast_Up_Rate':vote.mean(),'Absolute_forecast_imbalance':abs(vote.mean()-.5),'Forecast_minus_actual_up_rate':vote.mean()-y.mean(),'Near_constant':bool(vote.mean()<.1 or vote.mean()>.9)})
  votes=np.array(votes);f=(votes.sum(axis=0)>=3).astype(int);unique_f=len({v.tobytes() for v in votes});unique_p=len({p.tobytes() for p in probs});aggregation='deterministic_consensus_equivalent_to_single_seed' if r.Model in ['LogisticRegression','LightGBM'] and unique_f==1 else 'majority_3_of_5'
  pred[r.Model]=f;met=metric(y,f);meta[r.Model]={'Loss':r.Loss,'Validation_BA':r.WF_Val_BA_mean,'Origin':r.Origin,'Aggregation':aggregation,'Supplemental':False,'Seed_mean_BA':np.mean([v['Balanced_Accuracy'] for v in rows]),'Seed_mean_Macro_F1':np.mean([v['Macro_F1'] for v in rows]),'Seed_mean_Accuracy':np.mean([v['Accuracy'] for v in rows])}
  representatives.append({'Market':market,'Model':r.Model,'Loss':r.Loss,'N':len(y),'Aggregation':aggregation,'Unique_seed_forecast_series':unique_f,'Unique_seed_probability_series':unique_p,**met});determinism.append({'Market':market,'Model':r.Model,'Identical_binary_forecasts_all_seeds':unique_f==1,'Identical_probabilities_all_seeds':unique_p==1,'Classification_seed_variation_absent':unique_f==1,'Five_run_records_retained':True})
  seedmeans.append({'Market':market,'Model':r.Model,'Loss':r.Loss,'Mean_BA':meta[r.Model]['Seed_mean_BA'],'Mean_Macro_F1':meta[r.Model]['Seed_mean_Macro_F1'],'Mean_Accuracy':meta[r.Model]['Seed_mean_Accuracy']})
  pd.DataFrame({'Date':dates,'Y_true':y,'Majority_prediction':f,**{f'Seed_{s}_prediction':votes[i] for i,s in enumerate(SEEDS)}}).to_csv(OUT/'all_predictions'/f'{market}_{r.Model}_representative.csv',index=False)
 persistence=(close[locations]>close[locations-20]).astype(int);old=pd.read_csv(ROOT/f'artifacts/cross_market_statistics/{market}_majority_predictions.csv');assert np.array_equal(old.Persistence_prediction,persistence) and np.array_equal(pd.to_datetime(old.Date),dates)
 momentum20=(raw.Close>raw.Close.shift(20)).loc[dates].astype(int).to_numpy();assert np.array_equal(momentum20,persistence)
 equivalence.append({'Market':market,'Momentum20_definition':'I(P_t>P_t-20)','Persistence_definition':'I(P_t>P_t-20)','equivalent_to_existing_persistence':True,'duplicate_baseline_created':False,'additional_prespecified_momentum':'Momentum60'})
 ma=raw.Close.rolling(200,min_periods=200).mean();allrules={'Rule_200DMA':(raw.Close>ma).astype(int),'Rule_200DMA_Lag1':(raw.Close.shift(1)>ma.shift(1)).astype(int),'Momentum60':(raw.Close>raw.Close.shift(60)).astype(int)}
 for name,series in allrules.items():
  assert ma.loc[dates].notna().all();f=series.loc[dates].to_numpy();pred[name]=f;vp=[];vy=[]
  for fold in pack['folds']:vp.extend(series.loc[fold['val'][2]].to_numpy());vy.extend(fold['val'][1].numpy())
  val=metric(np.array(vy),np.array(vp));met=metric(y,f);rules.append({'Market':market,'Model':name,'N':len(y),'Supplemental':name=='Rule_200DMA_Lag1','Validation_BA':val['Balanced_Accuracy'],'Uses_P_t':name!='Rule_200DMA_Lag1',**met});meta[name]={'Loss':'fixed_rule','Validation_BA':val['Balanced_Accuracy'],'Origin':'Prespecified_rule','Aggregation':'deterministic_rule','Supplemental':name=='Rule_200DMA_Lag1'}
  pd.DataFrame({'Date':dates,'Y_true':y,'Y_pred':f,'Model':name}).to_csv(OUT/'all_predictions'/f'{market}_{name}.rule.csv',index=False)
 for name,f in [('Persistence',persistence),('Always-Up',np.ones(len(y),int)),('Always-Down',np.zeros(len(y),int))]:
  pred[name]=f;vp=[];vy=[]
  for fold in pack['folds']:
   vd=fold['val'][2];vloc=index.get_indexer(vd);vp.extend((close[vloc]>close[vloc-20]).astype(int) if name=='Persistence' else np.full(len(vd),int(name=='Always-Up')));vy.extend(fold['val'][1].numpy())
  meta[name]={'Loss':'baseline','Validation_BA':metric(np.array(vy),np.array(vp))['Balanced_Accuracy'],'Origin':'Existing_benchmark','Aggregation':'deterministic','Supplemental':False}
 # Economics for all fixed operational representatives (including optional lagged-rule diagnostic).
 start=locations[0]+1;end=np.where(index<='2025-12-31')[0][-1];edates=index[start:end+1];rt=np.r_[0.,close[1:]/close[:-1]-1];economics={}
 for name,forecast in {**pred,'Buy_Hold':np.ones(len(y),int),'Always_Cash':np.zeros(len(y),int)}.items():
  pos=np.zeros(len(index))
  if name=='Buy_Hold':pos[start:end+1]=1
  elif name!='Always_Cash':
   for location,signal in zip(locations,forecast):pos[location+1:end+1]=signal
  pos[end]=0;previous=np.r_[0.,pos[:-1]];changes=pos-previous;exposure=previous[start:end+1];gross=exposure*rt[start:end+1];turn=changes[start:end+1]
  # Independent causal lookup: a return at raw row j can use only signals at raw rows<=j-2.
  earned_rows=np.arange(start,end+1);last=np.searchsorted(locations,earned_rows-2,side='right')-1;expected=np.where(last>=0,forecast[np.maximum(last,0)],0)
  np.testing.assert_allclose(exposure,expected,atol=0,rtol=0)
  for j,date in enumerate(edates):alignment.append({'Market':market,'Model':name,'Return_date':str(date.date()),'Signal_date':str(dates[last[j]].date()) if last[j]>=0 else '', 'Position_effective_date':str(index[locations[last[j]]+1].date()) if last[j]>=0 else '', 'Position_previous_close':exposure[j],'No_same_close_execution':bool(last[j]<0 or dates[last[j]]<index[locations[last[j]]+1]<date)})
  for bps in [0,10,25,50]:
   costs=abs(turn)*bps/2/10000;net=gross-costs;assert np.isfinite(net).all() and (net>-1).all();met=economic_metrics(net,gross,exposure,turn,edates,costs);econ.append({'Market':market,'Model':name,'Mode':'Daily','Round_trip_bps':bps,**met});economics[(name,bps)]=met
   for date,p,gr,c,n,w in zip(edates,exposure,gross,costs,net,np.cumprod(1+net)):econpaths.append({'Market':market,'Model':name,'Date':str(date.date()),'Round_trip_bps':bps,'Position_previous_close':p,'Gross_return':gr,'Cost_debit':c,'Net_return':n,'Wealth':w})
 for name,f in pred.items():
  met=metric(y,f);ptest=pt(y,f);ix=np.arange(0,len(y),20);assert (np.diff(locations[ix])>=20).all();nmet=metric(y[ix],f[ix]);npt=pt(y[ix],f[ix]);non.append({'Market':market,'Model':name,'Loss':meta[name]['Loss'],'Supplemental':meta[name]['Supplemental'],'N':len(ix),'Phase':0,'Step':20,**nmet,'PT_statistic':npt['PT_statistic'],'PT_raw_p':npt['PT_two_sided_p'],'PT_positive_p':npt['PT_positive_one_sided_p'],'PT_status':npt['PT_status'],'Overlap_caveat':'Reduced overlap does not establish statistical independence.'})
  ptrows.append({'Market':market,'Model':name,'Selected_Loss':meta[name]['Loss'],'Supplemental':meta[name]['Supplemental'],**ptest,'Overlap_caveat':'Conventional PT does not fully account for H20 overlapping labels; no final Phase2 multiplicity correction is defined.'})
  row={'Market':market,'Model':name,'Selected_Loss':meta[name]['Loss'],'Origin':meta[name]['Origin'],'Validation_BA':meta[name]['Validation_BA'],'Test_BA':met['Balanced_Accuracy'],'Test_Accuracy':met['Accuracy'],'Macro_F1':met['Macro_F1'],'Forecast_Up_Rate':met['Pred_Pos_Rate'],'Actual_Up_Rate':met['Actual_Up_Rate'],'Delta_BA_vs_Persistence':met['Balanced_Accuracy']-metric(y,persistence)['Balanced_Accuracy'],'Delta_BA_vs_0_5':met['Balanced_Accuracy']-.5,'PT_statistic':ptest['PT_statistic'],'PT_raw_p':ptest['PT_two_sided_p'],'PT_status':ptest['PT_status'],'Nonoverlap_BA':nmet['Balanced_Accuracy'],'Economic_Exposure':economics[(name,10)]['Exposure'],'Economic_CAGR_10bps':economics[(name,10)]['CAGR'],'Supplemental':meta[name]['Supplemental'],'Prediction_aggregation':meta[name]['Aggregation'],'Mean_seed_Test_BA':meta[name].get('Seed_mean_BA',np.nan)}
  primary.append(row);freq.append({'Market':market,'Model':name,'Forecast_Up_Rate':met['Pred_Pos_Rate'],'Actual_Up_Rate':met['Actual_Up_Rate'],'Absolute_imbalance_from_0_5':abs(met['Pred_Pos_Rate']-.5),'Forecast_minus_actual_up_rate':met['Pred_Pos_Rate']-met['Actual_Up_Rate'],'Near_constant_forecast':bool(met['Pred_Pos_Rate']<.1 or met['Pred_Pos_Rate']>.9),'Diagnostic_only_not_exclusion':True})
save(alignment,'diagnostics/economic_alignment_audit.csv');assert all(r['No_same_close_execution'] for r in alignment)
save(representatives,'majority_vote_results.csv');save(rules,'rule_baseline_results.csv');save(equivalence,'diagnostics/momentum_equivalence_audit.csv');save(ptrows,'pt_results.csv');save(non,'nonoverlap_results.csv');save(econ,'transaction_cost_results.csv');pd.DataFrame(econpaths).to_csv(OUT/'diagnostics/economic_paths.csv.gz',index=False,float_format='%.17g',compression='gzip');save(freq,'diagnostics/forecast_frequency.csv');save(seedfreq,'diagnostics/forecast_frequency_seed_level.csv');save(determinism,'diagnostics/seed_determinism.csv');save(seedmeans,'diagnostics/learned_seed_means.csv')
pf=pd.DataFrame(primary);save(pf[~pf.Supplemental],'benchmark_comparison_table.csv');save(pf[pf.Supplemental],'diagnostics/supplementary_rule_comparison.csv')
rank=pf[~pf.Supplemental].copy()
for score in ['Test_BA','Macro_F1','Test_Accuracy']:rank['Rank_'+score]=rank.groupby('Market')[score].rank(ascending=False,method='average')
save(rank[['Market','Model','Rank_Test_BA','Rank_Macro_F1','Rank_Test_Accuracy']],'descriptive_market_rankings.csv');rr=rank.groupby('Model')[['Rank_Test_BA','Rank_Macro_F1','Rank_Test_Accuracy']].agg(['mean','median']);rr.columns=['_'.join(c) for c in rr.columns];rr.reset_index().to_csv(OUT/'cross_market_average_ranks.csv',index=False)
sm=pd.DataFrame(seedmeans);friedman=[]
for score in ['Mean_BA','Mean_Macro_F1']:
 table=sm[sm.Model.isin(ARCH)].pivot(index='Market',columns='Model',values=score).loc[list(M),ARCH];stat,p=stats.friedmanchisquare(*table.to_numpy().T);friedman.append({'Metric':score,'Market_blocks':5,'Architectures':4,'Architecture_family':'LNN,LSTM,Transformer,GRU; validation-selected losses; five-seed means','Friedman_statistic':stat,'raw_p':p,'Kendall_W':stat/(5*3),'Descriptive_phase1_not_final_family':True})
save(friedman,'neural_architecture_friedman.csv')
save([{'Scenario':'Current frozen manuscript','Architecture_count':3,'Market_count':5,'Hypotheses':15,'Membership':'LNN,LSTM,Transformer','Final_family_replaced':False,'Status':'Original Holm15 retained unchanged'}, {'Scenario':'Hypothetical after Phase1 GRU only','Architecture_count':4,'Market_count':5,'Hypotheses':20,'Membership':'LNN,LSTM,Transformer,GRU','Final_family_replaced':False,'Status':'Diagnostic size only; no new Holm significance claims'}, {'Scenario':'After Phase2','Architecture_count':np.nan,'Market_count':5,'Hypotheses':np.nan,'Membership':'Phase2 architecture list not supplied; future count=20+5*k additional architectures','Final_family_replaced':False,'Status':'Must be frozen after Phase2; no invented additions'}],'diagnostics/multiplicity_family_diagnostic.csv')
# Independent economics check: preserve old frozen benchmark paths and causal execution.
paths=pd.DataFrame(econpaths);old=pd.read_csv(ROOT/'artifacts/cross_market_economic/daily_strategy_returns.csv',float_precision='round_trip');map_names={'Persistence':'Persistence','Buy_Hold':'Buy_Hold','Always_Cash':'Always_Cash'}
for model,strategy in map_names.items():
 a=paths[paths.Model==model].set_index(['Market','Round_trip_bps','Date']).sort_index();b=old[(old.Mode=='Daily')&(old.Strategy==strategy)].set_index(['Market','Round_trip_bps','Date']).sort_index();assert a.index.equals(b.index)
 for col in ['Position_previous_close','Cost_debit','Net_return','Wealth']:np.testing.assert_allclose(a[col],b[col],atol=1e-12,rtol=0)
assert len(list((OUT/'checkpoints').glob('*_fold*.pt')))==375
assert len(list((OUT/'checkpoints').glob('*_final.pt')))==75
assert len(list((OUT/'all_predictions').glob('*.validation.csv')))==125
assert len(list((OUT/'all_predictions').glob('*.test.csv')))==75
for name,digest in run['source_sha256'].items():
 if name=='finalize.py':
  fix=json.loads((OUT/'diagnostics/determinism_fix.json').read_text());assert fix['original_sha256']==digest and fix['corrected_sha256']==sha(OUT/name)
 else:assert sha(OUT/name)==digest
for name,digest in run['protected_original_artifact_sha256'].items():assert sha(ROOT/name)==digest
for name,digest in run['input_sha256'].items():assert sha(ROOT/name)==digest
assert sha(ROOT/'artifacts/validation_selected_pt_tests/analyze.py')==run['source_existing_PT_sha256'];assert sha(ROOT/'artifacts/cross_market_economic/economic_protocol.json')==run['source_economic_protocol_sha256']
previous_lnn=pd.read_csv(ROOT/'artifacts/validation_selected_lnn_economic/daily_strategy_returns.csv',float_precision='round_trip')
a=paths[paths.Model=='LNN'].set_index(['Market','Round_trip_bps','Date']).sort_index();b=previous_lnn[(previous_lnn.Mode=='Daily')&(previous_lnn.Strategy=='Validation_LNN')].set_index(['Market','Round_trip_bps','Date']).sort_index();assert a.index.equals(b.index);np.testing.assert_allclose(a.Net_return,b.Net_return,atol=1e-12,rtol=0)
# Raw PT must satisfy the independently checked Pearson identity whenever margins vary.
for market in M:
 for row in [r for r in ptrows if r['Market']==market and r['PT_status']=='defined']:
  n=row['N'];py=row['Actual_Up_Rate'];pfor=row['Forecast_Up_Rate'];variance=4*py*(1-py)*pfor*(1-pfor)*(n-1)/(n*n);assert np.isclose(variance,row['Var_hat'],atol=1e-14,rtol=1e-10)
subprocess.run([sys.executable,str(OUT/'report.py')],check=True)
for name in ['methodology_notes.md','results_report.md','figures/phase1_predictive_and_frequency.png']:assert (OUT/name).is_file()
manifest={'status':'validated','completed_at_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':run['source_sha256'],'input_sha256':run['input_sha256'],'protected_original_artifact_sha256':run['protected_original_artifact_sha256'],'selection_lock':selection_lock,'new_validation_fit_jobs':375,'new_final_fit_jobs':75,'original_Holm15_redefined':False,'phase2_final_family_frozen':False,'PT_definition_source':'unchanged existing PT function, AST-extracted without executing old analysis','economic_definition_source':'unchanged existing metrics function and accounting protocol','test_driven_tuning':False}
(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
check={'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'existing_artifacts_unchanged':True,'no_test_driven_hyperparameter_selection':True,'validation_only_threshold_selection_reproduced':True,'GRU_structure_and_training_matched_LSTM':True,'original_loss_formulas_reused':True,'Logistic_and_LightGBM_frozen_before_test':True,'rules_frozen_before_test':True,'H':20,'W':20,'same_expanding_splits':True,'HMM_refit':False,'phase_search':False,'test_based_loss_selection':False,'all_validation_candidate_seed_runs':125,'all_final_seed_runs':75,'validation_predictions_saved':125,'test_predictions_saved':75,'new_final_checkpoint_inference_verified':True,'all_negative_and_null_results_retained':True,'old_benchmark_economic_paths_reproduced':True,'Momentum20_equals_Persistence':True,'Momentum60_added_without_duplicate_Momentum20':True,'no_final_Holm_family_redefinition':True}
(OUT/'completion_check.json').write_text(json.dumps(check,indent=2)+'\n')
print(pf[~pf.Supplemental][['Market','Model','Selected_Loss','Test_BA','Forecast_Up_Rate','Economic_CAGR_10bps']].to_string(index=False))
