# STEP2.7 남은 차단 항목

확인일2026-11-16. 검사72 PASS /0 FAIL은 코드·데이터 진단의 합격이지 학습 승인이나 최종 가격/PIT 인증이 아니다.

| 항목 | 판정 | 필요한 증거 |
|---|---|---|
| Excel 실제 존재·3939세션·3894가격 대조 수행·45일 일치 | PASS | 해시와 비교표 보존 |
| 가격 충돌 해소·최종 데이터 확정 | BLOCKED | 소수2자리 불일치2021-04-23/2021-05-06와 나머지 수치 차이의 공급처 확인/사전 승인 규칙; 임의 source 우선순위 금지 |
| 국내 종가 출처·t18:00 가용성 | BLOCKED | 공급처/추출·개정정책·과거 공표시각·수집지연 |
| Foreign_Net | BLOCKED | 시장범위·현물/선물·단위·부호·잠정/확정·최초공표/개정 정책 |
| Nasdaq/SOX | BLOCKED | 시장 close와 지수확정·공급처 available_at 지연 구분; 미국달력 미확보기간 포함 증빙 |
| F1 국내입력 제한 실험 | BLOCKED | 외부피처 불필요하나 가격 충돌·국내 공급처/18시 계약은 여전히 필요 |
| Label purging·window 미래포함 검사 | PASS | 후보 수치·고정 경계 수준, 최종가격/PIT가 아님 |
| 패키지 설치/import | PASS | 독립 venv torch2.10.0+cpu/ncps1.0.1/hmmlearn0.3.3 |
| 원본 모델환경·checkpoint·물리dt | BLOCKED | 원본버전 lock·승인 후 별도 구조/실행 검증 |
| 프로토콜 사양 snapshot | PASS | config·소스·프로토콜 해시 동결, 실행 허가 아님 |
| 원본 다중시드 개별 수동레짐 성능 | BLOCKED | 저장된 per-seed 예측/metrics 필요, 평균에서 역산 금지 |
| 원자료 공개 라이선스 | BLOCKED | 공급처 재배포 권한; 현재 raw/price/일별labels/features는 로컬만 |
| STEP3 Smoke/전체학습 실행 | BLOCKED | 필수 증거 모두 PASS + 별도 명시적 실행 승인 |

실행 gate는 data_validation/input_time_contract/model_environment/explicit_step3_execution_approval의4개 BLOCKED이며, 나머지3개(비교 수행·purging·사양동결)는 PASS다. 증빙별 blocker는 gate와 별도로 위 표에 분리했다. Foreign_Net의 단순 이전 세션 사용도 공개시각 검증 전에는 안전하다고 인증하지 않는다. 미국 same-date/무조건shift(1)/검증되지 않은0지연을 사용하지 않는다. processed_regression_data.csv도 기존 B06 미해결로 계속 제외한다.

동일 가격 소스·고정 피처·Origin/Seed·공통 날짜를 사전 확정해야 한다. F1을 성능을 보고 외부피처 대안으로 사후 채택하지 않는다. HMM과 수동레짐 결과는 독립 표, HMM은 향후 Train-only fit/forward filtering이며 Test median 대체는 금지한다.
