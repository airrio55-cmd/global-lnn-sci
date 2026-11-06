# JOURNAL OF FORECASTING — PHASE 2 ARCHITECTURE EXPANSION
## CfC + Positional-Encoding Transformer

This task extends the frozen Journal of Forecasting evaluation framework after Phase 1.

The manuscript studies how evaluation design affects apparent forecasting advantages across global equity markets.

Phase 2 adds two prespecified architectures:

1. CfC (Closed-form Continuous-time neural network)
2. Positional-Encoding Transformer (PE-Transformer)

The purpose is:

- to complete the liquid neural architecture comparison beyond LTC;
- to address the current Transformer implementation's lack of explicit positional encoding;
- to expand the final architecture universe before multiplicity correction and DM/GW/MCS analysis.

All settings must be frozen before inspecting test outcomes.

---

# 1. Critical restrictions

DO NOT:

- overwrite any existing artifact
- alter Phase 1 outputs
- alter existing LNN/LSTM/GRU/Transformer results
- alter Logistic Regression or LightGBM results
- alter target definitions
- alter H=20
- alter W=20
- alter validation/test splits
- use test results for loss selection
- use test results for threshold selection
- tune PE-Transformer architecture after inspecting test results
- tune CfC architecture after inspecting test results
- refit HMM regimes
- perform favorable phase search
- redefine the final Holm family until Phase 2 is complete
- replace the original Transformer with PE-Transformer
- replace LTC with CfC

Both new models are additional architectures.

---

# 2. Artifact directory

Create:

`artifacts/jof_phase2_architecture_expansion/`

Required outputs:

- `protocol_lock.json`
- `selected_configs.csv`
- `cfc_validation_results.csv`
- `cfc_seed_results.csv`
- `pe_transformer_validation_results.csv`
- `pe_transformer_seed_results.csv`
- `test_results_phase2.csv`
- `majority_vote_results.csv`
- `benchmark_comparison_phase2.csv`
- `forecast_frequency_diagnostics.csv`
- `pt_results_phase2.csv`
- `nonoverlap_results_phase2.csv`
- `transaction_cost_results_phase2.csv`
- `architecture_rank_table.csv`
- `final_model_universe_manifest.json`
- `completion_check.json`
- `methodology_notes.md`
- `results_report.md`

Recommended:

- `all_predictions/`
- `checkpoints/`
- `diagnostics/`
- `figures/`

---

# 3. Markets

Use exactly:

- S&P 500
- NASDAQ-100
- Nikkei 225
- EURO STOXX 50
- KOSPI 200

Use the same frozen processed data as the manuscript and Phase 1.

Do not rebuild data if existing frozen inputs are available.

---

# 4. Temporal protocol

Retain exactly:

Validation:

- 2019
- 2020
- 2021

Test:

- 2022–2025

Use the same expanding walk-forward validation protocol.

No test observation may influence:

- architecture settings
- loss selection
- threshold selection
- stopping decisions
- model family inclusion

---

# 5. Forecast target

Retain:

`Target_t = 1 if Close[t+20] / Close[t] - 1 > 0 else 0`

Horizon:

`H = 20 trading days`

Input window:

`W = 20 trading days`

---

# 6. Features

Use exactly the same COMMON_LOCAL feature set used by:

- LTC/LNN
- LSTM
- GRU
- existing Transformer

No new features.

No positional feature should be added as a raw explanatory variable.

Positional information for PE-Transformer must be encoded only through the positional-encoding layer.

---

# 7. Seeds

Use exactly the existing five seeds:

- 42
- 52
- 62
- 72
- 82

Do not add the second five seeds in Phase 2.

Ten-seed expansion is a later robustness phase.

---

# 8. CfC implementation

Use the existing installed `ncps` package.

Implement CfC using:

`ncps.torch.CfC`

CfC is a distinct liquid architecture from LTC.

Do not describe CfC as a replacement for LTC.

Use the closest possible dimensions to the frozen LTC model.

Required high-level structure:

- input_size = number of features
- hidden_size / units = 128 where supported
- batch_first = True where supported
- explicit Dropout(0.2) before output head
- final Linear(128, 2)

If `ncps.torch.CfC` returns an output sequence:

- use final timestep representation

If the API requires a slightly different constructor than LTC:

- document the exact constructor
- do not introduce additional hidden layers
- do not change width beyond what the library requires

Do NOT use AutoNCP wiring.

Use a standard fully connected CfC configuration.

---

# 9. CfC training settings

Match the existing neural protocol:

- hidden size = 128
- dropout = 0.2
- batch size = 64
- max epochs = 100
- patience = 10
- final refit epochs = 60
- MAX_LR = 0.005
- AdamW
- weight_decay = 1e-4
- OneCycleLR
- gradient clipping norm = 1.0
- StandardScaler
- same random-seed controls

If CfC requires a library-specific parameter that has no LTC counterpart:

- choose the package default
- record it in `protocol_lock.json`
- do not tune it

---

# 10. CfC loss candidates

Evaluate exactly:

- CE
- MILD_WCE
- MILD_FOCAL

Reuse the exact existing implementations.

Do not rewrite loss formulas.

For each market, select the loss by:

1. highest mean walk-forward validation BA across 2019–2021
2. tie → higher validation Macro F1
3. tie → selected threshold closest to 0.5
4. deterministic lexical ordering only if still tied

No test-driven selection.

---

# 11. CfC threshold selection

Threshold grid:

`0.30 to 0.70 inclusive, step 0.01`

Select using:

1. validation Balanced Accuracy
2. tie → validation Macro F1
3. tie → distance from 0.5

Freeze threshold before test evaluation.

---

# 12. PE-Transformer purpose

The existing primary Transformer intentionally remains unchanged.

The PE-Transformer is a prespecified architecture-sensitivity analysis that adds explicit positional information.

Do not overwrite or relabel the existing Transformer.

Final manuscript terminology must distinguish:

- Transformer (original, no explicit positional encoding)
- PE-Transformer (sinusoidal positional encoding)

---

# 13. PE-Transformer architecture

Replicate the frozen existing Transformer exactly except for positional encoding.

Frozen base Transformer:

- d_model = 128
- nhead = 4
- num_encoder_layers = 2
- dim_feedforward = 256
- dropout = 0.2
- activation = GELU
- batch_first = True
- final LayerNorm
- final Linear(128, 2)

Add only:

**standard sinusoidal positional encoding**

using the classical deterministic sine/cosine formulation.

Maximum sequence length must support W=20.

No learned positional embeddings.

No relative positional encoding.

No rotary embeddings.

No patching.

No CLS token.

No architecture tuning.

---

# 14. PE placement

Apply sinusoidal positional encoding after input projection to d_model and before Transformer encoder layers.

Conceptual flow:

input features
→ Linear(input_dim, 128)
→ add sinusoidal positional encoding
→ TransformerEncoder(2 layers)
→ final sequence position
→ LayerNorm
→ Linear(128, 2)

The final-position aggregation must match the existing Transformer.

---

# 15. PE-Transformer training

Use exactly the existing Transformer training protocol:

- AdamW
- weight_decay = 1e-4
- MAX_LR = 0.005
- OneCycleLR
- gradient clipping = 1.0
- batch size = 64
- epochs = 100
- patience = 10
- final refit epochs = 60
- dropout = 0.2
- same StandardScaler
- same seeds

---

# 16. PE-Transformer losses

Evaluate exactly:

- CE
- MILD_WCE
- MILD_FOCAL

Same validation-only selection rule as all other neural models.

Do not copy the loss selected by the original Transformer automatically.

PE-Transformer gets its own validation-only loss selection.

---

# 17. Majority vote

For both CfC and PE-Transformer:

combine the five frozen seed predictions by:

`Up if >= 3 of 5 seeds predict Up`

Do not probability-average.

Report both:

- five-seed mean metrics
- 3-of-5 majority metrics

Keep these conceptually separate.

---

# 18. Primary metrics

Report:

- Accuracy
- Balanced Accuracy
- Macro F1
- F1
- Recall
- Precision
- Forecast Up Rate
- Actual Up Rate

Primary metric:

`Balanced Accuracy`

---

# 19. Direct architecture comparison

For each market compare:

- LTC/LNN
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer

Do not select a winner using test data.

The comparison is descriptive after independently frozen validation selection.

Report:

- validation BA
- mean seed test BA
- majority test BA
- Macro F1
- Forecast Up Rate

---

# 20. Positional-encoding sensitivity

Create a paired diagnostic:

`pe_transformer_vs_original_transformer.csv`

For every market report:

- original Transformer validation-selected loss
- PE-Transformer validation-selected loss
- original majority BA
- PE majority BA
- ΔBA
- original Macro F1
- PE Macro F1
- ΔMacroF1
- original Forecast Up Rate
- PE Forecast Up Rate
- original Accuracy
- PE Accuracy

Interpretation must be symmetric.

Possible outcomes:

- PE improves performance
- PE worsens performance
- PE changes forecast frequency
- PE removes a prior positive signal
- PE creates an isolated positive signal

All are valid.

---

# 21. Liquid architecture sensitivity

Create:

`ltc_vs_cfc.csv`

For every market report:

- LTC selected loss
- CfC selected loss
- LTC validation BA
- CfC validation BA
- LTC mean-seed test BA
- CfC mean-seed test BA
- LTC majority BA
- CfC majority BA
- Forecast Up Rate
- Macro F1

Do not call either architecture superior without multiplicity-aware evidence.

---

# 22. Forecast-frequency diagnostics

For CfC and PE-Transformer calculate:

- Actual Up Rate
- Forecast Up Rate
- absolute distance from 0.5
- Forecast Up minus Actual Up

Define diagnostic flag:

`near_constant = True`

if:

- Forecast Up Rate < 0.10
or
- Forecast Up Rate > 0.90

Do not exclude or retune flagged models.

---

# 23. PT tests

Use the exact existing Pesaran–Timmermann implementation.

Evaluate majority predictions for:

- CfC × 5 markets
- PE-Transformer × 5 markets

Report:

- PT statistic
- two-sided raw p
- positive one-sided p
- Actual Up Rate
- Forecast Up Rate

These are diagnostic raw p-values in Phase 2.

Do NOT yet perform the final Holm correction until the final universe is frozen in Section 30.

---

# 24. Reduced-overlap

Use:

- phase = 0
- step = 20

No phase search.

For CfC and PE-Transformer report:

- N
- Accuracy
- BA
- Macro F1
- Forecast Up Rate
- PT statistic
- PT raw p

Mandatory wording in report:

> The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence.

---

# 25. Economic evaluation

Apply the existing long/cash framework.

Models:

- CfC
- PE-Transformer

Transaction costs:

- 0 bps
- 10 bps
- 25 bps
- 50 bps

Primary reporting:

10 bps.

Metrics:

- CAGR
- annualized volatility
- Sharpe
- Sortino
- maximum drawdown
- exposure
- number of trades
- turnover

No new trading assumptions.

---

# 26. Final architecture universe

After Phase 2 completes, freeze the neural architecture family as:

1. LTC/LNN
2. CfC
3. LSTM
4. GRU
5. Transformer
6. PE-Transformer

Non-neural learned benchmarks:

7. Logistic Regression
8. LightGBM

Rule baselines:

9. Persistence
10. 200DMA
11. Momentum60
12. Always-Up
13. Always-Down

Record this in:

`final_model_universe_manifest.json`

This file defines the universe to be used in later DM/GW/MCS/multiplicity work.

---

# 27. Friedman analysis

Perform a diagnostic neural-only Friedman test across the six neural architectures:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer

Metrics:

- majority BA
- majority Macro F1

Report:

- Friedman statistic
- raw p
- Kendall W

Important:

Only five market blocks exist.

Do not interpret non-significance as equivalence.

Do not interpret significance as proving one architecture dominates.

Final multiplicity-aware pairwise interpretation comes later.

---

# 28. Descriptive ranks

Generate per-market and cross-market descriptive ranks for:

Neural-only:

- LTC
- CfC
- LSTM
- GRU
- Transformer
- PE-Transformer

Learned-model universe:

- above six
- Logistic Regression
- LightGBM

Rank separately by:

- BA
- Macro F1
- Accuracy

Do not use these ranks to select the manuscript's primary model.

---

# 29. Existing KOSPI Transformer signal

Explicitly examine the previously observed KOSPI Transformer PT result.

Report:

- original Transformer KOSPI BA
- PE-Transformer KOSPI BA
- original PT
- PE PT
- original Forecast Up Rate
- PE Forecast Up Rate

Do not frame this as a replication target.

The purpose is architecture sensitivity.

---

# 30. Freeze final multiplicity families

Only AFTER all CfC and PE-Transformer predictions are complete, create:

`multiplicity_family_proposal.json`

Propose, but do not yet execute, the final families.

Recommended structure:

### Family A — Neural architecture × market PT family

6 neural architectures × 5 markets:

`30 tests`

### Family B — All learned-model × market PT family

8 learned models × 5 markets:

`40 tests`

### Family C — LTC-specific market family

5 tests

### Family D — PE sensitivity paired comparisons

5 markets

Do not apply Holm until Phase 3 unless explicitly required by existing pipeline.

Document exact membership.

---

# 31. Audit requirements

`completion_check.json` must confirm:

- existing artifacts unchanged
- Phase 1 artifacts unchanged
- same frozen data
- same H=20
- same W=20
- same split
- same feature set
- no test-driven loss selection
- no test-driven threshold selection
- CfC constructor frozen before test
- PE architecture frozen before test
- PE differs from original Transformer only by positional encoding
- no HMM refit
- no phase search
- all seed predictions saved
- all selected configs recorded
- all negative/null outcomes retained
- checkpoint replay verified
- no original Transformer replacement
- no LTC replacement
- final universe manifest created

Set:

`status = "validated"`

only if every audit passes.

---

# 32. results_report.md

Answer explicitly:

1. Does CfC materially differ from LTC?
2. Does CfC outperform LTC consistently across markets?
3. Does positional encoding materially change Transformer performance?
4. Does PE fix or worsen near-constant forecast behavior?
5. Does PE alter the KOSPI Transformer signal?
6. Do either CfC or PE show stable positive PT evidence?
7. What survives reduced-overlap evaluation?
8. Do economic results reflect timing skill or exposure?
9. Does the six-neural-model Friedman test detect stable ranking?
10. Does Phase 2 strengthen or weaken the evaluation-design thesis?
11. Is any architecture consistently dominant across five markets?
12. What should enter the final Phase 3 multiplicity and DM/GW analysis?

Use cautious manuscript-compatible language:

- apparent advantage
- architecture-sensitive
- benchmark-sensitive
- statistically fragile
- isolated positive exception
- no stable cross-market dominance
- did not detect

Avoid:

- proved superior
- robust superiority
- established dominance
- statistically equivalent

---

# 33. Repository handling

When complete:

- commit only the new Phase 2 directory
- do not modify prior artifacts
- push to GitHub main
- preserve all audit files
- final completion message <= 15 lines
