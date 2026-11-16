# STEP2.7 실행 준비도

확인일2026-11-16. **STEP3 모델/HMM Smoke Test 실행은 BLOCKED**다. 이번 단계에서 모델 생성·forward·checkpoint 로드·학습·HMM fit·GPU 질의/실험은0회다. training_enabled=false, hmm_fit_enabled=false, gpu_enabled=false를 유지한다.

## 패키지 설치와 환경 검증의 구분

사용자의 추가 설치 요청에 따라 /workspace/venvs/kookmin-step27 별도 venv에 torch2.10.0+cpu, ncps1.0.1, hmmlearn0.3.3을 설치했다. 수치 의존성은 기존 환경을 공유한다(system-site-packages). 패키지 import·정확한 버전·LTC 소스 SHA-256·constructor signature 검사 PASS. CUDA build=None인 CPU 배포판이며 GPU 조회는 하지 않았다. 설치가 모델 실행 승인을 뜻하지 않는다.

Torch 버전은 원본 저장 출력과 같지만 ncps/hmmlearn은 재현 후보 버전이다. 원본 ncps/hmmlearn lock, 실제 모델 행동, 수치 결정성 및 checkpoint 호환성은 미확인이다. 따라서 model_environment gate는 BLOCKED를 유지한다. requirements-step27.txt는 이번 설치/참조 의존성 핀이고 원본 환경 복원 완료 인증이 아니다. 설치 URL·확인일·버전·소스 해시는 provenance/step27_isolated_environment.json에 기록했다. 공식 PyTorch CPU index와 PyPI를 사용했고 패키지 설치로 원본·기존 lock은 변경하지 않았다.

## 원본 구조·학습 설정

원본 실제 셀8의 RecurrentModel, LNNModel, CfCModel과 셀6 FocalLoss·셀12 학습 함수 정의를 AST로 **문자열만 추출**해 로컬에 보존했다. 실행하지 않았으며 모델 정의는 새로 바꾸지 않았다. 해시·셀·행은 provenance/step27_notebook_source_references.json에 있다. 원본 train_model은 test tensor를 받아 마지막에 forward하므로 향후 신규 승인 runner에서 Train/Validation 선택과 최종 Test 접근을 분리해야 한다. 이번 Smoke 계획에는 Test 접근이 없다.

Hidden128/layer1/dropout0.2/window20/horizon20/batch64/maxepochs100/patience10, 검증BA 최대화, AdamW lr0.005/wd1e-4, OneCycleLR, Focal gamma2/alpha0.25, clip1, FP32/AMP-off/threshold0.5 및 seed목록·offset·feature순서를 기존 config 그대로 유지했다. 원본 비교식은 확률>0.5다. Focal alpha는 원본처럼 모든 표본에 공통 곱하는 값이며 클래스별 alpha_t 보정으로 해석하지 않는다. RNN계열 내부 dropout은 layer1이면0이고 마지막 출력 dropout0.2가 적용된다. LTC/CfC에도 마지막 출력 dropout이 적용된다.

| 모델 | F0 RAW(5) trainable | LOG/F1(2) trainable | RAW 고정등록 | LOG 고정등록 |
|---|---|---|---|---|
| RNN | 17538 | 17154 | 0 | 0 |
| LSTM | 69378 | 67842 | 0 | 0 |
| GRU | 52098 | 50946 | 0 | 0 |
| LTC | 69004 | 67462 | 17024 | 16640 |
| CfC | 83458 | 83074 | 0 | 0 |


이는 모델 생성 없이 계산한 정적 수다. RNN계열은 gate수 g=1/4/3에 대해 g(h·i+h²+2h)+2h+2다. LTC는 ncps1.0.1 dense/affine 기준4h²+4ih+7h+2i+2이며 고정 mask h²+ih를 별도로 보고했다. CfC는 참조 default/backbone128·1layer·mixed_memory=False 기준5h²+hi+7h+2다(h=128). LTC/CfC 총 등록 parameter 수는 trainable+고정등록이며 런타임 검증은 하지 않았다. 같은 hidden size가 같은 용량을 뜻하지 않는다.

LTC wrapper implicit_param_constraints=True, 직접 LTCCell 기본False를 구분한다. τ_raw=positive(cm)/positive(gleak), τ_effective=positive(cm)/(positive(gleak)+Σg_recurrent(hidden)+Σg_sensory(mapped_input)). wrapper 제약True일 때 positive=softplus다. 기본 solver6 substeps, timespans 생략 dt=1은 수치 step이며 검증 없이 물리적 ‘하루’로 인증하지 않는다. frozen-state conductance τ와 비선형 Jacobian 고유시간은 구분한다. 실제 τ forward/추출은 실행하지 않았다.

## 고정 Smoke 준비물

configs/step27_smoke_config.json은 O1/F1/seed2·5모델×RAW/LOG, 동일 hyperparameter·feature order·offset·Test접근false·실행false를 고정한다. 향후 smoke의1trainbatch+1validationbatch 한도는 구현 점검용이고 성능 실험이 아니다. src/kospi200/smoke_preparation.py는 정의 추출·정적 count·차단된 계획만 반환하며 학습 진입점은 제공하지 않는다. 필수 gate 누락도 차단한다. 명시적 STEP3 승인이 없는 현재 실행되지 않는다.

실험 config·원래 PROTOCOL·수동레짐 코드·Smoke config 해시는 step27_protocol_freeze.json에 동결했다. 이는 사양 snapshot이며 데이터 확정이나 실행 허가가 아니다. 원본 protocol 파일은 바꾸지 않고 새 규칙을 별도 버전으로 기록했다. 향후 GPU는 별도 명시적 승인과 모든 필수 gate PASS, 고정 Torch/CUDA/ncps·device 정보, AMP-off·결정성·프로세스 시작 전 CUBLAS 설정을 갖춰야 한다. 이번 CPU 설치로 GPU 준비를 인증하지 않는다.
