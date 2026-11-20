# STEP6B_LTC_REGIME_DIAGNOSTICS_KO

회고적 HMM 상태 분해와 고정 Test 예측의 기술적 분석이다. HMM 후보 실제fit100/100, 적격100, 부적격0, 실패0, 최종선택/순차filtering10/10, 연결한 기존신경망Test500/500이다. HMM은 새 신경망이 아니며 기존NN500fit에 더하지 않는다. 신경망학습·재추론/checkpoint forward,새금융bootstrap/Holm/p값,RAW5·LOG2 Ensemble,GPU,τactual,2026사용은모두0이다.

기존전체Test의LTC단일클래스예측24/100개를제거하거나교체하지않았다. 레짐부분집합에서단일클래스가되는추가예측도별도로집계했다. 아래수치는NN결과개수이며같은시장날짜의Seed반복을독립시장관측으로세지않는다. 실제Target한클래스인레짐과예측만한클래스인경우를분리했다.

LTC는A/B각각High에서12/50개,Low에서24/50개NN결과가단일클래스예측이었다. Low에서는후보별실제Target한클래스인레짐이각10개NN결과에해당해BA유효수는40/50였다. High는50/50이다. 따라서Low BA와High BA의단순비교는같은유효Origin집합의비교가아닐수있다. null제외는정의상무효처리이며낮은점수Seed제거가아니다.

| candidate | model | regime | completed_NN_results | degenerate_predictions | actual_single_class_regimes | BA_valid | BA_mean | MacroF1_mean | Recall0_mean | Recall1_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | LTC | High_Vol | 50 | 12 | 0 | 50 | 0.520894 | 0.442358 | 0.445849 | 0.595939 |
| A | LTC | Low_Vol | 50 | 24 | 10 | 40 | 0.533927 | 0.416822 | 0.410214 | 0.726112 |
| B | LTC | High_Vol | 50 | 12 | 0 | 50 | 0.519338 | 0.442956 | 0.432459 | 0.606216 |
| B | LTC | Low_Vol | 50 | 24 | 10 | 40 | 0.534665 | 0.417572 | 0.408230 | 0.708881 |

다른모델도동일진단규칙을적용했다. 전체모델표는다음과같다. 새로운레짐p값/가설가족을만들지않았다.

| candidate | model | regime | completed_NN_results | degenerate_predictions | actual_single_class_regimes | empty_regimes | BA_valid | BA_mean | MacroF1_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | CfC | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.531554 | 0.484445 |
| A | CfC | Low_Vol | 50 | 17 | 10 | 0 | 40 | 0.548089 | 0.440362 |
| A | GRU | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.530769 | 0.472932 |
| A | GRU | Low_Vol | 50 | 20 | 10 | 0 | 40 | 0.556232 | 0.446944 |
| A | LSTM | High_Vol | 50 | 1 | 0 | 0 | 50 | 0.513715 | 0.463928 |
| A | LSTM | Low_Vol | 50 | 21 | 10 | 0 | 40 | 0.541677 | 0.428233 |
| A | LTC | High_Vol | 50 | 12 | 0 | 0 | 50 | 0.520894 | 0.442358 |
| A | LTC | Low_Vol | 50 | 24 | 10 | 0 | 40 | 0.533927 | 0.416822 |
| A | RNN | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.520228 | 0.446483 |
| A | RNN | Low_Vol | 50 | 19 | 10 | 0 | 40 | 0.568158 | 0.428176 |
| B | CfC | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.525830 | 0.477851 |
| B | CfC | Low_Vol | 50 | 17 | 10 | 0 | 40 | 0.528912 | 0.423776 |
| B | GRU | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.530160 | 0.468715 |
| B | GRU | Low_Vol | 50 | 20 | 10 | 0 | 40 | 0.559350 | 0.449973 |
| B | LSTM | High_Vol | 50 | 1 | 0 | 0 | 50 | 0.509950 | 0.464169 |
| B | LSTM | Low_Vol | 50 | 21 | 10 | 0 | 40 | 0.556890 | 0.442889 |
| B | LTC | High_Vol | 50 | 12 | 0 | 0 | 50 | 0.519338 | 0.442956 |
| B | LTC | Low_Vol | 50 | 24 | 10 | 0 | 40 | 0.534665 | 0.417572 |
| B | RNN | High_Vol | 50 | 0 | 0 | 0 | 50 | 0.522468 | 0.450341 |
| B | RNN | Low_Vol | 50 | 19 | 10 | 0 | 40 | 0.565339 | 0.425331 |


A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING을 유지한다. O1~O4 Test의 후속 Validation 노출 한계를 인정하며 이 결과를 전향적 미관측시장/PIT 인증으로 주장하지 않는다.

개별 Train 날짜/행 수/input·scaler·HMM parameter·posterior·Test Target/확률/identity·SHA 매핑은 ignored private에만 보존했다. 공개본은 여러fit/Origin의 집계·구조적 방법·비민감 해시만 포함한다. n/support0/support1의 개별 상세표는 private 감사자료에 있다.
