"""Synthetic-only roundtrip, schema, recovery approval regression."""
from pathlib import Path
import sys,tempfile,copy,unittest
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step8br_storage import *
from kospi200.step8br_scope import *
def fixture():
 dates=np.asarray([str(np.datetime64('2010-01-01')+np.timedelta64(i,'D')) for i in range(230)],dtype='U10');ids=np.array([200,201],dtype='int64');return {'train_x':np.ones((2,2),dtype='float64'),'train_y':np.array([0,1],dtype='int64'),'test_x':np.ones((2,2),dtype='float64'),'test_y':np.array([0,1],dtype='int64'),'dates':dates[ids],'session_id':ids,'label_end':dates[ids+20],'price_close':np.arange(1,231,dtype='float64'),'price_dates':dates}
class Recovery(unittest.TestCase):
 def test_all_fields_real_roundtrip(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'new.npz';a=fixture();z=atomic_roundtrip(f,a);b=full_read(f);self.assertEqual(z['fields_actually_reread'],9);self.assertTrue(all(np.array_equal(a[k],b[k]) and a[k].dtype==b[k].dtype for k in a));self.assertFalse(z['allow_pickle'])
 def test_object_rejected(self):
  a=fixture();a['price_dates']=a['price_dates'].astype(object)
  with self.assertRaises(BlockedError):validate_payload(a)
 def test_wrong_shape_dtype_finite_and_schema(self):
  for name,v in [('train_x',np.ones((2,20,2))),('session_id',np.array([200.,201.])),('test_x',np.full((2,2),np.nan)),('price_close',np.ones(3))]:
   a=fixture();a[name]=v
   with self.assertRaises(BlockedError):validate_payload(a)
  a=fixture();a['unexpected']=np.array([1])
  with self.assertRaises(BlockedError):validate_payload(a)
 def test_bad_dates_duplicates_2026(self):
  for date in ['2026-01-01','2025-02-30','2010/01/01']:
   a=fixture();a['price_dates'][0]=date
   with self.assertRaises(BlockedError):validate_payload(a)
  a=fixture();a['dates'][1]=a['dates'][0]
  with self.assertRaises(BlockedError):validate_payload(a)
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'new.npz';atomic_roundtrip(f,fixture())
   with self.assertRaises(BlockedError):atomic_roundtrip(f,fixture())
 def test_approval_disjoint_from_old_scope(self):
  ids=[f'{i}_STEP8BR_V1' for i in range(40)];c={'scope':'STEP8BR_RECOVERY40','protocol_sha256':PROTOCOL_SHA,'max_evaluations':40,'max_Logistic_fits':10,'NN_execution':False,'HMM_execution':False,'identities':ids,'request_sha256':'req','prior_STEP8B_status':'BLOCKED40_PRESERVED','prior_evaluations':0};a={'scope':c['scope'],'approved':True,'config_sha256':'c','roster_sha256':'r','source_hashes':{'s':'h'},'request_sha256':'req'};args={'config_sha':'c','roster_sha':'r','source_hashes':{'s':'h'},'identity':ids[0]};self.assertTrue(require_scope(c,a,**args))
  for key,v in [('scope','STEP8B_BASELINES40'),('max_evaluations',41),('max_Logistic_fits',11),('protocol_sha256','changed'),('prior_STEP8B_status','COMPLETED40')]:
   bad=copy.deepcopy(c);bad[key]=v
   with self.assertRaises(BlockedError):require_scope(bad,a,**args)
  with self.assertRaises(BlockedError):require_scope(c,a,**{**args,'identity':'OLD_BASELINE_V1'})
  with self.assertRaises(BlockedError):require_scope(c,a,**{**args,'config_sha':'tampered'})
if __name__=='__main__':unittest.main(verbosity=2)
