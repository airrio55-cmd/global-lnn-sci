"""Candidate/Origin/Seed/date keyed original RAW5/LOG2 composition, supplied values only."""
import json
import pandas as pd
from .data import BlockedError
from .specs import RAW,LOG,keyed_ensemble

def original_lnn_composition(rows):
 required={'candidate','origin','seed','date','model','probability','effective_seed','feature_order','checkpoint_sha256'}
 if not required.issubset(rows):raise BlockedError('Missing original-channel lineage')
 d=rows.copy()
 if not d.candidate.isin(['A','B']).all():raise BlockedError('Unknown price candidate')
 expected={'LTC_RAW':(RAW,401),'LTC_LOG':(LOG,402),'RNN_RAW':(RAW,101)}
 for x in d.itertuples():
  if x.model not in expected:raise BlockedError('Unexpected ensemble component')
  features,offset=expected[x.model];order=json.loads(x.feature_order) if isinstance(x.feature_order,str) else list(x.feature_order)
  if order!=features or x.effective_seed!=x.seed+offset or not x.checkpoint_sha256:raise BlockedError('Channel/seed/checkpoint mismatch; F1 is not original RAW5/LOG2')
 if 'y' in d and not d.groupby(['candidate','origin','seed','date']).y.nunique().eq(1).all():raise BlockedError('Component label mismatch')
 out=[]
 for candidate,g in d.groupby('candidate',sort=True):
  composed=keyed_ensemble(g.drop(columns='candidate'));composed.insert(0,'candidate',candidate);out.append(composed)
 if not out:raise BlockedError('No paired ensemble values')
 return pd.concat(out,ignore_index=True)
