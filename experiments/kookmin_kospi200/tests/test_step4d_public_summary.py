"""Verify only the published summary, roster, aggregate CSV and hash manifest."""
from pathlib import Path
import csv,json,math,unittest
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
def rows(name):
 with (ROOT/name).open(newline='') as stream:return list(csv.DictReader(stream))
class PublicSummary(unittest.TestCase):
 def test_completed_budget(self):
  s=read('manifests/step4d_public_summary.json');self.assertEqual(s['new_fit_budget'],150);self.assertEqual(s['old_unique_completed_preserved'],350);self.assertGreaterEqual(s['new_completed'],0);self.assertLessEqual(s['new_completed']+s['new_failed']+s['new_blocked'],150);self.assertEqual(s['total_unique_completed'],350+s['new_completed']);self.assertEqual(s['remaining_unique_fits'],500-s['total_unique_completed'])
 def test_roster_unique_and_scoped(self):
  r=rows('manifests/step4d_job_roster.csv');self.assertEqual(len(r),150);self.assertEqual(len({x['run_id'] for x in r}),150);self.assertEqual({int(x['seed']) for x in r},{72,82,92});self.assertEqual({x['origin'] for x in r},{'O1','O2','O3','O4','O5'});self.assertEqual({x['candidate'] for x in r},{'A','B'})
 def test_multi_seed_aggregate_only(self):
  r=rows('manifests/step4d_public_aggregate_metrics.csv');self.assertEqual(len(r),50)
  for x in r:
   self.assertGreaterEqual(int(x['completed_seeds']),7);self.assertLessEqual(int(x['completed_seeds']),10);self.assertNotIn('run_id',x);self.assertNotIn('seed',x)
   for k,v in x.items():
    if k.endswith('_mean') or k.endswith('_std_ddof1'):self.assertTrue(math.isfinite(float(v)));self.assertGreaterEqual(float(v),0)
 def test_regime_summary_is_aggregate(self):
  r=rows('manifests/step4d_manual_regime_summary.csv');self.assertEqual(len(r),150)
  for x in r:
   self.assertGreaterEqual(int(x['reported_seeds']),7);self.assertLessEqual(int(x['reported_seeds']),10);self.assertNotIn('n_class0_per_seed',x);self.assertNotIn('n_class1_per_seed',x);self.assertNotIn('n_per_seed',x)
 def test_hash_manifest_has_no_individual_metrics(self):
  r=read('manifests/step4d_execution_manifest.json')['job_hashes'];self.assertEqual(len(r),150)
  allowed={'run_id','origin','seed','candidate','model','status','best_checkpoint_sha256','latest_checkpoint_sha256','history_sha256','postfit_checkpoint_audit_sha256'}
  for x in r:
   self.assertEqual(set(x),allowed)
   if x['status']=='COMPLETED':self.assertEqual(len(x['best_checkpoint_sha256']),64)
 def test_excluded_execution_and_provenance(self):
  s=read('manifests/step4d_public_summary.json')
  for k in ['Test_evaluation','HMM_fit','GPU','training_enabled','hmm_fit_enabled']:self.assertFalse(s[k])
  self.assertEqual(s['source_status'],'BOTH_UNVERIFIED');self.assertEqual(s['production_PIT'],'BLOCKED');self.assertEqual(s['postrun_FAIL'],0)
 def test_Validation_readiness_not_Test_or_inference(self):
  s=read('manifests/step4d_comparison_readiness_public.json');self.assertEqual(s['primary_family_size'],20);self.assertEqual(s['secondary_family_size'],80);self.assertEqual(s['origin_diagnostic_family_size'],100)
  for k in ['bootstrap_draws_executed','confirmatory_pvalues_executed','independent_Test_inputs_read','independent_Test_predictions_created','independent_Test_probability_files_verified']:self.assertEqual(s[k],0)
  self.assertFalse(s['seed_pooling_as_market_observations'])
if __name__=='__main__':unittest.main(verbosity=2)
