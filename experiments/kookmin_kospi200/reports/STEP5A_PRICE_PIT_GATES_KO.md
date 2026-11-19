# STEP5A_PRICE_PIT_GATES_KO

확인시각(KST): 2026-11-20T08:10:41.245073+09:00. 기존 완료500fit, 이번 신규학습0/Test 예측0/Test 성능0/금융 통계검정0/checkpoint load0/모델forward0/HMM0/Ensemble0/τactual0/GPU0/2026관측 사용0. 기존 원본·결과·모델·master flags는 보존한다. 이 문서는 준비·동결 감사이며 계획은 실행 결과가 아니다.

A=기존3894종가+보완45, B=사용자 Excel3939. 두실질 가격 충돌일2021-04-23/2021-05-06 및 나머지 정밀도 차이는 STEP27/28 가격감사·원자료 해시 그대로 보존했다. 이번에 가격을 다시 열거나 상세 값을 공개하지 않았다. 공식 거래일 일치는 가격 진위 인증이 아니다.

| 확인 항목 | A | B | 증거/한계 |
| --- | --- | --- | --- |
| 공급처 | UNKNOWN | UNKNOWN | 사용자 제공 파일이라는 점만 확인 |
| 지수정의/단위 | 명목상 KOSPI200/지수포인트, 공급처 정의 미인증 | 동일 미인증 | 지수코드·공식 원자료와 개별종가 대조 미확정 |
| 다운로드·추출 경로 | UNKNOWN | UNKNOWN | 원업스트림/추출코드 없음 |
| 역사적 수정·개정 | UNKNOWN | UNKNOWN | vintage 증거 없음 |
| 최초 게시/전송시각 | UNKNOWN | UNKNOWN | 과거 available_at 없음 |
| 수집시각 | 원업스트림 UNKNOWN | 원업스트림 UNKNOWN | 파일 업로드/감사일은 원수집시각 대체 아님 |
| t18:00 KST 가용성 | UNKNOWN | UNKNOWN | 당일 close 확정시각과 해당공급처 공개 지연 구분 |
| 현재증거 | 원파일/보완파일 SHA 및 보존감사 | 전체 Excel SHA/교차검증 | source certification 아님 |
| 주 가격 | PENDING | PENDING | Validation/Test 성능으로 선택 금지 |

BOTH_UNVERIFIED / historical available_at UNKNOWN / production-PIT BLOCKED 유지. 기존 provenance 확인일2026-11-16 및 STEP27/28/4D 문서에 근거하며 이번2026-11-20은 저장 증거 검토일이다. 새 공식 가격 증거를 확보했다고 주장하지 않는다.

공식 참고 URL: https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp 및 https://openapi.krx.co.kr/contents/OPP/INFO/OPPINFO003.jsp . 사용기준: 공급처/상품정의 확인을 위한 기존 참고 경로일 뿐, 사용자 파일의 upstream 또는 역사적18시 전달을 입증하지 않는다. 저장증거: provenance/kospi_close_provenance.json, krx_calendar_provenance.json, STEP28_DATA_DECISION_KO.md. URL의 일반 EOD 상품시각을 미상 공급처 값에 임의 적용하지 않는다.

회고적 A/B 비교는 두후보 모두 미인증이라는 한계를 명시한 별도 승인 아래 제안할 수 있다. production 인증에는 공급처·코드·단위·추출·개정·historical timestamp 증거가 추가로 필요하다.

공개 범위: 개별500개 identity와 체크포인트/입력/소스 해시를 연결한 동결 roster 및 상세 Test job plan은 자동 공개 승인 검토에서 외부 공개가 거부되어 로컬에만 보존한다. GitHub에는 코드·집계·구조적 달력 계약·요약 보고서만 게시한다. 거부된 개별 매핑을 다른 파일명으로 재게시하지 않는다.
