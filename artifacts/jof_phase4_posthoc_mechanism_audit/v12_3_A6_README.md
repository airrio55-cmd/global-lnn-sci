# v12.3 A6 timing reconciliation — interim diagnostic, NOT PASSED

Protocol lock: 88f1acbc5dff7067966478f6c80c82ae9f2a00e2. Diagnostic CSV: v12_3_A6_phase3_vs_archive_diagnostic.csv.

The 2022–2025 Phase 3 frozen scoring panels were independently read for all five markets. There are no duplicated dates, dates are increasing, and all observed outcomes are binary. Panel rows: SP500 963; NASDAQ100 963; NIKKEI225 938; EUROSTOXX50 964; KOSPI200 935.

For each of the ten market × (200DMA, Momentum60) cells, Delta P was recomputed from: (i) signal and y on the same Phase 3 row, and (ii) preceding stored Phase 3 row's signal versus current y (first outcome row excluded). The archived v12 Test_Effect is *not* reproduced exactly by either convention for any of ten pairs. Hence pure one-row shifting alone does not explain all discrepancies. This is NOT evidence that the archive is wrong: source prices, precise signal construction, horizon-endpoint exclusion, common-cutoff procedure, date intersection and calendar handling must be audited before adjudication. The average absolute difference between archived and preceding-row Phase 3 effects is approximately 0.00164, not zero.

The Phase 3 scoring data are **not known to contain the same prior-information-cutoff rule series as the newer Phase 4 v12 recomputation**. We must not rename a phase-3 same-row series t−1 without independent verification. Consequently v12.1/v12.2 lagged-row correlations, stratified AUC and regressions are descriptive exploratory reconstructions subject to this timing audit. Their signs may be informative but precise estimates and substantive inference are NOT FINAL.

Next within locked A6: reproduce rule generation from frozen market input on both archives, align actual source trading dates rather than row offsets, verify forecast origin versus 20-day forward label endpoints, compare the exact common date intersection, exclusions and binary tie definitions. Only then set A6 PASS and reuse the exact rule series for A1–A5. No additional mechanism hypotheses permitted.
