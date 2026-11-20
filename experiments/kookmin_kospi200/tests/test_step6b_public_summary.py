"""Public aggregate and synthetic metric checks; never fit/filter financial models."""
from pathlib import Path
import json,sys,unittest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step5b_policy import test_metrics
class PublicSummary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=json.loads((R/'manifests/step6b_execution_summary.json').read_text());cls.a=json.loads((R/'manifests/step6b_public_aggregate_summary.json').read_text())
 def test_01_actual_budget_and_statuses(self):
  s=self.s;self.assertEqual(s['HMM_candidates_actual_fit'],100);self.assertEqual(s['HMM_candidates_eligible']+s['HMM_candidates_ineligible']+s['HMM_candidates_failed'],100);self.assertEqual(s['filtered_HMM_cohorts']+s['cohorts_BLOCKED'],10);self.assertLessEqual(s['HMM_candidates_actual_fit'],s['HMM_candidate_budget'])
 def test_02_no_forbidden_execution_and_old_files(self):
  for k in ['old_files_changed','new_neural_training','neural_retraining','neural_checkpoint_load_forward','Test_prediction_regeneration','new_financial_bootstrap','new_Holm_correction','new_financial_pvalues','RAW_LOG_Ensemble','tau_actual_forward','GPU','2026_observations_used','failed_seed_replacement','duplicate_HMM_fit_identities','postrun_FAIL']:self.assertEqual(self.s[k],0)
  self.assertEqual(self.s['production_PIT'],'BLOCKED');self.assertEqual(self.s['source_status'],'BOTH_UNVERIFIED');self.assertEqual(self.s['existing_NN_training_preserved'],500);self.assertEqual(self.s['existing_Test_predictions_preserved'],500)
 def test_03_two_and_three_regime_definitions_separate(self):
  self.assertEqual(len(self.a['HMM_regime_groups']),100);self.assertEqual(len(self.a['manual_regime_reference_groups']),150);self.assertEqual({x['regime'] for x in self.a['HMM_regime_groups']},{'Low_Vol','High_Vol'});self.assertEqual({x['regime'] for x in self.a['manual_regime_reference_groups']},{'Low_Vol','Mid_Vol','High_Vol'})
 def test_04_seedwise_groups_and_missing_null(self):
  for r in self.a['HMM_regime_groups']:
   self.assertEqual(r['planned_NN_seeds'],10);self.assertLessEqual(r['completed_NN_seeds'],10)
   for metric in ['BA','macro_f1','recall0','recall1','positive_rate']:
    q=r[metric]
    if q['valid']==0:self.assertIsNone(q['mean'])
 def test_05_STE5B_null_and_threshold_policy(self):
  m=test_metrics([0,0],[.5,.5]);self.assertIsNone(m['BA']);self.assertIsNone(m['macro_f1']);self.assertEqual(m['recall0'],1.);self.assertIsNone(m['recall1']);self.assertEqual(m['positive_rate'],0)
 def test_06_no_private_input_date_parameter_mapping(self):
  forbidden={'run_id','job_id','seed','selected_seed','dates','session_id','Train_dates','Train_rows','support0','support1','scaler','parameters','posterior','probability','checkpoint_file','source_directory'}
  def scan(x):
   if isinstance(x,dict):
    self.assertFalse(set(x)&forbidden)
    for v in x.values():scan(v)
   elif isinstance(x,list):
    for v in x:scan(v)
  scan(self.a)
if __name__=='__main__':unittest.main(verbosity=2)
