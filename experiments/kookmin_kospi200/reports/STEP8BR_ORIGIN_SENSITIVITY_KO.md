# STEP8BR ORIGIN_SENSITIVITY

원 STEP8B BLOCKED40·실패NPZ·승인·source·ledger를그대로보존하고독립STEP8B-R40개identity를실행했다. 새완료40/BLOCKED0,Logistic Train-only fit10,Climatology추정10,가격규칙평가20이다. 과거NN학습횟수500에Logistic/Climatology/규칙을추가하지않는다. 기존NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED 및 이전9799파일/STEP8B scratch46파일 변경0. NN재학습·checkpoint load/forward·HMM fit/refilter·τ추가계측·새금융Bootstrap/Holm/p값·Ensemble/GPU·2026시장관측사용0. master flags=false.

이번 결과는 retrospective exploratory benchmark다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED는storage복구로변하지않는다. O1~O4 Test와후속Validation의역사적중복,Origin·Seed·중첩label의존성을유지한다. 거래수익성·전향적일반화·통계적우월성을인증하지않으며가격/모델/Seed/threshold를사후선택하지않는다.

Origin×Candidate별전체NN/기준모형BA/MacroF1/Brier/Recall/단일예측표는ignored private에보존한다. deterministic baseline1개의코호트성능이공개역산되지않도록공개Origin표는A/B에서NN이baseline보다좋음/나쁨/동률인후보개수만제공하고수치본표는공개하지않는다. A/B주분석은분리한5Origin집계다. 후보두개도독립시장복제가아니다.

|Origin|NN|기준모형|BA NN우세후보/2|BA NN열세후보/2|F1 NN우세후보/2|Brier NN우세후보/2|
|---|---|---|---:|---:|---:|---:|
|O1|RNN|CLIMATOLOGY|0|2|2|2|
|O1|RNN|MOMENTUM60|0|2|0|2|
|O1|LSTM|CLIMATOLOGY|0|2|2|2|
|O1|LSTM|MOMENTUM60|0|2|0|2|
|O1|GRU|CLIMATOLOGY|0|2|2|1|
|O1|GRU|MOMENTUM60|0|2|0|2|
|O1|LTC|CLIMATOLOGY|2|0|2|2|
|O1|LTC|MOMENTUM60|0|2|0|2|
|O1|CfC|CLIMATOLOGY|2|0|2|2|
|O1|CfC|MOMENTUM60|1|1|0|2|
|O2|RNN|CLIMATOLOGY|2|0|2|2|
|O2|RNN|MOMENTUM60|0|2|0|2|
|O2|LSTM|CLIMATOLOGY|2|0|2|2|
|O2|LSTM|MOMENTUM60|2|0|0|2|
|O2|GRU|CLIMATOLOGY|2|0|2|2|
|O2|GRU|MOMENTUM60|2|0|0|2|
|O2|LTC|CLIMATOLOGY|2|0|2|2|
|O2|LTC|MOMENTUM60|2|0|0|2|
|O2|CfC|CLIMATOLOGY|2|0|2|2|
|O2|CfC|MOMENTUM60|2|0|0|2|
|O3|RNN|CLIMATOLOGY|2|0|2|0|
|O3|RNN|MOMENTUM60|2|0|2|2|
|O3|LSTM|CLIMATOLOGY|2|0|2|2|
|O3|LSTM|MOMENTUM60|2|0|2|2|
|O3|GRU|CLIMATOLOGY|2|0|2|2|
|O3|GRU|MOMENTUM60|2|0|2|2|
|O3|LTC|CLIMATOLOGY|2|0|2|0|
|O3|LTC|MOMENTUM60|2|0|0|2|
|O3|CfC|CLIMATOLOGY|2|0|2|0|
|O3|CfC|MOMENTUM60|2|0|2|2|
|O4|RNN|CLIMATOLOGY|2|0|2|2|
|O4|RNN|MOMENTUM60|0|2|0|2|
|O4|LSTM|CLIMATOLOGY|2|0|2|1|
|O4|LSTM|MOMENTUM60|0|2|0|2|
|O4|GRU|CLIMATOLOGY|2|0|2|0|
|O4|GRU|MOMENTUM60|0|2|0|2|
|O4|LTC|CLIMATOLOGY|2|0|2|2|
|O4|LTC|MOMENTUM60|0|2|0|2|
|O4|CfC|CLIMATOLOGY|1|1|2|2|
|O4|CfC|MOMENTUM60|0|2|0|2|
|O5|RNN|CLIMATOLOGY|0|2|0|0|
|O5|RNN|MOMENTUM60|2|0|2|2|
|O5|LSTM|CLIMATOLOGY|0|2|0|0|
|O5|LSTM|MOMENTUM60|2|0|2|2|
|O5|GRU|CLIMATOLOGY|2|0|2|0|
|O5|GRU|MOMENTUM60|2|0|2|2|
|O5|LTC|CLIMATOLOGY|2|0|2|0|
|O5|LTC|MOMENTUM60|2|0|2|2|
|O5|CfC|CLIMATOLOGY|2|0|2|0|
|O5|CfC|MOMENTUM60|2|0|2|2|

가격A/B의baseline분류BA/F1/Recall의5Origin평균은같았고Logistic의Brier에는미세한수치차이가있다. 이는가격출처가인증됐거나두후보가동일하다는뜻이아니다. aggregate B−A 평균/방향수는JSON에있으며일별값/개별코호트차이는공개하지않는다.

확인일:2026-11-20 KST. 근거:원STEP8B동결사양·실패lineage,STEP8BR안전재읽기검사/실행ledger,기존STEP5BNN저장지표. 새공식가격/PIT출처검증은하지않았다.
