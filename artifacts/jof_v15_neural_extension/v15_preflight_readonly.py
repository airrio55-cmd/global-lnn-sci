"""Read-only V15 real-data preflight. NO neural fit or outcome statistics.
Run from repo root: python artifacts/jof_v15_neural_extension/v15_preflight_readonly.py --repo . 
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

MARKETS = {'SP500':'sp500_rerun','NASDAQ100':'nasdaq100','NIKKEI225':'nikkei225',
           'EUROSTOXX50':'eurostoxx50','KOSPI200':'kospi200'}
ORIGINS = [(2013,2015),(2014,2016),(2015,2017),(2016,2018),(2017,2019),(2018,2020)]
H=W=20

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dates_for(year0,year1,dates,features):
    end=np.datetime64(f'{year1+1}-01-01');start=np.datetime64(f'{year0}-01-01')
    return [i for i in range(201,len(dates)-H)
            if start<=dates[i]<end and dates[i+H]<end
            and np.isfinite(features[i-W:i]).all()]

def audit(repo):
    root=Path(repo).resolve()
    base=root/'artifacts/jof_phase1_benchmark_expansion'
    manifest=json.loads((base/'data_manifest.json').read_text())
    locked=root/'artifacts/jof_v14_preregistered_replication/first_run_20261109/v14_scoring_dates.csv'
    reference=pd.read_csv(locked,dtype={'Origin':str})
    reference['Date']=pd.to_datetime(reference.Date).dt.strftime('%Y-%m-%d')
    if reference.duplicated(['Market','Origin','Period','Date']).any():
        raise ValueError('Duplicated V14 reference dates')
    logcols=['Log_Ret','Disparity20']
    group_count=0;summary=[]
    for market,folder in MARKETS.items():
        row=next(a for a in manifest['markets'] if a['Market']==market)
        rawfile=root/'artifacts'/folder/'market_input.csv'
        featfile=base/'frozen_features'/f'{market}.csv'
        for path,k in ((rawfile,'Market_input_sha256'),(featfile,'Feature_input_sha256')):
            if sha(path)!=row[k]:
                raise RuntimeError(f'{market}: {k} mismatch')
        raw=pd.read_csv(rawfile,index_col=0,parse_dates=True,float_precision='round_trip')
        feats=pd.read_csv(featfile,index_col=0,parse_dates=True,float_precision='round_trip')
        if not raw.index.equals(feats.index) or not raw.index.is_monotonic_increasing or raw.index.has_duplicates:
            raise ValueError(f'{market}: index mismatch')
        cols=row['Feature_names']
        if not set(logcols).issubset(feats.columns) or not set(cols).issubset(feats.columns):
            raise ValueError(f'{market}: missing frozen feature columns')
        dates=raw.index.to_numpy(dtype='datetime64[D]')
        a=feats[cols].to_numpy(float);b=feats[logcols].to_numpy(float)
        for vy,ty in ORIGINS:
            label=f'O{vy-2012}'
            for period,s,e in [('Validation',vy,vy+1),('Test',ty,ty+1)]:
                indices=dates_for(s,e,dates,a)
                log_indices=set(dates_for(s,e,dates,b))
                if not set(indices).issubset(log_indices):
                    raise RuntimeError(f'{market}/{label}/{period}: LOG missing on RAW dates')
                actual=[str(dates[i]) for i in indices]
                expected=reference.loc[(reference.Market==market)&
                         (reference.Origin==label)&(reference.Period==period),'Date'].tolist()
                if actual!=expected:
                    raise RuntimeError(f'{market}/{label}/{period}: V14 dates mismatch')
                for train_year in ([vy-1,vy] if period=='Validation' else [ty-1]):
                    tr=dates_for(2010,train_year,dates,a)
                    if not tr or dates[tr[-1]+H]>=np.datetime64(f'{train_year+1}-01-01'):
                        raise RuntimeError(f'{market}/{label}: train label cutoff violation')
                    if not np.isfinite(b[np.concatenate([np.arange(i-W,i) for i in tr])]).all():
                        raise RuntimeError(f'{market}/{label}: LOG missing on train inputs')
                group_count+=1;summary.append((market,label,period,len(indices)))
    if group_count!=60:raise AssertionError(f'Expected 60 date groups, found {group_count}')
    return {'status':'PREFLIGHT_PASS','groups':group_count,
            'no_training':True,'no_outcome_evaluation':True,'summary':summary}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    report=audit(args.repo)
    if args.out:
        args.out.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: read-only V15 date and input checks (60 groups), no model fitting')

if __name__=='__main__':main()
