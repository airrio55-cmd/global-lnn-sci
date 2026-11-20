# STEP10 데이터 출처 및 PIT 증빙 감사

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 항목 | 판정 | 기존 증거·한계 | 추가 제출자료 |
| --- | --- | --- | --- |
| 가격 A 공급처·개정·조정 | UNKNOWN | STEP28/29 DATA_DECISION; STEP9A LIMITATIONS | 원 다운로드 로그, 공급처 계약, 지수코드·단위, 개정정책 |
| 가격 B 공급처·개정·조정 | UNKNOWN | 사용자 전체 Excel 교차대조는 가격 인증 아님 | 원 제공기관 증빙, 추출일·방식, 조정정책 |
| A/B 원천 인증 | BLOCKED | BOTH_UNVERIFIED / primary PENDING | 성능이 아닌 외부 출처에 따른 선택 증빙 |
| KRX 세션 정렬·20session label 계약 | VERIFIED | STEP25~27의 저장3939세션 대조; STEP5A contract | 파일·세션 구현 검증에 한정, 종가 공식인증 아님 |
| 학습 입력 관측시점·purging·scaler | VERIFIED | STEP3C/4D/5A 유지된 실행 lineage | 알고리즘 계약 확인; actual available_at 검증과 별개 |
| 한국 t18:00 실제 공급처 가용시각 | UNKNOWN | historical18KST available_at UNKNOWN | 당시 시각별 배포·수신 로그 및 수정 이력 |
| production-PIT | BLOCKED | 가격/공표시각 미해결 | 실제 관측시각·공급처 가용시각·버전 lineage |
| Foreign_Net 정의·단위·공표·개정 | UNKNOWN | STEP25 B05 및 STEP9A LIMITATIONS | 시장범위/현물·선물/금액·수량/단위/잠정확정/최초공표 증빙 |
| NASDAQ/SOX 시장종료/DST와 공급처 공개 | PARTIALLY_VERIFIED | STEP25 US calendar 일부 검증; 전체 CSV latency 미확정 | 2010~2025 실제 세션·조기폐장·공급처 지연/개정 증빙 |
| O1~O4 historical Test 노출 | VERIFIED | STEP3C MASTER 및 STEP9A; 뒤 Origin Validation과 중복 | 노출 사실 확인이며 pristine holdout 인증 아님 |
| 원형 RAW5/LOG2 Ensemble | NOT_IN_SCOPE | F1 두 피처 연구와 별개; 원형 미검증 | 외부 피처 PIT·사양·별도 승인 없이는 실행하지 않음 |
| 금융 STEP9B2 | BLOCKED | METHOD_NOT_VALIDATED; 금융 p값0 | 방법론 근거·독립 승인 전 실행 불가 |
| 2026 신규 자료·공식 원천 검색 | NOT_IN_SCOPE | STEP10 수집0/사용0 | 현 작업에서 새 시장자료를 수집하지 않음 |

위 VERIFIED는 해당 내부 계약 또는 노출 사실의 확인을 의미한다. SHA 일치는 파일 무결성이지 가격의 진실성·공표시각 증거가 아니다. 신규 KRX/공급처 검색이나 다운로드를 수행하지 않았다. 3939세션 정렬은 앞선 공식 캘린더 대조의 동결 증거를 인용한 것이며 이 단계에서 외부 재인증한 것은 아니다.

A/B의 두 날짜 가격 충돌과 원본 정밀도 차이 감사는 STEP27/28의 기존 판단을 유지한다. 2026년 가격을 label 확인용으로도 쓰지 않고 분석기간2010-01-01~2025-12-31을 바꾸지 않았다. 전체 F1 결과를 RAW5/LOG2 또는 Ensemble 성과로 기술하지 않는다. JOF V14/V15 및 별도 다국가 연구와 데이터·표·주장을 섞지 않는다.

