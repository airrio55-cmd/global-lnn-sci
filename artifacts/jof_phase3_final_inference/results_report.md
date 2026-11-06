# JOF Phase3 final statistical inference

This analysis uses only frozen saved predictions. No model was trained or tuned. The final universe contains six neural architectures, two other learned models and five deterministic benchmarks. All family memberships, test definitions and bootstrap settings were fixed before calculations.

## Core interpretation

Primary loss is Brier. For d=loss_model-loss_benchmark, negative favors the learned model and positive favors the benchmark. Probabilistic learned-model loss uses the equal-weight mean of five saved seed probabilities; directional statistics use the unchanged majority labels. These evaluate different forecast objects. Rule probabilities are their deterministic0/1 outputs, so Brier comparisons can favor softer probability forecasts without demonstrating directional superiority.

All conventional full-sample tests have an H20 overlapping-label caveat. HAC19 and stationary blocks with expected length20 are prespecified approximations, not proof that all dependence is removed.

Reduced-overlap evaluation lowers mechanical label overlap but does not establish statistical independence and substantially reduces sample size.

## Fourteen research questions

1. Learned models with positive Holm40-adjusted PT support:

| Market   | Model          |   PT_stat |   raw_p |   Holm40_p |   Forecast_Up_Rate |
|:---------|:---------------|----------:|--------:|-----------:|-------------------:|
| KOSPI200 | Transformer    |    3.7568 |  0.0002 |     0.0059 |             0.9626 |
| KOSPI200 | PE-Transformer |    3.6310 |  0.0003 |     0.0088 |             0.9893 |

Neural-only Holm30 support:

| Market   | Model          |   Holm30_p |
|:---------|:---------------|-----------:|
| KOSPI200 | Transformer    |     0.0043 |
| KOSPI200 | PE-Transformer |     0.0062 |

2. Positive signals by model across five markets:

| Model              |   Positive_PT_raw |   Positive_PT_Holm40 |   Positive_PT_Holm30 |
|:-------------------|------------------:|---------------------:|---------------------:|
| LNN                |                 0 |                    0 |               0.0000 |
| CfC                |                 0 |                    0 |               0.0000 |
| LSTM               |                 1 |                    0 |               0.0000 |
| GRU                |                 0 |                    0 |               0.0000 |
| Transformer        |                 1 |                    1 |               1.0000 |
| PE-Transformer     |                 1 |                    1 |               1.0000 |
| LogisticRegression |                 1 |                    0 |             nan      |
| LightGBM           |                 1 |                    0 |             nan      |

An isolated positive exception is not stable cross-market evidence. Significant negative association is reported separately and never counted as skill.

3. Brier wins against Persistence after the fixed40-test Holm family:

| Market      | Model_A            |   Mean_differential |   Benchmark_family_Holm_p |
|:------------|:-------------------|--------------------:|--------------------------:|
| NASDAQ100   | PE-Transformer     |             -0.1608 |                    0.0372 |
| NIKKEI225   | Transformer        |             -0.2042 |                    0.0120 |
| NIKKEI225   | PE-Transformer     |             -0.2067 |                    0.0254 |
| EUROSTOXX50 | LNN                |             -0.2107 |                    0.0004 |
| EUROSTOXX50 | CfC                |             -0.2638 |                    0.0000 |
| EUROSTOXX50 | PE-Transformer     |             -0.1807 |                    0.0168 |
| EUROSTOXX50 | LightGBM           |             -0.1812 |                    0.0167 |
| KOSPI200    | CfC                |             -0.1939 |                    0.0012 |
| KOSPI200    | Transformer        |             -0.2433 |                    0.0000 |
| KOSPI200    | PE-Transformer     |             -0.2298 |                    0.0000 |
| KOSPI200    | LogisticRegression |             -0.1840 |                    0.0062 |

4. Brier wins against200DMA after its separate40-test Holm family:

| Market      | Model_A        |   Mean_differential |   Benchmark_family_Holm_p |
|:------------|:---------------|--------------------:|--------------------------:|
| EUROSTOXX50 | CfC            |             -0.1943 |                    0.0124 |
| KOSPI200    | Transformer    |             -0.2134 |                    0.0036 |
| KOSPI200    | PE-Transformer |             -0.1999 |                    0.0188 |

5. Brier wins against Momentum60 after its separate40-test Holm family:

| Market      | Model_A   |   Mean_differential |   Benchmark_family_Holm_p |
|:------------|:----------|--------------------:|--------------------------:|
| EUROSTOXX50 | CfC       |             -0.2150 |                    0.0008 |

6. Original Transformer vs PE-Transformer: positive mean differential favors PE, negative favors original. Architecture-sensitive differences use the prespecified five-market DM Holm family; isolated significance is not cross-market superiority.

| Market      |   Mean_differential |   raw_two_sided_p |   Holm5_p | Favors_PE   |
|:------------|--------------------:|------------------:|----------:|:------------|
| SP500       |             -0.0053 |            0.5115 |    1.0000 | False       |
| NASDAQ100   |              0.0102 |            0.0192 |    0.0766 | True        |
| NIKKEI225   |              0.0025 |            0.8468 |    1.0000 | True        |
| EUROSTOXX50 |              0.0422 |            0.0000 |    0.0001 | True        |
| KOSPI200    |             -0.0135 |            0.3566 |    1.0000 | False       |

7. CfC vs LTC: the fixed benchmark/PT results for each are below. This is descriptive of inferential advantage, with no additional outcome-selected CfC-vs-LTC family.

| Market      | Model   |     BA |   PT_Holm40 |   DM_vs_Persistence_Holm |   DM_vs_Persistence_mean_differential |
|:------------|:--------|-------:|------------:|-------------------------:|--------------------------------------:|
| SP500       | LNN     | 0.4481 |      0.0441 |                   1.0000 |                               -0.0459 |
| SP500       | CfC     | 0.4168 |      0.0000 |                   0.8301 |                               -0.1190 |
| NASDAQ100   | LNN     | 0.4793 |      0.1605 |                   1.0000 |                                0.0828 |
| NASDAQ100   | CfC     | 0.4429 |      0.0000 |                   0.9439 |                               -0.1102 |
| NIKKEI225   | LNN     | 0.5179 |      1.0000 |                   1.0000 |                               -0.0244 |
| NIKKEI225   | CfC     | 0.5052 |      0.8897 |                   0.1598 |                               -0.1677 |
| EUROSTOXX50 | LNN     | 0.5002 |      1.0000 |                   0.0004 |                               -0.2107 |
| EUROSTOXX50 | CfC     | 0.4640 |      0.1212 |                   0.0000 |                               -0.2638 |
| KOSPI200    | LNN     | 0.5090 |      1.0000 |                   0.9583 |                               -0.0998 |
| KOSPI200    | CfC     | 0.5000 |    nan      |                   0.0012 |                               -0.1939 |

8. MCS membership (Brier, eleven fixed candidates):

| Market      | MCS90_retained                                                           | MCS90_eliminated                                                                                   | MCS95_retained                                                                       | Interpretation                                                                   |
|:------------|:-------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| SP500       | CfC,Momentum60,Rule_200DMA,PE-Transformer,Transformer,LogisticRegression | LightGBM,GRU,LSTM,LNN,Persistence                                                                  | Persistence,CfC,Momentum60,Rule_200DMA,PE-Transformer,Transformer,LogisticRegression | The MCS procedure did not eliminate these models at the stated confidence level. |
| NASDAQ100   | Rule_200DMA,PE-Transformer                                               | LNN,GRU,LSTM,LightGBM,CfC,LogisticRegression,Persistence,Momentum60,Transformer                    | Rule_200DMA,PE-Transformer                                                           | The MCS procedure did not eliminate these models at the stated confidence level. |
| NIKKEI225   | Transformer,PE-Transformer                                               | LSTM,GRU,LightGBM,LogisticRegression,LNN,Persistence,CfC,Momentum60,Rule_200DMA                    | Transformer,PE-Transformer                                                           | The MCS procedure did not eliminate these models at the stated confidence level. |
| EUROSTOXX50 | LNN,CfC                                                                  | GRU,Persistence,LogisticRegression,Transformer,LSTM,PE-Transformer,Momentum60,LightGBM,Rule_200DMA | LNN,CfC                                                                              | The MCS procedure did not eliminate these models at the stated confidence level. |
| KOSPI200    | PE-Transformer,Transformer                                               | Persistence,GRU,LightGBM,LNN,LSTM,Rule_200DMA,Momentum60,LogisticRegression,CfC                    | PE-Transformer,Transformer                                                           | The MCS procedure did not eliminate these models at the stated confidence level. |

The MCS procedure did not eliminate these models at the stated confidence level. Retention does not establish equality or identify a winner set.

9. SPA against Persistence:

| Market      |   SPA_statistic |   p_value | Reject_at_0_05   | Best_mean_improvement_model   |
|:------------|----------------:|----------:|:-----------------|:------------------------------|
| SP500       |          2.7140 |    0.0135 | True             | LogisticRegression            |
| NASDAQ100   |          3.0987 |    0.0031 | True             | PE-Transformer                |
| NIKKEI225   |          3.1826 |    0.0013 | True             | PE-Transformer                |
| EUROSTOXX50 |          6.3595 |    0.0001 | True             | CfC                           |
| KOSPI200    |          6.5459 |    0.0001 | True             | Transformer                   |

SPA tests whether the benchmark can be rejected against the set of alternatives. Rejection does not identify every superior alternative; the best mean differential model is descriptive.

10. Reduced-overlap primary Persistence contrasts (raw small-sample diagnostics):

| Market      | Model              |   N |   Mean_differential |   raw_p | Status   |
|:------------|:-------------------|----:|--------------------:|--------:|:---------|
| SP500       | LNN                |  49 |              0.0564 |  0.5744 | defined  |
| SP500       | CfC                |  49 |             -0.0522 |  0.5200 | defined  |
| SP500       | LSTM               |  49 |              0.1350 |  0.1718 | defined  |
| SP500       | GRU                |  49 |              0.1407 |  0.1376 | defined  |
| SP500       | Transformer        |  49 |             -0.0814 |  0.2823 | defined  |
| SP500       | PE-Transformer     |  49 |             -0.0842 |  0.2700 | defined  |
| SP500       | LogisticRegression |  49 |             -0.0722 |  0.3808 | defined  |
| SP500       | LightGBM           |  49 |              0.1683 |  0.0951 | defined  |
| NASDAQ100   | LNN                |  49 |              0.0604 |  0.5237 | defined  |
| NASDAQ100   | CfC                |  49 |             -0.1078 |  0.1938 | defined  |
| NASDAQ100   | LSTM               |  49 |              0.1257 |  0.2262 | defined  |
| NASDAQ100   | GRU                |  49 |              0.2225 |  0.0510 | defined  |
| NASDAQ100   | Transformer        |  49 |             -0.1470 |  0.0619 | defined  |
| NASDAQ100   | PE-Transformer     |  49 |             -0.1620 |  0.0348 | defined  |
| NASDAQ100   | LogisticRegression |  49 |             -0.0479 |  0.6504 | defined  |
| NASDAQ100   | LightGBM           |  49 |              0.0465 |  0.6638 | defined  |
| NIKKEI225   | LNN                |  47 |             -0.0801 |  0.5041 | defined  |
| NIKKEI225   | CfC                |  47 |             -0.2055 |  0.0272 | defined  |
| NIKKEI225   | LSTM               |  47 |             -0.0376 |  0.7386 | defined  |
| NIKKEI225   | GRU                |  47 |             -0.0220 |  0.8354 | defined  |
| NIKKEI225   | Transformer        |  47 |             -0.2440 |  0.0046 | defined  |
| NIKKEI225   | PE-Transformer     |  47 |             -0.2413 |  0.0070 | defined  |
| NIKKEI225   | LogisticRegression |  47 |             -0.0805 |  0.4501 | defined  |
| NIKKEI225   | LightGBM           |  47 |             -0.0589 |  0.5998 | defined  |
| EUROSTOXX50 | LNN                |  49 |             -0.0952 |  0.2533 | defined  |
| EUROSTOXX50 | CfC                |  49 |             -0.1356 |  0.0953 | defined  |
| EUROSTOXX50 | LSTM               |  49 |              0.0733 |  0.5141 | defined  |
| EUROSTOXX50 | GRU                |  49 |              0.1670 |  0.1447 | defined  |
| EUROSTOXX50 | Transformer        |  49 |              0.0138 |  0.8871 | defined  |
| EUROSTOXX50 | PE-Transformer     |  49 |             -0.0291 |  0.7497 | defined  |
| EUROSTOXX50 | LogisticRegression |  49 |              0.1198 |  0.2682 | defined  |
| EUROSTOXX50 | LightGBM           |  49 |             -0.0435 |  0.6392 | defined  |
| KOSPI200    | LNN                |  47 |             -0.1363 |  0.1289 | defined  |
| KOSPI200    | CfC                |  47 |             -0.2411 |  0.0032 | defined  |
| KOSPI200    | LSTM               |  47 |             -0.1849 |  0.0302 | defined  |
| KOSPI200    | GRU                |  47 |             -0.1676 |  0.0597 | defined  |
| KOSPI200    | Transformer        |  47 |             -0.2491 |  0.0016 | defined  |
| KOSPI200    | PE-Transformer     |  47 |             -0.2638 |  0.0009 | defined  |
| KOSPI200    | LogisticRegression |  47 |             -0.2424 |  0.0043 | defined  |
| KOSPI200    | LightGBM           |  47 |             -0.1542 |  0.0806 | defined  |

Loss of significance can reflect reduced power and dependence sensitivity; it does not alone prove an original result was invalid. Descriptive reduced-overlap MCS was not run because all N are below the prespecified100-observation minimum.

11. Statistically favorable models and frequency warnings:

| Market      | Model              |   Forecast_Up_Rate | near_constant_warning   |
|:------------|:-------------------|-------------------:|:------------------------|
| NASDAQ100   | PE-Transformer     |             0.6345 | False                   |
| NIKKEI225   | Transformer        |             0.0405 | True                    |
| NIKKEI225   | PE-Transformer     |             0.1855 | False                   |
| EUROSTOXX50 | LNN                |             0.9741 | True                    |
| EUROSTOXX50 | CfC                |             0.1898 | False                   |
| EUROSTOXX50 | PE-Transformer     |             0.1297 | False                   |
| EUROSTOXX50 | LightGBM           |             0.4710 | False                   |
| KOSPI200    | CfC                |             1.0000 | True                    |
| KOSPI200    | Transformer        |             0.9626 | True                    |
| KOSPI200    | PE-Transformer     |             0.9893 | True                    |
| KOSPI200    | LogisticRegression |             0.8299 | False                   |

A near-constant classification can coexist with varying probabilities. Neither is removed or retuned.

12. Economics of statistically favorable forecasts (existing10bps accounting):

| Market      | Model              |   Economic_CAGR_10bps |   Sharpe_10bps |   Exposure |   Turnover_10bps | exposure_warning   |
|:------------|:-------------------|----------------------:|---------------:|-----------:|-----------------:|:-------------------|
| NASDAQ100   | PE-Transformer     |                0.0625 |         0.4190 |     0.6405 |               76 | False              |
| NIKKEI225   | Transformer        |                0.0010 |         0.0462 |     0.0397 |                8 | True               |
| NIKKEI225   | PE-Transformer     |                0.0983 |         1.0464 |     0.1818 |               40 | False              |
| EUROSTOXX50 | LNN                |                0.0788 |         0.5318 |     0.9736 |               12 | True               |
| EUROSTOXX50 | CfC                |               -0.0342 |        -0.3044 |     0.1862 |               26 | False              |
| EUROSTOXX50 | PE-Transformer     |                0.0143 |         0.1971 |     0.1272 |               16 | False              |
| EUROSTOXX50 | LightGBM           |                0.0278 |         0.2721 |     0.4619 |              110 | False              |
| KOSPI200    | CfC                |                0.1447 |         0.7729 |     0.9990 |                2 | True               |
| KOSPI200    | Transformer        |                0.1494 |         0.8010 |     0.9623 |               18 | True               |
| KOSPI200    | PE-Transformer     |                0.1519 |         0.8063 |     0.9885 |                8 | True               |
| KOSPI200    | LogisticRegression |                0.0979 |         0.5943 |     0.8323 |              100 | False              |

Predictive-loss advantages do not establish economic advantages. No economic significance test is added here; extreme exposure may reflect persistent exposure or market avoidance.

13. Cross-market summary:

| Model              |   Mean_BA |   Mean_Macro_F1 |   Average_BA_rank_all13 |   Markets_BA_above0_5 |   Markets_BA_above_Persistence |   Positive_PT_raw |   Positive_PT_Holm40 |   Positive_PT_Holm30 |   DM_wins_vs_Persistence_Holm |   DM_wins_vs_200DMA_Holm |   DM_wins_vs_Momentum60_Holm |   MCS90_inclusions |   Near_constant_markets |   Average_exposure |
|:-------------------|----------:|----------------:|------------------------:|----------------------:|-------------------------------:|------------------:|---------------------:|---------------------:|------------------------------:|-------------------------:|-----------------------------:|-------------------:|------------------------:|-------------------:|
| LNN                |    0.4909 |          0.3771 |                  5.0000 |                     3 |                              3 |                 0 |                    0 |               0.0000 |                             1 |                        0 |                            0 |                  1 |                       3 |             0.4756 |
| CfC                |    0.4658 |          0.3145 |                 10.6000 |                     1 |                              2 |                 0 |                    0 |               0.0000 |                             2 |                        1 |                            1 |                  2 |                       3 |             0.2784 |
| LSTM               |    0.4864 |          0.3890 |                  5.8000 |                     3 |                              3 |                 1 |                    0 |               0.0000 |                             0 |                        0 |                            0 |                  0 |                       1 |             0.3692 |
| GRU                |    0.4678 |          0.3620 |                  9.6000 |                     1 |                              2 |                 0 |                    0 |               0.0000 |                             0 |                        0 |                            0 |                  0 |                       2 |             0.3893 |
| Transformer        |    0.4811 |          0.3599 |                  7.4000 |                     2 |                              3 |                 1 |                    1 |               1.0000 |                             2 |                        1 |                            0 |                  3 |                       3 |             0.3120 |
| PE-Transformer     |    0.4779 |          0.3992 |                  7.2000 |                     2 |                              3 |                 1 |                    1 |               1.0000 |                             4 |                        1 |                            0 |                  4 |                       1 |             0.4403 |
| LogisticRegression |    0.4831 |          0.3791 |                  7.6000 |                     1 |                              3 |                 1 |                    0 |             nan      |                             1 |                        0 |                            0 |                  1 |                       1 |             0.2956 |
| LightGBM           |    0.4769 |          0.3939 |                  8.2000 |                     2 |                              3 |                 1 |                    0 |             nan      |                             1 |                        0 |                            0 |                  0 |                       2 |             0.4263 |

No stable cross-market dominance is established by this table. Ranks are descriptive; raw conditional GW rejections alone are not superiority claims.

14. The evidence must be read jointly as benchmark-sensitive, architecture-sensitive, dependence-sensitive and multiplicity-sensitive. Isolated favorable findings are statistically fragile rather than universal superiority. The design thesis is assessed through the changes across fixed diagnostics below, not by treating every significant raw p-value as support.

| Final_assessment               |   Rows |
|:-------------------------------|-------:|
| benchmark-sensitive            |      7 |
| dependence-sensitive           |      4 |
| isolated descriptive advantage |      7 |
| multiplicity-sensitive         |      2 |
| no positive evidence           |     20 |

## Significant negative PT associations

| Market    | Model              |   PT_stat |   Holm40_p |   Forecast_Up_Rate |
|:----------|:-------------------|----------:|-----------:|-------------------:|
| SP500     | LNN                |   -3.1608 |     0.0441 |             0.3718 |
| SP500     | CfC                |   -7.4605 |     0.0000 |             0.1225 |
| SP500     | LSTM               |   -3.7268 |     0.0064 |             0.4943 |
| SP500     | GRU                |   -6.5394 |     0.0000 |             0.5992 |
| SP500     | Transformer        |   -3.6857 |     0.0073 |             0.3261 |
| SP500     | PE-Transformer     |   -7.3781 |     0.0000 |             0.2690 |
| SP500     | LogisticRegression |   -3.3930 |     0.0207 |             0.2295 |
| SP500     | LightGBM           |   -4.6325 |     0.0001 |             0.3967 |
| NASDAQ100 | CfC                |   -6.0974 |     0.0000 |             0.0820 |
| NASDAQ100 | Transformer        |   -4.1412 |     0.0012 |             0.0841 |
| NASDAQ100 | LightGBM           |   -3.3079 |     0.0273 |             0.2565 |

## Inference limitations

Only five market blocks exist, learned configurations were validation-selected, and all diagnostics reuse the same test observations. They are not independent confirmations. Original training is expanding rather than the fixed rolling window assumed in some GW theory; our reported GW-style conditional moment Wald test is a precisely specified robustness diagnostic, not exact original GW. It conditions on resolved historical losses, so its sample starts later. Monthly regimes were not refit. Log loss is secondary and learned-only, with unadjusted pairwise results stored without superiority claims. Bootstrap p-values are Monte Carlo approximations conditional on a fixed expected block length20; block-length sensitivity is not searched.
