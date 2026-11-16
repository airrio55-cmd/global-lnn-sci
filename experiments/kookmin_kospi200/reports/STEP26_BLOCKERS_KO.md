# STEP2.6 차단 항목 갱신

확인일 2026-11-16. 전체 Excel 수령으로 FULL_EXCEL_PRESENT와 COMMON_3894_PRICE_COMPARISON을 PASS로 변경했다. 비교 완료가 가격 충돌 해소나 공식 출처 인증을 뜻하지 않는다.

| 항목 | 상태 | 근거·남은 조건 |
|---|---|---|
| 전체 Excel 3939세션·45일 대조 | PASS | 전체 파일을 실제로 읽어 달력·CSV·보완 Excel과 대조 |
| 기존3894일 가격 비교 수행 | PASS | exact 차이3750건, 소수2자리 차이2건 기록 |
| 가격 차이 원천 판정 | BLOCKED | 2021-04-23·2021-05-06 포함 차이에 대한 공급처 공식 확인 필요, 기존 가격 유지 |
| 공식 가격 출처·개정정책 | BLOCKED | 사용자 파일 간 일치를 공식 인증으로 확대하지 않음 |
| 국내 종가 t18:00 가용성 | BLOCKED | 공급처 과거 공표·수집 시각 필요 |
| 외국인·NASDAQ·SOX PIT | BLOCKED | 기존 B04/B05 증빙 필요 |
| 원본 runtime·checkpoint·dt 단위 | BLOCKED | 기존 B07 유지, 실행하지 않음 |
| 원자료 공개 라이선스 | BLOCKED | 전체 가격·일별 타깃·피처 로컬 보존 |

총 6개 BLOCKED gate. 달력·국내 수치 구조 PASS를 5변수 PIT 실험 준비 완료로 보고하지 않는다. STEP3 모델/HMM Smoke Test 준비는 BLOCKED이며 training_enabled=false, hmm_fit_enabled=false다. 원본·기존 논문 결과·STEP1/2/2.5 보고서·JOF V14/V15는 보존한다. main에 병합하지 않는다.

회귀23개+STEP2.5 11개+STEP2.6 19개 = **53 PASS / 0 FAIL**. 실행·증빙 gate **6 BLOCKED**. 원본8개와 사용자제공3개 SHA-256 보존 검사 PASS.
