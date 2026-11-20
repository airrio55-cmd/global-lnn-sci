# STEP10B 초기1·5·10Seed 근거 감사

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

## DOCX 검색 범위와 차단

요청된 “[국민대 학위논문 체제] LNN 앙상블 기반 KOSPI200 지수 방향성 예측 모델에 관한 연구 (박사학위논문).docx”는 현재 /workspace의 attachments/library-files/shared/output/work 등 파일목록에서 확보하지 못했다. GitHub 기본브랜치의 ‘LNN 앙상블’, ‘.docx’ 검색도 결과가 없었다. 바이너리는 검색으로 누락될 수 있어 main과 audit의 고정head 재귀tree를 추가로 확인했다. tree는 각각3830/4519개 경로, truncated=false이며 해당 DOCX/학위논문 후보는 없다. 별도 JOF PDF가 보인다는 이유로 대체 문서로 삼지 않았다.

이는 모든 과거 commit·다른 branch·개인 저장소에 원본이 없다는 증명이 아니다. 정확한 DOCX와 원 SHA, 문서버전·작성일 및 각 표의 source Notebook/실행 연결이 필요하다. 제4.3/4.6/4.7/4.8~4.10절 및 표6~12는 현재 모두 BLOCKED다.

## 요청된 초기 수치의 확인 수준

| 검증대상 | 실제 발견 근거 | 판정 | 해석 제한 |
| --- | --- | --- | --- |
| DOCX 제4.3·4.6·4.7·4.8~4.10 및 표6~12 | 원본 부재 | BLOCKED | 논문 문장·표번호·대표Seed 검정 정책 미확인; Notebook 대체 불가 |
| LNN Single BA0.5420 ±0.0260 | 5Seed 셀15: 평균0.5420, SD0.0258 | PARTIAL_MATCH | 평균 일치, SD 마지막 자릿수 불일치; 논문의 반올림 규칙/오류 여부 UNKNOWN |
| LNN Single MacroF10.5305 ±0.0400 | 5Seed 셀15: 평균0.5305, SD0.0404 | PARTIAL_MATCH | 평균 일치, SD 표시값 불일치; 원문 임의 수정 금지 |
| LNN Ensemble BA0.5248 / Recall0.7919 / Positive F10.6971 | 5Seed 셀15의 해당 열 | MATCH_STORED_OUTPUT | 5Seed 지표평균 출력과 일치; 새 재현학습/문서동일성 인증 아님 |
| Test759 | 세 Notebook 셀10 저장출력759 | MATCH_STORED_OUTPUT | 현재첨부 조합의 이전진단과 호환; DOCX 실제날짜/Target 미확인 |
| Positive proportion62.06% | 요청문 보고값 | UNKNOWN | DOCX 및 초기 저장support 미확보; 수치에서 support를 역산하지 않음 |
| 1Seed42 / 5Seed42,52,62,72,82 / 10Seed2..92(step10) | 세 Notebook 셀5 source와 저장출력 | VERIFIED_CODE_AND_LOG | 같은 baseSeed라도 loader·channel·유효seed·데이터 같음 뜻 아님 |

위 SD는 저장 표시 문자열을 직접 읽은 값이며 원 예측으로 새로 계산하지 않았다. 셀15는 np.mean(vals), np.std(vals)의 **ddof=0** 표시다. 문서의 ±0.0260/±0.0400과 코드 출력의0.0258/0.0404를 동일 숫자라고 보고하지 않는다. 반올림 축약일 수 있다는 가능성은 있으나 원문 없이 원인 확정은 불가하다. Positive F1과 Macro F1은 다른 열이다. Ensemble의 Positive F1을 Single의 Macro F1과 직접 순위 비교하지 않는다.

## 재현성의 수준

세 Notebook은 환경 로그(Torch2.10.0+cpu, Windows Python3.12.0, CUDA False), Seed 설정·학습 완료 로그 및 요약 출력을 보존한다. 이는 “과거 실행 기록이 있고 재현성 장치를 의도했다”는 근거다. 동일 Seed 독립 재학습으로 logits/checkpoint/지표가 재현됐다는 증거는 아니다. 공통 Seed의 초기 RAW/LOG 예측 배열·checkpoint·입력/환경 hash chain이 없어5→10 공통Seed exact equality나 초기1→5 재현 성공을 인증하지 않는다. 이번 감사에서는 어떤 학습/forward도 실행하지 않았다.

원본의 ncps/hmmlearn 실제 실행버전이 저장되지 않아 최신 고정 venv와 bitwise 동일 환경이라고 할 수 없다. 같은 Torch 문자열이나 source SHA만으로 과거 결과 재현을 보증하지 않는다. 문서 원본과 당시 source/입력/예측 아카이브 확보가 먼저다.

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
