# Frozen-prediction economic evaluation

Primary: five-seed majority Long/Cash, daily single portfolio state, 10bps round trip, next-close execution with returns starting the following close-to-close interval. All model/threshold/HMM inputs unchanged. No strategy chosen from economic outcomes.

## Primary cost-adjusted performance

|Market|Strategy|CAGR|Sharpe|MDD|Exposure|Final wealth|
|---|---|---:|---:|---:|---:|---:|
|SP500|Best_Model|0.65%|0.114|-25.37%|35.2%|1.026|
|SP500|Persistence|6.13%|0.587|-15.87%|62.8%|1.261|
|SP500|Buy_Hold|10.78%|0.664|-22.77%|99.9%|1.490|
|SP500|Always_Cash|0.00%|nan|0.00%|0.0%|1.000|
|NASDAQ100|Best_Model|10.75%|0.730|-13.87%|57.8%|1.489|
|NASDAQ100|Persistence|10.46%|0.712|-26.18%|63.4%|1.473|
|NASDAQ100|Buy_Hold|14.00%|0.670|-29.92%|99.9%|1.666|
|NASDAQ100|Always_Cash|0.00%|nan|0.00%|0.0%|1.000|
|NIKKEI225|Best_Model|8.22%|0.810|-10.93%|17.7%|1.350|
|NIKKEI225|Persistence|4.59%|0.403|-31.25%|59.5%|1.186|
|NIKKEI225|Buy_Hold|17.52%|0.848|-26.26%|99.9%|1.846|
|NIKKEI225|Always_Cash|0.00%|nan|0.00%|0.0%|1.000|
|EUROSTOXX50|Best_Model|7.88%|0.532|-24.40%|97.4%|1.344|
|EUROSTOXX50|Persistence|-0.99%|-0.046|-16.83%|53.5%|0.962|
|EUROSTOXX50|Buy_Hold|8.42%|0.551|-22.42%|99.9%|1.371|
|EUROSTOXX50|Always_Cash|0.00%|nan|0.00%|0.0%|1.000|
|KOSPI200|Best_Model|14.92%|0.804|-23.58%|96.2%|1.693|
|KOSPI200|Persistence|5.41%|0.456|-24.27%|54.2%|1.221|
|KOSPI200|Buy_Hold|14.47%|0.773|-24.28%|99.9%|1.668|
|KOSPI200|Always_Cash|0.00%|nan|0.00%|0.0%|1.000|

## RQ6–RQ7: Economic translation and costs

The statements below use the frozen primary daily strategy. Positive CAGR alone is not outperformance, and a point estimate alone is not economically significant evidence.
- SP500: net CAGR 0.65%, Sharpe 0.114; CAGR cost drag from 0 to10bps 0.80%; delta CAGR vs Persistence -5.48%, vs Buy & Hold -10.13%.
- NASDAQ100: net CAGR 10.75%, Sharpe 0.730; CAGR cost drag from 0 to10bps 0.91%; delta CAGR vs Persistence +0.29%, vs Buy & Hold -3.25%.
- NIKKEI225: net CAGR 8.22%, Sharpe 0.810; CAGR cost drag from 0 to10bps 0.80%; delta CAGR vs Persistence +3.63%, vs Buy & Hold -9.30%.
- EUROSTOXX50: net CAGR 7.88%, Sharpe 0.532; CAGR cost drag from 0 to10bps 0.17%; delta CAGR vs Persistence +8.87%, vs Buy & Hold -0.54%.
- KOSPI200: net CAGR 14.92%, Sharpe 0.804; CAGR cost drag from 0 to10bps 0.40%; delta CAGR vs Persistence +9.51%, vs Buy & Hold +0.45%.

## RQ8–RQ9: Prespecified high/low regime regions

These are conditional realized-return summaries, not regime-timed strategies or independently established significance.
- NIKKEI225 High: N=120; mean net daily return 0.001880; Sharpe 2.765; delta Sharpe vs Persistence +3.195, vs Buy & Hold +0.905; delta mean return vs Persistence +0.002124, vs Buy & Hold -0.000762.
- EUROSTOXX50 High: N=154; mean net daily return 0.000625; Sharpe 0.632; delta Sharpe vs Persistence +1.602, vs Buy & Hold -0.246; delta mean return vs Persistence +0.000978, vs Buy & Hold -0.000272.
- KOSPI200 Low: N=137; mean net daily return 0.000691; Sharpe 1.143; delta Sharpe vs Persistence +1.236, vs Buy & Hold +0.000; delta mean return vs Persistence +0.000740, vs Buy & Hold +0.000000.

## RQ10: Prediction/economic disagreement

A/B use majority-vote BA vs Persistence and primary net CAGR; C uses majority accuracy versus Sharpe/MDD. Original five-seed mean BA flags are also saved.
- SP500: majority delta BA -0.0883, delta accuracy -0.1755, delta CAGR -5.48%; A=False, B=False, C=False.
- NASDAQ100: majority delta BA -0.0337, delta accuracy -0.0550, delta CAGR +0.29%; A=False, B=True, C=False.
- NIKKEI225: majority delta BA +0.0687, delta accuracy -0.0341, delta CAGR +3.63%; A=False, B=False, C=False.
- EUROSTOXX50: majority delta BA +0.0535, delta accuracy +0.1068, delta CAGR +8.87%; A=False, B=False, C=True.
- KOSPI200: majority delta BA +0.0116, delta accuracy +0.0652, delta CAGR +9.51%; A=False, B=False, C=False.

## Nonoverlapping robustness

|Market|Strategy|20-observation CAGR|Sharpe|MDD|
|---|---|---:|---:|---:|
|SP500|Best_Model|-3.57%|-0.216|-28.79%|
|SP500|Persistence|3.64%|0.368|-19.57%|
|SP500|Buy_Hold|10.78%|0.664|-22.77%|
|NASDAQ100|Best_Model|2.28%|0.219|-27.97%|
|NASDAQ100|Persistence|5.85%|0.438|-26.45%|
|NASDAQ100|Buy_Hold|14.00%|0.670|-29.92%|
|NIKKEI225|Best_Model|6.96%|0.850|-10.75%|
|NIKKEI225|Persistence|0.11%|0.089|-29.70%|
|NIKKEI225|Buy_Hold|17.52%|0.848|-26.26%|
|EUROSTOXX50|Best_Model|7.66%|0.522|-19.78%|
|EUROSTOXX50|Persistence|4.03%|0.396|-17.50%|
|EUROSTOXX50|Buy_Hold|8.42%|0.551|-22.42%|
|KOSPI200|Best_Model|15.12%|0.820|-23.58%|
|KOSPI200|Persistence|5.23%|0.398|-35.35%|
|KOSPI200|Buy_Hold|14.47%|0.773|-24.28%|

## Exploratory uncertainty

|Market|Comparator|Statistic|Estimate|95% moving-block CI|
|---|---|---|---:|---|
|SP500|Persistence|Delta_Mean_daily_return|-0.000209|[-0.000709, +0.000325]|
|SP500|Persistence|Delta_Sharpe|-0.473012|[-1.585973, +0.773113]|
|SP500|Persistence|Delta_CAGR|-0.054799|[-0.190171, +0.085136]|
|SP500|Buy_Hold|Delta_Mean_daily_return|-0.000417|[-0.000871, +0.000072]|
|SP500|Buy_Hold|Delta_Sharpe|-0.550284|[-1.281788, +0.294268]|
|SP500|Buy_Hold|Delta_CAGR|-0.101253|[-0.240619, +0.027396]|
|NASDAQ100|Persistence|Delta_Mean_daily_return|+0.000010|[-0.000550, +0.000635]|
|NASDAQ100|Persistence|Delta_Sharpe|+0.018175|[-0.826804, +1.009865]|
|NASDAQ100|Persistence|Delta_CAGR|+0.002907|[-0.155570, +0.170636]|
|NASDAQ100|Buy_Hold|Delta_Mean_daily_return|-0.000178|[-0.000841, +0.000469]|
|NASDAQ100|Buy_Hold|Delta_Sharpe|+0.060002|[-0.684535, +0.846569]|
|NASDAQ100|Buy_Hold|Delta_CAGR|-0.032484|[-0.241303, +0.143753]|
|NIKKEI225|Persistence|Delta_Mean_daily_return|+0.000121|[-0.000616, +0.000819]|
|NIKKEI225|Persistence|Delta_Sharpe|+0.407119|[-1.008294, +1.831958]|
|NIKKEI225|Persistence|Delta_CAGR|+0.036325|[-0.165686, +0.220967]|
|NIKKEI225|Buy_Hold|Delta_Mean_daily_return|-0.000401|[-0.001114, +0.000393]|
|NIKKEI225|Buy_Hold|Delta_Sharpe|-0.038577|[-1.138851, +1.075890]|
|NIKKEI225|Buy_Hold|Delta_CAGR|-0.092975|[-0.323293, +0.131410]|
|EUROSTOXX50|Persistence|Delta_Mean_daily_return|+0.000377|[-0.000022, +0.000789]|
|EUROSTOXX50|Persistence|Delta_Sharpe|+0.577579|[-0.150049, +1.369696]|
|EUROSTOXX50|Persistence|Delta_CAGR|+0.088683|[-0.017570, +0.206527]|
|EUROSTOXX50|Buy_Hold|Delta_Mean_daily_return|-0.000023|[-0.000152, +0.000115]|
|EUROSTOXX50|Buy_Hold|Delta_Sharpe|-0.019216|[-0.192238, +0.191614]|
|EUROSTOXX50|Buy_Hold|Delta_CAGR|-0.005420|[-0.039773, +0.033416]|
|KOSPI200|Persistence|Delta_Mean_daily_return|+0.000384|[-0.000114, +0.000799]|
|KOSPI200|Persistence|Delta_Sharpe|+0.347772|[-0.380197, +1.011242]|
|KOSPI200|Persistence|Delta_CAGR|+0.095115|[-0.040562, +0.224356]|
|KOSPI200|Buy_Hold|Delta_Mean_daily_return|+0.000013|[-0.000058, +0.000097]|
|KOSPI200|Buy_Hold|Delta_Sharpe|+0.030763|[-0.065755, +0.141374]|
|KOSPI200|Buy_Hold|Delta_CAGR|+0.004491|[-0.016389, +0.028948]|

All ten primary CAGR-difference 95% bootstrap intervals include zero. Net point-estimate improvements are not established economic superiority.

## Limits

No economic-significance claim is warranted solely from a positive point estimate or predictive BA. Read block intervals, costs and both benchmark comparisons jointly. Price-only local-currency indices, conservative close execution, stale prediction tails, empirical KOSPI observation dates, test-selected frozen Best configurations, and conditional HMM/return bootstraps limit interpretation. No models or regimes were reselected. methodology_notes.md documents metric definitions and alignment; prediction_return_alignment_audit.csv records signal, effective and return dates.
