# V15 code audit and integration report

Date:2026-11-09. Target branch:v15-neural-extension-step3-draft. Starting commit:f6cab21. This preparation commit is **not a protocol lock**. No neural fit, optimizer, gradient/backward, AUC computation or1080-fit run was performed. No V15 findings are claimed. Work used a separate Git worktree; main, V14 original outputs and V14.2 manuscript are protected.

## Fixed draft design

LSTM RAW, LTC RAW, CfC RAW, CfC LOG are the four trainable branches. CfC_ENSEMBLE is a fifth derived output, computed50/50 within matched seed/date and then averaged across seeds. LOG uses exactly existing Log_Ret and Disparity20 in that order for all five markets. This is a new adaptation, not an exact historical KOSPI200 replication. Seeds42/52/62, CE and60 epochs agree across config and runner; the missing explicit config loss field was added. CE/60 fixed validation epochs differ deliberately from the older patience10/max100 neural validation and historical KOSPI focal loss. No early stopping or threshold tuning is introduced.

V14 O1–O6 training, annually refit validation years, single two-year test, H=W20, minimum index201, label cutoff rule and exact common scoring dates are preserved. There is no extra embargo or refit during a test period. Scalers fit the union of rows in eligible training windows, never all dates or all validation rows.

## Findings and repairs

1. **Conflicting protocol/docs:** obsolete unresolved LOG/LTC-ensemble/ZIP claims removed. Corrected output count: four fitted branches produce five evaluated variants including diagnostic LOG;450 model-unit-seed outputs if all are counted.1080 remains the future fit count, not the number of independent observations.
2. **Missing declared loss:** config now explicitly CE, still DRAFT and both training/analysis permissions false. Shared validation rejects changed H/W,seeds,epochs,device,features,ensemble and H1 architecture scope.
3. **Weak representation/lock gate:** the provenance gate is now called by runner lock verification and covers the complete required data/runtime source inventory. Added config hash coverage, clean immutable commit and external lock-record requirements. Filling draft inventory is not a lock. Audit-only provenance validation is separately available.
4. **Insufficient fit retention:** future-only runner now saves state_dict, per-epoch training loss, scaler state/used-row masks, train/evaluation dates, tensor hashes, evaluation probabilities/labels, environment/config and failure details. Each branch/stage/seed gets a unique folder. Completion requires exactly1080 fits. No failure is silently skipped. These training paths were statically reviewed, not executed.
5. **Entry-point/output safety:** draft blocks direct runner/fit/analysis entrypoints; AUC requires separately enabled analysis permission, immutable lock and a complete1080-fit prediction manifest. Future outputs must be outside protected checkout and cannot overwrite an existing directory. Corrected literal newline writes and missing --out handling. Disabled repository bytecode writes before local imports so a clean-checkout gate does not block itself by creating __pycache__.
6. **Data/scaler tests:** consolidated V14 reference reuse, hash verification, RAW Close/index integrity, exact feature order/formulas and all90 train label boundaries. Added train-only scaler equality and target/future perturbation tests; LOG cannot change the date universe.
7. **Analysis structural completeness:** reject wrong/extra dates per every model/seed, duplicate/null keys, non-binary/inconsistent labels/signals and mismatched50/50 ensemble. Former global model/seed set checks could miss incomplete model/date series. No AUC was needed to test these checks.
8. **H1 alignment interpretation:** an unmet alignment prerequisite now prevents an H1-support label. Missing30-unit eligibility remains explicit, not imputed. Added evaluable alignment count. Secondary undefined Holm3 fields remain explicit nulls.
9. **Missing diagnostics:** added separate ensemble H3; per-seed validation/test/ΔAUC for all five variants; paired V14 per-model validation/test/ΔAUC plus neural/non-neural means; matched CfC ensemble-vs-RAW comparisons for all three AUC quantities. No statistical outcomes calculated in this audit.
10. **Forward-only coverage:** previous generic8-feature test expanded to each actual market dimension and the2-feature LOG branch for all three seeds. Audited topology, same-seed parameter and output equality against original notebook definitions.

## Static hypothesis review — no AUC or inference executed

- **H1:** equally weights only LSTM,LTC_RAW,CfC_RAW after seed probability averaging, then correlates200DMA effect shift with mean ΔAUC. CfC ensemble/LOG never double-weight CfC. Alignment≥16/30 negative test correlations is required for support language. At most30 dependent market-origin units; current input/signal eligibility is28/30.
- **H1b:** mean test alignment multiplied by200DMA effect shift; positive directional alternative, retained exactly.
- **H2:** Momentum60/Persistence shifts, negative alternatives. Only H1b and these two form Holm3; no expanded post-hoc family.
- **H3:** negative validation probability–Persistence correlation counts among90 planned architecture-unit pairs, with finite denominator; ensemble separately descriptive. No naive independent binomial p.
- **Permutation/rotation:** reuse original V14 functions unchanged (10000 nominal within-market permutations,seed20261109,actual market rotations and6 synchronized shifts). They are non-exact dependent-data diagnostics. V14 removes nonfinite rows before rotating, so6^5 is not the actual total with incomplete blocks. This preserves the original code rather than silently changing its missingness behavior: current eligible block sizes give5×5×6^3=5400. This limitation must remain in later reporting.
- **Seed stability:** three seeds are paired sensitivity analyses, never independent sample-size inflation. Individual variant AUCs and three-family seed H1 are planned, not computed.
- **V14 comparison:** both LogisticRegression/LightGBM remain unchanged. Future analysis pairs exact market/origin dates before validation/test/ΔAUC comparison and reports CfC RAW/ensemble on the same units. Baseline30-key uniqueness and completeness are checked.
- **Failure policy:** an incomplete fit or date series blocks analysis rather than introducing a new favorable model-successful intersection. Original signal-group missingness is retained and disclosed.

## Executed tests and evidence

| Check | Result |
|---|---|
| Original V14/Phase1 input checksums | pass, all five markets |
| Scoring-date groups |60/60 exact |
| Individual annual validation/test folds |90/90 exact cutoff checks |
| LOG finite on all RAW-eligible train/evaluation windows | pass |
| Log_Ret/Disparity20 frozen formula comparison | pass,1e-12 tolerance |
| Train-only scaler row union |90 folds pass |
| Future and target-row perturbation |90 folds pass, exact unchanged tensors/scalers |
| Forward-only topology and CPU determinism |60/60 pass, equal original parameters/outputs |
| Regression tests |6 pass |
| Fit/backward/optimizer/AUC calls under active traps |0/0/0/0 |
| Protocol lock created | no |

Logs and machine-readable evidence are in audit/. Formula verification only compares existing values; it does not replace frozen features. Synthetic malformed-input tests never calculate performance. The historical-data preflight calls records(preflight=True), so it does not compute target labels or AUC. StandardScaler.fit estimates normalization only, not a predictive model; this distinction is explicit in the evidence.

## Remaining risks and lock readiness

**Audit passes; protocol remains unapproved and unlocked.** It is ready for a separate lock review after explicit authorization and environment-version decisions, not for automatic locking or execution.

- Unknown historical external-variable release timestamps/vintages cannot be independently certified from frozen daily files. Original causal alignment rules are inherited, not newly verified real-time feeds. All five source leakage audits are included in provenance inventory.
- KOSPI200 uses its user-authorized empirical observation calendar; no claim that earlier XKRX differences are proven missing observations. No new dates or values were fabricated.
- Original V14 environment was Python3.12.16/numpy2.2.6/pandas2.2.3/sklearn1.6.1/LightGBM4.6.0. The audited current CPU environment is recorded separately and differs. Original V14 outputs were not recomputed to force agreement. Resolve and explicitly record the intended V15 environment before a future immutable lock.
- No60-epoch optimization, checkpoint replay after fitting, full1080-job orchestration or AUC/H1–H3 runtime was executed. These cannot be represented as tested by static review/forward-only checks. Any later bug fixes must retain old attempts and reauthorize protocol-affecting changes; no result-driven tuning.
- GPU was not audited; CPU-only configuration is enforced. Failure logs do not constitute a completed experiment, and the current runner intentionally refuses overwrite/resume of an existing output directory.
- Temporal and cross-market dependence and28/30 signal eligibility remain inferential limitations. No independent replication claim or causal interpretation is appropriate.

## Modified/new files

Updated: V15_CONFIG_DRAFT.json, V15_PROTOCOL_DRAFT.md, README_STEP3.md, PREFLIGHT_STATUS.md; v15_locked_runner.py, v15_analysis_draft.py, v15_preflight_readonly.py, v15_representation_gate.py, v15_smoke_no_fit.py.

Added: v15_common.py, v15_audit_only.py, test_v15_audit.py, this report, audit logs/results and preparation/source manifests. No file outside artifacts/jof_v15_neural_extension is included in the preparation commit.
