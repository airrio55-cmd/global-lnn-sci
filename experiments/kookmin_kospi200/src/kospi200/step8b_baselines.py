"""Frozen simple-baseline contract. No neural/HMM code or checkpoint I/O."""
import warnings,hashlib,json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import ConvergenceWarning
from .data import BlockedError
from .step5b_policy import test_metrics
MODELS=['CLIMATOLOGY','LOGISTIC','DMA200','MOMENTUM60']
LR_SPEC=dict(C=1.0,penalty='l2',solver='lbfgs',max_iter=1000,fit_intercept=True,class_weight=None,random_state=20261120,tol=1e-4)
def validate_alignment(dates,ids,y,ends,expected):
 arrays=[np.asarray(v) for v in [dates,ids,y,ends]]
 if len({len(v) for v in arrays})!=1 or len(set(map(str,arrays[0])))!=len(arrays[0]) or any(str(d)>'2025-12-31' for d in arrays[0]) or any(str(d)>'2025-12-31' for d in arrays[3]):raise BlockedError('Date/length/cutoff mismatch')
 if any(not np.array_equal(v,np.asarray(e)) for v,e in zip(arrays,expected)):raise BlockedError('Frozen date/session/Target/endpoint changed')
 if len(arrays[1])>1 and not np.all(np.diff(arrays[1])==1):raise BlockedError('Missing/duplicate Test sessions')
 if not np.isin(arrays[2],[0,1]).all():raise BlockedError('Unknown or invalid target')
 return True

def rule_probability(close,session_ids,model):
 c=np.asarray(close,dtype=np.float64);idx=np.asarray(session_ids,dtype=np.int64)
 if not np.isfinite(c).all() or np.any(c<=0) or len(idx)==0 or len(set(idx))!=len(idx) or (np.diff(idx)<=0).any() or idx.max()>=len(c):raise BlockedError('Invalid price/session prefix')
 if model=='DMA200':
  if idx.min()<199:raise BlockedError('200-session warmup unavailable')
  reference=np.array([np.mean(c[i-199:i+1]) for i in idx])
 elif model=='MOMENTUM60':
  if idx.min()<60:raise BlockedError('61-observation momentum warmup unavailable')
  reference=c[idx-60]
 else:raise BlockedError('Unknown rule')
 return (c[idx]>reference).astype(np.float64),reference

def train_climatology(y,n):
 y=np.asarray(y)
 if not len(y) or not np.isin(y,[0,1]).all():raise BlockedError('Invalid Train targets')
 return np.full(n,float(y.mean())),{'p_train':float(y.mean()),'Train_single_class':np.unique(y).size==1,'policy':'eligible even if Train single-class; no refit'}

def fit_logistic(train_x,train_y,test_x):
 x=np.asarray(train_x,dtype=np.float64);y=np.asarray(train_y);tx=np.asarray(test_x,dtype=np.float64)
 if x.ndim!=2 or tx.ndim!=2 or x.shape[1]!=2 or tx.shape[1]!=2 or len(x)!=len(y) or not np.isfinite(x).all() or not np.isfinite(tx).all():raise BlockedError('Two finite current-t features required')
 if np.unique(y).size!=2 or not np.isin(y,[0,1]).all():raise BlockedError('LOGISTIC Train single-class')
 scaler=StandardScaler();z=scaler.fit_transform(x);model=LogisticRegression(**LR_SPEC)
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always');model.fit(z,y)
 if any(issubclass(w.category,ConvergenceWarning) for w in caught):raise BlockedError('LOGISTIC nonconverged; no iteration/tolerance changes')
 if not np.isfinite(model.coef_).all() or not np.isfinite(model.intercept_).all():raise BlockedError('LOGISTIC nonfinite coefficients')
 p=model.predict_proba(scaler.transform(tx))[:,list(model.classes_).index(1)]
 return p,{'scaler_mean':scaler.mean_.tolist(),'scaler_scale':scaler.scale_.tolist(),'scaler_fit_rows':len(x),'scaler_scope':'retained purged Train current-t only','coefficients':model.coef_.tolist(),'intercept':model.intercept_.tolist(),'classes':model.classes_.tolist(),'n_iter':model.n_iter_.tolist(),'warnings':[str(w.message) for w in caught]}

def authorize(config,approval,config_sha,roster_sha,source_sha,identity):
 if config.get('scope')!='STEP8B_BASELINES40' or config.get('NN_execution') is not False or config.get('HMM_execution') is not False or config.get('max_evaluations')!=40 or config.get('max_Logistic_fits')!=10:raise BlockedError('Invalid independent baseline scope')
 if config.get('lr_spec')!=LR_SPEC or config.get('scaler_contract')!='retained_Train_current_t_only' or config.get('horizon')!=20 or config.get('threshold')!=0.5:raise BlockedError('Frozen model/scaler/label contract changed')
 if approval.get('scope')!=config['scope'] or approval.get('approved') is not True or approval.get('config_sha256')!=config_sha or approval.get('roster_sha256')!=roster_sha or approval.get('source_sha256')!=source_sha or approval.get('request_sha256')!=config.get('request_sha256'):raise BlockedError('Approval tampered or unbound')
 if identity not in config.get('identities',[]) or len(config['identities'])!=40 or len(set(config['identities']))!=40:raise BlockedError('Unapproved or duplicate identity')
 return True
