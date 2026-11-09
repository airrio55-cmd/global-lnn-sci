# V15.0 neural extension — frozen protocol

This is the authoritative V15.0 protocol payload. STEP4 authorizes freezing and execution-environment verification, **not training, AUC or H1–H3 execution**. The exact payload commit SHA and UTC time are recorded subsequently in V15_LOCK_RECORD.md/json; a Git commit cannot contain its own SHA. A record-only descendant commit does not replace the immutable payload anchor. Never cite the moving branch tip as the frozen SHA.

## Design and data

Markets: SP500,NASDAQ100,NIKKEI225,EUROSTOXX50,KOSPI200. Original V14 raw and Phase1 processed inputs remain byte-unchanged. Preserve source COMMON_LOCAL feature order, empirical observation calendars and missingness. No downloading, recalculation, filling or alternate calendars. Hashes of data, original source notebooks, original leakage audits, V14 code/scoring dates/unit results, active config, complete V15 source, environment and audit evidence are in V15_LOCK_PAYLOAD.json.

Horizon20 and window20 observed trading rows. Inputs are t−20…t−1. Target is I(Close[t+20]>Close[t]); ties0. Preserve V14 minimum index201, RAW finite-window eligibility and label endpoint inside each split's year-end. No added embargo. LOG must be finite on every RAW-eligible window and cannot add scoring dates. StandardScaler fits only the union of rows actually used in eligible training windows, shared across lags; no evaluation dates enter scaler fitting.

| Origin | Initial train | Fresh annual validation refits | Single fresh test fit |
|---|---|---|---|
| O1 |2010–2012|2013;2014|2015–2016|
| O2 |2010–2013|2014;2015|2016–2017|
| O3 |2010–2014|2015;2016|2017–2018|
| O4 |2010–2015|2016;2017|2018–2019|
| O5 |2010–2016|2017;2018|2019–2020|
| O6 |2010–2017|2018;2019|2020–2021|

Each validation year uses fresh expanding history through its preceding year and its own annual label cutoff. Pool both annual validation prediction sets. Test fit uses history through the last validation year and scores both test years without a test-period refit. All60 scoring-date groups and90 refit folds must match V14 exactly. This rolling-origin design differs from the earlier2022–2025 held-out experiments; those earlier outputs are never substituted.

## Networks and averaging

Four fitted branches: LSTM RAW,LTC RAW,CfC RAW,CfC LOG. Original128-unit architecture, dropout0.2 before two-logit Linear head, last timestep representation, original Linear initialization and installed fully connected ncps defaults. No AutoNCP. RAW uses each market's frozen COMMON_LOCAL. LOG is exactly ordered Log_Ret,Disparity20, using the existing values: diff(log(Close)) and Close/rolling_mean20(Close)−1. No additional transform.

CfC Ensemble is0.5×CfC RAW probability +0.5×CfC LOG probability for the same seed/date. Then average probabilities over seeds42,52,62 for each variant. Never average AUCs or substitute majority labels. CfC LOG remains a diagnostic output; the ensemble is not a fourth architecture in H1.

This is a new five-market analogue of a historical KOSPI200 CfC RAW/LOG ensemble, **not an exact replication** of its features, Disparity series or historical focal-loss specification. Historical external data source availability limitations remain; no prospective or independently preregistered replication is claimed after observing V14.

## Training specification — frozen but not executed

Seeds42,52,62. Fixed60 epochs for both annual validation fits and test fit. CE,AdamW lr.005/weight_decay1e-4,OneCycleLR,batch64,clip norm1. No early stopping, model/loss/feature/threshold tuning or validation-selected checkpoint. p>.5 labels are descriptive, not an AUC-selection threshold. This deliberately changes older neural validation100epoch/patience10 rules; equal epochs do not imply equal optimizer steps across expanding datasets.

CPU only, two PyTorch threads, strict deterministic algorithms and explicit Python/NumPy/Torch/loader seeds. Exact versions and installed code/binary attestations are in V15_ENVIRONMENT.lock.json and requirements-v15.lock.txt. No GPU equivalence claim. Runtime must pass version/hash verification before an authorized run; different versions require a separate amended version, not silent replacement.

Plan:5 markets×6 origins×3 seeds×4 branches×3 refits=1080 fits (720validation,360test), with0 extra ensemble fits. step4/job_manifest.json enumerates unique fit IDs, dimensions, sample counts and exact evaluation-date hashes. There are450 model-unit-seed outputs including all five derived/fitted variants, and at most30 dependent market-origin units.

Preserve per-fit state_dict, training-loss history, seeds, configuration/environment, train/evaluation dates, used scaler rows/statistics, tensor hashes, date probabilities/labels, timestamps and failures. Checkpoint reconstruction uses the same seed, topology and chunking and verifies probability tolerance1e-7 without changing saved probabilities. Partial failures block completion/analysis; do not skip, impute or select successful units. No optimizer-resume claim: an interrupted fit requires a separately documented attempt, preserving failed artifacts.

## Analysis specification — static review only in STEP4

H1: negative Spearman association of200DMA signal-effect shift with the equal-weight mean ΔAUC across LSTM,LTC_RAW,CfC_RAW only, after seed probability averaging. At least16/30 negative mean test alignment correlations is a prerequisite for H1-support interpretation. Missing units qualify the conclusion.

H1b: positive association of200DMA shift×mean test alignment with mean ΔAUC. H2: negative Momentum60/Persistence shift associations. Exactly H1b and the two H2 tests form Holm3. H3 counts negative validation probability–Persistence correlations among90 planned architecture-unit entries; ensemble separately descriptive; no independent-binomial p. Seeds are paired descriptive stability checks, never independent replication units.

Reuse V14's10000 nominal within-market permutations,seed20261109, actual market-specific circular rotations,6 synchronized shifts and descriptive within-market/leave-one-market-out diagnostics. Original helper filters finite rows before rotation. Current signal-only H1 eligibility is28/30 (SP500 O1 andNASDAQ100 O1 excluded), with signal-eligible block product5×5×6^3=5400; actual hypothesis-specific total must be reported if other undefined entries arise. These remain non-exact dependent-data diagnostics, not causal or confirmatory tests.

Compare unchanged V14 LogisticRegression andLightGBM on exact matched dates/units, retaining validation/test/ΔAUC and two-model means. CfC RAW vs ensemble is descriptive on identical dates. No expanded favorable inferential family, HMM refit or test-dependent model choice.

## Authorization and change control

Active configuration:V15_CONFIG_LOCKED.json. Its automatic training and analysis permissions remain false. A future separate explicit authorization may enable only the external per-run record's execution_authorized/analysis_authorized flags and corresponding CLI opt-in; it must preserve the exact anchor and hash inventory. Such a run authorization is not a change to frozen code/data/settings. STEP4 creates records with both flags false.

All tests at freeze are training-free. Forward tests and temporary random-model checkpoint fixtures do not establish60epoch numerical stability or successful1080-job runtime. Neither Test AUC nor H1–H3 statistics were computed. Historical release timestamps/vintages remain an acknowledged limitation, not newly certified point-in-time data.

Never amend, move the lock tag, rewrite the payload or overwrite frozen audit outputs. Any post-lock code/data/config/environment correction requires a new version directory and lock anchor, a detailed change record, retained original attempts and renewed approval before outcomes can inform changes. Record-only descendants are allowed only for lock/provenance metadata explicitly excluded by the verifier; they cannot change any frozen payload bytes. Run repeat audits into an external output directory.
