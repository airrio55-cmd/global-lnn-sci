"""Predeclared date-block effects on supplied predictions only; no data/model loading."""
import numpy as np
import pandas as pd
from .data import BlockedError
from .statistics import holm
METRICS=['balanced_accuracy','macro_f1','brier','recall0','recall1']
def metric(y,p,name):
 y=np.asarray(y);p=np.asarray(p);pred=p>.5
 if p.ndim!=2 or p.shape[0]!=len(y) or not np.isfinite(p).all() or ((p<0)|(p>1)).any() or not np.isin(y,[0,1]).all():raise BlockedError('Invalid paired probability packet')
 if name=='brier':return float(((p-y[:,None])**2).mean())
 if np.unique(y).size<2:return np.nan
 r=[(pred[y==j]==j).mean(axis=0) for j in [0,1]]
 if name=='balanced_accuracy':return float((r[0]+r[1]).mean()/2)
 if name in ['recall0','recall1']:return float(r[int(name[-1])].mean())
 if name=='macro_f1':
  f=[]
  for j in [0,1]:
   tp=((pred==j)&(y[:,None]==j)).sum(0);fp=((pred==j)&(y[:,None]!=j)).sum(0);fn=((pred!=j)&(y[:,None]==j)).sum(0);f.append(2*tp/(2*tp+fp+fn))
  return float(np.mean(f))
 raise BlockedError('Undeclared metric')
def paired_packet(frame,model_a,model_b,*,seeds):
 required={'origin','date','session_id','seed','model','y','probability'}
 if not required.issubset(frame):raise BlockedError('Missing paired date/seed lineage')
 d=frame[frame.model.isin([model_a,model_b])].copy();d['date']=pd.to_datetime(d.date)
 if not d.date.between('2010-01-01','2025-12-31').all() or d.duplicated(['origin','date','seed','model']).any():raise BlockedError('Duplicate/out-of-period rows')
 out=[]
 for origin,g in d.groupby('origin',sort=True):
  if not g.groupby('date').y.nunique().eq(1).all() or not g.groupby('date').session_id.nunique().eq(1).all():raise BlockedError('Label/session mismatch')
  parts=[]
  for m in [model_a,model_b]:
   x=g[g.model==m].pivot(index='date',columns='seed',values='probability').sort_index()
   if set(x.columns)!=set(seeds) or x.isna().any().any():raise BlockedError('Fixed10-seed roster incomplete; no seed pooling/substitution')
   parts.append(x[seeds])
  if not parts[0].index.equals(parts[1].index):raise BlockedError('Nonpaired model dates')
  z=g.drop_duplicates('date').set_index('date').reindex(parts[0].index)
  out.append({'origin':origin,'dates':parts[0].index,'session_id':z.session_id.to_numpy(),'y':z.y.to_numpy(),'a':parts[0].to_numpy(),'b':parts[1].to_numpy()})
 if not out:raise BlockedError('No paired Origin')
 return out

def bootstrap_effect(packets,*,metric_name,block_length,replicates=10000,seed=20261116):
 if block_length not in [20,40,60] or replicates!=10000 or metric_name not in METRICS:raise BlockedError('Frozen bootstrap specification required')
 starts=[]
 for z in packets:
  n=len(z['y']);sid=z['session_id'];possible=np.array([i for i in range(n-block_length+1) if np.array_equal(sid[i:i+block_length],np.arange(sid[i],sid[i]+block_length))])
  if not len(possible):raise BlockedError('No contiguous official-session block of requested length')
  starts.append(possible)
 effect=lambda z,ix:metric(z['y'][ix],z['a'][ix],metric_name)-metric(z['y'][ix],z['b'][ix],metric_name)
 observed=float(np.mean([effect(z,np.arange(len(z['y']))) for z in packets]));rng=np.random.default_rng(seed);values=[];invalid=0
 if not np.isfinite(observed):raise BlockedError('Undefined observed metric')
 for _ in range(replicates):
  diffs=[]
  for z,possible in zip(packets,starts):
   n=len(z['y']);s=rng.choice(possible,size=int(np.ceil(n/block_length)));ix=np.concatenate([np.arange(j,j+block_length) for j in s])[:n];diffs.append(effect(z,ix))
  v=float(np.mean(diffs))
  if np.isfinite(v):values.append(v)
  else:invalid+=1
 if invalid>.1*replicates:raise BlockedError('Undefined bootstrap class denominators >10%; report failure')
 v=np.asarray(values);return {'effect_a_minus_b':observed,'ci95':np.quantile(v,[.025,.975]).tolist(),'p_approx_centered':float((1+np.sum(np.abs(v-observed)>=abs(observed)))/(len(v)+1)),'invalid_replicates':invalid,'valid_replicates':len(v),'market_dates':sum(len(z['y']) for z in packets),'seed_count':packets[0]['a'].shape[1],'block_length':block_length,'metric':metric_name,'brier_lower_is_better':metric_name=='brier','p_is_approximate_not_exact':True}

def correct_frozen_family(rows,*,expected_size):
 from .master_protocol import comparison_family
 pairs={(r['candidate'],r['model_a'],r['model_b']) for r in comparison_family()}
 def key(r):return (r.get('origin','ALL'),r['candidate'],r['model_a'],r['model_b'],r['metric'])
 if expected_size==20:expected={('ALL',*p,'balanced_accuracy') for p in pairs}
 elif expected_size==80:expected={('ALL',*p,m) for p in pairs for m in ['macro_f1','brier','recall0','recall1']}
 elif expected_size==100:expected={(o,*p,'balanced_accuracy') for o in ['O1','O2','O3','O4','O5'] for p in pairs}
 elif expected_size==6:
  import itertools
  expected={('ALL',c,a,b,'balanced_accuracy') for c in ['A','B'] for a,b in itertools.combinations(['LTC_RAW','LTC_LOG','LNN_Ensemble'],2)}
 else:raise BlockedError('Undeclared hypothesis family')
 if len(rows)!=expected_size or {key(r) for r in rows}!=expected:raise BlockedError('Incomplete/duplicate predeclared family; no post-hoc deletion')
 if len({r['block_length'] for r in rows})!=1 or rows[0]['block_length'] not in [20,40,60]:raise BlockedError('Mixed/undeclared block family')
 for r,p in zip(rows,holm([x['p_approx_centered'] for x in rows])):r['p_holm_approx']=float(p)
 return rows
