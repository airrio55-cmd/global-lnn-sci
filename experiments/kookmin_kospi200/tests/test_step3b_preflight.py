"""Expansion preflight: no neural fit and no independent Test input."""
from pathlib import Path
import sys,json,hashlib,copy,tempfile,unittest
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R))
from runtime.step3b_worker import validate_scope,sha
from kospi200.rolling_pilot_data import read_origin_prefix
class ExpansionPreflight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'configs/step3b_pilot_config.json').read_text());cls.a=json.loads((R/'provenance/step3b_pilot_authorization.json').read_text());cls.g=json.loads((R/'manifests/step3b_preflight.json').read_text())
 def verify(self,c=None,a=None,g=None,j=None):return validate_scope(c or self.c,a or self.a,g or self.g,j or self.g['jobs'][0],sha(R/'configs/step3b_pilot_config.json'),sha(R/'runtime/step3b_worker.py'),sha(R/'manifests/step3b_preflight.json'))
 def test_01_scope_gates_and30identity_plan(self):self.assertTrue(self.verify());self.assertEqual(len(self.g['jobs']),30);self.assertEqual(len(self.g['reused_STEP3A']),10);self.assertTrue(all(x['status']=='PASS' for x in self.g['gates']))
 def test_02_old10_never_trainable(self):
  for row in self.g['reused_STEP3A']:
   fake={k:row[k] for k in ['run_id','origin','seed','candidate','model']}
   with self.assertRaises(ValueError):self.verify(j=fake)
 def test_03_scope_expansion_denied(self):
  for k,v in [('max_new_fits',31),('seeds',[2,12,22]),('origins',['O1','O2','O3']),('independent_Test_access',True),('training_enabled',True),('gpu_enabled',True)]:
   c=copy.deepcopy(self.c);c[k]=v
   with self.assertRaises(ValueError):self.verify(c=c)
 def test_04_approval_hash_and_gate_failure_denied(self):
  for k in ['config_sha256','worker_sha256','preflight_sha256']:
   a=copy.deepcopy(self.a);a[k]='bad'
   with self.assertRaises(ValueError):self.verify(a=a)
  g=copy.deepcopy(self.g);g['gates'][0]['status']='FAIL'
  with self.assertRaises(ValueError):self.verify(g=g)
 def test_05_old_hashes_match(self):
  for row in self.g['preserved_hash_checks']:self.assertEqual(sha(R/row['file']),row['sha256'])
 def test_06_all_frozen_implementation_hashes(self):
  for row in self.c['implementation_artifacts']:self.assertEqual(sha(R/row['file']),row['sha256'])
 def test_07_staging_shapes_cutoffs_and_support(self):
  for origin,expected in [('O1',2387),('O2',2635)]:
   for p in ['A','B']:
    i=self.g['datasets'][origin][p];m=i['metadata'];self.assertEqual(m['train_samples'],expected);self.assertEqual(m['validation_samples'],228);self.assertEqual(m['train_purged'],20);self.assertEqual(m['validation_unknown_excluded'],20);self.assertEqual(m['train_cutoff_violations'],0);self.assertEqual(m['validation_future_endpoint_violations'],0);self.assertLess(m['scaler']['fit_end'],m['validation_boundary_start']);self.assertLessEqual(m['price_end'],f"{i['validation_year']}-12-31")
    with np.load(R/i['array_file'],allow_pickle=False) as z:self.assertEqual(z['train_x'].shape,(expected,20,2));self.assertEqual(z['validation_x'].shape,(228,20,2));self.assertEqual(z['train_x'].dtype,np.float32)
 def test_08_O1_array_identity_STEP3A(self):
  old=json.loads((R/'manifests/step3a_preflight.json').read_text())
  for p in ['A','B']:self.assertEqual(self.g['datasets']['O1'][p]['array_sha256'],old['datasets'][p]['array_sha256'])
 def test_09_prefix_does_not_read_next_year(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'fixture.csv';p.write_text('Date,Close\n2021-12-29,1\n2021-12-30,2\n2022-01-03,FORBIDDEN\n2026-01-02,FORBIDDEN\n');out=read_origin_prefix(p,pd.to_datetime(['2021-12-29','2021-12-30']),2021);self.assertEqual(len(out),2)
 def test_10_manual_train_reference_fixed_before_training(self):
  for origin in ['O1','O2']:
   for p in ['A','B']:
    m=self.g['datasets'][origin][p]['metadata'];r=m['manual_reference'];self.assertEqual(r['partition'],'train');self.assertEqual(r['quantiles'],[30,70]);self.assertLess(r['train_end'],m['validation_boundary_start']);self.assertEqual(sum(s['n'] for s in m['manual_validation_support']),228)
 def test_11_same_A_B_dates_and_original_settings(self):
  old=json.loads((R/'configs/step3a_pilot_config.json').read_text());self.assertEqual(self.c['model_settings'],old['model_settings']);self.assertEqual(self.c['model_seed_offsets'],old['model_seed_offsets'])
  for origin in ['O1','O2']:self.assertEqual(self.g['datasets'][origin]['A']['date_information_sha256'],self.g['datasets'][origin]['B']['date_information_sha256'])
 def test_12_no_PIT_promotion_or_production_enable(self):
  b=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(b['training_enabled']);self.assertFalse(b['hmm_fit_enabled']);self.assertEqual(self.c['source_status'],'BOTH_UNVERIFIED');self.assertEqual(self.c['production_PIT_status'],'BLOCKED');self.assertEqual(self.c['scheduling']['maximum_concurrent_LTC'],1)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExpansionPreflight));(R/'manifests/step3b_preflight_tests.json').write_text(json.dumps({'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors),'scope':'preflight data/source/authorization only; no model fitting'},indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
