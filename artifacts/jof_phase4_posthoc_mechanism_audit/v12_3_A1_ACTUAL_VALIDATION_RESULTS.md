# JOF v12.3 A1: actually computed validation alignment (2026-11-08)

LOCKED protocol: 88f1acbc5dff7067966478f6c80c82ae9f2a00e2. Read all 200 selected validation probability files (five seeds per 5 markets × 8 selected models) through the GitHub connector; equal-weight average of probabilities for each model and market. Verified dates and true labels identical across each model's five seeds. Reconstructed three binary signals from the original market_input.csv Close using the real preceding market trading date relative to each validation forecast date, NOT the preceding prediction row. Pearson correlation of probability score versus binary signal, and empirical ROC AUC versus saved Y_true.

| Market | n | Mean Validation AUC | Mean r Persistence | Mean r 200DMA | Mean r Momentum60 | Negative r 200DMA models |
|---|---:|---:|---:|---:|---:|---:|
| SP500 | 637 | 0.60882124589 | -0.20971008933 | -0.03214871981 | -0.05068499922 | 4/8 |
| NASDAQ100 | 637 | 0.65294083794 | -0.42497029498 | +0.06154692412 | -0.16025128792 | 3/8 |
| NIKKEI225 | 608 | 0.67847599638 | +0.03121276790 | -0.10205606212 | +0.03807998833 | 7/8 |
| EUROSTOXX50 | 635 | 0.61185979408 | -0.27388401177 | -0.56908977532 | -0.40668624612 | 8/8 |
| KOSPI200 | 622 | 0.67586115947 | -0.24899454369 | -0.24810959769 | -0.32875958764 | 7/8 |

Grand mean Validation ROC AUC: **0.64559180675** (matches v12 archived 0.646 rounding). Negative correlations across the 40 selected model-market cases: Persistence **34/40**, 200DMA **29/40**, Momentum60 **31/40**.

Contrast: the corrected held-out Test 200DMA correlation is negative for **35/40**, with market means -0.475 SP500, -0.379 NASDAQ100, -0.407 Nikkei, -0.458 EUROSTOXX50, -0.205 KOSPI200. Validation 200DMA signs are mixed particularly in SP500 and NASDAQ100, not universally inverse. The claim that every model learned the same inverse 200DMA alignment already in validation is **not supported**. No causal attribution of learning mechanism is warranted. The Validation AUC is selection-conditioned and not an independent prospective skill estimate.

**Scope limitation:** This A1 computes point estimates; validation alignment block CI and exact pairwise model-level validation-to-test change CI were not computed. The 40-row full-precision CSV and Excel produced with this audit are available as conversation attachments. A2/A3/A4/A5 remain separate checks and are not implied complete by this A1 record.
