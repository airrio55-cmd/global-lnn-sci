"""Receive future caller-supplied LTC snapshots; no torch/model/checkpoint operations."""
import pandas as pd
from .data import BlockedError
from .tau import time_constants,REFERENCE_SHA

def supplied_tau_snapshot(*,inputs,hidden,params,lineage):
 required=['origin','seed','candidate','checkpoint_sha256','date','time_index','solver_substep','elapsed_time','ode_unfolds','dt_unit','implicit_param_constraints','source_commit']
 if any(k not in lineage for k in required):raise BlockedError('Incomplete tau snapshot lineage')
 if not pd.Timestamp('2010-01-01')<=pd.Timestamp(lineage['date'])<=pd.Timestamp('2025-12-31'):raise BlockedError('Out-of-period snapshot')
 if lineage['source_commit']!=REFERENCE_SHA or lineage['implicit_param_constraints'] is not True or lineage['ode_unfolds']!=6 or lineage['elapsed_time']<=0 or not lineage['checkpoint_sha256']:raise BlockedError('Unverified LTC semantics')
 if lineage['dt_unit']!='model_observation_step':raise BlockedError('Physical seconds/KRX-day tau unit not established')
 result=time_constants(inputs,hidden,params,input_mapping='affine',implicit_constraints=True,dt_unit=lineage['dt_unit'],source_commit=REFERENCE_SHA)
 return {**result,'lineage':dict(lineage),'physical_KRX_day_unit_verified':False,'actual_forward_executed_here':False}
