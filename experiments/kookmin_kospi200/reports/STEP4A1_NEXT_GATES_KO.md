# STEP4A-1 다음 실행 조건

사용자 승인 범위의 회고적·탐색적 CPU Train/Validation Pilot이다. A/B는 BOTH_UNVERIFIED이고 production-PIT는 BLOCKED다. 가격·모델·Seed·날짜·설정을 Validation 결과로 선택하지 않았다. 독립 Test2023 및 이후 가격 관측값, HMM fit, GPU, RAW5/외부피처/앙상블, τ 실측 forward, 확증 p값은 사용/실행하지 않았다. 2026년 관측 사용0이다. master production training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false는 변경하지 않았다.

이번 실제 완료 수는 기존40+신규20=60이다. 실패/미완료 identity는 완료 수에 넣지 않았다. O3 20개 완료가 전체500fit 또는 독립 Test 평가의 자동 승인이 아니다.

| 범위 | 전체 계획 | 이미 완료/재사용 | 남은 예정 | 승인 |
| --- | --- | --- | --- | --- |
| 이번 O3·Seed2/12·A/B·5모델 |20|20|0|이번 지시에 한정 |
| O4/O5·Seed2/12·A/B·5모델 |40|0|40|별도 승인 필요 |
| O1~O5·Seed22~92·A/B·5모델 |400|0|400|별도 승인 필요 |
| 국내F1 전체 A/B·5Origin·10Seed·5모델 |500|60|440|자동실행 금지 |

위 남은400+40은 이번20개가 모두 완료된 경우440이다. 실패가 있으면 그 identity의 실패 원인을 보존하고 재학습 여부/예산을 따로 승인받아야 하며 더 좋은Seed로 대체하지 않는다. 각 후속 실행에도 master config·학습kernel·기존완료hash, 해당Origin prefix/strict purge, Train-only scaler, 자원, 중복 방지와 독립 승인 범위를 재확인한다.

가격 A/B 공급처·개정정책·역사적18:00 KST 가용시각은 미확정이다. 현재 회고적·탐색적 양후보 비교를 공식가격/production-PIT 인증으로 승격하지 않는다. Validation BA로 주 가격·모델·Seed를 고르지 않는다. 기존 원본RAW5/LOG2·외부피처·전체Ablation·LNN Ensemble·HMM·GPU·τ actual forward·확증통계·Test는 각각 별도 증빙/사양/승인이 필요하다. 연구기간은2025-12-31까지이며2026년 가격으로 마지막20개 Target을 보완하지 않는다.

O1/O2/O3의 검증연도와 클래스 분포가 다른 점, 과거 논문 결과와 일부 후속 Origin Validation으로 이미 관찰한 역사적 연도가 있는 점을 유지한다. 독립 전향적 검증이나 시장의 인과적 레짐 효과로 표현하지 않는다. source/PIT 미해결과 제한된 두Seed를 보고서에 명시한다. production/new_fit flags는 false를 유지한다.
