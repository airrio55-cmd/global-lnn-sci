> Historical STEP3 page. STEP4 supersedes its draft-readiness status; see STEP4_REPORT.md and V15_LOCK_RECORD.md for the frozen anchor and authorization limits. Earlier audit/ records remain historical, not claims about changed code.

# V15 integrated code audit — draft only

The complete runner, representation gate, read-only real-data preflight, forward-only tests, structural analysis validator and regression tests are now present in this folder. No separate ZIP is needed. See [AUDIT_REPORT.md](AUDIT_REPORT.md) for changes, test evidence, static H1/H1b/H2/H3 review and remaining risks.

The study is a new five-market CfC RAW/LOG adaptation. LOG is fixed to existing Log_Ret and Disparity20. Four branches are trainable; the CfC ensemble is a derived matched-seed50/50 probability average. Neither older KOSPI200 replication nor a locked release is claimed.

Recommended unified audit (actively blocks fitting, backward and AUC):

```bash
python artifacts/jof_v15_neural_extension/v15_audit_only.py --repo . --out artifacts/jof_v15_neural_extension/audit
```

Individual read-only checks: from repository root using the reviewed environment:

```bash
python artifacts/jof_v15_neural_extension/v15_preflight_readonly.py --repo . --out artifacts/jof_v15_neural_extension/audit/preflight_results.json
python artifacts/jof_v15_neural_extension/v15_smoke_no_fit.py --repo . --out artifacts/jof_v15_neural_extension/audit/forward_results.json
python artifacts/jof_v15_neural_extension/test_v15_audit.py
```

The audit used /workspace/.venvs/global-lnn-sci/bin/python with PYTHONPATH=/workspace/.jof-phase1-deps. Exact installed versions are in audit/forward_results.json; they differ from the original V14 non-neural environment. No package version was silently changed in V14 artifacts.

`V15_CONFIG_DRAFT.json` is still DRAFT, with both training and analysis disabled. Source hashes in its representation provenance cover data and runtime sources, not an immutable lock. `audit/preparation_manifest.json` records this audit snapshot. No training command or lock-generation command was run. Historical V14 results, V14.2 manuscript and main worktree were preserved.
