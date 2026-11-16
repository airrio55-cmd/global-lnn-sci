# STEP4A-2 다음 실행 조건

STEP3C 동결 사양에 따른 회고적·탐색적 CPU Train/Validation Pilot이다. A/B=BOTH_UNVERIFIED, 18:00 KST production-PIT=BLOCKED를 유지한다. Validation으로 가격·모델·Seed·사양을 고르지 않았다. O4의 독립 Test2024, O5의 독립 Test2025 예측/평가, 2026 관측, HMM fit, GPU, 외부피처/RAW5/앙상블, τ 실측, 확증 p값은 사용/실행하지 않았다. master training_enabled=false/hmm_fit_enabled=false/new_fit_execution_enabled=false는 보존했다.

실제 누적 완료는 기존60+신규40=100개다. 100개 진단 행 수와 실제 완료 수를 구분한다. 실패/중단/BLOCKED는 성공 수에 넣지 않았고 임의 Seed 교체·재학습을 하지 않았다.

## 다음8개 Seed 확장 계획: 이번 실행 아님

Seeds=[22,32,42,52,62,72,82,92], Origin O1~O5, 후보A/B, F1두피처,5모델을 같은 master 사양으로 유지하면5×8×2×5=400fit이다. Origin별80fit, Seed별50fit, 후보별200fit이다. 이번40개가 모두 완료되면 국내F1 전체500 중100개 완료/400개 예정이 된다. 실제 실패가 있다면 전체 잔여는500−100=400이며, 실패 원인과 동일 identity의 재개/재시도 예산을 따로 승인받아야 한다.

400fit의 계획상 상한은40,000epoch/1,824,000optimizer updates이며 EarlyStopping에 따라 실제 수는 달라진다. 새 전용 config·승인·job roster를 만들고 현재 자원, master/source/environment/data/scaler hash, Origin별 prefix·Train20purge·Validation20UNKNOWN·경계·중복 방지와 기존완료 hash를 확인한 뒤 별도 승인된 범위만 실행한다. 현재 요청으로400fit이나 독립 Test를 자동 실행하지 않는다. 낮은 BA/단일 클래스 예측이 있었던 Seed를 삭제하거나 유리한 새 Seed로 대체하지 않는다.

현재 master의500/40재사용/460계획은 STEP3C 동결 당시 기록으로 보존했다. 새 단계의 누적100 및 남은400은 별도 실행 manifest/진단표에 기록하고 master 파일을 덮어쓰지 않는다. 추가40개 승인도 과거40/20개 학습을 다시 승인한 것은 아니다.

가격 공급처·개정정책·역사적18:00 KST 가용성은 미확정이며 A/B Validation 우열로 주 자료를 선택하지 않는다. production-PIT와 회고적 탐색 범위를 분리한다. 독립 Test 평가, HMM fit/forward filtering, RAW5/LOG2/외부피처/Ensemble/전체Ablation, GPU, LTC τ actual forward, 확증 p값은 각각 추가 증빙·사양·별도 승인 전 BLOCKED다. 2026 가격으로 미확정20세션 Target을 보완하지 않는다.

기존 논문 및 앞선 Origin의 Test연도가 후속 Origin Validation으로 이미 관찰되는 역사적 구조를 명시한다. 미관측 전향적 holdout 성능이나 인과적 시장 레짐 효과로 해석하지 않는다. 두Seed의 표준편차는 탐색적 진단이며 전체10Seed 안정성이나 통계적 확증 근거가 아니다. 기존파일/완료모델·JOF/main은 유지한다.
