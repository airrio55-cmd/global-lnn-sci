# Leave-one-market-out LNN representation transfer

New TRANSFER_COMMON experiment, not directly identical to COMMON_LOCAL base models. Fixed CE-only LNN, paired target training0.001 LR, identical budgets; initialization is the target-stage difference. Sources/folds/cutoffs fixed before training.

## RQ11–RQ12: Paired transfer and negative transfer

|Target|Scratch BA|Transfer BA|Mean delta BA|Delta Macro F1|Positive seeds|Transfer-positive|Robust-positive|Metric-consistent|Negative transfer|
|---|---:|---:|---:|---:|---:|---|---|---|---|
|SP500|0.481002|0.488971|+0.007968|-0.010216|2/5|True|False|False|False|
|NASDAQ100|0.500000|0.479431|-0.020569|+0.037601|0/5|False|False|False|True|
|NIKKEI225|0.516869|0.507526|-0.009344|+0.003530|1/5|False|False|False|True|
|EUROSTOXX50|0.510859|0.515362|+0.004502|+0.075512|3/5|True|False|True|False|
|KOSPI200|0.543218|0.543740|+0.000522|+0.010704|3/5|True|False|True|False|

## Seed uncertainty and majority-vote McNemar

All tests are exploratory, two-sided alpha0.05. Seed CIs do not represent independent market histories; McNemar tests accuracy and assumes independent pairs despite overlapping labels.

|Target|Metric|95% seed-bootstrap CI|Wilcoxon raw p|Holm5 p|Holm10 p|
|---|---|---|---:|---:|---:|
|SP500|Balanced_Accuracy|[-0.002516, +0.021136]|0.5|1|1|
|SP500|Macro_F1|[-0.024464, -0.000606]|0.25|0.75|1|
|NASDAQ100|Balanced_Accuracy|[-0.026969, -0.010166]|0.125|0.625|1|
|NASDAQ100|Macro_F1|[+0.012131, +0.063072]|0.125|0.625|1|
|NIKKEI225|Balanced_Accuracy|[-0.016344, -0.002343]|0.125|0.625|1|
|NIKKEI225|Macro_F1|[-0.023121, +0.030182]|0.8125|1|1|
|EUROSTOXX50|Balanced_Accuracy|[-0.004126, +0.013830]|0.625|1|1|
|EUROSTOXX50|Macro_F1|[+0.032907, +0.117526]|0.125|0.625|1|
|KOSPI200|Balanced_Accuracy|[-0.021877, +0.022676]|1|1|1|
|KOSPI200|Macro_F1|[-0.027993, +0.052898]|0.8125|1|1|

|Target|Majority accuracy delta|McNemar primary p|Holm p|
|---|---:|---:|---:|
|SP500|+0.000000|1|1|
|NASDAQ100|-0.068536|2.96253e-09|1.48127e-08|
|NIKKEI225|-0.122601|2.3937e-07|9.57481e-07|
|EUROSTOXX50|-0.022822|0.25335|0.506701|
|KOSPI200|+0.013904|0.0123434|0.0370301|

## RQ13: Exploratory regime dependence

Frozen HMM labels are used unchanged. No classifier is selected by regime.

|Target|Regime|N|Delta BA|Delta Macro F1|
|---|---|---:|---:|---:|
|SP500|Low|335|+0.005825|+0.019545|
|SP500|Normal|412|+0.002817|-0.009152|
|SP500|High|216|+0.000000|+0.000000|
|NASDAQ100|Low|140|+0.070185|-0.000777|
|NASDAQ100|Normal|451|-0.015286|+0.039276|
|NASDAQ100|High|372|+0.017412|+0.046107|
|NIKKEI225|Low|458|+0.038396|+0.064664|
|NIKKEI225|Normal|363|-0.056881|-0.127899|
|NIKKEI225|High|117|-0.021958|+0.053840|
|EUROSTOXX50|Low|463|+0.016295|+0.056295|
|EUROSTOXX50|Normal|347|+0.006912|+0.102378|
|EUROSTOXX50|High|154|+0.001713|+0.012818|
|KOSPI200|Low|137|+0.032490|+0.021233|
|KOSPI200|Normal|407|-0.012751|+0.004002|
|KOSPI200|High|391|-0.008835|-0.011984|

Prespecified focus regions:
- NIKKEI225 High: delta BA -0.021958, delta Macro F1 +0.053840, N=117; exploratory, not evidence for a retuned model.
- EUROSTOXX50 High: delta BA +0.001713, delta Macro F1 +0.012818, N=154; exploratory, not evidence for a retuned model.
- KOSPI200 Low: delta BA +0.032490, delta Macro F1 +0.021233, N=137; exploratory, not evidence for a retuned model.

## RQ14: Secondary economics in prespecified BA-positive markets

No rules or costs changed: primary daily next-close Long/Cash at10bps round trip. Markets with nonpositive mean Delta BA are excluded by design and are not silently reclassified.

|Target|Delta CAGR|Delta Sharpe|Delta MDD|
|---|---:|---:|---:|
|SP500|+0.000000|+0.000000|+0.000000|
|EUROSTOXX50|-0.027966|-0.118330|-0.019365|
|KOSPI200|+0.002840|+0.016197|+0.005348|

Pooled LOMO transfer can test target benefit but cannot isolate US vs foreign source contributions or Japan/Europe-to-Korea mechanisms. Negative transfer is a substantive result, not hidden. Feature compatibility is controlled by new Scratch baselines; no claim that these are identical feature experiments to archived COMMON_LOCAL results. See methodology_notes.md and transfer_protocol.json for frozen cutoffs, scaler/label audits, budgets and limits.
