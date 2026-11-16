# STEP3A 이후 남은 gate와 승인 범위

확인일: 2026-11-16 (Asia/Seoul). 이번 Pilot은 과거 O1 Train/Validation 학습과 저장/복원·구현 진단을 위한 별도 승인이다. 실시간 예측·production-PIT·투자 수익·미래정보 누출 완전 배제·확증적 일반화 성능은 인증하지 않는다.

| 항목 | 현재 판정 | 다음에 필요한 것 |
|---|---|---|
| O1 A/B F1 CPU Pilot | 실제 실행 결과 참조 | 허용된10fit 이외 추가 실행은 별도 승인 |
| 가격 소스/PIT | BOTH_UNVERIFIED / BLOCKED | 공급처·정의·단위·추출/수정·과거vintage·18시 가용성 증빙 |
| A/B 주 자료 선택 | 미선택 | Validation/Test 점수가 아닌 출처 신뢰성·정의·일관성 근거로 사전 결정 |
| Test 평가 | 미승인 | 학습·자료·지표·분석 protocol 확정 후 별도 승인 |
| 전체5Origin/10Seed | 미승인 | 전체 예산·복원 정책·최종 데이터/코드 해시·사전 검정계획 승인 |
| 외부5피처/Ablation | BLOCKED | Foreign_Net 시장/단위/공표, Nasdaq/SOX 공급처 PIT 및 공통 날짜 확보 |
| 수동 레짐 | 기존 Train-only 계획 유지 | 최종 자료로 Train30/70참조 동결; Validation/Test 재계산 금지 |
| HMM fit/레짐 | 미승인 | Train-only fit/선택·명칭, forward filtering·실패보고를 고정한 별도 승인 |
| GPU·LTC τ 분석 | 미승인 | 장치/수치환경 및 실제 시간단위·추출 정의와 추가 실행 승인 |

Validation은 EarlyStopping에 사용한 구현 진단이므로 최종 논문 일반화 성능으로 쓰지 않는다. 단일 클래스 예측·수치 민감도·실패도 있는 그대로 보고하며 이를 보고 seed·날짜·모델 구조·하이퍼파라미터를 바꾸지 않는다. A/B 비교에서 높은 점수를 보이는 후보를 자동 선택하지 않는다.

기존 production training_enabled=false, hmm_fit_enabled=false는 유지했다. 이번 승인은500/3000fit, 전체RO, Test, HMM fit, GPU 또는main 병합 승인으로 확장되지 않는다. 새 연구단계를 원하면 해당 목적·데이터·gate·예산·출력 범위를 별도로 승인해야 한다.
