"""Executed in the notebook namespace before any model/test metrics are computed."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('artifacts/sp500_rerun')
OUT.mkdir(parents=True, exist_ok=True)
LOCK = json.loads((OUT / 'protocol_lock.json').read_text())
assert SEEDS == [42, 52, 62, 72, 82]
assert START_DATE == '2010-01-01' and END_DATE == TEST_END == '2025-12-31'
assert TRAIN_END == '2018-12-31' and VAL_END == '2021-12-31'
assert HORIZON == WINDOW_SIZE == 20
assert (HIDDEN_SIZE, NUM_LAYERS, DROPOUT, MAX_LR, EPOCHS, PATIENCE, BATCH_SIZE, FOCAL_GAMMA) == (128, 1, .20, .005, 100, 10, 64, 1.)
assert LOSS_MODES == ['CE', 'MILD_WCE', 'MILD_FOCAL']
assert WF_FOLDS == [('2018-12-31', '2019-01-01', '2019-12-31'),
                    ('2019-12-31', '2020-01-01', '2020-12-31'),
                    ('2020-12-31', '2021-01-01', '2021-12-31')]
np.testing.assert_array_equal(THRESHOLD_GRID, np.round(np.arange(.30, .701, .01), 2))
assert LOCAL_FEATURE_MAP['SP500'] == LOCK['local_features']
assert all(meta['lag'] == 0 for meta in MARKET_CONFIG['SP500']['aux'].values())

exec(compile((OUT / 'acquire_inputs.py').read_text(), 'sp500_rerun-acquisition', 'exec'))
source_metadata = prepare_input_sources(globals())
snapshot = OUT / 'market_input.csv'
manifest_path = OUT / 'data_manifest.json'
if snapshot.exists():
    manifest = json.loads(manifest_path.read_text())
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == manifest['sha256']
else:
    raw = load_market_frame('SP500')
    assert list(raw.columns) == ['Close', 'VIX', 'US10Y', 'DXY']
    assert len(raw) > 3500 and raw.index.is_monotonic_increasing and raw.index.is_unique
    raw.to_csv(snapshot, float_format='%.17g', encoding='utf-8')
    manifest = {'downloaded_at_utc': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                'tickers': {'Close': '^GSPC', 'VIX': '^VIX', 'US10Y': '^TNX', 'DXY': 'DX-Y.NYB'},
                'sources': source_metadata['sources'],
                'availability_sha256': source_metadata['availability_sha256'],
                'rows': len(raw), 'first_date': str(raw.index.min().date()),
                'last_date': str(raw.index.max().date()),
                'policy': 'Frozen once before training; no data refresh or feature tuning based on test results.'}
    manifest_path.write_text(json.dumps(manifest, indent=2))

assert manifest['availability_sha256'] == source_metadata['availability_sha256']
availability = pd.read_csv(OUT / 'availability.csv', index_col=0, parse_dates=True)
availability_columns = [c for c in availability.columns if c.endswith('_available_at_utc')]
for column in availability_columns:
    availability[column] = pd.to_datetime(availability[column], utc=True)

FROZEN_RAW = pd.read_csv(snapshot, index_col=0, parse_dates=True, float_precision='round_trip')
assert list(FROZEN_RAW.columns) == ['Close', 'VIX', 'US10Y', 'DXY']
assert FROZEN_RAW.index.tz is None
assert FROZEN_RAW.index.min() >= pd.Timestamp(START_DATE)
assert FROZEN_RAW.index.max() <= pd.Timestamp(END_DATE)
assert FROZEN_RAW.index.is_unique and FROZEN_RAW.index.is_monotonic_increasing

_original_load_market_frame = load_market_frame


def load_market_frame(market):
    if market == 'SP500':
        return FROZEN_RAW.copy()
    return _original_load_market_frame(market)


audit_df = add_common_features(FROZEN_RAW)
feature_snapshot=OUT/'feature_input.csv'
if feature_snapshot.exists():
    assert hashlib.sha256(feature_snapshot.read_bytes()).hexdigest()==manifest['feature_sha256']
else:
    audit_df.to_csv(feature_snapshot,float_format='%.17g')
    manifest['feature_sha256']=hashlib.sha256(feature_snapshot.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest,indent=2))
audit_features = get_feature_columns(audit_df, 'SP500', 'COMMON_LOCAL')
assert audit_features == COMMON_FEATURES + LOCK['local_features']
assert len(audit_features) == 13
assert 'Target' not in audit_features and 'Forward_Ret20' not in audit_features

# A future-data perturbation must not change any earlier input feature.
cutoff = pd.Timestamp('2022-01-01')
perturbed = FROZEN_RAW.copy()
perturbed.loc[perturbed.index >= cutoff] *= 1.7
earlier = audit_df.index < cutoff
np.testing.assert_allclose(
    audit_df.loc[earlier, audit_features],
    add_common_features(perturbed).loc[earlier, audit_features], equal_nan=True,
)

audit_bundle = prepare_market_walkforward(audit_df, 'SP500', 'COMMON_LOCAL', verbose=False)
split_records = []


def audit_sequences(frame, pack, label):
    X, y, dates, returns = pack
    assert len(X) == len(frame) - WINDOW_SIZE == len(y) == len(dates) > 0
    assert X.shape[1:] == (20, 13) and torch.isfinite(X).all()
    assert dates.equals(pd.DatetimeIndex(frame.index[WINDOW_SIZE:]))
    for pos, target in enumerate(dates, start=WINDOW_SIZE):
        assert frame.index[pos - WINDOW_SIZE:pos].max() < target
    # Verify actual source calendars against a conservative 16:00 New York target cutoff.
    # All feature rows precede the target date; All input source dates precede target date; day-end bounds are conservative.
    available = availability.loc[frame.index, availability_columns]
    assert available.notna().all().all()
    row_times = pd.DatetimeIndex(available.max(axis=1)).as_unit('ns').asi8
    latest_input = np.lib.stride_tricks.sliding_window_view(row_times, WINDOW_SIZE)[:-1].max(axis=1)
    target_cutoffs = (dates.tz_localize('America/New_York') + pd.Timedelta(hours=16)).tz_convert('UTC').as_unit('ns').asi8
    assert (latest_input < target_cutoffs).all(), 'A source may not be available by the conservative U.S. target cutoff'
    split_records.append({'split': label, 'samples': len(y),
                          'first_target': str(dates.min().date()),
                          'last_target': str(dates.max().date())})


for fold in audit_bundle['folds']:
    tr, va = fold['train_df'], fold['val_df']
    assert tr.index.max() < va.index.min()
    np.testing.assert_allclose(fold['scaler'].mean_, tr[audit_features].mean())
    for frame, end in [(tr, fold['train_end']), (va, fold['val_end'])]:
        positions = FROZEN_RAW.index.get_indexer(frame.index)
        assert (positions >= 0).all()
        assert (FROZEN_RAW.index[positions + HORIZON] <= pd.Timestamp(end)).all()
    audit_sequences(tr, fold['train'], f"fold_{fold['fold_id']}_train")
    audit_sequences(va, fold['val'], f"fold_{fold['fold_id']}_val")
np.testing.assert_allclose(audit_bundle['final_scaler'].mean_, audit_bundle['final_train_df'][audit_features].mean())
assert audit_bundle['final_train_df'].index.max() <= pd.Timestamp(VAL_END)
assert audit_bundle['test_df'].index.min() > pd.Timestamp(VAL_END)
for name in ['final_train', 'test']:
    frame = audit_bundle['final_train_df' if name == 'final_train' else 'test_df']
    end = pd.Timestamp(VAL_END if name == 'final_train' else TEST_END)
    positions = FROZEN_RAW.index.get_indexer(frame.index)
    assert (FROZEN_RAW.index[positions + HORIZON] <= end).all()
    audit_sequences(frame, audit_bundle[name], name)

audit = {'status': 'passed', 'features': audit_features, 'raw_rows': len(FROZEN_RAW),
         'auxiliary_row_lag': {'VIX': 0, 'US10Y': 0, 'DXY': 0}, 'effective_last_feature_row': 'strictly before target row t',
         'decision_contract': 'predict close(t+20)/close(t) using only feature rows preceding t; no same-close execution assumption',
         'availability_policy': LOCK['availability_policy'],
         'checks': ['frozen raw input integrity; no target-close imputation', 'all source-availability bounds precede U.S. target cutoffs', 'future perturbation cannot affect past features', 'all input dates strictly before target dates',
                    'labels stay inside each split', 'scalers fitted on training only', '41 fixed validation thresholds'],
         'data_limit': 'Yahoo histories are not point-in-time vintage databases. Audit verifies calendar causality under declared availability bounds, not historical vendor revisions or exact intraday publication timestamps.',
         'splits': split_records}
(OUT / 'leakage_audit.json').write_text(json.dumps(audit, indent=2))
print('PREFLIGHT PASS:', len(FROZEN_RAW), 'daily rows;', len(audit_features), 'features; no test metrics inspected')


def checkpoint_experiment(rows, pred_store, bundle):
    """Persistence side effects only; model fitting and threshold rules untouched."""
    pd.DataFrame(rows).to_csv(OUT/'seed_results.partial.csv',index=False)
    pred_dir=OUT/'predictions';pred_dir.mkdir(exist_ok=True)
    ck_dir=OUT/'checkpoints';ck_dir.mkdir(exist_ok=True)
    tensor_file=OUT/'test_tensors.pt'
    if not tensor_file.exists():
        test_dates=bundle['test'][2]
        y=bundle['test'][1].numpy()
        pd.DataFrame({'Date':test_dates,'Y_true':y,'Always_Up':np.ones_like(y),'Always_Down':np.zeros_like(y),'Persistence':persistence_predictions(test_dates,FROZEN_RAW)}).to_csv(OUT/'baseline_predictions.csv',index=False)
        torch.save({'X':bundle['test'][0].clone(),'y':bundle['test'][1].clone(),'dates':bundle['test'][2].strftime('%Y-%m-%d').tolist(),'forward_returns':bundle['test'][3]},tensor_file)
    thresholds=[]
    for (model,loss,seed),item in pred_store.items():
        stem=f'{model}_{loss}_{seed}'
        thresholds.append({'Model':model,'Loss':loss,'Seed':seed,'Threshold':item['threshold']})
        destination=pred_dir/(stem+'.csv');val_dest=pred_dir/(stem+'.validation.csv');ck=ck_dir/(stem+'.pt')
        if destination.exists() and val_dest.exists() and ck.exists():continue
        assert np.isfinite(item['test_probs']).all() and np.isfinite(item['val_probs']).all()
        pd.DataFrame({'Date':item['dates'],'Y_true':item['y_true'],'Probability':item['test_probs'],'Y_pred':(item['test_probs']>item['threshold']).astype(int),'Threshold':item['threshold'],'Seed':seed,'Model':model,'Loss':loss,'Forward_Return20':item['forward_return']}).to_csv(destination,index=False,float_format='%.17g')
        val_dates=np.concatenate([f['val'][2].values for f in bundle['folds']])
        pd.DataFrame({'Date':pd.to_datetime(val_dates),'Y_true':item['val_y'],'Probability':item['val_probs'],'Y_pred':(item['val_probs']>item['threshold']).astype(int),'Threshold':item['threshold'],'Seed':seed,'Model':model,'Loss':loss}).to_csv(val_dest,index=False,float_format='%.17g')
        scaler=bundle['final_scaler']
        torch.save({'state_dict':item['state_dict'],'Model':model,'Loss':loss,'Seed':seed,'Threshold':item['threshold'],'input_size':item['input_size'],'feature_names':audit_features,'final_epochs':60,'scaler':{'mean':scaler.mean_,'scale':scaler.scale_,'var':scaler.var_,'n_samples_seen':int(scaler.n_samples_seen_)},'protocol_sha256':hashlib.sha256((OUT/'protocol_lock.json').read_bytes()).hexdigest(),'input_sha256':manifest['sha256']},ck)
    pd.DataFrame(thresholds,columns=['Model','Loss','Seed','Threshold']).to_csv(OUT/'selected_thresholds.csv',index=False,float_format='%.17g')
    (OUT/'progress.json').write_text(json.dumps({'status':'running','completed_runs':len(pred_store),'expected_runs':45,'updated_at_utc':datetime.now(timezone.utc).isoformat()},indent=2))
