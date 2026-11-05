# Journal of Forecasting: validation-selected PT robustness

No predictive training, loss changes, threshold tuning, feature/target change or HMM refit. All15 validation-selected architecture losses and75 original seed predictions verified.

**PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially.** PT is not a remedy for dependence; block-bootstrap and reduced-overlap checks remain central.

## 1–2. Neural forecasts and architecture consistency

Primary Holm15: **1/15 positive directional-support configurations**, **4/15 significant negative associations**. Significant negative PT is not evidence of positive forecasting skill.
- Positive isolated result: KOSPI200, Transformer/MILD_FOCAL, PT=3.756760, raw two-sided p=0.000172128, Holm15 p=0.00240979.

No architecture shows positive primary support consistently across markets. Seed-level nominal counts are descriptive; their p-values are not averaged. One undefined seed PT is retained and documented, not silently removed.

## Manuscript architecture table

|Market|Architecture|Loss|Accuracy|BA|Actual Up|Forecast Up|PT|Raw two-sided p|Holm15 p|Significant either direction|Positive support|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|SP500|LNN|MILD_FOCAL|0.412253|0.448056|0.660436|0.371755|-3.160760|0.00157358|0.0173094|True|False|
|SP500|LSTM|MILD_FOCAL|0.441329|0.436638|0.660436|0.494289|-3.726760|0.000193957|0.00252144|True|False|
|SP500|Transformer|MILD_FOCAL|0.391485|0.441247|0.660436|0.326064|-3.685656|0.000228114|0.00273737|True|False|
|NASDAQ100|LNN|MILD_FOCAL|0.334372|0.479284|0.664590|0.052960|-2.712017|0.00668752|0.0614912|False|False|
|NASDAQ100|LSTM|MILD_FOCAL|0.343718|0.471747|0.664590|0.101765|-2.739722|0.00614912|0.0614912|False|False|
|NASDAQ100|Transformer|MILD_WCE|0.328141|0.460795|0.664590|0.084112|-4.141207|3.45483e-05|0.000518225|True|False|
|NIKKEI225|LNN|MILD_WCE|0.423241|0.517863|0.616205|0.097015|1.798780|0.0720535|0.432321|False|False|
|NIKKEI225|LSTM|MILD_FOCAL|0.414712|0.503085|0.616205|0.120469|0.282499|0.777561|1|False|False|
|NIKKEI225|Transformer|MILD_FOCAL|0.398721|0.505825|0.616205|0.040512|0.880516|0.37858|1|False|False|
|EUROSTOXX50|LNN|MILD_FOCAL|0.560166|0.500173|0.563278|0.974066|0.033500|0.973276|1|False|False|
|EUROSTOXX50|LSTM|CE|0.465768|0.505770|0.563278|0.184647|0.458223|0.646793|1|False|False|
|EUROSTOXX50|Transformer|CE|0.431535|0.474316|0.563278|0.158714|-2.165937|0.030316|0.212212|False|False|
|KOSPI200|LNN|CE|0.560428|0.509019|0.565775|0.891979|0.881177|0.378222|1|False|False|
|KOSPI200|LSTM|CE|0.575401|0.514806|0.565775|0.962567|2.365643|0.0179988|0.14399|False|False|
|KOSPI200|Transformer|MILD_FOCAL|0.583957|0.523513|0.565775|0.962567|3.756760|0.000172128|0.00240979|True|True|

Table note: PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially.

## 3. LNN-only supplemental Holm5 table

|Market|Loss|N|Actual Up|LNN majority Up|Accuracy|BA|PT|Raw two-sided p|Holm5 p|Positive directional accuracy supported?|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
|SP500|MILD_FOCAL|963|0.660436|0.371755|0.412253|0.448056|-3.160760|0.00157358|0.00786791|False|
|NASDAQ100|MILD_FOCAL|963|0.664590|0.052960|0.334372|0.479284|-2.712017|0.00668752|0.0267501|False|
|NIKKEI225|MILD_WCE|938|0.616205|0.097015|0.423241|0.517863|1.798780|0.0720535|0.216161|False|
|EUROSTOXX50|MILD_FOCAL|964|0.563278|0.974066|0.560166|0.500173|0.033500|0.973276|0.973276|False|
|KOSPI200|CE|935|0.565775|0.891979|0.560428|0.509019|0.881177|0.378222|0.756444|False|

LNN positive directional support after two-sided Holm5: **0/5**. U.S. LNN negative rejections are retained as negative dependence, not rebranded as skill. The unadjusted Nikkei full-test positive one-sided tail is reported but does not pass the primary adjusted positive-support rule.

Table note: PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially.

## 4. Fixed first-phase reduced-overlap LNN PT

|Market|N|Accuracy|BA|PT|Two-sided raw p|Exploratory Holm5 p|Small-cell warning|
|---|---:|---:|---:|---:|---:|---:|---|
|SP500|49|0.306122|0.339962|-2.230210|0.0257335|0.128668|False|
|NASDAQ100|49|0.326531|0.456801|-1.213205|0.225051|0.900205|True|
|NIKKEI225|47|0.425532|0.509398|0.261503|0.793705|1|True|
|EUROSTOXX50|49|0.591837|0.507759|0.272609|0.785154|1|True|
|KOSPI200|47|0.595745|0.466667|-1.099744|0.271444|0.900205|True|

No reduced-overlap LNN PT survives its exploratory Holm5 adjustment. The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence. Small samples and sparse forecast margins reduce power and asymptotic reliability.

Table note: PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially; reduced overlap does not establish independence.

## 5. Nikkei High exploratory context

|Prediction|N|Actual Up / Always-Up Accuracy|Forecast Up|Accuracy|BA|PT|Two-sided p|Positive one-sided p|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|Seed_42|117|0.538462|0.136752|0.495726|0.523810|0.750558|0.452919|0.226459|
|Seed_52|117|0.538462|0.059829|0.504274|0.538360|1.751801|0.079808|0.039904|
|Seed_62|117|0.538462|0.102564|0.495726|0.526455|0.944446|0.344942|0.172471|
|Seed_72|117|0.538462|0.282051|0.538462|0.555556|1.337165|0.181169|0.0905844|
|Seed_82|117|0.538462|0.111111|0.521368|0.551587|1.777905|0.0754195|0.0377098|
|Majority|117|0.538462|0.085470|0.512821|0.544974|1.742285|0.0814585|0.0407293|
|Persistence|117|0.538462|0.572650|0.299145|0.292328|-4.546838|5.44579e-06|0.999997|
|Always_Up|117|0.538462|1.000000|0.538462|0.500000|nan|nan|nan|

Nikkei High majority Accuracy **0.512821** is below Always-Up **0.538462**, though above Persistence **0.299145**. Its BA is0.544974, PT=1.742285, two-sided p=0.0814585. The nominal positive one-sided p=0.0407293 is shown transparently, but this post-hoc conditional test is not confirmatory. No seed is selected by its p-value. Always-Up PT is undefined because the forecast is constant.

Table note: PT p-values use the conventional directional-accuracy test and should be interpreted cautiously because adjacent H=20 labels overlap substantially. High regimes are fixed; no HMM refitting or effective sample-size claim is made.

## Class imbalance and Persistence

Always-Up/Down Accuracy, BA and actual-positive rates are in pt_benchmark_context.csv, with NA PT for constant forecasts. Persistence is the original P_t-based benchmark, unlike neural t−1 input information; its raw PT context is not a replacement primary test. High nominal hit rates under imbalance are not sufficient directional-accuracy evidence.

## 6. Revised conclusion

**Outcome B.**
Directional predictability appears only in isolated configurations and does not establish stable cross-market superiority.

For the current data, the positive KOSPI Transformer exception must remain visible; it is not LNN evidence. The LNN-wide superiority/conditional-generalization claim is not strengthened. The evaluation-design and benchmark/negative-results framing remains appropriate, with a clearly qualified isolated positive exception. Nikkei High has weak two-sided PT and inferior hit rate to Always-Up, consistent with retaining it as descriptive and statistically fragile rather than established generalization. This conclusion does not show equivalence/no signal, and negative relationships must not be inverted without a new prespecified evaluation.

All source artifacts and selections remain unchanged. Conventional PT, block-bootstrap sensitivity, episode-aware permutation and reduced-overlap results have distinct assumptions; no one favorable test is used to override the rest.
