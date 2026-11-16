# STEP3D LTC 세 Origin 진단

설계2: A/B 병렬 회고적·탐색적 F1 CPU Train/Validation 연구다. A/B=BOTH_UNVERIFIED, production-PIT=BLOCKED를 유지한다. Validation으로 주 가격·모델·Seed·사양을 선택하지 않았다. 독립 Test/HMM/GPU/외부5피처/Ensemble/2026 관측 사용은 이번 단계0건이다.

| origin | candidate | seed | model | epochs | best_epoch | validation_BA | macro_f1 | recall0 | recall1 | accuracy | brier | prediction_positive_rate | degenerate_epoch_ratio | prediction_status | degenerate_prediction_epochs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | A | 2 | LTC | 16 | 6 | 0.511935 | 0.485714 | 0.542857 | 0.481013 | 0.500000 | 0.248523 | 0.473684 | 0.687500 | TWO_CLASS_PREDICTION | 11 |
| O1 | B | 2 | LTC | 16 | 6 | 0.511935 | 0.485714 | 0.542857 | 0.481013 | 0.500000 | 0.248523 | 0.473684 | 0.687500 | TWO_CLASS_PREDICTION | 11 |
| O1 | A | 12 | LTC | 11 | 1 | 0.500000 | 0.409326 | 0.000000 | 1.000000 | 0.692982 | 0.235897 | 1.000000 | 0.818182 | DEGENERATE_PREDICTION | 9 |
| O1 | B | 12 | LTC | 11 | 1 | 0.500000 | 0.409326 | 0.000000 | 1.000000 | 0.692982 | 0.235897 | 1.000000 | 0.818182 | DEGENERATE_PREDICTION | 9 |
| O2 | A | 2 | LTC | 31 | 21 | 0.580664 | 0.565714 | 0.480916 | 0.680412 | 0.565789 | 0.249096 | 0.587719 | 0.645161 | TWO_CLASS_PREDICTION | 20 |
| O2 | B | 2 | LTC | 31 | 21 | 0.571693 | 0.556941 | 0.473282 | 0.670103 | 0.557018 | 0.249117 | 0.587719 | 0.645161 | TWO_CLASS_PREDICTION | 20 |
| O2 | A | 12 | LTC | 18 | 8 | 0.579917 | 0.548427 | 0.396947 | 0.762887 | 0.552632 | 0.249762 | 0.671053 | 0.833333 | TWO_CLASS_PREDICTION | 15 |
| O2 | B | 12 | LTC | 18 | 8 | 0.579917 | 0.548427 | 0.396947 | 0.762887 | 0.552632 | 0.249766 | 0.671053 | 0.833333 | TWO_CLASS_PREDICTION | 15 |
| O3 | A | 2 | LTC | 17 | 7 | 0.538046 | 0.524941 | 0.543624 | 0.532468 | 0.539823 | 0.250536 | 0.482301 | 0.941176 | TWO_CLASS_PREDICTION | 16 |
| O3 | B | 2 | LTC | 17 | 7 | 0.531552 | 0.519587 | 0.543624 | 0.519481 | 0.535398 | 0.250533 | 0.477876 | 0.941176 | TWO_CLASS_PREDICTION | 16 |
| O3 | A | 12 | LTC | 11 | 1 | 0.500000 | 0.254125 | 0.000000 | 1.000000 | 0.340708 | 0.262837 | 1.000000 | 1.000000 | DEGENERATE_PREDICTION | 11 |
| O3 | B | 12 | LTC | 11 | 1 | 0.500000 | 0.254125 | 0.000000 | 1.000000 | 0.340708 | 0.262842 | 1.000000 | 1.000000 | DEGENERATE_PREDICTION | 11 |

단일 클래스 예측은 DEGENERATE_PREDICTION으로 별도 표시하며 NaN/손실 발산과 동일시하지 않는다. 기존 O3 4개 LTC는 수치 발산 실패가 아니라 완료된 퇴화 예측 사례다. Seed를 교체하거나 loss·patience·epoch를 변경하지 않았다. best epoch는 strict Validation BA의 최초 최고점이며 history 전체의 단일 클래스 epoch 비율을 보존했다.

O3 Seed2는 A/B 모두17epoch, best7이며 최적 checkpoint는 두 클래스 예측이다. 다만16/17epoch(94.12%)에서 단일 클래스 예측이었다. Seed12는 A/B 모두11epoch, best1, BA0.5이며11/11epoch(100%) 단일 클래스 예측이었다. 이 차이를 보존하며 수치 발산으로 오표기하지 않는다.
