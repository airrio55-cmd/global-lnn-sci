"""Shared draft-only integrity helpers; no training or outcome statistics."""
import sys
sys.dont_write_bytecode=True  # Keep future clean-checkout lock verification usable after local imports.
from pathlib import Path
import hashlib,json
import numpy as np
MARKETS={'SP500':'sp500_rerun','NASDAQ100':'nasdaq100','NIKKEI225':'nikkei225','EUROSTOXX50':'eurostoxx50','KOSPI200':'kospi200'}
ORIGINS=tuple((2013+i,2015+i) for i in range(6))
LOGCOLS=('Log_Ret','Disparity20');SEEDS=(42,52,62);H=W=20
BASE='artifacts/jof_v14_preregistered_replication/first_run_20261109'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def required_inventory(root):
 root=Path(root).resolve();paths=[]
 for market,folder in MARKETS.items():
  paths += [f'artifacts/{folder}/market_input.csv',f'artifacts/{folder}/SCI_v1_4_WALKFORWARD_{market}.ipynb',f'artifacts/{folder}/leakage_audit.json']
 paths += [f'artifacts/jof_phase1_benchmark_expansion/frozen_features/{m}.csv' for m in MARKETS]
 paths += ['artifacts/jof_phase1_benchmark_expansion/data_manifest.json','artifacts/jof_v14_preregistered_replication/run_v14_locked.py']
 paths += [f'{BASE}/{n}' for n in ['v14_scoring_dates.csv','v14_unit_level.csv','v14_input_inventory.json']]
 paths += [str(p.relative_to(root)) for p in sorted((root/'artifacts/jof_v15_neural_extension').glob('*.py'))]
 return paths

def validate_config(cfg):
 if cfg.get('epochs')!=60 or cfg.get('loss')!='CE' or cfg.get('seeds')!=list(SEEDS):raise ValueError('Expected draft fixed60 epochs,CE,seeds42/52/62')
 if cfg.get('H')!=20 or cfg.get('W')!=20:raise ValueError('Expected H=W20')
 if cfg.get('H1_families')!=['LSTM','LTC_RAW','CfC_RAW']:raise ValueError('H1 must have exactly three architecture families')
 if cfg.get('evaluated_variants')!=['LSTM','LTC_RAW','CfC_RAW','CfC_LOG','CfC_ENSEMBLE']:raise ValueError('Expected four branches and one derived ensemble')
 if cfg.get('device')!='cpu':raise ValueError('Only audited CPU execution is supported')
 if cfg.get('log_columns')!={m:list(LOGCOLS) for m in MARKETS}:raise ValueError('LOG must be exactly ordered Log_Ret,Disparity20 in all markets')
 if cfg.get('ensemble')!='CfC_RAW_0.5 + CfC_LOG_0.5; seed mean after matched-seed pair':raise ValueError('Ensemble differs from fixed matched-seed50/50')
 if cfg.get('log_representation_provenance',{}).get('classification')!='new_prespecified':raise ValueError('V15 LOG is a new five-market adaptation, not exact historical replication')
 return True

def require_training(cfg):
 validate_config(cfg)
 if cfg.get('status')!='LOCKED' or cfg.get('permission_to_train') is not True:raise RuntimeError('DRAFT: fitting is forbidden')

def integrity(raw,features,cols):
 if not raw.index.equals(features.index) or raw.index.has_duplicates or not raw.index.is_monotonic_increasing:raise ValueError('Invalid or mismatched chronological index')
 close=raw.Close.to_numpy(float)
 if not np.isfinite(close).all() or (close<=0).any():raise ValueError('Close must be finite and positive; no filling permitted')
 if not np.array_equal(close,features.Close.to_numpy(float)):raise ValueError('Frozen Close mismatch')
 if len(set(cols))!=len(cols) or not set(cols).issubset(features):raise ValueError('Invalid ordered feature columns')

def reference_dates(root):
 import pandas as pd
 ref=pd.read_csv(Path(root)/BASE/'v14_scoring_dates.csv',dtype={'Origin':str});ref['Date']=pd.to_datetime(ref.Date).dt.strftime('%Y-%m-%d')
 key=['Market','Origin','Period','Date']
 if ref.duplicated(key).any() or ref[key].isna().any().any():raise ValueError('Invalid V14 reference dates')
 expected={(m,f'O{i}',p) for m in MARKETS for i in range(1,7) for p in ['Validation','Test']}
 if set(ref.groupby(key[:3]).groups)!=expected:raise ValueError('Incomplete V14 reference60groups')
 return ref
