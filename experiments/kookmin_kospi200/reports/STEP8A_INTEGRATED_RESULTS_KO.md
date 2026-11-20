# STEP8A INTEGRATED_RESULTS

이번 단계는 저장 결과·checkpoint-level τ 요약의 읽기 전용 감사와 기술통계/설계다. checkpoint는 byte SHA만 대조하며 역직렬화·forward하지 않았다. NN500·Test500·STEP5C600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED를 보존한다. τ 전체 분류는 퇴화24/100, 유효 퇴화23개/사용23개, 비퇴화76/76, 전체99/100이다. 기존 확률 exact99개를 유지하고 중단1개를 재시도·대체·0채움하지 않았다. 신규 NN/기준모형 학습·checkpoint load/forward·Test 재생성·HMM fit/refilter·τ추가계측·금융bootstrap/Holm/p값·Ensemble·GPU·2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, historical18KST available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. O1~O4 Test와 후속 Validation의 역사적 중복 및 Origin/Seed/뉴런/window 의존성을 유지한다.

|영역|질문·자료|직접 근거/반대 근거|근거 수준·한계|사용 가능 표현 / 불가 표현|
|---|---|---|---|---|
|예측 성능|F1 5모델,5Origin,A/B,10Seed|STEP5B Test500; STEP5C Primary BA20·Origin BA100 가족은 블록20/40/60 모두 Holm<.05가0. Secondary에서는 Recall/Brier 일부 차이|기존 동결 검정만 인용; 비유의는 동등성 아님; 과거 Test 노출과 가격/PIT 한계|“BA 차이를 입증하지 못했다” / “LTC는 동등·우월하다” 불가|
|Seed/학습 안정성|500fit과 LTC24/100 퇴화|STEP4D Seed/epoch 진단 및 STEP5B 전체Test 퇴화; 다른모델·Origin 차이도 보존|동일 시장 날짜의 Seed는 독립 관측 아님; 퇴화는 NaN 발산과 다름|“특정 조건에서 단일클래스 예측 반복” / “실험횟수500으로 확증” 불가|
|시간·레짐|5Origin 및 Train-only HMM 최종10|STEP6B 고정 순차filter/기존 성능표; 실제 단일클래스 Low레짐 BA null|점유율·class support·유효 Origin집합이 달라 High/Low 단순비교 제한|“레짐별 기술적 변화” / “고변동성이 성능을 인과적으로 변화” 불가|
|LTC 내부 동역학|τ99개, 퇴화23/비퇴화76|STEP7B exact99; pooled0.0291 vs0.0490; STEP8A 층화/구성 점검|정의는 conductance 진단량; 한군 없는 셀/누락/작은군 존재|“유효표본에서 낮은 τ가 함께 관측됨” / “짧은 기억이 퇴화를 야기” 불가|

문장1 “LTC는 단일클래스 예측을 반복적으로 보였지만 전체 Test BA에서 일관된 통계적 열위를 보이지 않았다”는 STEP5B24/100 및 STEP5C BA가족으로 제한하여 사용 가능하다. 더 정확한 표현은 “동결 BA 검정에서 모델 간 차이를 입증하지 못했다”다. Secondary Recall1의 불리한 차이를 반대 근거로 함께 보고하며 동등성·열위 부재의 증명으로 쓰지 않는다.

문장2 “퇴화 LTC는 상대적으로 낮은 Effective τ를 보였지만 Origin/Seed 구성과의 연관 및 인과 메커니즘은 확인되지 않았다”는 수정이 필요하다. **Origin·Seed별 구성 불균형은 기술적으로 확인됐다. 그 구성에서 독립된 효과와 인과 메커니즘은 식별되지 않았다.** STEP7B pooled 값과 STEP8A 공존셀 분석이 직접 근거다.


확인일 2026-11-20 KST. 근거: 보존 STEP4D/5B/5C/6B/7B 보고서·execution manifest 및 checkpoint-level 요약. 신규 공식 원천확인·금융실험은 수행하지 않았다.
