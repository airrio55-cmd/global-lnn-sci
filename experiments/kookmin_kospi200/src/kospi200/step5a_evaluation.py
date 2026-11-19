"""STEP5A structural/synthetic evaluation only. No financial I/O or model imports."""
import hashlib,json
import numpy as np
from .data import BlockedError
from .manual_evaluation import supplied_prediction_metrics
from .master_statistics import paired_packet,bootstrap_effect,correct_frozen_family
SEEDS=[2,12,22,32,42,52,62,72,82,92]
MODELS=['RNN','LSTM','GRU','LTC','CfC']

def synthetic_metrics(y,probability,*,domain):
 if domain!='SYNTHETIC_FIXTURE':raise BlockedError('STEP5A permits synthetic fixtures only')
 y=np.asarray(y);p=np.asarray(probability)
 if y.ndim!=1 or p.shape!=y.shape or not np.isfinite(p).all() or ((p<0)|(p>1)).any() or not np.isin(y,[0,1]).all():raise BlockedError('Invalid labels/probabilities; no missing-to-zero conversion')
 pred=(p>.5).astype(int);m=supplied_prediction_metrics(y,pred)
 m.update(brier=float(np.mean((p-y)**2)) if len(y) else None,accuracy=float(np.mean(y==pred)) if len(y) else None,positive_prediction_rate=float(pred.mean()) if len(y) else None,single_class_prediction=bool(len(y) and len(np.unique(pred))==1),confusion_matrix=[[int(((y==a)&(pred==b)).sum()) for b in [0,1]] for a in [0,1]])
 return m

def synthetic_seed_scores(y,probabilities,*,seeds,domain):
 p=np.asarray(probabilities)
 if list(seeds)!=SEEDS or p.shape!=(len(y),10):raise BlockedError('All10 paired seeds required; no substitution/pooling')
 scores=[synthetic_metrics(y,p[:,i],domain=domain) for i in range(10)]
 names=['balanced_accuracy','macro_f1','brier','recall_class0','recall_class1','accuracy','positive_prediction_rate']
 return {'per_seed':scores,'mean':{k:float(np.mean([s[k] for s in scores])) if all(s[k] is not None for s in scores) else None for k in names},'market_dates':len(y),'seed_count':10,'probability_ensemble_created':False}

def synthetic_aligned_packet(frame,model_a,model_b,*,candidate,domain):
 if domain!='SYNTHETIC_FIXTURE' or candidate not in ['A','B'] or 'candidate' not in frame or set(frame.candidate)!={candidate}:raise BlockedError('Candidate/domain mixing prohibited')
 if set(frame.model)!={model_a,model_b} or model_a==model_b:raise BlockedError('Exactly two declared models required')
 packets=paired_packet(frame,model_a,model_b,seeds=SEEDS)
 for z in packets:
  sid=np.asarray(z['session_id'])
  if not np.issubdtype(sid.dtype,np.integer) or len(np.unique(sid))!=len(sid) or np.any(np.diff(sid)<=0):raise BlockedError('Official-session IDs must be unique and ascending')
 return packets

def synthetic_bootstrap(frame,model_a,model_b,*,candidate,metric_name,block_length,domain):
 packets=synthetic_aligned_packet(frame,model_a,model_b,candidate=candidate,domain=domain)
 return bootstrap_effect(packets,metric_name=metric_name,block_length=block_length,replicates=10000,seed=20261116)

def validate_checkpoint_identity(expected,metadata):
 """Metadata fixture validation only; never opens or deserializes a checkpoint."""
 for k in ['origin','candidate','seed','model','effective_seed','feature_order','best_checkpoint_sha256','master_sha256','data_sha256','environment_sha256']:
  if k not in expected or metadata.get(k)!=expected[k]:raise BlockedError('Checkpoint metadata identity/hash mismatch: '+k)
 return True

def reserve_fixture_evaluation(identity,completed,*,candidate,domain):
 if domain!='SYNTHETIC_FIXTURE' or candidate not in ['A','B'] or identity in completed:raise BlockedError('Unapproved/duplicate fixture evaluation')
 completed.add(identity);return True

def financial_test_entrypoint(*args,**kwargs):
 # Deliberately no file reads, checkpoint load or forward, even if caller flips a flag.
 raise BlockedError('STEP5A financial Test runtime is not released. Separate approval and SHA-bound execution implementation are required.')
