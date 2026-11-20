# STEP6A_FORWARD_FILTER_AUDIT_KO

STEP6A는 설계·동결·정적 감사·합성 시험 단계다. 실제 금융 HMM fit/filtering, 신경망 학습·재학습, Test 재추론, checkpoint load/forward, 금융 p값·bootstrap 재실행, RAW5/LOG2 Ensemble, LTC τactual, GPU 및2026가격 사용은 모두0이다. HMM100후보/최종10개는 계획이며 학습 완료가 아니다. hmm_fit_enabled=false/hmm_filtering_enabled=false를 유지한다.

고정된 Train 파라미터 θ 아래 p(z_t|x_1…x_t,θ)만 쓴다. 한 시점의 prior는 직전 posterior×transition, 현재 Gaussian emission을 곱하고 log-stable 정규화한다. 미래 관측·전체 Viterbi·smoothing posterior를 과거의 실시간 상태로 쓰지 않는다.

세 범위는 별개다: **파라미터 추정=유지된 Train만 / filtering 관측=해당t까지 / Target=평가만**. Train에서 θ를 추정했다는 조건부 filtering이며, in-sample Train 상태를 당시의 미관측 전향적 예측이라고 주장하지 않는다. 합성 미래변형 검사는 θ를 고정한 조건에서 과거 posterior가 bitwise 불변인지 검사했다. Validation/Test 변형은 Train fit 입력 자체를 바꾸지 못한다.

마지막 유지 Train 관측 posterior를 저장하고, 그다음 공식 세션부터 모든 bridge·Validation·Test 관측을 순서대로 반영한다. Train 말단 purge20세션도 금융 관측으로서는 존재하므로 filtering에서는 빠뜨리지 않는다. Validation 말단의 label purge도 관측을 삭제하는 이유가 아니다. 각 이어붙임은 첫session_id=직전session_id+1이고 전체 expected session vector와 일치해야 한다. 필터링 시작을 Test 첫날로 재초기화하거나 중간 전이를 건너뛰지 않는다.

HMM filtering은 Test 연도 말까지 관측할 수 있지만,2025말단20개 미확정 Target은 레짐 성능평가에서 계속 제외한다.2026관측은 금지다. Test t후 관측을 한꺼번에 넣어 과거 상태를 다시 추정하지 않는다. 실제 filtering은 이번0건이며 합성에서 batch-prefix와 bridge 순차 continuation의 결과가 정확히 같았다.

후속 상태 경로는 Origin/Candidate별1개를50개 신경망 예측에 공통 적용한다. session 누락·중복·정렬 오류는 차단하며 누락 관측을 미래값으로 보간하지 않는다. 관측 가용성이 확인되지 않은 실시간 PIT를 인증하지 않는다.

상세 금융 input/date/checkpoint/identity 매핑과 비공개 SHA 관계는 로컬 ignored 경로에만 보존한다. 공개본은 코드·구조적 계약·합성 결과·집계·비민감 해시만 포함한다.
