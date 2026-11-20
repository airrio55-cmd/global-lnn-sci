# STEP8BR NN_VS_BASELINE

원 STEP8B BLOCKED40·실패NPZ·승인·source·ledger를그대로보존하고독립STEP8B-R40개identity를실행했다. 새완료40/BLOCKED0,Logistic Train-only fit10,Climatology추정10,가격규칙평가20이다. 과거NN학습횟수500에Logistic/Climatology/규칙을추가하지않는다. 기존NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED 및 이전9799파일/STEP8B scratch46파일 변경0. NN재학습·checkpoint load/forward·HMM fit/refilter·τ추가계측·새금융Bootstrap/Holm/p값·Ensemble/GPU·2026시장관측사용0. master flags=false.

이번 결과는 retrospective exploratory benchmark다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED는storage복구로변하지않는다. O1~O4 Test와후속Validation의역사적중복,Origin·Seed·중첩label의존성을유지한다. 거래수익성·전향적일반화·통계적우월성을인증하지않으며가격/모델/Seed/threshold를사후선택하지않는다.

|가격|모델|BA|Macro F1|Brier|Recall0|Recall1|Accuracy|단일클래스 예측 결과수|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|A|RNN|0.518397|0.444842|0.251472|0.371868|0.664927|0.476753|0|
|A|LSTM|0.518008|0.469951|0.248489|0.329706|0.706311|0.516159|1|
|A|GRU|0.527844|0.477904|0.252249|0.396606|0.659083|0.509410|0|
|A|LTC|0.532387|0.452154|0.250427|0.462540|0.602233|0.529009|12|
|A|CfC|0.532112|0.486833|0.246920|0.392810|0.671414|0.522635|0|
|B|RNN|0.520134|0.448191|0.251259|0.369054|0.671214|0.481675|0|
|B|LSTM|0.519534|0.473133|0.249889|0.370416|0.668652|0.511738|1|
|B|GRU|0.527896|0.475803|0.251875|0.390023|0.665769|0.506820|0|
|B|LTC|0.531292|0.453225|0.250228|0.448740|0.613843|0.534035|12|
|B|CfC|0.518918|0.474423|0.251535|0.345741|0.692095|0.511699|0|

동일Origin/가격/날짜/Target에서기존NN10Seed의저장지표를동일가중평균한뒤5Origin평균했다. 새NN추론·성능재평가없이저장값만재사용했다. baseline은seed없는deterministic1회이며Seed를시장날짜10배로세지않는다.

- RQ1: A/B각각5Origin 평균에서모든NN의BA가최고baseline Momentum60(0.504416)보다높다. 이는기술적평균차이이며통계적우월성이아니다.
- RQ2: Origin별로일관되지는않는다. Momentum60대비NN BA가높은Origin수는 A에서RNN2/LSTM3/GRU3/LTC3/CfC3, B에서2/3/3/3/4(각5개중)다. RNN은과반Origin에서Momentum60보다낮아도평균은높아평균만의결론을피해야한다. 가격별결과를임의제외하지않았다.
- RQ3: BA높음이MacroF1/Brier로일치하지않는다. Momentum60 MacroF1 0.491019는모든NN의5Origin 평균보다높지만0/1 Brier0.425077은확률예측보다훨씬나쁘다. A의최저NN Brier는CfC0.246920, B는LSTM0.249889이며후보선택근거로쓰지않는다.
- RQ4: 기존전체Test 퇴화LTC는A/B각12개(총24)모두Climatology와BA=0.5로같다. MacroF1은각후보4개더높고8개같으며,Brier는8개더낮고4개더높다. 따라서추가BA가없는사례는있으나모든지표에서동일하다고단정하지않는다. 같은Origin/Seed의의존성을시장반복으로보지않는다.
- RQ5: 복잡모형의추가BA는관측되지만F1·확률품질·Origin 일관성은혼합됐다. 순위를통계적우수성/복잡성의인과효과로바꾸지않고단순모형을부정적결과때문에제거하지않았다.

Validation-Test 차이는baseline Validation을새로평가하지않았으므로산출하지않는다. NN의Validation선택지표와새baseline의다른정책/시점값을섞지않았다. 기존STEP5C Primary20/Secondary80/Origin100가족에baseline을추가하지않았고새p값/Bootstrap/Holm은0이다.

확인일:2026-11-20 KST. 근거:원STEP8B동결사양·실패lineage,STEP8BR안전재읽기검사/실행ledger,기존STEP5BNN저장지표. 새공식가격/PIT출처검증은하지않았다.

동일한것은Test날짜·Target·의사결정기준일이며입력표현/과거길이는동일하지않다. NN은20시점F1 window,Logistic은현재tF1,200DMA는200세션종가,Momentum은60세션간격정보를사용한다. 따라서이번비교를모델복잡도만분리한통제실험으로해석하지않는다.
