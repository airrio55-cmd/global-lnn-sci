# STEP10B RAW5/LOG2 Ensemble 범위 변경 감사

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

## 제외 경위와 확인 가능한 이유

원형RAW5/LOG2 Ensemble은 최신실험에서실패해제거된것이아니라 **실행범위에포함되지않았다**. 기존문서의순서는다음과같다.

| 단계 | 기존문서·결정 | 분류·확인 범위 |
| --- | --- | --- |
| STEP25~27 | Foreign_Net 범위/단위/공표, Nasdaq/SOX 공급처PIT 미해결; F1제한가능성검토 | DATA/PIT 문제 확인; 국내종가PIT도완전PASS아님 |
| STEP28 | F1두피처·공통Vol_Regime마스크와 별도smoke gate를준비; 외부5피처는B확장범주 | 새500결과전사양·범위변경;원형RAW5검증대체아님 |
| STEP29 | 합성CPU lifecycle만승인/완료, 실자료전체5피처미승인 | 호환성검사≠원형재현 |
| STEP3A | 사용자명시 F1/O1/Seed2/A,B/CPU 회고적Pilot 승인 | 제한실행scope; source/PIT를PASS로올린것아님 |
| STEP3B/3C 이후 | F1범위로Seed·Origin확장;master500budget;RAW5/LOG2 별도계획 | 고정범위확장;원형ensemble은추가증빙/승인대상 |
| STEP10 | F1 500 동결결과를집필대상으로통합; Ensemble미실행명시 | 성과에맞춰원형ensemble으로재명명불가 |

자원·CPU 예산 제한도 승인범위에 존재하지만, “오직 자원이 부족해서 원형을 뺐다”는 근거는 없다. 확인된 주된 경위는 외부데이터/PIT 차단과 사용자명시 F1 제한설계·별도승인이다. 신경망 성능이 낮아서 Ensemble을 제외했다는 증거는 찾지 못했다. 새500 Test 전에 F1범위가 정해졌다는 사실과 초기논문/일부Pilot 결과를전혀보지않은전향적사전등록이라는주장은다르다.

## 원형의 어떤 대상을 검증하지 못했는가

원형 LNN Single은LTC_RAW5(seed+401), LNN Ensemble은그RAW5와LTC_LOG2(seed+402;단일원본은411)의확률평균이다. 최신F1 LTC는두피처이지만offset401이다. 따라서원형Single도LOG402도아니고,동일확률두번평균은Ensemble재현이아니다. RAW/LOG가서로독립데이터라는주장도하지않는다.

STEP3C_LNN_ENSEMBLE_PLAN은원형Single/LOG/Ensemble의공통날짜·candidate/Origin/Seed 정렬과별도확장가족을설계했지만실행결과가아니다. 최신NN500에원형channel 학습이나Ensemble검증이숨어있다고보고하지않는다. CfC Ensemble 및Hybrid도미실행이다.

## 논문 RQ에 따른 필요성

주장이‘RAW5/LOG2 LNN 앙상블의추가효과’이면현F1만으로핵심RQ를답할수없다. 원자료·PIT·환경·공통평가계약을확보한뒤별도최소bridge가필요할수있다. 반면RQ가‘국내F1 신경망비교·학습안정성·레짐·LTC내부진단’이면원형ensemble을미검증Historical Baseline으로분리하고제목/RQ를정직하게조정하는경로가있다. 추가학습의필요성은논문핵심주장에의해정하며현재Test성능으로결정하지않는다.

지금은제안/검토이며학습·앙상블계산·신규평가를실행하지않았다.

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
