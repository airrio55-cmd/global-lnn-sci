# STEP8A BASELINE_PROTOCOL_PLAN

이번 단계는 저장 결과·checkpoint-level τ 요약의 읽기 전용 감사와 기술통계/설계다. checkpoint는 byte SHA만 대조하며 역직렬화·forward하지 않았다. NN500·Test500·STEP5C600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED를 보존한다. τ 전체 분류는 퇴화24/100, 유효 퇴화23개/사용23개, 비퇴화76/76, 전체99/100이다. 기존 확률 exact99개를 유지하고 중단1개를 재시도·대체·0채움하지 않았다. 신규 NN/기준모형 학습·checkpoint load/forward·Test 재생성·HMM fit/refilter·τ추가계측·금융bootstrap/Holm/p값·Ensemble·GPU·2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, historical18KST available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. O1~O4 Test와 후속 Validation의 역사적 중복 및 Origin/Seed/뉴런/window 의존성을 유지한다.

STEP8B는 아직 실행 승인되지 않았다. 아래는 사전 동결을 위한 **DRAFT**이며 금융 실행 예산0이다.

|후보|형태·입력|제안 사양/동률 처리|
|---|---|---|
|Train climatology|Train-only 추정|purging 후 Train Target의 상승비율을 고정 확률로 사용; p>0.5만1, 동률0|
|Logistic regression|학습형; t의 F1 두 피처|C=1,L2,lbfgs,max_iter1000,intercept=True,class_weight=None,random_state20261120 제안; frozen Train scaler; Validation/Test 탐색0. window 펼침을 하지 않는 별도 구조 기준모형임을 명시|
|200DMA|가격 규칙|t포함 과거200 공식세션 평균보다 Close[t]가 크면1; 동률0|
|Momentum60|가격 규칙|Close[t]>Close[t−60]이면1; 정확60세션 차이, 동률0|

각 규칙의 0/1신호를 확률로 취급할 경우 Brier는 사전에 그 정의를 명시하고 calibrated 확률이라고 주장하지 않는다. 모든 후보는 A/B를 독립 유지하고 기존5Origin Train/Validation/Test 및 Train label_end<Validation start purge를 재사용한다. Test 날짜·session·Target·label_end는 STEP5B와 정확히 맞추며 2025말단20 UNKNOWN 제외,2026사용0이다. Train climatology/Logistic은 정해진 Train만으로 fit; Validation을 selection에 사용하지 않는 제안이다. 규칙은 추가 scaler fit이 없다.

200DMA는 과거200가격, Momentum60은61개기준점이 필요하여 F1보다 긴 과거 정보집합이다. t 포함입력/18KST 계약과 공급처 available_at은 별도 검증해야 하며 기존 PIT 미확정을 면제하지 않는다. 준비 시 정확한 고정 Test 날짜에 warmup이 모두 있는지 검증한다. 부족하면 비교 BLOCKED이며 결과를 보고 날짜를 줄이지 않는다. 이번에는 원가격을 열지 않아 warmup 실행 검증은 BLOCKED다. 각Origin 허용 prefix와 입력시점≤t, endpoint≤2025-12-31,Train-only scaler/label purity를 승인 전에 감사한다. 새 baseline의 p값을 기존 STEP5C 가족에 추가하지 않고 별도 사전 가설/가족·승인으로만 계획한다. 학습/규칙 Test평가는0이다.

확인일 2026-11-20 KST. 근거: 보존 STEP4D/5B/5C/6B/7B 보고서·execution manifest 및 checkpoint-level 요약. 신규 공식 원천확인·금융실험은 수행하지 않았다.
