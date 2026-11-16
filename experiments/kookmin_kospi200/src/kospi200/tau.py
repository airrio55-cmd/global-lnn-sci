"""LTC snapshot analysis only. No torch import/forward/checkpoint load.

Reference: ncps/torch/ltc_cell.py @ 695ec22d7d1831f2ced67346ef7d2f08c525bd47.
No upstream code copied. Algebra independently implements conductance summaries.
"""
import numpy as np
import pandas as pd
from scipy.special import expit
from .data import BlockedError

REFERENCE_SHA='695ec22d7d1831f2ced67346ef7d2f08c525bd47'

def time_constants(inputs, hidden, params, *, input_mapping='affine',
                   implicit_constraints=None, dt_unit=None, source_commit=None):
    """Arrays at a specified solver substep, NOT a model trajectory simulation.

    tau_raw=cm/gleak; tau_effective=cm/(gleak+sum sensory+sum recurrent).
    Units follow trained elapsed_time; default ncps 1.0 is not inherently a KRX day.
    cm/dt solver coefficient is intentionally not part of physical conductance.
    """
    if not isinstance(implicit_constraints,bool):
        raise BlockedError('Explicit LTC wrapper/cell positive-parameter constraint mode required')
    if source_commit!=REFERENCE_SHA or dt_unit is None:
        raise BlockedError('ncps version/source and elapsed_time units must be verified')
    x=np.asarray(inputs,dtype=float);h=np.asarray(hidden,dtype=float)
    if x.ndim!=2 or h.ndim!=2 or len(x)!=len(h):
        raise BlockedError('Invalid snapshot dimensions')
    p={k:np.asarray(v,dtype=float) for k,v in params.items()}
    required=['cm','gleak','w','mu','sigma','sensory_w','sensory_mu','sensory_sigma','sparsity_mask','sensory_sparsity_mask']
    if not all(k in p for k in required) or not all(np.isfinite(a).all() for a in [x,h,*p.values()]):
        raise BlockedError('Missing/nonfinite LTC parameters')
    units=h.shape[1];inputs_n=x.shape[1]
    for name in ['cm','gleak']:
        if p[name].shape!=(units,):raise BlockedError('Invalid '+name+' shape')
    for name in ['w','mu','sigma','sparsity_mask']:
        if p[name].shape!=(units,units):raise BlockedError('Invalid recurrent shape')
    for name in ['sensory_w','sensory_mu','sensory_sigma','sensory_sparsity_mask']:
        if p[name].shape!=(inputs_n,units):raise BlockedError('Invalid sensory shape')
    if input_mapping not in ['affine','linear','identity']:
        raise BlockedError('Unknown input mapping')
    if input_mapping in ['affine','linear']:
        if 'input_w' not in p:raise BlockedError('Input mapping weights absent')
        x=x*p['input_w']
    if input_mapping=='affine':
        if 'input_b' not in p:raise BlockedError('Input mapping bias absent')
        x=x+p['input_b']
    positive=lambda a:np.logaddexp(0,a) if implicit_constraints else a
    cm,gl,w,sw=[positive(p[k]) for k in ['cm','gleak','w','sensory_w']]
    if (cm<=0).any() or (gl<=0).any() or (w<0).any() or (sw<0).any():
        raise BlockedError('Degenerate/nonpositive LTC conductance; no silent clipping')
    if (p['sparsity_mask']<0).any() or (p['sensory_sparsity_mask']<0).any():
        raise BlockedError('Invalid conductance masks')
    recurrent=(w*expit(p['sigma']*(h[:,:,None]-p['mu']))*p['sparsity_mask']).sum(axis=1)
    sensory=(sw*expit(p['sensory_sigma']*(x[:,:,None]-p['sensory_mu']))*p['sensory_sparsity_mask']).sum(axis=1)
    return {'tau_raw':np.broadcast_to(cm/gl,h.shape).copy(),
            'tau_effective':cm/(gl+recurrent+sensory),'unit':dt_unit,
            'interpretation':'frozen-state/input conductance time constant, not full nonlinear Jacobian eigen-timescale'}

def summarize_snapshots(rows):
    """Caller supplies date, seed, origin, Train-defined regime and tau values."""
    required={'date','seed','origin','regime','tau_raw','tau_effective'}
    if not required.issubset(rows):raise BlockedError('Missing tau lineage')
    if not np.isfinite(rows[['tau_raw','tau_effective']].to_numpy()).all() or (rows[['tau_raw','tau_effective']]<=0).any().any():
        raise BlockedError('Nonfinite or nonpositive tau summary')
    dt=pd.to_datetime(rows.date)
    if not dt.between('2010-01-01','2025-12-31').all():raise BlockedError('Tau observations outside period')
    return rows.groupby(['origin','seed','regime'])[['tau_raw','tau_effective']].quantile([.05,.25,.5,.75,.95])

def exploratory_association(tau_summary, performance):
    """Join fixed Origin/Seed/regime summaries; exploratory correlation only, no causal p-value."""
    from scipy.stats import spearmanr
    keys=['origin','seed','regime']
    if tau_summary.duplicated(keys).any() or performance.duplicated(keys).any():
        raise BlockedError('Ambiguous tau/performance lineage')
    joined=tau_summary.merge(performance,on=keys,validate='one_to_one')
    if len(joined)<3 or not np.isfinite(joined[['tau_effective_median','balanced_accuracy']].to_numpy()).all():
        raise BlockedError('Insufficient finite paired exploratory summaries')
    rho=float(spearmanr(joined.tau_effective_median,joined.balanced_accuracy).statistic)
    return {'spearman_rho_exploratory':rho,'paired_summaries':len(joined),
            'confirmatory_p_value':None,'caveat':'dependent summaries; descriptive only; date-block uncertainty required before inference'}
