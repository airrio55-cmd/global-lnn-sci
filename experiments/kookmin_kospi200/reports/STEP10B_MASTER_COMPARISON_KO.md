# STEP10B 초기·최신 실험 재현성·설계 비교 최종 감사

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

## 최종 판정

**D. NOT_COMPARABLE**: 초기5Seed 단일Test BA와최신10Seed×5Origin BA는같은모델입력·날짜·Target·집계가아니므로직접성능차이를재현성오류나개선/하락으로판정할수없다.

설계차이의설명수준은 **B. PARTIALLY_EXPLAINED**다. 코드·데이터·범위변경의여러차이는확인됐지만숫자차이에대한인과적분해는실행하지않았고초기DOCX와당시공통Seed예측이없다. A(모든차이완전설명)나C(통제동일조건의설명불가불일치/재현실패)라고보고하지않는다.

## 핵심 발견

1. 정확초기DOCX 미확보. 제4.3/4.6/4.7/4.8~4.10 및표6~12검증은BLOCKED다. 현재main/audit파일목록과로컬·기존기록에선원본을찾지못했다.
2. 5Seed Notebook 저장평균은요청된LNN Single BA0.5420/MacroF10.5305와일치하나SD는0.0258/0.0404로요청문0.0260/0.0400과다르다. 원문반올림/오기여부를만들어채우지않는다. Ensemble BA/Recall/PositiveF1도저장출력대응을확인했다.
3. 현재제공Notebook의최종활성LNN은 **LTC** 이며최신LTC와핵심정의source SHA가같다. CfC는별도다. 원문의‘CfC기반’은원문없어미확인이고이차이를성능차이원인으로단정할수없다.
4. 원형Single=RAW5, Ensemble=RAW5/LOG2확률결합;최신F1_LTC=두피처단일채널이다. 원형LOG2와도seedoffset/시간계약이같지않다.
5. 초기759와최신5Origin의날짜/label/평균은다르다. 최신LTC A0.532387/B0.531292는기존다중Origin동결요약이며초기평균에서차감한‘성능하락’이아니다.
6. 1→5에서는loader/LOGoffset/Hybrid가바뀌고,5→10은신경망Seed확장이지만HMM초기화후보도달라진다. HMM후처리변화를기본NN BA의원인으로단정하지않는다.
7. 원형Ensemble누락은외부PIT·제한F1 승인과범위동결의결과다. 최신500은원형앙상블재현이아니다.
8. McNemar correctness/Seed pooling과최신BA MBB/Holm은같은가설이아니며둘다의존성/타당성한계를갖는다. 기존결과는보존,새검정0이다.

검토자료158개와원본3Notebook,공통class 정의·저장요약·설정·과거날짜진단을사용했다. source와원문·실행동일성의증거수준을분리했다. 상세원인표,질문10개답,최소bridge안은각신규보고서에있다. 원문/출처공백을확인한채기술·탐색적F1 논문을집필하는안과원형앙상블을보완하는안은교수검토의별도선택이다.

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
