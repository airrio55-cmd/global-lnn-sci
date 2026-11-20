# STEP9B1R MASTER_REVIEW

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

최종 판정은 **BLOCKED_METHOD_NOT_VALIDATED** 이다. 기술적으로 구현된 방법은9개이나, 사전에 정한 핵심 holdout 적격성 조건을 모두 충족한 방법은 없다. 약한 의존성에서 좋아 보이는 결과나 높은 nominal power를 택해 금융 검정에 사용하지 않는다. 타당성 문제가 해소되지 않아 STEP9B-2를 진행하지 않는 선택을 논문에 명시할 수 있다.

비교 대상은 MBB20/40/60, stationary bootstrap 평균길이40/120, local moving blocks L40·위치창100, BA influence-function HAC Bartlett40/120 및 dependent Gaussian multiplier120이다. tapered block bootstrap은 조건·구현 차이를 문헌 검토했으나 현재 ratio-metric에 대한 검증된 구현을 만들지 않아 미실행으로 표시했다. calendar/Origin-aware는 정렬/estimand 처리이지 독립적인 타당성 보증이 아니다.

원래 estimand를 유지했다: 각Origin의 NN10Seed metric 평균−baseline1개 metric, 이후5Origin 동일가중. BA는 class별recall에 선형이므로 Seed의 **분류 indicator 평균**으로 계산을 빠르게 했지만 mean probability의Ensemble로 대체하지 않았다. F1은 선형이 아니므로 실제family 실험에서Seed별F1을 먼저 계산했다. 추론법의 sampling law·linearization 가정 차이는 별도안으로 명시한다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
