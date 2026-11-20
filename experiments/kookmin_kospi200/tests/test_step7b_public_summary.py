"""Public aggregate contract only. No checkpoint, financial arrays or inference."""
from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class PublicSummary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((R/'manifests/step7b_execution_summary.json').read_text());cls.a=json.loads((R/'manifests/step7b_public_aggregate_summary.json').read_text());cls.g=json.loads((R/'manifests/step7b_gate_results.json').read_text())
 def test_budget(self):
  self.assertLessEqual(self.s['financial_forwards'],100);self.assertLessEqual(self.s['financial_checkpoint_loads'],100)
 def test_accounting(self):self.assertEqual(self.s['completed']+self.s['BLOCKED']+self.s['not_attempted'],100)
 def test_equivalence(self):self.assertEqual(self.s['completed'],self.s['probability_exact_PASS'])
 def test_old_preserved(self):self.assertEqual(self.s['old_files_changed'],0);self.assertTrue(self.s['NN500_Test500_statistics600_HMM100_selected10_preserved'])
 def test_no_other_experiments(self):
  for k in ['new_NN_training','new_HMM_fit_or_refilter','new_Test_performance_metrics','financial_bootstrap_Holm_pvalues','Ensemble_GPU_2026']:self.assertEqual(self.s[k],0)
 def test_private_no_individual_groups(self):
  for g in self.a['groups']:self.assertGreaterEqual(g['n_checkpoints'],2);self.assertNotIn('checkpoint_sha256',g);self.assertNotIn('identity',g)
 def test_units_and_limits(self):self.assertEqual(self.a['units'],'model_observation_step');self.assertEqual(self.s['production_PIT'],'BLOCKED');self.assertEqual(self.s['LTC_whole_Test_degenerate_preserved'],24)
 def test_postrun(self):self.assertEqual(self.g['postrun_FAIL'],0)
if __name__=='__main__':unittest.main(verbosity=2)
