"""Independent synthetic DGP definitions; rho is binary Markov-error persistence.
No financial arrays, checkpoints, or market files are read.
"""
import numpy as np
N=1000
S=10
def errors(q,rho,rng):
 state=rng.random(11)<q[0];out=np.empty((11,len(q)),dtype=bool);out[:,0]=state
 for t in range(1,len(q)):state=rng.random(11)<rho*state+(1-rho)*q[t];out[:,t]=state
 return out

def make(name,rng):
 ret=rng.normal(size=N+20);y=(np.convolve(ret[1:],np.ones(20),mode='valid')>0).astype(int);o=np.repeat(np.arange(5),200);rho=.7;qb=np.full(N,.35);qn=qb.copy();target=0.
 if name=='iid_null':y=rng.integers(0,2,N);rho=0
 for code,value in [('AR098',.98),('AR095',.95),('AR09_',.9),('AR07',.7)]:
  if code in name:rho=value
 if name=='shared_break_null':qb[:500]=.15;qb[500:]=.45;qn=qb.copy()
 if name=='crossing_break_null':y=rng.integers(0,2,N);rho=0;qb[:500]=.15;qb[500:]=.55;qn=qb[::-1].copy()
 if name=='advantage_reversal_null':y=rng.integers(0,2,N);rho=0;qn=np.repeat([.15,.25,.35,.45,.55],200)
 if name=='prevalence_shift_null':y=(rng.random(N)<np.r_[np.full(500,.1),np.full(500,.9)]).astype(int)
 if name=='rare03_null':y=(rng.random(N)<.97).astype(int)
 if name=='rare10_null':y=(rng.random(N)<.9).astype(int)
 if name=='Origin_support_imbalance_null':y=(rng.random(N)<np.repeat([.03,.1,.5,.9,.97],200)).astype(int)
 if name=='unequal_Origin_sizes_null':o=np.repeat(np.arange(5),[100,150,200,250,300])
 for code,value in [('delta002',.02),('delta005',.05),('delta010',.1)]:
  if code in name:qn=qb-value;target=value
 e=errors(qn,rho,rng)[:10];eb=errors(qb,rho,rng)[10]
 if name in ['high_Seed_corr_null','shared_AB_error_null']:
  shared=errors(qn,rho,rng)[0];e=np.where(rng.random(e.shape)<.9,shared[None,:],e)
  if name=='shared_AB_error_null':eb=np.where(rng.random(N)<.6,shared,eb)
 p=np.where(y[None,:]^e,.7,.3);b=np.where(y^eb,.7,.3);return y,p,b,o,target

def family_data(name,rng):
 y,_,_,o,_=make(name,rng);q=np.full(N,.35)
 if name=='shared_break_null':q[:500]=.15;q[500:]=.45
 rho=.95 if 'AR095' in name else .7;out=[];common=errors(q,rho,rng)[0]
 for _ in range(5):out.extend(errors(q,rho,rng)[:10])
 out.extend(errors(q,rho,rng)[-2:]);e=np.asarray(out);e=np.where(rng.random(e.shape)<.5,common[None,:],e);p=np.where(y[None,:]^e,.7,.3);return y,p,o

def gaussian_null(rho,rng):
 import statistics
 threshold=statistics.NormalDist().inv_cdf(.65)
 ret=rng.normal(size=N+20);y=(np.convolve(ret[1:],np.ones(20),mode='valid')>0).astype(int);z=np.empty((11,N));z[:,0]=rng.normal(size=11)
 for t in range(1,N):z[:,t]=rho*z[:,t-1]+np.sqrt(1-rho*rho)*rng.normal(size=11)
 e=z>threshold;p=np.where(y[None,:]^e[:10],.7,.3);b=np.where(y^e[10],.7,.3);return y,p,b,np.repeat(np.arange(5),N//5),0.
