"""Frozen inference only: no training, predictions regenerated or source artifacts edited."""
import os
for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[key]='2'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast,itertools,sys,traceback
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score
from arch.bootstrap import MCS
from statistical_methods import dm,gw,holm,spa
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];os.chdir(ROOT);P1=ROOT/'artifacts/jof_phase1_benchmark_expansion';P2=ROOT/'artifacts/jof_phase2_architecture_expansion'
lock=json.loads((OUT/'protocol_lock.json').read_text());MARKETS=lock['markets'];LEARNED=lock['learned'];ARCH=lock['neural'];MODELS=lock['model_universe'];CANDIDATES=LEARNED+lock['rules'][:3];SEEDS=lock['seeds']
DIR={'SP500':'sp500_rerun','NASDAQ100':'nasdaq100','NIKKEI225':'nikkei225','EUROSTOXX50':'eurostoxx50','KOSPI200':'kospi200'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(name,x):(OUT/name).write_text(json.dumps(x,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x))+'\n')
def save(name,x):pd.DataFrame(x).to_csv(OUT/name,index=False,float_format='%.17g')
def metrics(y,f):return {'Accuracy':accuracy_score(y,f),'BA':balanced_accuracy_score(y,f),'Macro_F1':f1_score(y,f,labels=[0,1],average='macro',zero_division=0),'Forecast_Up_Rate':float(np.mean(f)),'Actual_Up_Rate':float(np.mean(y))}
source=ROOT/'artifacts/validation_selected_pt_tests/analyze.py';tree=ast.parse(source.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pt');ns={'np':np,'pd':pd,'stats':stats,'balanced_accuracy_score':balanced_accuracy_score,'f1_score':f1_score};exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),ns);pt=ns['pt']
selection=pd.read_csv(P2/'selected_configs.csv');benchmark=pd.read_csv(P2/'benchmark_comparison_phase2.csv');assert len(selection)==40
inventory=[];inputhash={};ALL={};PT=[];DM=[];GW=[];NON=[];MCSROWS=[];SPAROWS=[];CLASS=[]
def read(path):
 inputhash[str(path.relative_to(ROOT))]=sha(path);return pd.read_csv(path,float_precision='round_trip')
def load_predictions(market):
 labels={};probs={};refdates=None;y=None
 for model in LEARNED:
  loss=selection[(selection.Market==market)&(selection.Model==model)].Loss.iloc[0];predictions=[];probabilities=[]
  for seed in SEEDS:
   if model in ['CfC','PE-Transformer']:path=P2/'all_predictions'/f'{market}_{model}_{loss}_{seed}.test.csv'
   elif model in ['GRU','LogisticRegression','LightGBM']:path=P1/'all_predictions'/f'{market}_{model}_{loss}_{seed}.test.csv'
   else:path=ROOT/'artifacts'/DIR[market]/'predictions'/f'{model}_{loss}_{seed}.csv'
   p=read(path);dates=pd.to_datetime(p.Date)
   if refdates is None:refdates=dates;y=p.Y_true.to_numpy(int)
   assert np.array_equal(dates,refdates) and np.array_equal(p.Y_true,y)
   probability=p.Probability.to_numpy();assert np.isfinite(probability).all() and ((probability>=0)&(probability<=1)).all()
   f=(probability>p.Threshold.to_numpy()).astype(int)
   if 'Y_pred' in p:assert np.array_equal(f,p.Y_pred)
   probabilities.append(probability);predictions.append(f)
   inventory.append({'Market':market,'Model':model,'Loss':loss,'Seed':seed,'Source':str(path.relative_to(ROOT)),'SHA256':sha(path),'N':len(y),'First_date':str(dates.iloc[0].date()),'Last_date':str(dates.iloc[-1].date()),'Probability_available':True})
  if model in ['LogisticRegression','LightGBM']:
   assert all(np.array_equal(predictions[0],f) for f in predictions) and all(np.array_equal(probabilities[0],p) for p in probabilities),'Do not silently average nonidentical deterministic seeds'
  f=(np.sum(predictions,axis=0)>=3).astype(int);labels[model]=f;probs[model]=np.mean(probabilities,axis=0)
  rep=read((P2 if model in ['CfC','PE-Transformer'] else P1)/'all_predictions'/f'{market}_{model}_representative.csv');assert np.array_equal(rep.Majority_prediction,f) and np.array_equal(pd.to_datetime(rep.Date),refdates)
 rawpath=ROOT/'artifacts'/DIR[market]/'market_input.csv';inputhash[str(rawpath.relative_to(ROOT))]=sha(rawpath);raw=pd.read_csv(rawpath,index_col=0,parse_dates=True,float_precision='round_trip');loc=raw.index.get_indexer(refdates);close=raw.Close.to_numpy();assert np.array_equal((close[loc+20]>close[loc]).astype(int),y)
 prior=read(ROOT/'artifacts/cross_market_statistics'/f'{market}_majority_predictions.csv');assert np.array_equal(pd.to_datetime(prior.Date),refdates);labels['Persistence']=prior.Persistence_prediction.to_numpy(int)
 for model in ['Rule_200DMA','Momentum60']:
  path=P1/'all_predictions'/f'{market}_{model}.rule.csv';r=read(path);assert np.array_equal(pd.to_datetime(r.Date),refdates) and np.array_equal(r.Y_true,y);labels[model]=r.Y_pred.to_numpy(int)
 labels['Always-Up']=np.ones(len(y),int);labels['Always-Down']=np.zeros(len(y),int)
 for model in lock['rules']:
  probs[model]=labels[model].astype(float);inventory.append({'Market':market,'Model':model,'Loss':'deterministic_rule','Seed':'deterministic','Source':'Frozen saved rule/Persistence predictions; constants fixed0/1','N':len(y),'First_date':str(refdates.iloc[0].date()),'Last_date':str(refdates.iloc[-1].date()),'Probability_available':False})
 features=read(P1/'frozen_features'/f'{market}.csv');features.index=pd.to_datetime(features.iloc[:,0]);assert np.array_equal(features.index,raw.index)
 return {'y':y,'dates':refdates,'labels':labels,'prob':probs,'raw':raw,'loc':loc,'absret':features.Log_Ret.abs().to_numpy(),'vol':features.Vol20.to_numpy()}

def paired(market,A,B,losses,lossname='Brier',reduced=False):
 a,b=losses[A],losses[B];r={'Market':market,'Model_A':A,'Model_B':B,'Loss':lossname,**dm(a,b,h=1 if reduced else 20,lag=0 if reduced else 19),'Overlap_caveat':'H20 overlapping targets; HAC19 approximates dependence, does not guarantee valid finite-sample inference'}
 return r

def run():
 source_manifest=json.loads((OUT/'source_manifest.json').read_text());assert sha(OUT/'protocol_lock.json')==source_manifest['protocol_sha256']
 js('execution_status.json',{'status':'running','started_at_utc':datetime.now(timezone.utc).isoformat(),'no_training':True})
 # Freeze executed code hashes before the first outcome calculation.
 js('execution_manifest.json',{'source_sha256':{p.name:sha(p) for p in OUT.glob('*.py')},'protocol_sha256':sha(OUT/'protocol_lock.json'),'arch_version':'8.0.0','bootstrap_reps':10000,'random_seed':20261106})
 for market in MARKETS:
  print('LOAD',market,flush=True);data=load_predictions(market);ALL[market]=data;y=data['y'];labels=data['labels'];prob=data['prob'];losses={m:(prob[m]-y)**2 for m in MODELS};data['losses']=losses;ix=np.arange(0,len(y),20)
  save(f'diagnostics/{market}_frozen_scoring_inputs.csv',{'Date':data['dates'],'y_true':y,**{f'{m}_Probability':prob[m] for m in MODELS},**{f'{m}_Label':labels[m] for m in MODELS}})
  for model in MODELS:
   ptest=pt(y,labels[model]);PT.append({'Market':market,'Model':model,'PT_stat':ptest['PT_statistic'],'raw_p':ptest['PT_two_sided_p'],'positive_one_sided_p':ptest['PT_positive_one_sided_p'],'PT_status':ptest['PT_status'],**metrics(y,labels[model])})
   CLASS.append({'Market':market,'Model':model,**metrics(y,labels[model]),'Brier_mean':float(losses[model].mean())})
   npt=pt(y[ix],labels[model][ix]);NON.append({'Market':market,'Model':model,'Benchmark':'','Test':'PT','N':len(ix),'Phase':0,'Step':20,**metrics(y[ix],labels[model][ix]),'Statistic':npt['PT_statistic'],'raw_p':npt['PT_two_sided_p'],'Status':npt['PT_status'],'Low_power':True})
  for A,B in itertools.combinations(MODELS,2):
   DM.append(paired(market,A,B,losses));GW.append({'Market':market,'Model_A':A,'Model_B':B,'Loss':'Brier',**gw(losses[A],losses[B],data['loc'],data['absret'],data['vol'])})
  logloss={m:-(y*np.log(np.clip(prob[m],1e-12,1-1e-12))+(1-y)*np.log1p(-np.clip(prob[m],1e-12,1-1e-12))) for m in LEARNED}
  for A,B in itertools.combinations(LEARNED,2):DM.append(paired(market,A,B,logloss,'Log_loss_secondary'))
  for A in LEARNED:
   for B in lock['rules'][:3]:
    r=paired(market,A,B,{m:losses[m][ix] for m in MODELS},reduced=True);NON.append({'Market':market,'Model':A,'Benchmark':B,'Test':'DM','N':len(ix),'Phase':0,'Step':20,'Statistic':r['DM_stat'],'raw_p':r['raw_two_sided_p'],'Mean_differential':r['Mean_differential'],'HAC_lag':0,'Low_power':True,'Status':r['Status']})
  NON.append({'Market':market,'Model':'11model fixed candidate universe','Test':'MCS','N':len(ix),'Phase':0,'Step':20,'Low_power':True,'Status':'not_run_prespecified_N_less_than100'})
  # Joint bootstrap uses complete eleven-model set, even if learned majority predictions are constant.
  lossframe=pd.DataFrame({m:losses[m] for m in CANDIDATES});mcs=MCS(lossframe,size=.10,reps=10000,block_size=20,method='R',bootstrap='stationary',seed=20261106);mcs.compute();pvalues=mcs.pvalues
  assert np.isfinite(pvalues.Pvalue).all()
  for order,(model,row) in enumerate(pvalues.iterrows(),1):MCSROWS.append({'Market':market,'Model':model,'Elimination_order':order,'MCS_p':row.Pvalue,'MCS90_member':bool(row.Pvalue>.10),'MCS95_member':bool(row.Pvalue>.05),'Mean_Brier':lossframe[model].mean(),'Reps':10000,'Seed':20261106,'Expected_block_length':20,'Bootstrap':'stationary','Method':'R','N':len(y)})
  sr,means,mu=spa(lossframe.to_numpy(),benchmark_index=CANDIDATES.index('Persistence'));alternatives=[m for m in CANDIDATES if m!='Persistence'];best=alternatives[int(np.argmax(mu))];SPAROWS.append({'Market':market,**{k:v for k,v in sr.items() if k not in ['Mean_improvements','LR_variance']},'Benchmark':'Persistence','Best_mean_improvement_model':best,'Best_mean_improvement':float(np.max(mu)),'Reject_at_0_05':sr['p_value']<.05})
  save(f'diagnostics/{market}_SPA_variances.csv',[{'Model':m,'Mean_Persistence_minus_model_loss':mean,'LR_variance':var} for m,mean,var in zip(alternatives,mu,sr['LR_variance'])]);np.savez_compressed(OUT/'diagnostics'/f'{market}_SPA_bootstrap_means.npz',means=means,mu=mu,alternatives=np.array(alternatives))
  print('INFERENCE COMPLETE',market,flush=True);js('progress.json',{'markets_completed':len(ALL),'markets_total':5,'updated_at_utc':datetime.now(timezone.utc).isoformat()})
 save('prediction_inventory.csv',inventory);save('dm_results_all.csv',DM);save('gw_results_all.csv',GW);save('pt_results_all.csv',PT);save('nonoverlap_inference.csv',NON);save('mcs_results.csv',MCSROWS);save('spa_results.csv',SPAROWS);save('classification_and_loss_metrics.csv',CLASS)
 mcs=pd.DataFrame(MCSROWS);save('model_confidence_sets_by_market.csv',[{'Market':market,'MCS90_retained':','.join(g[g.MCS90_member].Model),'MCS90_eliminated':','.join(g[~g.MCS90_member].Model),'MCS95_retained':','.join(g[g.MCS95_member].Model),'Interpretation':'The MCS procedure did not eliminate these models at the stated confidence level.'} for market,g in mcs.groupby('Market',sort=False)])
 pf=pd.DataFrame(PT);dmf=pd.DataFrame(DM);gwf=pd.DataFrame(GW);nf=pd.DataFrame(NON);cf=pd.DataFrame(CLASS);families={}
 for family,models,name,col in [('A',ARCH,'holm_family_A_neural30.csv','Holm30_p'),('B',LEARNED,'holm_family_B_learned40.csv','Holm40_p'),('C',['LNN'],'holm_family_C_ltc5.csv','Holm5_p')]:
  f=pf[pf.Model.isin(models)].copy();assert len(f)==len(lock['Holm_families'][family]);f[col]=holm(f.raw_p);f['Holm_adjusted_p']=f[col];f['Undefined_p_counted_as1_for_correction']=f.raw_p.isna();f['sign_of_PT']=np.sign(f.PT_stat);f['positive_directional_support']=(f.PT_stat>0)&(f[col]<.05);f['Association']=np.where((f.PT_stat<0)&(f[col]<.05),'significant negative association',np.where(f.positive_directional_support,'positive directional support','no positive corrected support'));save(name,f);families[family]=f
 d=dmf[(dmf.Loss=='Brier')&(dmf.Model_A=='Transformer')&(dmf.Model_B=='PE-Transformer')].copy();assert len(d)==5;d['Holm5_p']=holm(d.raw_two_sided_p);d['Significant_difference']=d.Holm5_p<.05;d['Favors_PE']=d.Mean_differential>0;save('holm_family_D_pe5.csv',d)
 foc=[]
 for base in lock['rules'][:3]:
  f=dmf[(dmf.Loss=='Brier')&dmf.Model_A.isin(LEARNED)&(dmf.Model_B==base)].copy();assert len(f)==40;f['Benchmark_family_Holm_p']=holm(f.raw_two_sided_p);f['Model_win_after_Holm']=(f.Mean_differential<0)&(f.Benchmark_family_Holm_p<.05);f['Benchmark_win_after_Holm']=(f.Mean_differential>0)&(f.Benchmark_family_Holm_p<.05);save(f'dm_holm_vs_{base}.csv',f);foc.append(f)
 focal=pd.concat(foc,ignore_index=True);save('dm_focal_benchmarks.csv',focal);conclusions=[]
 economics=pd.concat([read(P1/'transaction_cost_results.csv'),read(P2/'transaction_cost_results_phase2.csv')],ignore_index=True);economics=economics[(economics.Round_trip_bps==10)&economics.Model.isin(LEARNED)];assert len(economics)==40
 for market in MARKETS:
  for model in LEARNED:
   primary=cf[(cf.Market==market)&(cf.Model==model)].iloc[0];p=families['B'][(families['B'].Market==market)&(families['B'].Model==model)].iloc[0];a=families['A'][(families['A'].Market==market)&(families['A'].Model==model)]
   mc=mcs[(mcs.Market==market)&(mcs.Model==model)].iloc[0];econ=economics[(economics.Market==market)&(economics.Model==model)].iloc[0];n=nf[(nf.Market==market)&(nf.Model==model)&(nf.Test=='PT')].iloc[0];row={'Market':market,'Model':model,'BA':primary.BA,'Macro_F1':primary.Macro_F1,'Forecast_Up_Rate':primary.Forecast_Up_Rate,'PT_raw_p':p.raw_p,'PT_stat':p.PT_stat,'PT_Holm30_or_40':p.Holm40_p,'PT_Holm40':p.Holm40_p,'PT_Holm30':a.Holm30_p.iloc[0] if len(a) else np.nan,'PT_positive_support':bool(p.positive_directional_support),'PT_association':p.Association,'MCS90_member':mc.MCS90_member,'MCS95_member':mc.MCS95_member,'reduced_overlap_BA':n.BA,'Economic_CAGR_10bps':econ.CAGR,'Sharpe_10bps':econ.Sharpe,'Exposure':econ.Exposure,'Turnover_10bps':econ.Turnover,'near_constant_warning':bool(primary.Forecast_Up_Rate<.1 or primary.Forecast_Up_Rate>.9),'exposure_warning':bool(econ.Exposure<.1 or econ.Exposure>.9)}
   wins=[]
   for base in lock['rules'][:3]:
    r=focal[(focal.Market==market)&(focal.Model_A==model)&(focal.Model_B==base)].iloc[0];tag={'Persistence':'Persistence','Rule_200DMA':'200DMA','Momentum60':'Momentum60'}[base];row[f'DM_vs_{tag}_raw_p']=r.raw_two_sided_p;row[f'DM_vs_{tag}_Holm']=r.Benchmark_family_Holm_p;row[f'DM_vs_{tag}_mean_differential']=r.Mean_differential;row[f'DM_win_vs_{tag}']=bool(r.Model_win_after_Holm);wins.append(bool(r.Model_win_after_Holm))
   ng=nf[(nf.Market==market)&(nf.Model==model)&(nf.Test=='DM')&(nf.Benchmark=='Persistence')].iloc[0];g=gwf[(gwf.Market==market)&(gwf.Model_A==model)&(gwf.Model_B=='Persistence')].iloc[0];row['GW_vs_Persistence_p']=g.raw_p;row['reduced_overlap_DM_vs_Persistence_p']=ng.raw_p
   rawpositive=p.PT_stat>0 and p.raw_p<.05;dependent=wins[0] and not(ng.raw_p<.05 and ng.Mean_differential<0)
   row['Final_assessment']='dependence-sensitive' if dependent else 'benchmark-sensitive' if any(wins) and not all(wins) else 'positive loss evidence but not directional evidence' if all(wins) and not p.positive_directional_support else 'multiplicity-sensitive' if rawpositive and not p.positive_directional_support else 'isolated descriptive advantage' if primary.BA>.5 else 'no positive evidence';conclusions.append(row)
 save('statistical_conclusion_matrix.csv',conclusions);c=pd.DataFrame(conclusions);summary=[];cf['BA_rank']=cf.groupby('Market').BA.rank(ascending=False,method='average')
 for model,g in c.groupby('Model',sort=False):
  x=cf[cf.Model==model];persistence=cf[cf.Model=='Persistence'].set_index('Market').BA;summary.append({'Model':model,'Mean_BA':g.BA.mean(),'Mean_Macro_F1':g.Macro_F1.mean(),'Average_BA_rank_all13':x.BA_rank.mean(),'Markets_BA_above0_5':int((g.BA>.5).sum()),'Markets_BA_above_Persistence':sum(r.BA>persistence[r.Market] for r in g.itertuples()),'Positive_PT_raw':int(((g.PT_stat>0)&(g.PT_raw_p<.05)).sum()),'Positive_PT_Holm40':int(g.PT_positive_support.sum()),'Positive_PT_Holm30':int(((g.PT_stat>0)&(g.PT_Holm30<.05)).sum()) if model in ARCH else np.nan,**{f'DM_wins_vs_{base}_Holm':int(g[f'DM_win_vs_{base}'].sum()) for base in ['Persistence','200DMA','Momentum60']},'MCS90_inclusions':int(g.MCS90_member.sum()),'Near_constant_markets':int(g.near_constant_warning.sum()),'Average_exposure':g.Exposure.mean()})
 save('cross_market_summary.csv',summary)
 import report
 report.generate(OUT,lock,c,pd.DataFrame(summary),families,d,focal,mcs,pd.DataFrame(SPAROWS),nf)
 for path,digest in source_manifest['protected_previous_artifact_sha256'].items():assert sha(ROOT/path)==digest,path
 for path,digest in inputhash.items():assert sha(ROOT/path)==digest,path
 assert len(DM)==5*(78+28) and len(GW)==390 and len(focal)==120 and len(MCSROWS)==55 and len(c)==40
 check={'status':'validated','no_retraining':True,'predictions_loaded_from_frozen_artifacts':True,'final_universe_unchanged':True,'Brier_primary_frozen_before_inference':True,'log_loss_secondary_learned_only':True,'HAC_lag19_primary':True,'DM_sign_fixed':True,'GW_conditioning_fixed_and_resolved_label_causal':True,'Holm_families_fixed_before_correction':True,'MCS_levels_fixed':True,'SPA_benchmark_Persistence_fixed':True,'block_length20_fixed':True,'bootstrap_seed20261106_fixed':True,'no_phase_search':True,'no_outcome_based_removal':True,'near_constant_flags_retained':True,'reduced_overlap_caveat_retained':True,'all_null_negative_retained':True,'existing_artifacts_unchanged':True,'method_independent_checks_passed':True,'learned_prediction_files':200,'pairwise_DM_rows':len(DM),'pairwise_GW_rows':len(GW),'MCS_candidate_rows':len(MCSROWS),'MCS_reps':10000,'SPA_reps':10000}
 js('completion_check.json',check);js('final_inference_manifest.json',{'status':'validated','protocol_sha256':sha(OUT/'protocol_lock.json'),'source_sha256':json.loads((OUT/'execution_manifest.json').read_text())['source_sha256'],'prediction_input_sha256':inputhash,'prior_artifact_ledger':'source_manifest.json','output_sha256':{str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*') if p.is_file() and p.name not in ['execution.log','execution_status.json','progress.json','final_inference_manifest.json'] and '__pycache__' not in p.parts},'completed_at_utc':datetime.now(timezone.utc).isoformat()});js('execution_status.json',{'status':'completed','validated':True,'completed_at_utc':datetime.now(timezone.utc).isoformat(),'publication':'pending'});print('VALIDATED',flush=True)
if __name__=='__main__':
 try:run()
 except BaseException as e:js('execution_status.json',{'status':'failed','error':str(e)});raise
