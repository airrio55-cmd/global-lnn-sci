# STEP 3B 이후 필수 Gate

회고적·탐색적 CPU Train/Validation 구현 진단이다. Validation은 조기 종료와 checkpoint 선택에 사용됐으므로 독립 일반화 성능이 아니다. A/B는 BOTH_UNVERIFIED, production-PIT는 BLOCKED이며 가격·모델·Seed를 선택하지 않았다. 독립 Test 평가, HMM fit, GPU, 전체 5Origin×10Seed, Ablation은 실행하지 않았다. production training_enabled=false, hmm_fit_enabled=false를 유지한다.

이번 승인 범위의 40개 identity 중 기존10 재사용/신규30개 완료, 신규실패0, BLOCKED0다. 실행 완료는 다음 본실험 승인이나 production-PIT 인증을 의미하지 않는다. 수동 레짐 지표는 동일 Validation 예측에 대한 탐색적 분석이며 HMM은 미실행이다.

| 항목 | 현재 판정 | 다음 단계에 필요한 사항 |
| --- | --- | --- |
| 승인된 O1/O2·Seed2/12·F1 CPU Pilot 실행 | PASS | 신규 추가 실행은 별도 승인 |
| 원본 정의·환경·Train-only scaler·purging | PASS | 변경 시 소스/환경/데이터 hash 재동결 |
| 가격 A/B 최종 주 분석 소스 | BLOCKED | 공급처·지수 코드·단위·추출 방법·개정정책 증빙으로 결정, Validation 우열 사용 금지 |
| t 18:00 KST 국내 종가 가용성 | BLOCKED | 실제 공급처 역사적 공개/가용시각 증빙; 생산 PIT PASS로 승격 금지 |
| 외국인 순매수 입력 | BLOCKED | 시장 범위·현물/선물·단위·부호·잠정/확정·최초 공개·개정 이력 |
| NASDAQ/SOX 및 전체5피처 | BLOCKED | 미국 세션 종료와 공급처 실제 공개 지연을 구분한 PIT 증빙 |
| 전체5Origin×10Seed 및 LNN Single/Ensemble | BLOCKED | 가격/정보시점 계약·사양·예산 동결과 별도 실행 승인 |
| 전체 Ablation | BLOCKED | 공통 날짜·외부 피처 PIT·별도 실행 승인 |
| HMM | BLOCKED | 동일 초기화 목록 동결, Train-only fit/상태명, 순차 forward filtering, 별도 승인 |
| LTC 시간상수 실측 | BLOCKED | 원시/유효 τ·단위·elapsed_time·constraint 검증 및 별도 forward 승인 |
| 독립 Test 평가 | BLOCKED | 사전 확정 프로토콜·분리 저장·선택 금지·별도 승인 |
| 통계적 확증 | BLOCKED | 두 Seed 표준편차는 탐색적; 날짜 paired moving-block bootstrap20/40/60·10,000회와 Holm 계획 별도 실행 |

필요한 사용자 결정은 출처 증빙을 바탕으로 한 최종 가격 소스, 국내 입력의 의사결정시각 계약, 후속 실행 범위/예산 승인이다. 현재 Pilot의 결과를 보고 주 분석 자료·Seed·모델·레짐 임계값을 정하지 않는다. 기존 production training_enabled=false와 hmm_fit_enabled=false는 계속 유지한다. 이번 30개 완료 identity는 재실행하지 않는다.

GitHub에는 공개 가능한 코드·모델별/Seed별 집계·검증 hash만 보존한다. 가격 원자료, 일별 레이블·확률, checkpoint 및 비공개 라이선스 자료는 게시하지 않는다. main과 JOF V14/V15는 유지한다.
