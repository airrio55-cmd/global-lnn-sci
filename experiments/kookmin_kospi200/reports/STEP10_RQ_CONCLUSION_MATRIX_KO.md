# STEP10 연구질문별 증거와 결론

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| RQ | Research objective | Frozen evidence | Observed findings | Counter-evidence | Statistical support | Data limitations | Allowed conclusion | Prohibited conclusion | Dissertation location |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RQ1 | 다섯 NN의 후속 Test 성능 비교 | manifests/step5b_public_aggregate_summary.json#/equal_Origin_weighted / manifests/step5c_execution_summary.json#/families | 저장 평균BA LTC A .532387/B .531292; 지표·가격별 순위 상이 | Primary BA20/Origin BA100 모두 세 블록 기각0; LSTM−LTC Recall1 기존 반대 증거 | FROZEN_DESCRIPTIVE / EXISTING_APPROX_INFERENCE | 가격/PIT 미확정, historical Test 노출, Origin/Seed/label 중첩 | 회고적 평균 차이 관측, NN간 BA 우월성 미입증 | LNN 최고·동등성 입증·전향적 예측력 확증 | 제5장·제9장·제10장 |
| RQ2 | Seed/Origin별 학습·예측 안정성 | manifests/step4d_verification_summary.json / manifests/step5b_public_aggregate_summary.json#/model_instability | LTC Validation/Test 단일예측24/100; LSTM Test2/100; 나머지 세 NN0 | 모든 LTC가 퇴화하지 않음; 단일예측은 NaN 발산과 다름 | FROZEN_DESCRIPTIVE | Validation checkpoint 선택; 10Seed는 독립 시장 반복이 아님 | 조건별 불안정성이 반복 관찰됨 | Seed10회로 미래 안정성 확증·성공 Seed만 선택 | 제6장·제9장 |
| RQ3 | 수동/HMM 레짐별 성능의 기술적 분해 | manifests/step6b_public_aggregate_summary.json#/model_regime_diagnostics / manifests/step6b_public_aggregate_summary.json#/manual_regime_reference_groups | HMM100후보/선택10; High/Low 점유율·유효분모 차이 | Low 일부 한클래스 BA/F1 null; 유효 Origin 집합 상이 | FROZEN_DESCRIPTIVE / NOT_TESTED | small support·상태 추정·구성 차이·historical 노출 | 동결 레짐별 기술적 패턴; null과 분모 함께 보고 | 시장 상태의 인과효과·유리한 레짐 선택 | 제7장·제9장 |
| RQ4 | LTC τ와 단일클래스 퇴화의 관계 | manifests/step7br_public_aggregate_summary.json / reports/STEP7BR_100_MODEL_INTEGRATION_KO.md | 초기99+독립복구1=100; 퇴화24·비퇴화76; 공존8/8 낮은 방향 | 구성 불균형·O5군 부재·중첩 의존성·사후 탐색 | EXPLORATORY_ASSOCIATION / NOT_IDENTIFIABLE | 새100 정량값 보완억제; 경제적 시간단위 아님 | 낮은 effective τ와 퇴화가 함께 관측됨 | τ가 퇴화 원인·경제적 기억길이·구성독립효과 | 제8장·제9장 |
| RQ5 | NN과 단순 기준모형 비교 | manifests/step8br_public_aggregate_summary.json#/candidate_primary / manifests/step8br_public_aggregate_summary.json#/Origin_comparison_directions | NN 평균BA는 Momentum60 .504416보다 높음; Momentum60 F1 .491019 가장 높음 | 기간·지표 불일관; 퇴화 LTC24의 추가BA 없음; 입력이력 차이 | FROZEN_DESCRIPTIVE / NOT_TESTED / BLOCKED_BY_DATA_PROVENANCE | baseline 검정 미실시, BOTH_UNVERIFIED, production-PIT BLOCKED | 같은 평가일의 기술적 benchmark 차이 | 통계적·투자·복잡도의 인과적 우월성 확증 | 제5장·제9장·제10장 |

FROZEN_DESCRIPTIVE=변경 없이 보존된 기술통계; EXISTING_APPROX_INFERENCE=가정 검증 한계를 가진 기존 근사 추론; EXPLORATORY_ASSOCIATION=사후 탐색적 연관; NOT_TESTED=해당 추론 미실시; NOT_IDENTIFIABLE=현재 설계에서 효과 식별 불가; BLOCKED_BY_DATA_PROVENANCE=원천·시점 증빙 불충분이다. 동일 RQ 안에서도 서로 다른 증거수준이 공존한다. 기술표 완성과 과학적 확증을 같은 PASS로 표시하지 않는다.

