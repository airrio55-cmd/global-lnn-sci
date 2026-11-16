"""STEP2.5 evidence and array-only checks; no model imports or execution."""
from pathlib import Path
import unittest,json,hashlib,sys
import pandas as pd,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.data import Calendar,labels_on_calendar,BlockedError
from kospi200.tau import time_constants,REFERENCE_SHA
class Step25Tests(unittest.TestCase):
 def test_01_official_sessions_and_calendar_hash(self):
  p=R/'provenance/krx_calendar_provenance.json';d=json.loads(p.read_text());s=pd.read_csv(R/'manifests/krx_sessions_2010_2025.csv',parse_dates=['Date'])
  self.assertEqual(len(s),3939);self.assertEqual(len(d['annual']),16);self.assertTrue(s.Date.is_unique)
  self.assertTrue((s.Date.dt.weekday<5).all());self.assertTrue(s.Date.between('2010-01-01','2025-12-31').all())
  self.assertEqual(hashlib.sha256((R/'manifests/krx_sessions_2010_2025.csv').read_bytes()).hexdigest(),d['session_csv_sha256'])
 def test_02_all45_dates_open_but_no_fabricated_closes(self):
  d=pd.read_csv(R/'manifests/kospi_missing_dates_audit.csv');self.assertEqual(len(d),45);self.assertTrue(d.krx_open.eq('YES').all());self.assertTrue(d.official_close.isna().all());self.assertTrue(d.official_close_exists.eq('UNKNOWN').all())
  self.assertEqual(len(pd.read_csv(R/'manifests/kospi_official_close_supplement.csv')),0)
 def test_03_real_session20_offsets_and_tail(self):
  s=pd.DatetimeIndex(pd.read_csv(R/'manifests/krx_sessions_2010_2025.csv').Date)
  k=pd.read_csv(R/'originals/KOSPI_200.csv',parse_dates=['Date']).set_index('Date')
  p=R/'manifests/krx_sessions_2010_2025.csv';cal=Calendar(s,'official KRX',hashlib.sha256(p.read_bytes()).hexdigest(),True)
  l=labels_on_calendar(k['종가'],cal)
  self.assertTrue(l.Target.tail(20).isna().all());self.assertEqual(str(l.index[-21].date()),'2025-12-01')
  self.assertEqual(str(l.label_end.iloc[-21].date()),'2025-12-30')
  ids={d:i for i,d in enumerate(s)}
  self.assertTrue(all(ids[end]-ids[t]==20 for t,end in l.label_end.dropna().items()))
 def test_04_original_hashes_unchanged(self):
  for item in json.loads((R/'evidence/input_manifest.json').read_text()):self.assertEqual(hashlib.sha256((R/'originals'/item['filename']).read_bytes()).hexdigest(),item['sha256'])
 def test_05_actual_origin_boundaries_and_blocked_counts(self):
  m=pd.read_csv(R/'manifests/rolling_origin_manifest.csv');self.assertEqual(len(m),15);self.assertTrue(m.confirmed_samples.isna().all());self.assertTrue(m.status.eq('BLOCKED').all())
  row=m[(m.origin=='O2')&(m.partition=='test')].iloc[0];self.assertEqual(row.official_boundary_start,'2022-01-03')
 def test_06_64_dst_clock_rules(self):
  d=pd.read_csv(R/'manifests/us_dst_transition_checks.csv');self.assertEqual(len(d),64);self.assertEqual(d.year.nunique(),16)
  for _,g in d.groupby(['year','transition']):
   g=g.sort_values('clock_probe_date');hours=[pd.Timestamp(t).hour for t in g.close_kst]
   self.assertEqual(hours,[6,5] if g.transition.iloc[0]=='START' else [5,6])
 def test_07_early_closes_and_no_2026_schedule(self):
  s=pd.read_csv(R/'manifests/us_official_schedule_2021_2025.csv');self.assertTrue(pd.to_datetime(s.source_date).between('2021-01-01','2025-12-31').all())
  early=s[s.kind=='EARLY_CLOSE'];self.assertEqual(len(early),10);self.assertTrue(early.close_et.map(lambda t:pd.Timestamp(t).hour==13).all())
  self.assertFalse(s.loc[s.source_date=='2025-01-09','is_open'].iloc[0])
 def test_08_future_schedule_perturbation_does_not_change_past_candidates(self):
  s=pd.read_csv(R/'manifests/us_official_schedule_2021_2025.csv');s=s[s.is_open].copy();s['close_utc']=pd.to_datetime(s.close_utc,utc=True)
  decisions=pd.DataFrame({'decision_at':pd.to_datetime(['2024-03-08T09:00Z','2024-03-11T09:00Z'])})
  def join(x):return pd.merge_asof(decisions,x[['source_date','close_utc']].sort_values('close_utc'),left_on='decision_at',right_on='close_utc',direction='backward')
  original=join(s);changed=s[s.close_utc<=pd.Timestamp('2024-03-11T09:00Z')];pd.testing.assert_frame_equal(original,join(changed))
  # This tests market-close candidates only. Provider-PIT cannot be verified without release data.
  real=pd.read_csv(R/'manifests/us_market_availability_audit.csv');self.assertTrue(real.provider_available_at.isna().all());self.assertTrue(real.production_PIT_date.isna().all())
 def test_09_gate_safety_foreign_and_no_run_flags(self):
  g=json.loads((R/'manifests/step25_gate_results.json').read_text());self.assertEqual(g['gate_results'][0]['status'],'PASS');self.assertFalse(g['STEP3_smoke_ready'])
  c=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(c['training_enabled']);self.assertFalse(c['hmm_fit_enabled'])
  f=json.loads((R/'manifests/foreign_net_provenance.json').read_text());self.assertFalse(f['same_day_input_allowed']);self.assertIsNone(f['first_publication_at'])
 def test_10_processed_recipe_not_claimed_as_provenance(self):
  d=json.loads((R/'provenance/processed_formula_verification.json').read_text());self.assertEqual(len(d['formulas']),9);self.assertTrue(all(x['matched_rows']==3854 for x in d['formulas']));self.assertFalse(d['generation_code_found']);self.assertFalse(d['used_in_default_experiment'])
 def test_11_ltc_reference_and_explicit_constraint_mode(self):
  d=json.loads((R/'provenance/ltc_version_verification.json').read_text());self.assertTrue(d['reference_cell_matches_ncps_1_0_1_bytewise']);self.assertTrue(d['reference_wrapper_matches_ncps_1_0_1_bytewise']);self.assertTrue(d['wrapper_default_implicit_constraints']);self.assertFalse(d['cell_direct_default_implicit_constraints']);self.assertEqual(d['ode_unfolds_default'],6)
  with self.assertRaisesRegex(BlockedError,'Explicit LTC wrapper/cell'):time_constants([[0]],[[0]],{},dt_unit='fixture',source_commit=REFERENCE_SHA)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Step25Tests);result=unittest.TextTestRunner(verbosity=2).run(suite)
 (R/'manifests/step25_test_results.json').write_text(json.dumps({'scope':'evidence/data/clock/numeric snapshot checks only','passed':result.testsRun-len(result.errors)-len(result.failures),'failed':len(result.errors)+len(result.failures),'market_close_candidate_perturbation':'PASS' if result.wasSuccessful() else 'FAIL','provider_PIT_real_data_perturbation':'BLOCKED_RELEASE_TIMESTAMPS_UNKNOWN'},indent=2)+'\n')
 sys.exit(0 if result.wasSuccessful() else 1)
