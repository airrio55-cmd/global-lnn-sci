# V15 neural extension: results archive

This directory archives the outputs of the V15 neural rolling-origin extension. **It produces no new results.** No model was retrained and no statistic was recomputed when this archive was made.

## Provenance
- Protocol, configuration and input lock: commit `d866841eeb87c63f42bd10240c7acc06ee7dbe49` (2026-11-09 10:19:02 UTC), which precedes all training. This results branch is built on that lineage.
- V15.1 recovery preparation: commit `c28ccde593d190384bfe5e10278b2ea25b923c38` (2026-11-10 04:49:30 UTC) on branch `v15-runtime-transfer-d866841`. It was written after the host shutdown at 04:12:32 UTC and before any AUC or hypothesis statistic was computed.
- Source package: `V15_neural_results_20261115_155330_KST.zip`, 347,874,734 bytes, SHA-256 `97bf958ab65091cf05964ca5c57a1903db136fc07a928dd95c214f2ab3f84f4e`.

## Integrity checks performed when archiving
- All 4,437 files listed in `PACKAGE_MANIFEST.json` match their recorded SHA-256 values; none are missing.
- `PACKAGE_MANIFEST.json` reports 1,080/1,080 logical jobs complete, with validation `PASS` (V15.2).
- The 71 files in the source package's `03_locked_payload/` are byte-identical to the same paths at the lock commit `d866841`. They are therefore not duplicated here.

## Contents
- `01_analysis/`: hypothesis statistics (`v15_results.json`), unit-level, seed and model tables, the V15.2 analysis and check scripts, `change_record.json` and `validation_report.json`.
- `02_training_run/`: per-fit metadata, predictions and training losses for all 1,080 fits; pooled predictions; execution configuration; logs; and the V15.1 recovery operations.
- `*.partial.csv` files are **interruption records**: outputs present when the original run stopped. They are kept unchanged on purpose and are not used in any analysis.
- Historical `FAILED` logs record the original tolerance-check failure that V15.2 corrected (Supporting Information S21.2).
- `03_lock_records/`: lock and authorization records.

## Model checkpoints
The 1,080 `checkpoint.pt` files (state_dicts, about 418 MB) are left out of git. They are distributed in the unmodified source package, attached as a release asset to tag `v15-results-20261115`. `CHECKPOINTS_SHA256.txt` lists the SHA-256 of every checkpoint at its original relative path.
