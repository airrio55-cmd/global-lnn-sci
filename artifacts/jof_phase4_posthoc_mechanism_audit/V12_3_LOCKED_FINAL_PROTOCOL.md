# Journal of Forecasting v12.3 — final post-hoc audit protocol (LOCKED)

Date: 2026-11-08 (Asia/Seoul). Scope: exploratory/post-hoc diagnostics only. This document locks the final additional analyses before inspecting new results. Preserve all Phase 1–4 frozen predictions and model selection. No retraining, retuning, further choice of controls, or hypothesis-search based on outputs.

## Six fixed checks
1. Validation (2019–2021) score–signal alignment: for five markets and eight final selected learned architectures, compute Pearson r between ensemble-mean probability scores and Persistence, 200DMA, Momentum60 signals using the same common prior-session (t−1) information cutoff as testing. Also compute test alignment with the exact same implementation. Report all 5×8×3 cells, and summaries, including missing-data issues.
2. Three-period 15 market–signal outcome relations: training 2010–2018, validation 2019–2021, held-out 2022–2025, for all five markets and the same three signals. Define effect ΔP=P(y=1|signal=1)−P(y=1|signal=0); preserve the original 20-day forward target construction and correct endpoint exclusions; do not invent unavailable training labels. Report all three periods even if any cannot be reconstructed.
3. Calendar audit: verify model prediction date, signal source date preceding forecast origin, outcome date, exchange holiday gaps, and test/validation sample intersections; report exact exclusions and mismatches.
4. Stratified held-out AUC by 200DMA=0/1, all five markets × eight architectures; publish n, positives, negatives, unstratified AUC, and strata AUC. For dependence-aware CI use paired circular moving-block bootstrap (B=2000; seed 20261108; L=20), resampling common dates across models and preserving signal/outcome pairing. Undefined-AUC resamples excluded with counts disclosed.
5. Sensitivity: repeat mean model-score/trend-signal correlation CIs and stratified AUC CIs with L=20,40,60 (B=2000; seed 20261108; 95% percentile). Treat clustered architecture averages as descriptive (five markets), not independent cross-sectional replication. Record CI for each block size, without selecting best size.
6. Validation selection optimism: include all validation candidate losses/configurations from frozen model-selection manifest, with selected versus nonselected ROC AUC distributions and count, and explain that validation AUC is selection-conditional; do not label it external generalization. If exact matching predictions are missing, report an explicit unverified item rather than substituting non-comparable candidates.

## Interpretive guards
- Reporting all outcomes is mandatory, including unfavorable/null results. The previous 6/10 excludes Persistence; always display 15/15 alongside subset 10/10 and give methodological reason.
- Correlation of model score with input-derived trend signal does not identify feature importance or causal weights. Test stratification and regression are descriptive conditioning, not causal mediation tests. Mean ROC AUC differences may involve selection optimism, cohort alignment and sample composition.
- Do not assert a single causal mechanism, market-specific significance after multiplicity correction without running it, or 'almost all due to trend' from stratified AUC alone.
- This lock applies to the final audit only. Any new questions are deferred to future revision and separately identified, not incorporated into this locked round.

## Immutable source
Phase 1 14bebac13d25c030226cee27691198b794855c9d; Phase 2 0568f9794909308076f20b78a2e6bce9b8454540; Phase 3 6756e3b5de716871db6460c09ed2c14e51e48fbe; Phase 4 v12 extension b56371c73af5d3c46a4bafa8ca2724604bbf8f24.
