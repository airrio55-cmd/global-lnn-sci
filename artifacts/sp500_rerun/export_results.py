"""Executed after the full notebook experiment; never tunes parameters."""
from itertools import product

assert RUN_MARKETS == ['SP500'] and RUN_FEATURE_SETS == ['COMMON_LOCAL']
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

store = all_prediction_store[('SP500', 'COMMON_LOCAL')]
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
lines = ['# SP500 COMMON_LOCAL + walk-forward results', '',
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
          'Original SP500 v1.4 features: common five + VIX level/1d/5d change, US10Y level/1d/5d difference, DXY 1d/5d log return. Source-row lag zero; X[i-20:i] excludes target date. No same-day future U.S. close enters an input window.', '',
          'Inputs downloaded once and frozen as source histories, market_input.csv and feature_input.csv with checksums before training. Scalers fitted train-only; split horizon containment, source availability and future perturbation checks passed.', '',
          'Every final model state_dict and scaler definition is saved with test tensors, validation probabilities, original validation-only thresholds and test predictions. Archived results are compared only after completion; no attempts are made to match archived values.', '',
          'Yahoo histories are not point-in-time vintages. The availability audit uses conservative source-date New York day-end bounds and does not certify absence of revisions.', '',
          'Δ BA describes performance differences, not statistical significance. '
          'The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.', '',
          '## Files', '',
          '- SCI_v1_4_WALKFORWARD_SP500.completed.ipynb: fully executed notebook',
          '- seed_results.csv: 45 learned rows and 3 baseline rows',
          '- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries',
          '- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines',
          '- predictions/: full-precision test and validation probabilities for every run',
          '- market_input.csv / data_manifest.json: frozen input and checksum',
          '- sources/ / sources_manifest.json / availability.csv: source histories, provenance, lags and availability bounds',
          '- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence', '']
(OUT / 'results_report.md').write_text('\n'.join(lines), encoding='utf-8')
(OUT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
print('EXPORT PASS: all 45 runs, 3 baselines and validation-only thresholds verified')

archived = pd.read_csv('artifacts/seed_results.csv')
archived = archived[archived.Seed.astype(str) != 'BASELINE'].copy()
archived.Seed=archived.Seed.astype(int)
paired=learned.merge(archived,on=['Market','Feature_Set','Model','Loss','Seed'],suffixes=('_rerun','_archived'),validate='one_to_one')
for metric in metrics:
    paired['Delta_'+metric]=paired[metric+'_rerun']-paired[metric+'_archived']
paired.to_csv(OUT/'archived_comparison.csv',index=False,float_format='%.17g')
with (OUT/'results_report.md').open('a') as report:
    report.write('\n## Archived comparison\n\nSee archived_comparison.csv for all 45 paired run differences, including thresholds. Differences are reported unchanged. This is a new reproducible candidate, not restoration of unsaved archived predictions.\n')
(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
