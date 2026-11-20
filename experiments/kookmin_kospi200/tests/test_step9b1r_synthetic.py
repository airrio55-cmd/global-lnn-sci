"""Independent synthetic regression only; no market-array or model access."""
from pathlib import Path
import sys,unittest
from unittest.mock import patch
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step9b1r_synthetic import *
from kospi200.step9b1_synthetic import bootstrap_BA
D='SYNTHETIC_ONLY'
class Redesign(unittest.TestCase):
 def fixture(self):
  rng=np.random.default_rng(12);n=1000;y=np.tile([0,1],500);p=rng.random((10,n));b=rng.random(n);o=np.repeat(np.arange(5),200);return y,p,b,o
 def test01_exact_estimand_matches_frozen_reference(self):
  y,p,b,o=self.fixture();c=BA_components(y,p,b,o,domain=D);v,_=bootstrap_BA(y,p,b,o,np.arange(1000)[None,:],domain=D);self.assertAlmostEqual(c['effect'],v[0],places=14)
 def test02_fast_resampling_matches_original_metric(self):
  y,p,b,o=self.fixture();c=BA_components(y,p,b,o,domain=D);idx=indices(1000,30,'MBB40',np.random.default_rng(2),domain=D);a=BA_bootstrap(c,idx,domain=D);v,_=bootstrap_BA(y,p,b,o,idx,domain=D);self.assertTrue(np.allclose(a,v,equal_nan=True,atol=1e-14))
 def test03_no_probability_ensemble(self):
  y,p,b,o=self.fixture();y[:]=np.tile([0,0,0,1],250);p[:5]=.01;p[5:]=.51;b[:]=.6;c=BA_components(y,p,b,o,domain=D);self.assertEqual(c['effect'],0);self.assertTrue(np.all((p>.5).mean(axis=0)==.5));self.assertTrue(np.all(p.mean(axis=0)<.5))
 def test04_unequal_Origin_equal_weight(self):
  y,p,b,o=self.fixture();o=np.repeat(np.arange(5),[100,150,200,250,300]);b[:]=.6;p[:]=b;p[:,o==0]=np.where(y[o==0],.9,.1);self.assertAlmostEqual(BA_components(y,p,b,o,domain=D)['effect'],.1)
 def test05_MBB_contiguous(self):
  for L in [20,40,60]:
   x=indices(1000,10,f'MBB{L}',np.random.default_rng(2),domain=D)
   for i in range(0,1000,L):self.assertTrue(np.all(np.diff(x[:,i:i+L],axis=1)==1))
 def test06_stationary_geometric_restarts(self):
  x=indices(1000,200,'STATIONARY40',np.random.default_rng(2),domain=D);continuity=(x[:,1:]==(x[:,:-1]+1)%1000).mean();self.assertTrue(.96<continuity<.985)
 def test07_local_window_bounds(self):
  x=indices(1000,10,'LOCAL40_W100',np.random.default_rng(2),domain=D);self.assertTrue(np.all(np.abs(x[:,::40]-np.arange(0,1000,40))<=100))
 def test08_IF_centered_within_Origins(self):
  y,p,b,o=self.fixture();c=BA_components(y,p,b,o,domain=D)
  for k in range(5):self.assertAlmostEqual(c['phi'][o==k].mean(),0,places=13)
 def test09_HAC_matches_multiplier_covariance_identity(self):
  y,p,b,o=self.fixture();phi=BA_components(y,p,b,o,domain=D)['phi'];q=40;coeff=np.convolve(phi,np.ones(q+1)/np.sqrt(q+1));self.assertAlmostEqual(hac_se(phi,q),np.linalg.norm(coeff)/len(phi),places=13)
 def test10_rare_class_not_repaired(self):
  y,p,b,o=self.fixture();y[o==0]=1;self.assertIsNone(BA_components(y,p,b,o,domain=D))
 def test11_minimum_support_exclusion_is_explicit(self):
  y,p,b,o=self.fixture();y[:200]=1;y[0]=0;c=BA_components(y,p,b,o,domain=D);r=infer(c,'HAC40',np.random.default_rng(2),domain=D);self.assertEqual(r['status'],'BLOCKED');self.assertEqual(r['reason'],'minimum_observed_class_support_below10')
 def test12_seed_count_not_dates(self):
  y,p,b,o=self.fixture();c=BA_components(y,p,b,o,domain=D);self.assertEqual(len(c['phi']),1000);self.assertEqual(c['features'].shape,(1000,20))
 def test13_reproducible_rng(self):self.assertTrue(np.array_equal(indices(1000,10,'STATIONARY40',np.random.default_rng(2),domain=D),indices(1000,10,'STATIONARY40',np.random.default_rng(2),domain=D)))
 def test14_family_pairing_same_index(self):
  idx=indices(1000,10,'MBB40',np.random.default_rng(2),domain=D);a=np.arange(1000);self.assertTrue(np.all((a+100)[idx]-a[idx]==100))
 def test15_financial_entrypoint_before_IO(self):
  with patch('builtins.open',side_effect=AssertionError('No finance read')):
   with self.assertRaises(BlockedError):financial_entrypoint(approved=True)
  with self.assertRaises(BlockedError):indices(1000,10,'MBB40',np.random.default_rng(2),domain='FINANCIAL')
 def test16_no_torch_HMM_imports(self):self.assertNotIn('torch',sys.modules);self.assertNotIn('hmmlearn',sys.modules)
if __name__=='__main__':unittest.main(verbosity=2)
