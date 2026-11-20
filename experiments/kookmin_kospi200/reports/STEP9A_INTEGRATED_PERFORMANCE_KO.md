# STEP9A INTEGRATED_PERFORMANCE

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

|가격|모델|Accuracy|BA|MacroF1|Brier↓|Recall0|Recall1|
|---|---|---:|---:|---:|---:|---:|---:|
|A|CLIMATOLOGY|0.530037|0.500000|0.340082|0.251364|0.000000|1.000000|
|A|LOGISTIC|0.491882|0.492492|0.359634|0.251151|0.068318|0.916665|
|A|DMA200|0.532941|0.482180|0.442626|0.467059|0.430809|0.533551|
|A|MOMENTUM60|0.574923|0.504416|0.491019|0.425077|0.430143|0.578689|
|A|RNN|0.476753|0.518397|0.444842|0.251472|0.371868|0.664927|
|A|LSTM|0.516159|0.518008|0.469951|0.248489|0.329706|0.706311|
|A|GRU|0.509410|0.527844|0.477904|0.252249|0.396606|0.659083|
|A|LTC|0.529009|0.532387|0.452154|0.250427|0.462540|0.602233|
|A|CfC|0.522635|0.532112|0.486833|0.246920|0.392810|0.671414|
|B|CLIMATOLOGY|0.530037|0.500000|0.340082|0.251364|0.000000|1.000000|
|B|LOGISTIC|0.491882|0.492492|0.359634|0.251150|0.068318|0.916665|
|B|DMA200|0.532941|0.482180|0.442626|0.467059|0.430809|0.533551|
|B|MOMENTUM60|0.574923|0.504416|0.491019|0.425077|0.430143|0.578689|
|B|RNN|0.481675|0.520134|0.448191|0.251259|0.369054|0.671214|
|B|LSTM|0.511738|0.519534|0.473133|0.249889|0.370416|0.668652|
|B|GRU|0.506820|0.527896|0.475803|0.251875|0.390023|0.665769|
|B|LTC|0.534035|0.531292|0.453225|0.250228|0.448740|0.613843|
|B|CfC|0.511699|0.518918|0.474423|0.251535|0.345741|0.692095|

원 STEP8BR 저장집계를그대로인용했다. NN은Origin/가격/모델별10Seed지표동일가중평균후5Origin동일가중평균,baseline은각Origin고정1결과후5Origin평균이다. 새금융수치/차이추정치를재계산하지않았다. 전체/코호트유효시장날짜·support·상세baseline1개수치는private원표를참조한다. 빈/실제한클래스BA·MacroF1=null,미지원Recall=null;실제양클래스단일예측은metric계산과DEGENERATE병기. 이번baseline40전체는BA/F1유효이며HMM부분집합null과구분한다.

NN−baseline BA/F1/Brier차이는traceability의저장8BR차이표에원값으로복사했다. Origin민감도는저장방향수/집계만공개하고deterministic개별코호트값은공개하지않는다. Momentum60대비BA우세Origin수는A:RNN2/LSTM3/GRU3/LTC3/CfC3,B:2/3/3/3/4(각5중)다. 평균순위는Origin전반의우월성이나선택기준이아니다.

지표별정확동률공동순위는traceability에저장값을정렬하여제공했다. A BA는LTC>CfC>GRU>RNN>LSTM>Momentum60>Climatology>Logistic>DMA200,B BA는LTC>GRU>RNN>LSTM>CfC>Momentum60>Climatology>Logistic>DMA200이다. MacroF1은두후보모두Momentum60가가장높고,A Brier는CfC,B는LSTM이가장낮다. Accuracy·Recall의순위도확인하되불균형클래스의accuracy/단일Recall을BA대신최적화하지않는다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
