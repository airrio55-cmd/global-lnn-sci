# STEP5A_TEST_EXPOSURE_AUDIT_KO

확인시각(KST): 2026-11-20T08:10:41.245073+09:00. 기존 완료500fit, 이번 신규학습0/Test 예측0/Test 성능0/금융 통계검정0/checkpoint load0/모델forward0/HMM0/Ensemble0/τactual0/GPU0/2026관측 사용0. 기존 원본·결과·모델·master flags는 보존한다. 이 문서는 준비·동결 감사이며 계획은 실행 결과가 아니다.

| Origin의 Test | 이미 관찰한 후속 Validation | 해당 Origin 모델선택에 사용? | 연구 전체 노출 |
| --- | --- | --- | --- |
| O1 2021 | O2 Validation2021 | O1 Train/Val≤2020, 저장 경계 PASS | 역사적으로 노출 |
| O2 2022 | O3 Validation2022 | O2 Train/Val≤2021, 저장 경계 PASS | 역사적으로 노출 |
| O3 2023 | O4 Validation2023 | O3 Train/Val≤2022, 저장 경계 PASS | 역사적으로 노출 |
| O4 2024 | O5 Validation2024 | O4 Train/Val≤2023, 저장 경계 PASS | 역사적으로 노출 |
| O5 2025 | 본500fit 후속 Validation 없음 | O5 Train/Val≤2024, 저장 경계 PASS | 원본 논문·이전 가격/레이블 감사 노출 가능; 미관측 인증 안 함 |

저장된 날짜/label_end·price-prefix metadata, input SHA 및 history의 Validation BA 선택 규칙이 각 Origin 경계와 일치한다. 이는 해당 코드·기록의 준수 검증이며 연구자의 모든 과거 관찰이나 숨은 수동선택 부재를 소급 증명하지 않는다. Test 기준일과 다음해 target endpoint의 노출은 구분한다.

향후 명칭은 retrospective rolling-origin evaluation이다. prospective unseen holdout, production-PIT validation, 실시간 거래 수익 검증이라고 쓰지 않는다. 이미 공개한 역사적 논문/Validation 성능을 새로운 검정 근거로 재사용하지 않는다. overlapping Train/Validation 기간·동일 시장·겹친20세션 forward horizon 및 연말 다음해 endpoint 때문에 Origin은 독립 반복 표본이 아니다. Seed 반복도 시장관측 수 증가가 아니다.

공개 범위: 개별500개 identity와 체크포인트/입력/소스 해시를 연결한 동결 roster 및 상세 Test job plan은 자동 공개 승인 검토에서 외부 공개가 거부되어 로컬에만 보존한다. GitHub에는 코드·집계·구조적 달력 계약·요약 보고서만 게시한다. 거부된 개별 매핑을 다른 파일명으로 재게시하지 않는다.
