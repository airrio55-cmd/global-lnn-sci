# STEP4A-2 실행 감사

STEP3C 동결 사양에 따른 회고적·탐색적 CPU Train/Validation Pilot이다. A/B=BOTH_UNVERIFIED, 18:00 KST production-PIT=BLOCKED를 유지한다. Validation으로 가격·모델·Seed·사양을 고르지 않았다. O4의 독립 Test2024, O5의 독립 Test2025 예측/평가, 2026 관측, HMM fit, GPU, 외부피처/RAW5/앙상블, τ 실측, 확증 p값은 사용/실행하지 않았다. master training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false는 보존했다.

독립 [승인](../provenance/step4a2_o4_o5_authorization.json)은 현재 사용자의 O4/O5·Seeds2/12·A/B·5모델·최대40fit만 허용한다. 전용 config와 o4_o5_pilot_execution_enabled=true를 사용했고 master/global false flags는 바꾸지 않았다. 기존60개 재학습, Seed22~92, 추가400fit 및 Test를 승인한 것으로 해석하지 않는다.

시작 2026-11-16T21:53:27.991124+09:00, 종료 2026-11-17T00:27:30.392325+09:00. 신규 완료40, 실패0, BLOCKED0, 중단미완료0이다. 확정 epoch 경계 재개 0건, 비완료 identity 0건을 그대로 기록했다. 신규757epoch/38793optimizer updates, 기존60개 재학습0이다. identity는 candidate/Origin/Seed/model/master config SHA/pilot config SHA로 추적하며 완료·실패한 identity를 더 좋은 Seed로 대체하지 않는다.

## 검증 결과

| 검사 | 결과 |
| --- | --- |
| 사전 운영 gate |12 PASS |
| 사전 제어/자료 검사 |12 PASS / 0 FAIL |
| 사후 결과 검사 |14 PASS / 0 FAIL |
| 이전 파일 938개 byte 보존 | PASS |
| 기존60개 checkpoint/history/확률·입력배열/scaler/지표/source hash | PASS |
| 신규 checkpoint 추가 복원 감사 |40/40 PASS |
| Train/Validation label_end 경계 위반 |0 |
| Test / 2026 / GPU / HMM / τ실측 / 확증 p값 |모두0 |

원본 정의(cell6/8), environment pin, 고정 설정 및 학습 kernel `676cff063a52141a62fef3f9cda96db582fb75a8a831f54b1a18d3aba91eff09`를 사전 확인했다. STEP3C 학습 부분과 바이트 동일하며 전용 worker 전체 파일 SHA는 승인/메타데이터 범위가 달라 별도로 기록한다. Hidden128/Layer1/Dropout.2/B64/W20/H20/Max100/Pat10/AdamW.005/wd1e-4/OneCycle100/Focal2,.25/clip1/CPU FP32/AMP OFF/threshold>.5를 유지했다. Focal alpha는 원본의 전역 손실 배율이며 사후 불균형 보정으로 바꾸지 않았다. Validation BA strict 개선만 checkpoint 선택에 사용했고 동률이면 최초 최고를 유지했다.

## Origin별 접근 차단

각 worker는 자기 fit output과 자기 Origin 입력 subtree만 읽도록 file barrier를 적용했다. O4는 가격 수치 prefix2010~2023, O5는2010~2024만 파싱했다. 전체 원천의 바이트 SHA 확인과 관측값 수치 사용을 구분한다. O4 worker가 O5 배열(2024 포함)을 읽거나 O5 worker가 O4 디렉터리를 읽으려 하면 PermissionError라는 사전 검사를 통과했다. worker는 자신에게 허용된 경로·입력/날짜/meta SHA를 먼저 검증한다.

O4 독립 Test2024 입력/예측을 만들지 않았다. O5 Validation2024는 해당 Origin에서 사용자 승인된 검증 자료이며 O4 모델에 전달하지 않았다. O5 독립 Test2025와2026 가격은 수치 파싱·레이블·스케일러·checkpoint 선택에 사용하지 않았다. 이전 O1~O3 비교는 이미 보존된 Validation 지표/epoch history만 사용했다. 원본Notebook은 해시 검증된 정의만 추출하고 전체 실행/저장 Test출력 사용을 하지 않았다.

## 현재 자원·복원·재개

cpu.max=`200000 100000`, memory.max=8589934592bytes를 새로 읽었다. 확인시각 `2026-11-16T21:50:50.670978+09:00`. 기존2core/8GiB와 같아 worker≤2/LTC≤1/Torch thread1/OMP-MKL-OpenBLAS1/PYTHONHASHSEED2를 고정했다. 환경/자원이 바뀌면 멈추도록 했다. GPU로 전환하지 않았다. 라이브러리는 Torch2.10.0+cpu/ncps1.0.1/hmmlearn0.3.3이며 설치·버전 변경 없이 유지했다.

checkpoint에 model/optimizer/scheduler/EarlyStopping/Python·NumPy·Torch CPU·DataLoader RNG/epoch/batch_position0/Origin·Seed·가격·모델/scaler/feature order/data·source·config·environment hash를 보존한다. 첫epoch 경계에서 원래 학습 logits와 복원 logits/state/RNG 일치를 확인한 뒤 같은 상태로 이어 학습했다. 최적 checkpoint는 두 독립 복원 logits와 저장된 best 확률 일치를 검사하고 model/optimizer/scheduler/EarlyStopping/RNG payload를 직렬화·복원 비교했다. 감사 중 추가 optimizer update0이다. 최초 best epoch의 원시 logits 파일이 없으므로 그 원시 tensor와 직접 비교했다고 주장하지 않는다. epoch1 원시 logits 비교와 best 복원 logits/확률 비교 범위를 구분한다.

손상/복원실패는 FAILED_CHECKPOINT_VERIFICATION으로 남기며 PASS로 바꾸지 않는다. 중단은 마지막 확정 epoch 경계에서만 같은 identity로 재개한다. batch중간 정확복구나 전체 새 재학습 반복을 검증했다고 주장하지 않는다. 실제 재개는 위 건수 및 record.resume_from_committed_epoch에 있다. best/latest/검증용 roundtrip checkpoint는 모두 새 ignored 경로에 보존한다.

- Master SHA `f4ea7a18d7812b00b8c581191a110f63a6799a22e066484ec251ee32f7912c5c`
- Pilot config SHA `b4d6c9e40971847354e4fd6c171cf261cdea0a7a61ae1e1ecff2e3c7b8178458`
- Worker SHA `cdbe5acc228ed1ed46f469ac68796cc0a3c8b77f1ecda3c26c7d1c2ed2f96313`
- Environment SHA `a08a66d21e0347868e5d6b423cb755e55a5aab5a4af0f798730e38bd46490ee5`

[runs](../manifests/step4a2_runs.csv)와 checkpoint_lineage_hashes.json sidecar에 master/pilot config·input/price/scaler/feature order/source/environment/best/latest hash를 연결했다. 원본 및 기존60개 checkpoint byte는 수정하지 않았다. raw가격·일별Target·확률·weights는 공개하지 않고 코드·집계·해시만 감사 브랜치에 저장한다. 상세 preflight manifest는 비공개 경로와 scaler 통계 때문에 자동 승인 검토에서 업로드가 거절돼 로컬에만 보존했다. 공개본은 preflight_public/실행 summary/preservation_public으로 줄였으며 CSV에서도 private directory를 제외했다. main/JOF V14/V15 및 기존 보고서/논문 성능표는 보존한다.
