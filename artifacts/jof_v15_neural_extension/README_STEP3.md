# V15 STEP 3 integration status — DRAFT, not locked

Branch: `v15-neural-extension-step3-draft`

The V15 protocol and blocked configuration are staged here. **No neural experiment has run and no V15 protocol has been locked.** The frozen V14 source, V14 results, and V14.2 manuscript must not be changed.

## Research audit

RAW = original frozen COMMON_LOCAL input variables. LOG = log-return-based variables, **not** merely taking a convenient subset of COMMON_LOCAL. The default branch does not contain a verified pre-existing RAW/LOG LNN Ensemble implementation. Frozen features contain `Log_Ret` and, for some markets, `DXY_LogRet1` and `DXY_LogRet5`; their presence does not determine the old LOG branch.

## Blocking steps before lock

1. Verify and record the old LOG feature-generation formula, all input columns per market, date alignment, and input hashes. If irretrievable, label it a newly specified LOG variant, not reproduction.
2. Copy the tested V15 STEP 3 Python code package into this folder; review all imports and link data manifests.
3. Run synthetic preflight, then read-only repository preflight matching all 60 V14 market-origin-period scoring-date groups. **Do not fit models** during preflight.
4. Confirm fixed 60 epochs and environment including torch/ncps versions. Verify CPU reproducibility and original topology.
5. Commit all source and immutable inputs, create a separate lock record with commit SHA + SHA256 inventory, then and only then allow full execution.

**Present repository scope:** draft protocol, config, this integration status. The full Python package is available separately as a downloadable artifact, not yet committed to this branch. Do not claim this branch is executable or ready for lock.
