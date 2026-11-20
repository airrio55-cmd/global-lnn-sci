"""Synthetic-only redesign experiment. No financial input or execution release."""
import math
import numpy as np
from .data import BlockedError
METHODS=['MBB20','MBB40','MBB60','STATIONARY40','STATIONARY120','LOCAL40_W100','HAC40','HAC120','MULTIPLIER120']
def guard(domain):
 if domain!='SYNTHETIC_ONLY':raise BlockedError('Financial bootstrap/CI/pvalues are not authorized')
def indices(n,B,method,rng,*,domain):
 guard(domain)
 if B<1 or n<200:raise BlockedError('Invalid synthetic size')
 if method.startswith('MBB'):
  L=int(method[3:]);s=rng.integers(0,n-L+1,(B,(n+L-1)//L));return (s[:,:,None]+np.arange(L)).reshape(B,-1)[:,:n]
 if method.startswith('STATIONARY'):
  L=int(method[10:]);idx=np.empty((B,n),dtype=np.int32);starts=rng.integers(0,n,(B,n),dtype=np.int32);restart=rng.random((B,n))<1/L;idx[:,0]=starts[:,0]
  for t in range(1,n):idx[:,t]=np.where(restart[:,t],starts[:,t],(idx[:,t-1]+1)%n)
  return idx
 if method=='LOCAL40_W100':
  L=40;positions=np.arange((n+L-1)//L)*L;lo=np.maximum(0,positions-100);hi=np.minimum(n-L,positions+100);s=lo[None,:]+(rng.random((B,len(lo)))*(hi-lo+1)[None,:]).astype(int);return (s[:,:,None]+np.arange(L)).reshape(B,-1)[:,:n]
 raise BlockedError('Not a resampling method')
def frequency(idx,n):
 return np.bincount((idx+np.arange(len(idx))[:,None]*n).ravel(),minlength=len(idx)*n).reshape(len(idx),n).astype(float)
def BA_components(y,p,b,o,*,domain):
 guard(domain);y=np.asarray(y);p=np.asarray(p);b=np.asarray(b);o=np.asarray(o);n=len(y)
 if p.ndim!=2 or p.shape[1]!=n or b.shape!=(n,) or o.shape!=(n,) or len(np.unique(o))!=5 or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or not np.isfinite(b).all():raise BlockedError('Invalid synthetic 5Origin×Seed inputs')
 # BA is linear in the per-Seed class recall rates, not in mean probability.
 positive_difference=(p>.5).mean(axis=0)-(b>.5);negative_difference=-positive_difference;features=[];effect=[];phi=np.zeros(n);supports=[]
 for name in np.unique(o):
  use=o==name;pos=use&(y==1);neg=use&(y==0);a=pos.sum();z=neg.sum();supports.append(min(a,z))
  if not a or not z:return None
  mp=positive_difference[pos].mean();mn=negative_difference[neg].mean();effect.append(.5*(mp+mn));features.extend([pos,neg,pos*positive_difference,neg*negative_difference]);no=use.sum();psi=.5*(pos/(a/no)*(positive_difference-mp)+neg/(z/no)*(negative_difference-mn));phi+=n/(5*no)*psi
 return {'effect':float(np.mean(effect)),'features':np.asarray(features,dtype=float).T,'phi':phi,'minimum_class_support':int(min(supports))}
def BA_bootstrap(component,idx,*,domain):
 guard(domain);n=component['features'].shape[0];v=(frequency(idx,n)@component['features']).reshape(len(idx),5,4);valid=np.all(v[:,:,:2]>0,axis=(1,2))
 with np.errstate(divide='ignore',invalid='ignore'):effect=(.5*(v[:,:,2]/v[:,:,0]+v[:,:,3]/v[:,:,1])).mean(axis=1)
 effect[~valid]=np.nan;return effect

def hac_se(phi,q):
 x=np.asarray(phi);n=len(x);out=float(x@x)
 for lag in range(1,q+1):out+=2*(1-lag/(q+1))*float(x[lag:]@x[:-lag])
 return math.sqrt(max(0,out))/n

def infer(component,method,rng,*,draws=499,domain):
 guard(domain)
 if component is None:return {'status':'BLOCKED','reason':'observed_missing_Origin_class','valid_draws':0,'invalid_draws':draws}
 obs=component['effect'];n=len(component['phi'])
 if method.startswith('HAC') or method.startswith('MULTIPLIER'):
  if component['minimum_class_support']<10:return {'status':'BLOCKED','reason':'minimum_observed_class_support_below10','valid_draws':0,'invalid_draws':0}
  q=int(method.replace('HAC','').replace('MULTIPLIER',''))
  if method.startswith('HAC'):
   se=hac_se(component['phi'],q)
   if se<=0:return {'status':'BLOCKED','reason':'nonpositive_HAC_variance','valid_draws':0,'invalid_draws':0}
   p=math.erfc(abs(obs/se)/math.sqrt(2));ci=[obs-1.959963984540054*se,obs+1.959963984540054*se];return {'status':'PASS','p':p,'CI':ci,'valid_draws':0,'invalid_draws':0,'variance_type':'BA influence-function Bartlett-HAC Gaussian-Wald'}
  coeff=np.convolve(component['phi'],np.ones(q+1)/math.sqrt(q+1));rep=obs+(rng.normal(size=(draws,len(coeff)))@coeff)/n
 else:
  idx=indices(n,draws,method,rng,domain=domain);rep=BA_bootstrap(component,idx,domain=domain)
 valid=np.isfinite(rep);V=int(valid.sum());invalid=len(rep)-V
 if invalid/len(rep)>.1:return {'status':'BLOCKED','reason':'more_than10percent_invalid_draws','valid_draws':V,'invalid_draws':invalid}
 values=rep[valid];p=(1+np.sum(np.abs(values-obs)>=abs(obs)))/(V+1);return {'status':'PASS','p':float(p),'CI':np.quantile(values,[.025,.975]).tolist(),'valid_draws':V,'invalid_draws':invalid,'variance_type':'BA_IF_Gaussian_multiplier' if method.startswith('MULTIPLIER') else 'resampled_exact_BA_metric'}

def financial_entrypoint(*args,**kwargs):raise BlockedError('STEP9B1R financial fit/forward/draw/pvalue/CI budgets0')
