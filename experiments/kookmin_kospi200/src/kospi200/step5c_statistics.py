"""STEP5C v1: frozen moving blocks, STEP5B null policy, paired FP64 metrics.

No file/model I/O. Seeds are averaged after per-seed metrics; never probabilities.
"""
import numpy as np
from .data import BlockedError
from .step5b_policy import test_metrics
from .statistics import holm
VERSION='STEP5C_STATISTICS_ADAPTER_V1'
METRICS=['BA','macro_f1','brier','recall0','recall1']
MODELS=['RNN','LSTM','GRU','LTC','CfC']
SEEDS=[2,12,22,32,42,52,62,72,82,92]
def validate_packet(y,p,sid):
 y=np.asarray(y);p=np.asarray(p);sid=np.asarray(sid)
 if y.ndim!=1 or p.ndim!=3 or p.shape[0]!=len(y) or sid.shape!=y.shape or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or ((p<0)|(p>1)).any():raise BlockedError('Invalid paired label/probability packet')
 if not np.issubdtype(sid.dtype,np.integer) or len(set(sid.tolist()))!=len(sid) or np.any(np.diff(sid)<=0):raise BlockedError('Duplicate/nonmonotone session IDs')
 return True

def metric_counts(y,p,weights):
 """B×dates frequency weights -> B×5metrics×models. Seed metrics remain distinct."""
 y=np.asarray(y);p=np.asarray(p,dtype=np.float64);w=np.asarray(weights,dtype=np.float64)
 if y.ndim!=1 or p.ndim!=3 or p.shape[0]!=len(y) or w.ndim!=2 or w.shape[1]!=len(y) or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or ((p<0)|(p>1)).any() or not np.isfinite(w).all() or (w<0).any():raise BlockedError('Invalid metric/count input')
 b,n=w.shape;m,s=p.shape[1:]
 if n==0:return np.full((b,5,m),np.nan)
 positive=(p>.5).astype(float);shape=(b,m,s);n1=(w@y)[:,None,None];total=w.sum(1)[:,None,None];n0=total-n1
 tp=(w@(positive*y[:,None,None]).reshape(n,-1)).reshape(shape);pred=(w@positive.reshape(n,-1)).reshape(shape);fp=pred-tp;fn=n1-tp;tn=n0-fp
 def div(x,d):
  shape=np.broadcast_shapes(x.shape,d.shape);return np.divide(x,d,out=np.full(shape,np.nan),where=np.broadcast_to(d,shape)>0)
 r0=div(tn,n0);r1=div(tp,n1);ba=(r0+r1).mean(-1)/2
 f0=div(2*tn,2*tn+fp+fn);f1=div(2*tp,2*tp+fp+fn);mf=np.concatenate([f0,f1],axis=-1).mean(-1);both=((n0>0)&(n1>0))[:,:,0];mf=np.where(both,mf,np.nan)
 loss=(p-y[:,None,None])**2;br=div((w@loss.reshape(n,-1)).reshape(shape),total).mean(-1)
 return np.stack([ba,mf,br,r0.mean(-1),r1.mean(-1)],axis=1)
def observed_metrics(y,p):return metric_counts(y,p,np.ones((1,len(y))))[0]
def scalar_reference(y,p):
 """Literal STEP5B per-seed score then mean, synthetic parity reference."""
 result=np.full((5,p.shape[1]),np.nan)
 for m in range(p.shape[1]):
  scores=[test_metrics(y,p[:,m,s]) for s in range(p.shape[2])]
  for i,key in enumerate(METRICS):
   if all(x[key] is not None for x in scores):result[i,m]=np.mean([x[key] for x in scores])
 return result

def contiguous_starts(sid,length):
 sid=np.asarray(sid)
 if length not in [20,40,60] or not np.issubdtype(sid.dtype,np.integer) or len(np.unique(sid))!=len(sid) or np.any(np.diff(sid)<=0):raise BlockedError('Invalid block/session contract')
 possible=np.array([i for i in range(len(sid)-length+1) if np.array_equal(sid[i:i+length],np.arange(sid[i],sid[i]+length))],dtype=np.int64)
 if not len(possible):raise BlockedError('No eligible consecutive-session block')
 return possible

def draw_weights(rng,sid,length):
 possible=contiguous_starts(sid,length);return weights_from_starts(rng,possible,len(sid),length)
def weights_from_starts(rng,possible,n,length):
 # Exactly the original rng.choice(start,size=ceil(n/L)) then concat/truncate rule.
 starts=rng.choice(possible,size=int(np.ceil(n/length)));ix=np.concatenate([np.arange(i,i+length) for i in starts])[:n];return np.bincount(ix,minlength=n).astype(np.float64)
def chunk_indices(rng,sids,length,count):
 """Advance draw-major then Origin-major, matching frozen bootstrap_effect."""
 possible=[contiguous_starts(s,length) for s in sids];weights=[np.empty((count,len(s)),dtype=float) for s in sids]
 for draw in range(count):
  for o,(sid,starts) in enumerate(zip(sids,possible)):weights[o][draw]=weights_from_starts(rng,starts,len(sid),length)
 return weights

def centered_summary(observed,draws,replicates=10000):
 values=np.asarray(draws,dtype=float)
 if len(values)!=replicates:raise BlockedError('Incomplete frozen draw budget')
 valid=values[np.isfinite(values)];invalid=replicates-len(valid);estimable=np.isfinite(observed) and invalid<=.1*replicates and len(valid)>0
 return {'observed_difference':float(observed) if np.isfinite(observed) else None,'ci95_percentile':np.quantile(valid,[.025,.975]).tolist() if len(valid) else None,'p_approx_centered':float((1+np.sum(np.abs(valid-observed)>=abs(observed)))/(len(valid)+1)) if estimable else None,'valid_replicates':len(valid),'invalid_replicates':invalid,'invalid_rate':invalid/replicates,'status':'PASS' if estimable else 'BLOCKED','p_is_finite_replication_approximation':True,'CI_is_simultaneous':False}

def apply_family(rows,expected_keys):
 def key(r):return (r['origin'],r['candidate'],r['model_a'],r['model_b'],r['metric'])
 if len(rows)!=len(expected_keys) or [key(r) for r in rows]!=expected_keys or len(set(expected_keys))!=len(expected_keys):raise BlockedError('Hypothesis family order/size/direction drift')
 complete=all(r['status']=='PASS' and r['p_approx_centered'] is not None for r in rows)
 adjusted=holm([r['p_approx_centered'] for r in rows]) if complete else [None]*len(rows)
 for row,p in zip(rows,adjusted):
  row.update(p_holm=float(p) if p is not None else None,family_status='PASS' if complete else 'BLOCKED',decision='DESCRIPTIVE_APPROX_EVIDENCE' if p is not None and p<.05 else 'SIGNIFICANT_DIFFERENCE_NOT_ESTABLISHED' if p is not None else 'BLOCKED_FAMILY')
 return rows
