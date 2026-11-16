# STEP3C 가격과 정보시점 결정

이번 단계는 사양·데이터 준비와 소스 정적 검사만 수행했다. 신규 모델 fit·모델 생성/forward·checkpoint load·HMM fit·독립 Test 예측/성능 평가·GPU 실행은 모두0건이다. production training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지한다. 기존40개와 원본·논문 결과·JOF V14/V15·main을 보존한다.

## 가격 후보와 선택 상태

A=기존 KOSPI_200.csv의3894개 종가+보완45개, B=사용자 전체 Excel3939개 종가. 두 후보의 source SHA-256은 prepared_inputs datasets의 source_sha256에 고정했다. 원본/보완 파일 및 과거 source 증거도 보존했다. 날짜가 공식 세션과 맞는다는 사실이 가격 공급처·당시 공개시각을 인증하지 않는다. 실제 공급처, 다운로드 방식, revision policy, 최초 공표/수집 지연은 UNKNOWN 또는 미검증이다. 주 가격 선택=PENDING, 연구 설계 선택=PENDING이다.

| 설계 | 선택 원칙 | 사용 및 보고 | 현재 |
| --- | --- | --- | --- |
| 1 | 외부 공급처·지수 정의·추출/개정 증거로 주 가격 선택 | 다른 후보를 동일 사양 민감도 분석으로 모두 보존 | PENDING: 사용자 선택/증빙 없음 |
| 2 | 출처 확인 불가를 명시한 A/B 병렬 회고적 탐색 설계 | 양쪽 결과를 빠짐없이 보고, 우열로 후보 제외 금지 | 사양 준비 PASS, 사용자 선택/실행 승인 PENDING |

설계2는 공식가격·production-PIT 인증을 대체하지 않는다. 이미 관찰한 A/B Validation BA로 주 가격을 정하지 않는다. 공급처 증거가 들어와 가격 정의가 바뀌면 현재40개가 자동 재사용되는 것으로 간주하지 않는다.

## t 18:00 KST 계약과 UNKNOWN

정규장 종료, 지수 종가 산출/확정, 정보상품 전송, 공급처 게시, 사용자의 수집 완료는 각각 다르다. 한국 거래일t 18:00, 입력t-19~t, Close[t]대비Close[t+20] 계약은 유지했다. 원본 t 제외 입력 또는 다음날 의사결정으로 임의 변경하지 않는다. same-day available_at을18:00이나15:30으로 채우지 않는다.

| 검증 요소 | 현재 | 필요한 증빙 |
| --- | --- | --- |
| 공식3939 거래 세션 | PASS | 기존 KRX 달력 source/SHA 유지 |
| 첨부CSV·Excel 실제 공급처 | UNKNOWN | 원천URL/지수식별자/추출 이력 |
| 최초 공표·수정 확정 정책 | UNKNOWN | 기간별 원문 규정/버전 이력 |
| 2010~2025 historical available_at | UNKNOWN | timestamp가 있는 원천/수집 로그 |
| 게시·수집 지연 | UNKNOWN | 공급처 SLA와 실제 수집 영수증 |
| t 18:00 국내 입력 production-PIT | BLOCKED | 관측별 available_at≤decision_time 증명 |

## 출처와 증거 한계

확인/재검토일2026-11-16. 이번 단계에서 새 공식가격·공표시각을 확보했다고 주장하지 않으며 기존 보존 자료를 참조했다.

- [KRX 휴장/거래일 자료](https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp):3939세션의 원천. [provenance](../provenance/krx_calendar_provenance.json)에 기존 추출일·SHA·규칙·연도별 검증이 있다. 가격 공급처 증거로 사용하지 않는다.
- [KRX 정보상품 안내](https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp):STEP2.5에서16:00/18:10 등 전송 구분을 확인했지만 이를 사용자 CSV의 available_at이나2010~2025 소급 정책으로 대입하지 않았다. 기존 [종가 provenance](../provenance/kospi_close_provenance.json)와 [STEP2.5](STEP25_DATA_VERIFICATION_KO.md)를 보존한다.
- 사용자 Excel의 지수/공급처 표시와 소수점 일치는 공급처 인증과 구분한다. 기존 두 날짜 충돌 및 정밀도 감사는 STEP2.8 보고서/비공개 로컬 상세표에 그대로 유지한다. 공개 보고서에 상세 가격을 다시 게시하지 않는다.

회고적 데이터 기반 예측(A)의 준비와 실제 시점 정보만 사용한 PIT 검증(B)을 분리한다. 회고적 학습 성공·Validation 지표·미래 perturbation 통과는 공급처 공표시각의 증거가 아니다. Foreign_Net 시장범위/단위/공표 및 Nasdaq/SOX 공급처 latency/PIT는 여전히 BLOCKED이고 F1에 합치지 않았다.
