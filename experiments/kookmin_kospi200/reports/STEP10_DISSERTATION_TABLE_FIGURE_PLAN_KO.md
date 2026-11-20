# STEP10 논문 표·그림 작성 명세

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

## Table1. 연구설계 및 데이터

- Source report: STEP10_DATA_PIT_GAP_AUDIT_KO.md
- Manifest pointer: manifests/step5a_test_calendar_contract.json
- Metric definition: 2010~2025; official-session horizon20; F1;5Origin×10Seed×A/B
- Sample unit: 세션·Origin·가격후보
- Caveats: 3939세션 정렬≠가격/PIT 인증; historic Test 노출
- Draft caption: 표1. 회고적 F1 연구의 기간·세션·정보시점 계약과 미해결 증빙.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table2. 모델·하이퍼파라미터

- Source report: STEP3C_MASTER_PROTOCOL_KO.md
- Manifest pointer: manifests/step4d_verification_summary.json
- Metric definition: Hidden128/1layer/dropout.2/window20/batch64/100epoch/patience10; AdamW .005/1e-4; Focal2/.25; OneCycleLR;clip1;CPUFP32;threshold>.5
- Sample unit: NN 아키텍처·고정 seed offset
- Caveats: 운영config 전체 게시 금지; 단순모형 정보이력 별도
- Draft caption: 표2. 다섯 신경망의 공통 설정과 모형별 정보이력.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table3. NN Test A/B 성능

- Source report: STEP10_FROZEN_RESULT_TABLES_KO.md
- Manifest pointer: manifests/step8br_public_aggregate_summary.json#/candidate_primary
- Metric definition: Accuracy,BA,MacroF1,Brier,Recall0/1
- Sample unit: Origin 내10Seed 평균 후5Origin 평균
- Caveats: 평균순위≠확증; A/B 분리
- Draft caption: 표3. 동결 신경망 Test 성능의 가격후보별 동일가중 요약.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table4. Baseline Test A/B 성능

- Source report: STEP8BR_BASELINE_RESULTS_KO.md
- Manifest pointer: manifests/step8br_public_aggregate_summary.json#/candidate_primary
- Metric definition: 동일6지표
- Sample unit: Origin별1결과 후5Origin 평균
- Caveats: Logistic10 fit는 NN500과 구분; 0/1 Brier 의미 차이
- Draft caption: 표4. 네 기준모형의 가격후보별 기술통계; 금융 검정 미실시.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table5. NN vs Baseline 비교

- Source report: STEP8BR_NN_VS_BASELINE_KO.md
- Manifest pointer: manifests/step8br_public_aggregate_summary.json#/NN_baseline_descriptive_comparisons
- Metric definition: 저장된 BA/F1/Brier 차이 및 Origin 방향
- Sample unit: 5Origin 요약·방향수
- Caveats: 상이한 입력이력; p값 NOT_TESTED; 개별 deterministic 값 억제
- Draft caption: 표5. 평균 BA 추가와 지표·Origin별 반대 증거를 함께 제시한 비교.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table6. Seed/Origin 안정성

- Source report: STEP4D_10SEED_STABILITY_KO.md
- Manifest pointer: manifests/step5b_public_aggregate_summary.json#/groups
- Metric definition: 저장10Seed 평균/표본표준편차·범위, 퇴화 수
- Sample unit: 모델·Origin·가격 내10Seed
- Caveats: 독립 시장관측10배 아님; Validation 선택 편향
- Draft caption: 표6. Seed/Origin 변동과 Test 단일클래스 예측의 기술적 진단.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table7. HMM 및 별도 수동 레짐 성능

- Source report: STEP10_REGIME_INTEGRATION_KO.md
- Manifest pointer: manifests/step6b_public_aggregate_summary.json#/model_regime_diagnostics
- Metric definition: BA/F1, 유효분모; support/Brier는 confidential 저장표
- Sample unit: Origin×가격×레짐의 저장 지표; Seed는 반복
- Caveats: Low 일부 한클래스; 유효 Origin 다름; 표7aHMM/7bManual 분리
- Draft caption: 표7. 레짐 점유율과 정의 가능 지표 수를 동반한 회고적 층화.
- Publication boundary: PUBLIC_SUMMARIES_PRIVATE_SUPPORT_BRIER_APPENDIX
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table8. LTC τ100 통합 진단

- Source report: STEP10_LTC_TAU100_INTEGRATION_KO.md
- Manifest pointer: manifests/step7br_public_aggregate_summary.json
- Metric definition: raw/effectiveτ 정의, 모델단위 유효계수와 방향
- Sample unit: checkpoint100; 퇴화24/비퇴화76
- Caveats: model_observation_step; 새100 정량평균/분포는 차감역산 방지로 비공개
- Draft caption: 표8. 초기99 계측과 독립1 복구를 연결한 보완100 진단 및 해석 범위.
- Publication boundary: PUBLIC_COUNTS_DIRECTIONS_ONLY_CONFIDENTIAL_NUMERIC_TABLE
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table9. 기존 통계검정 증거수준

- Source report: STEP10_STATISTICAL_EVIDENCE_KO.md
- Manifest pointer: manifests/step5c_execution_summary.json#/families
- Metric definition: 기존Holm기각수0/0/0,0/0/0,3/2/3
- Sample unit: 각블록별20/100/80가설
- Caveats: 블록별 결과는 독립 재현 아님; 근사타당성 미검증
- Draft caption: 표9. 동결 통계 결과와 후속 방법론 반례의 서로 다른 증거 역할.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Table10. 연구한계 및 미해결 Gate

- Source report: STEP10_NEXT_GATES_KO.md
- Manifest pointer: manifests/step10_gate_results.json
- Metric definition: PASS/FAIL/BLOCKED 및 증거수준
- Sample unit: gate·RQ
- Caveats: 동결 성공≠PIT 또는 검정 타당성 PASS
- Draft caption: 표10. 재현성·원천·추론·실행승인을 구분한 연구한계.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure1. 연구 전체 흐름

- Source report: STEP10_MASTER_AUDIT_KO.md
- Manifest pointer: manifests/step10_execution_summary.json
- Metric definition: 500fit→Test500→통계600/HMM100→τ99+1/baseline40→집필
- Sample unit: 단계
- Caveats: 실패/복구 분기 보존; 9B2 미실행
- Draft caption: 그림1. 성공과 실패를 함께 보존한 실증·감사 lineage.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure2. Rolling-Origin 설계

- Source report: STEP3C_MASTER_PROTOCOL_KO.md
- Manifest pointer: manifests/step5a_test_calendar_contract.json
- Metric definition: Train→Validation→Test;20session purge/label endpoint
- Sample unit: O1~O5
- Caveats: O1~O4 Test의 다음 Validation 노출 시각 명시
- Draft caption: 그림2. 다섯 Origin의 날짜 경계와 역사적 Test 노출 구조.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure3. BA·Macro F1 비교

- Source report: STEP10_FROZEN_RESULT_TABLES_KO.md
- Manifest pointer: manifests/step8br_public_aggregate_summary.json#/candidate_primary
- Metric definition: 저장5Origin 동일가중BA/F1
- Sample unit: 9모델×A/B
- Caveats: 새 CI/errorbar 생성 금지; 평균순위 선택 금지
- Draft caption: 그림3. 가격후보별 성능지표 순위의 불일관성; 기술적 요약.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure4. Origin별 성능변화

- Source report: STEP5B_TEST_RESULTS_KO.md
- Manifest pointer: manifests/step5b_public_aggregate_summary.json#/groups
- Metric definition: Origin별10Seed 저장BA/F1
- Sample unit: 5Origin×5NN×A/B
- Caveats: baseline deterministic 세부값 복원 금지; Seed SD는 금융CI 아님
- Draft caption: 그림4. 동결 NN 요약에 근거한 시기별 성능 변화.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure5. LTC 퇴화 빈도

- Source report: STEP5B_TEST_RESULTS_KO.md
- Manifest pointer: manifests/step5b_public_aggregate_summary.json#/model_instability
- Metric definition: 단일예측수/100
- Sample unit: 5NN 각각100결과
- Caveats: LTC24와 LSTM2, 다른3모델0 모두 표시; NaN과 구분
- Draft caption: 그림5. 모델별 전체 Test 단일클래스 예측 빈도.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure6. τ 분석 개념·분포의 공개/비공개 구분

- Source report: STEP10_LTC_TAU100_INTEGRATION_KO.md
- Manifest pointer: manifests/step7br_public_aggregate_summary.json
- Metric definition: cm/(gleak+sensory+recurrent), observation/substep
- Sample unit: 개념도 및 confidential checkpoint 분포
- Caveats: 공개는 개념도·분모·방향만; 새100 수치분포는 공개 금지
- Draft caption: 그림6. conductance 기반 τ의 정의와 99→100 보완 lineage; 수치분포는 confidential.
- Publication boundary: PUBLIC_CONCEPT_ONLY_CONFIDENTIAL_DISTRIBUTION
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure7. HMM 레짐 요약

- Source report: STEP10_REGIME_INTEGRATION_KO.md
- Manifest pointer: manifests/step6b_public_aggregate_summary.json#/market_regime_profile_multi_Origin
- Metric definition: 저장평균점유율·유효BA분모
- Sample unit: A/B×2레짐×5Origin
- Caveats: Test state 재생성 금지; 작은Low support·구성차이
- Draft caption: 그림7. HMM 점유율과 지표 정의 가능성; 시장 상태의 인과효과 아님.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

## Figure8. 증거수준 및 한계지도

- Source report: STEP10_RQ_CONCLUSION_MATRIX_KO.md
- Manifest pointer: manifests/step10_evidence_traceability.json#/research_questions
- Metric definition: 6종 evidence label과 RQ1~5
- Sample unit: RQ·주장
- Caveats: 색상 PASS가 확증을 의미하지 않도록 별도범례
- Draft caption: 그림8. 관측 기술통계·기존근사추론·탐색연관·미식별/차단의 지도.
- Publication boundary: PUBLIC_AGGREGATE_ONLY
- status: SPECIFICATION_READY_NOT_NEW_FINANCIAL_CALCULATION

이 패키지는 표10개·그림8개의 명세다. 새 금융 배열을 열거나 그래프를 만들지 않았다. 필요 시 기존 공개 다중Origin·다중Seed 요약만으로 도판을 렌더링할 수 있으나, 유의성 별표·신규 CI·누락값0·τ복구singleton 역산이 없어야 한다. 표7 confidential support/Brier와 표8/그림6 confidential τ수치의 공개 전 별도 재검토가 필요하다. 모든 표·그림에 출처 버전과 캡션을 유지한다.

