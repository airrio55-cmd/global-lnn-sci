# STEP3C 수동/HMM 레짐과 LTC τ 계획

이번 단계는 사양·데이터 준비와 소스 정적 검사만 수행했다. 신규 모델 fit·모델 생성/forward·checkpoint load·HMM fit·독립 Test 예측/성능 평가·GPU 실행은 모두0건이다. production training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지한다. 기존40개와 원본·논문 결과·JOF V14/V15·main을 보존한다.

## 수동 레짐

Vol_Regime=Log_Ret.rolling(40).std(ddof=1). 각 Origin/가격의 purging 후 유지된 Train 기준일에서 q30/q70(linear)를 구해 고정한다. Low≤q30, High≥q70, 나머지Mid다. Validation/Test 분위수 재계산·수동 임계값 조정은 금지다. 이미 준비된10개 Train reference는 prepared_inputs metadata.manual_reference에 있다. 신경망 입력에는 Vol_Regime을 넣지 않는다.

동일 checkpoint의 예측값을 레짐별로 분리해 BA/MacroF1/Recall0/Recall1/n/n0/n1 및 Seed별 값·평균·표본표준편차(ddof1)를 보고한다. 빈 레짐 또는 한 실제 클래스 레짐은 BA/MacroF1=null; Recall은 해당 실제 클래스 support가0일 때만null이다. 단일 예측 클래스지만 실제 두 클래스이면 BA/MacroF1 계산과 DEGENERATE_PREDICTION을 함께 기록한다. Seed를 연결해 n을 증가시키지 않는다. 레짐 결과로 모델/경계/임계값을 선택하지 않는다.

## HMM 별도 승인 계획

2-state GaussianHMM, full covariance, n_iter2000,tol1e-4,min_covar1e-4. observation=[Vol_Regime], 각 Origin/가격의 유지된 Train 기준일로만 scaler와 HMM을 fit한다. 초기화 후보[2,12,22,32,42,52,62,72,82,92]는 모든 Origin에서 같고 신경망Seed와 별개다. finite likelihood·수렴·positive covariance·Train forward-filter hard state 두 개 존재를 적격 기준으로 한다. 부적격 원인/점유율을 남기며 후보를 추가하지 않는다. 적격 후보 중 Train log likelihood 최대, 동률이면 작은 초기화Seed를 선택한다. Train 원단위 Vol_Regime mean 오름차순으로 Low/High 상태명을 고정한다. 신경망Seed마다 HMM을 다시 fit하지 않는다.

A/B×5Origin×10초기화=100 HMM candidate fit, 최종선택10개이며 신경망500fit와 별도다. 전체 실패/Train 상태붕괴는 HMM BLOCKED다. Test median이나 수동 레짐으로 대체하지 않는다. Test에 한 상태만 나타나도 상태를 조작하거나 재학습하지 않고 그 분포를 보고한다.

Validation/Test는 p(z_t|x≤t)의 순차 forward filtering만 사용한다. Train말단부터 검증/테스트 사이의 purge된 bridge 날짜도 관측 가능 이력 순서대로 posterior를 전파해 시간 전이를 생략하지 않는다. 전체 Viterbi/smoothing을 실시간 상태로 사용하지 않는다. 수동/HMM은 동일 신경망 예측확률·같은 label의 별도 표이며 한쪽 레짐이 유리하다는 이유로 선택하지 않는다. 현재 regimes.forward_filter/paired_regime_evaluation 인터페이스를 보존했고 실제 HMM fit/filtering 실자료 실행은 하지 않았다.

## LTC τ 정의·출처·인터페이스

참조는 [ncps1.0.1 PyPI](https://pypi.org/project/ncps/1.0.1/)와 [고정 공식 LTCCell 소스](https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py). 확인일2026-11-16, 기존 STEP2.5 소스/배포물 비교·STEP2.9 실행 호환성 증거를 재사용했다. 현재 installed cell SHA=`167a9d6e1f4dc653ce21420010709e1c995716e53ad0d8bbc2d53c19c40b123f`, wrapper SHA=`bbf3127013d3969994ecf0debf4eb37b56db750475ee71646a9decdf1aaf3026`이며 재대조한다. 원본 논문의 과거 ncps 버전까지 확정된 것은 아니다.

cm=capacitance, gleak=leak conductance. 원시 비율 τ_raw=positive(cm)/positive(gleak). 여기서 raw는 저장된 unconstrained parameter 자체가 아니라 상태와 입력 conductance를 제외한 비율이다. τ_effective=positive(cm)/(positive(gleak)+Σsensory_conductance(x)+Σrecurrent_conductance(h)). affine input mapping·sigmoid gate·sparsity mask와 implicit_param_constraints=True의 Softplus를 정확히 한 번 적용한다. 셀 직접생성 defaultFalse와 wrapperTrue를 혼동하지 않는다. 이 값은 고정된 입력/상태의 conductance 시간상수이며 전체 비선형 Jacobian 고유시간이나 경제적 기억길이를 뜻하지 않는다.

timespans 생략 시 elapsed_time=1.0, ode_unfolds=6, solver 내부 cm_t=cm/(elapsed_time/6). effective τ 분모에 수치 적분용 cm_t를 다시 더하지 않는다. 원본은 실제 경과 시간을 주지 않은 일별 관측 step이므로 단위는 model_observation_step으로 기록하고 초/정확한 KRX영업일 물리 단위를 인증하지 않는다. 주말·휴장일의 벽시계 시간 차이를 dt=1이 설명한다는 주장도 금지한다.

master_tau.supplied_tau_snapshot은 미래 호출자가 제공한 inputs/hidden/params와 checkpoint SHA·Origin/Seed/가격/date/time_index/solver_substep/elapsed_time/constraint/source hash를 요구한다. 모델·torch import/forward·checkpoint load를 수행하지 않는다. τ 계산은 기존 tau.time_constants에 위임한다. 일반 forward hook은 interval 입구 상태만 관측하므로6개 solver substep의 모든 h를 얻었다고 주장할 수 없다. 실제 substep τ가 필요하면 별도 승인된 비침습 instrumentation과 source 동등성 검증을 먼저 준비한다.

향후 동일 checkpoint에서 날짜별/뉴런별 snapshot을 얻어 레짐별 q05/q25/median/q75/q95·Seed/Origin 안정성·예측 지표와 탐색적 연관을 보고한다. 중복된 날짜/뉴런/Seed를 독립 관측으로 취급하지 않고 인과·확증 p값을 만들지 않는다. τ를 보고 checkpoint/모델/레짐을 다시 고르지 않는다. 실제 forward 기반 τ 추출은 이번0건이며 별도 승인 전 BLOCKED다.
