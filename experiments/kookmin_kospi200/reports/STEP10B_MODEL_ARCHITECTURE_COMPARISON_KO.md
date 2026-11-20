# STEP10B 모델 정의·LTC/CfC 구분

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| 대상 | 확인 코드 | 구조·사양 | 동등성 범위 |
| --- | --- | --- | --- |
| 초기 cell7 LNNModel | self.lnn=LNN(...) | 앞선 정의; import의 LNN 미정의, cell8로 덮임 | 이 정의만 골라 초기모델 판단 불가 |
| 초기 최종 cell8 LNNModel | self.ltc=LTC(input_size,h,batch_first=True) | LTC+last hidden dropout+Linear(h,2) | 1·5·10Seed 모두 같은 최종 AST정의 SHA |
| 초기 LNN Single | LNNModel RAW5, seed+401 | LTC5피처 | 최신 F1 LTC와 입력차원 다름 |
| 초기 LNN Ensemble | LTC_RAW5 + LTC_LOG2 확률0.5:0.5 | 두 독립channel모델; LOG는RAW의부분집합 | Seed평균이나 CfC Ensemble이 아님 |
| 최신 F1 LTC | 같은 최종 LNNModel 추출, input_size2, seed+401 | LTC2피처, CPUFP32 | 원형LOG2 offset402(단일411)와도 identity 다름 |
| 초기/최신 CfC | 별도 CfCModel: self.cfc=CfC(...) | LTC와 다른 ncps 셀, dropout+2logits | LNN과 이름만으로 혼동 금지 |
| 공통 head/초기화 | hidden128; 외부dropout0.2;2-class fc; Xavier uniform | cell8가 cell7 Kaiming을 덮음 | RNNlayer1은 내부dropout0, 외부dropout은0.2 |
| LTC constraints/라이브러리 | 원호출명은LTC; 당시ncps버전 UNKNOWN | 최신ncps1.0.1 wrapper constraints=True를기존검증 | 같은class source≠당시library·weights 동등성 |

## source SHA의 직접 확인

세 Notebook의 최종 RecurrentModel/LNNModel/CfCModel/init_weights(cell8), FocalLoss(cell6)는 AST 정의 단위로 완전히 동일하다. 최신 STEP3C config의 original_definition_hashes와도 일치한다. LNNModel 정의 SHA는 `ff2ec3b49fb1a96848b9a51aec6dbf4abfac5efdb02fa8fa10f48da77a7e0a7b`, CfCModel은 `2907b0ff7cc2dd6da70b9f9da189004de8f5e2d1fd8f2a06d14aeb26f438ebef`다. 최신worker는 해시검증된 정의를 추출해 LTC/CfC를 다른 클래스에 바인딩한다. 이번에는compile/exec/모델생성을 실행하지 않고 소스만 읽었다.

따라서 제공Notebook의 최종 LNN이 CfC라는 주장은 코드와 맞지 않는다. 다만 “초기논문이 CfC기반이라고 실제로 썼다”는 점은 DOCX 부재로 미확인이다. **문서–코드 불일치는 조건부 의심이며 확정된 원문오류가 아니다.** 문서가 다른 prototype·버전을 가리키면 그 코드/가중치·동일원본 연결을 받아야 한다.

초기LNN Single과 최신LTC는 제공Notebook 범위에서 같은 **LTC 계열과 핵심 클래스 source**를 공유한다. 그러나 RAW5 대F1_2, window정보집합, 데이터·분할·환경이 달라 같은 학습모델/가중치/실험은 아니다. 초기Ensemble과 최신 단일LTC는 직접 동등하지 않다. CfC와LTC의 구조 차이를 초기–최신 성능 변화의 원인으로 단정할 근거도 없다.

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
