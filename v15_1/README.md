# V15.1 recovery preparation

This directory is a versioned **procedural** recovery amendment. It never changes original V15.0 files,base data,models,features,seeds,60epochs,CE,optimizer,scheduler or analysis definitions. Read RECOVERY_PROTOCOL.md before any execution. The original run,container and SHA-verified backup must remain preserved.

## Current company-PC attempt

Source run: `~/v15-runs/v15_0_20261110T001623Z`

Backup: `~/v15-backup-20261110T042742Z.tar.gz`

Backup SHA256: `62f383a7d5642a0cc25d89a8ae4302b85f68ee4f58b9ce7d1b7d9b217a6a8997`

Reported old state:89complete,one interrupted,990pending. These counts are not assumed to be valid without per-job revalidation.

## Step A — preparation only,NO learning

```
cd ~/v15-runtime-transfer
git pull --ff-only
bash v15_1/prepare-recovery.sh
```

Expected outcome **if all89recorded jobs pass**:

```
RECOVERY_PREPARATION_PASS 89 reused; 991 new fits required;NO_NEW_TRAINING
```

The script verifies the original backup against every source file and checks original operation snapshots,recorded completed-job hashes,true labels,dates,scaler/tensor hashes,checkpoint replay and copied byte hashes. The source and backup are mounted read-only. A fully complete but unrecorded job is reported separately if one exists. A mismatched recorded completed job blocks preparation. Partial job folders stay in the old attempt; no old files are deleted/overwritten. A new external recovery directory and immutable preparation plan are created.

Send the summary for review before executing anything else. No recovery training has been performed by this preparation or the synthetic tests.

## Step B — separate explicit recovery execution

`bash v15_1/execute-recovery.sh` is only for after Step A readiness review. It starts a new externally authorized container; it does not restart the old one. It opens a separate minimized WindowsWSL keepalive client and records itsPID to reduce dependence on the main VSCode terminal. This cannot prevent Windows restart/power loss/IT termination and does not establish the previous shutdown cause. Keep host sleep/update arrangements under company policy. Close only the specific keepalive window after all work is finished;do not stopWSL during training.

Complete prepared jobs are reused without fitting; partial jobs start60epochs from scratch using original fixed seeds and fitting code. The full original probability/ensemble aggregation and analysis definitions are preserved. Recovery counts distinguish reused jobs and newly trained jobs. This is explicitly **not** an uninterrupted V15.0 execution. If this attempt is interrupted,preserve it and create another prepared attempt from a new verified backup;never rerun a partially executed directory.

## Progress and tests

After actual execution,`bash ~/v15-runtime-transfer/status-v15.sh` follows the latest run. `TRAINING_CONFIRMED` must come from an actual new saved epoch/loss; reused checkpoint files are not represented as new training.

`recovery_no_fit_test.json` reports only temporary random/untrained schema fixtures and mocked cache-miss fitting. It covers backup/source identity,source preservation,independent copies,partial-job quarantine,cache hit without fitting/RNG consumption,unchanged argument forwarding and rejection of recorded-complete corruption. It is not a training equivalence study. Actual company-PC89job validation remains necessary.

Code files and this protocol are SHA-bound in version_manifest.json;copy snapshots and source-run provenance are preserved per attempt. The Git transfer-branch commit identifies this amendment independently of the original immutable payload SHA.
