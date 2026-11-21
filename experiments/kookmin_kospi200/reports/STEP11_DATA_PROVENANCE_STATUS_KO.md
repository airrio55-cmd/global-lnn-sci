# STEP11 가격 출처 증거수준

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## A/B 구성 및 판정

| 항목 | 후보 A | 후보 B | 판정·한계 |
| --- | --- | --- | --- |
| 최초 보존 파일 | KOSPI_200.csv + 누락45일 보완 CSV | KOSPI 200 종가.xlsx | 사용자 수신본의 존재·SHA 연결 VERIFIED; 공급처 최초 배포본인지는 UNKNOWN |
| 기간내 구성 | 기존3894개 + 보완45개, 중복 합산 없음 | 전체3939개 | 기존 세션 감사 VERIFIED; Excel/CSV 보완본은 동일 자료이지 독립 검증자료가 아님 |
| 생성·추출 시각 | 원 CSV 최초 추출시각 UNKNOWN | 파일 내부 Last Updated 2026-11-16 11:28:12, timezone 불명 | 속성·표시시각 PARTIALLY_VERIFIED; 실제 다운로드/원 공급처 추출·수신시각 UNKNOWN |
| 공급처 | 미확정 | 미확정 | UNKNOWN. Word의 pykrx 서술·Excel 양식·코드명만으로 특정 공급처 인증 불가 |
| 지수 코드·단위 | KOSPI200 종가로 제공됐으나 원 제품 코드 연결 부족 | 파일 내부 I.101 / I31000040F, IDX, 지수 포인트 표기 | 문서상 정의 PARTIALLY_VERIFIED; 공식 제품 crosswalk와 라이선스 UNKNOWN |
| 조정·개정 | 미확정 | 미확정 | UNKNOWN. 현재 최종 값이 당시 배포 값이라는 보장 없음 |
| 누락 세션 | 원본 기간내45개 부족, 별도 보완 | 3939개 세션 포함 | 기존 달력 대조 VERIFIED. 공식 세션과 종가의 공식 인증은 별개 |
| 정밀도 | 다수 값이 float32 표현과 호환 | 대체로 소수 둘째 자리 표시 | 변환 방식 PARTIALLY_VERIFIED; 수치 패턴은 원 생성 로그가 아님 |

전체 Excel 속성의 created/modified 및 Last Updated는 기존 STEP10A에 기록돼 있다. 이는 2026년 시장 관측을 사용하는 일이 아니며, 2010~2025 각 행의 실제 최초 공급 시각을 입증하지도 않는다.

## 실제 차이의 종류

기존 교차감사 공통3894개 중 완전 일치144개, 소수 둘째 자리 일치3892개다. 나머지 정밀도 차이와 실질 충돌2개를 구분한다. 3892개는 기존 값이 Excel 값을 float32로 표현한 경우와 호환되지만, 실제 변환 경로가 그랬다는 증거는 없다. **2021-04-23, 2021-05-06** 두 날짜는 단순 정밀도만으로 설명되지 않는다. 개별 가격은 비공개 기존 충돌표에 보존하며 여기서는 재게시하지 않는다. 오기·수정 vintage·다른 지수 정의 등 원인은 UNKNOWN이다.

기존 감사에서는 A/B session 및 label_end가 같고 known3919/UNKNOWN20, A/B Target 차이0으로 기록됐다. 이는 가격·피처가 동일하다거나 성능 영향이 없다는 뜻이 아니다. 원본 행 shift를 공식 session 기반으로 고친 과거664건 horizon 불일치와47건 label 변경은 A/B 충돌2건의 효과와 구분한다. 이번에 재계산하지 않았다.

## 파일 무결성 연결

| 보존 원본 | SHA-256 |
| --- | --- |
| KOSPI_200.csv | `7612a3ea53427dcf0148ab6b1e22f34500e6bff6fe1f23e2da793e40b0b82c50` |
| 전체 종가 Excel | `13e34b707d64585fb2f94a828cd387fb89956ae935e27b4ccc9c02e2a2fbdd21` |
| 누락45일 CSV | `86ec5203ab99d931688627c380bce5b81bf416ff204e518772aa54a9ed71d513` |
| 동일 보완 Excel | `db2e6e049e89ef2563a0ada75f043bc65d3fa576e66ac5d5ba00229111af25ef` |

STEP10A와 STEP29의 보존 SHA, 변환·실행 manifest가 파일 간 연결을 제공한다. 이번 전체 기존파일 byte 보존 검사는 STEP11_EXECUTION_AUDIT에 별도로 기록한다. SHA는 인증된 공급처 서명·다운로드 영수증이 아니다. 공급처→최초 원본의 외부 연결은 UNKNOWN, 원본→현재 파생본/실행 아카이브의 내부 추적은 VERIFIED 범위다.

## 필요한 증거와 사용 제한

원 다운로드 파일/요청 ID·URL·시각·timezone, 제품 계약/학술 이용조건, 코드·단위 crosswalk, 보완 추출 코드, 두 충돌일의 공식 vintage, 적용기간별 조정·개정 정책, 배포/수신 로그를 원본 SHA와 연결해야 한다. 비밀키·비밀번호는 불필요하다. 공급처 권한·학술 이용조건도 확인해야 하며 공개 불가 자료는 비공개 심사 증빙으로 관리한다.

KRX 세션 provenance는 `provenance/krx_calendar_provenance.json`을 따른다. 기존 공식 가격 접근은 400 LOGOUT/403 등으로 실패한 기록이 있어 가격 인증으로 승격하지 않는다. 기존 경로: https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd , https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp . 기존 확인은 2026-11-16이며 STEP11에서 새 접근 성공을 주장하지 않는다. 동일 공신력 원천으로 A/B를 독립 인증한 증거는 발견되지 않았다. Test 성능에 따른 선택 없이 두 후보를 유지한다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
