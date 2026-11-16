"""STEP2.7 real-data audit checks and synthetic regime contracts; no models."""
from pathlib import Path
import sys,json,unittest,hashlib,ast
import pandas as pd,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.data import BlockedError,local_features
from kospi200.manual_evaluation import freeze_manual_reference,assign_manual_regimes,supplied_prediction_metrics,regime_metric_table
from kospi200.smoke_preparation import static_parameter_count,smoke_plan,extract_original_definitions
class Step27Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.audit=json.loads((R/'manifests/step27_data_validation.json').read_text());cls.c=json.loads((R/'configs/experiment_config.json').read_text())
 def test_01_full_excel_identity_and_quality(self):
  p=R/'data/user_supplied/KOSPI 200 종가.xlsx';self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),self.audit['full_excel_sha256']);self.assertEqual(self.audit['full_excel_sha256'],'13e34b707d64585fb2f94a828cd387fb89956ae935e27b4ccc9c02e2a2fbdd21')
  self.assertEqual(self.audit['full_excel_quality']['in_period_rows'],3939);self.assertTrue(self.audit['full_calendar_exact_match'])
 def test_02_all_three_price_comparisons(self):
  c=self.audit['comparison'];self.assertEqual([c[k] for k in ['common_dates','exact_matches','within_1e_minus9_matches','rounded_2dp_matches']],[3894,144,144,3892]);self.assertEqual(c['rounded_2dp_conflict_dates'],['2021-04-23','2021-05-06'])
 def test_03_conflicts_redacted_and_no_finalization(self):
  d=pd.read_csv(R/'manifests/step27_price_conflicts.csv');self.assertEqual(len(d),3750)
  for k in ['Close_original','Close_excel','difference']:self.assertNotIn(k,d.columns)
  self.assertIsNone(self.audit['confirmed_final_samples']);self.assertTrue(self.audit['final_data_status'].startswith('BLOCKED'))
 def test_04_exact45_and_horizon47_causes(self):
  self.assertEqual(self.audit['supplement_45_exact_matches_full_excel'],45);d=self.audit['label_change_cause'];self.assertTrue(d['all_have_different_horizon_end']);self.assertEqual([d[k] for k in ['changes','down_to_up','up_to_down','original_common_prices_modified']],[47,21,26,0])
 def test_05_origins_purge_window_and_class_counts(self):
  d=pd.read_csv(R/'manifests/step27_origin_manifest.csv');self.assertEqual(len(d),15);self.assertTrue(d.window_future_or_length_violations.eq(0).all());self.assertTrue(d.label_end_cutoff_violations.eq(0).all());self.assertTrue(d.final_confirmed_samples.isna().all());self.assertTrue(d[d.partition!='test'].purged_labels.eq(20).all());self.assertTrue(d.provisional_structural_samples.eq(d.up_samples+d.down_or_equal_samples).all())
 def test_06_tail_and_no_2026(self):
  s=self.audit['provisional_label_audit'];self.assertEqual(s['new_known']['known'],3919);self.assertEqual(s['new_unknown'],20);self.assertEqual(s['last_valid_base'],'2025-12-01');self.assertEqual(self.audit['2026_prices_used'],0)
 def test_07_frozen_train_quantiles_and_future_perturbation(self):
  dates=pd.bdate_range('2019-01-02',periods=100);v=pd.Series(np.arange(100,dtype=float),index=dates);train=dates[:40];ref=freeze_manual_reference(v,train,validation_start=dates[40],partition='train');a=assign_manual_regimes(v,ref);v.iloc[60:]*=100;new=freeze_manual_reference(v,train,validation_start=dates[40],partition='train');self.assertEqual(ref,new);pd.testing.assert_series_equal(a.iloc[:60],assign_manual_regimes(v,new).iloc[:60])
 def test_08_test_thresholds_and_collapsed_quantiles_rejected(self):
  idx=pd.bdate_range('2020-01-02',periods=50);v=pd.Series(1.,index=idx)
  with self.assertRaises(BlockedError):freeze_manual_reference(v,idx[:20],validation_start=idx[20],partition='test')
  with self.assertRaises(BlockedError):freeze_manual_reference(v,idx[:20],validation_start=idx[20],partition='train')
  with self.assertRaises(BlockedError):freeze_manual_reference(v,idx[:30],validation_start=idx[20],partition='train')
 def test_09_manual_boundary_membership_disjoint(self):
  idx=pd.bdate_range('2020-01-02',periods=5);v=pd.Series([0.,1.,2.,3.,4.],index=idx);ref={'partition':'train','low':1.,'high':3.,'train_end':'2019-12-30','validation_start':'2020-01-02'};self.assertEqual(assign_manual_regimes(v,ref).tolist(),['Low_Vol','Low_Vol','Mid_Vol','High_Vol','High_Vol'])
 def test_10_single_class_empty_and_binary_metrics(self):
  for y,p in [([],[]),([1,1],[1,0]),([0,0],[0,1])]:
   d=supplied_prediction_metrics(y,p);self.assertIsNone(d['balanced_accuracy']);self.assertIsNone(d['macro_f1']);self.assertEqual(d['n'],len(y))
  d=supplied_prediction_metrics([0,0,1,1],[0,1,1,1]);self.assertEqual(d['balanced_accuracy'],.75);self.assertAlmostEqual(d['macro_f1'],(.6666666666666666+.8)/2)
  with self.assertRaises(BlockedError):supplied_prediction_metrics([0,np.nan],[0,1])
 def test_11_seed_replication_does_not_pool_and_hmm_separate(self):
  d=pd.DataFrame([dict(origin='O1',seed=s,model='RNN',date='2021-01-04',regime='Low_Vol',y_true=1,y_pred=1) for s in [2,12]])
  t=regime_metric_table(d,regime_type='manual');self.assertEqual(t.n.max(),1);self.assertEqual(len(t),6)
  with self.assertRaises(BlockedError):regime_metric_table(d,regime_type='hmm')
  with self.assertRaises(BlockedError):regime_metric_table(pd.concat([d,d]),regime_type='manual')
 def test_12_historical_outputs_not_fabricated(self):
  d=pd.read_csv(R/'manifests/step27_historical_manual_metrics.csv');self.assertEqual(len(d),99);self.assertTrue(d.status.eq('HISTORICAL_STORED_OUTPUT_ONLY').all());p=pd.read_csv(R/'manifests/step27_historical_manual_per_seed.csv');self.assertEqual(len(p),528);self.assertEqual(p.balanced_accuracy.isna().sum(),495);self.assertEqual(len(pd.read_csv(R/'manifests/step27_historical_hmm_metrics.csv')),66)
 def test_13_source_definitions_preserved_as_text(self):
  p=next((R/'originals').glob('*10개*.ipynb'));d=extract_original_definitions(json.loads(p.read_text()));self.assertIn('out[:, -1, :]',d['LNNModel']['source']);self.assertIn('self.ltc = LTC(input_size, h, batch_first=True)',d['LNNModel']['source']);self.assertIn('optimizer = torch.optim.AdamW',d['train_model']['source'])
 def test_14_static_parameter_counts_not_runtime_claims(self):
  self.assertEqual(static_parameter_count('RNN',5)['trainable'],17538);self.assertEqual(static_parameter_count('LSTM',2)['trainable'],67842);self.assertEqual(static_parameter_count('LTC',2)['nontrainable_registered'],16640);self.assertFalse(static_parameter_count('CfC',2)['runtime_verified'])
 def test_15_smoke_fails_closed_and_hyperparameters_frozen(self):
  p=smoke_plan(self.c,{});self.assertFalse(p['executable']);self.assertEqual(len(p['unmet_gates']),7);self.assertEqual(p['model_settings'],self.c['model']);self.assertFalse(p['gpu_enabled']);self.assertFalse(p['training_enabled'])
 def test_16_no_model_execution_calls_or_imports_in_new_modules(self):
  for f in ['src/kospi200/manual_evaluation.py','src/kospi200/smoke_preparation.py','tools/step27_audit.py']:
   t=ast.parse((R/f).read_text())
   for n in ast.walk(t):
    if isinstance(n,(ast.Import,ast.ImportFrom)):
     names=[n.module] if isinstance(n,ast.ImportFrom) else [a.name for a in n.names]
     self.assertFalse(any(x and x.split('.')[0] in ['torch','ncps','hmmlearn'] for x in names))
    if isinstance(n,ast.Call):self.assertNotIn(ast.unparse(n.func),['exec','eval','torch.load','GaussianHMM','LTC','CfC'])
 def test_17_protocol_freeze_and_prior_artifacts(self):
  d=json.loads((R/'manifests/step27_protocol_freeze.json').read_text())
  for a in d['artifacts']:self.assertEqual(hashlib.sha256((R/a['file']).read_bytes()).hexdigest(),a['sha256'])
  p=json.loads((R/'provenance/step27_preservation.json').read_text());self.assertTrue(p['all_unchanged'])
  for a in p['prior_artifacts']:self.assertEqual(hashlib.sha256((R/a['file']).read_bytes()).hexdigest(),a['before_sha256'])
 def test_18_domestic_feature_prefix_invariance(self):
  c=pd.read_csv(R/'data/derived/kospi200_close_completed_2010_2025.csv',parse_dates=['Date']).set_index('Date').Close;cut=pd.Timestamp('2021-12-30');v=c.copy();v.loc[v.index>cut]*=10;pd.testing.assert_frame_equal(local_features(c).loc[:cut],local_features(v).loc[:cut]);self.assertEqual(self.audit['F1_input_only_provisional_known_windows'],3881)

 def test_19_isolated_install_import_not_original_runtime_proof(self):
  d=json.loads((R/'provenance/step27_isolated_environment.json').read_text());self.assertEqual(d['versions']['torch'],'2.10.0+cpu');self.assertEqual(d['versions']['ncps'],'1.0.1');self.assertEqual(d['versions']['hmmlearn'],'0.3.3');self.assertTrue(d['wrapper_implicit_param_constraints']);self.assertFalse(d['model_constructed']);self.assertFalse(d['hmm_fit']);self.assertFalse(d['original_ncps_hmmlearn_version_verified'])
