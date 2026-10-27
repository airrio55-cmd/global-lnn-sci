"""Freeze four Yahoo histories exactly once; original SP500 raw source lag zero."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import pandas as pd
import numpy as np

def prepare_input_sources(ns):
    out=Path('artifacts/sp500_rerun');directory=out/'sources';directory.mkdir(exist_ok=True)
    path=out/'sources_manifest.json'
    meta=json.loads(path.read_text()) if path.exists() else {'sources':{}}
    specs={'Close':'^GSPC','VIX':'^VIX','US10Y':'^TNX','DXY':'DX-Y.NYB'}
    loaded={}
    for name,ticker in specs.items():
        file=directory/(name+'.csv')
        if file.exists():assert hashlib.sha256(file.read_bytes()).hexdigest()==meta['sources'][name]['sha256']
        else:
            f=ns['download_yf_series'](ticker,name)
            assert len(f)>3500 and f.index.is_unique and f.index.is_monotonic_increasing
            f.to_csv(file,float_format='%.17g')
            meta['sources'][name]={'ticker':ticker,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'downloaded_at_utc':datetime.now(timezone.utc).isoformat()}
            path.write_text(json.dumps(meta,indent=2))
        loaded[name]=pd.read_csv(file,index_col=0,parse_dates=True,float_precision='round_trip')
    dates=loaded['Close'].index
    assert dates.tz is None and dates.is_unique and dates.is_monotonic_increasing
    assert np.isfinite(loaded['Close'].Close).all() and (loaded['Close'].Close>0).all()
    timing=pd.DataFrame(index=dates)
    for name,source in loaded.items():
        # Original SP500 config: source-observation lag 0, target calendar + ffill.
        sd=pd.Series(source.index,index=source.index).where(source[name].notna()).reindex(dates).ffill()
        timing[name+'_source_date']=sd
        timing[name+'_available_at_utc']=[(pd.Timestamp(d).tz_localize('America/New_York')+pd.DateOffset(days=1)-pd.Timedelta(nanoseconds=1)).tz_convert('UTC') if pd.notna(d) else pd.NaT for d in sd]
    timing.to_csv(out/'availability.csv')
    meta['availability_sha256']=hashlib.sha256((out/'availability.csv').read_bytes()).hexdigest()
    meta['policy']='Original archived SP500 source lag 0; conservative source-date New York day-end; sequence excludes target row; no initial bfill.'
    path.write_text(json.dumps(meta,indent=2))
    (out/'unchanged_yahoo_sources.json').write_text(json.dumps({n:meta['sources'][n]['sha256'] for n in specs},indent=2))
    def cached(ticker,out_name,start=ns['START_DATE'],end=ns['END_DATE']):
        assert start==ns['START_DATE'] and end==ns['END_DATE'] and ticker in specs.values()
        name=next(n for n,t in specs.items() if t==ticker)
        f=loaded[name].copy();f.columns=[out_name];return f
    ns['download_yf_series']=cached
    return meta
