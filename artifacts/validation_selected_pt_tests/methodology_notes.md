# Pesaran–Timmermann directional accuracy methodology

## Formula and authoritative reference
Pesaran, M.H. and Timmermann, A. (1992), *A Simple Nonparametric Test of Predictive Performance*, Journal of Business & Economic Statistics,10(4),461–465. The original conventional variance formula is reproduced; source was cross-checked against `rugarch::DACTest(test="PT")`, maintained by Alexios Ghalanos. Source/documentation URLs and exact retrieved content SHA256 are in pt_reference.json. No external market data or alternative directional-accuracy test is used.

For existing binary actual direction y and forecast f, define n=sample size, P_y=mean(y), P_f=mean(f), P_hat=mean(I[y=f]), and P_star=P_y P_f+(1−P_y)(1−P_f).

\[
V(\widehat P)=\frac{P_\star(1-P_\star)}{n},
\]
\[
V(\widehat P_\star)=\frac{(2P_y-1)^2 P_f(1-P_f)+(2P_f-1)^2 P_y(1-P_y)}{n}
 +\frac{4P_y P_f(1-P_y)(1-P_f)}{n^2},
\]
\[
\widehat V=V(\widehat P)-V(\widehat P_\star),\qquad
PT=\frac{\widehat P-P_\star}{\sqrt{\widehat V}}.
\]

Primary p=2Φ(−|PT|), two-sided conventional asymptotic standard-normal reference under directional independence. Supplemental prespecified positive-association p=1−Φ(PT). The positive tail is not selected after observing the sign. rugarch reports the latter tail; we additionally compute the requested primary two-sided tail.

For binary nondegenerate margins the same variance simplifies to 4P_y(1−P_y)P_f(1−P_f)(n−1)/n². This equality and the independent2×2 Pearson identity PT²=n/(n−1)×uncorrected Pearson chi-square are implementation checks, NOT replacement inference. A separate literal sign-coded translation of rugarch's formula is checked. Binary labels map to−1/+1 before using its forecast×actual>0 hit logic; passing0/1 directly would omit Down/Down hits and be wrong. No target label is redefined.

## Edge cases
Constant forecast has undefined PT variance: retain Accuracy/BA/marginal rates and mark "PT not defined for constant forecast", with NA statistic and p-values. Actual-constant or n<=1 cases are likewise undefined. Nonpositive/nonfinite variance is flagged, never silently replaced or clipped. All original formulas/components are saved, including an algebraic variance cross-check. Small expected2×2 cell count<5 is a diagnostic warning about the asymptotic reference, not a reason to remove inconvenient tests. Defined small-sample PT values remain visibly caveated.

## Frozen predictions and selection
Each of15 market/architecture losses is reverified by WF_Val_BA_mean from validation-only columns before opening test predictions; all expected configurations must match or processing stops. SP500 uses sp500_rerun only. Each of75 seed forecasts is original Probability>saved Threshold, strictly greater, never>=. Majority uses at least3 of5 binary votes, no averaged probabilities or optimized ensemble threshold. Full predictions/labels/Persistence are checked against already validated selected architecture outputs. No predictive training, checkpoint update, feature/target modification, HMM refit or signal inversion.

Architecture summaries show mean BA/Accuracy and mean/median of DEFINED seed PT values with defined/undefined counts. Counts of nominal p<0.05 are descriptive, not a combined p-value or75-test primary inference. P-values are not averaged. Zero/constant seeds are not dropped from75 rows.

## Multiplicity and direction
Family A:15 architecture-market majority PT two-sided tests, Holm15. Family B:5 LNN majority PT two-sided tests, Holm5 as supplemental LNN family. Positive one-sided Holm corrections for the same planned families are supplemental and labeled. Any undefined tests retain their planned hypothesis slot by internally reserving p1 during Holm, but undefined raw/adjusted results are displayed NA, not as a performed test. No undefined majority tests occurred in this analysis.

Significant_Holm15 flags rejection of independence in EITHER direction. Positive_direction_supported requires PT>0 AND primary two-sided adjusted p<0.05. A significant negative PT is negative association, NOT positive directional skill. Inverting those forecasts would be a new signal rule and is not done. The LNN manuscript support flag uses positive PT and two-sided Holm5<0.05; neither BA alone nor an unadjusted one-sided tail establishes support.

## Dependence and reduced-overlap robustness
**PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially.** This note appears in every manuscript-facing table. PT does not resolve dependence. Existing block-bootstrap and reduced-overlap analyses remain the main dependence-aware robustness checks.

Reduced-overlap selects the first frozen prediction row and every20th row thereafter, phase0 only, with no alternate offset. These rows are matched exactly to the prior validation-selected robustness subset. Five exploratory reduced-overlap PT p-values also receive a separately labeled Holm5; they are not merged with full-test primary families. The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence. N47–49 and small margins limit precision and power; nonsignificance is not equivalence.

## Benchmarks and Nikkei High
Always-Up/Down are descriptive class-imbalance context; constant-forecast PT is intentionally undefined. Persistence is the unchanged I(P_t>P_(t−20)) benchmark, verified against previous saved predictions. It uses P_t while neural inputs stop at t−1; the unequal information sets are retained and explicitly acknowledged, not fixed in this task. Benchmark PT raw p-values are context, not primary corrected hypotheses.

Nikkei High uses only frozen HMM High dates and LNN MILD_WCE, N117; all five seeds and the majority are shown without seed selection. No smoothing/refitting/relabeling of regimes. Always-Up Accuracy equals the High actual-positive rate (~0.538). Seed/majority Accuracy is compared with that trivial baseline and Persistence. High PT is exploratory and unadjusted for regime-cell/method exploration; nominal positive one-sided p-values are not confirmatory evidence. Small cells and overlapping labels compound the limitation. Existing episode-aware permutation and block-bootstrap results remain unchanged.

## Scope and conclusion policy
This is a retrospective reanalysis after prior test inspection. Validation-only loss verification removes explicit test-based loss selection but does not create a newly untouched test set. Outcome A means no positive primary Holm15 support; Outcome B means isolated positive support; Outcome C would describe broad positive support (at least8/15 across4 markets and2 architectures). These are interpretation labels only, not tuning rules. All positive, negative, null and undefined results are retained. No HMM/economic or prior statistical artifact is overwritten.

Reproduce analyze.py (requires the cited rugarch source/doc reference files in /tmp or equivalent recorded hash-matching sources), report.py, then validate.py. The source formula can be independently checked from the cited references; no network-derived observation enters PT data.
