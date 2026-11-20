"""Synthetic serialization regression only, no market reads or fitting."""
from pathlib import Path
import sys,unittest,io
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.step8b_storage_gate import inspect_safe_npz,BlockedError
class Storage(unittest.TestCase):
 def test_object_dates_rejected_before_release(self):
  b=io.BytesIO();np.savez(b,dates=np.array(['2020-01-02'],dtype=object));b.seek(0)
  with self.assertRaises(BlockedError):inspect_safe_npz(b)
 def test_Unicode_dates_and_numeric_inputs_accepted(self):
  b=io.BytesIO();np.savez(b,dates=np.array(['2020-01-02'],dtype='U10'),x=np.ones((1,2)));b.seek(0);s=inspect_safe_npz(b);self.assertFalse(s['dates']['hasobject']);self.assertEqual(s['x']['shape'],[1,2])
 def test_safe_roundtrip_without_pickle(self):
  b=io.BytesIO();np.savez(b,dates=np.array(['2020-01-02'],dtype='U10'));b.seek(0)
  with np.load(b,allow_pickle=False) as z:self.assertEqual(z['dates'][0],'2020-01-02')
if __name__=='__main__':unittest.main(verbosity=2)
