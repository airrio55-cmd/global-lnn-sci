# Phase 2 architecture expansion



All losses/thresholds were frozen using validation only before final fits. Existing artifacts and Phase1 outputs are byte-unchanged. No final Holm correction or DM/GW/MCS analysis was executed.



The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence.



## Market results (3-of-5 majority; seed means are reported separately)



| Market      | Model          | Selected_Loss   |   Test_BA |   Macro_F1 |   Forecast_Up_Rate |   Mean_seed_Test_BA |   Economic_CAGR_10bps |   Economic_Exposure |
|:------------|:---------------|:----------------|----------:|-----------:|-------------------:|--------------------:|----------------------:|--------------------:|
| SP500       | CfC            | MILD_WCE        |  0.416811 |   0.269867 |         0.122534   |            0.42674  |           -0.0501592  |          0.120163   |
| SP500       | PE-Transformer | MILD_WCE        |  0.388747 |   0.322687 |         0.268951   |            0.424306 |           -0.0363597  |          0.263747   |
| NASDAQ100   | CfC            | MILD_WCE        |  0.442928 |   0.264295 |         0.0820353  |            0.445397 |           -0.0460037  |          0.0804481  |
| NASDAQ100   | PE-Transformer | MILD_FOCAL      |  0.490533 |   0.490232 |         0.634476   |            0.503659 |            0.0624586  |          0.64053    |
| NIKKEI225   | CfC            | MILD_WCE        |  0.50519  |   0.288912 |         0.00639659 |            0.502769 |           -0.00218239 |          0.00626959 |
| NIKKEI225   | PE-Transformer | MILD_WCE        |  0.51979  |   0.422939 |         0.185501   |            0.527272 |            0.0982835  |          0.181818   |
| EUROSTOXX50 | CfC            | MILD_FOCAL      |  0.463988 |   0.388008 |         0.189834   |            0.476567 |           -0.0341508  |          0.186165   |
| EUROSTOXX50 | PE-Transformer | CE              |  0.478051 |   0.37236  |         0.129668   |            0.485036 |            0.0143135  |          0.127162   |
| KOSPI200    | CfC            | MILD_WCE        |  0.5      |   0.361339 |         1          |            0.503774 |            0.144716   |          0.998952   |
| KOSPI200    | PE-Transformer | CE              |  0.512315 |   0.387862 |         0.989305   |            0.542827 |            0.151906   |          0.98847    |



## Architecture sensitivity



| Market      |    Delta_BA |   Delta_Macro_F1 |
|:------------|------------:|-----------------:|
| SP500       | -0.0312446  |       -0.141777  |
| NASDAQ100   | -0.0363559  |       -0.0123702 |
| NIKKEI225   | -0.012673   |       -0.0826441 |
| EUROSTOXX50 | -0.036185   |        0.0063943 |
| KOSPI200    | -0.00901878 |       -0.0825654 |



| Market      |    Delta_BA |   Delta_Macro_F1 |
|:------------|------------:|-----------------:|
| SP500       | -0.0524999  |       -0.0686868 |
| NASDAQ100   |  0.0297383  |        0.207379  |
| NIKKEI225   |  0.0139658  |        0.10454   |
| EUROSTOXX50 |  0.00373573 |       -0.0115592 |
| KOSPI200    | -0.0111978  |       -0.0349854 |



## Research questions

1. CfC vs LTC: majority BA differences range from -0.0364 to -0.0090; descriptive architecture sensitivity, not a materiality test.

2. CfC exceeds LTC majority BA in 0/5 markets; this does not establish consistent multiplicity-aware superiority.

3. Positional encoding changes majority BA by -0.0525 to 0.0297; original Transformer is retained.

4. Forecast-frequency diagnostics retain all near-constant outcomes; compare original and PE rates in the paired table, without excluding or retuning.

5. KOSPI architecture sensitivity (not a replication target): [{"Market":"KOSPI200","Original_model":"Transformer","Added_model":"PE-Transformer","Original_Selected_Loss":"MILD_FOCAL","Added_Selected_Loss":"CE","Original_Validation_BA":0.6603027905,"Added_Validation_BA":0.6582950889,"Original_Mean_seed_Test_BA":0.5157127958,"Added_Mean_seed_Test_BA":0.5428273441,"Original_Test_BA":0.5235130882,"Added_Test_BA":0.5123152709,"Original_Macro_F1":0.4228477488,"Added_Macro_F1":0.3878623955,"Original_Forecast_Up_Rate":0.9625668449,"Added_Forecast_Up_Rate":0.9893048128,"Original_Test_Accuracy":0.5839572193,"Added_Test_Accuracy":0.5764705882,"Original_PT_statistic":3.7567597035,"Added_PT_statistic":3.6310491336,"Original_PT_raw_p":0.0001721276,"Added_PT_raw_p":0.0002822714,"Delta_BA":-0.0111978172,"Delta_Macro_F1":-0.0349853533}]

6. There are 1 positive conventional two-sided raw PT p<0.05 exceptions among the10 new comparisons. Raw tests with overlapping H20 labels do not establish stable positive evidence; final family correction is deferred.

7. Phase0/step20 metrics and PT are retained in nonoverlap_results_phase2.csv. No favorable phase search or independence claim is made.

8. Economic CAGR must be read with exposure, turnover and buy-and-hold in the benchmark table. Positive long/cash returns alone do not identify timing skill; this phase does not test economic significance.

9. Six-neural majority Friedman diagnostics: [{"Metric": "majority_Test_BA", "Friedman_statistic": 9.457142857142856, "raw_p": 0.09216179231921805, "Kendall_W": 0.3782857142857142, "Market_blocks": 5, "Architectures": 6, "Diagnostic_only": true}, {"Metric": "majority_Macro_F1", "Friedman_statistic": 6.942857142857136, "raw_p": 0.22492490440795657, "Kendall_W": 0.2777142857142854, "Market_blocks": 5, "Architectures": 6, "Diagnostic_only": true}]. Only five blocks: non-significance is not equivalence; significance is not dominance.

10. Interpret changes jointly as architecture-sensitive and benchmark-sensitive apparent advantages; isolated raw signals are statistically fragile rather than evidence that evaluation design no longer matters.

11. No stable cross-market dominance is established by this descriptive analysis or raw p-values.

12. Phase3 should use the fixed six-neural/eight-learned universe and the explicit30/40/5/5 family proposals. Freeze paired-test and DM/GW/MCS loss/differential definitions before execution.
