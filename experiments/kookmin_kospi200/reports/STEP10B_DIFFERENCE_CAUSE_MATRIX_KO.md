# STEP10B 차이 원인 분류 및 입증 수준

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| ID/분류 | 초기 증거 | 최신 증거 | 구체적 차이 | 영향 가능성 | 실제 영향 입증 | 추가 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| D01 DATA_DIFFERENCE | NBcell9;E02 | E03/E04 | 원CSV45세션누락/과거2026포함→2010~2025공식3939세션 A/B | label/rolling/window/표본이변함 | 기존data-only horizon664→0·label47변경 기록;성능인과기여미입증 | DOCX사용 원데이터/날짜/SHA |
| D02 DATA_DIFFERENCE | NBsmart_load 원CSV | STEP28/10A A/B | 원본+45보완 A 대전체Excel B;2일실질충돌·정밀도차이 | 수익률·Disparity·학습경로변화 가능 | 이전피처차이기록있음;초기↔최신BA차이분해없음 | 공식공급처·버전·수정정책 |
| D03 DATA_DIFFERENCE | NBcell9/10 | data.py/master_data.py | same-date외부join·ffill/bfill·nan_to_num0→외부제외/no0fill | 허용정보·결측/피처값차이 | 이전bfill실제0;코드위험자체가성능변화를입증하지않음 | 초기실행입력·유효시각·값lineage |
| F01 FEATURE_DIFFERENCE | NBcell9feats_raw/feats_log | STEP3Cfeature_order | RAW5 Single/RAW5+LOG2 ensemble→F1 LOG_Ret/Disparity | 다른정보집합·입력차원 | 구조차이확정;효과크기미입증 | 외부피처PIT·통제bridge승인 |
| F02 FEATURE_DIFFERENCE | NBcell10 create_tensors | master_data.py/frozenprotocol | t-20..t-1→t-19..t | 기준일정보포함여부변화 | 입력정렬차이확정;성능분리미실시 | 공통decision/availability계약 |
| M01 MODEL_ARCHITECTURE_DIFFERENCE | NBcell14 LNNensemble | 최신LTC F1 | 두channel LTC 확률결합→단일LTC | ensemble분산/표현차이가능 | 구성차이확정;원형추가효과최신NOT_TESTED | RAW5/LOG2 공통데이터·날짜·offset |
| M02 MODEL_ARCHITECTURE_DIFFERENCE | NBcell8 LNNModel(input_size5) | worker LNNModel(input_size2) | 핵심LTC class는같으나입력차원·일부parameter shape 다름 | 초기화/RNG소비/표현력차이가능 | 코드정의동일·입력인자차이확정;출력효과미분리 | 당시ncps버전·checkpoint |
| T01 TRAINING_DIFFERENCE | singlecell12 vs multi cell12 | STEP3B/Ckernel | 단일global-loader→multi/최신seededgenerator | shuffle·dropout RNG경로차이가능 | 정적차이확정;수치기여미입증 | 공통Seed별예측·RNG·환경기록 |
| T02 TRAINING_DIFFERENCE | single vs multi cell14 | STEP3Coffset/ensembleplan | LOGoffset411→402;Hybrid RNNens→RNNraw | 원형LOG/Hybrid예측차이가능 | 구현차이확정;원형Single RAW의효과와분리 | 정확한문서표의모델정의버전 |
| T03 TRAINING_DIFFERENCE | singleAMP조건/multiOFF | CPUFP32OFF | AMP지원코드는다름;저장실행은모두CPU | CUDA다른실행이면영향가능 | 현재저장CPU결과에AMP가원인이라는증거없음 | 실제장치·패키지·kernel기록 |
| T04 TRAINING_DIFFERENCE | 원본nominal학습설정 | 최신동일nominal설정 | 동일lr/scheduler여도Train배치수·기간·stop시점다름 | 실제LR/초기화·선택경로차이 | 스케줄설계차이경로확인;성능인과기여미입증 | 원학습history·selectedcheckpoint |
| T05 TRAINING_DIFFERENCE | Windows/Python3.12.0;ncps미기록 | 고정Linuxvenv/ncps1.0.1 | 패키지/플랫폼·프로세스RNG관리차이 | 동일Seedbitwise재현제약 | 같은Torch문자열만확인;환경동등성미확인 | lockfile/실행환경·RNG아카이브 |
| P01 TEST_PERIOD_DIFFERENCE | E02 과거단일759 | STEP5B 5Origin | 기간·표본·학습/Validation경계다름 | 시장/클래스구성차이 | 날짜집합의비동등확인;DOCX실제날짜UNKNOWN | 원논문기간·저장date/Target |
| A01 METRIC_AGGREGATION_DIFFERENCE | NBcell15 seedmean±ddof0 | STEP5B/8BR equalOrigin | 단일Test5Seed→각Origin10Seed후5Origin동일가중 | estimand/SD정의다름 | 집계함수차이확정;동일지표차감해석불가 | 공통date·정의·지표단위 |
| A02 METRIC_AGGREGATION_DIFFERENCE | NBcalculate_metrics | STEP5B policy | Positive F1·MacroF1·Recall의열구분,빈/한클래스정책차이 | 표/레짐해석변화가능 | 정의차이확정;사용자초기숫자의문서해석일부UNKNOWN | DOCX표6~12 및null정책 |
| S01 STATISTICAL_TEST_DIFFERENCE | NBcell18 McNemar | STEP5C MBB/Holm | correctness검정 대BA metric delta;baseline·가족도다름 | p값은서로다른가설/의존성가정 | 가설·방법차이확정;새검정없음 | 시계열/Seed의존성가정검토 |
| S02 STATISTICAL_TEST_DIFFERENCE | multiSeed연결·Bonf/BH | datepaired block·Holm | 동일시장정답을Seed수만큼반복한추론 | 과도한독립정보·작은p우려 | 구조적비독립확정;원p값을재계산/무효선언하지않음 | 적격추론법;9B1R METHOD_NOT_VALIDATED유지 |
| H01 IMPLEMENTATION_MISMATCH | NBcell9/10/14 주석5day/window50 | 실제SEEDS설정 window20/shift20 | 안내문과현재코드사양불일치 | 수치영향보다문서해석오류가능 | 불일치확정;horizon이5/50였다고추정불가 | 실행시source/version 증빙 |
| H02 IMPLEMENTATION_MISMATCH | NBcell7 vs8 정의 | 최신cell8추출 | 중복class/EarlyStopping/초기화가순서상덮임 | 구정의만인용하면모델오인 | 최종source재정의확정;원실행순서는UNKNOWN | Notebook execution history·실행버전 |
| H03 IMPLEMENTATION_MISMATCH | 5 vs10 cell14 HMM목록,cell11동일5개 | STEP6B고정후보집합/Trainfilter | NN Seed증가와함께HMM사양까지변경 | 레짐표민감도오염가능;기본NN예측원인으로단정불가 | 사양차이확정;실제최적상태영향재계산없음 | 동결상태·후보source/ledger |
| H04 IMPLEMENTATION_MISMATCH | Test분위수/Viterbi/Test명칭/median | Train-only q30/q70/filter/실패BLOCKED | 후처리레짐정의와미래정보사용차이 | 층화결과의서술/실시간해석달라짐 | 후처리차이확정;기본NN BA에직접인과주장금지 | 원문레짐주장·상태아카이브 |
| U01 UNKNOWN | 요청문 CfC원문주장 | 제공NB최종LTC | DOCX 원문·정확버전 없음 | 문서/코드불일치일수있음 | NOT_CONFIRMED | 정확DOCX·prototype source연결 |
| U02 UNKNOWN | 요청 SD .0260/.0400 | NB저장 .0258/.0404 | 평균은맞지만SD표시값다름 | 반올림/오기/버전차이가능 | 표시차이만확인;원인미확인 | DOCX 원표와반올림규칙 |
| U03 UNKNOWN | 요청 positive62.06%·759 | 최신Origin저장support | 초기실제classsupport·정확Target미확보 | 동일구성비교불가 | UNKNOWN | 원문·당시data/label증빙 |
| U04 UNKNOWN | 초기공통Seed | 최신같은baseSeed | 공통seed의원예측/checkpoint연결없음 | RNG오류/재현실패로결론낼수없음 | NOT_TESTED | 공통Seed결과·데이터·환경hashchain |

차이의 존재와 숫자 성능차이의 인과적 분해는 다르다. DATA/FEATURE/TRAIN/TEST/AGGREGATION 등 여러 축이 동시에 바뀌었으므로 한 요인에 성능차를 귀속하지 않는다. 특히 세Notebook의 최종LTC/CfC/FocalLoss class 정의가같고nominalhyperparameter도많이같다는 **동등한 부분**도 함께 보존한다. “초기LNN은CfC, 최신은LTC라달라졌다”는설명은현재증거로지원되지않는다.

직접수치비교의최종분류는 **D. NOT_COMPARABLE** 이며,설계차이설명수준은 **B. PARTIALLY_EXPLAINED**다. 모든차이의인과기여가검증된A(EXPLAINED_BY_DESIGN_CHANGE)로승격하지않고,통제조건에서예측불일치가나온것도아니므로 C(UNEXPLAINED_MISMATCH)를재현실패로확정하지않는다.

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
