"""Own-Origin Test windows from bounded prices; saved Train scaler transform only."""
from pathlib import Path
import csv,hashlib
import numpy as np,pandas as pd
from .data import BlockedError,local_features
from .manual_evaluation import assign_manual_regimes
FEATURES=['Log_Ret','Disparity']
def read_price_prefix(path,sessions):
 dates=pd.DatetimeIndex(sessions);rows=[]
 if dates.has_duplicates or not dates.is_monotonic_increasing or len(dates)==0 or dates.max()>pd.Timestamp('2025-12-31'):raise BlockedError('Invalid permitted prefix')
 with Path(path).open(newline='') as f:
  reader=csv.DictReader(f)
  if reader.fieldnames!=['Date','Close']:raise BlockedError('Unfrozen price schema')
  for d in dates:
   row=next(reader,None)
   if row is None or pd.Timestamp(row['Date'])!=d:raise BlockedError('Official prefix mismatch')
   p=float(row['Close'])
   if not np.isfinite(p) or p<=0:raise BlockedError('Nonpositive/nonfinite close')
   rows.append((d,p))
  # Never peek at a later source row; file hashing elsewhere is identity-only.
 return pd.Series([v for _,v in rows],index=dates,name='Close')
def build_test(close,sessions,origin,scaler,reference):
 dates=pd.DatetimeIndex(sessions);year=2020+int(origin[1:]);base=dates[dates.year==year];ids=pd.Series(np.arange(len(dates)),index=dates);known=base[ids.loc[base].to_numpy()+20<len(dates)]
 maxend=dates[int(ids.loc[known[-1]])+20]
 if not close.index.equals(dates[:dates.get_loc(maxend)+1]):raise BlockedError('Price prefix exceeds/does not cover allowed endpoints')
 if scaler['feature_order']!=FEATURES or scaler['source_partition']!='train' or pd.Timestamp(scaler['fit_end']).year>=year-1:raise BlockedError('Saved Train-only scaler/order mismatch')
 # Target endpoint suffix is never given to feature/window construction.
 feature_dates=dates[dates<=base[-1]];features=local_features(close.reindex(feature_dates));eligible=features.notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20);idx=known[eligible.reindex(known).to_numpy()]
 if len(idx)!=len(known):raise BlockedError('Unexpected input finite-mask losses; no silent sample selection')
 mean=np.asarray(scaler['mean']);scale=np.asarray(scaler['scale'])
 if mean.shape!=(2,) or scale.shape!=(2,) or not np.isfinite(mean).all() or not np.isfinite(scale).all() or np.any(scale<=0):raise BlockedError('Invalid frozen scaler')
 scaled=(features[FEATURES]-mean)/scale;x=[];y=[];end=[];windows=[]
 for t in idx:
  i=dates.get_loc(t);w=dates[i-19:i+1];target_date=dates[i+20]
  if len(w)!=20 or w[-1]!=t or w.max()>t or target_date>maxend:raise BlockedError('Window/endpoint contract violated')
  x.append(scaled.loc[w].to_numpy(dtype=np.float32));y.append(int(close.loc[target_date]>close.loc[t]));end.append(str(target_date.date()));windows.append([str(d.date()) for d in w])
 xx=np.stack(x);yy=np.asarray(y,dtype=np.int64)
 if xx.shape!=(len(idx),20,2) or not np.isfinite(xx).all():raise BlockedError('Invalid Test array')
 regimes=assign_manual_regimes(features.loc[idx,'Vol_Regime'],reference).to_numpy()
 meta={'origin':origin,'test_year':year,'samples':len(idx),'unknown_excluded':len(base)-len(known),'input_ineligible':len(known)-len(idx),'price_prefix_end':str(maxend.date()),'feature_history_end':str(base[-1].date()),'date_start':str(idx[0].date()),'date_end':str(idx[-1].date()),'label_end_max':end[-1],'feature_order':FEATURES,'scaler_fit':False,'threshold_refit':False,'manual_quantile_refit':False,'future_input_violations':0,'label_session_distance':20,'2026_used':0}
 return {'x':xx,'y':yy,'dates':np.array([str(d.date()) for d in idx]),'session_id':ids.loc[idx].to_numpy(dtype=np.int64),'label_end':np.array(end),'regime':regimes.astype(str),'volatility':features.loc[idx,'Vol_Regime'].to_numpy()},meta,windows
