"""STEP6A: synthetic-only HMM preparation. Financial entrypoints always blocked."""
import hashlib,json
import numpy as np
from .data import BlockedError
from .regimes import forward_filter
from .step5b_policy import test_metrics
SEEDS=[2,12,22,32,42,52,62,72,82,92]
HMM_KWARGS={'n_components':2,'covariance_type':'full','n_iter':2000,'tol':1e-4,'min_covar':1e-4}

def validate_train_scope(*,origin,candidate,partition,session_ids,allowed_train_ids,feature_order):
 if origin not in ['O1','O2','O3','O4','O5'] or candidate not in ['A','B'] or partition!='train' or feature_order!=['Vol_Regime']:raise BlockedError('Train-only one-observation scope required')
 ids=np.asarray(session_ids);allowed=np.asarray(allowed_train_ids)
 if ids.ndim!=1 or len(ids)==0 or not np.array_equal(ids,allowed) or not np.issubdtype(ids.dtype,np.integer) or np.any(np.diff(ids)<=0):raise BlockedError('Exactly retained purged Train base dates required')
 return True

def validate_parameters(parameters):
 p=parameters;start=np.asarray(p['startprob']);a=np.asarray(p['transmat']);mu=np.asarray(p['means']);cv=np.asarray(p['covars'])
 if start.shape!=(2,) or a.shape!=(2,2) or mu.shape!=(2,1) or cv.shape!=(2,1,1) or not all(np.isfinite(x).all() for x in [start,a,mu,cv]):raise BlockedError('Nonfinite/invalid GaussianHMM parameters')
 if np.any(start<0) or np.any(a<0) or not np.isclose(start.sum(),1) or not np.allclose(a.sum(1),1):raise BlockedError('Invalid initial/transition probabilities')
 for c in cv:
  if not np.allclose(c,c.T):raise BlockedError('Asymmetric covariance')
  try:np.linalg.cholesky(c)
  except np.linalg.LinAlgError as e:raise BlockedError('Nonpositive covariance') from e
 return True

def filter_sessions(x,session_ids,*,parameters,expected_session_ids,previous_posterior=None,previous_session_id=None):
 validate_parameters(parameters);xx=np.asarray(x,dtype=float);ids=np.asarray(session_ids);expected=np.asarray(expected_session_ids)
 if xx.shape!=(len(ids),1) or not np.isfinite(xx).all() or ids.ndim!=1 or not np.issubdtype(ids.dtype,np.integer) or not np.array_equal(ids,expected) or len(set(ids.tolist()))!=len(ids) or (len(ids)>1 and not np.all(np.diff(ids)==1)):raise BlockedError('Missing/duplicate/nonmonotone bridge sessions or invalid observation')
 if previous_posterior is not None and (previous_session_id is None or (len(ids) and ids[0]!=previous_session_id+1)):raise BlockedError('Bridge transition omitted')
 return forward_filter(xx,**parameters,previous_posterior=previous_posterior)

def train_state_names(raw_train,posteriors):
 x=np.asarray(raw_train,dtype=float).reshape(-1);q=np.asarray(posteriors);states=q.argmax(1)
 if q.shape!=(len(x),2) or not np.isfinite(x).all() or set(states)!={0,1}:raise BlockedError('Train hard-filter state collapse')
 means=np.array([x[states==i].mean() for i in [0,1]])
 if not np.isfinite(means).all() or means[0]==means[1]:raise BlockedError('Train raw-state means not distinguishable')
 order=np.argsort(means);return {int(order[0]):'Low_Vol',int(order[1]):'High_Vol'}

def candidate_eligibility(candidate):
 reasons=[]
 if candidate.get('seed') not in SEEDS:reasons.append('UNDECLARED_SEED')
 if not np.isfinite(candidate.get('train_log_likelihood',np.nan)):reasons.append('NONFINITE_TRAIN_LL')
 history=candidate.get('likelihood_history',[])
 # hmmlearn monitor.converged also becomes true at maxiter; that alone is insufficient.
 if not candidate.get('monitor_converged') or len(history)<2 or not np.isfinite(history).all() or not (0<=history[-1]-history[-2]<1e-4):reasons.append('NOT_TRUE_TOLERANCE_CONVERGENCE')
 try:validate_parameters(candidate['parameters'])
 except (BlockedError,KeyError):reasons.append('INVALID_PARAMETERS_COVARIANCE')
 if set(candidate.get('train_hard_states',[]))!={0,1}:reasons.append('TRAIN_STATE_COLLAPSE')
 evidence=candidate.get('reproducibility_evidence',{})
 if not evidence.get('synthetic_repeat_PASS') or not evidence.get('deterministic_settings') or evidence.get('fixed_seed')!=candidate.get('seed') or any(not isinstance(evidence.get(k),str) or len(evidence[k])!=64 for k in ['data_sha256','source_sha256','environment_sha256']):reasons.append('REPRODUCIBILITY_UNVERIFIED')
 return {'eligible':not reasons,'reasons':reasons}

def select_candidate(candidates):
 if len(candidates)!=10 or sorted(c['seed'] for c in candidates)!=SEEDS:raise BlockedError('All10 fixed initialization candidates must be accounted for')
 audited=[dict(c,eligibility=candidate_eligibility(c)) for c in candidates];eligible=[c for c in audited if c['eligibility']['eligible']]
 if not eligible:raise BlockedError('No eligible candidate; no seed/state-count/threshold fallback')
 chosen=sorted(eligible,key=lambda c:(-c['train_log_likelihood'],c['seed']))[0]
 return chosen,audited

def synthetic_train_fit(raw_train,*,seed,domain):
 if domain!='SYNTHETIC_FIXTURE' or seed not in SEEDS:raise BlockedError('Only explicitly synthetic fitting permitted in STEP6A')
 from sklearn.preprocessing import StandardScaler
 from hmmlearn.hmm import GaussianHMM
 x=np.asarray(raw_train,dtype=float)
 if x.ndim!=2 or x.shape[1]!=1 or len(x)<2 or not np.isfinite(x).all():raise BlockedError('Invalid synthetic Train observation')
 scaler=StandardScaler().fit(x);xx=scaler.transform(x);model=GaussianHMM(random_state=seed,**HMM_KWARGS);model.fit(xx)
 p={'startprob':model.startprob_.copy(),'transmat':model.transmat_.copy(),'means':model.means_.copy(),'covars':model.covars_.copy()}
 return {'parameters':p,'scaler_mean':scaler.mean_.copy(),'scaler_scale':scaler.scale_.copy(),'train_log_likelihood':float(model.score(xx)),'likelihood_history':list(model.monitor_.history),'monitor_converged':bool(model.monitor_.converged)}

def align_regime_predictions(predictions,states,*,origin,candidate,expected_ids):
 """Synthetic/in-memory contract. Reuse supplied probabilities; never creates them."""
 ids=np.asarray(predictions['session_id']);state_ids=np.asarray(states['session_id']);expected=np.asarray(expected_ids)
 if predictions['origin']!=origin or states['origin']!=origin or predictions['candidate']!=candidate or states['candidate']!=candidate:raise BlockedError('Origin/Candidate mixing')
 if len(ids)==0 or len(set(ids.tolist()))!=len(ids) or not np.array_equal(ids,expected) or np.any(np.diff(ids)<=0) or len(set(state_ids.tolist()))!=len(state_ids) or np.any(np.diff(state_ids)<=0):raise BlockedError('Evaluation session alignment/duplicate/missing')
 if not np.array_equal(predictions['dates'],states['evaluation_dates']) or not np.array_equal(predictions['label_end'],states['evaluation_label_end']) or not np.array_equal(predictions['y'],states['evaluation_y']):raise BlockedError('Frozen date/Target lineage changed')
 lookup=dict(zip(state_ids,states['regime']));
 if not set(ids).issubset(lookup) or not set(lookup.values()).issubset({'Low_Vol','High_Vol'}):raise BlockedError('Missing/invalid HMM state assignment')
 out=[];reg=np.array([lookup[i] for i in ids]);y=np.asarray(predictions['y']);prob=np.asarray(predictions['probability'])
 for name in ['Low_Vol','High_Vol']:
  mask=reg==name;out.append({'regime':name,'occupancy':float(mask.mean()),**test_metrics(y[mask],prob[mask])})
 if sum(r['n'] for r in out)!=len(ids):raise BlockedError('Regime sample conservation failure')
 return out

def financial_hmm_entrypoint(*args,**kwargs):
 raise BlockedError('STEP6A financial HMM fit/filter is not released; separate STEP6B approval and input/source/config/environment hashes required')
