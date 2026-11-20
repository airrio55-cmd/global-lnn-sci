"""Public structural and synthetic-only forward-filter checks. No HMM fitting."""
from pathlib import Path
import json,sys,unittest
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step6a_hmm import HMM_KWARGS,SEEDS,filter_sessions,financial_hmm_entrypoint
from kospi200.data import BlockedError
class PublicContract(unittest.TestCase):
 def test_01_frozen_spec_and_false_flags(self):
  c=json.loads((R/'configs/step6a_hmm_protocol.json').read_text());self.assertEqual(c['HMM'],HMM_KWARGS);self.assertEqual(c['hmm_initialization_seeds'],SEEDS);self.assertFalse(c['hmm_fit_enabled']);self.assertFalse(c['hmm_filtering_enabled'])
 def test_02_100_planned_candidates_not_completed(self):
  p=json.loads((R/'manifests/step6a_hmm_job_plan_public.json').read_text());self.assertEqual(len(p['origins'])*len(p['price_candidates'])*len(p['HMM_initialization_seeds']),100);self.assertNotIn('jobs',p);self.assertNotIn('cohorts',p);self.assertEqual(p['financial_fits_completed'],0);self.assertEqual(p['final_selected_HMMs_planned'],10)
 def test_03_financial_zero_and_preservation(self):
  s=json.loads((R/'manifests/step6a_execution_summary.json').read_text())
  for k in ['financial_HMM_fit','financial_HMM_filtering','financial_price_volatility_arrays_opened','financial_Test_prediction_arrays_opened','new_neural_training','retraining','Test_reinference','checkpoint_load_forward','new_financial_pvalues','financial_bootstrap_rerun','RAW_LOG_Ensemble','tau_actual_forward','GPU','2026_price_used','old_files_changed']:self.assertEqual(s[k],0)
  self.assertEqual(s['synthetic_PASS'],24);self.assertEqual(s['synthetic_FAIL'],0);self.assertEqual(s['production_PIT'],'BLOCKED');self.assertTrue(s['training500_preserved'] and s['Test500_preserved'] and s['STEP5C_results_preserved'])
 def test_04_future_invariance_without_fit(self):
  p={'startprob':np.array([.5,.5]),'transmat':np.array([[.9,.1],[.1,.9]]),'means':np.array([[0.],[2.]]),'covars':np.array([[[1.]],[[1.]]])};x=np.linspace(0,2,30)[:,None];ids=np.arange(30);a=filter_sessions(x,ids,parameters=p,expected_session_ids=ids);x[16:]=99.;b=filter_sessions(x,ids,parameters=p,expected_session_ids=ids);self.assertTrue(np.array_equal(a[:16],b[:16]))
 def test_05_financial_flags_cannot_release_entry(self):
  with self.assertRaises(BlockedError):financial_hmm_entrypoint(approved=True,hmm_fit_enabled=True)
 def test_06_readiness_blocked_and_no_private_mapping(self):
  g=json.loads((R/'manifests/step6a_hmm_gate_results.json').read_text());self.assertEqual(g['execution_gate'],'BLOCKED_PREPARATION_ONLY');self.assertEqual(g['BLOCKED'],6)
  p=json.loads((R/'manifests/step6a_hmm_job_plan_public.json').read_text());forbidden={'checkpoint_file','probability_file','source_directory','train_dates','train_session_ids','input_sha256'}
  self.assertFalse(set(p)&forbidden);self.assertFalse(p['per_cohort_Train_counts_and_filtering_ranges_published'])
if __name__=='__main__':unittest.main(verbosity=2)
