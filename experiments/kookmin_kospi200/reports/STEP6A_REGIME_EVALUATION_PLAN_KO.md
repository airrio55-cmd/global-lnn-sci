# STEP6A_REGIME_EVALUATION_PLAN_KO

STEP6A는 설계·동결·정적 감사·합성 시험 단계다. 실제 금융 HMM fit/filtering, 신경망 학습·재학습, Test 재추론, checkpoint load/forward, 금융 p값·bootstrap 재실행, RAW5/LOG2 Ensemble, LTC τactual, GPU 및2026가격 사용은 모두0이다. HMM100후보/최종10개는 계획이며 학습 완료가 아니다. hmm_fit_enabled=false/hmm_filtering_enabled=false를 유지한다.

STEP5B의 기존500개 확률/Target/date/session_id/label_end를 읽기 전용으로 재사용하며 신경망 forward0이다. Origin/Candidate별 선택 HMM10개 각각의 상태 경로를 같은 코호트의10Seed×5Model=50개 예측에 공통 적용한다. 모델/신경망 Seed마다 HMM을 다시 fit하지 않는다.

평가 join 전에 Origin·Candidate, 보존 날짜·실제 Target·label_end·공식 session_id가 같아야 한다. 상태는 bridge를 포함한 전체 세션 경로에서 평가 날짜로만 선택하고, 라벨·예측확률을 상태 관측이나 HMM 선택으로 넘기지 않는다. 정의된 Test 날짜/Target은 바꾸지 않는다.

각 Low/High에 n, support0/support1, occupancy, BA, MacroF1, Recall0/1, positive prediction rate를 계산하고 Seed별 값과 기술적 평균·ddof1 표준편차를 보존한다. 전체 n=두 레짐 n합을 검사한다. 같은 날짜의50개 신경망 결과가 새로운 시장 날짜50개를 만드는 것은 아니다.

빈 레짐은 성능지표 모두null, occupancy는 정의된 전체 평가 n>0일때0으로 기록한다. 실제 한 클래스면 BA/MacroF1 null, 있는 클래스 Recall만 정의, 없는 클래스 Recall null. 단일 클래스 **예측**과 실제 Target 한 클래스를 구분한다. STEP5B policy v1을 그대로 재사용하며 threshold>0.5(동률0) 고정, 재튜닝하지 않는다. 실패/미정의를0으로 채우지 않는다.

수동3레짐(Low/Mid/High)과 HMM2레짐(Low/High)은 별도 표다. 같은 분류체계나 동일 범주 경계라고 주장하지 않는다. 이번에는 새로운 금융 레짐 성능/통계 p값을 만들지 않았고, 향후에도 기존20/80/100 가족에 레짐 가설을 사후 추가하지 않는다.

상세 금융 input/date/checkpoint/identity 매핑과 비공개 SHA 관계는 로컬 ignored 경로에만 보존한다. 공개본은 코드·구조적 계약·합성 결과·집계·비민감 해시만 포함한다.
