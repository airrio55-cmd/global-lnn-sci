"""Checks a blocked release without model fitting or financial input access."""
from pathlib import Path
import json,hashlib,unittest
R=Path(__file__).resolve().parents[1]
class Summary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((R/'manifests/step8b_execution_summary.json').read_text());cls.a=json.loads((R/'manifests/step8b_public_aggregate_summary.json').read_text());cls.g=json.loads((R/'manifests/step8b_gate_results.json').read_text())
 def test_zero_financial_execution(self):
  for k in ['completed','financial_evaluations_started','Logistic_fits','climatology_estimations','rule_evaluations','NN_retraining_checkpoint_load_forward','HMM_fit_refilter','financial_tau_extraction','new_bootstrap_Holm_pvalues','Ensemble_GPU_2026']:self.assertEqual(self.s[k],0)
 def test_exact_roster_accounting(self):self.assertEqual(self.s['roster_units'],40);self.assertEqual(self.s['BLOCKED'],40);self.assertEqual(sum(x['BLOCKED'] for x in self.a['baselines']),40)
 def test_missing_metrics_not_zero(self):
  for x in self.a['baselines']:
   for k in ['Test_BA','Macro_F1','Brier','Recall0','Recall1']:self.assertIsNone(x[k])
 def test_gate_failure_not_promoted(self):self.assertEqual(self.g['persisted_input_gate_FAIL_cohorts'],10);self.assertFalse(self.g['financial_gate_changed_to_PASS']);self.assertEqual(self.s['retry_of_BLOCKED_identity'],0)
 def test_protocol_hash_frozen(self):self.assertEqual(hashlib.sha256((R/'configs/step8b_baseline_protocol.json').read_bytes()).hexdigest(),self.s['protocol_sha256'])
 def test_original_results_preserved(self):self.assertEqual(self.s['previous_files_changed'],0);self.assertTrue(self.s['existing_NN500_Test500_preserved']);self.assertTrue(self.s['master_flags_false'])
if __name__=='__main__':unittest.main(verbosity=2)
