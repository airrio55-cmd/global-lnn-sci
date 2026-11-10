# V15 frozen runtime transfer only

This independent orphan branch transfers a verified Docker runtime archive in five sub-100MiB parts. It does not modify main or the V15 experiment branch. No new training, AUC or H1–H3 inference was performed.

Payload anchor: `d866841eeb87c63f42bd10240c7acc06ee7dbe49`.

Image tag: `global-lnn-sci-v15-runtime:locked-d866841`.

Image ID: `sha256:cb7fdf00a342e756668faec689892d6d90c72fd0a3c13b8912ba9021d365de48`.

Reassembled archive SHA256: `9b6d1e17f519c99aa0b42055439f564430b9374e84fd07143e3541b68870dbe6`.

The archive was built from the exact audited installed Python/runtime libraries and required system shared libraries, without reinstalling ML packages. Container checks passed: frozen source/environment hashes; 60 V14 scoring-date groups; 90 folds; 60 deterministic forward-only checks. Docker save/load and gzip integrity also passed. No repository, user home or repository credentials were copied into the runtime image. Repository inputs are mounted separately.

## Download and reassemble in WSL Ubuntu

```bash
cd ~
git clone --depth 1 --single-branch --branch v15-runtime-transfer-d866841 https://github.com/airrio55-cmd/global-lnn-sci.git v15-runtime-transfer
cd ~/v15-runtime-transfer
bash restore-image.sh
```

All five parts and the reassembled file must report OK. The script refuses to silently overwrite an existing archive; it validates that archive instead. This command neither installs packages nor loads or runs an experimental model.

After validation, load using `sudo docker load -i v15-runtime-locked-d866841.tar.gz`. Before any training, verify the container against the separate clean checkout of the frozen V15 repository and repeat the no-fit checks on the company PC. The image defaults to verification-only mode. It never begins training automatically. Training and statistical analysis remain subject to external authorization and full-run integrity conditions.

## Artifact scope and redistribution

The runtime contains third-party Python packages and system libraries with their installed license notices. Python's license is retained in its standard library and package license metadata is included. Git binary version2.52.0 is included for local immutable-source verification; corresponding upstream source: https://www.kernel.org/pub/software/scm/git/git-2.52.0.tar.xz . System-library versions and source notices can be obtained from their upstream projects; this is a transport of the audited environment, not a newly claimed software implementation. Dockerfile and build recipe are provided for inspection; rebuilding does not imply identical bytes unless the exact source runtime and system binaries match.

Never publish experiment outcomes as complete merely because this runtime loads. The frozen runner has no skip-completed/resume functionality; interrupted attempts must be preserved and reviewed rather than silently restarted over completed jobs. Keep Windows powered on and prevent sleep/reboot only under company policy before a separately confirmed training launch.

## Execution helpers added after company-PC preflight

See OPERATIONS.md for the run authorization,single-launch,progress,integrity and failure policy. `start-v15.sh` launches the unchanged frozen runner; `status-v15.sh` reads actual Docker/process/job state. Operations source is outside the frozen payload and snapshotted per attempt. No model or statistical rule is changed by these helpers.

## V15.1 procedural recovery after the interrupted company-PC run

See v15_1/README.md and v15_1/RECOVERY_PROTOCOL.md. Preparation revalidates the original SHA-verified backup and completed jobs in read-only mounts and creates independent copies in a fresh attempt. It does not train or analyze. This is a versioned dispatch amendment,not a change to the frozen scientific payload. Execute recovery only after company-PC readiness review;keep the original run,container and backup.
