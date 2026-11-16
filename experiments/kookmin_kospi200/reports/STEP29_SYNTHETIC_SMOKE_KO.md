# STEP2.9 독립 합성 CPU Smoke 결과

확인일: 2026-11-16 (Asia/Seoul). 기준 commit: `d3341177c7032b09e9609fba3ad299785f52c43a`.

**다섯 모델 모두 PASS.** 이번 실행은 사용자가 별도로 승인한 합성 CPU 구조 호환성 점검이다. 실제 금융 데이터 모델 학습·실제 Test 추론·전체 Notebook 실행·HMM fit·GPU·전체 Rolling-Origin·Ablation은 실행하지 않았다. production의 training_enabled=false, hmm_fit_enabled=false와 기존 gate는 그대로다.

## 독립 실행 모드와 승인

`configs/step29_synthetic_smoke_config.json`은 execution_mode=STEP29_SYNTHETIC_CPU_ONLY, synthetic_execution_enabled=true와 production 학습 플래그 false를 함께 명시한다. `provenance/step29_synthetic_authorization.json`은 이번 사용자 지시를 근거로 config·runner SHA-256에 연결한 독립 승인 기록이다. 실자료용 STEP3 승인으로 사용할 수 없으며 가격 A/B 선택도 승인하지 않는다.

새 실행기는 가격/거래일/Test 파일 인자를 받지 않는다. 합성 프로세스의 파일 접근 barrier는 기존 data/ 영역과 attachments, 원본 CSV 접근을 거부하고, 해시가 지정된 원본 Notebook의 모델 소스만 예외로 읽는다. 실제 금융 데이터 접근 시도0건·허용0건, 모델 소스 Notebook 읽기1건이었다. 원본 JSON의 출력이나 학습 셀은 실행하지 않았다. 기존90개 데이터 전용 회귀검사는 별도 프로세스에서 수행했으며 그 자료를 모델 입력으로 연결하지 않았다.

## 합성 입력

고정 생성 seed2, NumPy default_rng의 독립 표준정규 난수를 이용해 Train/Validation 입력을 따로 생성했다. 각 입력은(64,20,2), float32이며 타깃은(64,), int64, 클래스0/1 각각32개다. 입력·타깃 유한성 PASS이고 Train/Validation 입력 해시는 서로 다르다. 같은 두 합성 batch를 모든 모델과 두 반복에서 재사용했다. 실제 Log_Ret/Disparity의 분포나 주가·시장 성능을 모사하지 않는다.

모델 seed는 base2+동결된 아키텍처 offset이다. 이는 시드 재사용 규칙이며 이번 검사를 RAW/LOG 실험으로 부르는 것은 아니다. 모델별 한 개의 2피처 구조 사례만 실행했다.

| 모델 | 유효 seed | trainable | 전체 등록 parameter | Forward | Backward | checkpoint 복원 | 동일 seed 반복 | 검사 |
|---|---|---|---|---|---|---|---|---|
| RNN | 103 | 17154 | 17154 | PASS | PASS | PASS | PASS | 14/14 PASS |
| LSTM | 203 | 67842 | 67842 | PASS | PASS | PASS | PASS | 14/14 PASS |
| GRU | 303 | 50946 | 50946 | PASS | PASS | PASS | PASS | 14/14 PASS |
| LTC | 403 | 67462 | 84102 | PASS | PASS | PASS | PASS | 14/14 PASS |
| CfC | 503 | 83074 | 83074 | PASS | PASS | PASS | PASS | 14/14 PASS |


모든 학습 forward 출력은(64,2), float32, CPU였다. loss·모든 trainable tensor의 gradient가 유한했고 gradient clipping1.0 적용 후 norm도 한도 안이었다. AdamW lr0.005/weight_decay1e-4, Focal gamma2/alpha0.25, hidden128/layer1/dropout0.2, batch64/window20, FP32/AMP-off를 그대로 사용했다. 원본 Focal alpha는 모든 표본에 공통 곱하는 값이며 class별 alpha_t 보정으로 해석하지 않았다.

각 모델은 반복당 합성 Train batch1개·Validation batch1개·optimizer update1회만 실행했다. 모델당2회 반복, **총 optimizer update10회**다. OneCycleLR은 원본의100epoch 설정과 한-batch loader를 조합한 계획(total_steps100)에서 step1회만 호출했다. epoch 학습 루프는 실행하지 않았다.

checkpoint는 매 반복마다 저장·weights_only/CPU로 복원했다. 새 모델에 model/optimizer/scheduler를 복원하고 **같은 Validation batch**를 다시 넣어 logits가 bitwise 동일함을 확인했다. 이 재생은 새 batch나 추가 optimizer update가 아니다. 같은 seed·입력·환경의2회 실행에서 학습 후 state, Train/Validation logits, 합성 loss가 정확히 같았다. 허용오차 완화·모델 단순화·설정 변경으로 검사를 통과시키지 않았다. 발견된 모델 오류는0건이다.

## 원본 정의의 정확한 재사용

실제 Notebook의1-based 셀번호와 셀 내부 행이다. 전체 Notebook SHA-256은 `b9e8542fc5783bc5dc734ddfd7bdfe69db26d4b540cde93ae3a722596485c1e7`다. 아래의 해시가 맞는 정의만 compile/exec했고, 원본 train_model·HMM·데이터 생성·결과 출력 코드는 실행하지 않았다.

| 정의 | 실제 셀 | 셀 내부 행 | 정의 SHA-256 |
|---|---|---|---|
| FocalLoss | 6 | 6~16 | 99f31d22f4549d6b370b5a7ede5e2606830b7b20dd66f834fd6e3b3eb2174b7d |
| init_weights | 8 | 5~9 | 721f2894a7a6f3dc3518f3e80bd17dd7a04ab08f9cdd47762de6212d7e674697 |
| RecurrentModel | 8 | 11~34 | 00844fd26fe3794dff89218879151544efe4b34cb07df9bd038f45e1dceec621 |
| LNNModel | 8 | 36~48 | ff2ec3b49fb1a96848b9a51aec6dbf4abfac5efdb02fa8fa10f48da77a7e0a7b |
| CfCModel | 8 | 50~62 | 2907b0ff7cc2dd6da70b9f9da189004de8f5e2d1fd8f2a06d14aeb26f438ebef |


LTC wrapper의 원본 호출은 제약 keyword를 생략한다. ncps1.0.1 wrapper 기본값은 implicit_param_constraints=True이고 실제 생성 cell에서도True·Softplus·solver6 substeps를 확인했다. 직접 LTCCell의 기본False와 구분했다. LTC의 고정 등록 mask16640개는 trainable67462개와 별도로 계산했다. 이것은 실제 금융 데이터의 τ 분포나 물리적 단위 검증이 아니다.

## 산출물과 검사 해석

합성 실행 판정은5모델×14항목=**70 PASS /0 FAIL /0 BLOCKED**다. 각 항목은 두 반복의 기록을 함께 확인하며 상세는 step29_smoke_results.json에 있다. 원본 코드 호환성은 해당 소스·버전·CPU·2피처·한 batch 범위의 실제 관측 결과다. RAW5피처는 정적 parameter count만 기록하고 실행하지 않았다.

로컬 출력: `data/derived/step29_synthetic_20261116T145248_KST/`. checkpoint10개, synthetic_batches.npz 및 로컬 로그/JSON은 ignored 영역에만 저장한다. GitHub에는 코드·해시·구조 검사 요약만 게시한다. 합성 loss 수치는 진단 로그이며 실증 BA/F1·예측 성능·모델 우열로 해석하지 않는다.

이번 승인 budget10회는 소비 완료로 기록했다. CLI는 같은 승인 기록의 재사용을 거부한다. 추가 실행에는 새 사용자 승인이 필요하다. 기존 production gate나 승인 파일을 바꾸어 우회하지 않았다.
