"""Rolling origins and train-only normalization; requires verified KRX sessions."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from .data import BlockedError, START, END

ORIGINS = [(f'O{i}', 2019+i-1, 2020+i-1, 2021+i-1) for i in range(1,6)]

def rolling_origins(labels, calendar, input_eligible=None):
    sessions = calendar.checked()
    if not labels.index.equals(sessions):
        raise BlockedError('Labels must use exact KRX calendar index')
    eligible = pd.Series(True,index=sessions) if input_eligible is None else input_eligible.reindex(sessions).fillna(False)
    manifests, selected = [], {}
    for origin, train_end, val_year, test_year in ORIGINS:
        val_dates = sessions[sessions.year == val_year]
        test_dates = sessions[sessions.year == test_year]
        if len(val_dates)==0 or len(test_dates)==0:
            raise BlockedError('Origin boundary absent from verified calendar')
        val_start, test_start = val_dates[0], test_dates[0]
        selected[origin] = {}
        for partition, mask, cutoff in [
            ('train', sessions.year<=train_end, val_start),
            ('validation', sessions.year==val_year, test_start),
            ('test', sessions.year==test_year, None)]:
            rows = labels.loc[mask]
            known = rows.Target.notna() & rows.label_end.notna()
            purged = known & (rows.label_end >= cutoff) if cutoff is not None else pd.Series(False,index=rows.index)
            kept = known & ~purged & eligible.reindex(rows.index)
            selected[origin][partition] = rows.index[kept]
            manifests.append({'origin':origin,'partition':partition,'boundary_start':str(rows.index[0].date()),
                'boundary_end':str(rows.index[-1].date()),'raw_rows':len(rows),'unknown_labels':int((~known).sum()),
                'purged_labels':int(purged.sum()),'input_ineligible_after_label_filter':int((known & ~purged & ~eligible.reindex(rows.index)).sum()),
                'eligible_samples':int(kept.sum()),'first_sample':str(rows.index[kept][0].date()) if kept.any() else '',
                'last_sample':str(rows.index[kept][-1].date()) if kept.any() else '',
                'next_cutoff':str(cutoff.date()) if cutoff is not None else '', 'status':'PASS'})
    return pd.DataFrame(manifests),selected

def window_dates(sessions, target_dates, *, window=20, include_t=True):
    """Reuse prior-partition feature history; never use future input context."""
    sessions=pd.DatetimeIndex(sessions)
    if sessions.has_duplicates or not sessions.is_monotonic_increasing or (sessions<START).any() or (sessions>END).any():
        raise BlockedError('Window history outside period or invalid ordering')
    result={}
    for t in target_dates:
        pos=sessions.get_indexer([t])[0]
        end=pos+1 if include_t else pos
        if pos<0 or end-window<0:
            continue
        result[t]=sessions[end-window:end]
    return result

def train_only_scaler(features, train_dates, val_start):
    """Fit only approved Train feature rows; returns transform + fit lineage."""
    idx=pd.DatetimeIndex(train_dates)
    if len(idx)==0 or idx.has_duplicates or (idx<START).any() or (idx>END).any() or (idx>=pd.Timestamp(val_start)).any() or not idx.isin(features.index).all():
        raise BlockedError('Scaler fit dates violate Train boundary')
    x=features.loc[idx]
    if not np.isfinite(x.to_numpy(dtype=float)).all():
        raise BlockedError('Nonfinite Train features')
    scaler=StandardScaler().fit(x)
    return scaler, {'fit_start':str(idx.min().date()),'fit_end':str(idx.max().date()),
                     'fit_rows':len(idx),'feature_order':list(x.columns),'source_partition':'train'}


def transform_checked(scaler, features):
    dates=pd.DatetimeIndex(features.index)
    if (dates<START).any() or (dates>END).any() or not np.isfinite(features.to_numpy(dtype=float)).all():
        raise BlockedError('Transform data outside period or nonfinite')
    if list(features.columns)!=list(scaler.feature_names_in_):
        raise BlockedError('Scaler feature order mismatch')
    return pd.DataFrame(scaler.transform(features),index=features.index,columns=features.columns)
