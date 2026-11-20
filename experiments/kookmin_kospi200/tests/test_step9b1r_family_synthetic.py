from pathlib import Path
import sys,unittest
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step9b1r_family_synthetic import prep,metrics,influence
from kospi200.step9b1r_synthetic import BA_components
class Family(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  rng=np.random.default_rng(42);cls.y=np.tile([0,1],500);cls.p=rng.uniform(.1,.9,(52,1000));cls.o=np.repeat(np.arange(5),200);cls.f,_=prep(cls.y,cls.p,cls.o);cls.obs=metrics(np.ones((1,1000))@cls.f)[0];cls.phi=influence(cls.y,cls.p,cls.o)
 def test01_complete20_80(self):self.assertEqual(self.obs.shape,(100,));self.assertEqual(self.phi.shape,(1000,100))
 def test02_contamination_gradient_all_metrics(self):
  for i in [0,199,200,999]:
   w=np.ones((1,1000));w[0,i]+=.001;derivative=(metrics(w@self.f)[0]-self.obs)*1000/.001;self.assertTrue(np.allclose(derivative,self.phi[i],rtol=.002,atol=2e-5))
 def test03_BA_IF_matches_exact_seed_metric(self):
  c=BA_components(self.y,self.p[:10],self.p[50],self.o,domain='SYNTHETIC_ONLY');self.assertAlmostEqual(c['effect'],self.obs[0],places=13);self.assertTrue(np.allclose(c['phi'],self.phi[:,0],atol=1e-13))
 def test04_AB_joint_dependence(self):
  primary=self.obs[:20].reshape(5,2,2);self.assertTrue(np.array_equal(primary[:,:,0],primary[:,:,1]))
if __name__=='__main__':unittest.main(verbosity=2)
