"""New resampling design checks with generated arrays only; no market file I/O."""
from pathlib import Path
import sys,unittest
from unittest.mock import patch
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step9a_synthetic import *
D='SYNTHETIC_ONLY'
class Synthetic(unittest.TestCase):
 def test_block20_40_60_contiguity(self):
  for L in [20,40,60]:
   z=moving_block_indices(600,L,np.random.default_rng(2),domain=D);self.assertEqual(len(z),600);self.assertTrue(np.all((z>=0)&(z<600)))
   for start in range(0,600,L):self.assertTrue(np.all(np.diff(z[start:start+L])==1))
 def test_repeatability_and_pairing(self):
  a=moving_block_indices(600,40,np.random.default_rng(2),domain=D);b=moving_block_indices(600,40,np.random.default_rng(2),domain=D);self.assertTrue(np.array_equal(a,b));x=np.arange(600);self.assertTrue(np.array_equal((x+100)[a]-x[a],np.full(600,100)))
 def test_block_preserves_more_adjacency_than_iid(self):
  b=moving_block_indices(600,20,np.random.default_rng(2),domain=D);iid=np.random.default_rng(2).integers(0,600,600);self.assertGreater(np.mean(np.diff(b)==1),np.mean(np.diff(iid)==1))
 def fixture(self):
  y=np.tile([0,1],100);origin=np.repeat(np.arange(5),40);p=np.stack([np.full(200,.4),np.full(200,.6)]);b=np.full(200,.6);return y,p,b,origin
 def test_identical_forecasts_zero_effect(self):
  y,p,b,o=self.fixture();p[:]=b;self.assertEqual(paired_origin_effect(y,p,b,o,np.arange(200),'BA',domain=D),0)
 def test_seed_metric_mean_not_ensemble(self):
  y,p,b,o=self.fixture();y[:]=np.tile([0,0,0,1],50);p[0]=.01;p[1]=.51;b[:]=.6
  value=paired_origin_effect(y,p,b,o,np.arange(200),'accuracy',domain=D);self.assertAlmostEqual(value,.25);self.assertAlmostEqual(test_metrics(y,p.mean(axis=0))['accuracy']-test_metrics(y,b)['accuracy'],.5)
 def test_date_count_not_seed_concatenation(self):
  y,p,b,o=self.fixture();self.assertEqual(p.shape[1],len(y));self.assertEqual(len(moving_block_indices(len(y),20,np.random.default_rng(2),domain=D)),len(y))
 def test_missing_Origin_draw_null(self):
  y,p,b,o=self.fixture();self.assertIsNone(paired_origin_effect(y,p,b,o,np.arange(40),'BA',domain=D))
 def test_single_true_class_draw_null(self):
  y,p,b,o=self.fixture();self.assertIsNone(paired_origin_effect(y,p,b,o,np.arange(0,200,2),'BA',domain=D))
 def test_constant_prediction_valid_when_truth_two_classes(self):
  y,p,b,o=self.fixture();self.assertIsNotNone(paired_origin_effect(y,p,b,o,np.arange(200),'BA',domain=D))
 def test_synthetic_plus_one_p_bounds(self):
  p=centered_synthetic_p(1,np.ones(100),domain=D);self.assertEqual(p,1/101);self.assertGreater(p,0);self.assertLessEqual(p,1)
 def test_holm_known_example(self):self.assertTrue(np.allclose(holm_synthetic([.01,.04,.03],domain=D),[.03,.06,.06]))
 def test_holm_invalid_family_blocked(self):
  with self.assertRaises(BlockedError):holm_synthetic([.1,np.nan],domain=D)
 def test_family_pairing_reuses_same_dates(self):
  y,p,b,o=self.fixture();idx=moving_block_indices(200,20,np.random.default_rng(2),domain=D);a=paired_origin_effect(y,p,b,o,idx,'BA',domain=D);z=paired_origin_effect(y,p,b,o,idx,'BA',domain=D);self.assertEqual(a,z)
 def test_unequal_Origin_sizes_equal_weight(self):
  sizes=[40,80,120,160,200];o=np.repeat(np.arange(5),sizes);y=np.tile([0,1],300);b=np.full(600,.6);p=np.tile(b,(2,1));p[:,o==0]=np.where(y[o==0],.9,.1)
  self.assertAlmostEqual(paired_origin_effect(y,p,b,o,np.arange(600),'BA',domain=D),.1)
 def test_synthetic_null_draws_all_block_lengths(self):
  y,p,b,o=self.fixture();p[:]=b
  for L in [20,40,60]:
   rng=np.random.default_rng(2);values=[]
   for _ in range(12):
    idx=moving_block_indices(200,L,rng,domain=D);v=paired_origin_effect(y,p,b,o,idx,'BA',domain=D)
    if v is not None:values.append(v)
   self.assertGreater(len(values),0);self.assertTrue(all(v==0 for v in values));self.assertEqual(centered_synthetic_p(0,values,domain=D),1)
 def test_financial_guard_before_IO(self):
  with patch('builtins.open',side_effect=AssertionError('No financial read')):
   with self.assertRaises(BlockedError):financial_statistics_entrypoint(approved=True)
  with self.assertRaises(BlockedError):moving_block_indices(200,20,np.random.default_rng(2),domain='FINANCIAL')
if __name__=='__main__':unittest.main(verbosity=2)
