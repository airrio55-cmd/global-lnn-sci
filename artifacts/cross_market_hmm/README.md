# Five-market causal HMM regime analysis

No predictive retraining, tuning, threshold changes, feature changes or regime-based model reselection. SP500 uses reproducible rerun only.

Monthly HMM fits: 240; iteration-limit hits: 0; negative final likelihood gains: 0. All 3-state specifications fixed before fitting.

## Frozen Best configuration by regime

|Market|Model / Loss|Regime|N|Positive label rate|Delta BA|Delta Macro F1|95% date-block CI|Small sample|
|---|---|---|---:|---:|---:|---:|---|---|
|SP500|LNN / MILD_WCE|Low|335|0.704|-0.0572|-0.1796|[-0.2046, +0.1126]|False|
|SP500|LNN / MILD_WCE|Normal|412|0.646|-0.0507|-0.0798|[-0.2509, +0.1574]|False|
|SP500|LNN / MILD_WCE|High|216|0.620|-0.0192|-0.0124|[-0.2954, +0.2293]|False|
|NASDAQ100|Transformer / CE|Low|140|0.843|-0.0063|-0.1540|[-0.0689, +0.0706]|False|
|NASDAQ100|Transformer / CE|Normal|451|0.703|-0.0331|-0.1714|[-0.1315, +0.0608]|False|
|NASDAQ100|Transformer / CE|High|372|0.551|+0.0352|-0.0095|[-0.1240, +0.1875]|False|
|NIKKEI225|LNN / CE|Low|458|0.648|+0.0178|-0.1188|[-0.1339, +0.1584]|False|
|NIKKEI225|LNN / CE|Normal|363|0.601|+0.0827|+0.0246|[-0.0893, +0.2457]|False|
|NIKKEI225|LNN / CE|High|117|0.538|+0.2402|+0.1390|[+0.0289, +0.4728]|False|
|EUROSTOXX50|LNN / MILD_FOCAL|Low|463|0.620|+0.0603|-0.0240|[-0.0501, +0.1624]|False|
|EUROSTOXX50|LNN / MILD_FOCAL|Normal|347|0.464|+0.0506|-0.0689|[-0.0774, +0.1863]|False|
|EUROSTOXX50|LNN / MILD_FOCAL|High|154|0.617|+0.1606|+0.1529|[-0.0054, +0.2931]|False|
|KOSPI200|LSTM / CE|Low|137|0.372|+0.1043|-0.0313|[-0.0922, +0.2572]|False|
|KOSPI200|LSTM / CE|Normal|407|0.604|-0.0306|-0.1085|[-0.1140, +0.0510]|False|
|KOSPI200|LSTM / CE|High|391|0.593|+0.0205|-0.0336|[-0.0885, +0.1202]|False|

## RQ1: Does LNN relative performance vary with regime?

The following compares each fixed LNN loss separately; no within-regime winner is selected. Values are delta BA vs Persistence in Low / Normal / High order.
- SP500, LNN CE: -0.0763 / -0.0408 / -0.0159.
- SP500, LNN MILD_FOCAL: -0.0571 / -0.0681 / -0.0388.
- SP500, LNN MILD_WCE: -0.0572 / -0.0507 / -0.0192.
- NASDAQ100, LNN CE: -0.0732 / -0.0025 / -0.0025.
- NASDAQ100, LNN MILD_FOCAL: +0.0073 / +0.0020 / -0.0129.
- NASDAQ100, LNN MILD_WCE: -0.0247 / +0.0070 / -0.0442.
- NIKKEI225, LNN CE: +0.0178 / +0.0827 / +0.2402.
- NIKKEI225, LNN MILD_FOCAL: +0.0141 / +0.0767 / +0.2291.
- NIKKEI225, LNN MILD_WCE: +0.0265 / +0.0641 / +0.2468.
- EUROSTOXX50, LNN CE: +0.0563 / +0.0317 / +0.1336.
- EUROSTOXX50, LNN MILD_FOCAL: +0.0603 / +0.0506 / +0.1606.
- EUROSTOXX50, LNN MILD_WCE: +0.0601 / +0.0598 / +0.1348.
- KOSPI200, LNN CE: +0.0951 / -0.0381 / -0.0287.
- KOSPI200, LNN MILD_FOCAL: +0.0966 / -0.0454 / -0.0159.
- KOSPI200, LNN MILD_WCE: +0.0951 / -0.0483 / -0.0646.

## RQ2–RQ4: Market-specific localization

Signs below refer to five-seed mean BA differences, not statistical proof.
- RQ3, SP500: LNN MILD_WCE — Low: delta BA -0.0572 (N=335); Normal: delta BA -0.0507 (N=412); High: delta BA -0.0192 (N=216).
- RQ3, NASDAQ100: Transformer CE — Low: delta BA -0.0063 (N=140); Normal: delta BA -0.0331 (N=451); High: delta BA +0.0352 (N=372).
- RQ2, NIKKEI225: LNN CE — Low: delta BA +0.0178 (N=458); Normal: delta BA +0.0827 (N=363); High: delta BA +0.2402 (N=117).
- RQ2, EUROSTOXX50: LNN MILD_FOCAL — Low: delta BA +0.0603 (N=463); Normal: delta BA +0.0506 (N=347); High: delta BA +0.1606 (N=154).
- RQ4, KOSPI200: LSTM CE — Low: delta BA +0.1043 (N=137); Normal: delta BA -0.0306 (N=407); High: delta BA +0.0205 (N=391).

Descriptive localization (not a test of differences between regimes):
- SP500: strongest Persistence BA advantage is in Low, delta BA -0.0572; positive Best-model BA deltas occur in none.
- NASDAQ100: strongest Persistence BA advantage is in Normal, delta BA -0.0331; positive Best-model BA deltas occur in ['High'].
- NIKKEI225: largest fixed Best-model BA delta is in High, +0.2402; positive deltas occur in ['Low', 'Normal', 'High']. Interpret together with regime N, CIs and Macro F1; maximum effect alone is not evidence of concentration.
- EUROSTOXX50: largest fixed Best-model BA delta is in High, +0.1606; positive deltas occur in ['Low', 'Normal', 'High']. Interpret together with regime N, CIs and Macro F1; maximum effect alone is not evidence of concentration.
- KOSPI200: largest fixed Best-model BA delta is in Low, +0.1043; positive deltas occur in ['Low', 'High']. Interpret together with regime N, CIs and Macro F1; maximum effect alone is not evidence of concentration.

## RQ5: BA improvement versus Macro F1 deterioration

Inspect Positive_label_rate and N in the table together with both deltas. Regimes with improved BA but worse Macro F1:
- NASDAQ100, High: positive-label share 0.551; delta BA +0.0352; delta Macro F1 -0.0095; N=372.
- NIKKEI225, Low: positive-label share 0.648; delta BA +0.0178; delta Macro F1 -0.1188; N=458.
- EUROSTOXX50, Low: positive-label share 0.620; delta BA +0.0603; delta Macro F1 -0.0240; N=463.
- EUROSTOXX50, Normal: positive-label share 0.464; delta BA +0.0506; delta Macro F1 -0.0689; N=347.
- KOSPI200, Low: positive-label share 0.372; delta BA +0.1043; delta Macro F1 -0.0313; N=137.
- KOSPI200, High: positive-label share 0.593; delta BA +0.0205; delta Macro F1 -0.0336; N=391.

This is an observed association, not proof that imbalance causes the metric disagreement. Balanced accuracy averages class recalls while Macro F1 also depends on precision and prediction prevalence; Pred_Pos_Rate and per-seed metrics are saved for diagnosis.

## Interpretation limits

Regimes are within-market, relative and month-remapped. Block CIs are conditional/exploratory, with small-regime flags and no multiple-comparison-adjusted significance claim. Class imbalance, label overlap, post-test Best selection, possible HMM nonconvergence and KOSPI empirical-calendar limitations must accompany any paper claim. See methodology_notes.md for full causal timing and bootstrap specification.
