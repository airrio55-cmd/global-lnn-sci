# STEP10A 가격 데이터 출처 감사

감사일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci`, `audit/kookmin-kospi200-20261116`, `experiments/kookmin_kospi200/`.

STEP10A는 기존 가격 provenance와 historical PIT 증빙의 읽기 전용 감사다. 신규 금융 학습·checkpoint load/forward·Test 예측/성능 재평가·HMM fit/refilter·τ 계측·bootstrap/draw·p값/CI는0이며 원본·기존 결과·설정을 변경하지 않는다. master training_enabled=false / hmm_fit_enabled=false / new_fit_execution_enabled=false를 유지한다. 2026년 날짜가 있는 파일 속성은 입수·편집 메타데이터로만 읽으며 2026 시장 관측은 사용하지 않는다.

가격 상태는 **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**다. SHA 일치는 무결성 증거이지 외부 공급처·공표시각·과거 vintage 인증이 아니다. Test 성능으로 A/B를 고르지 않는다.

## 가격 입수 lineage와 확인 수준

사용자로부터 작업환경으로 들어온 경로는 확인된다. 공급처에서 사용자의 원본 파일까지의 경로는 확인되지 않는다. 후보A는 원본 CSV와 사용자 보완자료를 혼합한 구성이며, 후보B는 한 전체 Excel을 사용한 구성이다. 한 파일이라는 점은 원천의 신뢰성·과거 가용성 증명이 아니다.

| 구성 | 제공 파일명 | 기간내 구성·입수기록 | 생성·추출일 | 공급처/정의 수준 |
| --- | --- | --- | --- | --- |
| A — 원본 부분 | KOSPI_200.csv | 기존3894개 기간내 관측; 원본2026행은 기존 필터로 제외 | 파일 생성·원 공급처 추출일 UNKNOWN | 공급처·공식 지수코드·개정/조정 UNKNOWN |
| A — 보완 부분 | KOSPI200_누락45일_종가_보완.csv | 공식 세션상 누락45개를 한 번만 병합 | 추출일 UNKNOWN; 전체 Excel에서 추출했다는 보완시트 서술 | USER_SUPPLIED_VERIFIED_MATCH; 공식 인증 아님 |
| 중복입력 금지 | KOSPI200_누락45일_종가_보완.xlsx | CSV와 같은 보완자료; 두 번 합산하지 않음 | 패키지 core 속성에서 생성/수정시각 확인 불가 | 45일 일치 및 출처시트 서술만 확인 |
| B — 전체 | KOSPI 200 종가.xlsx | 2010~2025 전체3939세션 종가 | 아래 파일 내부 메타데이터 참조 | I.101 / I31000040F는 파일 내부 주장; 공급처명 미확정 |

보완 Excel의 ‘출처 및 검증’ 시트는 원본 업로드 파일을 `KOSPI 200 종가.xlsx`, 코드를 `I.101 / I31000040F`, 행 수를3939, 추출 보완을45/45로 표시한다. “공급처/공표시각은 별도 확인 필요”라는 문구도 있다. 기존 감사에서45개 종가의 CSV/XLSX/전체Excel 일치는 확인됐다. 이는 동일 자료의 재표현·추출 관계와 호환되며 독립 공급처의 교차검증으로 세지 않는다. 원본 CSV 구간과 B 전체가 같은 공신력 원천에서 왔다는 증거는 **UNKNOWN**이다.

## Excel 메타데이터: 확인한 사실과 미확인 사실

전체 Excel은 Sheet1 상단16행에 조회 설정을, 이후에 날짜·종가를 둔다. 지수명 ‘코스피200’, 유형 IDX, 코드 I.101, 아이템 I31000040F, 아이템명 ‘종가지수(포인트)’, 일간, 조회기간20100101~20251231을 표시한다. 설정 중 ‘원화’도 있으나 실제 지수 아이템의 단위는 파일 표기의 포인트이며, 이를 통화로 환산한 공식 단위라고 해석하지 않는다. 코드 형식이나 레이아웃만으로 FnGuide/DataGuide/Yahoo/KRX 등 특정 공급처를 단정하지 않는다. 공급처의 공식 code crosswalk와 제품명·필드 정의가 필요하다.

파일 내부 Refresh는 `Last Updated: 2026-11-16 11:28:12`다. 이 문자열에는 timezone이 없으며 행별 관측·공표·수신시각이 아니다. docProps/core.xml은 created=`2026-11-16T02:00:08Z`, modified=`2026-11-16T02:28:43Z`를 담는다. 명시적 UTC값의 KST 환산은 각각2026-11-16 11:00:08, 11:28:43이나 이는 패키지 속성의 표시이며 원 공급처의 추출 영수증이 아니다. 패키지 속성도 편집될 수 있으므로 실제 원본 최초 생성시각으로 인증하지 않는다. App은 Microsoft Excel, AppVersion16.0300이고 Company 값은 비어 있다. Excel 애플리케이션 제조사는 가격 공급처가 아니다. 작성자·수정자 개인정보는 공개하지 않는다.

전체 및 보완 Excel 패키지에 externalLinks 파트와 connections.xml이 없었다. 이 검사는 현재 파일에 그 연결기록이 남아 있지 않다는 뜻이다. 과거 add-in/API 사용이 없었다는 증거는 아니다. 보완 Excel에는 확인 가능한 core 생성·수정 속성이 없었다. CSV의 원 생성·다운로드 날짜는 UNKNOWN이며 파일시스템 mtime이나 첨부 복사시각으로 채우지 않는다.

## 원본 Notebook·기존 저장소 참조를 통한 추적

원본 세 Notebook의 셀 배열1-based9(주석 ‘Cell6’)는 `smart_load('KOSPI_200')`로 재귀 glob의 첫 CSV를 읽는다. 현재 원천을 다운로드하는 코드는 발견하지 못했다. 당시 파일 선택 로그가 없어 원형 실행이 선택한 파일명·SHA까지 이 로더만으로 확정할 수 없다. 현재 F1의 고정 후보/SHA lineage와 원형 Notebook의 비결정적 파일 검색을 구분한다. Notebook를 실행하지 않았다.

고정 저장소 참조 `data/KOSPI200_provenance.json`과 `artifacts/kospi200/acquire_inputs.py`(@81010974…)도 같은 사용자 CSV를 보존·검사하는 내용이다. 보조 시리즈에 Yahoo라는 표현이 있어도 원본 KOSPI200 가격이 Yahoo 공급이라는 증거는 아니다. 해당 보조코드의 Seoul day-end 시간은 모델링 규칙이며 현재 F1의18시 수신 증거로 가져오지 않는다. 그 과거 문서의 달력45일 ‘미확인’ 서술은 후속 STEP25의 공식 세션 검증 이전 버전이므로 최신 세션 증거와 혼동하지 않는다.

## 날짜·가격 충돌의 원인 분류

- 날짜/완전성: 기존 CSV의 기간내3894일과 전체Excel3939일의 차이는45세션 누락이다. 이후 A에 보완45일을 넣어 A/B 완성 후보의 날짜 축은3939세션으로 같다. 같은 종가를 보완 CSV와 Excel에서 중복 합산하지 않았다.
- 표현정밀도: 공통3894일 중144일은 exact/1e-9 이내 일치.3892일은 소수2자리 일치하고 기존 STEP28에서 `old=float64(float32(Excel))`와 호환된다고 확인됐다. 이 중3748일은 exact 차이가 있다. 이는 **수치상 호환**이며 실제 CSV 생성단계의 float32 cast를 입증하지 않는다.
- 미해결 실질충돌: **2021-04-23, 2021-05-06**은 소수2자리에서도 다르고 정밀도 차이만으로 설명되지 않는다. 오기·가격 개정·지수 정의/필드·추출행 정렬 등의 가설은 있으나 어느 원인도 증명되지 않았다. 상세 가격은 기존 비공개 감사표에 유지하고 새 공개 보고서에 전송하지 않는다.
- label 이력과 분리: 과거47건 label 변경은 누락세션 복원으로 관측행+20을 실제세션+20으로 바꾼 이력이다. 기존 STEP28의 A/B known-label 및 label_end 차이0과 별개이며, “가격이 같음/피처·입력까지 같음”을 뜻하지 않는다. 이번에 어떤 label·피처도 재계산하지 않았다.

공식 가격 대조는 이전400 LOGOUT/403 응답으로 미완이며, 실패 응답을 가격 일치나 가격 오류 판정으로 사용하지 않는다. 확인된 가격 공급처·개정정책·공식 가격 정답은 아직 없다. Test 성능을 근거로 A/B 중 하나를 정답으로 택하지 않는다.

## 문제별 판정

| ID | 문제 | 판정 | 범위·근거 | Evidence |
| --- | --- | --- | --- | --- |
| P01 | 현재 작업환경까지의 파일 입수·보존 | VERIFIED | 사용자 제공 파일명·SHA·대화에 첨부된 이력과 로컬 보존 연결; upstream 단계 제외 | E01/E02 |
| P02 | 원본 CSV 실제 공급처·다운로드 경로 | UNKNOWN | 원 다운로드 영수증/추출코드·제품명이 없음; Notebook는 CSV 로더 | E01/E09/E11 |
| P03 | 전체 Excel 실제 공급처·추출 경로 | UNKNOWN | 내부 코드·MS Excel 속성만 있고 인증된 공급처 배포 증거 없음 | E02/E03 |
| P04 | 보완45일과 전체 Excel의 관계 | PARTIALLY_VERIFIED | 자기서술과 기존45값 일치; 독립 공식 원천 인증은 아님 | E04/E05 |
| P05 | 파일 생성·수정/Refresh 표시 | PARTIALLY_VERIFIED | XLSX 속성 값 확인; 원천 추출일·행별 공표/수신시각으로 인증 불가 | E03 |
| P06 | 지수명·코드·단위 정의 | PARTIALLY_VERIFIED | B 내부 I.101/I31000040F·종가지수 포인트; A 공식코드·양후보의 공식 crosswalk 미확정 | E02/E03/E05 |
| P07 | 소수정밀도 차이의 수치상 호환 | PARTIALLY_VERIFIED | 3892일 float32 표현 호환은 기존 정적 대조결과; 실제 생성변환 코드 미확보 | E05 |
| P08 | 두 날짜 실질 가격충돌의 근본원인 | UNKNOWN | 2021-04-23/2021-05-06은 정밀도만으로 설명 불가; 오기/개정/정의차이 중 확정불가 | E05/E07 |
| P09 | 공식 세션 날짜 정렬의 기존 증거 | VERIFIED | 기존3939현물세션과 완성후보 A/B 정렬; 공식 종가 인증 아님 | E02/E06 |
| P10 | A/B 동일 공신력 원천 연결·가격진위 판정 | BLOCKED | 양후보를 같은 공식 제품·버전으로 연결하는 증빙 및 공식 가격응답 부재 | E01/E07 |
| P11 | 수정·조정·재산출/vintage 정책 | UNKNOWN | 수정 전후 값, 발효일, 잠정/확정, 지수 정의 이력 미확보 | E01/E02 |
| P12 | F1 수학적 관측의존·18시 계약 | VERIFIED | t포함20window, Log_Ret/Disparity 순서·식 확인; 실제가용성 제외 | E10 |
| P13 | 행별 지수 공표·최초 공급처 공개시각 | UNKNOWN | 현재상품 공지만 있고 2010~2025의 해당 파일 채널·버전 기록 없음 | E08/E10 |
| P14 | 행별 실제 수신·ingestion·계산완료시각 | UNKNOWN | timestamped receipt/release/vintage 로그 없음; 지연0 가정 불가 | E03/E08 |
| P15 | historical18KST 입력 적격/production-PIT | BLOCKED | 현재 최종본 피처를 해당 날짜18시의 as-of 값이라고 인증할 수 없음 | E08/E10/E12 |

## 원본 파일 무결성 연결

| 제공 파일명 | 기존 및 현재 동일 SHA-256 |
| --- | --- |
| KOSPI_200.csv | 7612a3ea53427dcf0148ab6b1e22f34500e6bff6fe1f23e2da793e40b0b82c50 |
| KOSPI 200 종가.xlsx | 13e34b707d64585fb2f94a828cd387fb89956ae935e27b4ccc9c02e2a2fbdd21 |
| KOSPI200_누락45일_종가_보완.csv | 86ec5203ab99d931688627c380bce5b81bf416ff204e518772aa54a9ed71d513 |
| KOSPI200_누락45일_종가_보완.xlsx | db2e6e049e89ef2563a0ada75f043bc65d3fa576e66ac5d5ba00229111af25ef |

이 표의 SHA는 이미 보존된 파일의 동일성 확인용이다. 파일별 실제 upstream 공급처·배포시각과 연결되는 서명·영수증은 없다. 데이터 공급처와 공개 라이선스의 진위는 이 해시만으로 VERIFIED가 되지 않는다.

## 증거 연결 및 확인 시점

| ID | 증거 | 근거 위치 | 확인일 | 사용 기준·한계 |
| --- | --- | --- | --- | --- |
| E01 | 원본 및 후보의 기록상 연결 | manifests/step29_data_provenance.json#/upstream_file_hashes, /candidates | 2026-11-16 | 원본4개 SHA를 현재 대조; 외부 입수 전 단계는 미증명 |
| E02 | 전체 Excel 형식·내부주장 | manifests/step27_data_validation.json#/full_excel_metadata_claims, /comparison | 2026-11-16 | 파일 내부 코드·수치비교는 공급처 인증 아님 |
| E03 | XLSX 패키지 메타데이터 | KOSPI 200 종가.xlsx: docProps/core.xml, app.xml; Sheet1 상단16행 | 2026-11-21 신규 정적 확인 | 실제 추출/공표·수신 로그와 구분; 작성자 개인정보 비공개 |
| E04 | 보완자료 자기서술 | KOSPI200_누락45일_종가_보완.xlsx: 출처 및 검증 시트 | 2026-11-21 신규 정적 확인 | 전체 Excel로부터 추출했다는 내부 서술; 독립 공식 영수증 아님 |
| E05 | 누락·정밀도·실질충돌의 기존 감사 | reports/STEP26_PRICE_RECONCILIATION_KO.md, STEP27_FULL_PRICE_AUDIT_KO.md, STEP28_PRICE_CONFLICT_KO.md | 2026-11-16 | 이번에 가격을 재계산/재판정하지 않음 |
| E06 | 공식 세션 증거 | provenance/krx_calendar_provenance.json | 과거 조회2026-11-16 / 이번 로컬감사2026-11-21 | 3939 현물세션 날짜만; 종가/PIT 인증 아님 |
| E07 | 공식 가격 접근 실패 | provenance/step28_source_checks.json#/official_price_attempts; provenance/step25_source_catalog.json | 과거 조회2026-11-16 / 이번 로컬감사2026-11-21 | 400 LOGOUT/403은 가격 응답 아님; 신규 재조회 없음 |
| E08 | 현행 EOD 상품 시간 안내의 보존기록 | provenance/step28_source_checks.json#/timing_evidence | 과거 웹확인2026-11-16 / 이번 로컬감사2026-11-21 | 상품 안내의16:00/18:10을 미확인 공급처/과거기간에 대입 불가 |
| E09 | 원 Notebook 로더 | 원본 단일·5·10Seed Notebook 셀 배열1-based9, 주석 Cell6 | 2026-11-21 정적 확인 | smart_load glob첫 CSV; 원 실행 선택 파일·공급처 로그 없음 |
| E10 | 현재 F1 피처·시간 계약 | src/kospi200/data.py: local_features; master_data.py; pilot_data.py; configs/step3c_master_experiment_config.json | 기존 고정소스 / 2026-11-21 텍스트감사 | as-of vintage/received_at를 검증한 것이 아님 |
| E11 | 동일 CSV의 저장소 참조 | data/KOSPI200_provenance.json, artifacts/kospi200/acquire_inputs.py @81010974d4f56c5c02bc028af20e6bab356ae0e4 | 2026-11-21 고정ref 정적 확인 | 사용자 CSV를 보존하는 코드; 공급처 취득코드 아님 |
| E12 | 최종 한계·실험보존 | reports/STEP10_DATA_PIT_GAP_AUDIT_KO.md; manifests/step10_execution_summary.json | 2026-11-20 / 이번감사2026-11-21 | 동결 PASS와 가격/PIT BLOCKED는 별개 |

공식 URL은 과거 보존기록의 연결이며 이번 단계에서 새 가격 수집·공식 페이지 재인증을 수행하지 않았다.

- KRX 세션/휴장일: https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp
- KRX 가격 조회: https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd
- KRX 상품 안내: https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp
- KRX OpenAPI 이용 안내: https://openapi.krx.co.kr/contents/OPP/INFO/OPPINFO003.jsp
- 고정된 저장소 입수 보조코드: https://github.com/airrio55-cmd/global-lnn-sci/blob/81010974d4f56c5c02bc028af20e6bab356ae0e4/artifacts/kospi200/acquire_inputs.py

각 URL의 존재나 조회 성공만으로 첨부 파일과의 공급처 연결이 입증되지 않는다. 과거 실패 응답을 VERIFIED로 바꾸지 않는다.
