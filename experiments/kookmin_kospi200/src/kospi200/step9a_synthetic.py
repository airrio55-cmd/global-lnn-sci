"""Draft statistics tested ONLY with synthetic arrays. Financial release is closed."""
import numpy as np
from .data import BlockedError
from .step5b_policy import test_metrics

def moving_block_indices(n,length,rng,*,domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('No financial resampling authorized')
 if not isinstance(n,int) or not isinstance(length,int) or length<1 or length>n:raise BlockedError('Invalid block size')
 starts=rng.integers(0,n-length+1,size=(n+length-1)//length)
 return np.concatenate([np.arange(i,i+length) for i in starts])[:n]

def paired_origin_effect(y,nn_probability,baseline_probability,origin,indices,metric,*,domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('No financial metric computation authorized')
 y=np.asarray(y);p=np.asarray(nn_probability);b=np.asarray(baseline_probability);o=np.asarray(origin);idx=np.asarray(indices)
 if p.ndim!=2 or p.shape[1]!=len(y) or b.shape!=y.shape or o.shape!=y.shape or not np.isfinite(p).all() or not np.isfinite(b).all():raise BlockedError('Synthetic shape/finite mismatch')
 effects=[]
 for name in np.unique(o):
  used=idx[o[idx]==name]
  if not len(used) or np.unique(y[used]).size<2:return None
  nv=[test_metrics(y[used],s[used])[metric] for s in p];bv=test_metrics(y[used],b[used])[metric]
  if any(v is None for v in nv) or bv is None:return None
  effects.append(float(np.mean(nv))-bv)
 return float(np.mean(effects))

def centered_synthetic_p(observed,replicates,*,domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('Financial pvalue budget=0')
 z=np.asarray(replicates,dtype=float)
 if not z.size or not np.isfinite(z).all() or not np.isfinite(observed):raise BlockedError('Invalid synthetic replicates')
 return float((1+np.count_nonzero(np.abs(z-observed)>=abs(observed)))/(len(z)+1))

def holm_synthetic(pvalues,*,domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('Financial Holm budget=0')
 p=np.asarray(pvalues,dtype=float)
 if p.ndim!=1 or not np.isfinite(p).all() or np.any((p<0)|(p>1)):raise BlockedError('Invalid synthetic pvalues')
 order=np.argsort(p,kind='stable');out=np.empty_like(p);out[order]=np.minimum(1,np.maximum.accumulate(p[order]*np.arange(len(p),0,-1)));return out

def financial_statistics_entrypoint(*args,**kwargs):raise BlockedError('STEP9A financial testing disabled; STEP9B draft is not an approved release')
