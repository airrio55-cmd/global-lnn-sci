# STEP7B HMM_REGIME_TAU

정확100 LTC best checkpoint 중 실제 계측 완료99, BLOCKED1, 미시도0. 금융 forward 시작/예산차감100회·완료99회, checkpoint load100회. 기존 확률 exact 일치99개. 실패·결측을0으로 채우거나 다른 모델로 대체하지 않았다. 기존 NN500·Test500·통계600행·HMM100후보/최종10 보존, 이전8651파일 변경0.

CPU FP32 / AMP OFF / eval / no_grad / worker1. 추가 학습·HMM 재적합/refilter·기존 Test 성능 재산정·Ensemble·GPU·금융 bootstrap/Holm/p값·2026관측 사용0. 기존 production flags=false. 완료 identity 재실행0, 추가 baseline 금융 forward0.

단위 model_observation_step. τ는 고정 입력·상태 conductance 진단량이며 초·실제 영업일·경제적 기억길이·Jacobian 고유시간이 아니다. A/B BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. Origin/Seed/뉴런/중첩window는 독립 시장 표본이 아니다. O1~O4 Test와 후속 Validation의 역사적 중복 한계를 유지한다. 결과로 가격·모델·Seed·threshold·HMM을 선택하지 않는다. 금융 τ와 예측퇴화의 차이를 인과로 해석하지 않는다.

기존 STEP6B Low_Vol/High_Vol을 재학습·재명명·refilter하지 않고 prediction base date에 연결했다. 명칭은 “해당 예측 시점의 시장 레짐별 모델 내부 τ 분포”다. window 안 과거 날짜별 시장 상태를 의미하지 않는다. 같은 Origin/Candidate HMM 경로는 모든Seed에 공통이다. n_predictions는 Seed를 곱하지 않은 후보별 시장 기준일 수이며 JSON에 기록했다. 각 checkpoint 레짐 요약 후 집계했다. 빈 레짐은null, 작은 레짐/Origin구성 차이로 직접 인과 비교는 불가하다.

| 구분 | 유효/전체 checkpoint | q05 평균 | q25 평균 | median 평균 ± 표본SD | q75 평균 | q95 평균 |
|---|---:|---:|---:|---:|---:|---:|
| A / Low_Vol | 50/50 | 0.03609644 | 0.04032161 | 0.04400416 ± 0.014667 | 0.04832227 | 0.05699818 |
| A / High_Vol | 50/50 | 0.03628571 | 0.04075033 | 0.04461231 ± 0.015906 | 0.04923727 | 0.05823585 |
| B / Low_Vol | 49/49 | 0.03624302 | 0.04018429 | 0.04350117 ± 0.013753 | 0.04722828 | 0.05376939 |
| B / High_Vol | 49/49 | 0.03636727 | 0.04050272 | 0.04396438 ± 0.014605 | 0.04791482 | 0.05468074 |

확인일: 2026-11-20 KST. 근거: 동결 STEP7A 설치 ncps 1.0.1 소스SHA 및 이번 실제 read-only 실행 ledger/저장 확률·HMM 파일SHA. 공식 구현: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py . 설치소스 대조이며 과거 논문 환경이나 가격 원천의 소급 인증은 아니다.
