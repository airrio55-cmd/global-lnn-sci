# STEP2.6 차단 항목과 STEP3 준비도

확인일2026-11-16 KST. **STEP3 모델/HMM Smoke Test는 시작할 수 없다.** training_enabled=false, hmm_fit_enabled=false를 유지한다.

| 검증·작업 | 상태 | 남은 조건 |
|---|---|---|
| 전체 KOSPI 200 종가.xlsx | BLOCKED | 실제 파일이 없다. 전체 Excel 업로드 필요 |
| 공통3894일 신규 가격 대조·충돌 | BLOCKED | 수행0건, 충돌 수UNKNOWN. 신규값을 자동 정답으로 처리하지 않음 |
| 누락45일 동일성·병합 | PASS | CSV/XLSX 일치, 한 번씩만 추가 |
| 3939세션 종가·레이블·피처·window 구조 | PASS(사용자 제공 수치 수준) | 공식 가격 인증과 구분 |
| 공식 원천·추출일·수정정책 | BLOCKED | USER_SUPPLIED_VERIFIED_MATCH를 KRX_OFFICIAL_VERIFIED로 올리지 않음 |
| 국내 종가 t18:00 가용성 | BLOCKED | 공급처 공표·수집·개정 시각 증빙 필요 |
| 외국인·NASDAQ·SOX PIT | BLOCKED | 기존 B04/B05의 미확인 사항 유지 |
| 원본 ncps/hmmlearn·단위·checkpoint | BLOCKED | 기존 B07 미해결, 실제 실행 없음 |
| 원자료·전체 일별 파생물 공개 | BLOCKED | 공급처 라이선스 미확정, 로컬 보존 |

7개 BLOCKED gate는 JSON에 분리했다. 공개 라이선스 gate는 게시 범위의 차단이며, 나머지 가격 대조·원천·PIT·runtime 차단과 구분한다. 기존 B01 공식 달력 PASS는 유지한다. B02의 누락 복원은 수치적으로 끝났지만 공식 원천 인증은 끝나지 않았다.

기존23개+STEP2.5의11개+신규18개 검사, 합계 **52 PASS / 0 FAIL**이다. 파일이 없을 때 올바르게 차단하는 기능검사의 PASS와 실제 전체 Excel 대조가 BLOCKED인 것은 서로 다른 판단이다.

새로운 모델 성능·p값을 계산하거나 추정하지 않았다. 원본8개와 보완2개의 해시를 확인했고 기존 보고·manifest·논문 결과·원본 노트북·JOF V14/V15·잠금 파일은 변경하지 않았다. main은 병합 대상이 아니다. 남은 자료가 제공되면 충돌표·출처·PIT를 재검증하고, 별도 실행 승인 뒤에만 STEP3를 검토할 수 있다.
