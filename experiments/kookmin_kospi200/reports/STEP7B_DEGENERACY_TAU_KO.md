# STEP7B DEGENERACY_TAU

정확100 LTC best checkpoint 중 실제 계측 완료99, BLOCKED1, 미시도0. 금융 forward 시작/예산차감100회·완료99회, checkpoint load100회. 기존 확률 exact 일치99개. 실패·결측을0으로 채우거나 다른 모델로 대체하지 않았다. 기존 NN500·Test500·통계600행·HMM100후보/최종10 보존, 이전8651파일 변경0.

CPU FP32 / AMP OFF / eval / no_grad / worker1. 추가 학습·HMM 재적합/refilter·기존 Test 성능 재산정·Ensemble·GPU·금융 bootstrap/Holm/p값·2026관측 사용0. 기존 production flags=false. 완료 identity 재실행0, 추가 baseline 금융 forward0.

단위 model_observation_step. τ는 고정 입력·상태 conductance 진단량이며 초·실제 영업일·경제적 기억길이·Jacobian 고유시간이 아니다. A/B BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. Origin/Seed/뉴런/중첩window는 독립 시장 표본이 아니다. O1~O4 Test와 후속 Validation의 역사적 중복 한계를 유지한다. 결과로 가격·모델·Seed·threshold·HMM을 선택하지 않는다. 금융 τ와 예측퇴화의 차이를 인과로 해석하지 않는다.

확정 τ 집계의 전체Test 퇴화/비퇴화 checkpoint는 23/76개다. 중단 예약은 원래 퇴화 분류에 유지하되 확정 τ 분석에서 제외한다. 기존 전체Test 단일클래스24개/비퇴화76개의 그룹을 그대로 사용했다. τ로 그룹을 바꾸거나 제외하지 않았다. 레짐부분집합 단일클래스 예측은 별도 STEP6B 진단이며 전체Test 퇴화와 다른 사건이다. 소수군·Seed/Origin 구성의 의존성으로 차이를 원인/성능우수성으로 해석할 수 없다.

| 구분 | 유효/전체 checkpoint | q05 평균 | q25 평균 | median 평균 ± 표본SD | q75 평균 | q95 평균 |
|---|---:|---:|---:|---:|---:|---:|
| ALL / False | 76/76 | 0.729328 | 0.851036 | 0.990637 ± 0.030395 | 1.174798 | 1.414475 |
| ALL / True | 23/23 | 0.7604662 | 0.863857 | 1.0082 ± 0.025729 | 1.190734 | 1.371147 |
| ALL / False | 76/76 | 0.03953309 | 0.04464351 | 0.04902215 ± 0.014436 | 0.05416974 | 0.06369253 |
| ALL / True | 23/23 | 0.02615365 | 0.02782213 | 0.02909928 ± 0.00024713 | 0.03054163 | 0.03299263 |

확인일: 2026-11-20 KST. 근거: 동결 STEP7A 설치 ncps 1.0.1 소스SHA 및 이번 실제 read-only 실행 ledger/저장 확률·HMM 파일SHA. 공식 구현: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py . 설치소스 대조이며 과거 논문 환경이나 가격 원천의 소급 인증은 아니다.
