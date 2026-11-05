# Validation-selected LNN primary economic reanalysis

LNN losses were selected ONLY by five-seed mean 2019–2021 WF validation BA. 2022–2025 test outcomes were not used by the selection rule. All expected selections matched before any economic calculations. No predictive model/threshold/feature changes or HMM fitting. This folder replaces the manuscript primary economic table; all previous artifacts remain unchanged.

## Validation-only selection

|Market|Model|Loss|WF validation BA mean|
|---|---|---|---:|
|SP500|LNN|MILD_FOCAL|0.603727|
|NASDAQ100|LNN|MILD_FOCAL|0.565535|
|NIKKEI225|LNN|MILD_WCE|0.639022|
|EUROSTOXX50|LNN|MILD_FOCAL|0.631657|
|KOSPI200|LNN|CE|0.666024|

## Primary daily net results (10bps round trip)

|Market|Strategy|CAGR|Sharpe|MDD|Exposure|Category|
|---|---|---:|---:|---:|---:|---|
|SP500|Validation_LNN|2.48%|0.271|-20.12%|36.5%|Moderate|
|SP500|Persistence|6.13%|0.587|-15.87%|62.8%|Moderate|
|SP500|Buy_Hold|10.78%|0.664|-22.77%|99.9%|High|
|SP500|Always_Cash|0.00%|nan|0.00%|0.0%|Low|
|NASDAQ100|Validation_LNN|-3.76%|-0.428|-14.76%|5.2%|Low|
|NASDAQ100|Persistence|10.46%|0.712|-26.18%|63.4%|Moderate|
|NASDAQ100|Buy_Hold|14.00%|0.670|-29.92%|99.9%|High|
|NASDAQ100|Always_Cash|0.00%|nan|0.00%|0.0%|Low|
|NIKKEI225|Validation_LNN|5.72%|0.684|-10.75%|11.4%|Low|
|NIKKEI225|Persistence|4.59%|0.403|-31.25%|59.5%|Moderate|
|NIKKEI225|Buy_Hold|17.52%|0.848|-26.26%|99.9%|High|
|NIKKEI225|Always_Cash|0.00%|nan|0.00%|0.0%|Low|
|EUROSTOXX50|Validation_LNN|7.88%|0.532|-24.40%|97.4%|High|
|EUROSTOXX50|Persistence|-0.99%|-0.046|-16.83%|53.5%|Moderate|
|EUROSTOXX50|Buy_Hold|8.42%|0.551|-22.42%|99.9%|High|
|EUROSTOXX50|Always_Cash|0.00%|nan|0.00%|0.0%|Low|
|KOSPI200|Validation_LNN|11.46%|0.672|-23.04%|87.4%|High|
|KOSPI200|Persistence|5.41%|0.456|-24.27%|54.2%|Moderate|
|KOSPI200|Buy_Hold|14.47%|0.773|-24.28%|99.9%|High|
|KOSPI200|Always_Cash|0.00%|nan|0.00%|0.0%|Low|

## Exposure-aware interpretation and benchmark differences

- SP500: LNN exposure 36.5% (Moderate); delta CAGR vs Persistence -3.65%, vs Buy & Hold -8.29%; delta Sharpe vs Persistence -0.317, vs Buy & Hold -0.394.
- NASDAQ100: LNN exposure 5.2% (Low); delta CAGR vs Persistence -14.22%, vs Buy & Hold -17.76%; delta Sharpe vs Persistence -1.140, vs Buy & Hold -1.098.
- NIKKEI225: LNN exposure 11.4% (Low); delta CAGR vs Persistence +1.13%, vs Buy & Hold -11.80%; delta Sharpe vs Persistence +0.281, vs Buy & Hold -0.165.
- EUROSTOXX50: LNN exposure 97.4% (High); delta CAGR vs Persistence +8.87%, vs Buy & Hold -0.54%; delta Sharpe vs Persistence +0.578, vs Buy & Hold -0.019.
  **EUROSTOXX50: exposure exceeds90%. Economic performance is substantially influenced by persistent market exposure and may resemble a long-heavy strategy. Favorable strategy performance is partly attributable to persistent long exposure and therefore should not be interpreted as strong evidence of timing skill.**
- KOSPI200: LNN exposure 87.4% (High); delta CAGR vs Persistence +6.05%, vs Buy & Hold -3.01%; delta Sharpe vs Persistence +0.216, vs Buy & Hold -0.101.
  KOSPI200: exposure is high but below90%; favorable performance is partly attributable to persistent long exposure and should not be treated as strong evidence of timing skill.

## Nikkei225 differentiated case

Nikkei LNN exposure 11.4% versus Buy & Hold 99.9%; Sharpe 0.684 versus 0.848; MDD -10.75% versus -26.26%; High-regime mean predictive BA delta vs Persistence +0.246825.
These descriptive results support Nikkei225 as the strongest economically differentiated LNN case in this reanalysis: low exposure and drawdown protection with retained High-regime predictive advantage. This does not establish higher returns, universal superiority, or statistically supported timing skill.

## Predictive–economic consistency

Test BA below is the five-seed mean; operational majority BA is separately stored.

|Market|LNN mean BA|Persistence BA|Delta BA|Delta vs0.5|LNN CAGR|Persistence CAGR|Buy & Hold CAGR|A|B|C>90%|D>0.5|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
|SP500|0.438382|0.515074|-0.076692|-0.061618|2.48%|6.13%|10.78%|False|False|False|False|
|NASDAQ100|0.474637|0.532517|-0.057880|-0.025363|-3.76%|10.46%|14.00%|False|False|False|False|
|NIKKEI225|0.511176|0.451269|+0.059907|+0.011176|5.72%|4.59%|17.52%|False|False|False|True|
|EUROSTOXX50|0.508536|0.446689|+0.061847|+0.008536|7.88%|-0.99%|8.42%|False|False|True|True|
|KOSPI200|0.495425|0.503252|-0.007827|-0.004575|11.46%|5.41%|14.47%|False|True|False|False|

## Nonoverlap20 robustness (same first phase and10bps costs)

|Market|LNN CAGR|Persistence CAGR|Buy & Hold CAGR|LNN Sharpe|Persistence Sharpe|Buy & Hold Sharpe|LNN MDD|LNN exposure|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|SP500|-3.11%|3.64%|10.78%|-0.170|0.368|0.664|-32.23%|34.6%|
|NASDAQ100|-0.91%|5.85%|14.00%|-0.056|0.438|0.670|-13.87%|6.1%|
|NIKKEI225|2.12%|0.11%|17.52%|0.382|0.089|0.848|-10.75%|6.3%|
|EUROSTOXX50|7.66%|4.03%|8.42%|0.522|0.396|0.551|-19.78%|95.6%|
|KOSPI200|12.90%|5.23%|14.47%|0.718|0.398|0.773|-24.28%|94.3%|

## Frozen HMM regime economic evaluation

No regime changes signals. Conditional annualized returns are not stand-alone regime-timing CAGR.

|Market|Regime|N|Mean net return|Conditional annualized return|Sharpe|Exposure|Delta mean vs Persistence|Delta Sharpe vs Persistence|Delta mean vs Buy & Hold|Delta Sharpe vs Buy & Hold|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|SP500|Low|341|0.000397|10.34%|1.780|20.8%|-0.000024|+0.764|-0.000066|+0.768|
|SP500|Normal|425|-0.000014|-1.09%|-0.030|43.5%|-0.000258|-0.617|-0.000477|-0.755|
|SP500|High|216|-0.000036|-2.20%|-0.055|47.2%|-0.000080|-0.138|-0.000526|-0.515|
|NASDAQ100|Low|141|-0.000030|-0.76%|-0.856|1.4%|-0.000741|-2.028|-0.000530|-1.665|
|NASDAQ100|Normal|470|0.000021|0.52%|0.858|0.4%|-0.000795|-0.654|-0.001110|-0.802|
|NASDAQ100|High|371|-0.000382|-9.99%|-0.726|12.7%|-0.000253|-0.546|-0.000432|-0.765|
|NIKKEI225|Low|458|0.000118|2.92%|0.737|4.6%|-0.000757|-0.851|-0.001011|-0.996|
|NIKKEI225|Normal|379|0.000029|0.26%|0.075|20.1%|+0.000469|+0.976|+0.000371|+0.471|
|NIKKEI225|High|120|0.001337|38.44%|2.162|10.0%|+0.001581|+2.592|-0.001304|+0.302|
|EUROSTOXX50|Low|476|0.000309|7.11%|0.574|100.0%|+0.000451|+0.897|+0.000000|+0.000|
|EUROSTOXX50|Normal|353|0.000308|6.53%|0.459|95.2%|+0.000014|-0.318|+0.000055|+0.097|
|EUROSTOXX50|High|154|0.000625|13.51%|0.632|94.2%|+0.000978|+1.602|-0.000272|-0.246|
|KOSPI200|Low|137|0.000691|17.64%|1.143|100.0%|+0.000740|+1.236|+0.000000|+0.000|
|KOSPI200|Normal|409|-0.000031|-2.40%|-0.044|89.0%|+0.000153|+0.344|-0.000226|-0.303|
|KOSPI200|High|408|0.000971|25.03%|1.193|81.6%|+0.000195|-0.106|-0.000045|+0.059|

## Paired moving-block uncertainty

20 observations,2000 resamples, seed20261028; no HMM refit or prediction regeneration. Intervals represent time-series uncertainty under this specified conditional block procedure.

|Market|Comparator|Metric|Estimate|95% CI|
|---|---|---|---:|---|
|SP500|Persistence|Delta_Mean_daily_return|-0.000137|[-0.000647, +0.000421]|
|SP500|Persistence|Delta_Sharpe|-0.316510|[-1.475394, +0.965929]|
|SP500|Persistence|Delta_CAGR|-0.036491|[-0.174722, +0.109934]|
|SP500|Buy_Hold|Delta_Mean_daily_return|-0.000345|[-0.000793, +0.000119]|
|SP500|Buy_Hold|Delta_Sharpe|-0.393781|[-1.091981, +0.458361]|
|SP500|Buy_Hold|Delta_CAGR|-0.082945|[-0.223583, +0.042191]|
|NASDAQ100|Persistence|Delta_Mean_daily_return|-0.000583|[-0.001190, +0.000069]|
|NASDAQ100|Persistence|Delta_Sharpe|-1.140123|[-2.150089, +0.098419]|
|NASDAQ100|Persistence|Delta_CAGR|-0.142214|[-0.325171, +0.025525]|
|NASDAQ100|Buy_Hold|Delta_Mean_daily_return|-0.000771|[-0.001530, -0.000056]|
|NASDAQ100|Buy_Hold|Delta_Sharpe|-1.098295|[-2.113746, -0.134040]|
|NASDAQ100|Buy_Hold|Delta_CAGR|-0.177606|[-0.430447, +0.012994]|
|NIKKEI225|Persistence|Delta_Mean_daily_return|+0.000022|[-0.000664, +0.000708]|
|NIKKEI225|Persistence|Delta_Sharpe|+0.280919|[-1.089539, +1.706773]|
|NIKKEI225|Persistence|Delta_CAGR|+0.011285|[-0.180275, +0.179926]|
|NIKKEI225|Buy_Hold|Delta_Mean_daily_return|-0.000501|[-0.001256, +0.000254]|
|NIKKEI225|Buy_Hold|Delta_Sharpe|-0.164778|[-1.274992, +0.927660]|
|NIKKEI225|Buy_Hold|Delta_CAGR|-0.118015|[-0.358668, +0.095091]|
|EUROSTOXX50|Persistence|Delta_Mean_daily_return|+0.000377|[-0.000022, +0.000789]|
|EUROSTOXX50|Persistence|Delta_Sharpe|+0.577579|[-0.150049, +1.369696]|
|EUROSTOXX50|Persistence|Delta_CAGR|+0.088683|[-0.017570, +0.206527]|
|EUROSTOXX50|Buy_Hold|Delta_Mean_daily_return|-0.000023|[-0.000152, +0.000115]|
|EUROSTOXX50|Buy_Hold|Delta_Sharpe|-0.019216|[-0.192238, +0.191614]|
|EUROSTOXX50|Buy_Hold|Delta_CAGR|-0.005420|[-0.039773, +0.033416]|
|KOSPI200|Persistence|Delta_Mean_daily_return|+0.000255|[-0.000151, +0.000689]|
|KOSPI200|Persistence|Delta_Sharpe|+0.215993|[-0.412579, +0.935255]|
|KOSPI200|Persistence|Delta_CAGR|+0.060504|[-0.050649, +0.192553]|
|KOSPI200|Buy_Hold|Delta_Mean_daily_return|-0.000116|[-0.000265, +0.000138]|
|KOSPI200|Buy_Hold|Delta_Sharpe|-0.101017|[-0.296310, +0.226014]|
|KOSPI200|Buy_Hold|Delta_CAGR|-0.030120|[-0.075957, +0.039998]|

All 10 primary CAGR-difference intervals include zero: True. Positive net point estimates therefore do not establish economic superiority under this bootstrap.


## Diagnostic comparison with previous test-selected economics

Computed only after validation selections and new results are frozen; not used for selection.

|Market|Previous model/loss|New LNN loss|Previous CAGR|New CAGR|Previous exposure|New exposure|
|---|---|---|---:|---:|---:|---:|
|SP500|LNN/MILD_WCE|MILD_FOCAL|0.65%|2.48%|35.2%|36.5%|
|NASDAQ100|Transformer/CE|MILD_FOCAL|10.75%|-3.76%|57.8%|5.2%|
|NIKKEI225|LNN/CE|MILD_WCE|8.22%|5.72%|17.7%|11.4%|
|EUROSTOXX50|LNN/MILD_FOCAL|MILD_FOCAL|7.88%|7.88%|97.4%|97.4%|
|KOSPI200|LSTM/CE|CE|14.92%|11.46%|96.2%|87.4%|

## Revised manuscript conclusion

The methodological basis is stronger because the economic configuration rule is validation-only and LNN-specific. The substantive conclusion is **different and narrower**, not universal LNN superiority: U.S. negative/weak results remain, Nikkei offers differentiated low-exposure drawdown behavior, and favorable European/Korean results require persistent-long exposure interpretation. The comparison also changes architecture in NASDAQ100 and KOSPI200, so differences cannot be attributed to validation-vs-test loss selection alone.

Economic outcomes remain secondary evaluations of the same saved validation-selected predictions. Favorable point estimates do not establish economic superiority; consult intervals for each comparison rather than interpreting a positive estimate as significance. Price-index returns are stylized, local-currency proxies, not directly investable total-return portfolios. High exposure can make Long/Cash similar to Buy & Hold. Negative results are retained; none may be used for retuning. This retrospective reanalysis does not create a new untouched test set.
