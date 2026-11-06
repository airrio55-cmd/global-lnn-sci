# JOF Phase 2: CfC + PE-Transformer

See protocol_lock.json for prespecified settings and user_request.md for the complete request. Existing Phase1 and historical artifacts are protected by the SHA256 ledger in run_manifest.json. Input tensors, processed features and scalers are copied byte-preserved from Phase1 (tensor containers are reserialized with the Phase2 protocol hash; tensor values are unchanged).

execution_status.json, active_job.json, progress.json and execution.log record actual local execution. completion_check.json is created only after all validation, final predictions and checkpoint replay audits pass. publication.json is local-only and records the verified remote commit after successful publication. A running status is not completion or publication.

Validation:450 fits;150 candidate-seed records. Final:50 selected fits. Predictions and model state_dict checkpoints are resumable. Run using the original environment and isolated dependencies:

```
PYTHONPATH=/workspace/.jof-phase1-deps:/workspace/.hmm-plot-deps /workspace/.venvs/global-lnn-sci/bin/python -u artifacts/jof_phase2_architecture_expansion/run_phase2.py
```

Preflight is available with --preflight. It checks training-only finite losses/gradients and same-seed PE-zeroed output equivalence to the original Transformer. Source/protocol hashes must match on resume; do not edit them to tune or force a resumed experiment. Final statistics are descriptive; the30/40/5/5 hypothesis families are proposals only. No final Holm correction is run in Phase2.
