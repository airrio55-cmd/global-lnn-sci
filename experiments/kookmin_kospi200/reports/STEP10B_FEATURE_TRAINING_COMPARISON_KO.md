# STEP10B 피처·학습·Seed 조건 비교

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| 항목 | 초기1/5/10Seed | 최신 F1 | 해석 |
| --- | --- | --- | --- |
| feature order | RAW5=[Log_Ret,Foreign_Net,Nasdaq,SOX,Disparity], LOG2=[Log_Ret,Disparity] | F1=[Log_Ret,Disparity]만 | 외부3개 제외; 원형RAW5재현 아님 |
| 기본 hyperparameters | Hidden128/layer1/dropout.2/window20/batch64/max100/patience10 | 동일 고정 | 이 항목이 전부 바뀌었다는 설명은 부정 |
| loss | FocalLoss gamma2 alpha.25, crossentropy 2logits | 동일 정의·인자 | BCE 아님; alpha는 전역배율, 클래스별가중 아님 |
| optimizer/scheduler | AdamW lr.005 wd1e-4, OneCycleLR,clip1 | 동일 nominal설정 | Train batch수/실제epoch가 달라 실제LR경로까지같지는 않음 |
| checkpoint 선택 | cell8 EarlyStopping: Validation BA strict>, deepcopy; 동률patience 증가 | Validation BA strict>,최초최고 epoch;동률patience 증가 | cell6의 val_loss/참조state 구현은 덮어써짐 |
| FP32/AMP | 단일: CUDA일때AMP;5/10:use_amp=False | CPU FP32/AMP OFF | 세원본저장환경도CPU여서 실제AMP 차이원인 입증 없음 |
| shuffle/Loader | 모두shuffle=True;단일별도generator없음,5/10유효seed generator | 유효seed 전용generator,num_workers0,CPUthread1 | 같은seed숫자라도 RNG소비순서 다를 수 있음 |
| Seed offset RAW | 101/201/301/401/501 | 같은offset을F1에 사용 | input 차원/시점/기간이달라identity같음아님 |
| Seed offset LOG | 단일111/211/311/411/511;5/10은102/202/302/402/502 | 원형LOG학습안함;F1LTC는401 | F1을LOG402로 조용히재명명 불가 |
| Hybrid | 단일 .7LNNens+.3RNNens,5/10은 .7LNNens+.3RNN_RAW | 미실행 별도원형계약 | 1→5 변화는seed수만의 효과 아님 |
| 환경·결정성 | Windows Python3.12.0/Torch2.10+cpu저장, ncps/hmmlearn 미기록;deterministic try/except | Linux고정venv Python3.12.14/ncps1.0.1,실패명시/RNGcheckpoint | 설정의도≠동일seed 재학습출력증명 |
| 결측/스케일러 | nan_to_num 0; Train별Scaler; 분할별window손실 | no0fill; purgedTrain window 합집합만fit | 원본이Testfit한것은아님; 허용Train날짜가 다름 |

## 시드별 질문의 답

1. 초기Seed42는 단일원본의 RAW+LOG·한Test·cell12 global-loader 조건에서 기록됐다. 5/10Seed의base42는 RAWoffset은 같아도 별도loader generator와LOGoffset/Hybrid가 달라 독립재현이라고 할 수 없다. 저장 CPU환경이므로 AMP설정차이가 실제수치차이를 일으켰다고 주장하지 않는다.
2. 초기5Seed 평균은 동일Test에서 각seed별 model/ensemble 확률을threshold한 뒤 계산한 지표5개의 평균이다. LNN Ensemble은 같은seed RAW/LOG 확률평균이고, 그지표의seed평균과 확률의cross-seed평균은 다르다.
3. 초기10Seed는 **신경망 고정사양·Seed집합 측면에서**5Seed의확장이다. 그러나 공유seed를파일그대로재사용했다는증거는없고공통예측exact대조도불가하다. cell14의HMM초기화목록은5→10개로바뀌므로레짐민감도까지통제된단순확장은아니다. 두파일의cell11목록은여전히같은5개다.
4. 최신10Seed는base집합이같지만F1입력·날짜·label·window·평가집계가다르다. 전체동일학습조건이아니다.
5. 소스·설정차이로결과가달라질수있는경로는확인되지만숫자차이각각의원인은분리입증되지않았다. 같은Seed의다른결과를RNG오류로단정하지않는다.

5↔10의cell5/9/13/14/18 차이중9/13/18은안내·주석변경이주요하며cell9/14의‘5-day’나cell10의‘WINDOW_SIZE50’은실제상수20과불일치하는표시다. 이를새horizon5/50실험으로분류하지않는다.

## 증거 연결

| ID | 증거 | 위치 | 사용 범위·한계 |
| --- | --- | --- | --- |
| E01 | 초기 원본3 Notebook | originals의 단일/5개/10개시드 Notebook; 셀3,5~18 | 현재 파일 SHA·셀 source SHA와 저장출력 정적 확인; 재실행 아님 |
| E02 | 원형 데이터 분할의 과거 data-only 진단 | evidence/data_only_checks.json#/splits, /boundary_checks; reports/AUDIT_KO.md | 현재첨부CSV+코드에 대한 이전 진단; DOCX 실제기간으로 소급확정 불가 |
| E03 | 출처·정밀도·세션·label 이력 | STEP27_FULL_PRICE_AUDIT_KO, STEP28_DATA_DECISION_KO, STEP10A_PRICE_PROVENANCE_AUDIT_KO | 공급처/PIT 미확정; 가격·배열 재계산 없음 |
| E04 | 최신 고정모델·데이터 계약 | configs/step3c_master_experiment_config.json; STEP3C_MASTER_PROTOCOL_KO; runtime/step3b_worker.py, step3c_worker.py | FocalLoss와 최종모델 AST정의 SHA 일치; 실제금융함수 실행 없음 |
| E05 | 500학습 및 동결 Test | STEP4D/STEP5A/STEP5B 보고서·실행summary; step5b_public_aggregate_summary.json | 학습500/Test500, 가격·Origin별 저장지표와 날짜수 읽기만 |
| E06 | 최신 추론·반대증거 | step5c_execution_summary.json#/families; STEP10_STATISTICAL_EVIDENCE_KO; STEP9B1R_EXECUTION_READINESS_KO | 기존600행 및 기각수 보존; 새p값/Holm 없음 |
| E07 | 최종 성능과 기준모형 | step8br_public_aggregate_summary.json#/candidate_primary; STEP10_FROZEN_RESULT_TABLES_KO | 이미 동결된 다중Origin 요약만 인용; 상세 금융표 공개거부 범위 재게시 안함 |
| E08 | F1 제한·Ensemble 별도계약 | STEP28_F1_READINESS_KO, STEP29_READINESS_KO, STEP3A_EXECUTION_AUDIT_KO, STEP3C_LNN_ENSEMBLE_PLAN_KO | 새500결과 이전 F1 범위 문서·승인 이력; 미실행 RAW5/LOG2 계획과 구분 |
| E09 | 초기 DOCX 검색 | 로컬 workspace 파일검색; GitHub main/audit 고정head 재귀tree; 기본브랜치 텍스트검색 | DOCX 미확보; 현재2개 branch tree는 비잘림; 전체과거/외부보관소 부재를 증명한 것은 아님 |
| E10 | STEP10 freeze 및 최신 source/PIT | STEP10_MASTER_AUDIT_KO, FINAL_EXPERIMENT_INVENTORY, RQ_CONCLUSION_MATRIX, STEP10A 5보고서 | 내부무결성 동결과 과학적/PIT 인증은 별개 |
