# Journal of Forecasting Phase1 frozen benchmark expansion

All new settings were frozen before test evaluation.375 validation fits and validation-only selection preceded75 final fits. No existing model, prediction, HMM, economic artifact or original Holm15 is replaced.

## Validation-selected GRU and tabular configurations

|Market|Model|Selected loss/objective|Mean validation BA|
|---|---|---|---:|
|SP500|GRU|MILD_FOCAL|0.633595|
|SP500|LogisticRegression|L2|0.506440|
|SP500|LightGBM|Binary_logloss|0.484107|
|NASDAQ100|GRU|MILD_FOCAL|0.656356|
|NASDAQ100|LogisticRegression|L2|0.566559|
|NASDAQ100|LightGBM|Binary_logloss|0.518410|
|NIKKEI225|GRU|CE|0.670000|
|NIKKEI225|LogisticRegression|L2|0.535054|
|NIKKEI225|LightGBM|Binary_logloss|0.623641|
|EUROSTOXX50|GRU|CE|0.665359|
|EUROSTOXX50|LogisticRegression|L2|0.585519|
|EUROSTOXX50|LightGBM|Binary_logloss|0.529794|
|KOSPI200|GRU|CE|0.648654|
|KOSPI200|LogisticRegression|L2|0.619059|
|KOSPI200|LightGBM|Binary_logloss|0.538033|

## Primary operational benchmark comparison

Representative BA/Accuracy/MacroF1 use majority or deterministic consensus; five-seed mean BA is separate. No configuration is selected by this table.

|Market|Model|Loss|Validation BA|Test BA|Accuracy|Macro F1|Forecast Up|Actual Up|Delta BA vs Persistence|Nonoverlap BA|Economic exposure|10bps CAGR|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|SP500|GRU|MILD_FOCAL|0.633595|0.391019|0.434060|0.393162|0.599|0.660|-0.124055|0.259470|60.6%|2.98%|
|SP500|LogisticRegression|L2|0.506440|0.451481|0.369678|0.361947|0.229|0.660|-0.063593|0.373106|22.5%|3.23%|
|SP500|LightGBM|Binary_logloss|0.484107|0.422934|0.397715|0.395744|0.397|0.660|-0.092140|0.355114|38.9%|0.22%|
|SP500|LNN|MILD_FOCAL|0.603727|0.448056|0.412253|0.411644|0.372|0.660|-0.067019|0.339962|36.5%|2.48%|
|SP500|LSTM|MILD_FOCAL|0.617830|0.436638|0.441329|0.427627|0.494|0.660|-0.078436|0.323864|48.5%|0.47%|
|SP500|Transformer|MILD_FOCAL|0.636180|0.441247|0.391485|0.391374|0.326|0.660|-0.073827|0.356061|32.0%|-2.14%|
|SP500|Rule_200DMA|fixed_rule|0.455517|0.565518|0.628245|0.566674|0.717|0.660|+0.050444|0.551136|72.1%|6.28%|
|SP500|Momentum60|fixed_rule|0.438528|0.563600|0.617861|0.564532|0.690|0.660|+0.048526|0.613636|69.5%|9.19%|
|SP500|Persistence|baseline|0.425466|0.515074|0.558671|0.514657|0.641|0.660|+0.000000|0.567235|62.8%|6.13%|
|SP500|Always-Up|baseline|0.500000|0.500000|0.660436|0.397749|1.000|0.660|-0.015074|0.500000|99.9%|10.78%|
|SP500|Always-Down|baseline|0.500000|0.500000|0.339564|0.253488|0.000|0.660|-0.015074|0.500000|0.0%|0.00%|
|NASDAQ100|GRU|MILD_FOCAL|0.656356|0.471645|0.336449|0.290125|0.080|0.665|-0.060872|0.456801|7.8%|-8.91%|
|NASDAQ100|LogisticRegression|L2|0.566559|0.460074|0.386293|0.383033|0.263|0.665|-0.072443|0.417279|27.6%|0.54%|
|NASDAQ100|LightGBM|Binary_logloss|0.518410|0.450728|0.375909|0.371997|0.256|0.665|-0.081789|0.417279|25.2%|-2.67%|
|NASDAQ100|LNN|MILD_FOCAL|0.565535|0.479284|0.334372|0.276665|0.053|0.665|-0.053234|0.456801|5.2%|-3.76%|
|NASDAQ100|LSTM|MILD_FOCAL|0.668468|0.471747|0.343718|0.305822|0.102|0.665|-0.060771|0.443015|10.0%|-2.30%|
|NASDAQ100|Transformer|MILD_WCE|0.693409|0.460795|0.328141|0.282853|0.084|0.665|-0.071723|0.443015|8.2%|2.00%|
|NASDAQ100|Rule_200DMA|fixed_rule|0.459430|0.617383|0.669782|0.619853|0.698|0.665|+0.084866|0.610294|70.3%|15.88%|
|NASDAQ100|Momentum60|fixed_rule|0.390920|0.560512|0.605400|0.560109|0.656|0.665|+0.027994|0.579044|66.2%|10.69%|
|NASDAQ100|Persistence|baseline|0.406822|0.532517|0.577362|0.531938|0.647|0.665|+0.000000|0.534007|63.4%|10.46%|
|NASDAQ100|Always-Up|baseline|0.500000|0.500000|0.664590|0.399251|1.000|0.665|-0.032517|0.500000|99.9%|14.00%|
|NASDAQ100|Always-Down|baseline|0.500000|0.500000|0.335410|0.251166|0.000|0.665|-0.032517|0.500000|0.0%|0.00%|
|NIKKEI225|GRU|CE|0.670000|0.481863|0.404051|0.372919|0.161|0.616|+0.030594|0.430451|15.8%|4.43%|
|NIKKEI225|LogisticRegression|L2|0.535054|0.495309|0.380597|0.277044|0.005|0.616|+0.044041|0.500000|0.5%|0.89%|
|NIKKEI225|LightGBM|Binary_logloss|0.623641|0.515523|0.409382|0.333769|0.047|0.616|+0.064254|0.500940|4.6%|2.77%|
|NIKKEI225|LNN|MILD_WCE|0.639022|0.517863|0.423241|0.371556|0.097|0.616|+0.066595|0.509398|11.4%|5.72%|
|NIKKEI225|LSTM|MILD_FOCAL|0.686938|0.503085|0.414712|0.371104|0.120|0.616|+0.051817|0.483083|11.8%|9.45%|
|NIKKEI225|Transformer|MILD_FOCAL|0.714982|0.505825|0.398721|0.318398|0.041|0.616|+0.054556|0.491541|4.0%|0.10%|
|NIKKEI225|Rule_200DMA|fixed_rule|0.382880|0.456108|0.508529|0.447829|0.715|0.616|+0.004839|0.470865|72.0%|3.69%|
|NIKKEI225|Momentum60|fixed_rule|0.448732|0.488745|0.510661|0.488558|0.592|0.616|+0.037476|0.469925|59.9%|5.45%|
|NIKKEI225|Persistence|baseline|0.488496|0.451269|0.478678|0.451444|0.607|0.616|+0.000000|0.425752|59.5%|4.59%|
|NIKKEI225|Always-Up|baseline|0.500000|0.500000|0.616205|0.381266|1.000|0.616|+0.048731|0.500000|99.9%|17.52%|
|NIKKEI225|Always-Down|baseline|0.500000|0.500000|0.383795|0.277350|0.000|0.616|+0.048731|0.500000|0.0%|0.00%|
|EUROSTOXX50|GRU|CE|0.665359|0.492303|0.443983|0.380772|0.117|0.563|+0.045614|0.367241|11.5%|1.20%|
|EUROSTOXX50|LogisticRegression|L2|0.585519|0.482776|0.437759|0.384323|0.142|0.563|+0.036087|0.443966|13.9%|0.85%|
|EUROSTOXX50|LightGBM|Binary_logloss|0.529794|0.490031|0.486515|0.485912|0.471|0.563|+0.043342|0.483621|46.2%|2.78%|
|EUROSTOXX50|LNN|MILD_FOCAL|0.631657|0.500173|0.560166|0.381614|0.974|0.563|+0.053484|0.507759|97.4%|7.88%|
|EUROSTOXX50|LSTM|CE|0.657155|0.505770|0.465768|0.429518|0.185|0.563|+0.059081|0.443966|18.1%|2.51%|
|EUROSTOXX50|Transformer|CE|0.614117|0.474316|0.431535|0.383919|0.159|0.563|+0.027626|0.434483|15.6%|2.14%|
|EUROSTOXX50|Rule_200DMA|fixed_rule|0.447221|0.496909|0.522822|0.486005|0.704|0.563|+0.050220|0.554310|70.9%|3.05%|
|EUROSTOXX50|Momentum60|fixed_rule|0.435313|0.491835|0.502075|0.491657|0.580|0.563|+0.045146|0.602586|58.7%|-2.16%|
|EUROSTOXX50|Persistence|baseline|0.413251|0.446689|0.453320|0.446756|0.546|0.563|+0.000000|0.560345|53.5%|-0.99%|
|EUROSTOXX50|Always-Up|baseline|0.500000|0.500000|0.563278|0.360319|1.000|0.563|+0.053311|0.500000|99.9%|8.42%|
|EUROSTOXX50|Always-Down|baseline|0.500000|0.500000|0.436722|0.303971|0.000|0.563|+0.053311|0.500000|0.0%|0.00%|
|KOSPI200|GRU|CE|0.648654|0.502377|0.566845|0.372873|0.990|0.566|-0.000875|0.529412|99.0%|15.56%|
|KOSPI200|LogisticRegression|L2|0.619059|0.526030|0.568984|0.488957|0.830|0.566|+0.022777|0.521569|83.2%|9.79%|
|KOSPI200|LightGBM|Binary_logloss|0.538033|0.505413|0.568984|0.382316|0.984|0.566|+0.002160|0.500000|98.3%|12.86%|
|KOSPI200|LNN|CE|0.666024|0.509019|0.560428|0.443904|0.892|0.566|+0.005767|0.466667|87.4%|11.46%|
|KOSPI200|LSTM|CE|0.652304|0.514806|0.575401|0.410978|0.963|0.566|+0.011554|0.558824|96.2%|14.92%|
|KOSPI200|Transformer|MILD_FOCAL|0.660303|0.523513|0.583957|0.422848|0.963|0.566|+0.020261|0.542157|96.2%|14.94%|
|KOSPI200|Rule_200DMA|fixed_rule|0.440354|0.537735|0.540107|0.536454|0.523|0.566|+0.034483|0.577451|53.1%|10.42%|
|KOSPI200|Momentum60|fixed_rule|0.478784|0.591925|0.597861|0.591684|0.557|0.566|+0.088672|0.610784|56.5%|11.11%|
|KOSPI200|Persistence|baseline|0.457641|0.503252|0.510160|0.503158|0.553|0.566|+0.000000|0.476471|54.2%|5.41%|
|KOSPI200|Always-Up|baseline|0.500000|0.500000|0.565775|0.361339|1.000|0.566|-0.003252|0.500000|99.9%|14.47%|
|KOSPI200|Always-Down|baseline|0.500000|0.500000|0.434225|0.302759|0.000|0.566|-0.003252|0.500000|0.0%|0.00%|

## 1. Does GRU improve the neural benchmark set?

- SP500: GRU BA0.391019; highest existing validation-selected neural representative BA0.448056; difference-0.057037. Descriptive, not reselection.
- NASDAQ100: GRU BA0.471645; highest existing validation-selected neural representative BA0.479284; difference-0.007638. Descriptive, not reselection.
- NIKKEI225: GRU BA0.481863; highest existing validation-selected neural representative BA0.517863; difference-0.036001. Descriptive, not reselection.
- EUROSTOXX50: GRU BA0.492303; highest existing validation-selected neural representative BA0.505770; difference-0.013467. Descriptive, not reselection.
- KOSPI200: GRU BA0.502377; highest existing validation-selected neural representative BA0.523513; difference-0.021136. Descriptive, not reselection.

## 2–3. Do Logistic and LightGBM outperform deep models?

- SP500 LogisticRegression: delta BA vs highest of four fixed neural representatives=+0.003426.
- NASDAQ100 LogisticRegression: delta BA vs highest of four fixed neural representatives=-0.019210.
- NIKKEI225 LogisticRegression: delta BA vs highest of four fixed neural representatives=-0.022554.
- EUROSTOXX50 LogisticRegression: delta BA vs highest of four fixed neural representatives=-0.022994.
- KOSPI200 LogisticRegression: delta BA vs highest of four fixed neural representatives=+0.002517.
LogisticRegression exceeds all four neural representative BAs in2/5 markets. This is a descriptive comparison, not statistical superiority or a new winner-selection rule.
- SP500 LightGBM: delta BA vs highest of four fixed neural representatives=-0.025121.
- NASDAQ100 LightGBM: delta BA vs highest of four fixed neural representatives=-0.028556.
- NIKKEI225 LightGBM: delta BA vs highest of four fixed neural representatives=-0.002340.
- EUROSTOXX50 LightGBM: delta BA vs highest of four fixed neural representatives=-0.015739.
- KOSPI200 LightGBM: delta BA vs highest of four fixed neural representatives=-0.018100.
LightGBM exceeds all four neural representative BAs in0/5 markets. This is a descriptive comparison, not statistical superiority or a new winner-selection rule.

## 4. Do simple rules challenge learned models?

- SP500:200DMA BA0.565518, Momentum60 BA0.563600; highest learned representative BA0.451481. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.
- NASDAQ100:200DMA BA0.617383, Momentum60 BA0.560512; highest learned representative BA0.479284. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.
- NIKKEI225:200DMA BA0.456108, Momentum60 BA0.488745; highest learned representative BA0.517863. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.
- EUROSTOXX50:200DMA BA0.496909, Momentum60 BA0.491835; highest learned representative BA0.505770. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.
- KOSPI200:200DMA BA0.537735, Momentum60 BA0.591925; highest learned representative BA0.526030. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.

## 5–6. Forecast-frequency degeneration

- NASDAQ100, GRU: forecast Up0.080, actual Up0.665; retained unchanged.
- NASDAQ100, LNN: forecast Up0.053, actual Up0.665; retained unchanged.
- NASDAQ100, Transformer: forecast Up0.084, actual Up0.665; retained unchanged.
- NIKKEI225, LogisticRegression: forecast Up0.005, actual Up0.616; retained unchanged.
- NIKKEI225, LightGBM: forecast Up0.047, actual Up0.616; retained unchanged.
- NIKKEI225, LNN: forecast Up0.097, actual Up0.616; retained unchanged.
- NIKKEI225, Transformer: forecast Up0.041, actual Up0.616; retained unchanged.
- EUROSTOXX50, LNN: forecast Up0.974, actual Up0.563; retained unchanged.
- KOSPI200, GRU: forecast Up0.990, actual Up0.566; retained unchanged.
- KOSPI200, LightGBM: forecast Up0.984, actual Up0.566; retained unchanged.
- KOSPI200, LSTM: forecast Up0.963, actual Up0.566; retained unchanged.
- KOSPI200, Transformer: forecast Up0.963, actual Up0.566; retained unchanged.
These behaviors occur alongside validation-based threshold selection; this does not isolate thresholding as their cause. Probability learning, class imbalance and calibration can jointly matter. No near-constant case was excluded or retuned.
LogisticRegression: identical binary predictions across all5seeds in5/5 markets; five run records retained and no algorithmic classification seed variability/ensemble gain claimed for those markets.
LightGBM: identical binary predictions across all5seeds in5/5 markets; five run records retained and no algorithmic classification seed variability/ensemble gain claimed for those markets.

## 7–8. PT and reduced-overlap evidence

PT raw p-values are diagnostic in Phase1; expanded final multiplicity family is deliberately not yet frozen. Conventional PT does not resolve dependence fromH20 label overlap. A nominal positive test does not constitute final multiplicity-robust evidence.

|Market|Model|PT|Raw two-sided p|Positive one-sided p|Reduced-overlap BA|Reduced-overlap PT raw p|
|---|---|---:|---:|---:|---:|---:|
|SP500|GRU|-6.539439|6.17501e-11|1|0.259470|0.00133783|
|SP500|LogisticRegression|-3.392977|0.000691375|0.999654|0.373106|0.0367543|
|SP500|LightGBM|-4.632467|3.61334e-06|0.999998|0.355114|0.0461984|
|SP500|Rule_200DMA|4.274928|1.91199e-05|9.55994e-06|0.551136|0.461742|
|SP500|Momentum60|4.042109|5.29726e-05|2.64863e-05|0.613636|0.113289|
|NASDAQ100|GRU|-3.064955|0.00217703|0.998911|0.456801|0.225051|
|NASDAQ100|LogisticRegression|-2.659661|0.00782194|0.996089|0.417279|0.195261|
|NASDAQ100|LightGBM|-3.307919|0.00093992|0.99953|0.417279|0.195261|
|NASDAQ100|Rule_200DMA|7.494378|6.66133e-14|3.33067e-14|0.610294|0.113289|
|NASDAQ100|Momentum60|3.735318|0.000187478|9.37391e-05|0.579044|0.269606|
|NIKKEI225|GRU|-1.470869|0.141327|0.929337|0.430451|0.156333|
|NIKKEI225|LogisticRegression|-1.919870|0.0548743|0.972563|0.500000|nan|
|NIKKEI225|LightGBM|2.188040|0.0286667|0.0143333|0.500940|0.983459|
|NIKKEI225|Rule_200DMA|-2.898975|0.00374385|0.998128|0.470865|0.664786|
|NIKKEI225|Momentum60|-0.682478|0.494937|0.752532|0.469925|0.676804|
|EUROSTOXX50|GRU|-0.737290|0.460946|0.769527|0.367241|0.00834956|
|EUROSTOXX50|LogisticRegression|-1.520059|0.128496|0.935752|0.443966|0.314387|
|EUROSTOXX50|LightGBM|-0.615438|0.538266|0.730867|0.483621|0.819512|
|EUROSTOXX50|Rule_200DMA|-0.208693|0.834688|0.582656|0.554310|0.403266|
|EUROSTOXX50|Momentum60|-0.509739|0.610235|0.694883|0.602586|0.149532|
|KOSPI200|GRU|0.738323|0.460318|0.230159|0.529412|0.174686|
|KOSPI200|LogisticRegression|2.101351|0.0356102|0.0178051|0.521569|0.686626|
|KOSPI200|LightGBM|1.306564|0.191361|0.0956804|0.500000|nan|
|KOSPI200|Rule_200DMA|2.291299|0.0219462|0.0109731|0.577451|0.30217|
|KOSPI200|Momentum60|5.612695|1.992e-08|9.95999e-09|0.610784|0.137825|

The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence. Sparse cells/constant forecasts are recorded as in the existing PT implementation. No favorable phase is searched.

## 9. Predictive gains and economics

All costs0/10/25/50bps are saved; the following uses10bps round trip.

|Market|Model|CAGR|Annual vol|Sharpe|MDD|Exposure|One-way trades|Turnover|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|SP500|GRU|2.98%|15.42%|0.267|-21.11%|60.6%|196|196.0|
|SP500|LogisticRegression|3.23%|10.90%|0.346|-13.57%|22.5%|88|88.0|
|SP500|LightGBM|0.22%|13.25%|0.083|-24.77%|38.9%|66|66.0|
|SP500|Rule_200DMA|6.28%|10.89%|0.614|-17.89%|72.1%|28|28.0|
|SP500|Momentum60|9.19%|10.89%|0.862|-17.75%|69.5%|36|36.0|
|NASDAQ100|GRU|-8.91%|9.87%|-0.896|-30.49%|7.8%|52|52.0|
|NASDAQ100|LogisticRegression|0.54%|17.29%|0.117|-20.97%|27.6%|62|62.0|
|NASDAQ100|LightGBM|-2.67%|15.25%|-0.101|-30.33%|25.2%|62|62.0|
|NASDAQ100|Rule_200DMA|15.88%|14.72%|1.075|-13.58%|70.3%|16|16.0|
|NASDAQ100|Momentum60|10.69%|14.58%|0.770|-15.29%|66.2%|32|32.0|
|NIKKEI225|GRU|4.43%|10.62%|0.461|-12.47%|15.8%|102|102.0|
|NIKKEI225|LogisticRegression|0.89%|2.04%|0.445|-0.69%|0.5%|8|8.0|
|NIKKEI225|LightGBM|2.77%|4.90%|0.581|-3.59%|4.6%|28|28.0|
|NIKKEI225|Rule_200DMA|3.69%|16.73%|0.302|-35.92%|72.0%|42|42.0|
|NIKKEI225|Momentum60|5.45%|14.01%|0.449|-26.73%|59.9%|88|88.0|
|EUROSTOXX50|GRU|1.20%|9.26%|0.174|-15.70%|11.5%|66|66.0|
|EUROSTOXX50|LogisticRegression|0.85%|9.94%|0.134|-17.07%|13.9%|22|22.0|
|EUROSTOXX50|LightGBM|2.78%|13.34%|0.272|-19.63%|46.2%|110|110.0|
|EUROSTOXX50|Rule_200DMA|3.05%|12.38%|0.305|-19.68%|70.9%|20|20.0|
|EUROSTOXX50|Momentum60|-2.16%|11.33%|-0.135|-21.11%|58.7%|68|68.0|
|KOSPI200|GRU|15.56%|20.01%|0.823|-23.91%|99.0%|12|12.0|
|KOSPI200|LogisticRegression|9.79%|18.66%|0.594|-23.99%|83.2%|100|100.0|
|KOSPI200|LightGBM|12.86%|19.97%|0.706|-23.58%|98.3%|30|30.0|
|KOSPI200|Rule_200DMA|10.42%|14.65%|0.751|-23.33%|53.1%|28|28.0|
|KOSPI200|Momentum60|11.11%|15.31%|0.765|-26.07%|56.5%|42|42.0|

Across15new market-model cases, BA-positive/CAGR-negative mismatches:3; BA-negative/CAGR-positive mismatches:1. Full differences are retained in diagnostics/predictive_economic_disagreement.csv.

Predictive BA and return/Sharpe/drawdown need not agree. High exposure can resemble Buy & Hold and does not demonstrate timing skill; low exposure can suppress both risk and opportunity. Economic point estimates have no new confirmatory uncertainty claim in Phase1.

## Neural-only Friedman and descriptive ranks

- Mean_BA: statistic8.040000, raw p0.0451922, Kendall W0.536000, five market blocks/four neural architectures. Logistic/LightGBM excluded from this family.
- Mean_Macro_F1: statistic2.280000, raw p0.516363, Kendall W0.152000, five market blocks/four neural architectures. Logistic/LightGBM excluded from this family.

New-model near-constant representative cases:5/15; sign changes of BA advantage vs Persistence under fixed reduced overlap:4/15.

Five correlated markets give low power. Descriptive per-market and cross-market ranks are saved but do not establish statistical superiority. No final expanded Holm correction replaces the prior15. Phase2architecture membership must be specified/frozen before defining a final family.

## 10. Evaluation-design conclusion

Phase1 expands the benchmark universe without privileging LNN. The evidence should be interpreted market by market across validation selection, representative-vs-seed metrics, forecast-frequency degeneration, PT assumptions, reduced overlap and cost-adjusted exposure. Simple, neural, tree and rule models are all retained even when unfavorable. Any apparent isolated advantage is descriptive at this phase; neither a high rank nor unadjusted p-value establishes stable cross-market forecasting superiority. The final expanded-universe multiplicity interpretation remains pending Phase2.

All new settings, unchanged source hashes, independent checkpoint inference, original benchmark economics and momentum equivalence are audited. No existing artifact was overwritten.

Phase1 strengthens the evaluation-design motivation in the limited descriptive sense that forecast-frequency degeneration and/or overlap sensitivity remain observable in the expanded benchmark set. It does not strengthen an LNN-superiority claim. Which model leads depends on market, representative metric and baseline; final adjusted inference remains pending.

## Postprocessing verification correction

The initial finalizer omitted the original set_seed call before GRU checkpoint replay, leaving deterministic algorithms disabled. Matching the original training determinism settings resolved the mismatch without retraining, changing a probability/label/threshold, or relaxing the1e-7 tolerance. All75 saved test probability files exactly match the original final checkpoint metadata. All25 GRU checkpoints were replayed again under the correct settings; see diagnostics/final_checkpoint_probability_audit.csv and diagnostics/determinism_fix.json. The original run_manifest and failed-finalizer source are preserved for transparency.
