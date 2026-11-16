"""Date-paired moving blocks; seed repetition is not extra market dates."""
import numpy as np
import pandas as pd
from .data import BlockedError

def holm(pvalues):
    p=np.asarray(pvalues,dtype=float)
    if not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise BlockedError('Invalid p-values')
    order=np.argsort(p);out=np.empty(len(p));out[order]=np.minimum(1,np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p)))))
    return out

def paired_dates(predictions, model_a, model_b):
    """Input origin/date/seed/model/y/pred; average correctness across common seeds."""
    df=predictions.copy();keys=['origin','date','seed','model']
    df['date']=pd.to_datetime(df.date)
    if df.duplicated(keys).any() or not df['y'].isin([0,1]).all() or not df.pred.isin([0,1]).all():
        raise BlockedError('Duplicate keyed predictions or nonbinary labels/predictions')
    df=df[df.model.isin([model_a,model_b])]
    if len(df)==0 or (df.date<'2010-01-01').any() or (df.date>'2025-12-31').any():
        raise BlockedError('No paired data or date outside approved period')
    group=['origin','date','seed']
    if not df.groupby(group).model.nunique().eq(2).all() or not df.groupby(group).y.nunique().eq(1).all():
        raise BlockedError('Model/label pairing mismatch')
    counts=df.groupby(['origin','date','model']).seed.apply(lambda v:tuple(sorted(v)))
    if counts.nunique()!=1:
        raise BlockedError('Every date/model must share the fixed seed roster')
    df['correct']=(df.pred==df.y).astype(float)
    wide=df.pivot(index=group,columns='model',values='correct')
    wide['delta']=wide[model_a]-wide[model_b]
    date=wide.groupby(['origin','date']).delta.mean().to_frame()
    date['y']=df.groupby(['origin','date']).y.first()
    if not df.groupby(['origin','date']).y.nunique().eq(1).all():
        raise BlockedError('Seed label mismatch')
    return date.reset_index().sort_values(['origin','date'])

def moving_block_bootstrap(date_pairs, *, block_length=20, replicates=10000, seed=20261116,
                           metric='balanced_accuracy'):
    """Equal origin weight. Resample blocks within origin; recompute class means.

    CI is percentile. Null-centered bootstrap tail fraction is approximate,
    not an iid/exact McNemar p-value. Short origins fail instead of truncating blocks.
    """
    if block_length not in [20,40,60] or replicates<1 or metric not in ['accuracy','balanced_accuracy']:
        raise BlockedError('Unapproved block/metric/replicate count')
    dates=pd.to_datetime(date_pairs['date'])
    if not dates.between('2010-01-01','2025-12-31').all():
        raise BlockedError('Bootstrap dates outside approved period')
    if date_pairs.duplicated(['origin','date']).any():
        raise BlockedError('Seed pooling/date duplicates prohibited')
    groups=[g.sort_values('date') for _,g in date_pairs.groupby('origin',sort=True)]
    if not groups or any(len(g)<block_length for g in groups):
        raise BlockedError('Origin shorter than requested block')
    def effect(g):
        if metric=='accuracy': return float(g.delta.mean())
        if g.y.nunique()!=2: return np.nan
        return float(g.groupby('y').delta.mean().mean())
    observed=float(np.mean([effect(g) for g in groups]))
    if not np.isfinite(observed):
        raise BlockedError('Balanced accuracy undefined in an origin')
    rng=np.random.default_rng(seed);samples=[];invalid=0
    for _ in range(replicates):
        effects=[]
        for g in groups:
            n=len(g); starts=rng.integers(0,n-block_length+1,size=int(np.ceil(n/block_length)))
            idx=np.concatenate([np.arange(s,s+block_length) for s in starts])[:n]
            effects.append(effect(g.iloc[idx]))
        value=float(np.mean(effects))
        if np.isfinite(value):samples.append(value)
        else:invalid+=1
    if len(samples)<.9*replicates:
        raise BlockedError('More than 10% bootstrap replicates have undefined class denominators')
    vals=np.asarray(samples)
    p=(1+np.sum(np.abs(vals-observed)>=abs(observed)))/(len(vals)+1)
    return {'effect':observed,'ci95':np.quantile(vals,[.025,.975]).tolist(),'p_approx_centered':float(p),
       'market_dates':len(date_pairs),'replicates':replicates,'valid_replicates':len(vals),
       'invalid_replicates':invalid,'block_length':block_length,'origin_weighting':'equal'}

def configured_comparisons(predictions, baseline, compared_models, bootstrap_config):
    """Production invocation: fixed 10,000 draws and all predeclared block lengths.

    Not called in STEP2. Holm is applied across the fixed comparison family
    separately for each prespecified block length; no best-block selection.
    """
    required={'block_lengths':[20,40,60],'replicates':10000,'seed':20261116,'correction':'Holm'}
    if bootstrap_config!=required or len(set(compared_models))!=len(compared_models) or baseline in compared_models:
        raise BlockedError('Unapproved bootstrap config/comparison family')
    rows=[]
    for length in required['block_lengths']:
        family=[]
        for model in compared_models:
            dates=paired_dates(predictions,baseline,model)
            result=moving_block_bootstrap(dates,block_length=length,replicates=10000,seed=required['seed'])
            family.append({'baseline':baseline,'compared_model':model,**result})
        corrected=holm([r['p_approx_centered'] for r in family])
        for row,pvalue in zip(family,corrected):row['p_holm_approx']=float(pvalue)
        rows.extend(family)
    return pd.DataFrame(rows)
