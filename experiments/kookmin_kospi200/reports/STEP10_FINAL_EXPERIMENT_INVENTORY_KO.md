# STEP10 전체 실험 최종 목록

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 대상 | 확인 규모 | 근거 | 계수 규칙 |
| --- | --- | --- | --- |
| NN 학습 | 500 | STEP4D; STEP5A/5B frozen roster | 500개 고유 identity, STEP3D O3 재사용20 중복 제외 |
| NN Test 평가 | 500 | STEP5B | 새 평가 0, 저장 확률 SHA만 대조 |
| 기존 통계 결과 | 600 | STEP5C | Primary60 + Secondary240 + Origin300 |
| HMM 후보 학습 | 100 | STEP6B | 각 후보1 fit; Train-only |
| 선택 HMM | 10 | STEP6B | 후보100에 포함되는 최종 선택10; 추가10 fit 아님 |
| Baseline 평가 | 40 | STEP8BR | 4모형 × 5Origin × A/B |
| Logistic fit | 10 | STEP8BR | Baseline40의 일부; NN500에 합산하지 않음 |
| 원 τ | 99 PASS / 1 BLOCKED | STEP7B | 원 실패·partial·ledger 그대로 보존 |
| 보완 τ | 1 PASS | STEP7BR | 기존99 재계측 없음; 별도복구1 |
| 통합 τ | 100/100 | STEP7BR versioned integration | 퇴화24 / 비퇴화76; 공존셀8/8 같은 방향 |
| 원 baseline | BLOCKED40 | STEP8B | 실패40 삭제·성공덮어쓰기 없음 |
| 복구 baseline | PASS40 | STEP8BR | 원 STEP8B와 별도 버전 |
| 방법론 설계·합성 | 완료 / 금융 차단 | STEP9B1 | 통계적 명목 타당성 미확립 |
| 합성 재검토 | 4680 pair / 1200 family / 9설정 | STEP9B1R | METHOD_NOT_VALIDATED; 이 합성 수는 금융 실험 수 아님 |
| 금융 NN-baseline 검정 | NOT_EXECUTED | STEP9B2 | FINANCIAL_PVALUE_COUNT=0; NOT_TESTED |

실제 project 시작 snapshot은 10,048개 파일이다. 125개 관련 보고서를 읽고 메타데이터·SHA·실패 ledger를 대조한 세부 감사 5,380개가 PASS, FAIL0이었다. project 전체 snapshot은 __pycache__를 제외한 모든 기존 일반 파일이며, cache 제외를 숨기지 않는다. 개수는 수치 배열을 다시 평가한 결과가 아니라 기존 roster / result / manifest / ledger의 교차 확인이다.

NN은 정확히 O1~O5×A/B×10Seed×5모델의 집합이다. STEP3A/3B/4A1/4A2/3D/4B/4C/4D라는 단계 이름을 단순 합산하지 않는다. 500개 학습 checkpoint, 동결 Test 확률500, baseline 저장 출력40의 기록 SHA를 대조했으며 checkpoint 역직렬화와 확률 배열 수치 로드는 하지 않았다. HMM100후보와 선택10의 의미 차이는 위 표에 명시했다. 기록 간 불일치는 0이다.

근거: manifests/step4d_verification_summary.json, step5b_execution_summary.json, step5c_execution_summary.json, step6b_execution_summary.json, step7b_execution_summary.json, step7br_execution_summary.json, step8b_execution_summary.json, step8br_execution_summary.json, step9b1_protocol_status.json, step9b1r_method_review.json. 전체 금융 identity/SHA 연결은 private snapshot에만 있다.

