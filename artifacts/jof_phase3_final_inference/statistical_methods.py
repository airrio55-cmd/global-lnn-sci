"""Prespecified tests; sign d=loss_A-loss_B throughout."""
import numpy as np
from scipy import stats
from arch.bootstrap import StationaryBootstrap

def hac(moments,lag):
 x=np.asarray(moments,float)
 if x.ndim==1:x=x[:,None]
 x=x-x.mean(0);n=len(x);s=x.T@x/n
 for k in range(1,min(lag,n-1)+1):
  gamma=x[k:].T@x[:-k]/n;s+=(1-k/(lag+1))*(gamma+gamma.T)
 return s

def dm(a,b,h=20,lag=19):
 a=np.asarray(a,float);b=np.asarray(b,float);d=a-b;n=len(d);v=float(hac(d,lag)[0,0]);mean=float(d.mean());factor=np.sqrt((n+1-2*h+h*(h-1)/n)/n)
 result={'Mean_loss_A':a.mean(),'Mean_loss_B':b.mean(),'Mean_differential':mean,'N':n,'HAC_lag':lag,'HLN_factor':factor,'HAC_LR_variance':v}
 if v<=1e-16 or not np.isfinite(v):return {**result,'DM_stat':np.nan,'raw_two_sided_p':np.nan,'Status':'degenerate_variance'}
 z=mean/np.sqrt(v/n);t=z*factor;return {**result,'DM_stat_uncorrected':z,'DM_stat':t,'raw_two_sided_p':2*stats.t.sf(abs(t),n-1),'Status':'defined'}

def gw(a,b,locations,absret,vol,lag=19):
 d=np.asarray(a)-np.asarray(b);loc=np.asarray(locations);j=np.searchsorted(loc,loc-21,side='right')-1;keep=j>=0
 ix=np.where(keep)[0];z=np.column_stack([np.ones(len(ix)),d[j[keep]],absret[loc[keep]-1],vol[loc[keep]-1]])
 assert (loc[j[keep]]+20<=loc[keep]-1).all()
 good=np.isfinite(z).all(1);z=z[good];ix=ix[good]
 # Fixed nonsingular rescaling improves conditioning, leaves Wald statistic invariant.
 z=z/np.array([1.,1.,.01,.01]);g=z*d[ix,None];s=hac(g,lag);rank=np.linalg.matrix_rank(s);n=len(g)
 result={'N':n,'df':4,'HAC_lag':lag,'Covariance_rank':rank,'Mean_differential':float(d[ix].mean()),'Conditioning':'1,resolved_loss_differential,lagged_abs_Log_Ret,lagged_Vol20','Test_label':'GW-style conditional moment Wald (not exact original GW)'}
 if rank<4 or n<40:return {**result,'GW_stat':np.nan,'raw_p':np.nan,'Status':'singular_or_small_sample'}
 stat=float(n*g.mean(0)@np.linalg.solve(s,g.mean(0)));return {**result,'GW_stat':stat,'raw_p':stats.chi2.sf(stat,4),'Status':'defined'}

def holm(p):
 p=np.asarray(p,float);valid=np.isfinite(p);inputs=np.where(valid,p,1.);order=np.argsort(inputs,kind='stable');adjusted=np.empty(len(p));adjusted[order]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*inputs[order]));adjusted[~valid]=np.nan;return adjusted

def spa(losses,benchmark_index=8,reps=10000,block=20,seed=20261106):
 values=np.asarray(losses,float);b=values[:,benchmark_index];alternatives=np.delete(values,benchmark_index,axis=1);g=b[:,None]-alternatives;n,k=g.shape
 bs=StationaryBootstrap(block,np.arange(n),seed=seed);means=np.empty((reps,k))
 for i,data in enumerate(bs.bootstrap(reps)):means[i]=g[data[0][0]].mean(0)
 variance=n*means.var(0);sigma=np.sqrt(variance);good=sigma>1e-12
 if not good.all():raise ValueError('SPA degenerate variance: preserve all alternatives and report rather than silently dropping')
 mu=g.mean(0);observed=max(0.,float(np.max(np.sqrt(n)*mu/sigma)))
 center=np.where(mu>=-sigma/np.sqrt(n)*np.sqrt(2*np.log(np.log(n))),mu,0.)
 simulated=np.maximum(0,np.max(np.sqrt(n)*(means-center)/sigma,axis=1));p=(1+np.sum(simulated>=observed))/(reps+1)
 return {'SPA_statistic':observed,'p_value':float(p),'Alternative_count':k,'Mean_improvements':mu,'LR_variance':variance,'Reps':reps,'Bootstrap':'stationary','Block_length':block,'Seed':seed},means,mu
