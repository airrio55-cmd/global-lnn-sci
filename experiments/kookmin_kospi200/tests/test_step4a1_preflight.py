"""O3 authorization/data/static checks only. Never imports a model or loads weights."""
from pathlib import Path
import unittest,sys,json,hashlib,copy,tempfile
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.o3_pilot_scope import require_scope,planned_jobs
from kospi200.master_data import read_origin_prefix
from kospi200.data import BlockedError,local_features
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
class O3Preflight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'configs/step4a1_o3_pilot_config.json').read_text());cls.g=json.loads((R/'manifests/step4a1_preflight.json').read_text());cls.a=json.loads((R/'provenance/step4a1_o3_authorization.json').read_text())
 def test_01_exact_scope_and_valid_authorization(self):self.assertTrue(require_scope(self.c,self.a,self.g,self.g['jobs'][0],sha(R/'configs/step4a1_o3_pilot_config.json'),sha(R/'runtime/step4a1_worker.py'),sha(R/'manifests/step4a1_preflight.json')))
 def test_02_reject_extra_origin_seed_or_budget(self):
  for key,value in [('origins',['O3','O4']),('seeds',[2,12,22]),('max_new_fits',21),('gpu_enabled',True)]:
   c=copy.deepcopy(self.c);c[key]=value
   with self.assertRaises(BlockedError):require_scope(c,self.a,self.g,self.g['jobs'][0],'','','')
 def test_03_master_flags_and_sha_unchanged(self):
  p=R/'configs/step3c_master_experiment_config.json';m=json.loads(p.read_text());self.assertEqual(sha(p),self.c['master_config_sha256']);self.assertTrue(all(m[k] is False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']))
 def test_04_old40_160_hashes_preserved(self):
  self.assertEqual(len(self.g['old40_preserved_hashes']),160)
  for x in self.g['old40_preserved_hashes']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_05_fixed_original_source_and_learning_kernel(self):
  old=(R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1];new=(R/'runtime/step4a1_worker.py').read_text().split(' def equal(x,y):',1)[1];self.assertEqual(old,new);self.assertEqual(hashlib.sha256(new.encode()).hexdigest(),self.c['learning_kernel_sha256'])
  for x in self.c['implementation_artifacts']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_06_only20_unique_new_O3(self):self.assertEqual(self.g['jobs'],planned_jobs());self.assertEqual(len({x['run_id'] for x in self.g['jobs']}),20);self.assertEqual(set(self.g['datasets']),{'O3'})
 def test_07_boundaries_samples_purge_and_unknown(self):
  for x in self.g['datasets']['O3'].values():
   m=x['metadata'];self.assertEqual((m['train_samples'],m['validation_samples']),(2883,226));self.assertEqual(m['train_purged'],20);self.assertEqual(m['validation_unknown_excluded'],20);self.assertEqual(m['train_last_sample'],'2021-12-02');self.assertEqual(m['validation_last_sample'],'2022-12-01');self.assertLess(m['train_max_label_end'],m['validation_boundary_start']);self.assertEqual(m['validation_future_endpoint_violations'],0)
 def test_08_arrays_finite_shapes_and_train_only_scaler(self):
  for d in self.g['datasets']['O3'].values():
   self.assertLess(d['metadata']['scaler']['fit_end'],'2022-01-03');self.assertEqual(d['metadata']['feature_order'],['Log_Ret','Disparity'])
   with np.load(R/d['array_file'],allow_pickle=False) as z:self.assertEqual(z['train_x'].shape,(2883,20,2));self.assertEqual(z['validation_x'].shape,(226,20,2));self.assertTrue(np.isfinite(z['train_x']).all());self.assertTrue(np.isfinite(z['validation_x']).all());self.assertEqual(z['train_x'].dtype,np.float32)
 def test_09_no_future_prefix_read_and_perturbation(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'sentinel.csv';p.write_text('Date,Close\n2022-12-28,1\n2022-12-29,2\n2023-01-02,FORBIDDEN\n2026-01-02,FORBIDDEN\n');self.assertEqual(len(read_origin_prefix(p,pd.to_datetime(['2022-12-28','2022-12-29']),2022)),2)
  for d in self.g['datasets']['O3'].values():
   p=pd.read_csv(R/d['price_file'],float_precision='round_trip');s=pd.Series(p.Close.to_numpy(),index=pd.to_datetime(p.Date));cut=pd.Timestamp('2022-06-30');b=s.copy();b.loc[b.index>cut]*=1.2;self.assertTrue(local_features(s).loc[:cut].equals(local_features(b).loc[:cut]))
 def test_10_manual_train_only_reference_and_support(self):
  for d in self.g['datasets']['O3'].values():
   m=d['metadata'];ref=m['manual_reference'];self.assertEqual(ref['partition'],'train');self.assertEqual(ref['quantiles'],[30,70]);self.assertLess(ref['train_end'],'2022-01-03');self.assertEqual(sum(x['n'] for x in m['manual_validation_support']),226)
 def test_11_environment_resource_and_no_model_imports(self):self.assertEqual(Path('/sys/fs/cgroup/cpu.max').read_text().strip(),self.c['resources_current']['cpu_max']);self.assertEqual(int(Path('/sys/fs/cgroup/memory.max').read_text()),8589934592);self.assertNotIn('torch',sys.modules);self.assertNotIn('hmmlearn',sys.modules)
 def test_12_settings_match_master(self):
  master=json.loads((R/'configs/step3c_master_experiment_config.json').read_text());self.assertEqual(master['model_settings'],self.c['model_settings']);self.assertEqual(master['model_seed_offsets'],self.c['model_seed_offsets']);self.assertEqual(self.c['source_status'],'BOTH_UNVERIFIED');self.assertFalse(self.c['master460_execution_authorized'])
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(O3Preflight));fail={x._testMethodName:y for x,y in r.failures+r.errors};names=sorted(x for x in dir(O3Preflight) if x.startswith('test_'));(R/'manifests/step4a1_preflight_tests.json').write_text(json.dumps({'passed':r.testsRun-len(fail),'failed':len(fail),'tests':[{'id':n,'status':'FAIL' if n in fail else 'PASS',**({'error':fail[n]} if n in fail else {})} for n in names]},indent=2)+'\n');sys.exit(0 if r.wasSuccessful() else 1)
