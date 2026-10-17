"""Executed in the notebook namespace before any model/test metrics are computed."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('artifacts/nasdaq100')
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
assert LOCAL_FEATURE_MAP['NASDAQ100'] == LOCK['local_features']
assert all(meta['lag'] == 0 for meta in MARKET_CONFIG['NASDAQ100']['aux'].values())

snapshot = OUT / 'market_input.csv'
manifest_path = OUT / 'data_manifest.json'
if snapshot.exists():
    manifest = json.loads(manifest_path.read_text())
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == manifest['sha256']
else:
    raw = load_market_frame('NASDAQ100')
    assert list(raw.columns) == ['Close', 'VXN', 'SOX', 'US10Y', 'DXY']
    assert len(raw) > 3500 and raw.index.is_monotonic_increasing and raw.index.is_unique
    raw.to_csv(snapshot, float_format='%.17g', encoding='utf-8')
    manifest = {'downloaded_at_utc': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                'tickers': {'Close': '^NDX', 'VXN': '^VXN', 'SOX': '^SOX', 'US10Y': '^TNX', 'DXY': 'DX-Y.NYB'},
                'rows': len(raw), 'first_date': str(raw.index.min().date()),
                'last_date': str(raw.index.max().date()),
                'policy': 'Frozen once before training; no data refresh or feature tuning based on test results.'}
    manifest_path.write_text(json.dumps(manifest, indent=2))

FROZEN_RAW = pd.read_csv(snapshot, index_col=0, parse_dates=True, float_precision='round_trip')
assert list(FROZEN_RAW.columns) == ['Close', 'VXN', 'SOX', 'US10Y', 'DXY']
assert FROZEN_RAW.index.tz is None
assert FROZEN_RAW.index.min() >= pd.Timestamp(START_DATE)
assert FROZEN_RAW.index.max() <= pd.Timestamp(END_DATE)
assert FROZEN_RAW.index.is_unique and FROZEN_RAW.index.is_monotonic_increasing

_original_load_market_frame = load_market_frame


def load_market_frame(market):
    if market == 'NASDAQ100':
        return FROZEN_RAW.copy()
    return _original_load_market_frame(market)


audit_df = add_common_features(FROZEN_RAW)
audit_features = get_feature_columns(audit_df, 'NASDAQ100', 'COMMON_LOCAL')
assert audit_features == COMMON_FEATURES + LOCK['local_features']
assert len(audit_features) == 10
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

audit_bundle = prepare_market_walkforward(audit_df, 'NASDAQ100', 'COMMON_LOCAL', verbose=False)
split_records = []


def audit_sequences(frame, pack, label):
    X, y, dates, returns = pack
    assert len(X) == len(frame) - WINDOW_SIZE == len(y) == len(dates) > 0
    assert X.shape[1:] == (20, 10) and torch.isfinite(X).all()
    assert dates.equals(pd.DatetimeIndex(frame.index[WINDOW_SIZE:]))
    for pos, target in enumerate(dates, start=WINDOW_SIZE):
        assert frame.index[pos - WINDOW_SIZE:pos].max() < target
    # Feature t-1 can be finalized later than U.S. equity close on that date;
    # it is still prior-day information for the target interval starting at close(t).
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
         'auxiliary_row_lag': 0, 'effective_last_feature_row': 'strictly before target row t',
         'decision_contract': 'predict close(t+20)/close(t) using only feature rows preceding t; no same-close execution assumption',
         'checks': ['future perturbation cannot affect past features', 'all input dates strictly before target dates',
                    'labels stay inside each split', 'scalers fitted on training only', '41 fixed validation thresholds'],
         'data_limit': 'Yahoo daily history is not a point-in-time vintage database; audit addresses code/calendar causality, not historical vendor revisions.',
         'splits': split_records}
(OUT / 'leakage_audit.json').write_text(json.dumps(audit, indent=2))
print('PREFLIGHT PASS:', len(FROZEN_RAW), 'daily rows;', len(audit_features), 'features; no test metrics inspected')


def checkpoint_experiment(rows, pred_store, bundle):
    """Reporting side effects only; no changes to RNG, model, or selection rules."""
    pd.DataFrame(rows).to_csv(OUT / 'seed_results.partial.csv', index=False, encoding='utf-8-sig')
    pred_dir = OUT / 'predictions'
    pred_dir.mkdir(exist_ok=True)
    for (model, loss, seed), item in pred_store.items():
        dest = pred_dir / f'{model}_{loss}_{seed}.csv'
        validation_dest = pred_dir / f'{model}_{loss}_{seed}.validation.csv'
        assert np.isfinite(item['test_probs']).all() and np.isfinite(item['val_probs']).all()
        assert ((item['test_probs'] >= 0) & (item['test_probs'] <= 1)).all()
        if dest.exists() and validation_dest.exists():
            continue
        pd.DataFrame({'Date': item['dates'], 'Y_true': item['y_true'],
                      'Probability': item['test_probs'], 'Threshold': item['threshold'],
                      'Forward_Return20': item['forward_return']}).to_csv(dest, index=False, float_format='%.17g')
        val_dates = np.concatenate([fold['val'][2].values for fold in bundle['folds']])
        pd.DataFrame({'Date': pd.to_datetime(val_dates), 'Y_true': item['val_y'],
                      'Probability': item['val_probs']}).to_csv(
                          validation_dest, index=False, float_format='%.17g')
    progress = {'status': 'running', 'completed_runs': len(pred_store), 'expected_runs': 45,
                'updated_at_utc': datetime.now(timezone.utc).isoformat()}
    (OUT / 'progress.json').write_text(json.dumps(progress, indent=2))
