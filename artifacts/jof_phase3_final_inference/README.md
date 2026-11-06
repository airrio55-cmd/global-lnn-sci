# JOF Phase3 final inference

All outputs use existing saved predictions. No training, tuning, new architecture, threshold changes, HMM refit or nonoverlap phase search occurred. `protocol_lock.json` and `source_manifest.json` were written before inference. `execution_manifest.json` freezes executed code hashes. `final_inference_manifest.json` indexes input/output hashes, with previous artifact checksums retained in source_manifest.json. New learned scoring probabilities are equal-weight means of the five saved seed probabilities; directional outputs retain original3-of-5 labels. LNN denotes LTC/LNN; Rule_200DMA denotes200DMA.

`results_report.md` answers the14 requested questions; `methodology_notes.md` records all definitions and limitations. All required CSVs and source code are preserved. `statistical_methods.py` includes HAC/DM/GW-style Wald, fixed-family Holm and a studentized Hansen SPA. `verify_methods.py` independently verifies HAC, Holm, sign conventions and SPA against statsmodels/arch. Additional audit checks all final corrections against statsmodels and confirms membership/counts.

Reproduce without retraining:

```
PYTHONPATH=/workspace/.jof-phase3-deps:/workspace/.jof-phase1-deps:/workspace/.hmm-plot-deps /workspace/.venvs/global-lnn-sci/bin/python artifacts/jof_phase3_final_inference/verify_methods.py
PYTHONPATH=/workspace/.jof-phase3-deps:/workspace/.jof-phase1-deps:/workspace/.hmm-plot-deps /workspace/.venvs/global-lnn-sci/bin/python -u artifacts/jof_phase3_final_inference/analyze.py
```

Package versions and inspected arch source are archived under diagnostics/. Expected stationary block length20,10000 replicates and seed20261106 are fixed. Primary/full HAC19 contrasts are distinct from prespecified reduced-overlap HAC0/H1 diagnostics. Undefined p-values stay undefined but count conservatively as input1 within unchanged Holm family sizes. Source artifacts remain unchanged. GW is explicitly a conditional-moment robustness approximation, not exact original rolling-window GW. MCS retention does not imply equality. Predictive-loss improvement does not establish economic or directional superiority. PDF and300dpi PNG figures are reproducible diagnostics.

execution_status records validated calculation completion; local publication.json records the separate verified remote-main publication. No inference file itself can contain the SHA of its own commit.
