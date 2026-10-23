# EUROSTOXX50 COMMON_LOCAL + walk-forward results

Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.

Persistence Test BA: 0.446689; Macro F1: 0.446756.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| LNN | MILD_FOCAL | 0.508536 ± 0.007319 | 0.421767 ± 0.042050 | +0.061847 | 5/5 |
| LNN | MILD_WCE | 0.507359 ± 0.010803 | 0.407582 ± 0.041469 | +0.060670 | 5/5 |
| LSTM | CE | 0.498413 ± 0.024213 | 0.432560 ± 0.039000 | +0.051723 | 5/5 |
| LSTM | MILD_WCE | 0.498075 ± 0.017225 | 0.413473 ± 0.013484 | +0.051386 | 5/5 |
| LNN | CE | 0.497192 ± 0.007584 | 0.375564 ± 0.016877 | +0.050502 | 5/5 |
| Transformer | CE | 0.494875 ± 0.040944 | 0.410330 ± 0.044306 | +0.048186 | 4/5 |
| LSTM | MILD_FOCAL | 0.488347 ± 0.013389 | 0.403787 ± 0.011654 | +0.041657 | 5/5 |
| Transformer | MILD_WCE | 0.465558 ± 0.028935 | 0.347753 ± 0.041381 | +0.018869 | 3/5 |
| Transformer | MILD_FOCAL | 0.462307 ± 0.032252 | 0.338403 ± 0.026934 | +0.015617 | 3/5 |

## Protocol and changes

2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.

Common inputs: Log_Ret, Vol20, Momentum20, Disparity20, RSI14. Local inputs fixed before training: EUR_USD, VIX, lagged SP500, DE10Y, DE10Y_Change1, DE10Y_Change5. DE10Y is FRED/OECD IRLTLT01DEM156N, read directly from data/GERMANY_10Y_FRED_2010_2025.csv (no FRED or MOF connection). It is monthly; changes are percentage points of the lagged daily step series.

The original S&P500/NASDAQ100 notebooks and results remain unchanged. Training/model/loss/split functions retain the original protocol; only market data, local feature selection, causal audits, checkpoints and reporting are extended. No test-driven parameter or feature changes were made.

## Availability / leakage audit

EURUSD, VIX and S&P500 use the declared conservative alignment: one source-observation lag, European reindex and forward-fill only. U.S. input availability is conservatively bounded by source-date New York day-end. Exactly one monthly-period lag is applied: month M is eligible from the first day of M+1 at 00:00 Europe/Berlin local time, then forward-filled onto European trading dates only. January 2010 is first usable in February 2010, never in January. The CSV contains no 2009 warmup; initial missing rates stay missing and the inherited dropna/rolling rules apply. The four Yahoo inputs were frozen before training, without refresh based on test metrics. DE10Y_Change1/5 remain trailing 1/5-trading-day differences of this lagged step series, mostly zero between monthly updates.

X[i-20:i] excludes the target row. All input availability bounds were checked against a conservative 17:00 Europe/Berlin local time target cutoff, earlier than the regular 17:30 European cash close; half-days also use only prior source rows. Split horizon containment, train-only scalers, causal invariance under future perturbation, and validation-only threshold selection were checked. See availability.csv, sources_manifest.json and leakage_audit.json.

Yahoo/FRED/OECD historical downloads are not point-in-time vintages and lack complete intraday publication histories. The user-specified one-month lag is an observation-period convention, not a reconstructed publication calendar. The audit proves compliance with the lag and prevents same-month/initial backfilling; it does not certify actual historical release times or the absence of vendor revisions.

Δ BA describes performance differences, not statistical significance. The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.

## Files

- SCI_v1_4_WALKFORWARD_EUROSTOXX50.completed.ipynb: fully executed notebook
- seed_results.csv: 45 learned rows and 3 baseline rows
- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries
- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines
- predictions/: full-precision test and validation probabilities for every run
- market_input.csv / data_manifest.json: frozen input and checksum
- sources/ / sources_manifest.json / availability.csv: source histories, provenance, lags and availability bounds
- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence
