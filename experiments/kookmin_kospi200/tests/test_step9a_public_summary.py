"""Public evidence/draft consistency only; no market array reads or inference."""
from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class Evidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads((R/'manifests/step9a_evidence_traceability.json').read_text());cls.s=json.loads((R/'manifests/step9a_execution_summary.json').read_text());cls.d=json.loads((R/'configs/step9a_test_protocol_DRAFT.json').read_text())
 def test_financial_budgets_zero(self):
  for k in ['financial_fit','financial_checkpoint_load_forward','financial_Test_prediction_metric_recomputation','HMM_fit_refilter','financial_tau_extraction','financial_bootstrap_pvalues_Holm','financial_BOOTSTRAP_draw_budget','Ensemble_external_inputs_GPU_2026']:self.assertEqual(self.s[k],0)
 def test_draft_not_release(self):self.assertFalse(self.d['approved']);self.assertFalse(self.d['families_frozen']);self.assertTrue(self.d['historical_Test_results_already_seen']);self.assertEqual(self.d['financial_pvalue_budget'],0)
 def test_exact_saved_performance_and_differences(self):
  old=json.loads((R/'manifests/step8br_public_aggregate_summary.json').read_text());self.assertEqual(self.e['saved_performance'],old['candidate_primary']);self.assertEqual(self.e['saved_NN_baseline_differences'],old['NN_baseline_descriptive_comparisons'])
 def test_existing_statistics_not_new(self):
  expected={'primary':[0,0,0],'origin':[0,0,0],'secondary':[3,2,3]}
  for family,counts in expected.items():self.assertEqual([r['existing_Holm_below_005'] for r in self.e['existing_statistics_counts'] if r['family']==family],counts)
 def test_claim_sources_exist(self):
  self.assertEqual(len(self.e['claims']),9)
  for c in self.e['claims']:
   self.assertTrue(c['evidence_status']);self.assertFalse(c['new_financial_inference'])
   for p in c['source_reports']:self.assertTrue((R/p).is_file())
 def test_rankings_copy_saved_values(self):
  for g in self.e['rankings_of_saved_summaries']:
   for r in g['rows']:
    original=next(x for x in self.e['saved_performance'] if x['candidate']==g['candidate'] and x['model']==r['model']);self.assertEqual(r['value'],original['metrics'][g['metric']]['mean'])
 def test_no_private_financial_mapping(self):
  text=json.dumps(self.e);self.assertNotIn('checkpoint_file',text);self.assertNotIn('checkpoint_sha256',text);self.assertNotIn('/workspace/',text);self.assertFalse(self.e['individual_financial_lineage_published'])
 def test_preservation_and_limits(self):self.assertEqual(self.s['old_files_changed'],0);self.assertTrue(self.s['original_STEP8B_BLOCKED40_preserved']);self.assertEqual(self.s['production_PIT'],'BLOCKED');self.assertFalse(self.s['JOF_V16_multicountry_results_mixed'])
if __name__=='__main__':unittest.main(verbosity=2)
