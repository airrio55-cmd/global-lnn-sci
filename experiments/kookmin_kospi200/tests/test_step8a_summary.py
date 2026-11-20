"""Read-only aggregate consistency and disclosure contract; no financial execution."""
from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class AuditSummary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads((R/'manifests/step8a_public_aggregate_summary.json').read_text());cls.s=json.loads((R/'manifests/step8a_execution_summary.json').read_text())
 def test_preservation(self):self.assertEqual(self.s['previous_files_changed'],0);self.assertEqual(self.s['probability_exact_preserved'],99);self.assertEqual(self.s['tau_BLOCKED_preserved'],1)
 def test_no_execution(self):
  for k in ['new_training','checkpoint_load_or_forward','new_Test_prediction_or_performance','HMM_fit_or_refilter','financial_tau_extraction','financial_bootstrap_Holm_pvalues','new_confirmatory_hypotheses','baseline_financial_execution','Ensemble_GPU_2026']:self.assertEqual(self.s[k],0)
 def test_partitions(self):
  for key in ['origin_groups','price_groups','seed_groups','origin_price_groups']:
   self.assertEqual(sum(c['degenerate']['n'] for c in self.a[key]),23);self.assertEqual(sum(c['nondegenerate']['n'] for c in self.a[key]),76)
 def test_common_support(self):
  d=self.a['common_support_composition'];self.assertAlmostEqual(d['within_cell_component']+d['composition_component'],d['common_support_pooled_gap'],places=13);self.assertEqual(d['full10cell_standardized_effect'],'NOT_IDENTIFIABLE')
 def test_no_empty_cell_gap(self):
  for k in ['origin_groups','seed_groups','origin_price_groups']:
   for c in self.a[k]:
    if min(c['degenerate']['n'],c['nondegenerate']['n'])==0:self.assertIsNone(c['mean_gap_D_minus_N'])
 def test_singletons_private(self):
  for k in ['origin_groups','price_groups','seed_groups','origin_price_groups']:
   for c in self.a[k]:
    for group in ['degenerate','nondegenerate']:
     z=c[group]
     if z['n']==1:
      for field in ['mean','median','min','max','sample_std']:self.assertIsNone(z[field])
     if z['n']==2:
      for field in ['min','max','sample_std']:self.assertIsNone(z[field])
 def test_HMM_nulls(self):
  for g in self.a['HMM_integration']:
   if g['BA_valid']==0:self.assertIsNone(g['BA_mean'])
   self.assertNotIn('support0',g);self.assertNotIn('support1',g)
 def test_no_sensitive_mapping(self):
  text=json.dumps(self.a);self.assertNotIn('checkpoint_sha256',text);self.assertNotIn('checkpoint_file',text);self.assertNotIn('/workspace/',text);self.assertTrue(self.a['no_origin_seed_cross_mapping'])
 def test_units_limitations(self):self.assertEqual(self.a['units'],'model_observation_step');self.assertEqual(self.s['production_PIT'],'BLOCKED');self.assertTrue(self.s['master_flags_false'])
if __name__=='__main__':unittest.main(verbosity=2)
