# JOF Phase 4: post-hoc evaluation-design mechanism audit

Date: 2026-11-08 (Asia/Seoul)

This directory contains a post-hoc mechanism audit created after advisor review of the frozen Journal of Forecasting manuscript analysis. It does **not** retrain models, reselect architectures/losses/thresholds, or modify the Phase 1-3 frozen test predictions.

## Purpose
The audit asks which evaluation choices materially change the apparent forecasting conclusion while holding the saved prediction layer fixed wherever possible.

## Components
1. **Common-cutoff rule timing**: Persistence, 200DMA, and Momentum60 are recomputed at the learned models' t-1 forecast-origin information cutoff. The original t-based rules remain preserved in Phase 1/3 artifacts.
2. **Validation-only probability recalibration**: a monotone sigmoid map is fitted using 2019-2021 validation ensemble-mean probabilities only, with L2 slope stabilization (lambda=1). If the unconstrained slope is negative, the monotonicity-constrained solution is the zero-slope validation-prevalence constant. The mapping is applied unchanged to 2022-2025 test probabilities.
3. **Calibrated proper-score inference**: calibrated Brier loss is compared with 2010-2021 climatology by two-sided Diebold-Mariano tests using HAC lag 19 and the Harvey-Leybourne-Newbold correction. All 40 learned model-market comparisons form one Holm family.
4. **Dependence audit**: paired circular moving-block bootstrap intervals for Delta BA versus common-cutoff Persistence use block lengths 20, 40, and 60 and 2,000 deterministic resamples per specification.

## Main audit findings
- Common-cutoff rule timing changes BA by at most 0.0087.
- Learned-model wins are 24/40 versus common-cutoff Persistence, 11/40 versus 200DMA, and 9/40 versus Momentum60.
- Validation-only recalibration reduces mean learned-model Brier loss from 0.391 to 0.269.
- 39/40 calibrated cases remain numerically worse than climatology; 6/40 deficits remain significant after Holm40; no calibrated case is significantly better.
- The sole numerical calibrated improvement is Nikkei 225 Logistic Regression (Delta Brier about -0.00015; raw DM p=0.780; Holm40 p=1.000).
- Mean test ROC AUC is 0.475; only 4/40 cases exceed 0.55.
- No positive learned-model Delta BA versus common-cutoff Persistence has a 95% bootstrap interval above zero for all block lengths 20, 40, and 60.

## Frozen source lineage
Phase 1 frozen commit: 14bebac13d25c030226cee27691198b794855c9d
Phase 2 frozen commit: 0568f9794909308076f20b78a2e6bce9b8454540
Phase 3 frozen commit: 6756e3b5de716871db6460c09ed2c14e51e48fbe

The Phase 4 audit is explanatory and post-hoc; it is not represented as prospectively protocol-locked confirmatory evidence.
