"""Public recovery accounting/disclosure only; no financial model/data I/O."""
from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class RecoverySummary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((R/'manifests/step7br_execution_summary.json').read_text());cls.p=json.loads((R/'manifests/step7br_public_aggregate_summary.json').read_text())
 def test_single_budget(self):self.assertEqual(self.s['new_checkpoint_loads'],1);self.assertEqual(self.s['new_financial_forwards'],1);self.assertEqual(self.s['other99_checkpoint_reloads_remeasurements'],0)
 def test_exact_and_state(self):self.assertTrue(self.s['probability_exact_PASS']);self.assertTrue(self.s['parameter_RNG_unchanged']);self.assertTrue(self.s['observation_entry_equals_substep0'])
 def test_original_BLOCKED_not_promoted(self):
  old=json.loads((R/'manifests/step7b_execution_summary.json').read_text());self.assertEqual(old['completed'],99);self.assertEqual(old['BLOCKED'],1)
 def test_new100_accounting(self):self.assertEqual(self.s['versioned_tau_integration'],100);self.assertEqual(self.s['whole_Test_degenerate_tau_valid']+self.s['nondegenerate_tau_valid'],100)
 def test_no_prohibited_operations(self):
  for k in ['new_NN_training','HMM_fit_refilter','Test_performance_recomputation','new_financial_bootstrap_Holm_pvalues','Ensemble_GPU_AMP_2026']:self.assertEqual(self.s[k],0)
 def test_no_inverse_singleton_statistics(self):
  def walk(x):
   if isinstance(x,dict):
    for value in x.values():walk(value)
   elif isinstance(x,list):
    for value in x:walk(value)
   else:self.assertNotIsInstance(x,float)
  walk(self.p);self.assertFalse(self.s['numeric_updated_tau_and_deltas_published']);self.assertFalse(self.p['recovery_identity_published'])
 def test_no_old_changes_or_overclaims(self):self.assertEqual(self.s['old_files_changed'],0);self.assertEqual(self.s['original_process_termination_cause'],'UNKNOWN');self.assertEqual(self.s['production_PIT'],'BLOCKED')
if __name__=='__main__':unittest.main(verbosity=2)
