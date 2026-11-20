# STEP8BR BASELINE_RESULTS

원 STEP8B BLOCKED40·실패NPZ·승인·source·ledger를그대로보존하고독립STEP8B-R40개identity를실행했다. 새완료40/BLOCKED0,Logistic Train-only fit10,Climatology추정10,가격규칙평가20이다. 과거NN학습횟수500에Logistic/Climatology/규칙을추가하지않는다. 기존NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED 및 이전9799파일/STEP8B scratch46파일 변경0. NN재학습·checkpoint load/forward·HMM fit/refilter·τ추가계측·새금융Bootstrap/Holm/p값·Ensemble/GPU·2026시장관측사용0. master flags=false.

이번 결과는 retrospective exploratory benchmark다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED는storage복구로변하지않는다. O1~O4 Test와후속Validation의역사적중복,Origin·Seed·중첩label의존성을유지한다. 거래수익성·전향적일반화·통계적우월성을인증하지않으며가격/모델/Seed/threshold를사후선택하지않는다.

|가격|모델|BA|Macro F1|Brier|Recall0|Recall1|Accuracy|단일클래스 예측 결과수|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|A|CLIMATOLOGY|0.500000|0.340082|0.251364|0.000000|1.000000|0.530037|5|
|A|LOGISTIC|0.492492|0.359634|0.251151|0.068318|0.916665|0.491882|1|
|A|DMA200|0.482180|0.442626|0.467059|0.430809|0.533551|0.532941|1|
|A|MOMENTUM60|0.504416|0.491019|0.425077|0.430143|0.578689|0.574923|0|
|B|CLIMATOLOGY|0.500000|0.340082|0.251364|0.000000|1.000000|0.530037|5|
|B|LOGISTIC|0.492492|0.359634|0.251150|0.068318|0.916665|0.491882|1|
|B|DMA200|0.482180|0.442626|0.467059|0.430809|0.533551|0.532941|1|
|B|MOMENTUM60|0.504416|0.491019|0.425077|0.430143|0.578689|0.574923|0|

각후보별5Origin 동일가중평균이다. publicJSON에는Origin간표본SD도보존했다. Climatology는모든10결과에서양의상수확률이0.5를넘어항상1예측이다. Logistic·DMA200은각후보에서1개결과가단일클래스예측, Momentum60은0개였다. 실제Train/전체Test는모두두클래스여서금융본평가의BA/F1 null은0개이며한클래스/동률정책은합성시험으로확인했다. 규칙의0/1 Brier는degenerate probability 점수이고calibration으로해석하지않는다. 실패·결측을0으로대체하지않았다.

확인일:2026-11-20 KST. 근거:원STEP8B동결사양·실패lineage,STEP8BR안전재읽기검사/실행ledger,기존STEP5BNN저장지표. 새공식가격/PIT출처검증은하지않았다.
