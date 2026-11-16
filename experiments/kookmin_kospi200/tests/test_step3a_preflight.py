"""Pilot-only gate/data tests. No model creation and no Test-price read."""
from pathlib import Path
import sys,json,unittest,copy,tempfile
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R))
from kospi200.pilot_data import read_verified_o1_prefix,prepare_pilot_arrays,sha256,validation_metrics
from kospi200.data import BlockedError
from runtime.step3a_pilot import require_pilot_scope
class PilotPreflight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'configs/step3a_pilot_config.json').read_text());cls.a=json.loads((R/'provenance/step3a_pilot_authorization.json').read_text());cls.g=json.loads((R/'manifests/step3a_preflight.json').read_text())
 def verify(self,c=None,a=None,g=None):return require_pilot_scope(c or self.c,a or self.a,g or self.g,config_sha=sha256(R/'configs/step3a_pilot_config.json'),runner_sha=sha256(R/'runtime/step3a_pilot.py'),gates_sha=sha256(R/'manifests/step3a_preflight.json'))
 def test_01_all12_gates_and_approval(self):self.assertTrue(self.verify());self.assertEqual(len(self.g['gates']),12);self.assertTrue(all(r['status']=='PASS' for r in self.g['gates']))
 def test_02_no_scope_expansion(self):
  for key,value in [('origin','O2'),('max_fit_attempts',500),('test_access',True),('gpu_enabled',True),('production_gate_override',True),('training_enabled',True),('pilot_price_cutoff','2025-12-31'),('price_candidates',['B'])]:
   c=copy.deepcopy(self.c);c[key]=value
   with self.assertRaises(ValueError):self.verify(c=c)
 def test_03_any_failed_gate_stops_training(self):
  for i in range(len(self.g['gates'])):
   g=copy.deepcopy(self.g);g['gates'][i]['status']='FAIL'
   with self.assertRaises(ValueError):self.verify(g=g)
 def test_04_approval_bound_to_code_and_data(self):
  for key,value in [('config_sha256','bad'),('runner_sha256','bad'),('preflight_sha256','bad'),('scope','STEP29_SYNTHETIC_CPU_ONLY'),('permits_Test',True)]:
   a=copy.deepcopy(self.a);a[key]=value
   with self.assertRaises(ValueError):self.verify(a=a)
 def test_05_prefix_reader_does_not_parse_Test(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'fixture.csv';p.write_text('Date,Close\n2020-12-29,1\n2020-12-30,2\n2021-01-04,INVALID_MUST_NOT_PARSE\n2026-01-02,INVALID_MUST_NOT_PARSE\n')
   out=read_verified_o1_prefix(p,pd.to_datetime(['2020-12-29','2020-12-30']));self.assertEqual(out.Close.tolist(),[1.,2.])
 def test_06_real_O1_staging_horizon_mask_scaler(self):
  cal=pd.read_csv(R/self.g['calendar']['staged_file'],parse_dates=['Date']);seen=[]
  for name in ['A','B']:
   info=self.g['datasets'][name];prices=pd.read_csv(R/info['price_file'],parse_dates=['Date'],float_precision='round_trip');data,meta,dates=prepare_pilot_arrays(prices,cal,calendar_source='official KRX derived prefix',calendar_sha256=self.g['calendar']['staged_sha256'])
   self.assertEqual(data['train'][0].shape,(2387,20,2));self.assertEqual(data['validation'][0].shape,(228,20,2));self.assertEqual(meta['train_purged'],20);self.assertEqual(meta['validation_unknown_excluded'],20);self.assertEqual(meta['train_label_cutoff_violations'],0);self.assertEqual(meta['validation_future_endpoint_violations'],0);self.assertEqual(meta['scaler']['fit_rows'],2406);self.assertLess(meta['scaler']['fit_end'],'2020-01-02');self.assertLessEqual(meta['validation_max_label_end'],'2020-12-31');seen.append(dates)
  self.assertEqual(seen[0],seen[1])
 def test_07_future_staging_rows_rejected(self):
  info=self.g['datasets']['A'];prices=pd.read_csv(R/info['price_file'],parse_dates=['Date']);cal=pd.read_csv(R/self.g['calendar']['staged_file'],parse_dates=['Date']);prices.loc[len(prices)]=[pd.Timestamp('2021-01-04'),1e20]
  with self.assertRaises(BlockedError):prepare_pilot_arrays(prices,cal,calendar_source='fixture',calendar_sha256='a'*64)
 def test_08_metrics_degenerate_and_brier(self):
  m=validation_metrics([0,0,1,1],[1.,1.,1.,1.]);self.assertEqual(m['validation_BA'],.5);self.assertEqual(m['prediction_status'],'DEGENERATE_PREDICTION');self.assertEqual(m['brier'],.5);self.assertEqual(m['recall0'],0.);self.assertEqual(m['recall1'],1.)
 def test_09_production_gate_unchanged_and_unverified(self):
  b=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(b['training_enabled']);self.assertFalse(b['hmm_fit_enabled']);self.assertEqual(self.c['production_source_status'],'BOTH_UNVERIFIED');self.assertEqual(self.c['production_PIT_status'],'BLOCKED')
 def test_10_offsets_frozen_5_fits_each(self):
  b=json.loads((R/'configs/experiment_config.json').read_text());self.assertEqual(self.c['model_seed_offsets'],{m:b['seed_offsets'][m+'_RAW'] for m in b['models']});self.assertEqual(len(self.c['models'])*len(self.c['price_candidates']),10)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(PilotPreflight);result=unittest.TextTestRunner(verbosity=2).run(suite)
 (R/'manifests/step3a_preflight_tests.json').write_text(json.dumps({'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors),'scope':'O1-only data/authorization tests; no model/Test execution'},indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
