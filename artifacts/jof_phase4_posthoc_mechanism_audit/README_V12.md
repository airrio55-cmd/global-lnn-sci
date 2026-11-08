# JOF v12 temporal-instability extension

Date: 2026-11-08 (Asia/Seoul)

This extension belongs to the existing Phase 4 post-hoc mechanism audit. It uses only frozen 2019-2021 validation predictions, frozen 2022-2025 held-out predictions, and the original market inputs. No model is retrained, reselected, retuned, or refit for the v12 mechanism diagnostics.

## New diagnostics
- Validation-to-test changes in 200DMA and Momentum60 outcome relations at the common t-1 information cutoff.
- Independent circular moving-block resampling within validation and test (block length 20; 5,000 deterministic resamples) for the period difference in Delta P.
- Validation-to-test ROC-AUC degradation and a descriptive score-trend alignment diagnostic.
- Ten-bin descriptive Brier decomposition.
- Calibrated Brier versus climatology DM/HAC sensitivity at lags 19, 40, and 60, with Holm40 correction.

## Main findings
- Six of ten 200DMA/Momentum60 market-signal relations reverse sign from validation to test.
- Four period-difference 95% block intervals exclude zero; all four are the two signals in the S&P 500 and NASDAQ-100.
- Mean learned-model ROC AUC falls from 0.646 in validation to 0.475 in held-out test.
- Recalibration strongly reduces reliability error but leaves resolution near 0.01.
- No calibrated model-market case is significantly better than climatology at HAC lags 19, 40, or 60 after Holm40.
- These diagnostics are interpreted as evidence consistent with temporal instability contributing to held-out ranking failure, not as causal proof of a structural break.

The full model-level table is reported in Supporting Information. The repository continues to preserve all earlier Phase 1-3 frozen artifacts and the original Phase 4 audit.
