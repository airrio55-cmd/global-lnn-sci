# NASDAQ100 COMMON_LOCAL + walk-forward results

Completed: 45 learned runs (3 models × 3 losses × 5 seeds) and 3 baselines.

Persistence Test BA: 0.532517; Macro F1: 0.531938.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| Transformer | CE | 0.502597 ± 0.035163 | 0.409059 ± 0.136177 | -0.029921 | 1/5 |
| Transformer | MILD_WCE | 0.498142 ± 0.045120 | 0.367986 ± 0.142323 | -0.034375 | 1/5 |
| Transformer | MILD_FOCAL | 0.485549 ± 0.025305 | 0.302006 ± 0.092326 | -0.046969 | 0/5 |
| LNN | CE | 0.483538 ± 0.028411 | 0.328637 ± 0.078708 | -0.048979 | 0/5 |
| LSTM | MILD_FOCAL | 0.477752 ± 0.025731 | 0.342589 ± 0.054181 | -0.054766 | 0/5 |
| LNN | MILD_FOCAL | 0.474637 ± 0.029035 | 0.296985 ± 0.048532 | -0.057880 | 0/5 |
| LSTM | CE | 0.474233 ± 0.018733 | 0.328523 ± 0.039684 | -0.058285 | 0/5 |
| LSTM | MILD_WCE | 0.473475 ± 0.026328 | 0.330032 ± 0.043886 | -0.059043 | 0/5 |
| LNN | MILD_WCE | 0.459198 ± 0.010765 | 0.298071 ± 0.014991 | -0.073319 | 0/5 |

## Protocol and changes

2010–2025; horizon/lookback 20 trading days; seeds 42/52/62/72/82; LNN/LSTM/Transformer; CE/MILD_WCE/MILD_FOCAL; validation folds 2019/2020/2021; 41 thresholds 0.30–0.70; test 2022–2025. Hidden size 128, learning rate 0.005, maximum 100 epochs/fold, patience 10, batch size 64, final fit 60 epochs: unchanged.

Common inputs: Log_Ret, Vol20, Momentum20, Disparity20, RSI14. Local inputs fixed before training: VXN, SOX, US10Y, DXY_LogRet1, DXY_LogRet5. DXY transformations reuse the original 1-day/5-day logarithmic return definitions. Other computed auxiliary transformations are not selected as inputs.

The original S&P500 notebook and results remain unchanged. The NASDAQ100 copy adds the DXY ticker and its two selected inputs, switches the requested market/output directory, freezes the data snapshot, and adds causal audits, per-run checkpoints and reporting. Training, model, loss and split functions are unchanged apart from reporting-only checkpoint calls. No test-driven parameter/feature changes or model selection were made.

## Availability / leakage audit

Daily auxiliary rows keep the existing U.S. lag=0 alignment. Sequence X[i-20:i] excludes row i. Thus every input precedes the target date; the target return starts at close(i), and there is no assumption that VXN or DXY finalizes at the same instant as the Nasdaq cash close. Trailing returns and ffill only are used. Assertions checked date ordering, horizon containment, train-only scalers and causal invariance under future-data changes. Thresholds were recomputed exclusively from validation probabilities and verified against the fixed test thresholds. See leakage_audit.json and data_manifest.json. Yahoo daily history is not a point-in-time vintage database, so these checks do not certify the absence of vendor historical revisions.

Δ BA describes performance differences, not statistical significance. The test period is evaluated for reporting only; no test results feed back into fitting or threshold choice.

## Files

- SCI_v1_4_WALKFORWARD_NASDAQ100.completed.ipynb: fully executed notebook
- seed_results.csv: 45 learned rows and 3 baseline rows
- summary.csv / formatted_summary.csv: numerical and original formatted seed summaries
- persistence_comparison.csv / baselines.csv: per-seed differences and all baselines
- predictions/: full-precision test and validation probabilities for every run
- market_input.csv / data_manifest.json: frozen raw input and checksum
- protocol_lock.json / leakage_audit.json / execution.log: protocol, checks and execution evidence
