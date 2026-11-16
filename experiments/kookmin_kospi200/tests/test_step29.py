"""Post-run control and evidence checks. Never repeat synthetic model updates."""
from pathlib import Path
import sys,json,copy,hashlib,unittest,ast
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step29_synthetic_smoke import validate_synthetic_scope,CHECK_NAMES,MODELS
from runtime.step28_smoke_runtime import require_smoke_authorization
class Step29Controls(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'configs/step29_synthetic_smoke_config.json').read_text());cls.a=json.loads((ROOT/'provenance/step29_synthetic_authorization.json').read_text());cls.m=json.loads((ROOT/'manifests/step29_smoke_results.json').read_text());cls.e=json.loads((ROOT/'manifests/step29_runtime_environment.json').read_text())
 def auth(self,c=None,a=None):return validate_synthetic_scope(c or self.c,a or self.a,config_sha256=hashlib.sha256((ROOT/'configs/step29_synthetic_smoke_config.json').read_bytes()).hexdigest(),runner_sha256=hashlib.sha256((ROOT/'runtime/step29_synthetic_smoke.py').read_bytes()).hexdigest())
 def test_01_independent_scope_and_authorization_hashes(self):self.assertTrue(self.auth());self.assertFalse(self.c['training_enabled']);self.assertFalse(self.c['hmm_fit_enabled']);self.assertFalse(self.a['permits_production_training'])
 def test_02_scope_rejects_financial_paths_and_excess_budget(self):
  for key,value in [('market_data_access',True),('gpu_enabled',True),('production_gate_override',True),('training_enabled',True),('repetitions',3),('input_shape',[64,20,5]),('optimizer_updates_per_repetition',2),('price_path','forbidden.csv')]:
   c=copy.deepcopy(self.c);c[key]=value
   with self.assertRaises(ValueError):self.auth(c)
 def test_03_approval_does_not_authorize_production(self):
  c=json.loads((ROOT/'configs/step28_smoke_config.json').read_text());g=json.loads((ROOT/'manifests/step28_gate_results.json').read_text())
  with self.assertRaises(Exception):require_smoke_authorization(c,g,self.a,config_sha256=self.a['config_sha256'],gates_sha256='a'*64)
  c['training_enabled']=True
  for item in g['mandatory_A'].values():item['status']='PASS'
  with self.assertRaises(Exception):require_smoke_authorization(c,g,self.a,config_sha256=self.a['config_sha256'],gates_sha256='a'*64)
 def test_04_actual_five_model_matrix(self):
  self.assertEqual([r['model'] for r in self.m['models']],MODELS);self.assertEqual(self.m['check_counts'],{'PASS':70,'FAIL':0,'BLOCKED':0})
  for r in self.m['models']:self.assertEqual(set(r['checks']),set(CHECK_NAMES));self.assertTrue(all(v=='PASS' for v in r['checks'].values()))
 def test_05_actual_parameter_counts(self):
  expected={'RNN':17154,'LSTM':67842,'GRU':50946,'LTC':67462,'CfC':83074}
  for r in self.m['models']:
   for p in r['repetitions']:self.assertEqual(p['parameters']['trainable'],expected[r['model']])
 def test_06_fixture_classes_dtype_and_shapes(self):
  f=self.m['fixture'];self.assertNotEqual(f['train']['input_sha256'],f['validation']['input_sha256'])
  for p in f.values():self.assertEqual(p['input_shape'],[64,20,2]);self.assertEqual(p['input_dtype'],'float32');self.assertEqual(p['target_shape'],[64]);self.assertEqual(p['target_dtype'],'int64');self.assertEqual(p['class_counts'],{'0':32,'1':32});self.assertTrue(p['finite'])
 def test_07_exact_budget_gradients_and_checkpoints(self):
  self.assertEqual(self.m['optimizer_updates_total'],10)
  for row in self.m['models']:
   self.assertEqual(len(row['repetitions']),2)
   for rep in row['repetitions']:
    self.assertEqual(rep['optimizer_updates'],1);self.assertEqual(rep['scheduler_steps'],1);self.assertTrue(rep['gradient_finite']);self.assertTrue(rep['train_loss_finite']);self.assertTrue(rep['validation_loss_finite']);self.assertLessEqual(rep['gradient_norm_after_clip'],1.000001);self.assertEqual(rep['trained_state_sha256'],rep['restored_state_sha256']);p=ROOT/rep['checkpoint_file'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),rep['checkpoint_sha256'])
 def test_08_no_financial_read_or_test_epoch_GPU_HMM(self):
  self.assertEqual(self.m['file_access_barrier']['financial_read_attempts'],0);self.assertEqual(self.m['file_access_barrier']['financial_reads_allowed'],0)
  for k in ['actual_Test_accessed','HMM_fit_executed','GPU_executed','production_training_executed','full_Notebook_executed','epoch_loop_executed']:self.assertIs(self.m[k],False)
 def test_09_environment_and_LTC_constraint(self):
  for k,v in [('torch','2.10.0+cpu'),('ncps','1.0.1'),('hmmlearn','0.3.3')]:self.assertEqual(self.e['versions'][k],v)
  self.assertIsNone(self.e['cuda_build']);self.assertFalse(self.e['AMP_enabled']);self.assertFalse(self.e['packages_updated']);self.assertEqual(self.e['expected_version_differences'],{})
  row=next(r for r in self.m['models'] if r['model']=='LTC')
  for p in row['repetitions']:self.assertTrue(p['LTC_implicit_param_constraints']);self.assertEqual(p['LTC_positive_function'],'Softplus');self.assertEqual(p['LTC_solver_substeps'],6)
 def test_10_original_source_hashes_and_cell_locations(self):
  for k,v in self.m['original_source_lineage'].items():self.assertEqual(v['sha256'],self.c['original_definition_hashes'][k]);self.assertEqual(v['cell_1based'],6 if k=='FocalLoss' else 8)
  self.assertEqual(self.m['source_notebook_sha256'],self.c['source_notebook_sha256'])
 def test_11_no_RAW_LOG_or_5feature_execution_claim(self):
  self.assertEqual(self.m['model_cases'],5);self.assertEqual(self.m['RAW_5feature_runtime_status'],'BLOCKED_NOT_AUTHORIZED')
  for m in self.m['models']:self.assertEqual(m['input_kind'],'SYNTHETIC_2_FEATURES_NO_RAW_LOG_EXPERIMENT')
 def test_12_current_synthetic_scope_cannot_forge_or_drift(self):
  for key,value in [('config_sha256','bad'),('runner_sha256','bad'),('scope','STEP3_F1_O1_SEED2_CPU_SMOKE_ONLY'),('permits_HMM_fit',True)]:
   a=copy.deepcopy(self.a);a[key]=value
   with self.assertRaises(ValueError):self.auth(a=a)
 def test_13_entrypoint_rejects_consumed_approval_without_running_models(self):
  import subprocess
  notebook=next((ROOT/'originals').glob('*10개*.ipynb'));out=ROOT/'data/derived/step29_unauthorized_repeat_must_not_exist'
  self.assertFalse(out.exists())
  cmd=[sys.executable,str(ROOT/'tools/step29_synthetic_smoke.py'),'--config-path',str(ROOT/'configs/step29_synthetic_smoke_config.json'),'--approval-path',str(ROOT/'provenance/step29_synthetic_authorization.json'),'--notebook-path',str(notebook),'--output-dir',str(out)]
  result=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
  self.assertEqual(result.returncode,2);self.assertIn('already been executed',result.stderr);self.assertFalse(out.exists())
