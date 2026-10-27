# Five-market exploratory statistics

No retraining, tuning, threshold search or prediction replacement. Best model/loss selected post hoc by highest five-seed mean TEST BA, as requested. This selection introduces optimism; p-values are descriptive/exploratory and Holm does not correct the prior test-based winner selection.

## Best configurations

|Market|Model|Loss|Mean BA|Delta Persistence|Delta 0.5|Delta Macro F1|
|---|---|---|---:|---:|---:|---:|
|SP500|LNN|MILD_WCE|0.450897|-0.064177|-0.049103|-0.108536|
|NASDAQ100|Transformer|CE|0.502597|-0.029921|+0.002597|-0.122879|
|NIKKEI225|LNN|CE|0.515214|+0.063946|+0.015214|-0.040656|
|EUROSTOXX50|LNN|MILD_FOCAL|0.508536|+0.061847|+0.008536|-0.024989|
|KOSPI200|LSTM|CE|0.526016|+0.022763|+0.026016|-0.065594|

## McNemar

Primary McNemar uses user-requested five-seed majority votes: threshold each seed using its original validation-selected threshold, then predict positive if at least three of five vote positive. No threshold search or probability averaging. S&P500 uses the completed reproducible rerun in artifacts/sp500_rerun; archived SP500 and failed replay outputs are excluded. Holm adjusts exactly five computed market p-values. No seed-specific McNemar tests are performed or included. Ensemble metrics differ from the five-seed mean metrics in market_best_models.csv and are labeled separately.

Persistence labels were reproduced from frozen Close data using the unchanged original deterministic baseline definition and verified against stored metrics. All computed pairs have identical dates and y_true; model BA/F1 and persistence BA/F1/accuracy reproduce saved rows.

McNemar tests equality of error probability/accuracy, NOT Balanced Accuracy. The primary p-value is the larger of exact binomial and continuity-corrected asymptotic p-values. Overlapping 20-observation targets and serial dependence violate the independent-pair assumption of ordinary McNemar; exact means exact under its model, not dependence-robust. No confirmatory time-series significance claim is justified by these p-values.

## Seed bootstrap and Wilcoxon

10,000 percentile bootstrap samples of five seed deltas, RNG seed 20261026. This captures conditional training-seed variation, not uncertainty across independent market histories. Seeds share the same test set. With five nonzero differences, the smallest two-sided exact Wilcoxon p is 0.0625; alpha=0.05 significance is unattainable even before Holm. Ties/zero differences may alter exactness.

## Friedman and post-hoc

- ce_only: statistic=0.400000, raw p=0.818731, Holm p=1, significant=False.
- all_configs: statistic=3.840000, raw p=0.871263, Holm p=1, significant=False.

Friedman uses five market blocks of five-seed mean BA, not 25 independent blocks. CE-only and fixed nine-configuration comparisons remain separate; no architecture-specific best-loss selection. Holm corrects the two omnibus tests. Pairwise Wilcoxon runs only for a Holm-significant omnibus, with joint Holm across all triggered pairs. Five markets yield low power and chi-square Friedman p-values are asymptotic. Markets are economically correlated; block independence is an approximation.

Ranks use 1=highest BA and average ranks for ties. A lower-than-0.5 Persistence baseline makes a positive delta insufficient evidence of useful predictive superiority. BA improvements alongside worse Macro F1 are explicitly flagged. KOSPI200 uses its user-authorized empirical observation calendar; 45 XKRX date discrepancies are not confirmed missing KRX observations.

## Scope

All five market-level McNemar tests are available. SP500 data source: artifacts/sp500_rerun only. All input prediction and seed files remain unchanged, verified by SHA256. The five-seed representative is a majority vote of separately thresholded predictions, not a new tuned model. Architecture ranking is CE-only; fixed-configuration ranking is separately reported for all nine configurations.

## Majority-vote McNemar results

|Market|N|Delta Accuracy|Majority BA|Primary raw p|Holm p|Significant|
|---|---:|---:|---:|---:|---:|---|
|SP500|963|-0.175493|0.426786|1.64782e-10|8.23908e-10|True|
|NASDAQ100|963|-0.055036|0.498779|0.0101337|0.0202673|True|
|NIKKEI225|938|-0.034115|0.519973|0.23862|0.23862|False|
|EUROSTOXX50|964|+0.106846|0.500173|6.25975e-07|2.5039e-06|True|
|KOSPI200|935|+0.065241|0.514806|0.00253671|0.00761013|True|

These significance flags concern accuracy equality under ordinary McNemar assumptions; the sign of Delta Accuracy indicates improvement versus deterioration. They do not test BA directly. Majority-vote metrics are distinct from five-seed means.

## Seed-delta bootstrap

|Market|Mean delta BA|95% percentile CI|Wilcoxon raw p|Holm p|
|---|---:|---|---:|---:|
|SP500|-0.064177|[-0.076281, -0.045515]|0.0625|0.3125|
|NASDAQ100|-0.029921|[-0.055203, -0.002447]|0.1875|0.3125|
|NIKKEI225|+0.063946|[+0.055433, +0.074302]|0.0625|0.3125|
|EUROSTOXX50|+0.061847|[+0.056333, +0.067766]|0.0625|0.3125|
|KOSPI200|+0.022763|[+0.004388, +0.045848]|0.0625|0.3125|

Five-seed CIs describe conditional seed variability; they are not independence-corrected market-history confidence intervals. All five selected configurations have lower mean Macro F1 than Persistence; BA increases with Macro F1 deterioration are flagged for Nikkei225, EURO STOXX 50 and KOSPI200.

Post-hoc status: not performed because neither Holm-corrected omnibus test is significant. posthoc_wilcoxon.csv contains headers and no comparisons. See rankings_ce_only.csv for architecture ranks without best-loss selection and rankings_all_configs.csv for fixed model/loss ranks.
