"""Price/label integrity tests, never model scoring or training."""
from pathlib import Path
import sys,json,unittest,hashlib
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.data import Calendar,labels_on_calendar,local_features,BlockedError
from kospi200.reconciliation import validate_prices,reconcile_close,full_excel_comparison,build_labels_features
from kospi200.folds import rolling_origins

class Step26Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.audit=json.loads((R/'manifests/step26_cutoff_label_audit.json').read_text())
  cls.original=pd.read_csv(R/'originals/KOSPI_200.csv',parse_dates=['Date'],float_precision='round_trip').rename(columns={'종가':'Close'})[['Date','Close']]
  cls.completed=pd.read_csv(R/'data/derived/kospi200_close_completed_2010_2025.csv',parse_dates=['Date'],float_precision='round_trip')
  p=R/'manifests/krx_sessions_2010_2025.csv';s=pd.DatetimeIndex(pd.read_csv(p,parse_dates=['Date']).Date,name='Date')
  cls.cal=Calendar(s,'official KRX cash sessions',hashlib.sha256(p.read_bytes()).hexdigest(),True)
  cls.label,cls.features,cls.window=build_labels_features(cls.completed,cls.cal)
 def test_01_exact45_and_csv_xlsx_single_count(self):
  m=pd.read_csv(R/'manifests/kospi_supplement_45_audit.csv',parse_dates=['Date']);expected=pd.read_csv(R/'manifests/kospi_missing_dates_audit.csv',parse_dates=['date'])
  self.assertEqual(set(m.Date),set(expected.date));self.assertEqual(len(m),45);self.assertTrue(m.included_once.all());self.assertTrue(m.csv_xlsx_price_match.all());self.assertEqual(self.completed.original_or_supplement.eq('supplement').sum(),45)
 def test_02_3939_official_sessions_and_no_close_gaps(self):
  self.assertEqual(len(self.completed),3939);self.assertTrue(pd.DatetimeIndex(self.completed.Date).equals(self.cal.sessions));self.assertTrue(np.isfinite(self.completed.Close).all());self.assertTrue(self.completed.Close.gt(0).all());self.assertTrue(self.completed.Date.is_unique)
 def test_03_original3894_prices_preserved_exactly(self):
  a=validate_prices(self.original)[0].set_index('Date').Close;b=self.completed.set_index('Date').Close.reindex(a.index)
  np.testing.assert_array_equal(a.to_numpy(),b.to_numpy());self.assertEqual(len(a),3894)
 def test_04_full_excel_unavailable_is_blocked_not_equal(self):
  # The missing actual input is reported as BLOCKED, never a false successful comparison.
  m=full_excel_comparison(self.original,None,calendar=self.cal)
  self.assertEqual(len(m),3894);self.assertTrue(m.status.eq('BLOCKED_FULL_EXCEL_MISSING').all());self.assertTrue(m.exact_match.isna().all())
 def test_19_full_workbook_complete_and_45_prices_match(self):
  d=self.audit['full_excel_validation'];self.assertEqual(self.audit['full_excel_common_comparisons_performed'],3894);self.assertEqual(d['supplement_45_exact_matches'],45)
  m=pd.read_csv(R/'manifests/kospi_price_reconciliation.csv');self.assertEqual(len(m),3894);self.assertFalse(m.exact_match.isna().any())
 def test_05_no_official_source_overclaim(self):
  x=self.completed.query("original_or_supplement=='supplement'")
  self.assertTrue(x.source_type.eq('USER_SUPPLIED_VERIFIED_MATCH').all());self.assertFalse(self.audit['integrity']['official_source_verified']);self.assertFalse(self.completed.source_type.eq('KRX_OFFICIAL_VERIFIED').any())
 def test_06_exact20_horizon_and_tail20_unknown(self):
  self.assertTrue((self.label.label_end_session_id-self.label.session_id).dropna().eq(20).all());self.assertTrue(self.label.Target.tail(20).isna().all());self.assertEqual(self.label.Target.notna().sum(),3919);self.assertEqual(str(self.label.index[-21].date()),'2025-12-01')
 def test_07_2026_perturbation_excluded_before_labels(self):
  raw=self.original.copy();raw.loc[raw.Date>'2025-12-31','Close']=1e30
  pd.testing.assert_frame_equal(validate_prices(raw)[0],validate_prices(self.original)[0])
  self.assertTrue(self.completed.Date.between('2010-01-01','2025-12-31').all());self.assertTrue(self.label.label_end.dropna().le(pd.Timestamp('2025-12-31')).all())
 def test_08_trailing_features_future_invariance(self):
  c=self.completed.set_index('Date').Close;changed=c.copy();cut=pd.Timestamp('2020-12-30');changed.loc[changed.index>cut]*=7
  pd.testing.assert_frame_equal(local_features(c).loc[:cut],local_features(changed).loc[:cut])
 def test_09_mature_targets_future_invariance(self):
  c=self.completed.set_index('Date').Close;changed=c.copy();cut=pd.Timestamp('2020-12-30');changed.loc[changed.index>cut]*=7
  new=labels_on_calendar(changed,self.cal);mature=self.label.label_end.le(cut)
  pd.testing.assert_series_equal(self.label.loc[mature,'Target'],new.loc[mature,'Target'])
 def test_10_price_inside_horizon_can_change_target(self):
  # Correct causality contract: a target intentionally depends on its future endpoint.
  s=pd.bdate_range('2020-01-02',periods=50);cal=Calendar(s,'SYNTHETIC_FIXTURE','a'*64,True);c=pd.Series(100.,index=s)
  a=labels_on_calendar(c,cal);c.iloc[20]=200.;b=labels_on_calendar(c,cal);self.assertEqual(a.Target.iloc[0],0);self.assertEqual(b.Target.iloc[0],1)
 def test_11_fold_purging_and_no_boundary_violations(self):
  m,sel=rolling_origins(self.label,self.cal,self.window)
  self.assertEqual(m.query("partition=='train'").purged_labels.tolist(),[20]*5);self.assertEqual(m.query("partition=='validation'").purged_labels.tolist(),[20]*5)
  for _,row in m[m.partition!='test'].iterrows():
   self.assertTrue(self.label.loc[sel[row.origin][row.partition],'label_end'].lt(pd.Timestamp(row.next_cutoff)).all())
  self.assertEqual(m.query("origin=='O5' and partition=='test'").unknown_labels.iloc[0],20)
 def test_12_features_match_notebook_definitions(self):
  c=self.completed.set_index('Date').Close;log=np.log(c/c.shift(1))
  np.testing.assert_allclose(self.features.Log_Ret,log,equal_nan=True)
  np.testing.assert_allclose(self.features.Disparity,c/c.rolling(20).mean()-1,equal_nan=True)
  np.testing.assert_allclose(self.features.Vol_Regime,log.rolling(40).std(ddof=1),equal_nan=True)
  self.assertEqual(self.features.notna().all(axis=1).sum(),3899)
 def test_13_window20_include_t_count_and_no_auto_zero_fill(self):
  self.assertEqual((self.window & self.label.Target.notna()).sum(),3860);self.assertFalse(self.window.iloc[:59].any());self.assertTrue(self.window.iloc[59]);self.assertTrue(self.features.Vol_Regime.iloc[:40].isna().all())
 def test_14_664_discrepancies_repaired_and_distribution(self):
  s=self.audit['label_audit'];self.assertEqual(s['horizon_discrepancies_before'],664);self.assertEqual(s['horizon_discrepancies_after_session_id_repair'],0);self.assertEqual(s['common_Target_changes'],47)
  self.assertEqual(s['new_known']['up']+s['new_known']['down_or_equal'],3919)
 def test_15_original8_and_supplement2_hashes(self):
  for d in json.loads((R/'evidence/input_manifest.json').read_text()):self.assertEqual(hashlib.sha256((R/'originals'/d['filename']).read_bytes()).hexdigest(),d['sha256'])
  for d in self.audit['input_files']:
   if d['exists']:self.assertEqual(hashlib.sha256((R/'data/user_supplied'/d['file']).read_bytes()).hexdigest(),d['sha256'])
 def test_16_reject_duplicate_bad_prices_and_supplement_mismatch(self):
  a=pd.DataFrame({'Date':['2020-01-02','2020-01-02'],'Close':[1.,2.]})
  with self.assertRaises(BlockedError):validate_prices(a)
  for bad in [np.nan,np.inf,0.,-1.]:
   with self.assertRaises(BlockedError):validate_prices(pd.DataFrame({'Date':['2020-01-02'],'Close':[bad]}))
  b=self.completed.query("original_or_supplement=='supplement'")[['Date','Close']].copy();x=b.copy();x.iloc[0,1]+=1
  with self.assertRaises(BlockedError):reconcile_close(self.original,b,x,calendar=self.cal,expected_missing=b.Date,original_file='fixture',supplement_file='fixture',original_sha256='a'*64,supplement_sha256='b'*64)
 def test_17_conflict_detection_does_not_replace_original(self):
  s=pd.bdate_range('2020-01-02',periods=3);cal=Calendar(s,'SYNTHETIC_FIXTURE','a'*64,True)
  a=pd.DataFrame({'Date':s[:2],'Close':[100.,101.]});original=a.copy(deep=True);b=pd.DataFrame({'Date':s,'Close':[100.01,101.,102.]})
  m=full_excel_comparison(a,b,calendar=cal);self.assertEqual(m.exact_match.eq(False).sum(),1);pd.testing.assert_frame_equal(a,original)
 def test_18_external_PIT_and_training_gates_remain_blocked(self):
  m=pd.read_csv(R/'manifests/step26_rolling_origin_manifest.csv');self.assertTrue(m.external_5feature_PIT_verified_samples.isna().all());self.assertTrue(m.execution_status.str.startswith('BLOCKED').all())
  c=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(c['training_enabled']);self.assertFalse(c['hmm_fit_enabled']);self.assertFalse(self.audit['STEP3_smoke_ready'])
if __name__=='__main__':unittest.main()
