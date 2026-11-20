"""Synthetic-only calendar-aware paired block statistics. No financial release."""
import numpy as np
from .data import BlockedError
MODELS=['RNN','LSTM','GRU','LTC','CfC'];BASELINES=['MOMENTUM60','CLIMATOLOGY'];SECONDARY=['macro_f1','brier','recall0','recall1']
def families():
 return {'primary':[{'NN':n,'baseline':b,'candidate':c,'metric':'BA'} for n in MODELS for b in BASELINES for c in ['A','B']], 'secondary':[{'NN':n,'baseline':b,'candidate':c,'metric':m} for n in MODELS for b in BASELINES for c in ['A','B'] for m in SECONDARY]}
def synthetic_only(domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('STEP9B1 financial statistics prohibited')
def block_indices(n,L,B,rng,*,session_ids=None,domain):
 synthetic_only(domain)
 if not 1<=L<=n or B<1:raise BlockedError('Invalid synthetic block budget')
 ids=np.arange(n) if session_ids is None else np.asarray(session_ids)
 if len(ids)!=n or not np.all(np.diff(ids)==1):raise BlockedError('Noncontiguous official-session index; no gap bridging')
 starts=rng.integers(0,n-L+1,size=(B,(n+L-1)//L));return (starts[:,:,None]+np.arange(L)[None,None,:]).reshape(B,-1)[:,:n]
def bootstrap_BA(y,prob,baseline,origin,indices,*,domain):
 synthetic_only(domain);y=np.asarray(y);p=np.asarray(prob);b=np.asarray(baseline);o=np.asarray(origin);idx=np.asarray(indices);n=len(y)
 if p.ndim!=2 or p.shape[1]!=n or b.shape!=(n,) or o.shape!=(n,) or idx.ndim!=2 or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or not np.isfinite(b).all() or (p<0).any() or (p>1).any() or (b<0).any() or (b>1).any():raise BlockedError('Malformed synthetic arrays')
 names=np.unique(o)
 if len(names)!=5:raise BlockedError('Exactly5Origin synthetic estimand required')
 preds=np.vstack([p>.5,b>.5]);S=p.shape[0];cols=[]
 for name in names:
  pos=(o==name)&(y==1);neg=(o==name)&(y==0);cols.extend([pos,neg]);cols.extend(pos[None,:]&preds);cols.extend(neg[None,:]&~preds)
 f=np.asarray(cols,dtype=float).T;freq=np.zeros((len(idx),n));np.add.at(freq,(np.repeat(np.arange(len(idx)),n),idx.ravel()),1);counts=freq@f;v=counts.reshape(len(idx),5,2+2*(S+1));positive=v[:,:,0];negative=v[:,:,1];valid=np.all((positive>0)&(negative>0),axis=1)
 with np.errstate(invalid='ignore',divide='ignore'):
  ba=.5*(v[:,:,2:2+S+1]/positive[:,:,None]+v[:,:,2+S+1:]/negative[:,:,None]);effect=(ba[:,:,:S].mean(axis=2)-ba[:,:,S]).mean(axis=1)
 effect[~valid]=np.nan;return effect,valid

def family_inference(observed,replicates,*,domain):
 synthetic_only(domain);obs=np.asarray(observed,dtype=float);z=np.asarray(replicates,dtype=float)
 if obs.ndim!=1 or z.ndim!=2 or z.shape[1]!=len(obs) or not np.isfinite(obs).all():raise BlockedError('Incomplete family/observed estimand')
 valid=np.isfinite(z).all(axis=1);ratio=1-valid.mean()
 if ratio>.1 or valid.sum()<int(np.ceil(.9*len(z))):return {'status':'BLOCKED','valid':int(valid.sum()),'invalid':int((~valid).sum())}
 a=z[valid];p=(1+(np.abs(a-obs)>=np.abs(obs)).sum(axis=0))/(len(a)+1);order=np.argsort(p,kind='stable');holm=np.empty_like(p);holm[order]=np.minimum(1,np.maximum.accumulate(p[order]*np.arange(len(p),0,-1)));return {'status':'PASS','valid':int(valid.sum()),'invalid':int((~valid).sum()),'p':p,'Holm':holm,'CI95_marginal':np.quantile(a,[.025,.975],axis=0),'conditional_MCSE':np.sqrt(p*(1-p)/(len(a)+1))}

def financial_entrypoint(*args,**kwargs):raise BlockedError('STEP9B1 financial budget0; independent STEP9B2 approval and design review required')

def validate_families(spec,*,domain):
 synthetic_only(domain)
 if spec!=families():raise BlockedError('All20Primary/80Secondary hypotheses required; no omitted pairs')
 return True

def holm_known(p,*,domain):
 synthetic_only(domain);x=np.asarray(p,dtype=float)
 if x.ndim!=1 or not np.isfinite(x).all() or np.any((x<0)|(x>1)):raise BlockedError('Incomplete/invalid synthetic family')
 order=np.argsort(x,kind='stable');z=np.empty_like(x);z[order]=np.minimum(1,np.maximum.accumulate(x[order]*np.arange(len(x),0,-1)));return z
