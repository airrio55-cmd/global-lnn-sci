# STEP10B 실행·근거·SHA 보존 감사

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

## 실행 범위와 실제 행위

신규 금융 작업없이 source text/AST, Notebook 저장text output,기존 JSON/CSV 결과/정책/감사보고서를읽었다. 새금융가격·Target·확률배열을수치로드하거나metric을재평가하지않았다. Notebook source를compile/exec하지않고torch/ncps/hmmlearn을import하지않았다. 코드정의hash/Seed상수/저장표시문자열은정적으로대조했다. 현재5Origin×A/B의저장classsupport는JSON메타데이터에서Seed간일치만확인하고private에보존했으며새상승비율을계산·공개하지않았다.

원본문서는현재로컬파일검색과GitHub검색/고정main·audit tree 조회로찾았다. GitHub플러그인의텍스트검색은바이너리문서를보장하지않아공개GitHub REST tree 읽기전용조회로보완했다. 인증정보를추출/게시하지않았다. tree는비잘림이며해당DOCX후보0이지만다른과거/외부보관소에없다는주장은하지않는다. 관련없는JOF PDF를열어박사원문으로대체하지않았다. 업로드된요청텍스트는사용자지시로읽었고원Notebook 주석·기존문서내용은감사증거로만읽었다.

## 검토와 보존

검토source entries 158개,정적/증거검사 43 PASS /0 FAIL이다. 이외의최종scope/byte검사는종료검증절에추가한다. 정확DOCX원문·문서절/표·초기공통Seed 예측동일성·원문CfC서술은BLOCKED/UNKNOWN/NOT_TESTED이며소스검사PASS로승격하지않는다. 실제문서검증이차단된이번감사를‘초기실험완전재현성PASS’라고보고하지않는다.

작업시작기존 project 10,082개파일을SHA-256 snapshot하고종료때전수대조한다. 이전STEP10A 시작10077개핵심파일및그새5보고서도기존publication SHA와대조했다. 기존500 NN/500 Test,baseline40,STEP5C600,HMM100후보/선택10,τ보완100 및이전실패/복구기록은변경하지않는다. 원Notebook source와metadata를수정하거나저장출력을갱신하지않았다. __pycache__만snapshot에서제외하며핵심결과는모두포함한다.

## 공개 및 신규파일

신규12보고서와3manifest를만들되사용자‘신규보고서만commit/push’지시에따라원격audit commit은12보고서로한정한다. manifest3개는요청경로의로컬파일로작성하며커밋하지않는다. 전체source diff/Notebook출력/상세개별금융메타데이터/입출력SHA mapping/개별classsupport/τ단일복구값은로컬private작업자료에만둔다. 원본시리즈·일별Target/확률·weights/checkpoint를게시하지않는다. 과거공개거부된상세금융표/operational config/내부inventory를재시도하지않는다.

새보고서는초기요청수치의확인수준과설계비교만담고개별Seed모델성능표나대규모Origin별성능표를공개하지않는다. 원자료가격/τ singleton 역산수치를포함하지않는다. main/JOF는변경하지않으며원격branch fresh SHA+expected_sha로보호한다. 실제commit 및main전후동일성은별도완료receipt와최종보고로연결한다.

## 종료 검증

기존파일SHA·신규경로allowlist·공개byte·금융실행0의최종검증후아래에결과를기록한다. 필수원본문서검증의BLOCKED와허용된비교감사/보존PASS를구분한다.

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

최종 종료검증: 기존 10,082개 파일 byte SHA 변경0, 신규로컬경로는 보고서12개+manifest3개뿐이다. 종료 보존·범위·공개검사 35 PASS/0 FAIL이며 앞선정적검사43 PASS와다른그룹이다. 다만 원문DOCX/절·표검증은BLOCKED, 요청SD의저장출력 exact표시일치는불일치, 독립공통Seed재현은NOT_TESTED다. 전체초기재현성을PASS로표시하지않는다. 공개allowlist는보고서12개로만고정했고manifests3개는로컬에만보존한다. 신규금융 fit/forward/draw/pvalue/CI0, master false를유지한다.
