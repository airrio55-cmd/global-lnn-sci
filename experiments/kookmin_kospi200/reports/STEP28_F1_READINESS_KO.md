# STEP2.8 국내 F1 제한 실험 준비도

확인일 2026-11-16. F1은 입력순서 **Log_Ret, Disparity**만 사용한다. 외국인·Nasdaq·SOX·가공regression 파일을 읽지 않는다. 기존5피처 Historical Baseline과 다른 사전 지정 실험이며 동일 조건의 성능 비교라고 주장하지 않는다. 기존 config/protocol·원본/성능표는 보존했다.

## 데이터 전용 검증

A/B 모두3939공식세션·정확한 session_id+20·3919known/20UNKNOWN·기간내 endpoint 검증 PASS다. 입력은 t-19~t의20세션이다. Train label_end<Validation 시작, Validation 선택 label_end<Test 시작을 유지했다. Train/Valid 각각20purge, Test2025 마지막20UNKNOWN을 제외한다.

기본 F1 smoke는 STEP2.7의 공통 로컬피처20window 적격 마스크를 명시적으로 유지한다. Vol_Regime은 모델 입력이 아니라 수동 레짐용 auxiliary다. 전체known-window3860개, O1Train2387/Valid228로 A/B 동일하다. F1두입력의 결측만 요구하면3881개(O1Train2408)가 될 수 있지만 이 별도적격 수를 현재 smoke 마스크로 조용히 바꾸지 않았다. 공통 비교와 입력전용 마스크의 차이는 사전 정의한 warm-up 정책으로 관리한다.

Scaler는 각 Origin에서 **유지된 Train 입력window 날짜의 합집합**만 fit한다. Validation/Test는 transform만 가능하다. 실제 데이터 전용 StandardScaler 진단과 미래 perturbation 검사를 수행했으며 신경망/HMM 학습과 구분한다.

| Origin | scaler fit 첫날 | 마지막날 | fit행 |
|---|---|---|---|
| O1 | 2010-03-03 | 2019-11-29 | 2406 |
| O2 | 2010-03-03 | 2020-12-01 | 2654 |
| O3 | 2010-03-03 | 2021-12-02 | 2902 |
| O4 | 2010-03-03 | 2022-12-01 | 3148 |
| O5 | 2010-03-03 | 2023-11-29 | 3393 |


prepare_o1_arrays는2021년 이후 가격을 타깃·피처 생성 전에 제거하므로 O1 Test 가격/정답을 전혀 필요로 하지 않는다.2020년 말 유효미확정20개는 제외해Validation228개다. 2021년 이후 가격을 바꾸고2026 sentinel을 추가해도 Train/Validation 입력과 정답이 정확히 같은지 검사했다. dtype은float32, shape는각샘플(20,2), 정답int64이며 비유한값 자동0치환은 없다.

## 예측시각 계약

현재계약 **t18:00 KST·t포함입력**은 변경하지 않았다. A/B 공급처별 과거 available_at·최초/개정 종가·전송/수집 지연 증거가 모두 없어 production-PIT는 **BLOCKED**다. 현재 KRX 상품 전송시간이나 정규장 종료만으로 익명 CSV/Excel이18시에 가용했다고 가정하지 않는다. 원천 가격 진위와 시점 가용성은 별도 요건이다.

사전 정의 가능한 대안은 다음과 같으며 **제안일 뿐 승인/적용하지 않았다**.

- t18:00 유지·입력t-20~t-1: t종가 입력을 제외하지만 t-1종가의 실제 공표/개정 가용성 증빙은 여전히 필요하다. 타깃은Ct→Ct+20으로 유지하는 경우 그 경제적 해석을 별도 명시해야 한다.
- 다음 실제 KRX 세션09:00 의사결정·입력<=t: Ct가그시각에 가용하다는 증빙을 요구한다. Ct→Ct+20 타깃을 유지하면 의사결정과기준일이 달라지므로 새 config/사양으로 등록해야 하며 원래18:00 실험과 동등 비교를 주장하지 않는다.

이 대안의09:00은 제안 의사결정시각이지 공급처의 확인된 공표시각이 아니다. 어떤 lag도 자동 안전 인증으로 쓰지 않는다. 사용자 승인 없이 기존 계약을 바꾸지 않는다.2026년으로 넘어가는 관측/의사결정은 허용하지 않는다.

## 코드 준비와 현재 한계

runtime/step28_smoke_runtime.py와 tools/step28_smoke.py에 실제 동작 코드를 작성했고 **실행하지 않았다**. configs/step28_smoke_config.json은training_enabled=false/hmm_fit_enabled=false, CPU, O1/Seed2/F1을 고정한다. 원본10seed Notebook의 정확한 모델/loss정의를 해시로 검증한 뒤 정의만 재사용하도록 했고 전체Notebook은 실행하지 않는다. 공통 hyperparameter는 그대로다.

향후 승인된 smoke는5모델×RAW/LOG=10경우, 각각1TrainBatch+1ValidationBatch를2회 반복해재현성을 확인한다(총20Train batch update 예정). 이는 구현점검용 한도이며 최대100epoch/기존 scheduler 사양을 바꾸는 실증 실험이 아니다. 입력(64,20,2)·FP32·CPU, loss finite/backward·clip1·AdamW·OneCycle step, model/optimizer/scheduler checkpoint 저장/복원·validation logits 동일성·고정시드 재실행 동일성을 확인한다. Torch weights_only 로드, 새 ignored 출력디렉터리만 허용하며 기존 결과는 덮어쓰지 않는다. Test 정답/지표는 읽거나 출력하지 않고 수치 loss를 성능표로 보고하지 않는다.

Torch/ncps는설치/import/소스검사 PASS, 실제 생성/forward/backward/복원은 미실행이므로 라이브러리 호환성은 PARTIAL이다. F1의 신규고정환경 실험에는 과거 checkpoint나 원본hmmlearn버전 증명을 필수로 요구하지 않는다. 다만 Historical Baseline 재현을 완료했다고 주장할 수 없다. 실제 실행은 모든 필수A gate PASS+config/gates해시에 연결된 별도 사용자 승인 후에만 가능하며 현재는 BLOCKED다.
