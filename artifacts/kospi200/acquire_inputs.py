"""Original target observations + frozen lagged Yahoo auxiliary series only."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def day_end(date,zone):
    if pd.isna(date):return pd.NaT
    return (pd.Timestamp(date).normalize().tz_localize(zone)+pd.DateOffset(days=1)-pd.Timedelta(nanoseconds=1)).tz_convert('UTC')

def prepare_input_sources(ns):
    out=Path('artifacts/kospi200');directory=out/'sources';directory.mkdir(exist_ok=True)
    lock=json.loads((out/'protocol_lock.json').read_text())
    source=Path(lock['primary_path']);assert digest(source)==lock['primary_sha256']
    original=pd.read_csv(source,float_precision='round_trip')
    original['Date']=pd.to_datetime(original.Date,errors='raise')
    frame=original[original.Date.between(ns['START_DATE'],ns['END_DATE'])].copy()
    assert not frame.Date.duplicated().any()
    assert frame.Date.is_monotonic_increasing
    close=pd.to_numeric(frame['종가'],errors='raise')
    assert close.notna().all() and np.isfinite(close).all() and (close>0).all()
    assert len(frame)==3894
    assert frame.Date.min()==pd.Timestamp('2010-01-04') and frame.Date.max()==pd.Timestamp('2025-12-30')
    dates=pd.DatetimeIndex(frame.Date,name='Date')
    primary=pd.DataFrame({'Close':close.to_numpy()},index=dates)
    f=directory/'Close.csv'
    if f.exists():
        frozen=pd.read_csv(f,index_col=0,parse_dates=True,float_precision='round_trip')
        pd.testing.assert_frame_equal(frozen,primary)
    else:primary.to_csv(f,float_format='%.17g')
    calendar={'status':'passed_empirical_integrity','policy':lock['calendar_policy'],'XKRX_expected_rows':3939,'observed_rows':3894,'difference':45,'classification':'calendar implementation discrepancy','discrepancy_not_confirmed_as_missing_KRX_observations':True,'pykrx_verification':'unavailable because current index endpoint returned empty data (user-reported); cloud acquisition independently blocked by proxy CONNECT 403','pykrx_verification_claimed':False,'duplicates':0,'Close_NaN':0,'Close_nonpositive':0,'date_ascending':True,'period':['2010-01-01','2025-12-31'],'first_observation':str(dates.min().date()),'last_observation':str(dates.max().date()),'target_imputation':False}
    (out/'calendar_audit.json').write_text(json.dumps(calendar,indent=2)+'\n')
    manifest_file=out/'sources_manifest.json'
    meta=json.loads(manifest_file.read_text()) if manifest_file.exists() else {'sources':{}}
    meta['primary']={'path':str(source),'sha256':digest(source),'provenance_path':'data/KOSPI200_provenance.json','provenance_sha256':digest('data/KOSPI200_provenance.json'),'source':'User-provided original research KOSPI200 data; identity attested by user','selected_columns':{'Date':'Date','Close':'종가'},'period_filter':[ns['START_DATE'],ns['END_DATE']],'raw_rows':len(original),'selected_rows':len(primary),'calendar':calendar}
    meta['sources']['Close']={'sha256':digest(f),'source':'original user CSV, no target imputation'}
    def save():manifest_file.write_text(json.dumps(meta,indent=2)+'\n')
    save()
    loaded={}
    for name,ticker in {'USD_KRW':'KRW=X','SOX':'^SOX','VIX':'^VIX'}.items():
        file=directory/(name+'.csv')
        if file.exists():assert digest(file)==meta['sources'][name]['sha256']
        else:
            aux=ns['download_yf_series'](ticker,name)
            assert len(aux)>3500 and aux.index.is_unique and aux.index.is_monotonic_increasing
            assert aux.index.tz is None
            aux.to_csv(file,float_format='%.17g')
            meta['sources'][name]={'ticker':ticker,'sha256':digest(file),'downloaded_at_utc':datetime.now(timezone.utc).isoformat()}
            save()
        loaded[name]=pd.read_csv(file,index_col=0,parse_dates=True,float_precision='round_trip')
    timing=pd.DataFrame(index=dates)
    timing['Close_available_at_utc']=[day_end(d,'Asia/Seoul') for d in dates]
    for name,aux in loaded.items():
        shifted=aux[name].shift(1)
        source_dates=pd.Series(aux.index,index=aux.index).shift(1).where(shifted.notna()).reindex(dates).ffill()
        assert (source_dates.dropna()<source_dates.dropna().index).all()
        timing[name+'_source_date']=source_dates
        timing[name+'_available_at_utc']=[day_end(d,'America/New_York') for d in source_dates]
    timing.to_csv(out/'availability.csv')
    meta['availability_sha256']=digest(out/'availability.csv')
    meta['timing_policy']={'target':'Use observed CSV dates only; no reindexing or filling target Close','auxiliary':'One source-observation lag, reindex to observed target dates, auxiliary-only ffill; never bfill','availability':'Conservative source-date New York day-end including USDKRW; target Seoul day-end; all input rows precede target row','limitations':'Exact daily FX publication timestamp and historical revisions unavailable; not point-in-time-vintage certification'}
    save()
    (out/'unchanged_yahoo_sources.json').write_text(json.dumps({name:meta['sources'][name]['sha256'] for name in ['Close','USD_KRW','SOX','VIX']},indent=2)+'\n')
    def cached_download(ticker,out_name,start=ns['START_DATE'],end=ns['END_DATE']):
        specs={'KRW=X':'USD_KRW','^SOX':'SOX','^VIX':'VIX'}
        assert start==ns['START_DATE'] and end==ns['END_DATE'] and ticker in specs,'Frozen-input run; refresh disabled'
        f=loaded[specs[ticker]].copy();f.columns=[out_name];return f
    ns['download_yf_series']=cached_download
    return meta
