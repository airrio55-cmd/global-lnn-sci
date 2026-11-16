# STEP3C 전체 실행 계획과 예산

이번 단계는 사양·데이터 준비와 소스 정적 검사만 수행했다. 신규 모델 fit·모델 생성/forward·checkpoint load·HMM fit·독립 Test 예측/성능 평가·GPU 실행은 모두0건이다. production training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지한다. 기존40개와 원본·논문 결과·JOF V14/V15·main을 보존한다.

## 예산 정의

| scenario | planned_total_fits | confirmed_reusable_fits | planned_new_fits | basis | execution_authorized |
| --- | --- | --- | --- | --- | --- |
| F1_A | 250 | 20 | 230 | one price, one F1 stream | False |
| F1_B | 250 | 20 | 230 | one price, one F1 stream | False |
| F1_AB | 500 | 40 | 460 | domestic baseline, current exact scope | False |
| FULL_RAW_LOG_ONE_PRICE | 500 | 0 | 500 | legacy500 definition: two channels and one price | False |
| FULL_RAW_LOG_AB | 1000 | 0 | 1000 | additional to F1, LOG offset mismatch prevents automatic reuse | False |
| LTC_RAW_LOG_AB_SUBSET | 200 | 0 | 200 | subset of1000; do not add twice | False |
| ENSEMBLE_PROBABILITY_COMBINATION | 0 | 0 | 0 | no neural fit | False |
| ABLATION6_TWO_CHANNELS_ONE_PRICE_NAIVE | 3000 | 0 | 3000 | legacy3000, no dedup | False |
| ABLATION6_TWO_CHANNELS_AB_NAIVE | 6000 | 0 | 6000 | includes FULL F0, no dedup | False |
| ABLATION_AB_INCREMENT_OVER_FULL_NAIVE | 5000 | 0 | 5000 | 6000minus1000 | False |
| ABLATION_AB_LOG_DEDUP_CONDITIONAL | 3500 | 0 | 3500 | only if exact common dates/scaler/arrays/seed/source match; reuse unconfirmed | False |
| ABLATION_AB_INCREMENT_OVER_FULL_DEDUP_CONDITIONAL | 2500 | 0 | 2500 | 3500minus1000 if identity verified | False |


국내 F1은 한 개2피처 스트림이다. 전체500=A/B두후보×5Origin×10Seed×5모델, 신규460이다. 기존 원본의500은 **한 가격×5Origin×10Seed×5모델×RAW/LOG두채널**로 정의가 다르다. 기존3000은 같은 한 가격의6개 ablation까지 포함한 재사용 없는 상한이다. 현재 F1의500을 원본5피처 실험이나3000 실험 완료로 표현하지 않는다.

FULL_RAW_LOG_AB1000은 F1과 별도 사양이며 현재 기존40개를 자동 차감하지 않았다. LTC RAW/LOG만의200은 그1000 안의 부분집합이다. 앙상블 확률 결합의 추가 신경망 fit는0이다. HMM 후보 fit100회는 별도 예산으로 신경망500에 합산하지 않는다.

Ablation F0~F5: RAW는 기존 [specs.py](../src/kospi200/specs.py)의 순서, LOG는 항상[Log_Ret,Disparity].6×5Origin×10Seed×5모델×2채널=3000/가격, A/B6000이며 F0 전체1000을 포함한다. F0 대비 추가5000은 재사용 없는 상한이다. 모든6사양의 공통 날짜·동일scaler·seed/offset·배열·환경이 확인되면 같은 LOG 모델을 사양 간 공유할 수 있어 A/B3500(기존F0 대비 추가2500)까지 줄일 수 있다. 이는 조건부 계산이며 외부 PIT 공통 날짜가 미확정이므로 현재 재사용 확정0이다. F1 RAW도 현재 기본실험과 같은 identity일 때에만 추가 차감하며, 이를 확인하기 전 예산 절감을 주장하지 않는다. 예산 표의 시나리오는 서로 더하는 목록이 아니다.

## Origin별 데이터·경계

| origin | candidate | partition | boundary_start | boundary_end | first_sample | last_sample | min_label_end | max_label_end | samples | class0 | class1 | train_purged | unknown_excluded | metadata_basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | A | train | 2010-01-04 | 2019-12-30 | 2010-03-30 | 2019-11-29 | 2010-04-27 | 2019-12-30 | 2387 | 1071 | 1316 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O1 | A | validation | 2020-01-02 | 2020-12-30 | 2020-01-02 | 2020-12-01 | 2020-02-03 | 2020-12-30 | 228 | 70 | 158 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O1 | B | train | 2010-01-04 | 2019-12-30 | 2010-03-30 | 2019-11-29 | 2010-04-27 | 2019-12-30 | 2387 | 1071 | 1316 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O1 | B | validation | 2020-01-02 | 2020-12-30 | 2020-01-02 | 2020-12-01 | 2020-02-03 | 2020-12-30 | 228 | 70 | 158 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O2 | A | train | 2010-01-04 | 2020-12-30 | 2010-03-30 | 2020-12-01 | 2010-04-27 | 2020-12-30 | 2635 | 1145 | 1490 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O2 | A | validation | 2021-01-04 | 2021-12-30 | 2021-01-04 | 2021-12-02 | 2021-02-01 | 2021-12-30 | 228 | 131 | 97 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O2 | B | train | 2010-01-04 | 2020-12-30 | 2010-03-30 | 2020-12-01 | 2010-04-27 | 2020-12-30 | 2635 | 1145 | 1490 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O2 | B | validation | 2021-01-04 | 2021-12-30 | 2021-01-04 | 2021-12-02 | 2021-02-01 | 2021-12-30 | 228 | 131 | 97 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O3 | A | train | 2010-01-04 | 2021-12-30 | 2010-03-30 | 2021-12-02 | 2010-04-27 | 2021-12-30 | 2883 | 1276 | 1607 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O3 | A | validation | 2022-01-03 | 2022-12-29 | 2022-01-03 | 2022-12-01 | 2022-02-03 | 2022-12-29 | 226 | 149 | 77 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O3 | B | train | 2010-01-04 | 2021-12-30 | 2010-03-30 | 2021-12-02 | 2010-04-27 | 2021-12-30 | 2883 | 1276 | 1607 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O3 | B | validation | 2022-01-03 | 2022-12-29 | 2022-01-03 | 2022-12-01 | 2022-02-03 | 2022-12-29 | 226 | 149 | 77 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O4 | A | train | 2010-01-04 | 2022-12-29 | 2010-03-30 | 2022-12-01 | 2010-04-27 | 2022-12-29 | 3129 | 1443 | 1686 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O4 | A | validation | 2023-01-02 | 2023-12-28 | 2023-01-02 | 2023-11-29 | 2023-02-01 | 2023-12-28 | 225 | 93 | 132 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O4 | B | train | 2010-01-04 | 2022-12-29 | 2010-03-30 | 2022-12-01 | 2010-04-27 | 2022-12-29 | 3129 | 1443 | 1686 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O4 | B | validation | 2023-01-02 | 2023-12-28 | 2023-01-02 | 2023-11-29 | 2023-02-01 | 2023-12-28 | 225 | 93 | 132 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O5 | A | train | 2010-01-04 | 2023-12-28 | 2010-03-30 | 2023-11-29 | 2010-04-27 | 2023-12-28 | 3374 | 1544 | 1830 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O5 | A | validation | 2024-01-02 | 2024-12-30 | 2024-01-02 | 2024-11-29 | 2024-01-30 | 2024-12-30 | 224 | 116 | 108 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O5 | B | train | 2010-01-04 | 2023-12-28 | 2010-03-30 | 2023-11-29 | 2010-04-27 | 2023-12-28 | 3374 | 1544 | 1830 | 20 | 0 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O5 | B | validation | 2024-01-02 | 2024-12-30 | 2024-01-02 | 2024-11-29 | 2024-01-30 | 2024-12-30 | 224 | 116 | 108 | 0 | 20 | STEP3C_REBUILT_PREFIX_NO_MODEL |
| O1 | A | test_PLANNED_NOT_EVALUATED | 2021-01-04 | 2021-12-30 | 2021-01-04 | 2021-12-30 | 2021-02-01 | 2022-01-28 | 248 | 149 | 99 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O1 | B | test_PLANNED_NOT_EVALUATED | 2021-01-04 | 2021-12-30 | 2021-01-04 | 2021-12-30 | 2021-02-01 | 2022-01-28 | 248 | 149 | 99 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O2 | A | test_PLANNED_NOT_EVALUATED | 2022-01-03 | 2022-12-29 | 2022-01-03 | 2022-12-29 | 2022-02-03 | 2023-01-31 | 246 | 157 | 89 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O2 | B | test_PLANNED_NOT_EVALUATED | 2022-01-03 | 2022-12-29 | 2022-01-03 | 2022-12-29 | 2022-02-03 | 2023-01-31 | 246 | 157 | 89 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O3 | A | test_PLANNED_NOT_EVALUATED | 2023-01-02 | 2023-12-28 | 2023-01-02 | 2023-12-28 | 2023-02-01 | 2024-01-29 | 245 | 104 | 141 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O3 | B | test_PLANNED_NOT_EVALUATED | 2023-01-02 | 2023-12-28 | 2023-01-02 | 2023-12-28 | 2023-02-01 | 2024-01-29 | 245 | 104 | 141 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O4 | A | test_PLANNED_NOT_EVALUATED | 2024-01-02 | 2024-12-30 | 2024-01-02 | 2024-12-30 | 2024-01-30 | 2025-02-04 | 244 | 118 | 126 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O4 | B | test_PLANNED_NOT_EVALUATED | 2024-01-02 | 2024-12-30 | 2024-01-02 | 2024-12-30 | 2024-01-30 | 2025-02-04 | 244 | 118 | 126 | 0 | 0 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O5 | A | test_PLANNED_NOT_EVALUATED | 2025-01-02 | 2025-12-30 | 2025-01-02 | 2025-12-01 | 2025-02-05 | 2025-12-30 | 222 | 45 | 177 | 0 | 20 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |
| O5 | B | test_PLANNED_NOT_EVALUATED | 2025-01-02 | 2025-12-30 | 2025-01-02 | 2025-12-01 | 2025-02-05 | 2025-12-30 | 222 | 45 | 177 | 0 | 20 | EXISTING_STEP27_AGGREGATE_ONLY__NO_TEST_EVALUATION |


Train/Validation은 새 prefix로 재구성했고 Test는 과거 STEP2.7의 집계와 공식 달력만 대조했다. Test 날짜별 가격/Target/확률을 새로 읽어 평가하지 않았다. Test 표본 수는 국내 종가/세션/입력 마스크 관점의 구조적 수이며 가격 원천·production-PIT·외부5변수 확정 표본 수가 아니다. Test2025는222개 예정이고 마지막20개 UNKNOWN을 제외한다. Origin/class별 유리한 날짜를 선택하지 않는다.

## 실행 identity·상한·자원

[500개 job plan](../manifests/step3c_job_plan.csv)은 REUSE_COMPLETED40/PLANNED_NOT_AUTHORIZED460으로 구분한다. O1/O2 신규각80, O3/O4/O5각100, 후보당신규230이다. 최대46,000epoch, Train batch수38/42/46/49/53 기준 최대2,120,000optimizer updates이며 EarlyStopping에 따라 실제 수는 줄 수 있다. 완료/실패 identity를 더 좋은 Seed로 대체하지 않는다. 모델 성능으로 예산·날짜·설정을 변경하지 않는다.

현재 새 확인 자원: cpu.max=`200000 100000`, quota=2.0cores, memory.max=8589934592bytes. 확인시각 `2026-11-16T18:44:38.498297+09:00`. 이전 STEP3B 수치를 가정하지 않고 cgroup를 다시 읽었다. worker≤2/LTC≤1/Torch thread1/OMP-MKL-OpenBLAS1/CPU FP32로 계획한다. 실행 때 현재 자원이 동결값과 다르면 재검증 후 승인된 자원 사양을 만들고 GPU로 임의 이동하지 않는다. epoch 수가 성능 기반으로 달라지므로 확정 소요시간을 약속하지 않는다.

## 준비 코드와 복구

master_data.py는 다섯Origin의 Train/Validation prefix만 생성한다. master_protocol.py는500identity/40재사용/460신규·고정 roster·승인을 검증한다. step3c_worker/manager는 STEP3B의 학습·저장·복원 처리에 근거한 비활성 실행 코드다. max Validation 길이228이라는 기존 상수는 metadata의 각 Origin 표본 수로만 바꿨다. 현재 new_fit_execution_enabled=false여서 worker/model import 전에 차단한다. 기존 STEP3A/3B 승인서를 재사용할 수 없다.

별도 실행 release에는 사용자 승인 reference·config/worker/manager/preflight SHA·460예산·회고적 한계 인정·Test/HMM/GPU 금지·기존40재학습 금지를 바인딩한다. 새로운 config의 제어 플래그와 승인 파일이 필요하며 TEMPLATE(approved=false)는 실행 승인이 아니다. 현재 실행하지 않은 새 다섯Origin 통합 runtime의 실제 실행 호환성은 다음 승인 범위에서 확인할 항목이며 정적검사를 실제 실행 PASS로 쓰지 않는다.

manager lock, identity별 예약/fit.lock, LTC 메모리 lock, 완료/실패 재실행 금지, epoch경계 checkpoint를 사용한다. model/optimizer/scheduler/EarlyStopping/RNG(Python,NumPy,Torch CPU,DataLoader)/Origin/Seed/가격/scaler/피처순서/hash/epoch/batch_position=0를 저장한다. 중단 epoch는 마지막 확정 경계에서 동일 identity로 재개하며 batch중간의 정확복구를 주장하지 않는다. 완료된40개 디렉터리는 읽기/해시 확인용으로만 참조한다. 실제 Test 평가 경로는 이 Train/Validation worker에 제공하지 않고 별도 승인·고정 checkpoint 이후 처리한다.

재준비 명령은 tools/step3c_prepare.py 다음 tools/step3c_freeze.py이며 새 private run 경로를 만든다. 이미 동결한 산출물을 이유 없이 다시 만들지 않는다. 원자료/arrays/date별Target/probability/checkpoint는 ignored data/derived/에만 저장한다. 공개 대상은 코드·집계·해시다.
