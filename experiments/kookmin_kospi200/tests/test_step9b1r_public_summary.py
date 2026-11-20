"""Public-only consistency; no real market arrays or model I/O."""
from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class Summary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((R/'manifests/step9b1r_simulation_summary.json').read_text());cls.m=json.loads((R/'manifests/step9b1r_method_review.json').read_text())
 def test01_financial_budgets_zero(self):self.assertEqual(self.s['financial_fit_forward_draw_pvalues_CI'],0);self.assertFalse(self.m['financial_bootstrap_enabled']);self.assertEqual(self.m['financial_pvalue_budget'],0)
 def test02_no_method_claimed_valid(self):self.assertEqual(self.m['status'],'BLOCKED_METHOD_NOT_VALIDATED');self.assertIsNone(self.m['recommended_financial_method']);self.assertTrue(all(not x['all_core_criteria_passed'] for x in self.s['eligibility_against_frozen_core_criteria']))
 def test03_exact_prior_reproduction(self):self.assertEqual(len(self.s['source_prior_reproduction']),6);self.assertTrue(all(x['matches_prior_exact'] for x in self.s['source_prior_reproduction']))
 def test04_pair_dataset_accounting(self):
  groups={}
  for r in self.s['pair_experiments']['results']:groups.setdefault((r['phase'],r['DGP']),r['datasets']);self.assertEqual(groups[r['phase'],r['DGP']],r['datasets'])
  self.assertEqual(sum(groups.values()),4680)
 def test05_invalid_not_zero_filled(self):
  for r in self.s['pair_experiments']['results']:
   if not r['eligible_datasets']:self.assertIsNone(r['rejection_conditional_on_eligible']['point']);self.assertIsNone(r['coverage_conditional_on_eligible']['point'])
 def test06_Holm_resolution_not_false_pass(self):
  for r in self.s['full_family_experiments']['results']:
   if r['draws']==199:self.assertFalse(r['informative_Holm_tail_resolution']);self.assertIn('MC_RESOLUTION',r['interpretation'])
 def test07_old_families_and_tau_preserved(self):
  old=json.loads((R/'configs/step9b1_protocol.json').read_text());self.assertEqual(old['primary_Holm_size'],20);self.assertEqual(old['secondary_Holm_size'],80);self.assertTrue(self.m['tau100_recovery_preserved']);self.assertEqual(self.m['old_files_changed'],0)
 def test08_no_private_paths(self):
  for token in ['/workspace/output/','/workspace/work/','/workspace/attachments/','sediment://']:self.assertNotIn(token,json.dumps(self.s))
if __name__=='__main__':unittest.main(verbosity=2)
