# STEP5C_NULL_POLICY_AUDIT_KO

이번 결과는 retrospective rolling-origin statistical analysis다. 가격 A/B는 별도 보고하며 BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, 주가격 PENDING을 유지한다. 모델/가격/Seed/기간/가설을 결과에 따라 선택하지 않았다. finite-replication 중심화 bootstrap p값은 근사값이며 percentile95%CI는 동시 신뢰구간이 아니다. Seed와 Origin을 독립 시장 반복으로 간주하지 않는다.

기존 master_statistics.metric는 실제한클래스일때 Brier 외 BA/MacroF1/Recall0/Recall1을모두NaN 처리했다. 기존STEP3C master와 통계소스는 수정하지 않았다.

STEP5C_STATISTICS_ADAPTER_V1을 생성해 STEP5B에서 이미 동결된 지표정의만 복구했다. BA/MacroF1은 실제한클래스면null, Recall0은실제0 support가있을때계산/없으면null, Recall1도동일하다. Brier/Accuracy는유효비어있지않은입력에서계산,빈집합은null. 단일클래스 **예측**은 실제두클래스일때 BA/MacroF1을null로만들지 않는다. NaN/inf 입력차단,결측0대체금지다.

STEP5B policy v1 SHA `3ff7bb17dc23bc026815861620ce47d33e4112bf5b02160d2d3e24f7e990aee3`

새 statistics adapter SHA `1e44187609b8df23df68967dd1a5c5c5bbe934adaf06d7f4e4c11e8a4b12ab2f`

versioned policy contract SHA `edf94c08f23ca03cc9ee9c56f0dcde96c3a40ea7153cb6531d660169ad2dc0d6`

합성21개PASS/0FAIL. 실제0·1모두/0만/1만/예측모두0/모두1/빈집합/0.5경계/NaN·inf 거절/같은입력의STEP5B per-seed metric 일치를 검증했다. FP64 빈도수 행렬 계산의 지표 오차는 합성에서절대5e-15이내, 실제 관측지표의STEP5B 집계일치도5e-15이내였다. 이는 Test성능에 맞춘 새estimand/가설선택이 아니라 기존정의와구현의정합성복구다. 새로운가족/기간/시드/threshold는추가하지않았다.

공개본은 사전 가설의 다중fit 집계·방법·비민감 SHA만 포함한다. 개별 금융일자/Target/확률·민감 identity/SHA매핑·draw벡터·checkpoint·실제scaler/Train임계값은 로컬 비공개로 보존했다.
