# STEP4A-1 O3 수동 레짐

사용자 승인 범위의 회고적·탐색적 CPU Train/Validation Pilot이다. A/B는 BOTH_UNVERIFIED이고 production-PIT는 BLOCKED다. 가격·모델·Seed·날짜·설정을 Validation 결과로 선택하지 않았다. 독립 Test2023 및 이후 가격 관측값, HMM fit, GPU, RAW5/외부피처/앙상블, τ 실측 forward, 확증 p값은 사용/실행하지 않았다. 2026년 관측 사용0이다. master production training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false는 변경하지 않았다.

Vol_Regime=Log_Ret.rolling(40).std(ddof1), O3 유지된 Train 기준일의30/70 분위수(linear)만 사용했다. Low≤q30, High≥q70, 나머지Mid다. A/B별로 독립 계산한 임계값을 학습 전에 고정했고2022 Validation으로 재계산하지 않았다.

| candidate | Train 시작 | Train 종료 | Train n | q30 | q70 |
| --- | --- | --- | --- | --- | --- |
| A | 2010-03-30 | 2021-12-02 | 2883 | 0.007659558104 | 0.010297714896 |
| B | 2010-03-30 | 2021-12-02 | 2883 | 0.007655982316 | 0.010297709869 |


## Validation support: 모델/Seed별 동일 날짜

| candidate | regime | n | n_class0 | n_class1 |
| --- | --- | --- | --- | --- |
| A | Low_Vol | 0 | 0 | 0 |
| A | Mid_Vol | 35 | 32 | 3 |
| A | High_Vol | 191 | 117 | 74 |
| B | Low_Vol | 0 | 0 | 0 |
| B | Mid_Vol | 35 | 32 | 3 |
| B | High_Vol | 191 | 117 | 74 |


빈 레짐 또는 실제 정답 클래스 하나이면 BA/MacroF1=null이다. Recall은 해당 실제 클래스 support가 없을 때null, 존재하면 계산한다. 실제 두 클래스이지만 단일 예측 클래스라면 지표를 계산하고 DEGENERATE_PREDICTION을 별도 기록한다. 없는 결과를0으로 채우지 않았다. n은 Seed당 원래 날짜 수이며 Seed를 합쳐 시장 표본 수를 늘리지 않는다.

## 모델별 두 Seed 평균/표본 표준편차

| candidate | model | regime | reported_seeds | metric_valid_seeds | n_per_seed | n_class0_per_seed | n_class1_per_seed | balanced_accuracy_mean | balanced_accuracy_std_ddof1 | macro_f1_mean | macro_f1_std_ddof1 | recall_class0_mean | recall_class1_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | CfC | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.672586 | 0.074280 | 0.605098 | 0.097884 | 0.405983 | 0.939189 |
| A | CfC | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| A | CfC | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.671875 | 0.132583 | 0.357920 | 0.186501 | 0.343750 | 1.000000 |
| A | GRU | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.640737 | 0.054393 | 0.573419 | 0.074734 | 0.376068 | 0.905405 |
| A | GRU | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| A | GRU | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.562500 | 0.088388 | 0.189474 | 0.156308 | 0.125000 | 1.000000 |
| A | LSTM | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.596558 | 0.052923 | 0.493949 | 0.107856 | 0.260684 | 0.932432 |
| A | LSTM | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| A | LSTM | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.531250 | 0.044194 | 0.139147 | 0.085135 | 0.062500 | 1.000000 |
| A | LTC | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.524024 | 0.033975 | 0.410568 | 0.185718 | 0.277778 | 0.770270 |
| A | LTC | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| A | LTC | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.458333 | 0.058926 | 0.224474 | 0.205805 | 0.250000 | 0.666667 |
| A | RNN | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.562630 | 0.024052 | 0.482426 | 0.102322 | 0.307692 | 0.817568 |
| A | RNN | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| A | RNN | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.554688 | 0.011049 | 0.185387 | 0.019741 | 0.109375 | 1.000000 |
| B | CfC | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.676369 | 0.051779 | 0.629163 | 0.030877 | 0.474359 | 0.878378 |
| B | CfC | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| B | CfC | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.710938 | 0.121534 | 0.415222 | 0.162948 | 0.421875 | 1.000000 |
| B | GRU | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.623094 | 0.029442 | 0.542882 | 0.031548 | 0.320513 | 0.925676 |
| B | GRU | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| B | GRU | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.562500 | 0.088388 | 0.189474 | 0.156308 | 0.125000 | 1.000000 |
| B | LSTM | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.596558 | 0.052923 | 0.493949 | 0.107856 | 0.260684 | 0.932432 |
| B | LSTM | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| B | LSTM | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.531250 | 0.044194 | 0.139147 | 0.085135 | 0.062500 | 1.000000 |
| B | LTC | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.520646 | 0.029197 | 0.407574 | 0.181484 | 0.277778 | 0.763514 |
| B | LTC | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| B | LTC | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.458333 | 0.058926 | 0.224474 | 0.205805 | 0.250000 | 0.666667 |
| B | RNN | High_Vol | 2 | 2 | 191 | 117 | 74 | 0.562630 | 0.024052 | 0.482426 | 0.102322 | 0.307692 | 0.817568 |
| B | RNN | Low_Vol | 2 | 0 | 0 | 0 | 0 | null | null | null | null | null | null |
| B | RNN | Mid_Vol | 2 | 2 | 35 | 32 | 3 | 0.562500 | 0.022097 | 0.198736 | 0.038619 | 0.125000 | 1.000000 |


각 Seed의 BA/MacroF1/Recall0/1/n/n0/n1은 [개별 CSV](../manifests/step4a1_manual_regime_metrics.csv)에 있다. 두 Seed 평균/표준편차는 탐색적 진단이다. 동일 best checkpoint의 저장된 Validation 확률만 분류했고 레짐 결과로 모델·경계·Seed를 선택하지 않았다. HMM fit/분류/결과표는 만들지 않았다.
