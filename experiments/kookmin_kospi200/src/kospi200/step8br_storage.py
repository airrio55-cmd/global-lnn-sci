"""Versioned STEP8B-R strict NPZ schema and full atomic roundtrip, no pickle."""
from pathlib import Path
import os,re,hashlib,json
import numpy as np
from .data import BlockedError
SCHEMA={'train_x':('float64','N,2'),'train_y':('int64','N'),'test_x':('float64','M,2'),'test_y':('int64','M'),'dates':('<U10','M'),'session_id':('int64','M'),'label_end':('<U10','M'),'price_close':('float64','K'),'price_dates':('<U10','K')}
def schema_sha():return hashlib.sha256(json.dumps(SCHEMA,sort_keys=True).encode()).hexdigest()
def validate_payload(a):
 if set(a)!=set(SCHEMA):raise BlockedError('Unexpected/missing persisted fields')
 n=len(a['train_y']);m=len(a['test_y']);k=len(a['price_close']);dims={'N':n,'M':m,'K':k,'2':2}
 if min(n,m,k)<=0:raise BlockedError('Empty input')
 for name,(dtype,shape) in SCHEMA.items():
  x=np.asarray(a[name]);expected=tuple(dims[v] for v in shape.split(','))
  if x.dtype.hasobject or x.dtype.fields is not None or x.dtype!=np.dtype(dtype) or x.shape!=expected:raise BlockedError('Unsafe dtype/shape: '+name)
  if x.dtype.kind in 'if' and not np.isfinite(x).all():raise BlockedError('Nonfinite numeric field')
  if x.dtype.kind=='U':
   for d in x:
    s=str(d)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',s) or s<'2010-01-01' or s>'2025-12-31':raise BlockedError('Malformed/out-of-period date')
    try:parsed=np.datetime64(s,'D')
    except ValueError as e:raise BlockedError('Invalid calendar date') from e
    if str(parsed)!=s:raise BlockedError('Noncanonical date')
   if len(set(map(str,x)))!=len(x) or np.any(x[1:]<=x[:-1]):raise BlockedError('Duplicate/unsorted dates')
 if not np.isin(a['train_y'],[0,1]).all() or not np.isin(a['test_y'],[0,1]).all() or np.any(a['price_close']<=0):raise BlockedError('Invalid label/price')
 ids=a['session_id']
 if np.any(ids<0) or np.any(ids>=k) or not np.all(np.diff(ids)==1):raise BlockedError('Invalid official Test session sequence')
 if not np.array_equal(a['price_dates'][ids],a['dates']):raise BlockedError('Price/Test date alignment mismatch')
 return True

def full_read(path):
 with np.load(path,allow_pickle=False) as z:a={name:z[name].copy() for name in z.files}
 validate_payload(a);return a

def atomic_roundtrip(path,expected):
 path=Path(path);validate_payload(expected)
 if path.exists():raise BlockedError('Existing versioned input cannot be replaced')
 path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_name(path.name+'.pending')
 if temp.exists():raise BlockedError('Uncommitted input already exists')
 with temp.open('xb') as f:np.savez(f,**expected);f.flush();os.fsync(f.fileno())
 before=hashlib.file_digest(temp.open('rb'),'sha256').hexdigest();actual=full_read(temp)
 if any(not np.array_equal(actual[k],expected[k]) or actual[k].dtype!=expected[k].dtype for k in expected):raise BlockedError('Roundtrip changed a field')
 if hashlib.file_digest(temp.open('rb'),'sha256').hexdigest()!=before:raise BlockedError('Input bytes changed during roundtrip')
 os.replace(temp,path)
 return {'sha256':before,'fields_actually_reread':len(actual),'all_fields_equal':True,'schema_sha256':schema_sha(),'allow_pickle':False,'finalized_after_PASS':True}
