# KOSPI200 COMMON_LOCAL + walk-forward results

Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.

Persistence Test BA: 0.503252; Macro F1: 0.503158.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| LSTM | CE | 0.526016 ± 0.026176 | 0.437564 ± 0.045630 | +0.022763 | 5/5 |
| Transformer | MILD_FOCAL | 0.515713 ± 0.025558 | 0.439666 ± 0.048950 | +0.012461 | 4/5 |
| LSTM | MILD_FOCAL | 0.515688 ± 0.015674 | 0.417667 ± 0.026249 | +0.012436 | 4/5 |
| LSTM | MILD_WCE | 0.512543 ± 0.019563 | 0.420879 ± 0.043372 | +0.009291 | 4/5 |
| LNN | MILD_FOCAL | 0.501298 ± 0.018205 | 0.412137 ± 0.035504 | -0.001954 | 3/5 |
| Transformer | CE | 0.498872 ± 0.021487 | 0.423441 ± 0.069780 | -0.004380 | 2/5 |
| LNN | CE | 0.495425 ± 0.021613 | 0.425862 ± 0.040540 | -0.007827 | 2/5 |
| Transformer | MILD_WCE | 0.492863 ± 0.050297 | 0.445545 ± 0.084415 | -0.010390 | 2/5 |
| LNN | MILD_WCE | 0.474058 ± 0.034460 | 0.412682 ± 0.037110 | -0.029194 | 1/5 |

## Protocol and changes

2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.

Common: Log_Ret, Vol20, Momentum20, Disparity20, RSI14. Local: USD_KRW, SOX, VIX; unchanged original KOSPI200 config.

## Data and calendar

Primary source: user-provided KOSPI200 original research data, KOSPI200_daily_2010_2025.csv, Date and 종가 columns. Original file unchanged; 2026 rows excluded. Actual 3894 observations in 2010–2025 define the empirical trading-day calendar. Horizon and lookback count observed rows.

XKRX expected rows 3939; observed 3894; difference 45. This calendar implementation discrepancy is not confirmed as missing KRX observations. User reports the current pykrx index endpoint returned empty data; the cloud attempt was separately blocked by proxy 403. No authoritative KRX cross-check is claimed. No target dates or prices are inserted, forward-filled or synthesized. Comparability is limited by this empirical calendar convention.

## Leakage audit

USD_KRW (KRW=X), SOX (^SOX), VIX (^VIX): one source-observation lag, then reindex/forward-fill onto observed target dates, never initial backfill. Source availability bounded conservatively at source-date New York day-end, including daily FX whose exact vendor publication history is unavailable. Target Close availability bounded at Seoul day-end. X[i-20:i] excludes target row; every window availability bound precedes conservative 15:00 KST target cutoff.

Future perturbation invariance, split horizon containment and train-only scalers were checked. Thresholds are selected only from validation predictions. Source hashes and original core code hashes are locked. No test-driven feature or parameter changes.

Historical data are not point-in-time vintages; exact intraday releases and vendor revisions are not certified. Calendar integrity is empirical, not a certification of complete exchange coverage. See calendar_audit.json, data_manifest.json and leakage_audit.json.

Δ BA describes performance differences, not statistical significance. The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.

## Files

- SCI_v1_4_WALKFORWARD_KOSPI200.completed.ipynb: fully executed notebook
- seed_results.csv: 45 learned rows and 3 baseline rows
- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries
- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines
- predictions/: full-precision test and validation probabilities for every run
- market_input.csv / data_manifest.json: frozen input and checksum
- sources/ / sources_manifest.json / availability.csv: source histories, provenance, lags and availability bounds
- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence
