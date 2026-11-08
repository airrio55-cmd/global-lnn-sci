# V14 Pre-registered Rolling-Origin Historical Replication Protocol

**Status:** LOCKED AT COMMIT REFERENCING THIS FILE — no V14 model fitted or V14 outcome computed before lock.

**Protocol lock:** the immutable Git commit containing this document and `run_v14_locked.py`; inspect Git history for the commit SHA and UTC timestamp. The protocol's content is immutable once locked.

## 1. Purpose and status of prior knowledge

This historical replication evaluates whether the association observed in the 2022–2025 post-hoc analysis—larger shifts toward trend continuation coinciding with greater losses in discrimination—recurs in overlapping pre-2022 rolling-origin windows. This is **pre-specified historical replication**, not prospective validation, causal identification, or an independent fresh dataset. The original 2022–2025 outcomes, the prior 2010–2018 aggregate signal–outcome effects, and the choice of 200DMA as the primary signal were already seen before protocol drafting. No V14 rolling-origin model AUC was calculated as part of preparing this protocol.

**Repository inventory (2026-11-09, before lock):** an inspection of the default-branch file tree in `airrio55-cmd/global-lnn-sci` (approximately 3,812 tree entries when inspected) found **no paths matching** `v14`, `rolling_origin`, `rolling-origin`, `preregister`, `pre-register`, `historical.replication`, or `2015.2016`. This is a **path-based check only**, not a proof that the results were never calculated off-repository or under other names. Any subsequently discovered prior result must be disclosed.

## 2. Markets, features, target and timing

Five markets: SP500, NASDAQ100, NIKKEI225, EUROSTOXX50, KOSPI200. Use the exact frozen `artifacts/<market>/market_input.csv` and `artifacts/jof_phase1_benchmark_expansion/frozen_features/<market>.csv` and the market-specific `COMMON_LOCAL` feature names in the phase-one `data_manifest.json`, without fetching or refreshing data. The primary target at forecast date *t* is `1[Close_(t+20) > Close_t]`, measured on each market’s actual session index, with equality assigned zero. Each W=20 input window comprises feature rows **t−20 through t−1** (oldest first). The three signals—Persistence (20 sessions), 200DMA and Momentum60—use the actual preceding market session (t−1), with 200DMA computed using the 200 closes through t−1 inclusive.

An observation may enter a split only if its forecast date lies within that split; its target endpoint t+20 is no later than the split’s end; its 20-window inputs predate t; and the input features are finite. **Do not add an extra 20-row purge after enforcing the label-endpoint rule.** For each fit, StandardScaler parameters are fitted only on the features of that fit’s eligible training interval, shared across all 20 lags, then the W20 tensor is flattened to chronological 20×F columns without another scaler. Reuse the original fixed modeling configurations, not post-hoc thresholds; AUC is computed on raw probabilities. The available original frozen market features are retrospective: their real-time availability, especially externally sourced features, is not independently guaranteed. This caveat must be carried to the final paper.

## 3. Six expanding origins (fixed)

| Origin | Initial training years | Validation years | Test years |
|:--|:--|:--|:--|
| O1 | 2010–2012 | 2013–2014 | 2015–2016 |
| O2 | 2010–2013 | 2014–2015 | 2016–2017 |
| O3 | 2010–2014 | 2015–2016 | 2017–2018 |
| O4 | 2010–2015 | 2016–2017 | 2018–2019 |
| O5 | 2010–2016 | 2017–2018 | 2019–2020 |
| O6 | 2010–2017 | 2018–2019 | 2020–2021 |

This produces 5×6=30 market–origin units. Neighboring validation and test periods overlap and all markets share calendar-year shocks; the 30 units are not independent.

## 4. Exact training and scoring protocol (binding)

For **each market, origin, and each of the two fixed models**, produce validation probability predictions by **two annual expanding walk-forward fits**, one for each validation calendar year. For validation year *Y*, fit the model using **all eligible historical observations whose forecast date is strictly before January 1 of Y and whose 20-session target endpoint falls no later than December 31 of Y−1**, with no observations from Y or later in the estimator or scaler. Predict every eligible forecast date in Y (targets must resolve by December 31 of Y). Concatenate the predictions from the two annual folds in chronological date order; compute a **single pooled 2-year validation ROC AUC** (not the arithmetic average of the two annual AUCs). Refitting the scaler and model afresh for each annual fold is mandatory.

For **the two-year test**, fit the estimator and scaler **one additional time** on *all* eligible historical observations through the final validation year, requiring every training observation’s forward label endpoint to resolve no later than December 31 of that final validation year. Predict the full fixed two-year test window **without annual refits** and compute its pooled ROC AUC. No test outcome or feature at or after the test forecast origin may enter fitted model parameters or preprocessing. No part of 2022–2025 enters the replication.

Training may include observations from earlier validation years once their targets were observed; this is intentional expanding refitting. All years use the original market trading calendars. If either outcome class is absent, or either signal group has fewer than 20 eligible model-scoring observations in validation or test where an effect is required, record that statistic as undefined and apply the prespecified missingness rules, without choosing a replacement observation. If a model fit fails, record the failure and do not change its hyperparameters.

## 5. Fixed models

**LogisticRegression:** `penalty='l2', solver='lbfgs', C=1.0, max_iter=5000, fit_intercept=True, tol=1e-4, class_weight=None, random_state=42`.

**LGBMClassifier:** `objective='binary', n_estimators=300, learning_rate=.03, num_leaves=31, max_depth=-1, min_child_samples=20, subsample=1., colsample_bytree=1., reg_alpha=0., reg_lambda=0., class_weight=None, verbosity=-1, random_state=42, data_random_seed=42, feature_fraction_seed=42, bagging_seed=42, drop_seed=42, extra_seed=42, deterministic=True, force_col_wise=True, n_jobs=2`.

Never tune hyperparameters, thresholds, features, seeds or training durations using rolling-origin results. Reuse exact source dataset and original COMMON_LOCAL feature order. Record software versions and input hashes.

## 6. Predefined variables

For each unit *u* and model *m*, compute validation and test empirical ROC AUC and `ΔAUC(u,m)=AUC_test−AUC_validation`. The H1 outcome is their arithmetic mean across two models, when both are defined. For signal *s*, compute `E_w(u,s)=P(y=1|s=1)−P(y=1|s=0)` separately in validation and test on the **identical model-scoring dates**; `S(u,s)=E_test−E_validation`. Positive S indicates movement toward trend continuation. For each model and period, compute Pearson score–signal correlation `r_w(u,m,s)`; for H1b use `r̄_test(u,200DMA)`, the average of the two model-specific test correlations, and define `T(u)=S(u,200DMA)×r̄_test(u,200DMA)`. Do not substitute absolute values or reverse the sign convention.

## 7. Fixed hypotheses and interpretation condition

**H1 (sole primary directional hypothesis):** across the 30 units, `ρ_Spearman[S(u,200DMA), mean_m ΔAUC(u,m)] < 0`.

**H1b (secondary, pre-specified alignment-conditioned diagnostic):** `ρ_Spearman[T(u), mean_m ΔAUC(u,m)] > 0`, using the Test-period score–200DMA alignment multiplied by the 200DMA relation shift. A positive directional association is expected if reversal-biased scoring interacts adversely with a continuation shift. This is descriptive association, not a causal decomposition: *T* includes predictions derived from the fitted models. **Because T and AUC_test share the same test-period scores and outcomes, positive H1b association is partly mechanical; report H1b only as a consistency check, never as independent evidence for H1.**

**H2 (two secondary directional hypotheses):** replace the 200DMA relation shift in H1 by Momentum60 and Persistence respectively; hypothesized correlations are negative.

**H3 (descriptive, no independent-unit p-value):** more than 50% of the 60 model×unit validation score–Persistence correlations are negative. Report numerator, denominator and market-level counts; neither a naive binomial p-value nor a pooled independent-unit CI is allowed.

**Predeclared prerequisite for interpreting H1 as a trend-reversal mechanism:** if mean test-period 200DMA alignment is negative in **at most 15 of the 30 market–origin units**, classify the directional H1 result as **"alignment prerequisite not met"**, regardless of nominal p-value, while still publishing the original three-way H1 decision label and all raw statistics. If negative in at least 16 units, label **"alignment prerequisite descriptively met"**; this does **not** establish causation or validate the nominal p-value. Near-zero alignment remains classified by its literal sign with the full distribution disclosed, not discarded.

## 8. Pre-specified statistics and limitations

- Primary statistic: pooled 30-unit Spearman ρ for H1, with market-wise 6-unit Spearman values and within-market-centered-rank descriptive association reported alongside it. Market effects may contribute to the pooled coefficient.
- **Nominal permutation diagnostic:** 10,000 draws using seed 20261109, shuffling S over the 6 origins within each market; calculate the same pooled Spearman statistic and a one-sided `(1 + # permuted statistic ≤ observed)/(10001)` for H1/H2, and `(1 + # permuted statistic ≥ observed)/(10001)` for H1b. This permutation is **not an exact dependent-data test**; market overlaps and cross-market common shocks undermine exchangeability. Report p as *nominal*, not confirmatory.
- **Dependence sensitivities:** enumerate every independent circular shift of each market’s **evaluable origin sequence** (including identity; the total is the product of the number of evaluable origins per market, not fixed at 7776), report pooled ρ and the tail fraction in the direction fixed above. This approximately preserves within-market order but imposes artificial wraparound and fails to preserve shared annual shocks. Additionally enumerate 6 synchronized circular shifts of all five market series together; six shifts cannot yield p < .05. Neither approach gives an exact p-value.
- **Secondary family and multiplicity:** report nominal H1b, H2-Momentum60 and H2-Persistence permutation p-values and separately a Holm correction over this **fixed family of three**. The H1 unadjusted nominal p-value remains the designated primary result; all nominal and sensitivity limitations remain.
- **Other fixed diagnostics:** two model-specific H1 associations; fixed-effect descriptive regression of ΔAUC on S and market dummies; leave-one-market-out pooled Spearman associations. Apply without selecting attractive outcomes. H3 reports raw sign proportions; optional within-unit serial moving-block (L=20, 2000) correlation CI is descriptive only.
- Undefined correlations or AUCs: record all missing cells and reasons. **Minimum group size (pre-specified):** compute each signal–outcome effect E only if both signal=0 and signal=1 have at least 20 eligible observations in that validation/test period. If a signal group has fewer than 20, its E and shift S are undefined. If fewer than 30 H1 units are evaluable, compute H1 with the available complete cases and report **"evaluated on N of 30 units"**; use the same pre-specified nominal-direction labels, with the explicit complete-case caveat. No imputation or replacement of missing units. For permutation diagnostics, shuffle only evaluable predictor values within each market, retaining the missingness mask; circular shifts rotate only the evaluable origin sequence per market (the count of distinct combinations becomes the product of eligible market-wise sequence lengths, not necessarily 6^5). The synchronized shifts use six shared offset values, reduced modulo each market’s eligible length.

## 9. Fixed reporting rules

The H1 directional label is based on the preselected pooled Spearman and nominal permutation p: (a) `ρ<0` and `p<.05` → **"Nominally supported under a non-exact permutation diagnostic"**; (b) `ρ<0` and `p≥.05` → **"Directionally consistent, nominally non-significant"**; (c) `ρ≥0` → **"Not supported in direction"**. Append the alignment-prerequisite label from §7, plus whether the dependence sensitivity agrees. Never replace this with causal or robustly confirmatory wording. For H1b/H2 report direction, nominal p, Holm-three p, and sensitivities separately; no secondary finding changes the primary H1 label. H3 has no confirmatory p-value.

All results, including contradictory ones, must be reported. This historical replication cannot independently verify the main study's neural model performance because it refits only two non-neural models. The number of effective independent origins is much smaller than 30.

## 10. Outputs and frozen analysis conduct

Before **any fitting**, commit this protocol and the executable analysis script, with hashes and its associated input-inventory log. Then execute the frozen script one time, writing `v14_unit_level.csv`, `v14_results.json`, `v14_execution.log`, fit/sample diagnostics and complete model-scoring dates. Commit all output files. Document any post-run implementation bug and both original/corrected runs, without silently replacing outcomes.

One new SI section, one Results paragraph, and an Abstract sentence should report H1's exact §9 label with the prerequisite and the dependence caveats. Keep the v13.4 manuscript baseline immutable. No model retraining outside these two prespecified estimators, new market features, new horizons, residual S&P explanatory analyses or LNN ensembles. Do not add post-hoc controls or claim independent prospective preregistration.

## 11. Price-only pre-lock feasibility audit (not outcomes)

Before any model fit or inspection of the 20-session target labels, the original frozen Close series was used solely to count 200DMA=0/1 dates. The date filter required a forecast date within the prespecified two-year window and its 20-session target **endpoint date** no later than the window’s end; it did not calculate any y values, AUCs or effect estimates. Across the 60 market–origin–period pairs, only SP500 O1 Validation (200DMA=0: **6**, 200DMA=1: **478**) and NASDAQ100 O1 Validation (200DMA=0: **2**, 200DMA=1: **482**) fell below the 20-observation minimum. Other 58 price-only periods met the 20/20 requirement. These are **price-only upper-bound counts**, not final model-eligible group sizes: finite COMMON_LOCAL feature-window requirements can exclude additional dates. All 60 counts are reproduced by `run_v14_locked.py --preflight` without model fitting or reading outcome values. On this price-only screen, **at most 28/30 H1 units** are evaluable; the final complete-case N will be disclosed as determined by the frozen feature masks. The minimum group rule was frozen **before any V14 model fitting, AUC or E computation**.

## 12. Pre-execution checklist

1. Compare this text against the repository's frozen preprocessing, fold and estimator implementations; confirm all dataset paths, timing restrictions and source-input hashes.
2. Confirm the GitHub inventory observation in §1, documenting any other known historical analysis even if not reflected in repository file paths.
3. Perform **code-only validation** (syntax/static checks without fitting or calculating V14 outcome statistics); commit the fully executable script and protocol and record their lock commit SHA and UTC date in a separate lock record. Do not edit the locked protocol retroactively just to fill header blanks.
4. Execute, preserve all results, apply §9 labels regardless of sign and assess consistency with v13.4 as supplementary rather than modifying original frozen data.

## Revision history (pre-lock), then immutable lock

This final-review candidate incorporates the original draft, dependence-aware review, annual expanding-validation fit definition, fixed test re-fit definition, an H1 alignment prerequisite, and a pre-specified H1b. It removes the editorial review note. No V14 model fitting or rolling-origin evaluation occurred during preparation of these protocol revisions.

Pre-lock amendment: added an a priori 20/20 signal-group eligibility rule, complete-case reporting and variable-length circular-shift counts; recorded the price-only preflight, and flagged H1b's shared-score/outcome mechanical association. Original three-way H1 direction labels and no-retuning rule remain unchanged.
