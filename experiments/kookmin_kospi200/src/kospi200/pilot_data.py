"""O1-only retrospective pilot staging and preprocessing. No model training."""
import csv,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from .data import Calendar,BlockedError,labels_on_calendar,local_features
from .folds import window_dates,train_only_scaler,transform_checked
FEATURES=['Log_Ret','Disparity']

def sha256(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_verified_o1_prefix(path,sessions):
    """Read exactly the known 2010..2020 prefix. Never iterate any Test-price row.

    Caller first verifies entire file identity against a prior 3939-session audit.
    File hashing is integrity-only; no post-2020 Close is parsed here.
    """
    sessions=pd.DatetimeIndex(sessions)
    if not len(sessions) or sessions.has_duplicates or not sessions.is_monotonic_increasing or (sessions.year>2020).any():
        raise BlockedError('Invalid O1-only sessions')
    rows=[]
    with Path(path).open(newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=['Date','Close']:raise BlockedError('Expected exact Date/Close candidate schema')
        for expected in sessions:
            row=next(reader,None)
            if row is None or pd.Timestamp(row['Date'])!=expected:raise BlockedError('O1 prefix date/calendar mismatch')
            close=float(row['Close'])
            if not np.isfinite(close) or close<=0:raise BlockedError('Invalid O1 close')
            rows.append((expected,close))
        # Deliberately NO next(reader), EOF scan, or post-2020 numeric parsing.
    return pd.DataFrame(rows,columns=['Date','Close'])

def prepare_pilot_arrays(prices,session_frame,*,calendar_source,calendar_sha256):
    if list(prices.columns)!=['Date','Close'] or list(session_frame.columns)!=['Date','session_id']:
        raise BlockedError('Unexpected staging schema')
    dates=pd.DatetimeIndex(pd.to_datetime(session_frame.Date),name='Date')
    if (dates.year>2020).any() or (pd.to_datetime(prices.Date).dt.year>2020).any():raise BlockedError('Test/future prices forbidden')
    if not np.array_equal(session_frame.session_id.to_numpy(),np.arange(len(dates))):raise BlockedError('Session ID gaps')
    c=prices.copy();c['Date']=pd.to_datetime(c.Date)
    if not pd.DatetimeIndex(c.Date).equals(dates):raise BlockedError('Candidate must exactly match O1 calendar')
    if not np.isfinite(c.Close).all() or c.Close.le(0).any():raise BlockedError('Nonfinite/nonpositive prices')
    calendar=Calendar(dates,calendar_source,calendar_sha256,True)
    labels=labels_on_calendar(c.set_index('Date').Close,calendar,20)
    features=local_features(c.set_index('Date').Close)
    eligible=features.notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20)
    valid_start=dates[dates.year==2020][0]
    train_raw=labels.index[labels.index.year<=2019];valid_raw=labels.index[labels.index.year==2020]
    purge=labels.label_end.ge(valid_start)&labels.index.isin(train_raw)
    train=labels.index[(labels.index.year<=2019)&eligible&labels.Target.notna()&labels.label_end.lt(valid_start)]
    valid=labels.index[(labels.index.year==2020)&eligible&labels.Target.notna()&labels.label_end.le(pd.Timestamp('2020-12-31'))]
    windows=window_dates(dates,train,window=20,include_t=True)
    fit_dates=pd.DatetimeIndex(sorted({d for value in windows.values() for d in value}))
    scaler,lineage=train_only_scaler(features[FEATURES],fit_dates,valid_start)
    finite=features[FEATURES].notna().all(axis=1)
    scaled=transform_checked(scaler,features.loc[finite,FEATURES])
    arrays={};date_info={}
    for name,indices in [('train',train),('validation',valid)]:
        ws=window_dates(dates,indices,window=20,include_t=True)
        if len(ws)!=len(indices) or any(len(w)!=20 or w[-1]!=t or w.max()>t for t,w in ws.items()):raise BlockedError('Window alignment failure')
        xx=np.stack([scaled.loc[ws[t]].to_numpy(dtype=np.float32) for t in indices])
        yy=labels.loc[indices,'Target'].to_numpy(dtype=np.int64)
        if not np.isfinite(xx).all() or set(np.unique(yy))!={0,1}:raise BlockedError('Invalid model arrays/classes')
        arrays[name]=(xx,yy);date_info[name]={'dates':[str(t.date()) for t in indices],'label_end':[str(t.date()) for t in labels.loc[indices,'label_end']]}
    ids=pd.Series(session_frame.session_id.to_numpy(),index=dates)
    end_ids=ids.reindex(pd.DatetimeIndex(labels.label_end.dropna())).to_numpy()
    base_ids=ids.loc[labels.label_end.notna()].to_numpy()
    if not np.equal(end_ids-base_ids,20).all():raise BlockedError('Horizon not exactly20 sessions')
    meta={'price_rows':len(c),'price_start':str(dates.min().date()),'price_end':str(dates.max().date()),'test_price_rows_read':0,
       'train_boundary_start':str(train_raw.min().date()),'train_boundary_end':str(train_raw.max().date()),
       'validation_boundary_start':str(valid_raw.min().date()),'validation_boundary_end':str(valid_raw.max().date()),
       'train_samples':len(train),'validation_samples':len(valid),'train_purged':int(purge.sum()),
       'validation_unknown_excluded':int(labels.loc[valid_raw,'Target'].isna().sum()),
       'train_first_sample':str(train.min().date()),'train_last_sample':str(train.max().date()),
       'validation_first_sample':str(valid.min().date()),'validation_last_sample':str(valid.max().date()),
       'train_max_label_end':str(labels.loc[train,'label_end'].max().date()),'validation_max_label_end':str(labels.loc[valid,'label_end'].max().date()),
       'train_label_cutoff_violations':int(labels.loc[train,'label_end'].ge(valid_start).sum()),
       'validation_future_endpoint_violations':int(labels.loc[valid,'label_end'].gt(pd.Timestamp('2020-12-31')).sum()),
       'feature_order':FEATURES,'auxiliary_not_model_input':['Vol_Regime'],'window':20,'include_t':True,
       'common_Vol_Regime_window_mask':True,'2026_observations_used':0,'scaler':{**lineage,'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'var':scaler.var_.tolist()},
       'class_counts':{k:{'0':int((y==0).sum()),'1':int((y==1).sum())} for k,(_,y) in arrays.items()}}
    if (meta['price_rows'],meta['train_samples'],meta['validation_samples'],meta['train_purged'],meta['validation_unknown_excluded'])!=(2714,2387,228,20,20):
        raise BlockedError('Frozen O1 sample/purge counts changed')
    return arrays,meta,date_info

def validation_metrics(y,probability):
    y=np.asarray(y);p=np.asarray(probability,dtype=float)
    if y.shape!=p.shape or set(np.unique(y))!={0,1} or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise BlockedError('Invalid validation labels/probabilities')
    pred=(p>.5).astype(np.int64);recall=[];f1=[]
    for c in [0,1]:
        true=y==c;guess=pred==c;tp=int((true&guess).sum());fn=int((true&~guess).sum());fp=int((~true&guess).sum())
        recall.append(tp/(tp+fn));f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.)
    positive=float(pred.mean())
    return {'validation_BA':float(np.mean(recall)),'macro_f1':float(np.mean(f1)),'recall0':recall[0],'recall1':recall[1],
            'accuracy':float((pred==y).mean()),'brier':float(np.mean((p-y)**2)),'prediction_positive_rate':positive,
            'prediction_status':'DEGENERATE_PREDICTION' if positive in [0.,1.] else 'TWO_CLASS_PREDICTION'}
