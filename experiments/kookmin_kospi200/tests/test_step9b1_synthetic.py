"""Structural tests on independent synthetic arrays; no financial files."""
from pathlib import Path
import sys,unittest,copy
from unittest.mock import patch
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step9b1_synthetic import *
from kospi200.step9a_synthetic import paired_origin_effect
D='SYNTHETIC_ONLY'
class Design(unittest.TestCase):
 def fixture(self):
  rng=np.random.default_rng(2);y=np.tile([0,1],250);o=np.repeat(np.arange(5),100);p=rng.uniform(.1,.9,(10,500));b=rng.uniform(.1,.9,500);return y,p,b,o
 def idx(self,L=20):return block_indices(500,L,25,np.random.Generator(np.random.PCG64(20261120)),domain=D)
 def test01_paired_alignment(self):
  a=self.idx();x=np.arange(500);self.assertTrue(np.array_equal((x+20)[a]-x[a],np.full(a.shape,20)))
 def test02_seed_metric_average(self):
  y,p,b,o=self.fixture();a,v=bootstrap_BA(y,p,b,o,np.arange(500)[None,:],domain=D);ref=paired_origin_effect(y,p,b,o,np.arange(500),'BA',domain=D);self.assertAlmostEqual(a[0],ref)
 def test03_not_ensemble_metric(self):
  y,p,b,o=self.fixture();y[:]=np.tile([0,0,0,1],125);p[:5]=.01;p[5:]=.51;b[:]=.6
  self.assertAlmostEqual(paired_origin_effect(y,p,b,o,np.arange(500),'accuracy',domain=D),.25)
 def test04_five_Origin_equal_weight(self):
  o=np.repeat(np.arange(5),[40,80,100,120,160]);y=np.tile([0,1],250);b=np.full(500,.6);p=np.tile(b,(10,1));p[:,o==0]=np.where(y[o==0],.9,.1);a,v=bootstrap_BA(y,p,b,o,np.arange(500)[None,:],domain=D);self.assertAlmostEqual(a[0],.1)
 def test05_within_block_contiguity(self):
  for L in [20,40,60]:
   idx=self.idx(L)
   for start in range(0,500,L):self.assertTrue(np.all(np.diff(idx[:,start:min(start+L,500)],axis=1)==1))
 def test06_year_boundary_label_overlap(self):
  idx=block_indices(1000,40,40,np.random.default_rng(2),domain=D);self.assertTrue(np.any((idx[:,:-1]==199)&(idx[:,1:]==200)));self.assertEqual(len(set(range(200,220))&set(range(201,221))),19)
 def test07_common_index_all_pairs(self):
  a=self.idx();one=np.arange(500);self.assertTrue(np.array_equal(one[a],one[a.copy()]))
 def test08_AB_shared_date_dependence(self):
  a=self.idx();A=np.arange(500);B=A+100;self.assertTrue(np.all(B[a]-A[a]==100))
 def test09_oneclass_truth_null(self):
  y,p,b,o=self.fixture();y[o==0]=1;a,v=bootstrap_BA(y,p,b,o,np.arange(500)[None,:],domain=D);self.assertFalse(v[0]);self.assertTrue(np.isnan(a[0]))
 def test10_constant_prediction_valid(self):
  y,p,b,o=self.fixture();p[:]=.6;b[:]=.6;a,v=bootstrap_BA(y,p,b,o,np.arange(500)[None,:],domain=D);self.assertTrue(v[0]);self.assertEqual(a[0],0)
 def test11_common_invalid_mask(self):
  z=np.zeros((100,20));z[0,3]=np.nan;r=family_inference(np.zeros(20),z,domain=D);self.assertEqual(r['valid'],99);self.assertEqual(len(r['p']),20)
 def test12_missing_Origin_BLOCKED(self):
  y,p,b,o=self.fixture();idx=np.tile(np.arange(100),5)[None,:];a,v=bootstrap_BA(y,p,b,o,idx,domain=D);r=family_inference([0],a[:,None],domain=D);self.assertEqual(r['status'],'BLOCKED')
 def test13_plus_one(self):self.assertEqual(family_inference([1],np.ones((100,1)),domain=D)['p'][0],1/101)
 def test14_Holm_known_example(self):self.assertTrue(np.allclose(holm_known([.01,.04,.03],domain=D),[.03,.06,.06]))
 def test15_PCG64_reproducible(self):self.assertTrue(np.array_equal(self.idx(),self.idx()))
 def test16_complete_families(self):
  f=families();self.assertEqual(len(f['primary']),20);self.assertEqual(len(f['secondary']),80);self.assertTrue(validate_families(f,domain=D));f['primary'].pop()
  with self.assertRaises(BlockedError):validate_families(f,domain=D)
 def test17_calendar_gap_rejected(self):
  ids=np.arange(500);ids[250:]+=1
  with self.assertRaises(BlockedError):block_indices(500,20,10,np.random.default_rng(2),session_ids=ids,domain=D)
 def test18_invalid_ratio_boundary(self):
  a=np.zeros((100,20));a[:10,0]=np.nan;self.assertEqual(family_inference(np.zeros(20),a,domain=D)['status'],'PASS');a[10,0]=np.nan;self.assertEqual(family_inference(np.zeros(20),a,domain=D)['status'],'BLOCKED')
 def test19_synthetic_alternative_direction(self):
  y,p,b,o=self.fixture();p[:]=np.where(y,.9,.1);b[:]=.6;a,v=bootstrap_BA(y,p,b,o,np.arange(500)[None,:],domain=D);self.assertAlmostEqual(a[0],.5)
 def test20_marginal_CI_not_simultaneous(self):
  a=np.tile(np.linspace(-1,1,101)[:,None],(1,20));r=family_inference(np.zeros(20),a,domain=D);self.assertEqual(r['CI95_marginal'].shape,(2,20))
 def test21_financial_entrypoint_before_IO(self):
  with patch('builtins.open',side_effect=AssertionError('No financial read')):
   with self.assertRaises(BlockedError):financial_entrypoint(approved=True)
  with self.assertRaises(BlockedError):self.idx_financial()
 def idx_financial(self):return block_indices(500,20,10,np.random.default_rng(2),domain='FINANCIAL')
 def test22_old_metric_source_import_only(self):
  self.assertNotIn('torch',sys.modules);self.assertNotIn('hmmlearn',sys.modules)
if __name__=='__main__':unittest.main(verbosity=2)
