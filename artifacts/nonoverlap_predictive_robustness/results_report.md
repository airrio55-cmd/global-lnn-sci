# Final non-overlapping predictive robustness

This analysis addresses robustness to overlapping H=20 forecast labels. The prespecified subset starts at the first frozen test observation and selects every20th observed prediction row. No model selection, phase search, training, new prediction or threshold change. Main full-test results remain unchanged.

|Market|N full / subset|Full delta BA|Subset delta BA|BA sign preserved|Full delta accuracy|Subset delta accuracy|Holm p|
|---|---:|---:|---:|---|---:|---:|---:|
|SP500|963 / 49|-0.088288|-0.211174|True|-0.175493|-0.306122|0.106793|
|NASDAQ100|963 / 49|-0.033739|-0.060662|True|-0.055036|-0.061224|1|
|NIKKEI225|938 / 47|+0.068704|+0.146617|True|-0.034115|+0.063830|1|
|EUROSTOXX50|964 / 49|+0.053484|-0.052586|False|+0.106846|+0.020408|1|
|KOSPI200|935 / 47|+0.011554|+0.082353|True|+0.065241|+0.170213|0.395841|

Full contrasts use the same frozen majority vote as the primary cross-market analysis, not means of seed metrics. McNemar concerns accuracy, not BA. It is exploratory: reduced label overlap does not guarantee complete serial independence, and small subset N reduces power. Prior test-based Best selection remains a limitation. Negative and nonsignificant results are retained.

## Paired McNemar details

|Market|n00|n01|n10|n11|Exact p|Continuity-corrected p|Primary p|Holm p|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|SP500|8|26|11|4|0.0200739|0.0213585|0.0213585|0.106793|
|NASDAQ100|14|10|7|18|0.629059|0.627626|0.629059|1|
|NIKKEI225|7|16|19|5|0.735879|0.735317|0.735879|1|
|EUROSTOXX50|11|9|10|19|1|1|1|1|
|KOSPI200|10|5|13|19|0.0962524|0.0989602|0.0989602|0.395841|

## Findings

BA sign preserved in 4/5 markets; accuracy sign preserved in 4/5. Holm-significant market-level McNemar tests: 0/5. This is a robustness check only, not a replacement for main results or evidence of equivalence. See selected_dates.csv and methodology_notes.md for exact phase, spacing and integrity checks.
