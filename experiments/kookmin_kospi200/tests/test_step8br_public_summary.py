"""Public-only recovery accounting and aggregation; no model/data execution."""
from pathlib import Path
import json,hashlib,unittest
R=Path(__file__).resolve().parents[1]
class Summary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((R/'manifests/step8br_execution_summary.json').read_text());cls.a=json.loads((R/'manifests/step8br_public_aggregate_summary.json').read_text())
 def test_new40_original40_distinct(self):self.assertEqual(self.s['completed'],40);self.assertEqual(self.s['BLOCKED'],0);self.assertEqual(self.s['original_STEP8B_BLOCKED_preserved'],40);self.assertEqual(self.s['duplicate_evaluations'],0)
 def test_fit_budget(self):self.assertEqual(self.s['Logistic_fits'],10);self.assertEqual(self.s['climatology_estimations'],10);self.assertEqual(self.s['rule_evaluations'],20)
 def test_read_all90_fields(self):self.assertEqual(self.s['fields_actually_reread'],90);self.assertTrue(self.s['numeric_and_original_nonobject_fields_unchanged'])
 def test_no_prohibited_execution(self):
  for k in ['NN_retraining_checkpoint_load_forward','HMM_fit_refilter','financial_tau_extraction','financial_bootstrap_Holm_pvalues','Ensemble_GPU_2026']:self.assertEqual(self.s[k],0)
 def test_old_protocol_and_schema_SHA(self):
  self.assertEqual(hashlib.sha256((R/'configs/step8b_baseline_protocol.json').read_bytes()).hexdigest(),self.s['protocol_sha256']);schema=json.loads((R/'configs/step8br_input_schema.json').read_text());self.assertEqual(hashlib.sha256(json.dumps(schema,sort_keys=True).encode()).hexdigest(),self.s['schema_sha256'])
 def test_equal_weight_5Origins(self):
  a=self.a['candidate_primary'];self.assertEqual(len(a),18)
  for r in a:self.assertEqual(r['n_origins'],5);self.assertEqual(r['n_results'],5 if r['kind']=='baseline' else 50)
 def test_comparison_delta_consistency(self):
  for c in self.a['NN_baseline_descriptive_comparisons']:
   n=next(r for r in self.a['candidate_primary'] if r['candidate']==c['candidate'] and r['model']==c['NN']);b=next(r for r in self.a['candidate_primary'] if r['candidate']==c['candidate'] and r['model']==c['baseline'])
   for k in ['BA','macro_f1','brier']:self.assertAlmostEqual(c['metrics'][k]['mean_NN_minus_baseline'],n['metrics'][k]['mean']-b['metrics'][k]['mean'],places=13)
 def test_no_deterministic_Origin_numbers(self):
  for r in self.a['Origin_secondary_AB_mean']:
   if r['model'] in ['CLIMATOLOGY','LOGISTIC','DMA200','MOMENTUM60']:self.assertTrue(all(v is None for v in r['metrics'].values()))
  self.assertFalse(self.a['individual_cohort_baseline_metrics_published'])
 def test_preservation_and_PIT(self):self.assertEqual(self.s['old_files_changed'],0);self.assertTrue(self.s['master_flags_false']);self.assertEqual(self.s['production_PIT'],'BLOCKED');self.assertTrue(self.s['NN500_Test500_stats600_HMM100_selected10_tau99PASS_1BLOCKED_preserved'])
if __name__=='__main__':unittest.main(verbosity=2)
