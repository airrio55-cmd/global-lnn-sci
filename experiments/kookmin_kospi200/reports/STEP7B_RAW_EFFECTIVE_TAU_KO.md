# STEP7B RAW_EFFECTIVE_TAU

정확100 LTC best checkpoint 중 실제 계측 완료99, BLOCKED1, 미시도0. 금융 forward 시작/예산차감100회·완료99회, checkpoint load100회. 기존 확률 exact 일치99개. 실패·결측을0으로 채우거나 다른 모델로 대체하지 않았다. 기존 NN500·Test500·통계600행·HMM100후보/최종10 보존, 이전8651파일 변경0.

CPU FP32 / AMP OFF / eval / no_grad / worker1. 추가 학습·HMM 재적합/refilter·기존 Test 성능 재산정·Ensemble·GPU·금융 bootstrap/Holm/p값·2026관측 사용0. 기존 production flags=false. 완료 identity 재실행0, 추가 baseline 금융 forward0.

단위 model_observation_step. τ는 고정 입력·상태 conductance 진단량이며 초·실제 영업일·경제적 기억길이·Jacobian 고유시간이 아니다. A/B BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. Origin/Seed/뉴런/중첩window는 독립 시장 표본이 아니다. O1~O4 Test와 후속 Validation의 역사적 중복 한계를 유지한다. 결과로 가격·모델·Seed·threshold·HMM을 선택하지 않는다. 금융 τ와 예측퇴화의 차이를 인과로 해석하지 않는다.

τ_raw는 positive(cm)/positive(gleak), τ_effective는 positive(cm)/(positive(gleak)+sensory합+recurrent합)이다. Positive는 실제 constraints=True의 Softplus를 정확1회 적용한다. cm_t는 적분용이며 τ 분모에 더하지 않는다. A observation-entry와 B 실제 substep0~5를 분리했다. A=step0 exact 일치,20×6개 callback/128뉴런/유한양수/hidden 연속성을 검증했다. 저장은 τ_effective·hidden_pre·recurrent_sum을 모든 substep에 보존하고 sensory합은 6단계 동일성을 검증해 관측당1회 보존한다. rawτ는128개/모델로 중복 제거한다. 복원 규칙과 source/config/identity/관측일/예측일/session/window/neuron/substep lineage는 private metadata에 있다.

관측 및 substep은 서로 다른 분석 수준이다. 아래는 checkpoint별 quantile을 먼저 구한 후 같은 후보 안에서 평균/표본SD를 구한 기술통계다. 전체 신경/날짜를 연결한 독립표본 추정이 아니다. mean/std와 범위는 공개 집계JSON에 있다.

tau_raw

| 구분 | 유효/전체 checkpoint | q05 평균 | q25 평균 | median 평균 ± 표본SD | q75 평균 | q95 평균 |
|---|---:|---:|---:|---:|---:|---:|
| A / ALL | 50/50 | 0.7345462 | 0.8527677 | 0.9951617 ± 0.031146 | 1.182741 | 1.423983 |
| B / ALL | 49/49 | 0.7386192 | 0.855287 | 0.9942639 ± 0.029491 | 1.174174 | 1.384436 |

observation_entry

| 구분 | 유효/전체 checkpoint | q05 평균 | q25 평균 | median 평균 ± 표본SD | q75 평균 | q95 평균 |
|---|---:|---:|---:|---:|---:|---:|
| A / ALL | 50/50 | 0.03656997 | 0.04101315 | 0.04490546 ± 0.016083 | 0.04967443 | 0.06289285 |
| B / ALL | 49/49 | 0.03665726 | 0.04075732 | 0.04425789 ± 0.01478 | 0.04836213 | 0.05953723 |

solver_substep

| 구분 | 유효/전체 checkpoint | q05 평균 | q25 평균 | median 평균 ± 표본SD | q75 평균 | q95 평균 |
|---|---:|---:|---:|---:|---:|---:|
| A / ALL | 50/50 | 0.0363837 | 0.04085504 | 0.0447126 ± 0.015897 | 0.04933233 | 0.05831733 |
| B / ALL | 49/49 | 0.0364666 | 0.04061354 | 0.04406809 ± 0.01461 | 0.04801514 | 0.05476727 |

확인일: 2026-11-20 KST. 근거: 동결 STEP7A 설치 ncps 1.0.1 소스SHA 및 이번 실제 read-only 실행 ledger/저장 확률·HMM 파일SHA. 공식 구현: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py . 설치소스 대조이며 과거 논문 환경이나 가격 원천의 소급 인증은 아니다.
