"""Independently authorized financial adapter. Frozen STEP7A arithmetic is reused."""
from .step7a_tau import SyntheticTauTap,require_cell,weights_fingerprint,build_solver,CELL_SHA,source_sha
from .data import BlockedError
import numpy as np

class RecoveryTauTap(SyntheticTauTap):
 def __init__(self,cell,*,metadata,job,release):
  require_cell(cell)
  if release.get('scope')!='STEP7BR_RECOVERY1' or release.get('financial_tau_enabled') is not True:raise BlockedError('Independent STEP7BR single recovery release required')
  if metadata.get('data_domain')!='FROZEN_STEP5B_TEST' or metadata.get('checkpoint_sha256')!=job['best_checkpoint_sha256'] or metadata.get('LTCCell_source_sha256')!=CELL_SHA or metadata.get('tau_source_sha256')!=source_sha():raise BlockedError('Financial source/checkpoint lineage mismatch')
  for k in ['origin','candidate','seed']:
   if metadata.get(k)!=job[k]:raise BlockedError('Financial identity mismatch')
  if metadata.get('elapsed_time')!=1. or metadata.get('ode_unfolds')!=6 or metadata.get('implicit_param_constraints') is not True or metadata.get('dt_unit')!='model_observation_step':raise BlockedError('Financial solver mismatch')
  days=metadata['batch_window_dates'];ids=metadata['batch_window_session_ids']
  if len(days)!=job['n'] or len(ids)!=job['n'] or any(len(d)!=20 or len(s)!=20 or not np.all(np.diff(s)==1) or max(d)>'2025-12-31' for d,s in zip(days,ids)):raise BlockedError('Financial window boundary mismatch')
  self.cell=cell;self.metadata=dict(metadata);self.expected={k:job[k] for k in ['origin','candidate','seed']};self.records=[];self.observations=[];self.hidden_outputs=[];self.index=-1;self.before_fingerprint=weights_fingerprint(cell);self._forward=cell.forward;self._solver=cell._ode_solver;self.compiled=build_solver(self)
