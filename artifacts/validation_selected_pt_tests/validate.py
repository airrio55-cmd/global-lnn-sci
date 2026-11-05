"""Independent PT reference-formula/Pearson checks on actual frozen cases."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast
import numpy as np,pandas as pd
from scipy import stats
from sklearn.metrics import balanced_accuracy_score,f1_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
manifest=json.loads((OUT/'analysis_manifest.json').read_text());protocol=json.loads((OUT/'pt_protocol.json').read_text());reference=json.loads((OUT/'pt_reference.json').read_text())
for key in ['input_sha256','protected_original_artifact_sha256']:
 for name,digest in manifest[key].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
assert hashlib.sha256(Path('/tmp/rugarch-tests-pt.R').read_bytes()).hexdigest()==reference['source_sha256']
selection=pd.read_csv(OUT/'selected_primary_configs.csv');assert len(selection)==15
M={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
oldsel=pd.read_csv(ROOT/'artifacts/validation_selected_statistical_robustness/selected_primary_configs.csv')
for r in selection.itertuples():
 f=pd.read_csv(ROOT/M[r.Market]/'summary.csv',usecols=['Model','Loss','WF_Val_BA_mean']);f=f[f.Model==r.Architecture].sort_values(['WF_Val_BA_mean','Loss'],ascending=[False,True]);assert f.iloc[0].Loss==r.Selected_Loss
 assert oldsel[(oldsel.Market==r.Market)&(oldsel.Architecture==r.Architecture)].Loss.iloc[0]==r.Selected_Loss
# Compile ONLY the PT function for edge checks; never execute the analysis script or overwrite its results.
tree=ast.parse((OUT/'analyze.py').read_text());definition=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pt');space={'np':np,'stats':stats,'balanced_accuracy_score':balanced_accuracy_score,'f1_score':f1_score};exec(compile(ast.Module(body=[definition],type_ignores=[]),'pt-function-only','exec'),space)
seed=pd.read_csv(OUT/'pt_seed_level_results.csv',float_precision='round_trip');major=pd.read_csv(OUT/'pt_holm_adjusted_results.csv',float_precision='round_trip');non=pd.read_csv(OUT/'pt_nonoverlap_results.csv',float_precision='round_trip');high=pd.read_csv(OUT/'pt_nikkei_high_results.csv',float_precision='round_trip');bench=pd.read_csv(OUT/'pt_benchmark_context.csv',float_precision='round_trip');audit=pd.read_csv(OUT/'majority_forecasts_audit.csv');selected_dates=pd.read_csv(OUT/'pt_nonoverlap_selected_dates.csv')
assert len(seed)==75 and len(major)==15 and len(non)==5 and len(high)==8 and len(bench)==15
cases=[];original={}
for r in seed.itertuples():
 directory=ROOT/M[r.Market];p=pd.read_csv(directory/'predictions'/f'{r.Architecture}_{r.Selected_Loss}_{r.Seed}.csv',float_precision='round_trip');f=(p.Probability.to_numpy()>r.Threshold).astype(int);y=p.Y_true.to_numpy(int);assert np.allclose(p.Threshold,r.Threshold,atol=1e-14,rtol=0)
 original[(r.Market,r.Architecture,r.Seed)]=f;cases.append(('Seed',f'{r.Market}/{r.Architecture}/{r.Seed}',y,f,r._asdict()))
for r in major.itertuples():
 g=audit[(audit.Market==r.Market)&(audit.Architecture==r.Architecture)];y=g.Y_true.to_numpy(int);votes=np.array([original[(r.Market,r.Architecture,s)] for s in [42,52,62,72,82]]);f=(votes.sum(axis=0)>=3).astype(int);assert np.array_equal(f,g.Majority_forecast)
 cases.append(('Majority',f'{r.Market}/{r.Architecture}',y,f,r._asdict()))
for r in non.itertuples():
 g=audit[(audit.Market==r.Market)&(audit.Architecture=='LNN')].reset_index(drop=True);ix=np.arange(0,len(g),20);s=selected_dates[selected_dates.Market==r.Market];assert np.array_equal(s.Original_prediction_row,ix) and np.array_equal(s.Y_true,g.iloc[ix].Y_true) and np.array_equal(s.LNN_majority,g.iloc[ix].Majority_forecast);assert np.array_equal(pd.to_datetime(s.Date),pd.to_datetime(g.iloc[ix].Date))
 cases.append(('Nonoverlap',r.Market,g.iloc[ix].Y_true.to_numpy(int),g.iloc[ix].Majority_forecast.to_numpy(int),r._asdict()))
for r in bench.itertuples():
 g=audit[(audit.Market==r.Market)&(audit.Architecture=='LNN')];y=g.Y_true.to_numpy(int);f=g.Persistence.to_numpy(int) if r.Benchmark=='Persistence' else np.full(len(y),int(r.Benchmark=='Always_Up'))
 cases.append(('Benchmark',r.Market+'/'+r.Benchmark,y,f,r._asdict()))
hmm=pd.read_csv(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv');hmm.Date=pd.to_datetime(hmm.Date);g=audit[(audit.Market=='NIKKEI225')&(audit.Architecture=='LNN')];mask=hmm[hmm.Market=='NIKKEI225'].set_index('Date').loc[pd.to_datetime(g.Date),'Regime'].eq('High').to_numpy();assert mask.sum()==117
for r in high.itertuples():
 f=(original[('NIKKEI225','LNN',int(r.Seed))] if r.Aggregation.startswith('Seed_') else g.Majority_forecast.to_numpy(int) if r.Aggregation=='Majority' else g.Persistence.to_numpy(int) if r.Aggregation=='Persistence' else np.ones(len(g),int))
 cases.append(('Nikkei_High',r.Aggregation,g.Y_true.to_numpy(int)[mask],f[mask],r._asdict()))
diagnostics=[];constant=0
for category,key,y,f,r in cases:
 n=len(y);a=2*y-1;b=2*f-1;px=float(np.mean(a>0));py=float(np.mean(b>0));ph=float(np.mean(a*b>0));pstar=py*px+(1-py)*(1-px)
 # Literal rugarch sign-based formula, with its variable naming and term order.
 vhit=pstar*(1-pstar)/n
 vstar=(2*py-1)**2*px*(1-px)/n+(2*px-1)**2*py*(1-py)/n+4*px*py*(1-px)*(1-py)/(n*n)
 variance=vhit-vstar
 assert np.isclose(r['Observed_hit_rate'],ph,atol=1e-14,rtol=0) and np.isclose(r['Expected_independent_hit_rate'],pstar,atol=1e-14,rtol=0)
 assert np.isclose(r['Var_hat'],variance,atol=1e-14,rtol=0)
 if len(np.unique(f))==1:
  constant+=1;assert r['PT_status']=='PT not defined for constant forecast' and np.isnan(r['PT_statistic']) and np.isnan(r['PT_two_sided_p']) and np.isnan(r['PT_positive_one_sided_p'])
  diagnostics.append({'Category':category,'Case':key,'N':n,'Status':r['PT_status'],'Reference_formula_checked':True,'Pearson_identity_checked':False,'Small_cell_warning':r['Small_cell_warning']});continue
 assert len(np.unique(y))==2 and variance>0
 reference_stat=(ph-pstar)/np.sqrt(variance);table=np.bincount(2*y+f,minlength=4).reshape(2,2);pearson=stats.chi2_contingency(table,correction=False).statistic
 assert np.isclose(reference_stat,r['PT_statistic'],atol=1e-10,rtol=0)
 assert np.isclose(reference_stat**2,n/(n-1)*pearson,atol=1e-8,rtol=1e-10)
 assert np.isclose(2*stats.norm.cdf(-abs(reference_stat)),r['PT_two_sided_p'],atol=1e-14,rtol=0)
 assert np.isclose(stats.norm.cdf(-reference_stat),r['PT_positive_one_sided_p'],atol=1e-14,rtol=0)
 diagnostics.append({'Category':category,'Case':key,'N':n,'Status':r['PT_status'],'Reference_formula_checked':True,'Pearson_identity_checked':True,'PT_reference_difference':reference_stat-r['PT_statistic'],'Small_cell_warning':r['Small_cell_warning']})
def verify_holm(frame,pcol,outcol):
 p=frame[pcol].fillna(1).to_numpy();ix=np.argsort(p);last=0
 for rank,pos in enumerate(ix):
  last=max(last,min(1,(len(p)-rank)*p[pos]));actual=frame[outcol].iloc[pos]
  if pd.isna(frame[pcol].iloc[pos]):assert pd.isna(actual)
  else:assert np.isclose(last,actual,atol=1e-12,rtol=0)
verify_holm(major,'PT_two_sided_p','Holm15_p');verify_holm(major,'PT_positive_one_sided_p','Holm15_positive_p');lnn=major[major.Architecture=='LNN'];verify_holm(lnn,'PT_two_sided_p','Holm5_LNN_p');verify_holm(lnn,'PT_positive_one_sided_p','Holm5_LNN_positive_p');verify_holm(non,'PT_two_sided_p','Exploratory_Holm5_p')
assert np.array_equal(major.Positive_direction_supported_Holm15,major.PT_statistic.gt(0)&major.Holm15_p.lt(.05));assert np.array_equal(lnn.Directional_Accuracy_Supported_Holm5,lnn.PT_statistic.gt(0)&lnn.Holm5_LNN_p.lt(.05))
assert bench[bench.Benchmark.isin(['Always_Up','Always_Down'])].PT_statistic.isna().all()
# Actual-constant edge uses an existing frozen label/prediction subset, not a new market forecast.
y=g.Y_true.to_numpy(int)[mask];f=g.Majority_forecast.to_numpy(int)[mask];edge=space['pt'](y[y==1],f[y==1]);assert edge['PT_status']=='PT not defined for constant actual direction' and np.isnan(edge['PT_statistic'])
pd.DataFrame(diagnostics).to_csv(OUT/'pt_test_diagnostics.csv',index=False)
for key in ['input_sha256','protected_original_artifact_sha256']:
 for name,digest in manifest[key].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
required=['selected_primary_configs.csv','pt_seed_level_results.csv','pt_architecture_summary.csv','pt_lnn_majority_results.csv','pt_holm_adjusted_results.csv','pt_nonoverlap_results.csv','methodology_notes.md','results_report.md','analysis_manifest.json','manuscript_pt_table.csv','manuscript_lnn_pt_table.csv']
assert all((OUT/name).is_file() for name in required)
# Required dependence caveat must be present on every manuscript-facing CSV table.
for name in ['manuscript_pt_table.csv','manuscript_lnn_pt_table.csv']:
 f=pd.read_csv(OUT/name);assert f.Dependence_note.str.contains('adjacent H=20 labels overlap substantially',regex=False).all()
manifest.update(status='validated',script_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.py')},protocol_sha256=hashlib.sha256((OUT/'pt_protocol.json').read_bytes()).hexdigest());(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
check={'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'seed_tests':75,'primary_majority_tests':15,'LNN_supplemental_majority_tests':5,'nonoverlap_LNN_tests':5,'Nikkei_High_N':117,'no_training':True,'no_threshold_tuning':True,'no_feature_target_or_selection_changes':True,'no_HMM_refit':True,'prediction_and_all_original_tracked_artifact_hashes_unchanged':True,'validation_loss_rule_verified':True,'majority_3_of_5_verified':True,'strict_probability_greater_than_threshold_verified':True,'nonoverlap_phase':0,'nonoverlap_step':20,'phase_search':False,'Nikkei_High_loss':'MILD_WCE','authoritative_rugarch_formula_checked':True,'independent_Pearson_identity_checked':True,'independent_Holm_families_checked':True,'constant_forecast_case_count_including_benchmark_High_context':constant,'undefined_seed_tests':int(seed.PT_statistic.isna().sum()),'undefined_majority_tests':int(major.PT_statistic.isna().sum()),'constant_forecast_NA_handling_verified':True,'actual_constant_edge_handling_verified':True,'checked_actual_frozen_cases':len(cases)}
(OUT/'completion_check.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check,indent=2))
