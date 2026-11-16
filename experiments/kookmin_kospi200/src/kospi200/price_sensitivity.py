"""Data-only price scenarios. No source selection, model fitting or predictions."""
import numpy as np
import pandas as pd
from .data import BlockedError
from .reconciliation import build_labels_features, validate_prices
from .folds import rolling_origins, window_dates, train_only_scaler
from .manual_evaluation import freeze_manual_reference, assign_manual_regimes

FEATURE_ORDER=['Log_Ret','Disparity']
CONFLICT_DATES=pd.DatetimeIndex(['2021-04-23','2021-05-06'])


def align_candidates(a, b, calendar):
    x,_=validate_prices(a);y,_=validate_prices(b);sessions=calendar.checked()
    if not pd.DatetimeIndex(x.Date).equals(sessions) or not pd.DatetimeIndex(y.Date).equals(sessions):
        raise BlockedError('Both candidates must cover the identical official sessions')
    return x,y


def feature_difference(a,b):
    result={}
    for name in a:
        valid=a[name].notna()&b[name].notna();delta=(b.loc[valid,name]-a.loc[valid,name]).abs()
        result[name]={'finite_pairs':int(valid.sum()),'missing_mask_differences':int(a[name].isna().ne(b[name].isna()).sum()),
                      'exact_differences':int(delta.gt(0).sum()),
                      'over_1e_minus12':int(delta.gt(1e-12).sum()),'over_1e_minus6':int(delta.gt(1e-6).sum()),
                      'over_1e_minus3':int(delta.gt(1e-3).sum()),
                      'max_absolute_difference':float(delta.max()),'mean_absolute_difference':float(delta.mean())}
    return result


def f1_structure(prices,calendar):
    labels,features,common_window=build_labels_features(prices,calendar)
    f1_window=features[FEATURE_ORDER].notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20)
    common_manifest,common_selected=rolling_origins(labels,calendar,common_window)
    f1_manifest,f1_selected=rolling_origins(labels,calendar,f1_window)
    return {'labels':labels,'features':features,'common_window':common_window,'f1_window':f1_window,
            'common_manifest':common_manifest,'common_selected':common_selected,'f1_manifest':f1_manifest,'f1_selected':f1_selected}


def compare_candidates(a,b,calendar):
    a,b=align_candidates(a,b,calendar);sa=f1_structure(a,calendar);sb=f1_structure(b,calendar)
    la,lb=sa['labels'],sb['labels'];known=la.Target.notna()&lb.Target.notna()
    changed=la.Target[known].ne(lb.Target[known]);enddiff=(la.label_end.notna()|lb.label_end.notna())&la.label_end.ne(lb.label_end)
    origins=[];thresholds=[];scalers=[]
    for origin in sa['common_selected']:
        va=sa['common_manifest'].query('origin==@origin and partition=="validation"').boundary_start.iloc[0]
        train_a=sa['common_selected'][origin]['train'];train_b=sb['common_selected'][origin]['train']
        ra=freeze_manual_reference(sa['features'].Vol_Regime,train_a,validation_start=va,partition='train')
        rb=freeze_manual_reference(sb['features'].Vol_Regime,train_b,validation_start=va,partition='train')
        record={'origin':origin,'reference':'STEP27 retained Train base dates; common local feature-window mask',
                'train_rows_A':len(train_a),'train_rows_B':len(train_b),'low_A':ra['low'],'low_B':rb['low'],
                'high_A':ra['high'],'high_B':rb['high'],'low_delta':rb['low']-ra['low'],'high_delta':rb['high']-ra['high'],
                'validation_test_refit':False}
        for partition in ['train','validation','test']:
            da=sa['common_selected'][origin][partition];db=sb['common_selected'][origin][partition]
            row={'origin':origin,'partition':partition,'common_regime_samples_A':len(da),'common_regime_samples_B':len(db),
                 'common_date_membership_changes':len(da.symmetric_difference(db)),
                 'F1_input_only_samples_A':len(sa['f1_selected'][origin][partition]),
                 'F1_input_only_samples_B':len(sb['f1_selected'][origin][partition]),
                 'F1_date_membership_changes':len(sa['f1_selected'][origin][partition].symmetric_difference(sb['f1_selected'][origin][partition]))}
            origins.append(row)
            common=da.intersection(db)
            ta=assign_manual_regimes(sa['features'].loc[common,'Vol_Regime'],ra)
            tb=assign_manual_regimes(sb['features'].loc[common,'Vol_Regime'],rb)
            record[partition+'_manual_membership_changes']=int(ta.ne(tb).sum())
        thresholds.append(record)
        # Fit diagnostic StandardScaler on the union of retained Train input windows ONLY.
        ws=window_dates(calendar.sessions,train_a,window=20,include_t=True)
        fit_dates=pd.DatetimeIndex(sorted({d for dates in ws.values() for d in dates}))
        _,lineage=train_only_scaler(sa['features'][FEATURE_ORDER],fit_dates,va)
        scalers.append({'origin':origin,**lineage,'fit_policy':'union of retained Train input-window dates; no validation/test',
                        'fit_max_before_validation':bool(fit_dates.max()<pd.Timestamp(va))})
    return {'sessions':len(a),'known_labels_A':int(la.Target.notna().sum()),'known_labels_B':int(lb.Target.notna().sum()),
            'unknown_labels_A':int(la.Target.isna().sum()),'unknown_labels_B':int(lb.Target.isna().sum()),
            'known_label_differences':int(changed.sum()),'down_to_up':int(((la.Target[known]==0)&(lb.Target[known]==1)).sum()),
            'up_to_down':int(((la.Target[known]==1)&(lb.Target[known]==0)).sum()),'label_end_differences':int(enddiff.sum()),
            'features':feature_difference(sa['features'],sb['features']),'origins':origins,'manual_thresholds':thresholds,
            'Train_only_scaler_diagnostics':scalers,'final_source_selected':None,'model_performance_estimated':False,
            '2026_prices_used':0},sa,sb
