# STEP10 LTC τ100 보완 통합

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 버전 | 계측 상태 | 해석·공개 범위 |
| --- | --- | --- |
| 원 STEP7B | 99 PASS / 1 BLOCKED | 당시99개 결과/실패 유지 |
| 독립 STEP7B-R | 1 PASS | 확률 float32 exact, parameter/RNG 불변 |
| 보완 통합 v100 | 100/100; 퇴화24/24, 비퇴화76/76 | 공존 Origin×가격8/8에서 퇴화군 effective τ가 낮은 방향 |

논문 본문 권장 문장: “99개 초기 계측 후 독립 복구로 100개 통합을 완성했다.” STEP8A/STEP9A의99개 분석을100개 분석으로 조용히 교체하지 않는다. 초기 공존셀7/7과 보완8/8은 같은 통합 이력의 서로 다른 버전이며 독립 재현 두 번이 아니다. 기존99개 row와 통합100 중 대응99개의 완전 일치를 확인했다. 복구 snapshot은 byte SHA만 대조했고 추가 checkpoint load/forward는0이다.

raw τ=positive(cm)/positive(gleak), effective τ=positive(cm)/(positive(gleak)+Σsensory conductance+Σrecurrent conductance)이다. 실제 ncps constraints 설정의 positive 변환을 정확히 한 번 적용한 기존 계측을 참조한다. cm_t는 solver 적분항이며 τ 분모에 추가하지 않는다. effective τ는 입력과 hidden 상태에 의존한다. observation-entry와 실제6 solver substep 관측을 구분하며 dt=1은 model_observation_step 계약이다. 원시 τ와 유효 τ를 섞지 않고, τ를 물리적 초·경제적 기억길이·Jacobian 고유시간으로 해석하지 않는다.

퇴화군의 낮은 effective τ는 사후 탐색적 연관이다. Origin/가격/Seed 구성, 중첩 window·뉴런·substep 의존성과 O5 퇴화군 부재가 남아 구성독립효과는 NOT_IDENTIFIABLE이다. 인과효과·퇴화 원인·레짐의 경제적 기억효과를 주장하지 않는다. 확률 exact 재현은 계측의 출력 보존 근거이며 인과적 타당성의 근거가 아니다.

공개는 위 완성 분모와 방향만 유지한다. 신규100 평균·합·분산·분위수·분포·99 대비 변화·복구셀 상세값을 공개하면 기존99 공개값과 차감해 복구1개가 드러날 수 있다. 소수점 축약으로 우회하지 않으며 양군/Origin/Seed/HMM 업데이트까지 보완억제를 적용했다. Figure6도 신규100 수치 분포를 공개하지 않는 개념도로 설계한다. 논문 confidential table은 기존 tau100_aggregates_PRIVATE의 저장값을 그대로 복사한 별도 private 자료이고, 공개 승인 전 학위논문 공개본에도 넣지 않는다.

출처: reports/STEP7BR_100_MODEL_INTEGRATION_KO.md, STEP7BR_DEGENERACY_SENSITIVITY_KO.md, STEP7BR_OUTPUT_EQUIVALENCE_KO.md; manifests/step7br_public_aggregate_summary.json. 원STEP7B/8A/9A는 역사적 버전으로 유지한다.

