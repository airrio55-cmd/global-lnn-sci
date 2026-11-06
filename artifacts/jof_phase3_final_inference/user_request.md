# JOURNAL OF FORECASTING — PHASE 3 FINAL STATISTICAL INFERENCE
## DM/GW + Final Holm Families + MCS/SPA

This task performs the final inferential layer for the Journal of Forecasting manuscript after completion of:

- Phase 1 benchmark expansion
- Phase 2 architecture expansion

No new predictive architecture is introduced in Phase 3.

The model universe is now frozen.

---

# 1. Frozen final model universe

## Neural architectures

1. LTC/LNN
2. CfC
3. LSTM
4. GRU
5. Transformer
6. PE-Transformer

## Non-neural learned models

7. Logistic Regression
8. LightGBM

## Rule / benchmark models

9. Persistence
10. 200DMA
11. Momentum60
12. Always-Up
13. Always-Down

Markets:

- S&P 500
- NASDAQ-100
- Nikkei 225
- EURO STOXX 50
- KOSPI 200

No model may be added, removed, or redefined after test outcomes are inspected.

---

# 2. Critical restrictions

DO NOT:

- retrain any model
- alter any saved prediction
- alter validation-selected losses
- alter thresholds
- alter majority-vote definitions
- alter H=20
- alter W=20
- alter train/validation/test splits
- refit HMM regimes
- search favorable non-overlap phases
- choose loss differential after viewing statistical results
- choose a benchmark after seeing pairwise p-values
- remove unfavorable models from MCS/SPA
- redefine multiplicity families after seeing adjusted p-values

All statistical definitions must be frozen before final calculations.

---

# 3. Artifact directory

Create:

`artifacts/jof_phase3_final_inference/`

Required outputs:

- `protocol_lock.json`
- `prediction_inventory.csv`
- `pairwise_loss_definitions.json`
- `dm_results_all.csv`
- `gw_results_all.csv`
- `holm_family_A_neural30.csv`
- `holm_family_B_learned40.csv`
- `holm_family_C_ltc5.csv`
- `holm_family_D_pe5.csv`
- `mcs_results.csv`
- `spa_results.csv`
- `model_confidence_sets_by_market.csv`
- `cross_market_summary.csv`
- `nonoverlap_inference.csv`
- `statistical_conclusion_matrix.csv`
- `final_inference_manifest.json`
- `completion_check.json`
- `methodology_notes.md`
- `results_report.md`

Recommended:

- `diagnostics/`
- `figures/`

---

# 4. Prediction source

Use only saved test predictions from existing frozen artifacts.

Primary prediction aggregation:

- stochastic neural models: 3-of-5 majority predictions
- Logistic Regression: deterministic prediction
- LightGBM: deterministic consensus if identical across seeds
- rules: deterministic

Also retain probability forecasts where available for loss-based tests.

Do not regenerate probabilities if frozen saved probabilities exist.

---

# 5. Test period

Primary test period remains:

`2022–2025`

All statistical inference in Phase 3 refers to this frozen held-out period unless explicitly labelled reduced-overlap.

---

# 6. Forecast horizon

Primary:

`H = 20`

Therefore overlapping target labels are present.

Every conventional asymptotic test must carry this caveat.

---

# 7. Primary loss differential for DM/GW

Because the task is binary directional forecasting, use a prespecified proper scoring rule.

Primary loss:

## Brier loss

For model m at time t:

`L_m,t = (p_m,t - y_t)^2`

where:

- `p_m,t` = predicted Up probability
- `y_t` = realized binary target

For deterministic rules without probabilities:

use binary forecast as probability 0 or 1.

This is intentional and must be documented.

Loss differential:

`d_t = L_A,t - L_B,t`

Positive mean d means model B has lower loss.

Do not change the sign convention later.

---

# 8. Secondary loss

Use one secondary loss only:

## Binary log loss

For probability-based learned models:

`- [y log(p) + (1-y) log(1-p)]`

Clip probabilities only for numerical stability:

`eps = 1e-12`

For deterministic 0/1 rules, binary log loss becomes numerically extreme and is not the preferred cross-family comparison.

Therefore:

- Brier = primary all-model comparison
- Log loss = secondary learned-model-only comparison

Do not use Accuracy or BA directly as DM loss.

---

# 9. Diebold–Mariano test

For each market, perform pairwise DM tests using Brier loss.

Use HAC/Newey-West variance.

Primary lag:

`H - 1 = 19`

Reason:

20-day overlapping forecast targets induce serial dependence up to approximately H−1 lags.

Use a two-sided test.

Report:

- Market
- Model_A
- Model_B
- Mean_loss_A
- Mean_loss_B
- Mean_differential
- DM_stat
- raw_two_sided_p
- HAC_lag
- N

If available and appropriate, use Harvey-Leybourne-Newbold small-sample correction, but document it explicitly.

Do not switch between corrected and uncorrected results based on significance.

---

# 10. DM comparison structure

Avoid reporting every pair in the manuscript body.

Compute full pairwise results, but prespecify focal comparisons.

## Focal benchmark comparisons

For each learned model compare against:

- Persistence
- 200DMA
- Momentum60

Learned models:

- LTC/LNN
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer
- Logistic Regression
- LightGBM

This gives:

`8 learned × 3 benchmarks × 5 markets = 120 focal DM comparisons`

Store all 120.

Also compute full pairwise matrix for MCS support.

---

# 11. Giacomini–White conditional predictive ability

Run GW as a robustness analysis.

Primary loss differential:

Brier loss differential.

Conditioning variables must be frozen before results.

Use a parsimonious conditioning vector:

1. intercept
2. lagged loss differential
3. lagged absolute market return
4. lagged Vol20

All conditioning variables must be observable at forecast origin.

Do not add additional conditioning variables after seeing results.

Use HAC covariance with lag 19.

Report:

- GW statistic
- degrees of freedom
- raw p
- N
- conditioning specification

If implementation constraints prevent exact original GW test, document the implemented conditional predictive ability test precisely.

Do not label an approximation as exact GW.

---

# 12. Final Holm multiplicity families

Use the frozen Phase 2 family proposal.

## Family A — Neural architecture × market PT family

6 neural architectures × 5 markets = 30 tests.

Members:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer

Apply Holm correction across the 30 primary two-sided PT p-values.

Output:

`holm_family_A_neural30.csv`

Columns:

- Market
- Model
- PT_stat
- raw_p
- Holm30_p
- sign_of_PT
- Forecast_Up_Rate
- positive_directional_support

Define:

`positive_directional_support = True`

only if:

- PT statistic > 0
- Holm-adjusted p < 0.05

Negative significant association must not count as skill.

---

# 13. Family B — all learned-model × market PT

8 learned models × 5 markets = 40 tests.

Models:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer
- Logistic
- LightGBM

Apply Holm across all 40.

Output:

`holm_family_B_learned40.csv`

Interpretation:

This is the broad multiplicity-aware learned-model PT family.

---

# 14. Family C — LTC-specific market family

5 markets.

Apply Holm5 to LTC PT values.

This preserves continuity with the previous manuscript analysis.

Do not replace prior values silently; report updated family context explicitly.

---

# 15. Family D — PE sensitivity family

5 paired market-level comparisons:

Original Transformer vs PE-Transformer.

Primary paired metric:

Brier loss.

Use paired DM raw p-values for the five market comparisons.

Apply Holm5.

Output:

`holm_family_D_pe5.csv`

Purpose:

test whether positional encoding produces systematic out-of-sample loss differences market by market.

Do not infer cross-market superiority from isolated significance.

---

# 16. DM multiplicity

Create separate Holm families for the focal DM benchmark comparisons.

Recommended:

## DM-Persistence family

8 models × 5 markets = 40 tests

## DM-200DMA family

8 × 5 = 40

## DM-Momentum60 family

8 × 5 = 40

Do not combine all 120 unless explicitly justified.

Record both:

- raw p
- benchmark-family Holm p

This makes interpretation cleaner.

---

# 17. Model Confidence Set

Run MCS separately by market.

Universe:

all non-constant forecasting strategies except Always-Up and Always-Down.

Primary MCS loss:

Brier loss.

Candidate set:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer
- Logistic
- LightGBM
- Persistence
- 200DMA
- Momentum60

Use confidence level:

`90%`

Also report sensitivity at:

`95%`

Use block bootstrap to respect temporal dependence.

Primary block length:

`20`

Bootstrap replications:

`10,000`

Seed:

`20261106`

If computationally expensive, minimum 5,000 is acceptable, but record exact count.

Report per market:

- models retained in 90% MCS
- models eliminated
- elimination order
- p-values
- 95% MCS membership

Do not call all retained models equivalent.

Use:

> statistically indistinguishable within the resolution of the MCS procedure

only if technically appropriate.

---

# 18. Superior Predictive Ability test

Run Hansen SPA separately by market.

Benchmark:

`Persistence`

Alternative model set:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer
- Logistic
- LightGBM
- 200DMA
- Momentum60

Primary loss:

Brier loss.

Block bootstrap:

- block length = 20
- replications = 10,000
- seed = 20261106

Report:

- SPA statistic
- p-value
- benchmark
- number of alternatives
- best mean loss differential model

Interpretation:

A significant SPA result means at least one alternative has superior expected predictive loss relative to Persistence under the test specification.

It does NOT identify all superior models.

---

# 19. Reduced-overlap statistical robustness

Construct fixed reduced-overlap sample:

- phase = 0
- step = 20

No phase search.

Repeat a compact subset of inference:

- DM vs Persistence
- DM vs 200DMA
- DM vs Momentum60
- PT
- descriptive MCS if enough observations

Because N is small, clearly flag low power.

Do not rely on asymptotic inference if cells are degenerate.

Output:

`nonoverlap_inference.csv`

Mandatory wording:

> Reduced-overlap evaluation lowers mechanical label overlap but does not establish statistical independence and substantially reduces sample size.

---

# 20. Statistical conclusion matrix

Create:

`statistical_conclusion_matrix.csv`

One row per:

`Market × Learned Model`

Columns:

- BA
- Macro_F1
- Forecast_Up_Rate
- PT_raw_p
- PT_Holm30_or_40
- PT_positive_support
- DM_vs_Persistence_raw_p
- DM_vs_Persistence_Holm
- DM_vs_200DMA_raw_p
- DM_vs_200DMA_Holm
- DM_vs_Momentum60_raw_p
- DM_vs_Momentum60_Holm
- GW_vs_Persistence_p
- MCS90_member
- MCS95_member
- reduced_overlap_BA
- reduced_overlap_DM_vs_Persistence_p
- Economic_CAGR_10bps
- Exposure
- Final_assessment

Suggested final assessment categories:

- no positive evidence
- isolated descriptive advantage
- benchmark-sensitive
- dependence-sensitive
- architecture-sensitive
- multiplicity-sensitive
- positive loss evidence but not directional evidence
- robust within tested framework

Use the last category only if multiple independent diagnostics support it.

---

# 21. Cross-market summary

Create:

`cross_market_summary.csv`

For each model report:

- mean BA
- mean Macro F1
- average BA rank
- number of markets BA > 0.5
- number of markets BA > Persistence
- number of positive PT raw p<0.05
- number of positive PT Holm significant
- number of DM wins vs Persistence after Holm
- number of DM wins vs 200DMA after Holm
- number of DM wins vs Momentum60 after Holm
- number of MCS90 inclusions
- number of near-constant forecast markets
- average economic exposure

Do not use this table alone to claim dominance.

---

# 22. Directional support rule

For PT:

A result is positive support only when:

- statistic > 0
- adjusted p < 0.05

A significant negative PT statistic must be labelled:

`significant negative association`

not:

`significant directional accuracy`

---

# 23. DM sign convention

If:

`d_t = loss_model - loss_benchmark`

Then:

- mean d < 0 favors model
- mean d > 0 favors benchmark

Record this prominently in methodology_notes.md.

Never reverse interpretation in tables.

---

# 24. GW sign interpretation

GW tests equality of conditional predictive ability.

Do not say:

“Model A is superior”

from a significant GW test alone.

Use the sign of the corresponding mean loss differential to describe direction.

---

# 25. MCS interpretation

Avoid:

- “all models in MCS are equal”
- “winner set”

Prefer:

> The MCS procedure did not eliminate these models at the stated confidence level.

---

# 26. SPA interpretation

Avoid:

> SPA proves model X is superior.

Prefer:

> SPA tests whether the benchmark can be rejected against the set of alternatives.

If significant, identify which model has the most favorable mean loss differential descriptively.

---

# 27. Forecast-frequency integration

For every statistically favorable result, check Forecast-Up Rate.

If:

`Forecast_Up_Rate < 0.10 or > 0.90`

flag:

`near_constant_warning = True`

Any favorable PT/DM result with near-constant forecasts requires cautious interpretation.

---

# 28. Economic interpretation integration

Do not equate predictive-loss superiority with economic superiority.

For any statistically favorable model:

report:

- CAGR
- Sharpe
- Exposure
- turnover

If exposure > 0.90 or < 0.10, explicitly note that economic outcomes may largely reflect persistent market exposure or avoidance.

---

# 29. Final figures

Create publication-ready diagnostic figures if useful:

1. heatmap of Holm-adjusted PT results
2. heatmap of DM vs benchmark outcomes
3. MCS membership matrix
4. model × market conclusion matrix

Do not create decorative figures.

---

# 30. results_report.md

Answer explicitly:

1. Which learned models survive Holm-adjusted PT?
2. Are any positive PT signals stable across markets?
3. Which models beat Persistence by Brier loss after Holm?
4. Which models beat 200DMA after Holm?
5. Which models beat Momentum60 after Holm?
6. Does PE-Transformer differ significantly from the original Transformer?
7. Does CfC offer any inferential advantage over LTC?
8. What models remain in each market's MCS?
9. Does SPA reject Persistence in any market?
10. Do reduced-overlap results preserve the main inferential conclusions?
11. Do statistically favorable results coincide with near-constant forecasts?
12. Do predictive-loss advantages translate into economic advantages?
13. Is any architecture consistently dominant across five markets?
14. Does the final evidence strengthen or weaken the manuscript's evaluation-design thesis?

---

# 31. Required final language

Use:

- apparent advantage
- statistically fragile
- benchmark-sensitive
- architecture-sensitive
- dependence-sensitive
- multiplicity-sensitive
- isolated positive exception
- no stable cross-market dominance
- did not detect

Avoid:

- proved superiority
- universally superior
- robust winner
- established dominance
- equivalent models

---

# 32. Completion audit

`completion_check.json` must verify:

- no retraining performed
- predictions loaded from frozen artifacts
- final universe unchanged
- Brier primary loss frozen before inference
- log loss secondary learned-only
- HAC lag 19 used
- DM sign convention fixed
- GW conditioning set fixed
- Holm families fixed before correction
- MCS confidence levels fixed
- SPA benchmark fixed to Persistence
- block length 20 fixed
- bootstrap seed fixed
- no favorable phase search
- no model removed after seeing results
- near-constant flags retained
- reduced-overlap caveat retained
- all null and negative outcomes retained

Set:

`status = "validated"`

only if all checks pass.

---

# 33. Repository handling

When complete:

- commit only the new Phase 3 directory
- do not modify prior Phase 1/2 artifacts
- push to GitHub main
- final completion message <= 15 lines
