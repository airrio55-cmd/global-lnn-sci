# STEP4A-1 실행 감사

사용자 승인 범위의 회고적·탐색적 CPU Train/Validation Pilot이다. A/B는 BOTH_UNVERIFIED이고 production-PIT는 BLOCKED다. 가격·모델·Seed·날짜·설정을 Validation 결과로 선택하지 않았다. 독립 Test2023 및 이후 가격 관측값, HMM fit, GPU, RAW5/외부피처/앙상블, τ 실측 forward, 확증 p값은 사용/실행하지 않았다. 2026년 관측 사용0이다. master production training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false는 변경하지 않았다.

독립 [승인](../provenance/step4a1_o3_authorization.json)은 이번 사용자 붙여넣은 요청의 SHA와 O3/Seeds2,12/A,B/5모델/20fit만 허용한다. master config와 원본을 수정하지 않았다. 전용 o3_pilot_execution_enabled=true와 독립 config/승인을 사용하고 production/new_fit_execution_enabled=false를 유지한다. STEP3C의460개 실행 승인으로 해석하지 않는다.

시작 2026-11-16T20:47:37.687511+09:00, 종료 2026-11-16T21:25:47.166648+09:00. 신규 완료20, 실패0, BLOCKED0, 중단미완료0. 동일 identity의 확정 epoch 재개 기록 0건, 비완료 identity 0건이다. 신규421epoch/19366optimizer steps, 기존40개 재학습0이다. 완료 identity는 재실행하지 않았다. 각 identity는 candidate/Origin/seed/model/config SHA로 추적한다.

## 실행 전 및 후 검사

| 검사 | 결과 |
| --- | --- |
| 실행 전 운영gate |12 PASS |
| 전용 사전 검사 |12 PASS / 0 FAIL |
| 사후 저장 결과 검사 |14 PASS / 0 FAIL |
| 이전 파일 663개 byte 보존 | PASS |
| 기존40개 출력160개 hash | PASS |
| 신규 최적 checkpoint 추가 감사 |20/20 PASS |
| Train/Validation cutoff 위반 |0 |
| 독립Test2023+ / 2026 / GPU / HMM / τ / p값 |모두0 |

원본 정의(cell6/8)·모델설정·seed offset·환경과 학습 kernel SHA를 사전 검증했다. kernel `676cff063a52141a62fef3f9cda96db582fb75a8a831f54b1a18d3aba91eff09`는 STEP3C와 바이트 동일하다. 전용 worker 전체 파일 SHA는 승인/메타데이터 범위가 달라 master worker와 다르며 이를 숨기지 않는다. Hidden128/Layer1/Dropout.2/Batch64/W20/H20/Max100/Pat10/AdamW.005/wd1e-4/OneCycle100/Focal2,.25/clip1/FP32/AMP OFF/threshold>.5를 유지했다. source/artifact hash는 config와 execution manifest에 있다.

## 자료 접근 차단

full source 파일은 provenance 바이트 SHA만 확인했고 수치 파싱은 KRX prefix3208행(2010-01-04~2022-12-29)에서 멈췄다. 다음2023행을 peek하지 않는다. 모델 worker는 해당 fit output과 이번 O3 input subtree만 허용하는 file barrier를 사용했다. 원본Notebook은 해시 검증된 정의 추출 목적으로만 읽고 전체 실행/저장 Test출력 사용을 하지 않았다. 2023년 이후 관측 가격·Test Target/확률/지표는 새로 읽거나 배열화하지 않았다. 비교 자료는 기존 O1/O2 Validation 집계/epoch history(최대2021)뿐이다.

## 자원과 복원

현재 cpu.max=`200000 100000`, memory.max=8589934592bytes를 새로 읽었다. STEP3B와 같은2core/8GiB이므로 worker≤2, LTC≤1, torch thread1을 사전 고정했다. 각 모델 subprocess를 CPU FP32·OMP/MKL/OpenBLAS1·PYTHONHASHSEED2로 실행했다. GPU로 이동하지 않았다. Torch/ncps/hmmlearn 버전 2.10.0+cpu/1.0.1/0.3.3를 보존했고 HMM은 fit하지 않았다.

checkpoint는 model/optimizer/scheduler/EarlyStopping, Python/NumPy/Torch CPU/DataLoader RNG, Origin/seed/가격/모델/config, data/scaler/feature/source/env SHA, epoch/batch_position0를 보존한다. epoch1에서 원래 학습 logits와 복원 logits/state/RNG를 정확히 비교하고 그 상태로 이어 학습했다. 최적 checkpoint는 두 독립 복원 및 전체 payload serialization roundtrip으로 logits 동일성을 검사했고, 저장된 완료 best 확률과도 정확히 일치시켰다. optimizer/scheduler는 restore만 하고 추가 step0이다. 원래 best epoch의 원시 logits 자체는 당시 파일에 저장하지 않았으므로 그 원시 tensor와의 직접 비교라고 주장하지 않는다. 대신 epoch1 원시 logits 비교, best probability 일치, 복원 logits 일치의 범위를 구분했다. 실제 오류면 FAILED_CHECKPOINT_VERIFICATION이며 PASS로 바꾸거나 다른Seed로 대체하지 않는다.

batch 중간 정확복구가 아니라 마지막 확정 epoch 경계에서만 재개한다. 실제 재개 여부는 위 건수와 각 record의 resume_from_committed_epoch에 있다. 검증용 checkpoint_roundtrip_private.pt도 ignored 로컬에만 보존하며 새 model fit은 아니다. 전체 신선한 재학습 반복은 예산상 실행하지 않았다.

- Master config SHA: `f4ea7a18d7812b00b8c581191a110f63a6799a22e066484ec251ee32f7912c5c`
- 전용 config SHA: `101f1ef711aa963f5eecc7d85b53fff0a5acf376d4799d1bbc942e5c2053d854`
- 전용 worker SHA: `00947e4d33be7d9b891ea18441fbfff0d37b648befa9bfae65614a354fd255ad`
- 환경 SHA: `a08a66d21e0347868e5d6b423cb755e55a5aab5a4af0f798730e38bd46490ee5`

각 fit의 checkpoint_lineage_hashes.json sidecar와 runs CSV에는 input/price/scaler/feature-order/config/source/environment SHA 및 best/latest checkpoint SHA를 연결했다. checkpoint 원래 바이트를 바꾸지 않고 검증 메타데이터를 별도 저장했다.

모든 체크포인트/가격/일별레이블/확률은 data/derived의 새 ignored 경로에 있다. 코드·집계·해시만 감사 브랜치에 게시하며 main/JOF V14/V15/원본/기존 결과는 수정하지 않는다.
