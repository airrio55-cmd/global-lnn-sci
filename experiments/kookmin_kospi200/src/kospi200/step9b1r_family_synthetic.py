"""Fixed-size synthetic20/80-family metric/IF checks. Not a financial adapter."""
import numpy as np
from .data import BlockedError
N=1000
K=52
def prep(y,p,o):
 pred=p>.5;features=[];groups=[];minsupport=1000
 for origin in range(5):
  use=o==origin;groups.append(use);pos=y==1;neg=~pos;features.append(use);features.extend((use&pos)[None,:]&pred);features.extend((use&pos)[None,:]&~pred);features.extend((use&neg)[None,:]&pred);features.extend((use&neg)[None,:]&~pred);features.extend((p-y[None,:])**2*use[None,:]);minsupport=min(minsupport,int((use&pos).sum()),int((use&neg).sum()))
 return np.asarray(features,dtype=float).T,minsupport

def metrics(count):
 a=count.reshape(len(count),5,1+5*K);n=a[:,:,0];tp=a[:,:,1:1+K];fn=a[:,:,1+K:1+2*K];fp=a[:,:,1+2*K:1+3*K];tn=a[:,:,1+3*K:1+4*K];loss=a[:,:,1+4*K:];valid=np.all((n>0)&((tp+fn)[:,:,0]>0)&((tn+fp)[:,:,0]>0),axis=1)
 with np.errstate(invalid='ignore',divide='ignore'):
  BA=.5*(tp/(tp+fn)+tn/(tn+fp));F1=tp/(2*tp+fn+fp)+tn/(2*tn+fn+fp);Brier=loss/n[:,:,None];r0=tn/(tn+fp);r1=tp/(tp+fn);v=np.stack([BA,F1,Brier,r0,r1],axis=-1);nn=v[:,:,:50].reshape(len(count),5,5,10,5).mean(axis=3);base=v[:,:,50:];delta=(nn[:,:,:,None,:]-base[:,:,None,:,:]).mean(axis=1);delta=np.repeat(delta[:,:,:,None,:],2,axis=3);primary=delta[:,:,:,:,0].reshape(len(count),20);secondary=delta[:,:,:,:,1:].reshape(len(count),80);combined=np.concatenate([primary,secondary],axis=1)
 combined[~valid]=np.nan;return combined

def influence(y,p,o):
 pred=(p>.5).T;phi=np.zeros((N,100))
 for origin in range(5):
  use=o==origin;yy=y[use];pp=p[:,use].T;pr=pred[use];no=len(yy);one=np.stack([(yy[:,None]==1)&pr,(yy[:,None]==1)&~pr,(yy[:,None]==0)&pr,(yy[:,None]==0)&~pr],axis=1).astype(float);mu=one.mean(axis=0);tp,fn,fp,tn=mu;pos=tp+fn;neg=tn+fp;dp=2*tp+fp+fn;dn=2*tn+fp+fn
  if np.any(pos==0) or np.any(neg==0):return None
  g=np.zeros((K,4,5));g[:,0,0]=.5*fn/pos**2;g[:,1,0]=-.5*tp/pos**2;g[:,2,0]=-.5*tn/neg**2;g[:,3,0]=.5*fp/neg**2;g[:,0,1]=1/dp-2*tp/dp**2;g[:,1,1]=g[:,2,1]=-tp/dp**2-tn/dn**2;g[:,3,1]=1/dn-2*tn/dn**2;g[:,2,3]=-tn/neg**2;g[:,3,3]=fp/neg**2;g[:,0,4]=fn/pos**2;g[:,1,4]=-tp/pos**2
  score=np.einsum('nck,kcm->nkm',one-mu[None,:,:],g);loss=(pp-yy[:,None])**2;score[:,:,2]=loss-loss.mean(axis=0);nn=score[:,:50].reshape(no,5,10,5).mean(axis=2);base=score[:,50:];delta=(nn[:,:,None,:]-base[:,None,:,:])*N/(5*no);delta=np.repeat(delta[:,:,:,None,:],2,axis=3);phi[use]=np.concatenate([delta[:,:,:,:,0].reshape(no,20),delta[:,:,:,:,1:].reshape(no,80)],axis=1)
 return phi

def financial_entrypoint(*args,**kwargs):raise BlockedError('No financial family input or testing authorized')
