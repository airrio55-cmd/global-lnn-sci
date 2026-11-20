# STEP10B 데이터·분할·정보시점 비교

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| 항목 | 초기 제공Notebook/첨부조합 | 최신 F1 동결 | 판정·주의 |
| --- | --- | --- | --- |
| 공급처·조정 | KOSPI CSV/외부CSV 공급처·개정·조정 불명 | A/B BOTH_UNVERIFIED, historical18 UNKNOWN | UNKNOWN; 가격진위는 둘 다 미검증 |
| 가격 정밀도 | 원CSV 소수표현; 실제생성cast 미증명 | A=원본+45보완 / B=전체Excel; 기존3892일 float32호환·2일 실질충돌 | 완전 동일가격 아님; 원천정답 미선택 |
| A/B 구분 | 없음; smart_load glob첫 파일 | 고정 A/B 두 후보를 모두 보존 | DATA_DIFFERENCE |
| 기간 | 첨부조합 이전진단: 2010-03-04~2026-03-05(전처리후) | 분석2010-01-01~2025-12-31; 가격2010-01-04~2025-12-30 | 초기DOCX의 실제기간은 UNKNOWN |
| 분할 | len×60/20/잔여20, 고정연도 아님 | 5개 확장 Train / 1년Validation / 다음년Test | TEST_PERIOD_DIFFERENCE |
| 초기Train | 2337행 2010-03-04~2019-10-24; scored2317 시작2010-04-01 | O1 Train2010~2019부터 O5 Train2010~2023 | 이전 data-only 진단; 논문원본 미검증 |
| 초기Validation | 779행 2019-10-25~2022-12-20; scored759 시작2019-11-22 | O1~O5 Validation2020/21/22/23/24 | 여러해 단일Validation vs 연도별 선택 |
| 초기Test | 779행 2022-12-21~2026-03-05; scored759 시작2023-01-19 | Test2021/22/23/24/25의5Origin | NOT_COMPARABLE |
| Test n | 759(세 Notebook 저장출력) | O1..O5=248/246/245/244/222, 후보A/B 동일 | Seed/모델/후보 반복을 시장n으로 곱하지 않음 |
| 상승비율 | 62.06%는 사용자보고; DOCX/support 미확보 | Origin별 동결support 별도; 저장10Seed 일치 확인, 상세private | UNKNOWN/NOT_COMPARABLE; 새비율을 만들어 채우지 않음 |
| Target | (Close.shift(-20)>Close).astype(int), 관측행20 | 공식KRX session_id+20, 미래없으면UNKNOWN | 끝20행False→0 문제; 예전47건horizon수정 기록 구분 |
| 달력 | 원본45세션 누락; 관측행 순서 | 공식3939세션; 보완가격의 공식성은 미확정 | session완전성과 가격인증 구분 |
| 입력/결정시각 | X[i:i+20], y[i+20]: t-20..t-1; 실제cutoff 미정 | t-19..t 포함;18:00 KST 계약, PIT BLOCKED | 같은window20도 정보집합 다름 |
| 결측 | same-date join, ffill/bfill, nan_to_num(비정상0) | 보간/bfill/자동0 금지, 공통Vol_Regime적격mask | bfill실제적용0은 기존감사; 코드위험과 실제영향 구분 |
| 표준화 | Train만fit, Valid/Test transform; RAW/LOG 별도 | 각Origin 유지Train window날짜 합집합fit, 후보별분리 | 원본을 Test-fit이라 비난하지 않음; fit범위는 다름 |
| purging/embargo | 명시 purge/시점계약 없음; 분할각첫20window제외 | Train/Validation label_end cutoff20purge; Test2025끝20UNKNOWN | 추가별도embargo는 명시없음; window손실≠purge |
| 과거입력 재사용 | 분할마다 window독립, Test첫20손실 | 과거Train/Valid 입력 window 재사용 허용 | Test 시작일 적격·표본구성이 달라짐 |

## 비교 단위와 누출 판단의 제한

초기759와 최신5Origin은 같은 날짜집합이 아니다. 초기 구간의 일부가 최신2023~2025와 겹쳐도 전체기간·목표·window·세션·학습선택 정책이 다르다. 이 이전진단 날짜를 미확보 DOCX의 표 날짜라고 단정하지 않는다. 새로2026 가격을 읽어 초기759를 재생성하지 않았다.

원본 target 마지막20의0 변환, 누락거래일, 기간종료 미고정, 경계 forward label 문제는 코드와 이전진단으로 확인됐다. 그러나 각 문제로 BA가 몇 bp 바뀌었는지는 새통제실험 없이 입증되지 않는다. 초기 train label_end가 raw Validation 시작을 넘지만 Validation scored 시작은 그 이후인 구조도 있다(E02). 실제 fit/예측시각 계약이 없으므로 “모든 표본에 누출”이라고 단정하지 않고, 최신의 명시적 partition cutoff와 다름을 보고한다. 추가 embargo를 했다고 꾸미지 않는다.

2025 Test 마지막20UNKNOWN 제외와2021~2024 Test label_end의 다음년 진입 허용은 기존최신사양이다. O1~O4 Test는 후속Origin Validation으로 역사적으로 이미 노출됐다. 달력purge가 있어도 pristine prospective holdout이라고 부를 수 없다.

상승비율은 초기 문서 미확인으로 비워둔다. 최신의 저장 JSON support는 Origin/후보마다10Seed가 같은지 읽기대조했고 상세support는 private에 보존했다. 새Target/확률을 평가하거나 공개 제한된 classsupport를 재게시하지 않았다. 문서의62.06%만으로 초기support를 역산하지 않는다.

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
