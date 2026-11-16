"""One prediction store, separate manual/HMM evaluation tables. No fitting."""
import pandas as pd
from .data import BlockedError,START,END
from .manual_evaluation import regime_metric_table


def evaluate_same_predictions(predictions, manual_regimes, hmm_regimes, *, provenance):
    """Future interface; caller supplies existing predictions and frozen causal regimes.

    Attach regime by Origin/date with a validated one-to-one map before seed/model
    repetition. Table metrics remain keyed by Origin/Seed/Model (no seed pooling).
    """
    if (provenance.get('manual_reference_partition')!='train'
        or provenance.get('hmm_fit_partition')!='train'
        or provenance.get('hmm_decode')!='forward_filter'
        or provenance.get('hmm_state_naming_partition')!='train'
        or provenance.get('hmm_status')!='PASS'
        or not provenance.get('availability_verified')
        or provenance.get('test_median_fallback',True)):
        raise BlockedError('Train-only references, causal HMM and verified availability required')
    p=predictions.copy();p['date']=pd.to_datetime(p.date)
    keys=['origin','seed','model','date']
    if not set(keys+['probability','y_true']).issubset(p) or p.duplicated(keys).any():
        raise BlockedError('Prediction lineage incomplete/duplicate')
    if not p.date.between(START,END).all() or not p.probability.between(0,1).all():
        raise BlockedError('Prediction period or probability invalid')
    p['y_pred']=(p.probability>.5).astype(int)
    out={}
    for kind,masks in [('manual',manual_regimes),('hmm',hmm_regimes)]:
        d=masks.copy();d['date']=pd.to_datetime(d.date)
        if d.duplicated(['origin','date']).any():raise BlockedError('Regime map must be unique per Origin/date')
        joined=p.merge(d[['origin','date','regime']],on=['origin','date'],how='left',validate='many_to_one')
        if joined.regime.isna().any():raise BlockedError('Missing regime dates; do not silently change sample set')
        out[kind]=regime_metric_table(joined,regime_type=kind)
    return out
