"""O1 Pilot post-run audits. No model fit, no Test source, no extra trial."""
from pathlib import Path
import sys,json,hashlib,unittest
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.pilot_data import validation_metrics
class PilotResults(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((R/'manifests/step3a_execution_manifest.json').read_text());cls.g=json.loads((R/'manifests/step3a_preflight.json').read_text());cls.run_directory=R/cls.m['run_directory'];cls.c=json.loads((R/'configs/step3a_pilot_config.json').read_text())
 def test_01_exact_ten_distinct_attempts(self):
  self.assertEqual(self.m['fit_attempts'],10);self.assertEqual(set(self.m['fit_ledger']),{p+'_'+n for p in ['A','B'] for n in ['RNN','LSTM','GRU','LTC','CfC']});self.assertEqual(self.m['completed_models']+self.m['failed_models'],10)
 def test_02_same_dates_seeds_and_counts(self):
  self.assertEqual(self.g['datasets']['A']['date_information_sha256'],self.g['datasets']['B']['date_information_sha256'])
  for row in self.m['fit_ledger'].values():self.assertEqual(row['train_samples'],2387);self.assertEqual(row['validation_samples'],228);self.assertEqual(row['base_seed'],2);self.assertEqual(row['effective_seed'],2+self.c['model_seed_offsets'][row['model']])
 def test_03_only_O1_train_validation_and_no_2026(self):
  for info in self.g['datasets'].values():
   d=json.loads((R/info['date_file']).read_text());self.assertEqual(set(d),{'train','validation'})
   for part in d.values():self.assertTrue(all(x<='2020-12-31' for k in ['dates','label_end'] for x in part[k]))
   self.assertLess(max(d['train']['label_end']),min(d['validation']['dates']))
  self.assertEqual(self.m['actual_Test_price_rows_read'],0);self.assertEqual(self.m['2026_observations_used'],0)
 def test_04_best_epoch_first_max_BA_only(self):
  for row in self.m['fit_ledger'].values():
   if row['status']!='COMPLETED':continue
   h=json.loads((self.run_directory/row['run_id']/'history.json').read_text());best=max(x['validation_BA'] for x in h);first=next(x['epoch'] for x in h if x['validation_BA']==best);self.assertEqual(first,row['best_validation_epoch']);self.assertEqual(best,row['metrics']['validation_BA']);self.assertTrue(row['early_stopping_selection_verified'])
 def test_05_patience10_and_max100(self):
  for row in self.m['fit_ledger'].values():
   if row['status']!='COMPLETED':continue
   h=json.loads((self.run_directory/row['run_id']/'history.json').read_text());self.assertEqual(len(h),row['epochs_completed']);self.assertLessEqual(len(h),100);best=-1.;counter=0
   for x in h:
    if x['validation_BA']>best:best=x['validation_BA'];counter=0
    else:counter+=1
    self.assertEqual(x['early_stopping_counter'],counter);self.assertLessEqual(counter,10)
   if len(h)<100:self.assertEqual(counter,10)
 def test_06_validation_metrics_match_private_probabilities(self):
  for row in self.m['fit_ledger'].values():
   if row['status']!='COMPLETED':continue
   with np.load(self.run_directory/row['run_id']/'validation_predictions_private.npz',allow_pickle=False) as z:
    self.assertEqual(len(z['probability']),228);self.assertTrue(all(x<='2020-12-31' for x in z['dates']));m=validation_metrics(z['y_true'],z['probability'])
   self.assertEqual(m,row['metrics'])
 def test_07_degenerate_flags_not_suppressed(self):
  for row in self.m['fit_ledger'].values():
   if row['status']!='COMPLETED':continue
   h=json.loads((self.run_directory/row['run_id']/'history.json').read_text());self.assertEqual(row['epochs_with_degenerate_prediction'],sum(x['prediction_status']=='DEGENERATE_PREDICTION' for x in h));p=row['metrics']['prediction_positive_rate'];self.assertEqual(row['prediction_status'],'DEGENERATE_PREDICTION' if p in [0.,1.] else 'TWO_CLASS_PREDICTION')
 def test_08_real_checkpoint_roundtrip_and_epoch_boundary_resume(self):
  import torch
  for row in self.m['fit_ledger'].values():
   if row['status']!='COMPLETED':continue
   self.assertTrue(row['checkpoint_restore']);self.assertTrue(row['epoch1_resume_roundtrip']);self.assertTrue(row['RNG_restore_exact']);self.assertFalse(row['full_fresh_retrain_reproducibility_executed']);p=self.run_directory/row['run_id']/'latest.pt';q=torch.load(p,map_location='cpu',weights_only=True)
   self.assertTrue({'model','optimizer','scheduler','early_stopping','RNG','scaler_metadata','environment','feature_order','input_data_sha256','runner_sha256'}.issubset(q));self.assertEqual(set(q['RNG']),{'Python','NumPy','Torch_CPU','DataLoader'});self.assertEqual(q['completed_epoch'],row['epochs_completed'])
 def test_09_code_data_and_config_hashes(self):
  self.assertEqual(hashlib.sha256((R/'runtime/step3a_pilot.py').read_bytes()).hexdigest(),self.m['runner_sha256']);self.assertEqual(hashlib.sha256((R/'configs/step3a_pilot_config.json').read_bytes()).hexdigest(),self.m['config_sha256'])
  for x in self.m['implementation_artifacts']:self.assertEqual(hashlib.sha256((R/x['file']).read_bytes()).hexdigest(),x['sha256'])
 def test_10_production_and_source_status_unchanged(self):
  b=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(b['training_enabled']);self.assertFalse(b['hmm_fit_enabled']);self.assertTrue(self.m['pilot_execution_enabled']);self.assertEqual(self.m['source_status'],'BOTH_UNVERIFIED');self.assertEqual(self.m['production_PIT_status'],'BLOCKED');self.assertIsNone(self.m['main_price_candidate_selected'])
 def test_11_scope_exclusions_and_file_access(self):
  for k in ['HMM_fit_executed','GPU_executed','full_RO_executed','Ablation_executed','full_Notebook_executed','hyperparameters_changed_after_results','model_fit_repeated_to_select_A_B']:self.assertFalse(self.m[k])
  self.assertEqual(self.m['file_access_barrier']['forbidden_financial_access_attempts'],0);self.assertEqual(self.m['Test_predictions_generated'],0);self.assertEqual(self.m['test_dataframes_constructed'],0)
 def test_12_aggregated_public_metrics_only(self):
  d=pd.read_csv(R/'manifests/step3a_pilot_metrics.csv');self.assertEqual(len(d),self.m['completed_models']);self.assertNotIn('probability',d);self.assertNotIn('y_true',d);self.assertNotIn('Date',d);self.assertEqual(set(d.candidate),{'A','B'});self.assertTrue(d.validation_BA.between(0,1).all())
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(PilotResults);result=unittest.TextTestRunner(verbosity=2).run(suite)
 (R/'manifests/step3a_postrun_tests.json').write_text(json.dumps({'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors),'scope':'O1 Pilot records/validation/checkpoints only; no additional model fitting or Test access'},indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
