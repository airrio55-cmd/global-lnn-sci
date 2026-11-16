"""Pure config/probability operations; no model construction or forward."""
import numpy as np
from .data import BlockedError

RAW=['Log_Ret','Foreign_Net','Nasdaq','SOX','Disparity']
LOG=['Log_Ret','Disparity']
ABLATIONS={'F0':RAW,'F1':LOG,'F2':[f for f in RAW if f!='Foreign_Net'],
           'F3':[f for f in RAW if f!='Nasdaq'],'F4':[f for f in RAW if f!='SOX'],
           'F5':['Log_Ret','Disparity','Foreign_Net']}
OFFSETS={'RNN_RAW':101,'RNN_LOG':102,'LSTM_RAW':201,'LSTM_LOG':202,'GRU_RAW':301,
         'GRU_LOG':302,'LTC_RAW':401,'LTC_LOG':402,'CfC_RAW':501,'CfC_LOG':502}

def validate_config(c):
    assert c['training_enabled'] is False and c['hmm_fit_enabled'] is False
    assert c['period']=={'start':'2010-01-01','end':'2025-12-31','use_2026_for_targets':False}
    assert c['seeds']==[2,12,22,32,42,52,62,72,82,92]
    assert c['features']=={'RAW':RAW,'LOG':LOG} and c['ablations']==ABLATIONS
    assert c['seed_offsets']==OFFSETS
    assert c['bootstrap']=={'block_lengths':[20,40,60],'replicates':10000,'seed':20261116,'correction':'Holm'}
    expected={'hidden_size':128,'layers':1,'dropout':.2,'window':20,'horizon':20,'batch':64,
       'max_epochs':100,'patience':10,'selection_metric':'balanced_accuracy','optimizer':'AdamW',
       'lr':.005,'weight_decay':1e-4,'scheduler':'OneCycleLR','focal_gamma':2,'focal_alpha':.25,
       'gradient_clip':1.,'dtype':'float32','amp':False,'threshold':.5}
    assert c['model']==expected
    return True

def common_ablation_dates(frames):
    dates=None
    for f in frames.values():
        finite=f.index[np.isfinite(f.to_numpy(dtype=float)).all(axis=1)]
        dates=finite if dates is None else dates.intersection(finite)
    return dates.sort_values()

def ensemble(ltc_raw,ltc_log,rnn_raw):
    arrays=[np.asarray(x,dtype=float) for x in (ltc_raw,ltc_log,rnn_raw)]
    if len({x.shape for x in arrays})!=1 or any(not np.isfinite(x).all() or ((x<0)|(x>1)).any() for x in arrays):
        raise BlockedError('Probability shape/range mismatch; align origin/seed/date keys first')
    lnn=.5*arrays[0]+.5*arrays[1]
    return {'LNN Ensemble':lnn,'Hybrid_SOTA':.7*lnn+.3*arrays[2]}

def keyed_ensemble(probabilities):
    """Enforce same Origin/Seed/date before combining precomputed probabilities."""
    import pandas as pd
    df=probabilities.copy();keys=['origin','seed','date']
    df['date']=pd.to_datetime(df.date)
    if df.duplicated(keys+['model']).any() or not df.date.between('2010-01-01','2025-12-31').all():
        raise BlockedError('Duplicate keyed probability or period violation')
    wide=df.pivot(index=keys,columns='model',values='probability')
    names=['LTC_RAW','LTC_LOG','RNN_RAW']
    if not set(names).issubset(wide) or wide[names].isna().any().any():
        raise BlockedError('Same-seed RAW/LOG/RNN probabilities missing')
    out=ensemble(*[wide[n].to_numpy() for n in names])
    return pd.DataFrame(out,index=wide.index).reset_index()

def experiment_plan(config):
    """Declarative jobs only. Does not construct, load or run a model."""
    validate_config(config);jobs=[]
    for origin in config['origins']:
        for spec,raw_features in config['ablations'].items():
            for seed in config['seeds']:
                for model in config['models']:
                    for channel in ['RAW','LOG']:
                        jobs.append({'origin':origin['origin'],'feature_spec':spec,'seed':seed,
                            'model':model,'channel':channel,'features':list(raw_features if channel=='RAW' else LOG),
                            'effective_seed':seed+OFFSETS[f'{model}_{channel}'],
                            'training_enabled':False,'status':'BLOCKED_PENDING_DATA_GATES'})
    return jobs
