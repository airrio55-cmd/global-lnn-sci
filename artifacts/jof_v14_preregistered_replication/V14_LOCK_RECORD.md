# V14 pre-execution lock and price-only audit

**Binding lock commit:** `2e60d259eb96c859ec4374541600218c8a414ffa`.

**UTC Git author time:** `2026-11-08T23:02:43Z` (KST 2026-11-09 08:02:43).

The lock commit atomically introduced both `V14_PREREGISTERED_ROLLING_ORIGIN_PROTOCOL_LOCKED.md` and `run_v14_locked.py`. Their blob SHA-1 identifiers in Git are `02a229c3d64ef148862d7068f52cd01f7bcf0b52` and `8105888cae35ea46f344deb90dd604499a1216d1`, respectively. These files are binding; this separate note only records the commit and reproducibility context.

The original frozen Close series was used before lock **only to count 200DMA=0 and 200DMA=1 dates**, filtering forecast dates and target **endpoint dates**, without inspecting labels, model outputs, AUC or E. See `v14_price_only_200dma_group_inventory.csv` for all 60 market × origin × period counts. SP500 O1 Validation: 6 vs 478; NASDAQ100 O1 Validation: 2 vs 482. In this price-only screen, at most 28/30 H1 units pass the 20/20 signal-group minimum. Final model-eligible counts may be lower because finite feature-window restrictions apply.

Repository tree name scan before lock found no existing V14 rolling-origin result paths; does not rule out work outside the repository. **No V14 estimator was trained and no V14 labels/AUC/E values were calculated in the lock preparation.** Code execution, including its preflight feature-mask calculation, has not yet been performed in this environment. The source was inspected for protocol consistency, but Python syntax compilation and end-to-end test are not yet independently certified; any subsequently found bug must be disclosed with both original and corrected versions, as prescribed in the lock.

Baseline manuscript remains v13.4, unchanged by this lock.
