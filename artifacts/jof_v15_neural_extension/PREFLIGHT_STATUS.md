# V15 audit checkpoint — 2026-11-09

**DRAFT / NO LOCK / NO FIT / NO AUC.** Complete code is now integrated in this branch; the older statements that runtime sources remain in a ZIP are superseded.

Executed in the isolated worktree with the existing CPU environment:

- All60 V14 market/origin/period scoring-date groups: exact match.
- All90 annual-validation/two-year-test refit folds: training label endpoints within cutoff; no test-period refit.
- Both RAW/LOG: finite on every required input window; no LOG-only date expansion.
- Input hashes match original V14 inventory and frozen Phase1 manifest.
- Existing Log_Ret and Disparity20 values match their documented price formulas within1e-12 tolerance; source files were not recalculated or modified.
- All90 fold scalers: train-only window-row union; target-row and future perturbation leaves training tensors/scalers and first evaluated window exactly unchanged.
- 60 synthetic forward checks: five real feature dimensions ×four branches ×three seeds; logits finite, bitwise deterministic on CPU, and parameter/output identity with original notebook implementations.
- Six regression tests passed, including malformed/missing predictions, incorrect50/50 ensemble, changed settings, corrupted inventory and blocked fit/AUC entrypoints.
- Unified audit additionally trapped optimizer construction, backward, sklearn/LightGBM fit and AUC calls: all zero.
- Price/feature-only200DMA group eligibility remains28/30 units; no AUC or signal-outcome statistics computed.

Evidence: audit/preflight_results.json, audit/forward_results.json, audit/execution_boundary.json, audit/regression_tests.log and audit/preparation_manifest.json.

This does not certify unknown real historical publication times or vintages. It does not validate60-epoch numerical stability, GPU execution or the complete statistical analysis runtime, which were deliberately not executed. Current versions differ from the original V14 non-neural execution; they must be explicitly reviewed before any future lock. Details and static analysis findings are in AUDIT_REPORT.md. The code-review commit must not be cited as a protocol lock.
