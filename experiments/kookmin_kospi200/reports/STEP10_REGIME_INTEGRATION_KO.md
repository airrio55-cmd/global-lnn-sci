# STEP10 레짐 통합 — 공개 요약

이번 STEP10은 기존 결과의 읽기 전용 감사와 논문 집필 준비다. 신규 금융 fit/forward/draw/pvalue/CI는0이며 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, 주가격 PENDING, historical18:00 available_at UNKNOWN, production-PIT BLOCKED다.

자동 공개 승인 검토에서 상세 금융 파생표의 구체적 공개 승인이 확인되지 않아 전송이 거부되었다. 이 공개본은 상세 금융 수치를 제거한 출처·집계계약·해석 요약이다. 전체 논문용 표는 ignored 비공개 집필 패키지에 보존한다. 거부된 상세 자료를 다시 전송하거나 다른 파일로 우회하지 않는다.

수동 레짐은 Train-only Vol_Regime q30/q70으로 Low/Mid/High를 정의한다. HMM은 Train-only Gaussian 상태모형의 후보 중 Train 기준으로 선택하고 Train 기준 상태 이름을 유지한 forward filtering 결과다. 두 레짐은 상태 수·정의·점유율이 달라 별도 표로 유지한다. Test 전체 Viterbi, Test 분위수 재계산, 재적합·refilter를 수행하지 않았다.

confidential 표에는 기존 저장 n, support0/support1, 유효 metric 개수, BA/F1/Brier, Origin 구성과 점유율을 그대로 연결했다. 시장 support를 Seed 반복 수만큼 부풀리지 않는다. 일부 Low 레짐의 실제 Target이 한클래스여서 BA/Macro F1은 null이다. 해당 클래스가 없는 Recall은 null이며 비어 있지 않은 표본의 Brier는 별도 정의를 따른다. null을0으로 치환하지 않는다.

High/Low 평균은 유효 Origin 구성이 다를 수 있다. 레짐별 차이를 인과적 시장 효과나 유리한 군 선택 근거로 사용하지 않는다. τ에 연결한 레짐은 예측 기준일의 기존 상태이며 전체 입력 window의 상태를 뜻하지 않는다.

기존 증거 연결:

- reports/STEP6B_HMM_REGIME_TEST_KO.md: 기존 HMM 층화 결과의 버전.
- manifests/step6b_public_aggregate_summary.json: HMM_regime_groups, manual_regime_reference_groups, market_regime_profile_multi_Origin, model_regime_diagnostics, method_definitions.
- reports/STEP10_DISSERTATION_TABLE_FIGURE_PLAN_KO.md: 표7과 그림7의 출처·분모·null·공개 범위 명세.

새 공개본은 상세 Origin·모델·레짐별 금융 수치와 class support를 포함하지 않는다. 전체 저장값을 옮긴 집필용 표는 ignored 비공개에 유지한다.
