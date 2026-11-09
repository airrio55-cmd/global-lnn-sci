# V15 draft — historical CfC ensemble source recovered

**Status:** DRAFT, NOT LOCKED, NO V15 TRAINING. The V14 locked scripts, output files, and manuscript are unchanged.

Earlier Korean JKSCI manuscript and Figure 1 explicitly define KOSPI200 **CfC** ensemble: RAW [Log_Ret, Foreign_Net, Nasdaq, SOX, Disparity] (5 variables), LOG [Log_Ret, Disparity] (2 variables), score average 0.5/0.5 and W=20. The previous assumption of an LTC ensemble was incorrect.

V15 proposes an **adapted, new cross-market** CfC ensemble, using the frozen market-specific COMMON_LOCAL columns for RAW and [Log_Ret, Disparity20] for LOG. The latter must not be described as reproducing the original two-feature Disparity series. The original notebook defines Log_Ret = diff(log(Close)) and Disparity20 = Close / rolling_mean_20(Close) - 1. Do not regenerate or refresh frozen input data; verify its hashes instead.

The V15 architecture comparison is LSTM, LTC RAW, CfC RAW, and the diagnostic CfC RAW/LOG ensemble. Trainable branches: LSTM RAW, LTC RAW, CfC RAW, CfC LOG. Four fits per market/origin/seed/fold, 1,080 fits in the full planned study. V14 held-out comparison and H1-H3 remain fixed in the draft protocol.

**Important:** Complete Python runner sources are in the separately delivered V15 package and are NOT YET entirely present in this GitHub branch. Do not run or lock this branch. Preflight with real market CSVs, ncps runtime tests, and independent review are still pending. CE loss and 60 fixed epochs are proposed V15 settings (the historical KOSPI200 ensemble used a different FocalLoss setting). GitHub branch is not a validated executable release.

Blocking criteria:
1. Review frozen Disparity20/Log_Ret feature formula provenance, as-of timing and input hashes.
2. Commit and review complete Python runner/tests, validate matched V14 RAW scoring dates in 60 groups.
3. Pass torch/ncps deterministic smoke tests without performing the historical experimental fit.
4. Explicitly approve 60 epochs + CE and lock an immutable commit; write external lock SHA/inventory.
5. Only after these steps may the full rolling-origin neural experiment begin.
