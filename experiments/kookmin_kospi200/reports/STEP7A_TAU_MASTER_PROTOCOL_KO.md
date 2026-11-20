# STEP7A TAU_MASTER_PROTOCOL

τ_raw=positive(cm)/positive(gleak). τ_effective=positive(cm)/(positive(gleak)+ΣG_sensory(x)+ΣG_recurrent(h)). wrapper implicit_param_constraints=True에 맞춰 Softplus를 정확히 한 번 적용한다. raw는 unconstrained 파라미터 비율이 아니다. reversal potential은 고정 상태 conductance 분모에 직접 들어가지 않지만 hidden 동역학에는 관여한다.

단위 model_observation_step. elapsed_time=1, ode_unfolds=6, cm_t=positive(cm)/(elapsed_time/6). cm_t와 epsilon은 τ 분모에 더하지 않는다. 초·벽시계·실제 KRX 경과일·경제적 기억길이·Jacobian 고유시간으로 해석하지 않는다.

후속 제안은 B 실제 substep을 한 번 계측하고 A observation-entry를 substep0에서 함께 얻는 방식이다. 모델별 원본 입력 batch를 정확히 한 번 forward한다. 100개 LTC(5Origin×A/B×10Seed)와 퇴화24개를 모두 유지한다. 사전 원본 Test/scaler/window/HMM 상태를 재사용한다. q05/q25/median/q75/q95를 모델별로 먼저 요약하고 Origin/Seed/가격/HMM Low·High/퇴화 여부별 탐색적 분포를 비교한다. HMM 상태는 예측 기준일에 연결한다. window 안의 관측일과 예측 기준일은 별도 키다. 뉴런·중첩 날짜·Seed는 독립 시장 표본이 아니다. 인과·성능 우수성·p값을 주장하지 않는다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
