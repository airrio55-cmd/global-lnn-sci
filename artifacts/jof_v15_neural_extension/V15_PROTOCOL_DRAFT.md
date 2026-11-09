# V15 Neural Rolling-Origin Extension — Protocol DRAFT

**Status: DRAFT / NOT LOCKED / NO V15 OUTCOME EXAMINED**  
**Source repository:** `airrio55-cmd/global-lnn-sci`, default branch `main`; inspected 2026-11-09.  
**V14 lock commit:** `2e60d259eb96c859ec4374541600218c8a414ffa` (do not alter).  
**V15 lock commit:** NOT SET. DO NOT START MODEL FITTING until blocking choices are resolved, code-only preflight passes, and protocol + executable code are committed.

## 1. Scope and evidentiary status

Separate *pre-specified historical neural extension* of the already observed V14 analysis, **not** a prospective or independently preregistered replication. The V14 outcome is known to the researchers. Preserve V14 files and V14.2 manuscript unchanged. Report all V15 outcomes, successes, and failures.

## 2. Frozen datasets, windows, labels

Five markets: `SP500`, `NASDAQ100`, `NIKKEI225`, `EUROSTOXX50`, `KOSPI200`. Reuse each original `artifacts/<market-folder>/market_input.csv`, `artifacts/jof_phase1_benchmark_expansion/frozen_features/<MARKET>.csv`, and `data_manifest.json` `Feature_names` for exact market-specific `COMMON_LOCAL`. Verify SHA256 against source manifest/inventory before execution; no downloading or recomputing features.

Forecast date t: target `1[Close_(t+20) > Close_t]`, ties 0. Inputs chronological feature rows `t−20` to `t−1` inclusive (20×F). A row qualifies only if forecast date falls within the split, forward label endpoint t+20 lies inside that split's last session, all inputs finite, and signal lookbacks exist. Model and StandardScaler fit using eligible training samples only, scaler fit on the union of training feature rows used in input windows and shared over the 20 lags. **No extra embargo** beyond this exact V14 label-endpoint restriction. The original frozen external feature availability caveat persists.

## 3. Rolling origins and retraining

| Origin | Initial training | Validation | Test |
|---|---|---|---|
| O1 | 2010–2012 | 2013–2014 | 2015–2016 |
| O2 | 2010–2013 | 2014–2015 | 2016–2017 |
| O3 | 2010–2014 | 2015–2016 | 2017–2018 |
| O4 | 2010–2015 | 2016–2017 | 2018–2019 |
| O5 | 2010–2016 | 2017–2018 | 2019–2020 |
| O6 | 2010–2017 | 2018–2019 | 2020–2021 |

Per market × origin × seed × base architecture/representation, train three **fresh** models: train on all eligible history up to prior year, predict validation year 1; fresh expanding train through next prior year, predict validation year 2; fresh expanding train through last validation year, predict entire two-year test with no test-period refit. Two validation years' predictions are concatenated and a single pooled AUC is computed. Honor V14 market trading calendars and exact scoring dates.

## 4. Candidate architecture and predictions

- LSTM / LTC(LNN RAW) / CfC: preserve original notebook model definitions and `ncps` version where applicable. Input shape B×20×F; 128 hidden, 0.2 explicit output dropout, two logits, positive-class probability from softmax.
- LTC LOG: **BLOCKING / UNRESOLVED**. An earlier RAW/LOG ensemble was discussed, but a source implementation or exact LOG representation has NOT been located in inspected default branch. The presence of `Log_Ret` in COMMON_LOCAL does *not* define a separate LOG input. Do not invent or silently choose LOG transformation.
- LNN ensemble by matched seed: `P_LNN_Ens,s = 0.5*P_LTC_RAW,s + 0.5*P_LTC_LOG,s`, and then ensemble probabilities across 3 seeds. Models must score exactly the same dates with the same labels. The ensemble is an input-representation variant of LTC, not a fourth independent architecture.
- Seeds: `[42,52,62]` fixed; per-seed models train from scratch. Main model predictions are **mean probabilities over seeds**; separate seed-specific diagnostics included. Compare against V14 locked Logistic Regression + LightGBM, with matched market/origin dates.

**H1 main neural estimand:** equal-weight mean ΔAUC across *three architecture families* LSTM, LTC RAW, CfC (using seed probability ensembles). LNN RAW/LOG Ensemble is **secondary descriptive** and NOT added as a fourth model into this H1 mean, because that would double-weight LTC. The V14 main statistic remains its two-model mean. Define neural/non-neural differences on matched market-origin units.

## 5. Training rule (must lock before run)

Source Phase2 protocol lists AdamW, weight decay 1e-4, max LR .005, OneCycleLR, gradient clip 1, batch 64, max epochs 100, patience 10 for validation, and final epochs 60. **V15 draft recommendation:** CE (two-logit cross-entropy); AdamW/OneCycleLR as original; **fixed 60 epochs for BOTH validation years and test**, no early stopping or performance-based checkpoint selection on evaluation windows, no threshold tuning for ROC AUC. This changes the original validation training rule, deliberately to avoid using the same observed Validation AUC/BA for model selection and estimation. This 60-epoch policy remains *proposed*, not binding until code/config review and explicit lock. No changing it after any V15 outcomes are viewed.

Set Python/NumPy/Torch seeds; deterministic algorithms strict or record and halt unsupported operations. Record CPU/GPU, library/OS versions, `CUBLAS_WORKSPACE_CONFIG` if GPU, torch and ncps hashes, model checkpoints, per-fit loss, start/end timestamps and failure messages. Record exact feature order, data SHA256 and code SHA.

## 6. Statistical reproduction (from V14; no cherry-picking)

V14 signal definitions on previous trading session t−1: Persistence 20 sessions, 200DMA of 200 closes ending t−1, Momentum60 60 sessions. Evaluate signal-outcome relation shift `S(u,s)=E_test−E_val` on exact common model-scoring dates. AUC difference `ΔAUC(u,m)=AUC_test−AUC_val`.

- **H1 primary:** Spearman `rho[S(u,200DMA), mean_m ΔAUC(u,m)]<0` for three neural architecture families; fixed group eligibility and alignment-prerequisite logic of V14; missing 30-unit pairs explicitly reported without imputation.
- **H1b:** Spearman `rho[S(u,200DMA) × mean_m corr(P_test,m,200DMA_test), mean_m ΔAUC(u,m)]>0`.
- **H2:** negative correlations for Momentum60 and Persistence signal shifts (two secondary tests).
- **H3 descriptive:** fraction of neural model × market/origin validation score–Persistence correlations <0. Three architecture families × 30 units => 90 entries if fully defined; never use naive independent-unit binomial p value. LNN Ensemble H3 separately descriptive.
- Use exactly V14's 10,000 nominal within-market permutation (seed 20261109), market-specific circular shifts (6^5), synchronized circular shifts (6), primary H1 nominal directional label, alignment prerequisite, Holm correction for *three* secondary tests H1b/H2-Momentum/H2-Persistence, and descriptive leave-one-market-out and within-market checks. These are non-exact dependent-data diagnostics; no causal or confirmatory claims.
- Additional **descriptive** comparisons: per-seed ΔAUC and H1 sign/size (do not treat seeds as independent samples), paired neural vs V14 non-neural `AUC_val`, `AUC_test`, and `ΔAUC`; matched LTC RAW vs LTC RAW/LOG ensemble. No post-hoc inferential family expansion.

**Eligibility issue:** V14 had only 28/30 evaluable H1 units in reported output due to 200DMA signal-group restrictions. Reproduce each eligibility screen exactly and report any model-specific fit failures. Do not replace missing units or tune them away.

## 7. Execution order and artifact retention

1. Verify exact source paths, code hashes, frozen data hashes; audit original RAW/LOG implementation from historical code if available. If unresolved, disable ensemble and **do not label a substitute as the legacy RAW/LOG approach**.
2. Resolve LOG input and fixed epoch policy; finalize protocol and complete executable V15 runner; code-only/synthetic preflight, no actual V15 model fits.
3. Commit source, protocol, environment and validation tests to a NEW V15 path; record SHA+UTC time as lock (not in V14 directories).
4. Execute all predeclared combinations once without result-dependent changes. Record original and any corrected bug-fix runs separately.
5. Store date-level probabilities, true labels, predicted class, eligible sample masks, fit metrics and errors; compute seed ensemble and model family summaries; publish complete output.

## 8. Execution count and interpretation

4 underlying trainable networks: LSTM, LTC RAW, CfC, LTC LOG. `5 markets × 6 origins × 3 seeds × 4 networks × 3 refits = 1,080` fits, **if LOG is defined**. Outputs span 4 evaluated model variants × 5 × 6 × 3 = 360 model-unit-seed combinations; independent market-origin clusters are at most 30 and temporally/cross-sectionally dependent. If LOG cannot be sourced, run only a separately relabeled 3-model design after changing/locking protocol; never pretend 1,080 fits took place.

## 9. Blocking decisions / signoff

- [ ] Exact LOG representation + transformations + frozen source code or honest new-definition label
- [ ] Fixed 60-epoch policy confirmed as pre-result choice
- [ ] Confirm date matching and feature indexing with synthetic tests
- [ ] Confirm whether H1 H1b shared score dates require intersecting model-successful dates (define failure treatment with V14 complete-case logic)
- [ ] Commit lock and UTC time before any outcomes

No fitting, no claimed V15 statistical findings, no change to V14/V14.2 while this draft is open.

## 10. STEP 2 continuation — user clarification (2026-11-09)

The researcher has clarified: **RAW denotes the original input variables; LOG denotes a log-return-based feature representation.** This removes ambiguity about the *conceptual* ensemble branches, but does not yet specify the exact LOG columns, their lagging, or transformation of non-price covariates. Existing frozen `COMMON_LOCAL` already includes `Log_Ret`; this alone does **not** produce a distinct LOG representation. To avoid inventing a historical implementation, the V15 runner requires an explicit ordered list of existing frozen log-based features *per market* (`V15_CONFIG_TEMPLATE.json` → `log_columns`). LOG columns must be verified against the historical definition. No new features are calculated online, no speculative log transformation is performed, and RAW/LOG valid-date masks must coincide with V14.

The runner has been written to permit locked execution with an explicit config and Git SHA/hash inventory. It refuses to train unless config status is `LOCKED`, 60 fixed epochs and 3 seeds are present, Git tracked files are clean, HEAD matches the lock record, and all specified locked hashes match. This is **not a claim that the protocol is locked now**. It remains draft until those conditions are met. If exact historical LOG columns cannot be recovered, any new representation must be honestly labeled a *newly specified LOG-feature variant*, not a reconstruction of an earlier ensemble.

Original V14 non-neural method remains a comparison baseline. V15's fixed 60 epochs is a deliberate deviation from V14-era neural validation early stopping, to prevent evaluation-window outcomes choosing their own checkpoint. Equal epoch counts are not necessarily equal optimization exposure across expanding datasets; disclose this limitation.