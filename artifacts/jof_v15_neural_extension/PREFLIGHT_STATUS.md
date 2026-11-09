# V15 Read-only preflight / integration checkpoint

**Status: NO LOCK; NO FIT; NO V15 PERFORMANCE RESULTS.**

Added `v15_preflight_readonly.py` to compare frozen raw/feature hashes, all 60 V14 market-origin-period scoring-date groups, RAW/LOG 2-feature finite dates, and train label endpoints. Run on a full local checkout (without torch or ncps):

```bash
python artifacts/jof_v15_neural_extension/v15_preflight_readonly.py --repo .
```

This preflight does not calculate AUC or fit estimators. Passing means data alignment and time boundary checks passed; it does **not** certify original real-time external feature availability.

**Historical model identity:** archived KOSPI200 JKSCI manuscript documents two CfC branches, RAW [Log_Ret, Foreign_Net, Nasdaq, SOX, Disparity], LOG [Log_Ret, Disparity], W=20 and 50/50 probability average. V15's intended cross-market LOG [Log_Ret, Disparity20] and RAW frozen COMMON_LOCAL are *new adaptations*. Retain the historical-vs-V15 distinction and never assert byte-identical historical reproduction.

**Execution remains BLOCKED:** full neural runner is still in a downloadable ZIP, not fully committed here; 60-epoch CE settings await review; torch/ncps smoke tests and actual-data preflight are not yet performed; frozen feature/as-of availability must be disclosed. No workflow here trains V15.

**Lock criteria:**
- Commit and inspect every V15 runtime file and hashes on dedicated branch.
- Run synthetic tests and above read-only data check; retain stdout and version inventory.
- Check ncps topology, deterministic settings and CPU availability with random synthetic tensors only.
- Explicitly approve epoch/loss/three seeds and code, then record immutable lock SHA in separate lock record.
- Only then enable historical fits using a separate opt-in command.

## Read-only GitHub-content cross-check — 2026-11-09

Source: GitHub frozen market CSVs and frozen Phase1 feature CSVs, read through the repository connector. All five markets were examined using the 201-index minimum, W=20, H=20, feature-finiteness filter, and **two separate annual validation folds** with yearly label endpoints, plus the single two-year test fold.

- SP500: 12/12 market-origin-period groups, V14 scoring dates exact; LOG [Log_Ret, Disparity20] finite on all RAW eligible dates.
- NASDAQ100: 12/12, same.
- NIKKEI225: 12/12, same.
- EUROSTOXX50: 12/12, same.
- KOSPI200: 12/12, same.
- **Total 60/60 groups exact; zero LOG-window missingness on V14 RAW dates.**

This was an independent, read-only JavaScript content audit in the connector, **not execution of the Python preflight on a full local checkout**. Input SHA256, installed torch/ncps, GPU determinism, feature publication times, and full locked runner are still pending. No labels used for accuracy/AUC; no training or V15 outcome analysis.

The Python `v15_preflight_readonly.py` was amended to apply annual validation cutoff rules and requires execution in the complete repository before lock.
