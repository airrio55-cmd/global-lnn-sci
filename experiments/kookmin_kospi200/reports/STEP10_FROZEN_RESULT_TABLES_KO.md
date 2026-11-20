# STEP10 동결 성능표 — 공개 요약

이번 STEP10은 기존 결과의 읽기 전용 감사와 논문 집필 준비다. 신규 금융 fit/forward/draw/pvalue/CI는0이며 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, 주가격 PENDING, historical18:00 available_at UNKNOWN, production-PIT BLOCKED다.

자동 공개 승인 검토에서 상세 금융 파생표의 구체적 공개 승인이 확인되지 않아 전송이 거부되었다. 이 공개본은 상세 금융 수치를 제거한 출처·집계계약·해석 요약이다. 전체 논문용 표는 ignored 비공개 집필 패키지에 보존한다. 거부된 상세 자료를 다시 전송하거나 다른 파일로 우회하지 않는다.

공통 모형은 RNN, LSTM, GRU, LTC, CfC 및 CLIMATOLOGY, LOGISTIC, DMA200, MOMENTUM60이다. 가격 A/B는 분리한다. NN은 Origin별 Seed 지표 평균 후 Origin 동일가중평균, 기준모형은 Origin별 단일 결과 후 동일가중평균이다. 금융 예측배열을 다시 평가하지 않았고 기존 동결 요약만 집필용 confidential 표로 옮겼다.

집필 지표는 Accuracy, Balanced Accuracy, Macro F1, Brier, Recall0, Recall1이다. BA=(Recall0+Recall1)/2, Macro F1은 두 클래스 F1의 평균, Brier는 확률 제곱오차다. 빈 레짐 또는 실제 한클래스 BA/F1은 null이며 예측만 한클래스인 경우와 구분한다. SD는 Seed 간 기술적 변동이며 시장 CI가 아니다.

평균 지표별 순위와 Origin별 방향은 서로 다르며, 지표·가격·Seed를 사후 선택하지 않는다. NN과 baseline의 입력이력은 달라 복잡도의 인과효과 비교로 해석할 수 없다. Baseline 대비 금융 통계적 우월성은 NOT_TESTED다.

기존 증거 연결:

- STEP8BR_NN_VS_BASELINE_KO.md와 STEP9A_INTEGRATED_PERFORMANCE_KO.md: 저장 성능과 반대 증거의 기존 버전.
- manifests/step8br_public_aggregate_summary.json: candidate_primary, price_sensitivity_aggregate, Origin_comparison_directions.
- manifests/step5b_public_aggregate_summary.json: groups, model_instability.
- manifests/step9a_evidence_traceability.json: 기존 저장 순위와 근거.

위 문서는 기존 증거의 위치 안내다. 거부된 상세 Origin/모델/Seed 수치를 새 공개표에 재수록하지 않는다. 상세표의 출처·원정밀도·값 일치 검사는 비공개 감사에 보존했다.
