"""Independent synthetic preflight. Never reads market files or checkpoints."""
from pathlib import Path
import sys,unittest,copy
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step8b_baselines import *
class Synthetic(unittest.TestCase):
 def test_logistic_Train_only(self):
  x=np.arange(80,dtype=float).reshape(40,2)/40;y=np.tile([0,1],20);t=np.ones((4,2));p,a=fit_logistic(x,y,t);q,b=fit_logistic(x,y,t*100);self.assertEqual(a['scaler_mean'],b['scaler_mean']);self.assertEqual(a['coefficients'],b['coefficients']);self.assertEqual(a['scaler_fit_rows'],40);self.assertTrue(np.isfinite(p).all())
 def test_climatology_future_invariant(self):
  y=np.array([1,0,1,1]);p,m=train_climatology(y,3);self.assertTrue(np.array_equal(p,[.75]*3));q,_=train_climatology(y,5);self.assertTrue(np.all(q==p[0]))
 def test_dma200_exact(self):
  c=np.arange(1,251,dtype=float);p,m=rule_probability(c,[199,200],'DMA200');self.assertEqual(m[0],np.mean(c[:200]));self.assertEqual(m[1],np.mean(c[1:201]));self.assertTrue(np.all(p==1))
 def test_momentum60_exact(self):
  c=np.arange(1,101,dtype=float);p,m=rule_probability(c,[60,70],'MOMENTUM60');self.assertTrue(np.array_equal(m,c[[0,10]]));self.assertTrue(np.all(p==1))
 def test_rule_ties(self):
  for model in ['DMA200','MOMENTUM60']:
   p,_=rule_probability(np.ones(220),[200,201],model);self.assertTrue(np.all(p==0))
 def test_future_rules_invariant(self):
  c=np.arange(1,301,dtype=float);v=c.copy();v[220:]*=2
  for model in ['DMA200','MOMENTUM60']:self.assertTrue(np.array_equal(rule_probability(c,[200,210],model)[0],rule_probability(v,[200,210],model)[0]))
 def test_warmup_failure(self):
  for model,idx in [('DMA200',198),('MOMENTUM60',59)]:
   with self.assertRaises(BlockedError):rule_probability(np.ones(250),[idx],model)
 def test_null_policy_and_ties(self):
  m=test_metrics([0,0],[.5,.6]);self.assertIsNone(m['BA']);self.assertIsNone(m['macro_f1']);self.assertIsNone(m['recall1']);self.assertEqual(m['recall0'],.5)
 def test_degenerate_prediction_eligible(self):
  m=test_metrics([0,1],[.4,.4]);self.assertEqual(m['BA'],.5);self.assertEqual(m['prediction_status'],'DEGENERATE_PREDICTION');self.assertIsNotNone(m['macro_f1'])
 def test_clim_single_Train_class(self):
  p,m=train_climatology([1,1],2);self.assertTrue(m['Train_single_class']);self.assertTrue(np.all(p==1))
 def test_lr_single_Train_class_BLOCKED(self):
  with self.assertRaises(BlockedError):fit_logistic(np.ones((4,2)),np.ones(4),np.ones((2,2)))
 def test_alignment_duplicates_and_Target_changes(self):
  d=np.array(['2020-01-02','2020-01-03']);ids=np.array([1,2]);y=np.array([0,1]);e=np.array(['2020-02-03','2020-02-04']);expected=(d,ids,y,e);self.assertTrue(validate_alignment(d,ids,y,e,expected))
  for args in [(d,ids,1-y,e),([d[0],d[0]],ids,y,e),(d,[1,3],y,e)]:
   with self.assertRaises(BlockedError):validate_alignment(*args,expected)
 def test_approval_tampering_and_candidate_mix(self):
  ids=[str(i) for i in range(40)];c={'scope':'STEP8B_BASELINES40','NN_execution':False,'HMM_execution':False,'max_evaluations':40,'max_Logistic_fits':10,'identities':ids,'request_sha256':'r','lr_spec':LR_SPEC,'scaler_contract':'retained_Train_current_t_only','horizon':20,'threshold':.5};a={'scope':c['scope'],'approved':True,'config_sha256':'c','roster_sha256':'j','source_sha256':'s','request_sha256':'r'};self.assertTrue(authorize(c,a,'c','j','s','0'))
  for key,value in [('max_evaluations',41),('max_Logistic_fits',11),('NN_execution',True),('scaler_contract','test'),('lr_spec',{**LR_SPEC,'C':2})]:
   z=copy.deepcopy(c);z[key]=value
   with self.assertRaises(BlockedError):authorize(z,a,'c','j','s','0')
  with self.assertRaises(BlockedError):authorize(c,a,'changed','j','s','0')
  with self.assertRaises(BlockedError):authorize(c,a,'c','j','s','OTHER_CANDIDATE')
 def test_metric_policy_is_frozen_function(self):
  from kospi200.step5b_policy import test_metrics as frozen
  self.assertIs(test_metrics,frozen)
if __name__=='__main__':unittest.main(verbosity=2)
