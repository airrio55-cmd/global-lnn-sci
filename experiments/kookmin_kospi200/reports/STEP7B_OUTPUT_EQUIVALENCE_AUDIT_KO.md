# STEP7B OUTPUT_EQUIVALENCE_AUDIT

정확100 LTC best checkpoint 중 실제 계측 완료99, BLOCKED1, 미시도0. 금융 forward 시작/예산차감100회·완료99회, checkpoint load100회. 기존 확률 exact 일치99개. 실패·결측을0으로 채우거나 다른 모델로 대체하지 않았다. 기존 NN500·Test500·통계600행·HMM100후보/최종10 보존, 이전8651파일 변경0.

CPU FP32 / AMP OFF / eval / no_grad / worker1. 추가 학습·HMM 재적합/refilter·기존 Test 성능 재산정·Ensemble·GPU·금융 bootstrap/Holm/p값·2026관측 사용0. 기존 production flags=false. 완료 identity 재실행0, 추가 baseline 금융 forward0.

단위 model_observation_step. τ는 고정 입력·상태 conductance 진단량이며 초·실제 영업일·경제적 기억길이·Jacobian 고유시간이 아니다. A/B BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. Origin/Seed/뉴런/중첩window는 독립 시장 표본이 아니다. O1~O4 Test와 후속 Validation의 역사적 중복 한계를 유지한다. 결과로 가격·모델·Seed·threshold·HMM을 선택하지 않는다. 금융 τ와 예측퇴화의 차이를 인과로 해석하지 않는다.

프로세스가 완료 기록 없이 종료된 예약 identity 1개는 BLOCKED로 유지하며 재실행하지 않았다. OOM 기록은 없고 종료 원인은 UNKNOWN이다. 원 확률과의 불일치로 확인된 사건과 구분한다. 사전 동결 기준 float32 확률 배열 exact equality를 사용했다. 기존 STEP5B와 동일 전체 cohort batch를 한 번 처리했다. 사후 tolerance 완화/추가 baseline/새 checkpoint 선택은 금지했다. raw logits 저장본이 없어 금융 logits 직접 비교를 주장하지 않는다. 원본 softmax 확률과 identity·날짜·session·label_end 및 dtype을 비교했다. 파라미터 fingerprint와 Python/NumPy/Torch RNG 불변을 모든 성공 모델에서 확인했다. 실패 모델의 τ는 확정 분석에 포함하지 않는다.

확인일: 2026-11-20 KST. 근거: 동결 STEP7A 설치 ncps 1.0.1 소스SHA 및 이번 실제 read-only 실행 ledger/저장 확률·HMM 파일SHA. 공식 구현: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py . 설치소스 대조이며 과거 논문 환경이나 가격 원천의 소급 인증은 아니다.
