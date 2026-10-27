# SP500 COMMON_LOCAL + walk-forward results

Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.

Persistence Test BA: 0.515074; Macro F1: 0.514657.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| LNN | MILD_WCE | 0.450897 ± 0.021032 | 0.406120 ± 0.039372 | -0.064177 | 0/5 |
| LSTM | MILD_WCE | 0.449641 ± 0.022996 | 0.443536 ± 0.026156 | -0.065433 | 0/5 |
| LNN | CE | 0.448909 ± 0.018968 | 0.413487 ± 0.037477 | -0.066165 | 0/5 |
| LSTM | CE | 0.445902 ± 0.017003 | 0.431979 ± 0.022227 | -0.069172 | 0/5 |
| Transformer | CE | 0.440475 ± 0.035221 | 0.408488 ± 0.059960 | -0.074599 | 0/5 |
| LSTM | MILD_FOCAL | 0.440316 ± 0.015255 | 0.430111 ± 0.016047 | -0.074758 | 0/5 |
| Transformer | MILD_FOCAL | 0.439789 ± 0.034921 | 0.376967 ± 0.088273 | -0.075286 | 0/5 |
| LNN | MILD_FOCAL | 0.438382 ± 0.019559 | 0.404379 ± 0.024849 | -0.076692 | 0/5 |
| Transformer | MILD_WCE | 0.431020 ± 0.027688 | 0.402555 ± 0.043430 | -0.084055 | 0/5 |

## Protocol and changes

2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.

Original SP500 v1.4 features: common five + VIX level/1d/5d change, US10Y level/1d/5d difference, DXY 1d/5d log return. Source-row lag zero; X[i-20:i] excludes target date. No same-day future U.S. close enters an input window.

Inputs downloaded once and frozen as source histories, market_input.csv and feature_input.csv with checksums before training. Scalers fitted train-only; split horizon containment, source availability and future perturbation checks passed.

Every final model state_dict and scaler definition is saved with test tensors, validation probabilities, original validation-only thresholds and test predictions. Archived results are compared only after completion; no attempts are made to match archived values.

Yahoo histories are not point-in-time vintages. The availability audit uses conservative source-date New York day-end bounds and does not certify absence of revisions.

Δ BA describes performance differences, not statistical significance. The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.

## Files

- SCI_v1_4_WALKFORWARD_SP500.completed.ipynb: fully executed notebook
- seed_results.csv: 45 learned rows and 3 baseline rows
- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries
- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines
- predictions/: full-precision test and validation probabilities for every run
- market_input.csv / data_manifest.json: frozen input and checksum
- sources/ / sources_manifest.json / availability.csv: source histories, provenance, lags and availability bounds
- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence

## Archived comparison

See archived_comparison.csv for all 45 paired run differences, including thresholds. Differences are reported unchanged. This is a new reproducible candidate, not restoration of unsaved archived predictions.
