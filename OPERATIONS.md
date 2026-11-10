# Company-PC execution controls — wrapper outside the frozen payload

These scripts do not modify the V15.0 protocol,source,data,model,seed,epochs,loss,split,scaler,probabilities or statistical definitions. Each of1080fits and all AUC/H1–H3 calculations are delegated to the original SHA-locked runner/analysis. The wrapper supplies run authorization,monitoring and metric-free artifact validation only. The image and frozen experiment branch remain unchanged.

The user has explicitly approved training and subsequent statistics. An external per-run record enables both flags; analysis runs only after all1080fits and all per-fit/combined integrity checks pass. No selection,tuning,partial-run analysis or automatic retry is performed. Existing V15 containers or fit directories block a duplicate launch. The frozen runner has no resume: never restart an interrupted run or silently skip/retrain completed jobs. Preserve evidence and review recovery/version changes separately.

## Launch,only after company-PC preflight and power checks passed

In the transfer checkout:

```
git pull --ff-only
bash start-v15.sh
```

The launcher checks actual Windows C: free space (at least15GiB),WSL availableRAM(at least10GiB),swap(at least3GiB),Linux free space,image ID,clean source and immutable source/environment hashes. It allocates a single CPU container with2CPUquota,12GiB RAM ceiling and16GiB combinedRAM+swap ceiling,leaving OS headroom on the current15GiB WSL guest. These are host resource limits,not changes to model settings. No GPU and no package installation is performed. If a limit is insufficient,record OOM/failure without changing parameters or automatically retrying.

The container is network-isolated,has a read-only image and source checkout,uses writable temporary cache/output mounts,and has restart=no. Operations code is snapshotted with hashes into the external run directory before launch. No results are written into the frozen Git checkout.

The launcher waits up to180seconds for an actual saved epoch/loss. `CONTAINER_CREATED` alone is not training confirmation. `TRAINING_CONFIRMED` is printed only when a finite saved training-loss row is observed. It reports observation time,not a fabricated exact first optimizer-step timestamp. Final source-fit start/end times are retained in metadata. If startup is still pending after the wait,inspect status and do not launch a second copy.

## Progress and artifact retention

```
bash ~/v15-runtime-transfer/status-v15.sh
```

Run directories are `~/v15-runs/v15_0_<UTC>/`; `~/v15-runs/latest_run.txt` points to the latest attempt. Files include authorization.json,operation source hashes,process/progress/job statusJSON+CSV,training.log,results/fits/<JobID>/{training_loss.csv,checkpoint.pt,fit_metadata.json,predictions.csv},combined predictions,failures and final manifests. Checkpoint files use the exact frozen torch serializer.

Jobs progress PENDING→RUNNING→COMPLETE orFAILED. COMPLETE requires60finite epoch rows,expected metadata,seed/architecture/loss/dimensions,true labels,exact dates/counts,train-only scaler and input tensor hashes,finite checkpoint weights,exact saved probabilities/labels,checkpoint replay and fileSHA256. The wrapper waits for the next fit directory (or child exit) before inspecting completed CSVs,avoiding a partial-write race. Ongoing first-epoch detection tolerates transient incomplete lossCSV writes. No performance metric chooses completion or influences a later job.

Every frozen file is periodically rehashed. Any drift,NaN/Inf,failed replay,wrong date/seed or child failure stops the remaining run and retains prior artifacts. A stopped container or staleRUNNING file is not claimed as active; status-v15.sh prints live Docker state andOOMKilled/exit code. Abrupt host shutdown may prevent final failure bookkeeping,so preserve the whole directory and inspect Docker state. No automatic resume exists.

On successful1080-fit completion,all completed file hashes are checked again; source combined probabilities,labels,seeds,dates,50/50ensemble and source completion manifest are verified before analysis. The frozen analysis receives the separately enabled authorization and a new output directory. AUC/statistics are not computed for partial/failed runs. Null and opposite-direction outcomes are retained.

Keep Windows powered on,Ubuntu terminal open,and sleep/hibernation disabled. Avoid reboot,WSLshutdown and source Git edits during training. Review Windows Update restart scheduling within company policy. This is a company-PC job,not a separately managed cloud VM; closing the browser does not control it,but host/WSL shutdown can interrupt it. No claim of guaranteed uninterrupted Windows operation is made.

## Testing

launcher_no_fit_test.json records schema/integrity tests on temporary random,untrained fixtures,including corrupted-probability rejection and the actual read-only container's optimizer/scheduler constructor imports. No optimizer step,backward,estimator fit,AUC or actual training occurred in those tests. Fixture artifacts were removed. Frozen environment verification also passed in verification-only mode with the external authorization record. This does not claim a real1080-fit rehearsal or trained-result equivalence.
