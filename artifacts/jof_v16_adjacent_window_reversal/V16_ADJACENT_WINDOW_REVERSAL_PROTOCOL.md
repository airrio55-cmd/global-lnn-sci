# V16 Pre-specified Model-Free Adjacent-Window Reversal Test

**Status:** LOCKED at the Git commit that adds this file together with `v16_locked.py` and `v16_fetch_data.py`. That commit precedes any V16 data download. The lock's SHA and UTC timestamp are in the Git history, and the content is immutable after the lock.

## 1. Purpose and prior knowledge

V14 and V15 related learners' changes in discrimination to shifts in trend-signal relations. Combining their unit-level outputs after both runs had finished (an explicitly post-hoc analysis) suggested a model-free regularity: the conditional payoff of a trend signal in one two-year window tends to be **negatively** related to its payoff in the next two-year window. If that holds, validation-period relations would systematically mislead any learner, whatever its architecture.

On the 2013–2021 rolling-origin windows of the five study markets, these were the post-hoc Spearman correlations between the validation-window effect and the test-window effect:

| Signal | ρ | N |
|---|---|---|
| 200DMA | −0.453 | 28 |
| Persistence | −0.514 | 30 |
| Momentum60 | −0.262 | 30 |

Those windows overlap, and the hypothesis was formed from them. **V16 is the first test of this hypothesis on data that did not form it**: six markets new to the study and pre-2010 history for the original five markets. The test is model-free. It fits no model and does not test any learner directly; any link to learner behavior is an interpretation.

What had already been seen when this protocol was drafted:
- the original 2010–2025 frozen inputs of the five study markets, together with all V14/V15 results derived from them;
- no index data before 2010 in any analysis by the authors that we know of;
- no data for the six Sample A markets in this project.

Any later evidence of prior exposure must be disclosed.

## 2. Data (one-time freeze)

- **Source:** Yahoo Finance daily index closes via `yfinance` (`auto_adjust=False`, field `Close`), retrieved once by `v16_fetch_data.py` for 1996-01-01 to 2022-01-30. File hashes, retrieval time and software versions go in `v16_data_manifest.json`. The data folder is committed before `v16_locked.py` runs in full mode.
- **Not point-in-time:** Yahoo histories are not point-in-time vintages, and missing sessions are never filled. Rows with missing or non-positive closes are dropped, and duplicate dates keep their first occurrence.
- **Sample A (new markets, blocks B1–B12):**

  | Market | Ticker |
  |---|---|
  | FTSE 100 | ^FTSE |
  | DAX | ^GDAXI |
  | Hang Seng | ^HSI |
  | S&P/TSX | ^GSPTSE |
  | S&P/ASX 200 | ^AXJO |
  | TAIEX | ^TWII |

- **Sample B (study markets, blocks B1–B6 only, ending 2009):**

  | Market | Ticker |
  |---|---|
  | S&P 500 | ^GSPC |
  | NASDAQ-100 | ^NDX |
  | Nikkei 225 | ^N225 |
  | EURO STOXX 50 | ^STOXX50E |
  | KOSPI 200 | ^KS200 |

- **Excluded periods:** no observation from 2010 onwards is used for Sample B, and no observation from 2022 onwards is used for any market. The 2022–2025 period that motivated the study is therefore excluded throughout.

## 3. Windows

- **Blocks:** twelve fixed two-year calendar blocks, B1 = 1998–1999, B2 = 2000–2001, …, B12 = 2020–2021.
- **Pairs:** six disjoint adjacent pairs, P1 = (B1, B2), P2 = (B3, B4), …, P6 = (B11, B12). Each block belongs to exactly one pair, so no two pairs share data.
- **Planned pairs:** Sample A has 6 per market; Sample B has P1–P3 per market. That gives 36 + 15 = **51 planned pairs**.
- **Block eligibility** (decided from dates only). A block is eligible if:
  - at least 200 sessions precede its first session;
  - its first session is on or before 15 January of its first year, and its last session is on or after 15 December of its second year;
  - no gap between consecutive sessions inside it exceeds 15 calendar days.
- **Pair eligibility:** a pair is evaluable for a signal only if both of its blocks are eligible and both effects are defined. Missing pairs are reported with reasons and are never replaced.

## 4. Variables (identical to V14 signal definitions)

On each market's observed session index:

- **Target** at forecast date *t*: y = 1[Close(t+20) > Close(t)], with ties set to 0.
- **Signals**, all computed at t−1:
  - Persistence = 1[C(t−1) > C(t−21)]
  - 200DMA = 1[C(t−1) > mean(C(t−200)…C(t−1))]
  - Momentum60 = 1[C(t−1) > C(t−61)]
- **Eligible forecast dates:** t lies in the block, and t+20 lies in the same block. Inputs may use sessions before the block.
- **Block effect:** E_b(s) = P(y=1 | s=1) − P(y=1 | s=0) over the block's eligible dates. E is undefined if either signal group has fewer than 20 dates.

## 5. Hypotheses

**H1 (sole primary hypothesis):** across all evaluable pairs, Spearman ρ[E_first(200DMA), E_second(200DMA)] < 0.

**H2 (secondary):** the same test for Persistence and for Momentum60, with a Holm correction across these two.

**Inference.** The primary test is a nominal one-sided within-market permutation p-value:
- E_second is shuffled among each market's own evaluable pairs;
- 10,000 draws, seed 20261116;
- p = (1 + #{ρ_perm ≤ ρ_obs}) / 10,001.

Pairs are disjoint in time, but markets share calendar shocks. The permutation is therefore a non-exact diagnostic, and its p-value is reported as nominal, never as confirmatory.

**Pre-specified sensitivities**, each reported for all three signals whatever its sign:
1. Calendar-demeaned ρ: each E minus the cross-market mean E of the same block. This removes common calendar shocks.
2. Market-centered ρ.
3. Sample A only and Sample B only.
4. The range of pooled ρ when leaving out one market at a time, and when leaving out one pair position (P1–P6) at a time.
5. Within-market ρ for markets with at least 4 evaluable pairs, reported as the count of negative values.
6. The fraction of pairs whose effect changes sign.

**Pre-lock design check (synthetic data only).** No real data were used for this check. `v16_locked.py` was run on simulated random-walk prices with the same market and block layout. In 60 replicates with no true relation, the pooled 200DMA ρ had mean −0.023 and SD 0.157, so the design does not create a negative correlation mechanically. A full synthetic run took about 11 seconds and correctly excluded blocks that had late series starts or 42-day gaps.

## 6. Decision labels (as in V14 §9)

H1 is labeled as follows:
- **ρ < 0 and p < .05:** "Nominally supported under a non-exact permutation diagnostic".
- **ρ < 0 and p ≥ .05:** "Directionally consistent, nominally non-significant".
- **ρ ≥ 0:** "Not supported in direction".

The label always carries "evaluated on N of 51 planned pairs". It is also qualified when the calendar-demeaned sensitivity disagrees in sign; the sensitivity is reported next to the label rather than replacing it. Secondary results never change the H1 label. All results are reported, whatever their sign.

## 7. Execution sequence

1. **Lock:** commit this protocol, `v16_locked.py` and `v16_fetch_data.py` (this commit), and record the SHA.
2. **Freeze data:** run `v16_fetch_data.py` once and commit the data folder and manifest, without opening any effect.
3. **Preflight:** run `v16_locked.py --preflight`. It records the inventory, block eligibility and signal-group counts, and never computes y.
4. **Commit the preflight output.**
5. **Analyse:** run `v16_locked.py` once and commit every output unchanged.

Steps 2–5 run in one GitHub Actions workflow, added in a separate commit after the lock. Each step commits its own output before the next step starts. The workflow log is kept as an artifact.

A code failure is fixed only by a documented change record that leaves the statistical functions intact, as in V15.2.

## 8. Reporting and use in the paper

- **Scope:** V16 is reported as a pre-specified, model-free, out-of-sample check of a hypothesis formed post hoc. It is not described as prospective, causal or as a test of any learner.
- **If H1 is nominally supported:** the manuscript may say that trend-signal relations tended to reverse between adjacent windows in markets and periods that played no part in forming the hypothesis.
- **If H1 is not supported:** the manuscript retains the in-sample observation only as a post-hoc description, or omits it. It does not search for alternative windows, signals or markets.
- **Fixed design:** block length, signals, markets, periods and thresholds may not be changed after the lock.
