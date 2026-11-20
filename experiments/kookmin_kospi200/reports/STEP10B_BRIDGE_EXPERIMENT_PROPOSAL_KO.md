# STEP10B 최소 bridge 실험 제안 — 미승인·미실행

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

## 필요성의 조건

현재기술·탐색적F1의5개RQ를집필하는데추가금융실험이자동필수인것은아니다. 그러나학위논문핵심주장을‘원형RAW5/LOG2 LNN앙상블의추가효과’로유지하려면최신500만으로답할수없으므로별도bridge를검토해야한다. 초기원문을못받은상태에서예산부터활성화하지않는다.

## Gate0: 금융 실행 없이 먼저 할 일

정확DOCX(제4장·표6~12 포함), 해당원Notebook버전/패키지/사용CSV/SHA, seed별저장예측·date/Target·checkpoint/hashchain을확보한다. 같은날짜/Target/metric의아카이브비교가가능해지면그범위에서단순문서오류를먼저해소할수있다. 현승인은그아카이브가없는상태에서모델forward를실행하는승인이아니다.

공통공급처·지수정의·개정·historical available_at, 외부RAW5가용성및공통유한표본·purge·Train-only scaler 계약을먼저검토한다. A/B중주자료는외부증빙으로결정하거나두후보를미리병렬고정한다. 기존Test지표로선택하지않는다. 사용할Test는이미노출된회고적구간이라는한계를유지한다.

## 최소 구조 제안 — 실행 예산은0

- 가격/기간: 공급처증빙에따른한후보와한연속공통평가구간을우선검토한다. 원문과저장date/label 교집합이라는규칙을사전에정하며,좋은성능Origin을골라기간을정하지않는다. 기존첨부진단상2023~2025가일부겹치지만DOCX날짜가미확인이라정확일자는지금확정하지않는다.
- BaseSeed:42는초기1/5/10의공통구조점검용후보다. 좋은성능Seed라서고르는것이아니며1Seed로강건성을주장하지않는다.
- 모델 최소3개: LTC_RAW5(offset401), LTC_LOG2(offset402), 현재F1_LTC2(offset401). 같은공통target/window/Train/Validation/Test/optimizer사양으로독립학습해야한다. 같은2피처여도LOG402와F1_401을동일identity라고재사용하지않는다.
- 조합: RAW5/LOG2의확률0.5:0.5는위2개모델에서계산하며추가fit0이다. F1 comparator와Single/Ensemble을같은날짜에서기술적으로비교한다. RNNHybrid/CfC/다른모델은핵심질문에필요한경우에만별도추가한다.
- 규모: 이구조의1가격×1구간×1Seed는 **3 fit** 제안이다.5개공통Seed[42,52,62,72,82]까지안정성을보려면15fit/가격/구간,양가격병렬이면각각6fit 또는30fit다. 이는산술적제안규모이며현재승인된예산이나실행결과가아니다.

이제안은원형구조를공통수정프로토콜에서비교하는bridge이며버그·외부PIT미확인을그대로실시간실험으로재현하는것이아니다. 원형회고적실행의정확한재현과수정계약에서의비교는별도목표다. window/label/purge등각수정의인과적효과까지분리하려면추가factor별통제설계가필요하며위3fit로전체원인분해가완성되지않는다.

## 실행 차단

원본문서·출처/외부피처·공통date/Target·환경·코드·승인 gate를충족한뒤별도사용자승인과독립예산을받아야한다. 현재 financial fit/forward/draw/pvalue=0, bridge_approved=false다. 이미본Test에사후적인전향적등록이라는명칭을붙이지않는다. STEP9B1R METHOD_NOT_VALIDATED이므로새금융검정/CI를제안3fit에끼워넣지않는다. 이번에는config·실행roster를활성화하지않았고신규Seed나Ensemble학습을자동시작하지않는다.

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
