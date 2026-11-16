# STEP 3B 실행·무결성 감사

회고적·탐색적 CPU Train/Validation 구현 진단이다. Validation은 조기 종료와 checkpoint 선택에 사용됐으므로 독립 일반화 성능이 아니다. A/B는 BOTH_UNVERIFIED, production-PIT는 BLOCKED이며 가격·모델·Seed를 선택하지 않았다. 독립 Test 평가, HMM fit, GPU, 전체 5Origin×10Seed, Ablation은 실행하지 않았다. production training_enabled=false, hmm_fit_enabled=false를 유지한다.

## 승인 및 실행 예산

독립 승인 [authorization](../provenance/step3b_pilot_authorization.json), [고정 config](../configs/step3b_pilot_config.json), [사전 manifest](../manifests/step3b_preflight.json)를 실행 전에 확정했다. pilot_execution_enabled=true는 이번 30개 CPU fit에만 적용된다. 기존 production flag는 false다. 기존 O1/Seed2는 새 job 목록에서 금지하고 고유 identity 예약·프로세스 lock·manager lock으로 중복 실행을 막는다. 완료/실패 identity는 재시작해도 대체하거나 재학습하지 않는다.

시작 2026-11-16T17:06:02.004247+09:00, 종료 2026-11-16T18:13:22.859986+09:00. 신규 완료 30, 실패 0, BLOCKED 0, 미완료 0. 신규 601epoch/24350optimizer updates, 기존 STEP3A 240epoch/9,120updates는 재실행하지 않았다. 최대100epoch·patience10·strict Validation BA만 checkpoint 선택에 사용했다. 동률은 개선이 아니며 10회 지속 시 종료한다.

CPU quota2core/메모리8GiB 증거에 따라 실행 전에 동시 worker≤2, LTC≤1, Torch thread1로 고정했다. LTC 직렬화는 메모리 예산을 위한 사전 실행정책이며 성능을 보고 바꾸지 않았다. 원본 모델 정의 및 FocalLoss SHA-256 검증 후 해당 정의만 실행하고 전체 Notebook은 실행하지 않았다.

## 검증 결과

| 검사 | 판정/수치 |
| --- | --- |
| 실행 전 운영 gate | 12 PASS |
| STEP3B preflight 단위 검사 | 12 PASS / 0 FAIL |
| 저장된 결과·checkpoint·집계 검사 | 16 PASS / 0 FAIL |
| 기존 파일 270개 점검(README/CHANGELOG 추가 설명 제외) | PASS |
| 기존 완료10개 관련 47개 해시 대조 | PASS |
| 신규 최적 checkpoint 복원·동일 logits | 30/30 PASS |
| epoch1 재개 roundtrip·RNG 복원 | 30/30 PASS |
| Train/Validation label_end 위반 | 0 |
| 독립 Test / HMM fit / GPU / 2026 사용 | 모두 0 |
| production-PIT·가격 원천 인증 | BLOCKED / BOTH_UNVERIFIED |

기존 테스트를 무조건 실행하면 현재 금지된 독립 Test 입력을 읽을 수 있어 전체 과거 테스트를 재실행하지 않았다. 이번 승인 범위의 Origin-specific preflight 및 저장 결과 테스트로 회귀를 확인했다. 3939세션 달력 검증은 전체 가격 입력을 뜻하지 않는다. 각 worker는 자기 Origin staging과 자기 output만 읽도록 파일 접근 barrier를 적용했고 금지 접근 시도는 0건이다. 가격 파일은 필요한 prefix 행만 소비하고 이후 행을 next/peek하지 않는다. O2 Validation2021을 O1 worker가 읽는 것도 금지한다.

## 고정 설정 및 재현성의 범위

2피처 원본 구조의 기대 trainable parameter 수는 RNN17,154 / LSTM67,842 / GRU50,946 / LTC67,462 / CfC83,074다. 각 생성 시 실제 수와 대조하며 LTC는 implicit_param_constraints=True도 검사한다. 고정 비학습 파라미터를 trainable 수에 합산하지 않는다.

Hidden128/Layer1/Dropout0.2/Batch64/Window20/Horizon20/MaxEpoch100/Patience10, AdamW lr0.005 wd0.0001, OneCycleLR(계획100epoch), Focal gamma2 alpha0.25, gradient clip1, CPU FP32 AMP OFF, 확률>0.5를 유지했다. Focal alpha는 원본의 전역 배율이며 클래스 가중치로 새로 해석하지 않는다. F1은 2피처 호환성 사양으로 원본 RAW5피처 성능과 동일 실험이라고 주장하지 않는다.

Checkpoint는 model/optimizer/scheduler/early-stopping, Python/NumPy/Torch CPU/DataLoader RNG, epoch/batch_position, Origin/Seed/모델/가격 후보, feature 순서, scaler, 데이터·코드·환경 hash를 포함한다. 매 fit의 epoch1에서 저장·복원 후 logits/state/RNG 일치를 확인하고 복원 상태로 이어 학습했다. 종료 후 best checkpoint를 다시 읽어 logits/선택 지표를 확인했다. checkpoint는 epoch 경계 batch_position=0이며 중단 epoch는 마지막 확정 경계에서 같은 identity로 재개한다. batch 중간부터 정확히 재개한다고 주장하지 않는다. 완료 fit 전체를 새로 반복하지 않았으므로 전체 재학습 반복 일치를 새로 검증했다고 주장하지 않는다.

환경은 2.10.0+cpu(CPU)/ncps1.0.1/hmmlearn0.3.3, Python3.12.14, FP32다. hmmlearn은 버전 확인만 했고 fit하지 않았다. 구체적인 환경·소스·데이터·최적/최종 checkpoint hash는 실행 manifest와 runs CSV에 있다. 전체 후보 파일은 출처 무결성 확인을 위한 바이트 해시만 대조했고, 모델 입력·레이블·scaler 계산에 쓰는 가격 수치 파싱은 각 Origin의 Validation 종료 이전 prefix로 제한했다.

- Config SHA-256: `9a5a5f95c98d188c79ac197590052673ea627db0d70958455b0a1eee3c8bacdc`
- Worker SHA-256: `cc57070603b2e830097ded3edc36cb10302493a381b86bbbdceaeb4ce2d200c3`
- Manager SHA-256: `bae3b4c2b7c799c8720b305afb164db3788f21d5e3d74661f315847a6647c480`
- 환경 SHA-256: `a08a66d21e0347868e5d6b423cb755e55a5aab5a4af0f798730e38bd46490ee5`

## 보존 및 공개 범위

원본 Notebook·CSV·논문 성능표·완료된 checkpoint·기존 STEP1~3A 구현/보고서는 보존했다. 새 코드·집계·검증 hash만 감사 브랜치에 게시한다. `data/`의 가격/일별 Target/Validation 확률/checkpoint는 ignored 로컬에 남긴다. main/JOF V14/V15는 변경하지 않는다. 상세 보존 증거는 [preservation](../provenance/step3b_preservation.json), 전체 검사 집계는 [verification](../manifests/step3b_verification_summary.json)다.
