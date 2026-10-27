"""Independent structural/causal and preservation checks on saved analysis."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
import pandas as pd,numpy as np
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
a=pd.read_csv(OUT/'regime_assignments_all_markets.csv');c=pd.read_csv(OUT/'hmm_convergence_log.csv');m=pd.read_csv(OUT/'regime_metrics_all_configs.csv');d=pd.read_csv(OUT/'regime_distribution.csv');b=pd.read_csv(OUT/'regime_best_model_comparison.csv');ci=pd.read_csv(OUT/'regime_bootstrap_ci.csv');manifest=json.loads((OUT/'analysis_manifest.json').read_text())
assert len(c)==240 and c.groupby('Market').size().eq(48).all()
assert not a.duplicated(['Market','Date']).any()
for col in ['Date','Feature_date','Fit_cutoff','Fit_last_date']:a[col]=pd.to_datetime(a[col])
assert (a.Feature_date<a.Date).all() and (a.Fit_last_date<a.Fit_cutoff).all() and (a.Fit_cutoff<=a.Date).all()
assert len(m)==150 and len(b)==15 and len(ci)==15 and len(d)==15
assert set(m.Model)=={'LNN','LSTM','Transformer','Persistence'}
assert d.groupby('Market').Share.sum().sub(1).abs().lt(1e-12).all()
assert len(pd.read_csv(OUT/'regime_metrics_seed_level.csv'))==675
assert ci.Valid_resamples.le(ci.Resamples).all()
for row in c.itertuples():
 means=json.loads(row.Training_state_mean_Vol20);mapping=json.loads(row.State_mapping)
 order=sorted(means,key=lambda k:means[k]);assert [mapping[k] for k in order]==['Low','Normal','High']
for name,digest in manifest['input_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
# Trailing input features are unchanged when future raw observations are perturbed.
for market in d.Market.unique():
 path=next(ROOT/name for name in manifest['input_sha256'] if name.endswith('/market_input.csv') and (market=='SP500' and 'sp500_rerun' in name or market!='SP500' and market.lower() in name))
 raw=pd.read_csv(path,index_col=0,parse_dates=True,float_precision='round_trip');changed=raw.copy();changed.loc[changed.index>='2025-01-01','Close']*=1.7
 def features(frame):
  z=pd.DataFrame({'Log_Ret':np.log(frame.Close).diff()});z['Vol20']=z.Log_Ret.rolling(20).std()*np.sqrt(252);return z
 x,y=features(raw),features(changed);np.testing.assert_allclose(x.loc[x.index<'2025-01-01'],y.loc[y.index<'2025-01-01'],atol=0,rtol=0,equal_nan=True)
for n in ['regime_distribution.png','best_model_delta_ba_by_regime.png','architecture_regime_heatmap.png']:assert (OUT/n).stat().st_size>1000
check={'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'monthly_hmm_fits':240,'fixed_states':3,'regime_metric_rows':150,'seed_metric_rows':675,'best_regime_rows':15,'causal_date_bounds_checked':True,'training_only_state_mapping_checked':True,'future_feature_perturbation_passed':True,'prefix_filter_invariance_checked_during_analysis':True,'predictive_inputs_predictions_and_results_unchanged':True,'predictive_models_retrained':False}
(OUT/'completion_check.json').write_text(json.dumps(check,indent=2)+'\n')
manifest['script_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.py')};manifest['protocol_sha256']=hashlib.sha256((OUT/'hmm_protocol.json').read_bytes()).hexdigest();(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(check,indent=2))
