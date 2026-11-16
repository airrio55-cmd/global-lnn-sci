"""STEP2.6 user-supplied price reconciliation, not official-source certification."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from .data import START,END,BlockedError,labels_on_calendar,local_features

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_prices(frame, *, date_col='Date', close_col='Close'):
    """Report source order, filter first, reject invalid in-period prices/duplicate dates."""
    if date_col not in frame or close_col not in frame:
        raise BlockedError('Explicit date/close columns required; no guessed columns')
    date=pd.to_datetime(frame[date_col],errors='coerce')
    if date.isna().any() or date.dt.tz is not None or not date.eq(date.dt.normalize()).all():
        raise BlockedError('Invalid/missing/non-session timestamp dates')
    mask=date.between(START,END)
    prices=pd.DataFrame({'Date':date.loc[mask], 'Close':pd.to_numeric(frame.loc[mask,close_col],errors='coerce')})
    if prices.Date.duplicated().any():raise BlockedError('Duplicate price dates')
    if not np.isfinite(prices.Close.to_numpy(dtype=float)).all() or (prices.Close<=0).any():
        raise BlockedError('Missing/nonfinite/nonpositive close; no interpolation')
    details={'raw_rows':len(frame),'in_period_rows':len(prices),'excluded_before_2010':int((date<START).sum()),
      'excluded_2026_or_later':int((date>END).sum()),'source_sorted_ascending':bool(date.is_monotonic_increasing),
      'source_sorted_descending':bool(date.is_monotonic_decreasing),'invalid_in_period_prices':0,'duplicate_dates':0}
    return prices.sort_values('Date').reset_index(drop=True),details

def reconcile_close(original, supplement, xlsx_supplement, *, calendar, expected_missing,
                    original_file, supplement_file, original_sha256, supplement_sha256):
    sessions=calendar.checked()
    a,meta_a=validate_prices(original);b,meta_b=validate_prices(supplement);x,meta_x=validate_prices(xlsx_supplement)
    if len(b)!=45 or len(x)!=45 or meta_b['raw_rows']!=45 or meta_x['raw_rows']!=45:
        raise BlockedError('Each supplement representation must contain exactly 45 rows')
    if not b.Date.equals(x.Date) or not np.array_equal(b.Close.to_numpy(),x.Close.to_numpy()):
        raise BlockedError('CSV/XLSX supplement mismatch')
    expected=pd.DatetimeIndex(expected_missing)
    if expected.has_duplicates or len(expected)!=45 or set(b.Date)!=set(expected):
        raise BlockedError('Supplement must match all expected 45 dates exactly')
    if a.Date.isin(b.Date).any():raise BlockedError('Supplement overlaps original; cannot silently replace prices')
    if not a.Date.isin(sessions).all() or not b.Date.isin(sessions).all():
        raise BlockedError('Non-KRX session observation')
    missing=sessions.difference(pd.DatetimeIndex(a.Date))
    if set(missing)!=set(expected):raise BlockedError('Original missing set differs from approved audit')
    def add(frame,kind,file,digest,status):
        out=frame.copy();out['source_type']=status;out['source_file']=file
        out['original_or_supplement']=kind;out['verified_session']=True;out['source_sha256']=digest;return out
    completed=pd.concat([add(a,'original',original_file,original_sha256,'USER_SUPPLIED_ORIGINAL_PRESERVED'),
                         add(b,'supplement',supplement_file,supplement_sha256,'USER_SUPPLIED_VERIFIED_MATCH')],ignore_index=True).sort_values('Date').reset_index(drop=True)
    if not pd.DatetimeIndex(completed.Date).equals(sessions):raise BlockedError('Completed prices must match every official KRX session one-to-one')
    return completed,{'original':meta_a,'supplement_csv':meta_b,'supplement_xlsx':meta_x,'rows':len(completed),
       'supplement_counted_once':True,'official_source_verified':False,'status':'PASS_USER_SUPPLIED_NUMERIC_SESSION_INTEGRITY'}

def full_excel_comparison(original, full_frame, *, calendar):
    """A second source is compared, never treated as truth or substituted into prices."""
    a,_=validate_prices(original)
    if full_frame is None:
        return pd.DataFrame({'Date':a.Date,'original_present':True,'full_excel_present':False,
             'exact_match':pd.NA,'within_1e_minus9':pd.NA,'rounded_2dp_match':pd.NA,'difference':pd.NA,
             'status':'BLOCKED_FULL_EXCEL_MISSING'})
    b,_=validate_prices(full_frame)
    if not pd.DatetimeIndex(b.Date).equals(calendar.checked()):raise BlockedError('Full Excel calendar coverage invalid')
    compared=a.merge(b,on='Date',how='left',suffixes=('_original','_excel'),validate='one_to_one')
    compared['difference']=compared.Close_excel-compared.Close_original
    compared['exact_match']=compared.Close_excel.eq(compared.Close_original)
    compared['within_1e_minus9']=np.isclose(compared.Close_excel,compared.Close_original,atol=1e-9,rtol=0)
    compared['rounded_2dp_match']=compared.Close_excel.round(2).eq(compared.Close_original.round(2))
    compared['status']=np.where(compared.exact_match,'EXACT_MATCH','PRICE_DIFFERENCE_REQUIRES_REVIEW')
    return compared

def build_labels_features(completed, calendar):
    close=completed.set_index('Date').Close
    labels=labels_on_calendar(close,calendar)
    ids=pd.Series(np.arange(len(calendar.checked())),index=calendar.sessions,dtype='Int64')
    labels['session_id']=ids;labels['label_end_session_id']=ids.shift(-20)
    features=local_features(close)
    ready=features.notna().all(axis=1)
    return labels,features,ready.rolling(20,min_periods=20).sum().eq(20)

def label_audit(original, completed, calendar):
    a,_=validate_prices(original);old=a.set_index('Date').Close
    labels,features,window_ok=build_labels_features(completed,calendar)
    old_end=pd.Series(old.index,index=old.index).shift(-20)
    future=old.shift(-20);known=future.notna()
    old_target=pd.Series(pd.NA,index=old.index,dtype='Int64');old_target.loc[known]=(future[known]>old[known]).astype(int)
    comparable=old_end.notna()&labels.label_end.reindex(old.index).notna()
    differences=pd.DataFrame({'Date':old.index,'old_label_end':old_end.to_numpy(),
      'new_label_end':labels.label_end.reindex(old.index).to_numpy(),'old_Target':old_target.to_numpy(),
      'new_Target':labels.Target.reindex(old.index).to_numpy()})
    differences['horizon_date_changed']=differences.old_label_end.notna()&differences.new_label_end.notna()&differences.old_label_end.ne(differences.new_label_end)
    differences['Target_changed']=pd.array([pd.NA if pd.isna(x) or pd.isna(y) else x!=y for x,y in zip(differences.old_Target,differences.new_Target)],dtype='boolean')
    def dist(v):
        v=v.dropna().astype(int);return {'known':len(v),'down_or_equal':int(v.eq(0).sum()),'up':int(v.eq(1).sum()),'up_ratio':float(v.mean()) if len(v) else None}
    summary={'comparison_scope':'Cutoff-first original observed-row reference, not exact historical notebook results',
       'old_known':dist(old_target),'new_known':dist(labels.Target),
       'legacy_bug_demo_distribution':dist((future>old).astype(int)),
       'old_unknown':int(old_target.isna().sum()),'new_unknown':int(labels.Target.isna().sum()),
       'horizon_discrepancies_before':int(differences.horizon_date_changed.sum()),
       'horizon_discrepancies_after_session_id_repair':int((labels.label_end_session_id-labels.session_id).dropna().ne(20).sum()),
       'common_known_compared':int(comparable.sum()),'common_Target_changes':int(differences.Target_changed.fillna(False).sum()),
       'common_down_to_up':int(((differences.old_Target==0)&(differences.new_Target==1)).sum()),
       'common_up_to_down':int(((differences.old_Target==1)&(differences.new_Target==0)).sum()),
       'old_unknown_to_new_known_on_common_dates':int((old_target.isna()&labels.Target.reindex(old.index).notna()).sum()),
       'last_valid_base':str(labels.index[labels.Target.notna()][-1].date()),'last_label_end':str(labels.loc[labels.Target.notna(),'label_end'].iloc[-1].date()),
       'unknown_start':str(labels.index[-20].date()),'unknown_end':str(labels.index[-1].date()),
       'feature_ready':int(features.notna().all(axis=1).sum()),'feature_ready_known_labels':int((features.notna().all(axis=1)&labels.Target.notna()).sum()),
       'window20_include_t_known_labels':int((window_ok&labels.Target.notna()).sum()),
       'feature_formula_policy':'Log_Ret=ln(C/C.shift(1)); Disparity=C/C.rolling(20).mean()-1; Vol_Regime=Log_Ret.rolling(40).std(ddof=1)',
       'feature_formula_changed':False,'2026_prices_used':0,'model_metrics_generated':False,'price_source_certification':'NOT_KRX_OFFICIAL_VERIFIED'}
    return labels,features,window_ok,differences,summary
