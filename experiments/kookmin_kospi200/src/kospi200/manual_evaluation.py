"""Train-only manual regime references and metrics for supplied predictions.

No model imports, training, predictions, HMM fitting or historical recomputation.
"""
import numpy as np
import pandas as pd
from .data import BlockedError, START, END


def freeze_manual_reference(volatility, train_dates, *, validation_start, partition):
    if partition != 'train':
        raise BlockedError('Only Train may define manual regime thresholds')
    dates = pd.DatetimeIndex(train_dates)
    if (not len(dates) or dates.has_duplicates or not dates.is_monotonic_increasing
        or (dates < START).any() or (dates > END).any()
        or (dates >= pd.Timestamp(validation_start)).any()
        or volatility.index.has_duplicates or not dates.isin(volatility.index).all()):
        raise BlockedError('Invalid Train reference dates')
    values = volatility.loc[dates].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise BlockedError('Nonfinite Train volatility')
    low, high = np.percentile(values, [30, 70], method='linear')
    if low >= high:
        raise BlockedError('Collapsed quantiles; do not overlap Low/High or tune on Test')
    return {'low':float(low), 'high':float(high), 'partition':'train',
            'train_start':str(dates.min().date()), 'train_end':str(dates.max().date()),
            'rows':len(dates), 'validation_start':str(pd.Timestamp(validation_start).date()),
            'quantiles':[30,70], 'method':'linear', 'variable':'Vol_Regime'}


def assign_manual_regimes(volatility, reference):
    if (reference.get('partition') != 'train' or reference['low'] >= reference['high']
        or pd.Timestamp(reference['train_end']) >= pd.Timestamp(reference['validation_start'])):
        raise BlockedError('Invalid frozen Train reference')
    idx = pd.DatetimeIndex(volatility.index)
    if idx.has_duplicates or not idx.is_monotonic_increasing or (idx < START).any() or (idx > END).any():
        raise BlockedError('Invalid regime dates')
    x = volatility.to_numpy(dtype=float)
    if not np.isfinite(x).all():
        raise BlockedError('Missing volatility cannot become a regime')
    return pd.Series(np.where(x <= reference['low'], 'Low_Vol',
                     np.where(x >= reference['high'], 'High_Vol', 'Mid_Vol')), index=idx, name='regime')


def supplied_prediction_metrics(y_true, y_pred):
    """Fixed labels [0,1]; single-class and empty BA/MacroF1 are null, never zero."""
    a, b = np.asarray(y_true), np.asarray(y_pred)
    if a.ndim != 1 or b.shape != a.shape or not np.isin(a,[0,1]).all() or not np.isin(b,[0,1]).all():
        raise BlockedError('Finite binary predictions and known labels required')
    supports = [int((a == c).sum()) for c in [0,1]]
    recalls = [float(((a == c)&(b == c)).sum()/supports[c]) if supports[c] else None for c in [0,1]]
    f1 = []
    for c in [0,1]:
        tp = int(((a==c)&(b==c)).sum());fp = int(((a!=c)&(b==c)).sum());fn = int(((a==c)&(b!=c)).sum())
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.)
    both = min(supports)>0
    return {'n':len(a), 'n_class0':supports[0], 'n_class1':supports[1],
            'recall_class0':recalls[0], 'recall_class1':recalls[1],
            'balanced_accuracy':float(np.mean(recalls)) if both else None,
            'macro_f1':float(np.mean(f1)) if both else None,
            'status':'PASS' if both else 'EMPTY' if len(a)==0 else 'SINGLE_CLASS_NOT_ESTIMABLE'}


def regime_metric_table(rows, *, regime_type):
    """Separate manual/HMM tables, no seed concatenation or sample count inflation."""
    if regime_type not in ['manual','hmm']:
        raise BlockedError('Explicit manual/HMM table type required')
    keys=['origin','seed','model'];required=keys+['date','regime','y_true','y_pred']
    if not set(required).issubset(rows):
        raise BlockedError('Missing prediction lineage')
    d=rows.copy();d['date']=pd.to_datetime(d.date)
    allowed=['Low_Vol','Mid_Vol','High_Vol'] if regime_type=='manual' else ['HMM_0','HMM_1']
    if (d.duplicated(keys+['date']).any() or not d.date.between(START,END).all()
        or not d.regime.isin(allowed).all()):
        raise BlockedError('Duplicate dates, period violation or mixed regime types')
    out=[]
    for identity,g in d.groupby(keys):
        for regime in allowed:
            sub=g[g.regime==regime]
            out.append(dict(zip(keys,identity),regime=regime,regime_type=regime_type,
                            **supplied_prediction_metrics(sub.y_true.to_numpy(),sub.y_pred.to_numpy())))
    return pd.DataFrame(out)
