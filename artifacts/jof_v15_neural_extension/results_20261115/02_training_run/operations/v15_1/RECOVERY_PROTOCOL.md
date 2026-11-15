# V15.1 procedural recovery amendment — no outcome-dependent change

Base scientific payload remains d866841eeb87c63f42bd10240c7acc06ee7dbe49. V14,main,the V15.0 source/config/environment and original interrupted attempt remain unchanged. This is **V15.1 execution control**,not an uninterrupted or unmodified V15.0 CLI run.

Reason: original attempt received externalSIGTERM at2026-11-10T04:12:32UTC.89jobs were recorded complete,one active job was interrupted and990were pending. OOMKilled=false. The subsequently supplied Docker journal confirms systemd stopped docker.service and dockerd completed a graceful shutdown at04:12:32–34UTC. Whether this was a whole-WSL shutdown or a Docker-only stop is still not established. No performance,AUC or hypothesis results determined this amendment. The user requested a versioned recovery procedure after preserving a backup.

## Scientific invariants

Same5markets,O1–O6,annual validation refits/two-year test fit,20-dayH/W,same exact dates,label endpoints,training-onlyscalers,features/LOG order,seeds42/52/62,60epochs,CE,architecture,initialization,AdamW/OneCycleLR and CPU environment. No early stopping,tuning,selection,threshold or ensemble-weight changes. Same-seed CfC RAW/LOG probabilities are combined by the original50/50 code. Base immutable hashes/environment must pass before preparation and execution. Base analysis definitions and null/opposite-direction reporting remain unchanged.

## Prepare-only gate

The original run and backup are mounted read-only. The default backup is v15-backup-20261110T042742Z.tar.gz with SHA25662f383a7d5642a0cc25d89a8ae4302b85f68ee4f58b9ce7d1b7d9b217a6a8997. Verify gzip/tar contents against the entire source file inventory without extraction; reject unsafe paths/symlinks and any content drift. Verify original authorization/source anchor and operation snapshot hashes.

Every recordedCOMPLETE job must match its previously recorded four-fileSHA set. Independently verify60finite loss rows,checkpoint fields/finite state,true labels,exact input/date/scaler hashes and checkpoint replay using the original source. A mismatched recordedCOMPLETE job blocks preparation,not silent retraining. Fully valid but previously unrecorded complete folders may be recovered only after all the same checks and explicit provenance recording. Partial/noncomplete failed folders remain preserved in the old attempt and are listed for full restart.

Copy only fully validated jobs into a fresh external attempt directory using independent byte copies,never hardlinks. Recheck copied digests. Never overwrite or move the original files. Preparation creates a readiness/plan manifest and **does not start learning or AUC/statistics**. Any failed preparation remains a separate attempt and cannot be overwritten. The user must inspect the reuse/new-fit counts before explicitly executing recovery.

## Versioned dispatch

V15.1 explicitly installs an in-memory fit_predict **dispatch adapter** around the original frozen fitting function. This changes job orchestration; it does not claim the full V15.0 CLI is unchanged. The original CLI refuses existing output; V15.1 calls its guarded run function with prepared cache directories instead.

A cache hit is allowed only for a JobID in the immutable prepared reuse plan,with matching model,seed,60epochs,CPU,dimensions,training/evaluation dates,ordered columns and all four preserved file hashes. Return the saved checkpoint's exact float32 probabilities,not rounded/recomputed CSV probabilities. Do not construct/train a replacement model or consume model RNG on cache hits. Every actual cache miss delegates all arguments unchanged to the original fit_predict,which resets its own seeds and trains60epochs from scratch. A preexisting unplanned job directory blocks execution. No optimizer/partial-epoch state is reused.

The original run function reconstructs all date-level outputs and50/50 ensembles in the same order,using cached exact probabilities where applicable. Its fit_count1080denotes logical job completion,**not1080new fits in this recovery attempt**. Keep a separate dispatch ledger and report reused,newly trained and failed/interrupted prior attempts. Original cached per-job learning timestamps/loss histories remain preserved; cached dispatchSeconds are not original training times.

New controller starts progress at the verified reuse count,never at zero. It verifies new completed jobs and the final combined output as before. Periodic frozen-file checks remain. Only after1080logical jobs and all hashes/date/seed/checkpoint/ensemble checks pass may the separately authorized original statistical analysis execute. No partial-run AUC/H1–H3 analysis or favorable selection.

## Interruptions and host continuity

No automatic retries or Docker restart. If recovery is interrupted,preserve it and prepare a new attempt from its verified completed artifacts and a new backup; do not rerun a prepared/partly executed directory. Recovery at job boundaries is supported; partial jobs restart from epoch1 with the same seed. Old partial attempts are reported and retained.

Execution opens a separate minimized Windows WSL client running sleep infinity,so closing the main VSCode/Ubuntu terminal need not be the only process maintaining WSL. This does **not** prevent Windows restart,power loss,IT policy termination or Docker service shutdown. It does not establish why the previous run stopped. Keep host power/sleep/update arrangements within company policy. The keepalivePID is recorded for the operator;never indiscriminately kill WSL processes.

## Evidence and authorization

All recovery code/scripts and this document are SHA-bound in version_manifest.json and copied outside the repository for each attempt. The transfer-branch Git commit plus external operation-code hashes identify the procedural version. Source models/data/config remain anchored by the baseSHA. Approval to prepare recovery is not a claim that company-PC artifacts have already passed: they are only accessible on the company PC. Actual execution requires the separate execute-recovery.sh invocation after READY validation.

Unit tests use temporary synthetic,untrained checkpoints and mocked fitting calls;no real learning,AUC or hypotheses are executed during preparation/testing. Report those as schema/dispatch tests,not a trained equivalence experiment. Any scientific or implementation amendment beyond this dispatch policy requires another version/change record.
