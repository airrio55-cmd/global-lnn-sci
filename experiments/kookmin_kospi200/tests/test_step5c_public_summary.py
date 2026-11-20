"""Public synthetic policy and complete hypothesis-family audit only."""
from pathlib import Path
import itertools,json,sys,unittest
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step5c_statistics import observed_metrics,scalar_reference,centered_summary,contiguous_starts,MODELS
from kospi200.statistics import holm
class PublicStatistics(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.summary=json.loads((R/'manifests/step5c_execution_summary.json').read_text());cls.rows=json.loads((R/'manifests/step5c_public_aggregate_summary.json').read_text())['rows']
 def test_01_budget_and_no_new_models(self):
  s=self.summary;self.assertEqual(s['hypothesis_rows_completed'],600);self.assertEqual(s['verified_committed_chunks'],120);self.assertEqual(s['replicates_per_block_per_hypothesis'],10000)
  for k in ['new_training','new_Test_inference','checkpoint_loads','checkpoint_forwards','HMM_fit','RAW_LOG_Ensemble','GPU','tau_actual_forward','2026_observations_used','old_files_changed','postrun_FAIL']:self.assertEqual(s[k],0)
  self.assertEqual(s['production_PIT'],'BLOCKED');self.assertEqual(s['source_status'],'BOTH_UNVERIFIED')
 def test_02_exact_families_each_block(self):
  pairs=[(p,a,b) for p in ['A','B'] for a,b in itertools.combinations(MODELS,2)]
  for block in [20,40,60]:
   primary=[r for r in self.rows if r['block_length']==block and r['family']=='primary'];self.assertEqual([(r['candidate'],r['model_a'],r['model_b']) for r in primary],pairs)
   self.assertEqual(len([r for r in self.rows if r['block_length']==block and r['family']=='secondary']),80);self.assertEqual(len([r for r in self.rows if r['block_length']==block and r['family']=='origin']),100)
 def test_03_validity_and_Holm_recompute(self):
  for block in [20,40,60]:
   for family in ['primary','secondary','origin']:
    rows=[r for r in self.rows if r['block_length']==block and r['family']==family]
    for r in rows:self.assertEqual(r['valid_replicates']+r['invalid_replicates'],10000);self.assertLessEqual(r['invalid_rate'],.1);self.assertGreaterEqual(r['p_holm'],r['p_approx_centered']);self.assertLessEqual(r['p_holm'],1);self.assertFalse(r['CI_is_simultaneous'])
    self.assertTrue(np.array_equal(holm([r['p_approx_centered'] for r in rows]),[r['p_holm'] for r in rows]))
 def test_04_null_policy_matches_STEP5B(self):
  for y in [np.array([0,1]),np.array([0,0]),np.array([1,1]),np.array([],dtype=int)]:
   p=np.full((len(y),2,10),.5);self.assertTrue(np.allclose(observed_metrics(y,p),scalar_reference(y,p),atol=5e-15,rtol=0,equal_nan=True))
 def test_05_centered_tail_and_gap_fixture(self):
  z=centered_summary(1.,np.tile([-2.,-1.,0.,1.,2.],2000));self.assertEqual(z['p_approx_centered'],8001/10001)
  sid=np.r_[np.arange(50),np.arange(100,150)]
  for i in contiguous_starts(sid,40):self.assertTrue(np.all(np.diff(sid[i:i+40])==1))
 def test_06_no_private_vectors_in_public_rows(self):
  forbidden={'run_id','seed','dates','session_id','y','probability','checkpoint_file','scaler','draw_values','source_directory'}
  for row in self.rows:self.assertFalse(set(row)&forbidden);self.assertEqual(row['effect_direction'],'model_a minus model_b')
if __name__=='__main__':unittest.main(verbosity=2)
