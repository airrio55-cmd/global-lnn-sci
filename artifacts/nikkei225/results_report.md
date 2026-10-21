# NIKKEI225 COMMON_LOCAL + walk-forward results

Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.

Persistence Test BA: 0.451269; Macro F1: 0.451444.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| LNN | CE | 0.515214 ± 0.011906 | 0.410788 ± 0.060436 | +0.063946 | 5/5 |
| Transformer | CE | 0.511339 ± 0.018762 | 0.322929 ± 0.039672 | +0.060070 | 5/5 |
| Transformer | MILD_FOCAL | 0.511184 ± 0.008129 | 0.355996 ± 0.045944 | +0.059915 | 5/5 |
| LNN | MILD_WCE | 0.511176 ± 0.008222 | 0.385225 ± 0.032188 | +0.059907 | 5/5 |
| LNN | MILD_FOCAL | 0.509870 ± 0.027232 | 0.395627 ± 0.062773 | +0.058601 | 5/5 |
| Transformer | MILD_WCE | 0.509097 ± 0.009147 | 0.299169 ± 0.020160 | +0.057828 | 5/5 |
| LSTM | CE | 0.496176 ± 0.014383 | 0.392393 ± 0.038934 | +0.044908 | 5/5 |
| LSTM | MILD_FOCAL | 0.495879 ± 0.012670 | 0.384064 ± 0.019614 | +0.044610 | 5/5 |
| LSTM | MILD_WCE | 0.479288 ± 0.031695 | 0.372935 ± 0.023504 | +0.028019 | 4/5 |

## Protocol and changes

2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.

Common inputs: Log_Ret, Vol20, Momentum20, Disparity20, RSI14. Local inputs fixed before training: USD_JPY, VIX, lagged SP500, JP10Y, JP10Y_Change1, JP10Y_Change5. JP10Y is FRED/OECD IRLTLT01JPM156N, read directly from data/JAPAN_10Y_FRED_2010_2025.csv (no FRED or MOF connection). It is monthly; changes are percentage points of the lagged daily step series.

The original S&P500/NASDAQ100 notebooks and results remain unchanged. Training/model/loss/split functions retain the original protocol; only market data, local feature selection, causal audits, checkpoints and reporting are extended. No test-driven parameter or feature changes were made.

## Availability / leakage audit

USDJPY, VIX and S&P500 keep the original Nikkei configuration: one source-observation lag, Tokyo reindex and forward-fill only. U.S. input availability is conservatively bounded by source-date New York day-end. Exactly one monthly-period lag is applied: month M is eligible from the first day of M+1 at 00:00 JST, then forward-filled onto Tokyo trading dates only. January 2010 is first usable in February 2010, never in January. The CSV contains no 2009 warmup; initial missing rates stay missing and the inherited dropna/rolling rules apply. The four original Yahoo inputs are read from unchanged frozen source files, not refreshed. JP10Y_Change1/5 remain trailing 1/5-trading-day differences of this lagged step series, mostly zero between monthly updates.

X[i-20:i] excludes the target row. All input availability bounds were checked against a conservative 15:00 JST target cutoff, also safe relative to the later 15:30 Tokyo close introduced in November 2024. Split horizon containment, train-only scalers, causal invariance under future perturbation, and validation-only threshold selection were checked. See availability.csv, sources_manifest.json and leakage_audit.json.

Yahoo/FRED/OECD historical downloads are not point-in-time vintages and lack complete intraday publication histories. The user-specified one-month lag is an observation-period convention, not a reconstructed publication calendar. The audit proves compliance with the lag and prevents same-month/initial backfilling; it does not certify actual historical release times or the absence of vendor revisions.

Δ BA describes performance differences, not statistical significance. The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.

## Files

- SCI_v1_4_WALKFORWARD_NIKKEI225.completed.ipynb: fully executed notebook
- seed_results.csv: 45 learned rows and 3 baseline rows
- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries
- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines
- predictions/: full-precision test and validation probabilities for every run
- market_input.csv / data_manifest.json: frozen input and checksum
- sources/ / sources_manifest.json / availability.csv: source histories, provenance, lags and availability bounds
- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence
