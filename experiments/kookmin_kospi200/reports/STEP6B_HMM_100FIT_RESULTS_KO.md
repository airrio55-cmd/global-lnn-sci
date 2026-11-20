# STEP6B_HMM_100FIT_RESULTS_KO

회고적 HMM 상태 분해와 고정 Test 예측의 기술적 분석이다. HMM 후보 실제fit100/100, 적격100, 부적격0, 실패0, 최종선택/순차filtering10/10, 연결한 기존신경망Test500/500이다. HMM은 새 신경망이 아니며 기존NN500fit에 더하지 않는다. 신경망학습·재추론/checkpoint forward,새금융bootstrap/Holm/p값,RAW5·LOG2 Ensemble,GPU,τactual,2026사용은모두0이다.

5Origin×A/B×동결10초기화의100개를 각각1회 학습했다. 실제 적격100/부적격0/실패0이며 전부 최종LL/수렴/finite parameter/양의정부호 covariance/Train hard state2개/고정lineage 기준을 통과했다. 모든코호트가 성공해 **최종HMM10개 완료**라고 보고한다. 완료/실패 seed 대체나 중복fit은0이다.

반복수의 다중fit 집계: 평균19.22, 중앙값20, 범위5~42. 2000회 cap을 수렴으로 간주한 후보는없다. HMM초기화 Seed와NN학습 Seed는별개다. 최종HMM1개가각코호트50개NN결과에공통적용됐다.

HMM Test점유율은5Origin동일가중 평균으로 A/B모두 Low24.6274%,High75.3726%다. 이는Train기준의잠재상태분해이며Test분위수로비율을강제하지않았다. 더세부적인시드별후보LL/실제상태평균/수렴마지막증분/점유율/파라미터SHA와선택은private에보존한다.

| candidate | method | regime | Origin_cohorts | occupancy_equal_Origin_mean | mean_Test_volatility_equal_Origin | positive_class_fraction_equal_Origin |
| --- | --- | --- | --- | --- | --- | --- |
| A | HMM | High_Vol | 5 | 0.753726 | 0.012789 | 0.545284 |
| A | HMM | Low_Vol | 5 | 0.246274 | 0.008991 | 0.513344 |
| A | MANUAL | High_Vol | 5 | 0.701139 | 0.012977 | 0.563345 |
| A | MANUAL | Low_Vol | 5 | 0.059266 | 0.006671 | 0.438258 |
| A | MANUAL | Mid_Vol | 5 | 0.239595 | 0.009372 | 0.444661 |
| B | HMM | High_Vol | 5 | 0.753726 | 0.012789 | 0.545284 |
| B | HMM | Low_Vol | 5 | 0.246274 | 0.008985 | 0.513344 |
| B | MANUAL | High_Vol | 5 | 0.701139 | 0.012977 | 0.563345 |
| B | MANUAL | Low_Vol | 5 | 0.062492 | 0.006718 | 0.430068 |
| B | MANUAL | Mid_Vol | 5 | 0.236369 | 0.009374 | 0.449522 |


A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING을 유지한다. O1~O4 Test의 후속 Validation 노출 한계를 인정하며 이 결과를 전향적 미관측시장/PIT 인증으로 주장하지 않는다.

개별 Train 날짜/행 수/input·scaler·HMM parameter·posterior·Test Target/확률/identity·SHA 매핑은 ignored private에만 보존했다. 공개본은 여러fit/Origin의 집계·구조적 방법·비민감 해시만 포함한다. n/support0/support1의 개별 상세표는 private 감사자료에 있다.
