"""Origin-bounded retrospective pilot data; never constructs independent Test inputs."""
from pathlib import Path
import csv
import numpy as np,pandas as pd
from .data import Calendar,BlockedError,labels_on_calendar,local_features
from .folds import window_dates,train_only_scaler,transform_checked
from .manual_evaluation import freeze_manual_reference,assign_manual_regimes
FEATURES=['Log_Ret','Disparity']

def read_origin_prefix(path,sessions,validation_year):
    dates=pd.DatetimeIndex(sessions)
    if dates.has_duplicates or not dates.is_monotonic_increasing or not len(dates) or (dates.year>validation_year).any():raise BlockedError('Invalid origin prefix')
    rows=[]
    with Path(path).open(newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=['Date','Close']:raise BlockedError('Unexpected source schema')
        for date in dates:
            row=next(reader,None)
            if row is None or pd.Timestamp(row['Date'])!=date:raise BlockedError('Official prefix mismatch')
            value=float(row['Close'])
            if not np.isfinite(value) or value<=0:raise BlockedError('Invalid origin price')
            rows.append((date,value))
        # Never peek at or parse a price row after this Origin's Validation year.
    return pd.DataFrame(rows,columns=['Date','Close'])

def prepare_origin(prices,session_frame,*,origin,calendar_source,calendar_sha256):
    if origin not in ['O1','O2']:raise BlockedError('Unapproved Origin')
    validation_year={'O1':2020,'O2':2021}[origin];train_end=validation_year-1
    dates=pd.DatetimeIndex(pd.to_datetime(session_frame.Date),name='Date');p=prices.copy();p['Date']=pd.to_datetime(p.Date)
    if (dates.year>validation_year).any() or (p.Date.dt.year>validation_year).any():raise BlockedError('Independent Test/future row forbidden')
    if not pd.DatetimeIndex(p.Date).equals(dates) or not np.array_equal(session_frame.session_id,np.arange(len(dates))):raise BlockedError('Session IDs or dates invalid')
    if not np.isfinite(p.Close).all() or p.Close.le(0).any():raise BlockedError('Price invalid; no interpolation')
    cal=Calendar(dates,calendar_source,calendar_sha256,True);close=p.set_index('Date').Close
    labels=labels_on_calendar(close,cal,20);features=local_features(close)
    mask=features.notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20)
    vstart=dates[dates.year==validation_year][0];cutoff=pd.Timestamp(f'{validation_year}-12-31')
    train=labels.index[(labels.index.year<=train_end)&mask&labels.Target.notna()&labels.label_end.lt(vstart)]
    valid=labels.index[(labels.index.year==validation_year)&mask&labels.Target.notna()&labels.label_end.le(cutoff)]
    win=window_dates(dates,train);fit=pd.DatetimeIndex(sorted({d for w in win.values() for d in w}))
    scaler,lineage=train_only_scaler(features[FEATURES],fit,vstart)
    finite=features[FEATURES].notna().all(axis=1);scaled=transform_checked(scaler,features.loc[finite,FEATURES])
    arrays={};date_info={}
    for name,idx in [('train',train),('validation',valid)]:
        windows=window_dates(dates,idx)
        if len(windows)!=len(idx) or any(len(w)!=20 or w[-1]!=t or w.max()>t for t,w in windows.items()):raise BlockedError('Invalid input window')
        x=np.stack([scaled.loc[windows[t]].to_numpy(dtype=np.float32) for t in idx]);y=labels.loc[idx,'Target'].to_numpy(dtype=np.int64)
        if not np.isfinite(x).all() or set(np.unique(y))!={0,1}:raise BlockedError('Input/label failure')
        arrays[name]=(x,y);date_info[name]={'dates':[str(d.date()) for d in idx],'label_end':[str(d.date()) for d in labels.loc[idx,'label_end']]}
    ids=pd.Series(session_frame.session_id.to_numpy(),index=dates);known=labels.label_end.notna()
    if not np.equal(ids.reindex(pd.DatetimeIndex(labels.loc[known,'label_end'])).to_numpy()-ids.loc[known].to_numpy(),20).all():raise BlockedError('Not exactly20 official sessions')
    purge=int(((labels.index.year<=train_end)&labels.label_end.ge(vstart)).sum());unknown=int(labels.loc[labels.index.year==validation_year,'Target'].isna().sum())
    expected={'O1':(2714,2387,228),'O2':(2962,2635,228)}[origin]
    if (len(dates),len(train),len(valid))!=expected or purge!=20 or unknown!=20:raise BlockedError('Frozen origin counts/purge mismatch')
    reference=freeze_manual_reference(features.Vol_Regime,train,validation_start=vstart,partition='train')
    regimes=assign_manual_regimes(features.loc[valid,'Vol_Regime'],reference)
    support=[]
    for reg in ['Low_Vol','Mid_Vol','High_Vol']:
        y=labels.loc[regimes.index[regimes==reg],'Target'].astype(int)
        support.append({'regime':reg,'n':len(y),'n_class0':int(y.eq(0).sum()),'n_class1':int(y.eq(1).sum())})
    meta={'origin':origin,'validation_year':validation_year,'price_rows':len(dates),'price_start':str(dates.min().date()),'price_end':str(dates.max().date()),
          'train_samples':len(train),'validation_samples':len(valid),'train_purged':purge,'validation_unknown_excluded':unknown,
          'train_boundary_start':str(dates.min().date()),'train_boundary_end':str(dates[dates.year==train_end].max().date()),
          'validation_boundary_start':str(vstart.date()),'validation_boundary_end':str(dates.max().date()),
          'train_first_sample':str(train.min().date()),'train_last_sample':str(train.max().date()),'validation_first_sample':str(valid.min().date()),'validation_last_sample':str(valid.max().date()),
          'train_max_label_end':str(labels.loc[train,'label_end'].max().date()),'validation_max_label_end':str(labels.loc[valid,'label_end'].max().date()),
          'train_cutoff_violations':int(labels.loc[train,'label_end'].ge(vstart).sum()),'validation_future_endpoint_violations':int(labels.loc[valid,'label_end'].gt(cutoff).sum()),
          'feature_order':FEATURES,'common_Vol_Regime_window_mask':True,'scaler':{**lineage,'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'var':scaler.var_.tolist()},
          'class_counts':{k:{'0':int((y==0).sum()),'1':int((y==1).sum())} for k,(_,y) in arrays.items()},
          'manual_reference':reference,'manual_validation_support':support,'independent_Test_rows':0,'2026_used':0}
    return arrays,meta,date_info,regimes
