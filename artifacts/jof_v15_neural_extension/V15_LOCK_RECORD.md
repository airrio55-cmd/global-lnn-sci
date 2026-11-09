# V15.0 immutable protocol lock record

- Payload lock commit SHA: `d866841eeb87c63f42bd10240c7acc06ee7dbe49`
- Freeze/commit UTC: `2026-11-09T10:19:02+00:00`
- Korea time: `2026-11-09T19:19:02+09:00`
- Annotated tag: `v15-neural-extension-lock-20261109-step4` (points to payload, not record-only descendant).
- Active protocol/config: V15_PROTOCOL_LOCKED.md / V15_CONFIG_LOCKED.json.
- Complete source,data,configuration,environment,audit inventory: V15_LOCK_PAYLOAD.json; mirrored in V15_LOCK_RECORD.json.
- Training authorization: **false**. AUC/statistical analysis authorization: **false**.
- Actual neural fits/Test AUC/H1–H3 executions: **0/0/0**.

All allowed pre-lock checks passed before the payload commit. The immutable payload and the exact installed environment were subsequently verified on a clean checkout; both unauthorized execution and analysis were rejected by their guards. See step4/post_lock_verification.json. Temporary checkpoints in tests were random,untrained fixtures and were removed.

This record is committed after the payload because a Git commit cannot include its own SHA. The moving draft branch tip may therefore differ from the frozen SHA above. Verification reads the manifest at that immutable anchor and checks ancestry plus exact current/anchor hashes; a record-only descendant cannot change frozen code/data/settings. Use the anchor,never an unqualified branch tip,for reproduction.

For verification only,copy V15_LOCK_RECORD.json to an external location (e.g./tmp/v15-lock-record.json) and invoke:

```bash
python artifacts/jof_v15_neural_extension/v15_locking.py --repo . --config artifacts/jof_v15_neural_extension/V15_CONFIG_LOCKED.json --record /tmp/v15-lock-record.json
```

This command verifies only; it does not train or evaluate. The current record must remain execution_authorized=false and analysis_authorized=false for STEP4. A future separately explicit run authorization may enable only external authorization flags plus CLI opt-in,keeping the frozen SHA/inventory unchanged. No training command was issued or scheduled.

Any code,data,config,environment or methodology correction after freeze requires a new version directory,change record,new SHA/time and approval. Do not amend this anchor,move the tag or silently replace outputs. Metadata-only descendant permissions are narrowly enumerated by the verifier; see CHANGE_CONTROL.md. Git SHA/content hashes identify immutable bytes; no claim of administrator-proof remote-ref protection is made.

V14 original results,V14.2 manuscript and main were not modified. Remaining limitations and resource estimates are in STEP4_REPORT.md. Version pins do not prove a fresh install or cross-hardware bitwise equivalence; preserve the audited runtime and verify full fingerprints before any future authorized experiment.
