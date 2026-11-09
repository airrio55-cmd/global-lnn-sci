# V15 neural extension — integrated protocol draft

**DRAFT / NOT LOCKED. No authorization to train or calculate AUC.** This code-review commit is not an immutable protocol lock. V14 outputs, original locked code and V14.2 manuscript remain unchanged. This is a historical, pre-result specification of V15 after observing V14, not a prospective preregistration.

## Data and timing retained from V14

Use the original five market_input.csv files, Phase1 frozen feature CSVs and ordered COMMON_LOCAL feature lists. Hashes must match both Phase1 and the original V14 input inventory. No data download, feature refresh, backfill or synthetic observations. Preserve the existing empirical market calendars and source availability limitations.

H=W=20 observed trading rows. At forecast t use exactly t-20 through t-1; label is I(Close[t+20]>Close[t]). Preserve V14's minimum raw index201, finite RAW-window eligibility and within-split forward label endpoint. No extra embargo. Scaler is fit only on the union of feature rows in eligible training windows, shared across lags. LOG must be finite on the same RAW-eligible dates; no LOG-only dates are added.

| Origin | Initial training | Annual validation folds | Single test fold |
|---|---|---|---|
| O1 | 2010–2012 | 2013; 2014 | 2015–2016 |
| O2 | 2010–2013 | 2014; 2015 | 2016–2017 |
| O3 | 2010–2014 | 2015; 2016 | 2017–2018 |
| O4 | 2010–2015 | 2016; 2017 | 2018–2019 |
| O5 | 2010–2016 | 2017; 2018 | 2019–2020 |
| O6 | 2010–2017 | 2018; 2019 | 2020–2021 |

Each validation year receives a fresh fit on eligible history through the preceding year, with its own year-end label cutoff. Pool the two annual validation prediction sets; do not treat them as one two-year fit. A third fresh fit uses all eligible history through the last validation year and predicts the entire two-year test with no test-period refit. Exactly match all60 V14 market/origin/period scoring-date groups and90 individual refit folds.

## Four trainable branches and one derived variant

Train LSTM RAW, LTC RAW, CfC RAW and CfC LOG. RAW uses the existing per-market COMMON_LOCAL input. LOG is exactly ordered `[Log_Ret, Disparity20]`, reusing existing values: diff(log(Close)) and Close/rolling_mean20(Close)-1. No extra logarithm or transformation of Disparity20.

Historical JKSCI KOSPI200 material reportedly describes CfC RAW [Log_Ret, Foreign_Net, Nasdaq, SOX, Disparity] and LOG [Log_Ret, Disparity]. Those historical files are not part of this checkout and their exact Disparity series was not independently verified here. V15 is a **new five-market adaptation**, not an exact reproduction of that KOSPI200 experiment. Do not claim a historical LTC ensemble or identical original features/loss.

For each matched seed/date, CfC_ENSEMBLE =0.5 CfC_RAW probability +0.5 CfC_LOG probability. Then average probabilities across seeds for every evaluated variant. This is probability averaging, not majority vote and not averaging model AUCs. CfC_LOG is retained diagnostically. H1 uses only LSTM, LTC RAW and CfC RAW; the ensemble never becomes a fourth architecture family.

Architecture topology matches the original notebook:128 units, explicit dropout0.2, last timestep and Linear128→2. Fully connected ncps LTC/CfC retain library defaults. No AutoNCP or extra hidden layers are added. CfC library defaults include its internal backbone; this is not a tuned extension.

## Training proposal, not an executed or locked experiment

Seeds `[42,52,62]`; CE; fixed60 epochs for every validation and test fit. Original AdamW lr.005/weight_decay1e-4, OneCycleLR, batch64, clip norm1. No early stopping or threshold selection; a descriptive class output uses p>.5. This intentionally differs from older neural100-epoch/patience10 validation and from historical KOSPI200 focal loss. Equal epochs do not imply equal optimization steps as training history grows.

Only CPU was audited. Strict deterministic PyTorch settings are required. Four branches ×5 markets ×6 origins ×3 seeds ×3 refits =1080 future fits. There are450 evaluated model/unit/seed combinations when all five output variants are counted;360 counts only four outputs excluding diagnostic CfC_LOG. Independent units are at most30, not450 or1080.

Future execution must preserve every model state, per-epoch training loss, train/evaluation dates, scaler statistics and used-row masks, tensor hashes, date-level probabilities/labels, source hash inventory, environment, timestamps and failure message. Fail fast; do not skip failures to create a favorable complete-case subset. An incomplete run is not analyzed. Outputs must be outside the protected checkout, then separately reviewed before publication. No fits are run by import or preflight.

## Static analysis contract retained from V14

Use original V14 functions for nominal10000 within-market permutations (seed20261109), rotations, rank statistics, leave-one-market-out and within-market diagnostics. Importing those functions must never invoke V14.main or estimator fitting. Do not alter V14 source.

- H1: negative Spearman of200DMA signal-effect shift and equally weighted three-family mean ΔAUC. Alignment prerequisite is at least16/30 negative mean test probability–200DMA correlations. A missing prerequisite or fewer than30 eligible units must qualify the conclusion.
- H1b: positive correlation of shift×mean test alignment with mean ΔAUC.
- H2: negative correlations for Momentum60 and Persistence shifts.
- Secondary Holm family has exactly3 members: H1b and both H2 tests. Undefined members are not silently promoted to support.
- H3: count negative validation probability–Persistence correlations across3×30 planned entries; no independent-binomial p. CfC ensemble H3 is separate descriptive output.
- Seed diagnostics report per-variant validation/test/ΔAUC and each seed's three-family H1 sign/size. Seeds are not independent replications.
- V14 comparisons retain both non-neural models' validation/test/ΔAUC and their two-model means, paired by exact dates and30 market-origin keys. CfC ensemble vs RAW is descriptive on identical dates.

Signal effect requires at least20 observations in each binary signal group in both periods. Price/feature-only audit reproduces28/30 eligible200DMA units. Original V14.rotate_p rotates **after finite-row filtering**: the nominal6^5 rotation count applies only to complete six-origin blocks; with missing units the actual product is smaller (5×5×6^3=5400 for the current eligibility). Preserve original behavior and record actual total, not a falsely exact7776. Six synchronized rotations also remain non-exact dependent-data diagnostics.

## Current restrictions and future lock conditions

Config stays DRAFT; permission_to_train=false and permission_to_analyze=false. This task creates no lock file/record/commit designation and performs no model fitting or AUC calculation. Future locking requires separate explicit authorization, environment review and an immutable clean-checkout SHA with full inventory, including config and all runtime/input sources. The lock record must be external to the checkout. Draft inventory completion does not constitute locking. Forward-only checks cannot certify60-epoch numerical stability or real historical external-feature publication times.
