# Validation-selected statistical, reduced-overlap and Nikkei High robustness

All15 architecture-specific loss selections match the required validation-only WF BA rule.75 primary seed runs are reused unchanged. SP500 uses reproducible rerun only. No training, threshold change, HMM refit or old artifact replacement.

## 1. What changes under validation selection?

The primary tables now use the validation-selected loss inside every architecture, not the old test-selected market winner. Seed-based statistics and majority-vote statistics remain separate. LNN seed inference uses both labeled Holm families; reduced-overlap direction counts are recalculated, not inherited.

|Market|Architecture|Selected loss|WF validation BA|
|---|---|---|---:|
|SP500|LNN|MILD_FOCAL|0.603727|
|SP500|LSTM|MILD_FOCAL|0.617830|
|SP500|Transformer|MILD_FOCAL|0.636180|
|NASDAQ100|LNN|MILD_FOCAL|0.565535|
|NASDAQ100|LSTM|MILD_FOCAL|0.668468|
|NASDAQ100|Transformer|MILD_WCE|0.693409|
|NIKKEI225|LNN|MILD_WCE|0.639022|
|NIKKEI225|LSTM|MILD_FOCAL|0.686938|
|NIKKEI225|Transformer|MILD_FOCAL|0.714982|
|EUROSTOXX50|LNN|MILD_FOCAL|0.631657|
|EUROSTOXX50|LSTM|CE|0.657155|
|EUROSTOXX50|Transformer|CE|0.614117|
|KOSPI200|LNN|CE|0.666024|
|KOSPI200|LSTM|CE|0.652304|
|KOSPI200|Transformer|MILD_FOCAL|0.660303|

## 2. Manuscript primary LNN statistical table

|Market|Loss|Mean test BA|Persistence BA|Mean delta BA|Seed-bootstrap95% CI|Seeds>P|Wilcoxon raw p|Holm15 p|LNN-only Holm5 p|Majority delta accuracy|McNemar raw p|McNemar Holm5 p|
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
|SP500|MILD_FOCAL|0.438382|0.515074|-0.076692|[-0.087626,-0.058788]|0/5|0.0625|0.9375|0.3125|-0.146417|1.1883e-07|4.7532e-07|
|NASDAQ100|MILD_FOCAL|0.474637|0.532517|-0.057880|[-0.082721,-0.036723]|0/5|0.0625|0.9375|0.3125|-0.242991|8.16103e-20|4.08051e-19|
|NIKKEI225|MILD_WCE|0.511176|0.451269|+0.059907|[+0.053890,+0.066591]|5/5|0.0625|0.9375|0.3125|-0.055437|0.0431473|0.0431473|
|EUROSTOXX50|MILD_FOCAL|0.508536|0.446689|+0.061847|[+0.056516,+0.067745]|5/5|0.0625|0.9375|0.3125|+0.106846|6.25975e-07|1.87793e-06|
|KOSPI200|CE|0.495425|0.503252|-0.007827|[-0.025822,+0.007967]|2/5|0.625|0.9375|0.625|+0.050267|0.0175285|0.0350571|

Footnotes: seed bootstrap describes algorithmic seed variability only; Wilcoxon n5 has low power. Primary Wilcoxon Holm covers15 architecture-market tests; LNN-only Holm5 is supplemental. McNemar tests Accuracy/correctness, NOT BA. Overlapping H20 labels violate strict independence assumptions; full-test McNemar is supportive, not definitive.

## 3. Architecture comparison

- Balanced_Accuracy: Friedman statistic=1.200000, raw p=0.548812, Holm2 p=1, Kendall W=0.1200.
- Macro_F1: Friedman statistic=1.200000, raw p=0.548812, Holm2 p=1, Kendall W=0.1200.

The analysis did not detect a stable cross-market architecture ranking, although the small number of market blocks limits inferential power. This is not evidence that architectures are equivalent.

## 4. Recomputed non-overlap manuscript table

|Market|Full majority delta BA|Subset N|Subset LNN BA|Subset Persistence BA|Subset delta BA|BA sign preserved|McNemar Holm5 p|
|---|---:|---:|---:|---:|---:|---|---:|
|SP500|-0.067019|49|0.339962|0.567235|-0.227273|True|0.106793|
|NASDAQ100|-0.053234|49|0.456801|0.534007|-0.077206|True|0.236919|
|NIKKEI225|+0.066595|47|0.509398|0.425752|+0.083647|True|1|
|EUROSTOXX50|+0.053484|49|0.507759|0.560345|-0.052586|False|1|
|KOSPI200|+0.005767|47|0.466667|0.476471|-0.009804|False|1|

BA direction is preserved in **3/5** markets; Accuracy direction in **5/5**. These are newly calculated validation-selected counts, not the old4/5 statement. The reduced-overlap subset lowers mechanical label overlap but does not establish full independence. N47–49 gives low power; retain negative/sign-changing results.

## 5. Nikkei High absolute primary metrics

Configuration: LNN MILD_WCE; N=117, positive-label rate=0.538462. Primary LNN values are five-seed metric means, not an artificially enlarged585-row sample.

|Metric|LNN MILD_WCE seed mean|Persistence|Difference|
|---|---:|---:|---:|
|Accuracy|0.511111|0.299145|+0.211966|
|Balanced_Accuracy|0.539153|0.292328|+0.246825|
|Macro_F1|0.448748|0.290385|+0.158363|
|Recall|0.174603|0.380952|-0.206349|
|Precision|0.710881|0.358209|+0.352672|
|F1|0.267717|0.369231|-0.101514|
|Pred_Pos_Rate|0.138462|0.572650|-0.434188|

Absolute LNN BA is 0.539153, only modestly above0.5, while Persistence BA is 0.292328. The large relative delta+0.246825 partly reflects weak baseline performance; it is not evidence of high absolute predictive accuracy.

## 6. New MILD_WCE time-series sensitivity

|Metric|Observed delta|95% moving-block CI|Valid / requested|Invalid|
|---|---:|---|---:|---:|
|Delta_BA|+0.246825|[+0.009408,+0.475510]|9991/10000|9|
|Delta_Macro_F1|+0.158363|[-0.147346,+0.485464]|9991/10000|9|
|Delta_Accuracy|+0.211966|[-0.166606,+0.566987]|9991/10000|9|

These are freshly computed MILD_WCE intervals, not reused CE intervals. They condition on frozen HMM labels and exclude HMM refitting/regime uncertainty/model-selection uncertainty/multiplicity across regime cells.

Episode-restricted permutation: observed mean delta BA=+0.246825, two-sided Monte Carlo p=0.334267, permutations=10000; 7 contiguous High episodes, 9 blocks, 5 shorter end blocks. No block crosses a High interruption. These episode/block counts are descriptive construction counts, NOT an effective sample-size estimate. The test is exploratory, post-hoc, not preregistered and not confirmatory.

Although117 daily High-regime observations are available, the20-day forecast horizon induces substantial dependence among adjacent labels, so the effective amount of independent information is materially smaller than the raw observation count. No exact independent information count is asserted.

## 7. Manuscript interpretation

**Outcome B.**
The apparent Nikkei High-regime advantage is descriptive but statistically fragile once temporal dependence is more explicitly acknowledged.

The BA bootstrap CI has a positive lower bound and Nikkei non-overlap BA direction remains positive; these supportive results are retained. However, the interval is wide, Macro F1/Accuracy intervals span zero, and the episode-restricted permutation evidence is weak. The positive BA interval must not be promoted alone as confirmatory evidence.

The manuscript should shift toward a **benchmark/negative-results framing**, with Nikkei High presented as a promising but statistically fragile descriptive exception rather than the central claim of established conditional generalization. This does not prove no effect or justify retuning. Negative U.S. results and European/Korean reduced-overlap sign reversals must remain visible.

No result is used to alter models, seeds, thresholds, source data or HMM labels. Old statistical, nonoverlap, HMM and economic artifacts remain intact. Full seed/architecture, majority, nonoverlap, bootstrap and permutation samples and construction manifests are retained for audit.
