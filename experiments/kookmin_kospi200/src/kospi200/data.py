"""Date/availability contracts. Unknown provenance fails closed."""
from dataclasses import dataclass
import numpy as np
import pandas as pd

START = pd.Timestamp('2010-01-01')
END = pd.Timestamp('2025-12-31')

class BlockedError(ValueError):
    pass

def cutoff(frame, date_col='Date'):
    out = frame.copy()
    dates = pd.to_datetime(out[date_col], errors='raise')
    if dates.dt.tz is not None:
        raise BlockedError('Session dates must be timezone-free dates; use explicit availability timestamps separately')
    if dates.isna().any():
        raise BlockedError('Missing source session date')
    out[date_col] = dates
    return out.loc[dates.between(START, END)].sort_values(date_col).reset_index(drop=True)

@dataclass(frozen=True)
class Calendar:
    sessions: pd.DatetimeIndex
    source: str
    sha256: str
    verified: bool = False

    def checked(self):
        if not self.verified or not self.source or len(self.sha256) != 64:
            raise BlockedError('Verified KRX calendar with source and SHA-256 required')
        s = pd.DatetimeIndex(self.sessions)
        if s.tz is not None or s.hasnans or s.has_duplicates or not s.is_monotonic_increasing:
            raise BlockedError('Invalid KRX session ordering')
        if len(s) == 0 or (s < START).any() or (s > END).any():
            raise BlockedError('KRX sessions outside approved period')
        return s

def labels_on_calendar(close, calendar, horizon=20):
    """Endpoint is the 20th actual KRX session, never the 20th observed price row."""
    sessions = calendar.checked()
    c = close.copy()
    c.index = pd.DatetimeIndex(c.index)
    c = c.loc[(c.index >= START) & (c.index <= END)]
    if c.index.has_duplicates or not c.index.isin(sessions).all():
        raise BlockedError('Duplicate/non-KRX price dates')
    c = c.reindex(sessions).astype(float)
    if (c.dropna() <= 0).any() or not np.isfinite(c.dropna()).all():
        raise BlockedError('Invalid close')
    future = c.shift(-horizon)
    label_end = pd.Series(sessions, index=sessions).shift(-horizon)
    target = pd.Series(pd.NA, index=sessions, dtype='Int64')
    known = c.notna() & future.notna() & label_end.notna()
    target.loc[known] = (future.loc[known] > c.loc[known]).astype(int)
    reason = pd.Series('confirmed', index=sessions)
    reason.loc[c.isna()] = 'missing_current_close'
    reason.loc[c.notna() & future.isna() & label_end.notna()] = 'missing_KRX_endpoint_close'
    reason.loc[label_end.isna()] = 'horizon_outside_approved_period'
    return pd.DataFrame({'Close': c, 'Target': target, 'label_end': label_end, 'label_status': reason})

def local_features(close):
    """No filling: missing KRX sessions propagate to feature eligibility."""
    dates = pd.DatetimeIndex(close.index)
    if dates.has_duplicates or not dates.is_monotonic_increasing or (dates < START).any() or (dates > END).any():
        raise BlockedError("Feature history outside period or invalid ordering")
    log = np.log(close / close.shift(1))
    return pd.DataFrame({'Log_Ret': log, 'Disparity': close / close.rolling(20).mean() - 1,
                         'Vol_Regime': log.rolling(40).std()})

def require_aware(series, name):
    try:
        tz = series.dt.tz
    except AttributeError as exc:
        raise BlockedError(name + ': homogeneous timezone-aware timestamps required') from exc
    if tz is None or series.isna().any():
        raise BlockedError(name + ': explicit timezone and no missing timestamps required')
    return series.dt.tz_convert('UTC')

def pit_join(decisions, records, *, variable, max_age, availability_verified, metadata):
    """Latest released observation, backward as-of only; returns full row lineage.

    records: source_date, observed_at, available_at, value, source, source_sha256, record_id.
    decisions: decision_at (aware), optional sample_date. No fabricated release times.
    """
    required = {'source_date','observed_at','available_at','value','source','source_sha256','record_id'}
    if not availability_verified or not metadata.get('availability_evidence'):
        raise BlockedError(variable + ': availability evidence missing')
    if variable == 'Foreign_Net' and not all(metadata.get(k) for k in ('unit','market_scope','release_policy')):
        raise BlockedError('Foreign_Net unit/market/release policy unverified')
    if not required.issubset(records.columns) or max_age is None:
        raise BlockedError('Missing lineage columns/max_age')
    age_limit = pd.Timedelta(max_age)
    if age_limit <= pd.Timedelta(0):
        raise BlockedError('max_age must be positive and approved')
    r = cutoff(records, 'source_date')
    r['observed_at'] = require_aware(r['observed_at'], 'observed_at')
    r['available_at'] = require_aware(r['available_at'], 'available_at')
    if (r.available_at < r.observed_at).any():
        raise BlockedError('Release before observation')
    if r[['source','source_sha256','record_id']].isna().any().any():
        raise BlockedError('Missing source lineage')
    if not r.source_sha256.map(lambda x: isinstance(x,str) and len(x)==64).all():
        raise BlockedError('Invalid source hash')
    if r.record_id.duplicated().any() or r.available_at.duplicated().any():
        raise BlockedError('Ambiguous records/revisions: supply deterministic PIT revision policy')
    release_order = r.sort_values('observed_at').available_at
    if not release_order.is_monotonic_increasing:
        raise BlockedError('Out-of-order revisions require a verified vintage policy')
    d = decisions.copy()
    d['decision_at'] = require_aware(d['decision_at'], 'decision_at')
    local_dates = d.decision_at.dt.tz_convert('Asia/Seoul').dt.tz_localize(None).dt.normalize()
    if not local_dates.between(START, END).all():
        raise BlockedError('Decision outside approved period')
    d['_input_order'] = np.arange(len(d))
    # A future record with a future release can never match an earlier decision.
    out = pd.merge_asof(d.sort_values('decision_at'), r.sort_values('available_at'),
                        left_on='decision_at', right_on='available_at', direction='backward')
    out['age'] = out.decision_at - out.observed_at
    out['availability_age'] = out.decision_at - out.available_at
    stale = out.observed_at.isna() | (out.age > age_limit)
    out['status'] = np.where(stale, 'BLOCKED', 'PASS')
    out['reason'] = np.where(out.observed_at.isna(), 'no_prior_available_observation',
                             np.where(stale,'max_age_exceeded','latest_available'))
    out.loc[stale,'value'] = np.nan
    out['variable'] = variable
    out['availability_evidence'] = metadata['availability_evidence']
    return out.sort_values('_input_order').drop(columns='_input_order').reset_index(drop=True)

def us_schedule_records(values, schedule, *, schedule_verified, source, source_sha256,
                        release_policy_verified, release_delay=None):
    """Use an externally verified session-close schedule; DST/early closes live there.

    A zero delay is allowed only with explicit release-policy evidence. No inferred times.
    schedule columns: source_date, market_close (aware America/New_York or aware UTC).
    """
    if not schedule_verified or not release_policy_verified or release_delay is None:
        raise BlockedError('US schedule/release latency not verified')
    s = cutoff(schedule,'source_date')
    s['observed_at'] = require_aware(s['market_close'],'market_close')
    delay = pd.Timedelta(release_delay)
    if delay < pd.Timedelta(0):
        raise BlockedError('Negative release delay')
    out = cutoff(values,'source_date').merge(s[['source_date','observed_at']],on='source_date',how='left',validate='one_to_one')
    if out.observed_at.isna().any():
        raise BlockedError('US session missing from verified schedule')
    out['available_at'] = out.observed_at + delay
    out['source'] = source
    out['source_sha256'] = source_sha256
    out['record_id'] = out.source_date.dt.strftime('%Y-%m-%d')
    return out
