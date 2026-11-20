# STEP8A TAU_MECHANISM_LIMITS

이번 단계는 저장 결과·checkpoint-level τ 요약의 읽기 전용 감사와 기술통계/설계다. checkpoint는 byte SHA만 대조하며 역직렬화·forward하지 않았다. NN500·Test500·STEP5C600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED를 보존한다. τ 전체 분류는 퇴화24/100, 유효 퇴화23개/사용23개, 비퇴화76/76, 전체99/100이다. 기존 확률 exact99개를 유지하고 중단1개를 재시도·대체·0채움하지 않았다. 신규 NN/기준모형 학습·checkpoint load/forward·Test 재생성·HMM fit/refilter·τ추가계측·금융bootstrap/Holm/p값·Ensemble·GPU·2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, historical18KST available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. O1~O4 Test와 후속 Validation의 역사적 중복 및 Origin/Seed/뉴런/window 의존성을 유지한다.

τ_raw=positive(cm)/positive(gleak), τ_effective=positive(cm)/(positive(gleak)+ΣG_sensory(x)+ΣG_recurrent(h)). Positive1회/constraints=True/elapsed1/6substep 계약은 변경하지 않는다. τ_raw의 checkpoint 간 차이는 파라미터 비율의 기술적 차이이며 어떤 cm 또는 gleak이 원인인지 요약만으로 분해할 수 없다. τ_effective에는 입력과 hidden 전도도, neuron/window 구성, Origin·Seed 학습결과가 함께 반영된다.

저장 요약으로 raw/effective의 median·quantile·within-checkpoint std, 관측entry와substep, 고정HMM 그룹을 비교할 수 있다. 그러나 감각/순환 conductance의 개별 기여·cm/gleak 분리·τ와시간의trajectory·Jacobian·입력반사실 효과는 checkpoint-level 요약만으로 식별되지 않는다. raw와 effective median의 비율이나 차이를 conductance 기여율로 바꾸지 않는다. private raw arrays가 존재해도 이번에는 열거나 새 분해계산하지 않았다. 추가 계산/설계는 별도 승인 범위다. τ 단위는 model_observation_step이며 실제 일수·경제 기억·인과 메커니즘이 아니다.

확인일 2026-11-20 KST. 근거: 보존 STEP4D/5B/5C/6B/7B 보고서·execution manifest 및 checkpoint-level 요약. 신규 공식 원천확인·금융실험은 수행하지 않았다.

저장 checkpoint별 raw τ median의 평균은 퇴화23개 1.0082001, 비퇴화76개 0.9906370이다. 이는 effective τ의 반대 방향 기술적 차이이며 raw/effective 차이를 개별 conductance 기여로 분해한 것은 아니다.
