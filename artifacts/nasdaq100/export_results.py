"""Executed after the full notebook experiment; never tunes parameters."""
from itertools import product

assert RUN_MARKETS == ['NASDAQ100'] and RUN_FEATURE_SETS == ['COMMON_LOCAL']
assert RUN_MODELS == ['LNN', 'LSTM', 'Transformer']
assert RUN_LOSS_MODES == ['CE', 'MILD_WCE', 'MILD_FOCAL']
learned = global_results[global_results['Seed'].astype(str) != 'BASELINE'].copy()
baseline = global_results[global_results['Seed'].astype(str) == 'BASELINE'].copy()
keys = ['Market', 'Feature_Set', 'Model', 'Loss', 'Seed']
expected = set(product(RUN_MARKETS, RUN_FEATURE_SETS, RUN_MODELS, RUN_LOSS_MODES, SEEDS))
assert len(learned) == 45 and set(learned[keys].itertuples(index=False, name=None)) == expected
assert len(baseline) == 3 and set(baseline['Model']) == {'Always-Up', 'Always-Down', 'Persistence'}
metrics = ['Accuracy', 'Balanced_Accuracy', 'Macro_F1', 'F1', 'Recall', 'Precision',
           'Pred_Pos_Rate', 'WF_Val_BA', 'WF_Val_Macro_F1', 'Threshold']
assert np.isfinite(learned[metrics].to_numpy(dtype=float)).all()

store = all_prediction_store[('NASDAQ100', 'COMMON_LOCAL')]
assert len(store) == 45
for (model, loss, seed), entry in store.items():
    # Recompute thresholds from validation labels/probabilities only.
    threshold, _ = select_validation_threshold(entry['val_y'], entry['val_probs'], THRESHOLD_GRID)
    assert threshold == entry['threshold']
    recalculated = calculate_metrics(entry['y_true'], probs=entry['test_probs'], threshold=threshold)
    row = learned[(learned.Model == model) & (learned.Loss == loss) & (learned.Seed == seed)].iloc[0]
    for key, value in recalculated.items():
        assert np.isclose(row[key], value)

summary = learned.groupby(['Market', 'Feature_Set', 'Model', 'Loss'])[metrics].agg(['mean', 'std'])
summary.columns = ['_'.join(c) for c in summary.columns]
summary = summary.reset_index()
pers = baseline[baseline.Model == 'Persistence'][['Market', 'Feature_Set', 'Accuracy', 'Balanced_Accuracy', 'Macro_F1']]
pers = pers.rename(columns={m: 'Persistence_' + m for m in ['Accuracy', 'Balanced_Accuracy', 'Macro_F1']})
comparison = learned.merge(pers, on=['Market', 'Feature_Set'], validate='many_to_one')
summary = summary.merge(pers, on=['Market', 'Feature_Set'], validate='many_to_one')
for metric in ['Accuracy', 'Balanced_Accuracy', 'Macro_F1']:
    comparison['Delta_' + metric] = comparison[metric] - comparison['Persistence_' + metric]
    summary['Delta_' + metric + '_mean'] = summary[metric + '_mean'] - summary['Persistence_' + metric]
counts = comparison.assign(Beats_Persistence=comparison.Delta_Balanced_Accuracy > 0).groupby(
    ['Market', 'Feature_Set', 'Model', 'Loss']).Beats_Persistence.sum().reset_index(name='Seeds_Beating_Persistence')
summary = summary.merge(counts, on=['Market', 'Feature_Set', 'Model', 'Loss'], validate='one_to_one')

global_results.to_csv(OUT / 'seed_results.csv', index=False, encoding='utf-8-sig')
summary.to_csv(OUT / 'summary.csv', index=False, encoding='utf-8-sig')
global_summary.to_csv(OUT / 'formatted_summary.csv', index=False, encoding='utf-8-sig')
comparison.to_csv(OUT / 'persistence_comparison.csv', index=False, encoding='utf-8-sig')
baseline.to_csv(OUT / 'baselines.csv', index=False, encoding='utf-8-sig')
display(summary)
display(baseline)

baseline_row = baseline[baseline.Model == 'Persistence'].iloc[0]
lines = ['# NASDAQ100 COMMON_LOCAL + walk-forward results', '',
         'Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.', '',
         f'Persistence Test BA: {baseline_row.Balanced_Accuracy:.6f}; Macro F1: {baseline_row.Macro_F1:.6f}.', '',
         '| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |',
         '|---|---|---:|---:|---:|---:|']
for r in summary.sort_values('Balanced_Accuracy_mean', ascending=False).itertuples():
    lines.append(f'| {r.Model} | {r.Loss} | {r.Balanced_Accuracy_mean:.6f} ± {r.Balanced_Accuracy_std:.6f} '
                 f'| {r.Macro_F1_mean:.6f} ± {r.Macro_F1_std:.6f} | {r.Delta_Balanced_Accuracy_mean:+.6f} '
                 f'| {int(r.Seeds_Beating_Persistence)}/5 |')
lines += ['', '## Protocol and changes', '',
          '2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; '
          'CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. '
          'Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.', '',
          'Common inputs: Log_Ret, Vol20, Momentum20, Disparity20, RSI14. '
          'Local inputs fixed before training: VXN, SOX, US10Y, DXY_LogRet1, DXY_LogRet5. '
          'DXY transformations reuse the original 1-day/5-day logarithmic return definitions. '
          'Other computed auxiliary transformations are not selected as inputs.', '',
          'The original S&P500 notebook and results remain unchanged. The NASDAQ100 copy adds the DXY ticker '
          'and its two selected inputs, switches the requested market/output directory, freezes the data snapshot, '
          'and adds causal audits, per-run checkpoints and reporting. Training, model, loss and split functions are unchanged '
          'apart from reporting-only checkpoint calls. No test-driven parameter/feature changes or model selection were made.', '',
          '## Availability / leakage audit', '',
          'Daily auxiliary rows keep the existing U.S. lag=0 alignment. Sequence X[i-20:i] excludes row i. '
          'Thus every input precedes the target date; the target return starts at close(i), and there is no assumption '
          'that VXN or DXY finalizes at the same instant as the Nasdaq cash close. Trailing returns and ffill only are used. '
          'Assertions checked date ordering, horizon containment, train-only scalers and causal invariance under future-data changes. '
          'Thresholds were recomputed exclusively from validation probabilities and verified against the fixed test thresholds. '
          'See leakage_audit.json and data_manifest.json. Yahoo daily history is not a point-in-time vintage database, '
          'so these checks do not certify the absence of vendor historical revisions.', '',
          'Δ BA describes performance differences, not statistical significance. '
          'The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.', '',
          '## Files', '',
          '- SCI_v1_4_WALKFORWARD_NASDAQ100.completed.ipynb: fully executed notebook',
          '- seed_results.csv: 45 learned rows and 3 baseline rows',
          '- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries',
          '- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines',
          '- predictions/: full-precision test and validation probabilities for every run',
          '- market_input.csv / data_manifest.json: frozen raw input and checksum',
          '- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence', '']
(OUT / 'results_report.md').write_text('\n'.join(lines), encoding='utf-8')
(OUT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
print('EXPORT PASS: all 45 runs, 3 baselines and validation-only thresholds verified')
