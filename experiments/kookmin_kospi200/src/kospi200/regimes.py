"""Filtering from supplied parameters only. Does not import hmmlearn or fit HMMs."""
import numpy as np
from .data import BlockedError

def forward_filter(x, *, startprob, transmat, means, covars, previous_posterior=None):
    """p(z_t | x_<=t), no smoothing/Viterbi. x must already be PIT/train-scaled.

    To continue validation/test, pass the last filtered posterior of the preceding
    available history; otherwise the first emission uses startprob directly.
    """
    x=np.asarray(x,dtype=float); means=np.asarray(means,dtype=float)
    a=np.asarray(transmat,dtype=float); initial=np.asarray(startprob,dtype=float)
    cov=np.asarray(covars,dtype=float)
    if x.ndim!=2 or means.ndim!=2 or x.shape[1]!=means.shape[1]:
        raise BlockedError('HMM dimensions invalid')
    k,d=means.shape
    if a.shape!=(k,k) or initial.shape!=(k,) or (a<0).any() or (initial<0).any():
        raise BlockedError('Invalid HMM probabilities')
    if not np.allclose(a.sum(axis=1),1) or not np.isclose(initial.sum(),1):
        raise BlockedError('HMM probabilities must sum to one')
    if cov.shape==(k,d):
        cov=np.array([np.diag(c) for c in cov])
    if cov.shape!=(k,d,d) or not all(np.isfinite(v).all() for v in [x,means,a,initial,cov]):
        raise BlockedError('Invalid HMM parameters')
    chols=[]
    for c in cov:
        if not np.allclose(c,c.T):
            raise BlockedError('Nonsymmetric covariance')
        try: chols.append(np.linalg.cholesky(c))
        except np.linalg.LinAlgError as exc: raise BlockedError('Nonpositive covariance') from exc
    prev=None if previous_posterior is None else np.asarray(previous_posterior,dtype=float)
    if prev is not None and (prev.shape!=(k,) or (prev<0).any() or not np.isclose(prev.sum(),1)):
        raise BlockedError('Invalid previous filtering posterior')
    result=[]
    for row in x:
        prior=initial if prev is None else prev@a
        logs=[]
        for i,l in enumerate(chols):
            residual=np.linalg.solve(l,row-means[i])
            emission=-.5*(d*np.log(2*np.pi)+2*np.log(np.diag(l)).sum()+residual@residual)
            logs.append(np.log(prior[i]) + emission if prior[i]>0 else -np.inf)
        logs=np.asarray(logs)
        maximum=np.max(logs)
        if not np.isfinite(maximum):
            raise BlockedError('Degenerate HMM emission likelihood')
        weights=np.exp(logs-maximum)
        prev=weights/weights.sum();result.append(prev.copy())
    return np.asarray(result).reshape((-1,k))

def train_regime_reference(train_vol, train_state_means, *, partition):
    if partition!='train':
        raise BlockedError('Test/validation thresholds and state names prohibited')
    v=np.asarray(train_vol,dtype=float);m=np.asarray(train_state_means,dtype=float)
    if not np.isfinite(v).all() or not np.isfinite(m).all() or len(v)==0:
        raise BlockedError('Invalid Train regime reference')
    lo,hi=np.percentile(v,[30,70])
    return {'low':float(lo),'high':float(hi),'state_order':np.argsort(m).tolist(),'reference_partition':'train'}

def regime_status(states, k=2):
    if states is None:
        return {'status':'BLOCKED','reason':'HMM_fit_failed; no_test_median_fallback'}
    states=np.asarray(states)
    if len(np.unique(states))<k:
        return {'status':'BLOCKED','reason':'state_collapse; no_test_median_fallback'}
    return {'status':'PASS','reason':'all_states_observed'}

def hmm_training_plan(train_features, train_dates, validation_start, *, partition):
    """Prepare only a declarative Train-fit request. Never calls an HMM library."""
    import pandas as pd
    if partition!='train':
        raise BlockedError('HMM fit plan may reference Train only')
    from .data import START,END
    dates=pd.DatetimeIndex(train_dates)
    if len(dates)==0 or dates.has_duplicates or (dates<START).any() or (dates>END).any() or (dates>=pd.Timestamp(validation_start)).any() or not dates.isin(train_features.index).all():
        raise BlockedError('HMM fit dates cross validation boundary')
    if not np.isfinite(train_features.loc[dates].to_numpy(dtype=float)).all():
        raise BlockedError('Invalid HMM Train features')
    return {'fit_enabled':False,'partition':'train','fit_rows':len(dates),
            'first_date':str(dates.min().date()),'last_date':str(dates.max().date()),
            'feature_order':list(train_features.columns),'selection':'Train log likelihood only',
            'states':2,'covariance_type':'full','n_iter':2000,'tol':1e-4,'min_covar':1e-4,
            'initialization_seeds':[2,12,22,32,42,52,62,72,82,92]}


def filter_dated(observations, *, train_parameter_provenance, **parameters):
    """Production wrapper: timestamped, ordered input and Train-only parameter provenance."""
    import pandas as pd
    from .data import START,END
    dates=pd.DatetimeIndex(observations.index)
    if dates.has_duplicates or not dates.is_monotonic_increasing or (dates<START).any() or (dates>END).any():
        raise BlockedError('HMM filtering history outside period/ordering')
    p=train_parameter_provenance
    if p.get('fit_partition')!='train' or not p.get('checkpoint_sha256') or not p.get('availability_verified'):
        raise BlockedError('Verified Train-only HMM parameter lineage required')
    if pd.Timestamp(p['train_label_end_max'])>=pd.Timestamp(p['validation_start']):
        raise BlockedError('Train label provenance crosses validation boundary')
    return forward_filter(observations.to_numpy(dtype=float),**parameters)
