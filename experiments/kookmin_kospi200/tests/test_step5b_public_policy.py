"""Public synthetic policy and aggregate checks; no financial artifact mapping."""
from pathlib import Path
import json,sys,unittest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step5b_policy import test_metrics
from kospi200.data import BlockedError
class PublicPolicy(unittest.TestCase):
 def test_threshold_strict(self):
  m=test_metrics([0,1],[.5,.5]);self.assertEqual(m['tn'],1);self.assertEqual(m['fn'],1);self.assertEqual(m['positive_rate'],0)
 def test_null_policy_supported_recall(self):
  m=test_metrics([1,1],[.9,.1]);self.assertIsNone(m['BA']);self.assertIsNone(m['macro_f1']);self.assertIsNone(m['recall0']);self.assertEqual(m['recall1'],.5);self.assertEqual(m['accuracy'],.5)
 def test_empty_and_invalid(self):
  self.assertIsNone(test_metrics([],[])['brier'])
  with self.assertRaises(BlockedError):test_metrics([1],[float('nan')])
 def test_aggregate_budget_and_forbidden_execution_zero(self):
  s=json.loads((R/'manifests/step5b_execution_summary.json').read_text());self.assertEqual(s['actual_completed']+s['failed']+s['BLOCKED'],500);self.assertEqual(s['actual_Test_forward_calls'],s['actual_completed']);self.assertEqual(s['completed_duplicate_evaluations'],0)
  for key in ['new_model_fits','retraining','optimizer_updates','HMM_fit','Ensemble','GPU','tau_actual_forward','financial_bootstrap','financial_Holm','financial_pvalues','2026_observations_used','old_files_changed']:self.assertEqual(s[key],0)
  self.assertEqual(s['production_PIT'],'BLOCKED');self.assertEqual(s['source_status'],'BOTH_UNVERIFIED');self.assertEqual(s['postrun_FAIL'],0)
 def test_public_multi_seed_only_and_complete(self):
  a=json.loads((R/'manifests/step5b_public_aggregate_summary.json').read_text());self.assertEqual(len(a['groups']),50);self.assertEqual(len(a['manual_regime_aggregates']),150);self.assertEqual(len(a['validation_Test_gaps']),50);self.assertEqual(len(a['price_B_minus_A']),25)
  for g in a['groups']:self.assertEqual(g['planned_seeds'],10);self.assertEqual(g['completed_seeds'],10);self.assertEqual(g['BA']['valid'],10)
  def check(x):
   if isinstance(x,dict):
    for k,v in x.items():self.assertNotIn(k,['run_id','seed','checkpoint_file','source_directory','scaler','support0','support1']);check(v)
   elif isinstance(x,list):
    for v in x:check(v)
  check(a)
if __name__=='__main__':unittest.main(verbosity=2)
