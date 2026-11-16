"""Authorized O4/O5 preflight: data/metadata only, no model import or fit."""
from pathlib import Path
import unittest,sys,json,hashlib,copy,subprocess,importlib.metadata
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R))
from kospi200.o4_o5_pilot_scope import require_scope,planned_jobs
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
class PilotPreflight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'configs/step4a2_o4_o5_pilot_config.json').read_text());cls.g=json.loads((R/'manifests/step4a2_preflight.json').read_text());cls.a=json.loads((R/'provenance/step4a2_o4_o5_authorization.json').read_text())
 def test_01_scope_authorized40(self):self.assertTrue(require_scope(self.c,self.a,self.g,self.g['jobs'][0],sha(R/'configs/step4a2_o4_o5_pilot_config.json'),sha(R/'runtime/step4a2_worker.py'),sha(R/'manifests/step4a2_preflight.json')))
 def test_02_reject_extra_origin_seed_budget_GPU(self):
  for k,v in [('origins',['O3','O4','O5']),('seeds',[2,12,22]),('max_new_fits',41),('gpu_enabled',True)]:
   c=copy.deepcopy(self.c);c[k]=v
   with self.assertRaises(ValueError):require_scope(c,self.a,self.g,self.g['jobs'][0],'','','')
 def test_03_master_original_flags_sha(self):
  p=R/'configs/step3c_master_experiment_config.json';m=json.loads(p.read_text());self.assertEqual(sha(p),self.c['master_config_sha256']);self.assertTrue(all(m[k] is False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']));self.assertEqual(self.c['model_settings'],m['model_settings'])
 def test_04_old60_outputs_arrays_scalers_history_hashes(self):
  self.assertEqual(len(self.g['reused_completed']),60);self.assertGreaterEqual(len(self.g['old60_preserved_hashes']),260)
  for x in self.g['old60_preserved_hashes']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_05_identical_learning_kernel_and_source_pins(self):
  old=(R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1];new=(R/'runtime/step4a2_worker.py').read_text().split(' def equal(x,y):',1)[1];self.assertEqual(old,new);self.assertEqual(hashlib.sha256(new.encode()).hexdigest(),self.c['learning_kernel_sha256'])
  for x in self.c['implementation_artifacts']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_06_exact40_unique_grid(self):self.assertEqual(self.g['jobs'],planned_jobs());self.assertEqual(len({x['run_id'] for x in self.g['jobs']}),40);self.assertEqual(set(self.g['datasets']),{'O4','O5'})
 def test_07_boundaries_purge_unknown(self):
  for origin,parts in self.g['datasets'].items():
   for d in parts.values():
    m=d['metadata'];self.assertEqual((m['train_samples'],m['validation_samples']),{'O4':(3129,225),'O5':(3374,224)}[origin]);self.assertEqual(m['train_purged'],20);self.assertEqual(m['validation_unknown_excluded'],20);self.assertLess(m['train_max_label_end'],m['validation_boundary_start']);self.assertEqual(m['validation_future_endpoint_violations'],0)
 def test_08_arrays_shape_feature_order_train_scaler(self):
  for parts in self.g['datasets'].values():
   for d in parts.values():
    m=d['metadata'];self.assertEqual(m['feature_order'],['Log_Ret','Disparity']);self.assertLess(m['scaler']['fit_end'],m['validation_boundary_start'])
    with np.load(R/d['array_file'],allow_pickle=False) as z:
     self.assertEqual(z['train_x'].shape,(m['train_samples'],20,2));self.assertEqual(z['validation_x'].shape,(m['validation_samples'],20,2));self.assertEqual(z['train_x'].dtype,np.float32);self.assertTrue(np.isfinite(z['train_x']).all());self.assertTrue(np.isfinite(z['validation_x']).all())
 def test_09_per_origin_access_barrier(self):
  from kospi200.master_data import read_origin_prefix
  run=R/self.c['run_directory'];source=R/self.c['source_notebook_file']
  for origin,forbidden in [('O4','O5'),('O5','O4')]:
   allowed=R/self.g['datasets'][origin]['A']['array_file'];denied=R/self.g['datasets'][forbidden]['A']['array_file']
   code="import sys;from pathlib import Path;sys.path.insert(0,"+repr(str(R))+ ");from runtime.step4a2_worker import barrier;barrier(Path("+repr(str(R))+"),Path("+repr(str(run))+"),Path("+repr(str(run/'jobs'/'preflight_only'))+"),"+repr(origin)+",Path("+repr(str(source))+"));Path("+repr(str(allowed))+").open('rb').read(1)\ntry:Path("+repr(str(denied))+").open('rb').read(1)\nexcept PermissionError:print('BLOCKED_EXPECTED')\nelse:raise RuntimeError('Cross-Origin read allowed')"
   p=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);self.assertIn('BLOCKED_EXPECTED',p.stdout)
 def test_10_manual_train_only_and_fixed_offsets(self):
  self.assertEqual(self.c['model_seed_offsets'],{'RNN':101,'LSTM':201,'GRU':301,'LTC':401,'CfC':501})
  for parts in self.g['datasets'].values():
   for d in parts.values():
    m=d['metadata'];q=m['manual_reference'];self.assertEqual(q['partition'],'train');self.assertEqual(q['quantiles'],[30,70]);self.assertLess(q['train_end'],m['validation_boundary_start']);self.assertEqual(sum(x['n'] for x in m['manual_validation_support']),m['validation_samples'])
 def test_11_resources_versions_no_model_import(self):
  self.assertEqual(Path('/sys/fs/cgroup/cpu.max').read_text().strip(),'200000 100000');self.assertEqual(int(Path('/sys/fs/cgroup/memory.max').read_text()),8589934592);self.assertEqual({k:importlib.metadata.version(k) for k in self.c['environment_versions']},self.c['environment_versions']);self.assertNotIn('torch',sys.modules)
 def test_12_prefix_and_exact_horizon_dates(self):
  calendar=pd.read_csv(R/'manifests/krx_sessions_2010_2025.csv');lookup=dict(zip(calendar.Date,calendar.session_id));self.assertEqual(len(calendar),3939)
  for origin,parts in self.g['datasets'].items():
   year={'O4':2023,'O5':2024}[origin]
   for d in parts.values():
    dates=json.loads((R/d['date_file']).read_text())
    for partition in dates.values():
     for t,end in zip(partition['dates'],partition['label_end']):self.assertEqual(lookup[end]-lookup[t],20);self.assertLessEqual(end,f'{year}-12-31')
if __name__=='__main__':
 z=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PilotPreflight));bad={x._testMethodName:y for x,y in z.failures+z.errors};names=sorted(x for x in dir(PilotPreflight) if x.startswith('test_'));(R/'manifests/step4a2_preflight_tests.json').write_text(json.dumps({'passed':z.testsRun-len(bad),'failed':len(bad),'tests':[{'id':n,'status':'FAIL' if n in bad else 'PASS',**({'error':bad[n]} if n in bad else {})} for n in names]},indent=2)+'\n');sys.exit(0 if z.wasSuccessful() else 1)
