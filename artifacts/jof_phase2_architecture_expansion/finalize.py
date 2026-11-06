"""Locked Phase2 diagnostics; never select on test or execute final Holm."""
import os
for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[key]='2'
from pathlib import Path
import json,hashlib,ast
import numpy as np,pandas as pd,torch,nbformat
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,recall_score,precision_score
from architectures import install,audit
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];P1=ROOT/'artifacts/jof_phase1_benchmark_expansion';os.chdir(ROOT)
M={'SP500':'sp500_rerun','NASDAQ100':'nasdaq100','NIKKEI225':'nikkei225','EUROSTOXX50':'eurostoxx50','KOSPI200':'kospi200'};NEW=['CfC','PE-Transformer'];ARCH=['LNN','CfC','LSTM','GRU','Transformer','PE-Transformer'];LEARNED=ARCH+['LogisticRegression','LightGBM'];SEEDS=[42,52,62,72,82]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(name,x):(OUT/name).write_text(json.dumps(x,indent=2)+'\n')
def save(name,x):pd.DataFrame(x).to_csv(OUT/name,index=False,float_format='%.17g')
def metric(y,p):return {'Accuracy':accuracy_score(y,p),'Balanced_Accuracy':balanced_accuracy_score(y,p) if len(np.unique(y))==2 else np.nan,'Macro_F1':f1_score(y,p,labels=[0,1],average='macro',zero_division=0),'Recall':recall_score(y,p,zero_division=0),'Precision':precision_score(y,p,zero_division=0),'F1':f1_score(y,p,zero_division=0),'Pred_Pos_Rate':float(np.mean(p)),'Actual_Up_Rate':float(np.mean(y))}
def extract(path,name,ns):
 node=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name==name);exec(compile(ast.Module(body=[node],type_ignores=[]),str(path), 'exec'),ns);return ns[name]
pt=extract(ROOT/'artifacts/validation_selected_pt_tests/analyze.py','pt',{'np':np,'pd':pd,'stats':stats,'balanced_accuracy_score':balanced_accuracy_score,'f1_score':f1_score})
economic=extract(ROOT/'artifacts/cross_market_economic/analyze.py','metrics',{'np':np,'pd':pd})
lock=json.loads((OUT/'protocol_lock.json').read_text());run=json.loads((OUT/'run_manifest.json').read_text());selection=json.loads((OUT/'selection_lock.json').read_text())
assert sha(OUT/'selected_configs.csv')==selection['selection_sha256'] and sha(OUT/'frozen_thresholds.csv')==selection['thresholds_sha256']
selected=pd.read_csv(OUT/'selected_configs.csv',float_precision='round_trip');validation=pd.read_csv(OUT/'validation_selection_results.csv',float_precision='round_trip');testresults=pd.read_csv(OUT/'test_results_phase2.csv',float_precision='round_trip')
assert len(selected)==40 and len(validation)==150 and len(testresults)==50
ns={};notebook=nbformat.read(ROOT/'artifacts/sp500_rerun'/lock['notebooks']['SP500'],4)
for i in [1,3,13,14]:exec(compile(notebook.cells[i].source,f'original-{i}','exec'),ns)
install(ns);torch.set_num_threads(2)
for r in validation.itertuples():
 v=pd.read_csv(OUT/'all_predictions'/f'{r.Market}_{r.Model}_{r.Loss}_{r.Seed}.validation.csv',float_precision='round_trip');thr,_=ns['select_validation_threshold'](v.Y_true,v.Probability,ns['THRESHOLD_GRID']);assert thr==r.Threshold
 assert np.isclose(metric(v.Y_true,(v.Probability>thr).astype(int))['Balanced_Accuracy'],r.WF_Val_BA,atol=1e-12,rtol=0)
for (market,model),g in validation.groupby(['Market','Model']):
 a=g.groupby('Loss').agg(BA=('WF_Val_BA','mean'),MF=('WF_Val_Macro_F1','mean'),Dist=('Abs_threshold_distance','mean')).reset_index().sort_values(['BA','MF','Dist','Loss'],ascending=[False,False,True,True]);assert selected[(selected.Market==market)&(selected.Model==model)].Loss.iloc[0]==a.Loss.iloc[0]
for model,name in [('CfC','cfc_validation_results.csv'),('PE-Transformer','pe_transformer_validation_results.csv')]:save(name,validation[validation.Model==model])
majority=[];frequency=[];pts=[];non=[];econ=[];paths=[];replays=[];comparison=[]
for market,folder in M.items():
 pack=torch.load(OUT/'checkpoints'/f'{market}_input_tensors.pt',weights_only=False,map_location='cpu');assert pack['protocol_sha256']==sha(OUT/'protocol_lock.json');X,y,dates=pack['test'][:3];y=y.numpy();audit(ns,X[:64])
 raw=pd.read_csv(ROOT/'artifacts'/folder/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');index=raw.index;close=raw.Close.to_numpy();loc=index.get_indexer(dates);assert (loc>=0).all()
 for r in selected[(selected.Market==market)&selected.Model.isin(NEW)].itertuples():
  votes=[];seedmetrics=[]
  for seed in SEEDS:
   f=OUT/'all_predictions'/f'{market}_{r.Model}_{r.Loss}_{seed}.test.csv';p=pd.read_csv(f,float_precision='round_trip');assert np.array_equal(pd.to_datetime(p.Date),dates) and np.array_equal(p.Y_true,y)
   ck=torch.load(OUT/'checkpoints'/f'{market}_{r.Model}_{r.Loss}_{seed}_final.pt',weights_only=False,map_location='cpu');assert ck['selection_lock_sha256']==sha(OUT/'selection_lock.json') and ck['protocol_sha256']==sha(OUT/'protocol_lock.json')
   ns['set_seed'](seed);model=ns['build_model'](r.Model,X.shape[-1]);model.load_state_dict(ck['state_dict']);model.eval()
   with torch.no_grad():replay=torch.softmax(model(X),dim=1)[:,1].numpy()
   np.testing.assert_allclose(replay,p.Probability,atol=1e-7,rtol=0);np.testing.assert_allclose(ck['probabilities'],p.Probability,atol=0,rtol=0)
   vote=(p.Probability.to_numpy()>p.Threshold.to_numpy()).astype(int);assert np.array_equal(vote,p.Y_pred) and np.array_equal((replay>p.Threshold.to_numpy()).astype(int),vote)
   met=metric(y,vote);row=testresults[(testresults.Market==market)&(testresults.Model==r.Model)&(testresults.Seed==seed)].iloc[0]
   for k in met:
    if k in row:assert np.isclose(row[k],met[k],atol=1e-12,rtol=0)
   replays.append({'Market':market,'Model':r.Model,'Seed':seed,'Max_probability_error':float(np.max(abs(replay-p.Probability))),'Labels_identical':True});votes.append(vote);seedmetrics.append(met)
  forecast=(np.sum(votes,axis=0)>=3).astype(int);met=metric(y,forecast);majority.append({'Market':market,'Model':r.Model,'Loss':r.Loss,'N':len(y),'Aggregation':'majority_3_of_5',**met})
  save(f'all_predictions/{market}_{r.Model}_representative.csv',{'Date':dates,'Y_true':y,'Majority_prediction':forecast,**{f'Seed_{s}_prediction':votes[i] for i,s in enumerate(SEEDS)}})
  frequency.append({'Market':market,'Model':r.Model,'Actual_Up_Rate':float(y.mean()),'Forecast_Up_Rate':float(forecast.mean()),'Absolute_distance_from_0_5':abs(float(forecast.mean())-.5),'Forecast_minus_actual_up_rate':float(forecast.mean()-y.mean()),'near_constant':bool(forecast.mean()<.1 or forecast.mean()>.9)})
  ptest=pt(y,forecast);pts.append({'Market':market,'Model':r.Model,**ptest,'Raw_diagnostic_only':True})
  ix=np.arange(0,len(y),20);non.append({'Market':market,'Model':r.Model,'N':len(ix),'Phase':0,'Step':20,**metric(y[ix],forecast[ix]),**{k:v for k,v in pt(y[ix],forecast[ix]).items() if k.startswith('PT_')}})
  start=loc[0]+1;end=np.where(index<='2025-12-31')[0][-1];edates=index[start:end+1];returns=np.r_[0.,close[1:]/close[:-1]-1];pos=np.zeros(len(index))
  for location,signal in zip(loc,forecast):pos[location+1:end+1]=signal
  pos[end]=0;prev=np.r_[0.,pos[:-1]];turn=(pos-prev)[start:end+1];exposure=prev[start:end+1];gross=exposure*returns[start:end+1]
  latest=np.searchsorted(loc,np.arange(start,end+1)-2,side='right')-1;expected=np.where(latest>=0,forecast[np.maximum(latest,0)],0);np.testing.assert_array_equal(exposure,expected)
  for bps in [0,10,25,50]:
   costs=abs(turn)*bps/2/10000;net=gross-costs;e=economic(net,gross,exposure,turn,edates,costs);econ.append({'Market':market,'Model':r.Model,'Mode':'Daily','Round_trip_bps':bps,**e})
   for date,p,g,c,n in zip(edates,exposure,gross,costs,net):paths.append({'Market':market,'Model':r.Model,'Round_trip_bps':bps,'Date':date,'Position_previous_close':p,'Gross_return':g,'Cost_debit':c,'Net_return':n})
  ten=next(e for e in reversed(econ) if e['Round_trip_bps']==10)
  comparison.append({'Market':market,'Model':r.Model,'Selected_Loss':r.Loss,'Validation_BA':r.WF_Val_BA_mean,'Test_BA':met['Balanced_Accuracy'],'Test_Accuracy':met['Accuracy'],'Macro_F1':met['Macro_F1'],'Forecast_Up_Rate':met['Pred_Pos_Rate'],'Actual_Up_Rate':met['Actual_Up_Rate'],'Mean_seed_Test_BA':np.mean([m['Balanced_Accuracy'] for m in seedmetrics]),'Mean_seed_Macro_F1':np.mean([m['Macro_F1'] for m in seedmetrics]),'Economic_CAGR_10bps':ten['CAGR'],'Economic_Exposure':ten['Exposure'],'PT_statistic':ptest['PT_statistic'],'PT_raw_p':ptest['PT_two_sided_p'],'PT_status':ptest['PT_status'],'Prediction_aggregation':'majority_3_of_5'})
save('majority_vote_results.csv',majority);save('forecast_frequency_diagnostics.csv',frequency);save('pt_results_phase2.csv',pts);save('nonoverlap_results_phase2.csv',non);save('transaction_cost_results_phase2.csv',econ);save('diagnostics/checkpoint_replay.csv',replays);pd.DataFrame(paths).to_csv(OUT/'diagnostics/economic_paths.csv.gz',index=False,float_format='%.17g',compression='gzip')
old=pd.read_csv(P1/'benchmark_comparison_table.csv',float_precision='round_trip');combined=pd.concat([old,pd.DataFrame(comparison)],ignore_index=True);assert len(combined)==65;save('benchmark_comparison_phase2.csv',combined)
oldmeans=pd.read_csv(P1/'diagnostics/learned_seed_means.csv');combined.loc[combined.Model.isin(oldmeans.Model),'Mean_seed_Macro_F1']=[oldmeans[(oldmeans.Market==r.Market)&(oldmeans.Model==r.Model)].Mean_Macro_F1.iloc[0] for r in combined[combined.Model.isin(oldmeans.Model)].itertuples()]
save('direct_architecture_comparison.csv',combined[combined.Model.isin(ARCH)])
paired={}
for original,added,filename in [('Transformer','PE-Transformer','pe_transformer_vs_original_transformer.csv'),('LNN','CfC','ltc_vs_cfc.csv')]:
 rows=[]
 for market in M:
  a=combined[(combined.Market==market)&(combined.Model==original)].iloc[0];b=combined[(combined.Market==market)&(combined.Model==added)].iloc[0];r={'Market':market,'Original_model':original,'Added_model':added}
  for c in ['Selected_Loss','Validation_BA','Mean_seed_Test_BA','Test_BA','Macro_F1','Forecast_Up_Rate','Test_Accuracy','PT_statistic','PT_raw_p']:r['Original_'+c]=a[c];r['Added_'+c]=b[c]
  r['Delta_BA']=b.Test_BA-a.Test_BA;r['Delta_Macro_F1']=b.Macro_F1-a.Macro_F1;rows.append(r)
 save(filename,rows);paired[added]=pd.DataFrame(rows)
ranks=[];averages=[]
for family,models in [('neural',ARCH),('all_learned',LEARNED)]:
 table=combined[combined.Model.isin(models)].copy()
 for c in ['Test_BA','Macro_F1','Test_Accuracy']:table['Rank_'+c]=table.groupby('Market')[c].rank(ascending=False,method='average')
 table['Family']=family;ranks.extend(table[['Market','Model','Family','Rank_Test_BA','Rank_Macro_F1','Rank_Test_Accuracy']].to_dict('records'))
 for model,g in table.groupby('Model'):
  averages.append({'Family':family,'Model':model,**{f'{agg}_{c}':getattr(g[c],agg)() for agg in ['mean','median'] for c in ['Rank_Test_BA','Rank_Macro_F1','Rank_Test_Accuracy']}})
save('architecture_rank_table.csv',ranks);save('cross_market_average_ranks.csv',averages)
fried=[]
for score in ['Test_BA','Macro_F1']:
 table=combined[combined.Model.isin(ARCH)].pivot(index='Market',columns='Model',values=score).loc[list(M),ARCH];st,p=stats.friedmanchisquare(*table.to_numpy().T);fried.append({'Metric':'majority_'+score,'Friedman_statistic':st,'raw_p':p,'Kendall_W':st/25,'Market_blocks':5,'Architectures':6,'Diagnostic_only':True})
save('neural_architecture_friedman.csv',fried)
# Final universe/family PROPOSALS are created only after all final probabilities exist and replay passes.
assert len(list((OUT/'checkpoints').glob('*_fold*.pt')))==450 and len(list((OUT/'checkpoints').glob('*_final.pt')))==50
assert len(list((OUT/'all_predictions').glob('*.validation.csv')))==150 and len(list((OUT/'all_predictions').glob('*.test.csv')))==50
universe={'neural_architectures':ARCH,'display_names':{'LNN':'LTC/LNN','Transformer':'Transformer (original, no explicit positional encoding)','PE-Transformer':'PE-Transformer (sinusoidal positional encoding)'},'non_neural_learned':['LogisticRegression','LightGBM'],'rule_baselines':['Persistence','Rule_200DMA','Momentum60','Always-Up','Always-Down'],'markets':list(M),'selection':'independently frozen validation-only loss and seed thresholds','predictions_complete_and_replay_verified':True,'no_replacement_of_existing_models':True};js('final_model_universe_manifest.json',universe)
js('multiplicity_family_proposal.json',{'status':'proposal_only_not_executed','Holm_applied':False,'Phase3_required':True,'families':{'A':{'test':'two-sided PT on majority predictions','count':30,'membership':[f'{m}:{a}' for m in M for a in ARCH]},'B':{'test':'two-sided PT on majority/consensus predictions','count':40,'membership':[f'{m}:{a}' for m in M for a in LEARNED]},'C':{'test':'two-sided PT on LTC majority predictions','count':5,'membership':[f'{m}:LNN' for m in M]},'D':{'test':'paired original Transformer vs PE-Transformer; specific test to freeze in Phase3 before execution','count':5,'membership':[f'{m}:Transformer_vs_PE-Transformer' for m in M]}},'old_Holm_results_unchanged':True,'constant_forecast_undefined_PT':'retain membership and status, no fabricated p-value'})
for path,digest in run['protected_original_artifact_sha256'].items():assert sha(ROOT/path)==digest,path
for path,digest in run['input_sha256'].items():assert sha(ROOT/path)==digest,path
for path,digest in run['source_sha256'].items():assert sha(OUT/path)==digest,path
# Explicit answers use descriptive differences only, with no superiority claims from raw p.
lines=['# Phase 2 architecture expansion','', 'All losses/thresholds were frozen using validation only before final fits. Existing artifacts and Phase1 outputs are byte-unchanged. No final Holm correction or DM/GW/MCS analysis was executed.', '', 'The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence.', '', '## Market results (3-of-5 majority; seed means are reported separately)','',pd.DataFrame(comparison)[['Market','Model','Selected_Loss','Test_BA','Macro_F1','Forecast_Up_Rate','Mean_seed_Test_BA','Economic_CAGR_10bps','Economic_Exposure']].to_markdown(index=False),'','## Architecture sensitivity','',paired['CfC'][['Market','Delta_BA','Delta_Macro_F1']].to_markdown(index=False),'',paired['PE-Transformer'][['Market','Delta_BA','Delta_Macro_F1']].to_markdown(index=False),'','## Research questions']
c=paired['CfC'];pe=paired['PE-Transformer'];positive=[r for r in pts if np.isfinite(r['PT_statistic']) and r['PT_statistic']>0 and r['PT_two_sided_p']<.05]
lines += [f'1. CfC vs LTC: majority BA differences range from {c.Delta_BA.min():.4f} to {c.Delta_BA.max():.4f}; descriptive architecture sensitivity, not a materiality test.',f'2. CfC exceeds LTC majority BA in {int((c.Delta_BA>0).sum())}/5 markets; this does not establish consistent multiplicity-aware superiority.',f'3. Positional encoding changes majority BA by {pe.Delta_BA.min():.4f} to {pe.Delta_BA.max():.4f}; original Transformer is retained.', '4. Forecast-frequency diagnostics retain all near-constant outcomes; compare original and PE rates in the paired table, without excluding or retuning.', '5. KOSPI architecture sensitivity (not a replication target): '+pe[pe.Market=='KOSPI200'].to_json(orient='records'),f'6. There are {len(positive)} positive conventional two-sided raw PT p<0.05 exceptions among the10 new comparisons. Raw tests with overlapping H20 labels do not establish stable positive evidence; final family correction is deferred.', '7. Phase0/step20 metrics and PT are retained in nonoverlap_results_phase2.csv. No favorable phase search or independence claim is made.', '8. Economic CAGR must be read with exposure, turnover and buy-and-hold in the benchmark table. Positive long/cash returns alone do not identify timing skill; this phase does not test economic significance.', '9. Six-neural majority Friedman diagnostics: '+json.dumps(fried)+'. Only five blocks: non-significance is not equivalence; significance is not dominance.', '10. Interpret changes jointly as architecture-sensitive and benchmark-sensitive apparent advantages; isolated raw signals are statistically fragile rather than evidence that evaluation design no longer matters.', '11. No stable cross-market dominance is established by this descriptive analysis or raw p-values.', '12. Phase3 should use the fixed six-neural/eight-learned universe and the explicit30/40/5/5 family proposals. Freeze paired-test and DM/GW/MCS loss/differential definitions before execution.']
(OUT/'results_report.md').write_text('\n\n'.join(lines)+'\n')
(OUT/'methodology_notes.md').write_text('''# Frozen methodology
Exact Phase1 processed tensors, per-feature training-only scalers, original label purges and W20 windows are reused without feature reconstruction or network access. Historical source timestamp/vintage limitations remain as in source audits. Original CfCModel calls ncps.torch.CfC(input_size,128,batch_first=True); unspecified package defaults are preserved. Fully connected CfC is distinct from LTC, with explicit0.2 dropout and Linear128->2. Internal default CfC backbone is library behavior, not an added tuned architecture. Original Linear initialization is reused.

PE-Transformer subclasses the original Transformer and adds only a persistent sinusoidal buffer after input projection. It adds no parameters or dropout. Before fitting, same-seed original and PE model parameters are checked identical; with PE zeroed, outputs are bit-identical. The original unmasked encoder only sees the20 past input observations and therefore is not changed to a causal attention mask.

All450 validation fits (2 architectures x5 markets x3 losses x5 seeds x3 folds) precede all50 selected final fits. Each seed threshold comes from pooled three-fold validation only; loss is chosen by five-seed mean validation BA, MacroF1, mean threshold distance and lexical loss. No model is selected from test metrics. Majority is binary3-of-5, never probability averaging. Seed means and majority metrics differ intentionally.

Checkpoint replay restores the original set_seed deterministic algorithms before constructing each model, uses CPU evaluation and verifies probabilities at original1e-7 tolerance and exact labels. CSVs preserve17 significant digits. Source SHA ledgers protect all tracked historical artifacts and Phase1.

Conventional PT is the unchanged validated function. Constant forecast undefined results are retained. H20 serial dependence limits conventional PT interpretation. Phase0/step20 is fixed and does not establish independence. No final Holm, DM, GW, MCS or paired PE significance tests are executed. Family proposals are future work; no HMM refit occurs.

Economics exactly follows existing long/cash accounting: prediction at t executes next close, first earns next interval, round-trip bps charged half per one-way position change, final liquidation included. Costs0/10/25/50bps; primary10bps. No dividends/FX, shorts or leverage. Baselines using P_t have an information difference from learned windows excluding t, unchanged and explicitly retained. Positive CAGR may reflect exposure rather than timing. Ranks and Friedman use operational majority metrics and five market blocks; no primary model reselection.
''')
check={'status':'validated','existing_artifacts_unchanged':True,'Phase1_artifacts_unchanged':True,'same_frozen_data':True,'H':20,'W':20,'same_split':True,'same_feature_set':True,'no_test_driven_loss_selection':True,'no_test_driven_threshold_selection':True,'CfC_constructor_frozen_before_test':True,'PE_architecture_frozen_before_test':True,'PE_differs_only_by_positional_encoding':True,'no_HMM_refit':True,'no_phase_search':True,'all_seed_predictions_saved':True,'all_selected_configs_recorded':True,'all_negative_null_outcomes_retained':True,'checkpoint_replay_verified':True,'no_original_Transformer_replacement':True,'no_LTC_replacement':True,'final_universe_manifest_created':True,'validation_fits':450,'final_fits':50,'Holm_not_executed':True}
js('completion_check.json',check);js('analysis_manifest.json',{'status':'validated','source_sha256':run['source_sha256'],'input_sha256':run['input_sha256'],'selection_lock':selection,'output_sha256':{str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*') if p.is_file() and p.suffix in ['.csv','.md','.json'] and p.name not in ['analysis_manifest.json','execution_status.json','progress.json','active_job.json']}})
print(pd.DataFrame(comparison).to_string(index=False),flush=True)
