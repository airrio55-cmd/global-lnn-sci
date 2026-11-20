# STEP10A 실행·보존·공개 감사

감사일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci`, `audit/kookmin-kospi200-20261116`, `experiments/kookmin_kospi200/`.

STEP10A는 기존 가격 provenance와 historical PIT 증빙의 읽기 전용 감사다. 신규 금융 학습·checkpoint load/forward·Test 예측/성능 재평가·HMM fit/refilter·τ 계측·bootstrap/draw·p값/CI는0이며 원본·기존 결과·설정을 변경하지 않는다. master training_enabled=false / hmm_fit_enabled=false / new_fit_execution_enabled=false를 유지한다. 2026년 날짜가 있는 파일 속성은 입수·편집 메타데이터로만 읽으며 2026 시장 관측은 사용하지 않는다.

가격 상태는 **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**다. SHA 일치는 무결성 증거이지 외부 공급처·공표시각·과거 vintage 인증이 아니다. Test 성능으로 A/B를 고르지 않는다.

## 실제 수행한 확인

관련 기존 STEP25~29·STEP10 보고서/manifest, provenance 및 추가 정적계약 소스 합계 **90개 근거 파일**을 읽었다. 이 수에는 관련 모델·실행 준비 문맥도 포함되며 신규 금융 결과를 계산하지 않았다. 별도로 원본 Notebook3개를 JSON 정적 코드로 읽고, 셀 배열1-based9의 CSV 로더를 확인했다. 공급처 다운로드를 입증하는 acquisition 호출은 그 코드에서 발견하지 못했다. 코드 부재는 원 공급처가 존재하지 않는다는 증거가 아니라 현재 자료에 연결 증빙이 없다는 뜻이다.

원본/전체/보완4개 파일 SHA는 STEP29의 보존값과 대조했다. 작업 시작 시 기존 project **10,077개 파일**을 byte SHA-256으로 snapshot했으며 종료 때 동일 목록을 재검사한다. 기존 STEP10 이전10048개 snapshot도 별도로 대조해 변화0을 확인했다. 기존 STEP10 공개18개 문서의 현재 SHA도 publication metadata와 일치한다. cache인 __pycache__를 제외하고 원본·소스·config·financial result·checkpoint·ledger를 포함한 기존 일반 파일이 대상이다.

새로 확인한 Excel 내용은 package core/app 속성, 상단16행과 보완의 출처시트뿐이다. 작성자·수정자 식별자는 공개하지 않았다. 원자료 가격열·일별Target·모델확률·τ 배열을 수치로 읽거나 재계산하지 않았고 checkpoint를 역직렬화하지 않았다. 정밀도·두 가격 충돌·label 차이는 기존 기록을 읽어 분류했다. 2026 metadata 날짜는 시장 관측이 아니다.

고정ref81010974…의 저장소 입수 보조코드를 GitHub 읽기 도구로 확인했다. 이 코드는 텍스트로만 읽었고 실행하지 않았다. 현재 KRX/공급처 가격 페이지 재조회·신규 금융 수집은0이다. 공식 세션·가격 요청 실패·EOD 시간은 과거2026-11-16의 보존 증거로 인용하며 신규 공식 확인으로 표시하지 않는다. 새로 확보된 권위 있는 가격 원천 인증은0건이다.

## 판정의 의미

문제별 VERIFIED/PARTIALLY_VERIFIED/UNKNOWN/BLOCKED는 STEP10A_PRICE_PROVENANCE_AUDIT의 P01~P15에 있다. 문서 감사 완료와 source/PIT 검증 완료를 혼동하지 않는다. 수정·조정·수신시각이 비어 있으면 UNKNOWN으로 유지한다. SHA 일치·Excel 내부코드·현행상품 안내·상호파일 일치로 VERIFIED를 만들어내지 않는다. A/B 주 자료를 선택하지 않았고 공급처를 추정해 채우지 않았다.

## 기존 연구 보존

NN500 및 Test500, Baseline40, STEP5C600행, HMM100후보/선택10, 원STEP7B99PASS/1BLOCKED와 보완τ100, 원STEP8B BLOCKED40와 복구40, STEP9B1/R 방법론 미검증 기록을 수정하지 않는다. τ의 새100 정량집계나 단일복구값을 생성/공개하지 않는다. production training_enabled=false/hmm_fit_enabled=false는 유지되며 source/PIT 상태는 BOTH_UNVERIFIED/PENDING/UNKNOWN/BLOCKED다.

## 새 파일과 공개 범위

이번 audit commit 대상은 아래5개 신규 보고서뿐이다. 기존 파일·프로토콜·config·manifest·실험 결과는 수정하지 않는다. 전체 byte snapshot·상세 읽기목록·원본메타데이터 감사작업 로그는 로컬 scratch에만 보존한다. 원자료·가격열·일별label·확률·checkpoint·내부 identity/SHA 매핑·실제Train threshold·class support·개별τ·개인정보·첨부 UUID를 게시하지 않는다. 과거 자동승인에서 거부된 상세 금융 성능표·operational config·inventory를 재전송하지 않는다.

- reports/STEP10A_PRICE_PROVENANCE_AUDIT_KO.md
- reports/STEP10A_HISTORICAL_PIT_AUDIT_KO.md
- reports/STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md
- reports/STEP10A_REMEDIATION_DECISION_KO.md
- reports/STEP10A_EXECUTION_AUDIT_KO.md

commit/push는 audit 브랜치에만 수행하고 remote 최신 SHA를 확인한 expected_sha 보호를 사용한다. main은 전후 동일 SHA, 새 diff는 위5개 경로 한정으로 검증한다. JOF V14/V15 및 다른 프로젝트 파일은 쓰지 않는다. GitHub commit SHA는 순환 자기참조 대신 별도 완료 영수증과 최종 응답으로 연결한다.

## 종료 보존 검사

최종 종료 SHA·공개 staged-byte 검사 결과는 아래에 완료 후 기재한다. 실패하면 보존 완료로 보고하거나 후속 금융 작업을 실행하지 않는다. 증빙이 추가로 오기 전까지 가격/PIT 인증은 BLOCKED이고 후속 금융 실행은 자동 시작하지 않는다.

종료 검증 결과: 기존 10,077개 파일 byte SHA 변경0, 신규경로는 요청 보고서5개뿐이다. 정적·범위·보존 검사 35 PASS / 0 FAIL. 문제별 판정은 VERIFIED3 / PARTIALLY_VERIFIED4 / UNKNOWN6 / BLOCKED2이며, 감사 완료가 source/PIT 인증 완료를 뜻하지 않는다. 신규 금융 fit/forward/draw/pvalue/CI 및 수집0, 주가격 선택0, master flags=false다. 공개 staged byte와 원격 branch/main 보존은 publication receipt로 연결한다.
