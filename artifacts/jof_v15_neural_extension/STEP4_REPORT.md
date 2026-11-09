# V15 STEP4 final verification and protocol freeze

**All allowed pre-lock checks passed.** No actual neural training, optimizer/backward, AUC or H1–H3 execution occurred. V15.0 is frozen by the payload commit identified in V15_LOCK_RECORD.md/json. The branch tip may be a record-only descendant; use the payload SHA, not the moving branch name. Current external records authorize neither training nor analysis.

## PASS/FAIL checklist

| Check | Result |
|---|---|
|STEP3 original audit/code/input hash chain|PASS|
|Syntax/import,all V15 modules|PASS|
|Fixed4branches+derivedensemble,seeds42/52/62,CE60,H=W20|PASS|
|V14 annual validation/test refit plan and scoring dates60groups|PASS|
|Split label endpoints/train-onlyscalers/futureperturbation90folds|PASS|
|Same-seed CPU forward60checks|PASS|
|Untrained temporary checkpoint save/replay20checks|PASS|
|H1/H1b/H2/H3 static scope and gates;no inference executed|PASS|
|Unique1080job manifest:720validation+360test|PASS|
|Environment versions+code/binary attestation|PASS|
|Six regression tests,including draft no-fit/AUC guards|PASS|
|V14/manuscripts/main preservation|PASS|

There are no unresolved critical failures within the explicitly authorized no-training scope. Training convergence,full1080-job runtime and end-to-end AUC/statistical execution were intentionally not tested and are not claimed as validated. Forward/restore fixtures used random initialization and were removed.

## Frozen environment and hashes

| Component | V15 audited version | Original V14 non-neural version |
|---|---|
|Python|3.12.14|3.12.16|
|PyTorch|2.14.1+cpu|not used in V14 non-neural experiment|
|ncps|1.0.1|not used in V14 non-neural experiment|
|numpy|2.5.4|2.2.6|
|pandas|3.0.6|2.2.3|
|scikit-learn|1.9.1|1.6.1|
|LightGBM|4.7.0|4.6.0|

Exact pins for118 installed distributions are in requirements-v15.lock.txt. Full hashes of critical package Python source and native binaries, including bundled numerical libraries where present, are in V15_ENVIRONMENT.lock.json. Python binary SHA256: `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`.

Version differences can change parsing/dtypes,scaler rounding,random or numerical behavior. Exact date/missingness/scaler and original-model forward tests pass in this V15 runtime, but this is not a claim that reexecuting V14 with new versions reproduces its predictions. Original V14 results were not rerun or altered. Its fixed existing non-neural results remain the comparison. The intended V15 version stack is now explicitly frozen, rather than silently adopting V14 versions.

Environment file SHA256: `c8971b9951a2796b7d7dcd78b86851c110df7e35cc18b253fd191caae1fcaf1f`. Requirements SHA256: `a5decc552ccaaaa04f9a6e6f1aeeb194dfd96b927928922a414a2fce556c3ddd`. All source/data/config/evidence file hashes are bound by V15_LOCK_PAYLOAD.json.

These are installed-runtime fingerprints, not wheel-download hashes. No fresh installation,container rebuild or cross-hardware bitwise reproduction was tested. Future execution must match the audited interpreter/packages/code/binaries; merely satisfying version numbers is insufficient. Preserve the audited runtime or separately obtain matching artifacts.

## Execution feasibility and resources

The plan has1080fits,720validation and360test; no extra fit for ensemble. Manifest has1080unique fit IDs and source date hashes. Estimated optimizer steps:1,431,360. The runtime plan is checked against this file before a future authorized fit.

A serial two-thread run has measured forward-equivalent work of29.0hours. Applying a declared,uncalibrated3–8× factor for autograd/backward/optimizer and I/O gives approximately87–232hours (3.6–9.7days). This is a planning range,not a completion guarantee or a measured training benchmark. Actual LTC backward costs,CPU contention,failures and environment lifetime can move it outside this range.

Serialized state_dict sizes measured on untrained synthetic fixtures imply345.0MiB for all1080model states. This excludes retained optimizer state (not promised). Reserve at least3GiB per complete run for states,date probabilities,partial/finalCSV,loss histories and metadata,plus extra for failed attempts/backups. Expected per-fit evaluation rows total334,968. No actual experiment checkpoint exists.

RAM reservation:8–16GiB per serial job. Observed audit peak was0.75GiB without autograd; it is not training memory. A retained64×128×128 float32 tensor across20steps×6LTC ODE unfolds is0.46875GiB; multiple retained intermediates and model/workspace overhead motivate the conservative reservation. Backward memory was not measured. Current cgroup quota is400000 100000; concurrency is not benchmarked and is not the default.

Technical prerequisites for a later CPU run passed,but **execution is not authorized by STEP4**. Keep both external authorization flags false. A separate explicit run authorization can change only the external authorization record and CLI opt-in,not frozen payload bytes. No task was scheduled or detached for training.

## Remaining risks

- Historical daily source publication timestamps/vintages were not independently certified; original causal availability rules are inherited. KOSPI200 keeps its user-approved empirical observation calendar; no missing-date fabrication.
- Fixed60epoch optimization,possibleOOM,fullcheckpoint replay after real training,and full AUC/H1–H3 runtime remain unexecuted. Any later bug fix belongs in a new version with preserved failed attempts.
- Only the frozen Linux CPU stack is supported. No GPU,other-version or cross-hardware deterministic equivalence was established.
- V14 outcomes were already observed; this is a historical pre-result neural extension,not independent prospective preregistration. At most30 dependent market-origin units and28current signal-eligible H1 units remain inferential limitations.
- Git SHA and file hashes identify immutable content; remote refs are not claimed to be administratively deletion-proof. Preserve the lock SHA/record independently.

## Lock mechanics and changes

The payload commit is made first; its exact SHA and UTC are added in a record-only descendant because self-referential commit SHA is impossible. V15_LOCK_RECORD.md/json,post-lock verification and the immutable lock tag identify that anchor. Verification checks ancestry,clean checkout,anchor and current file hashes,complete inventory,and exact environment. Training/analysis require separate external authorization and completion gates.

Do not rerun tests into frozen step4/ or audit/ directories after freeze; use external output. Post-lock code,data,config or environment changes require a separately versioned directory and new lock/change record. CHANGE_CONTROL.md governs amendments. No changes were made to V14 original outputs,V14.2 manuscript or main.
