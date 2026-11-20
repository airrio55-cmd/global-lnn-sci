# STEP8A ENSEMBLE_DATA_GATES

이번 단계는 저장 결과·checkpoint-level τ 요약의 읽기 전용 감사와 기술통계/설계다. checkpoint는 byte SHA만 대조하며 역직렬화·forward하지 않았다. NN500·Test500·STEP5C600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED를 보존한다. τ 전체 분류는 퇴화24/100, 유효 퇴화23개/사용23개, 비퇴화76/76, 전체99/100이다. 기존 확률 exact99개를 유지하고 중단1개를 재시도·대체·0채움하지 않았다. 신규 NN/기준모형 학습·checkpoint load/forward·Test 재생성·HMM fit/refilter·τ추가계측·금융bootstrap/Holm/p값·Ensemble·GPU·2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, historical18KST available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. O1~O4 Test와 후속 Validation의 역사적 중복 및 Origin/Seed/뉴런/window 의존성을 유지한다.

원형 RAW5=[Log_Ret,Foreign_Net,Nasdaq,SOX,Disparity], LOG2=[Log_Ret,Disparity]. 기존 F1 LTC는두피처 단일채널 별도 사양이며 RAW5/LOG2 Ensemble 재현이 아니다. 채널별 seed offset과 0.5:0.5/Hybrid 계약은 원형 비교 사양으로 별도 동결해야 하며 이번에는 학습/추론하지 않는다.

|입력/항목|기존 증거|미해결/판정|
|---|---|---|
|Foreign_Net|원본 파일/hash/날짜 확인; foreign_net_provenance.json|시장범위·현물/선물·금액/수량·단위·부호·집계주체·공급기관·잠정/확정·개정·최초게시/입수시각 UNKNOWN; 당일사용금지/BLOCKED|
|NASDAQ/SOX|STEP2.5 공식 미국2021~25달력·DST·early close 증거|시장마감과 공급처CSV available_at은 다름;2010~20공식전체세션/earlyclose·지수확정규칙·공급처latency/max_age 미확정. PIT PARTIAL/BLOCKED|
|한국18KST|시점계약은 있으나 공급처증거부족|같은날join/무조건shift1로 인증하지 않음; verified available_at≤decision time인 가장최근값만 허용|
|휴장/결측|KRX공식3939세션 확인|bfill금지;ffill도source와최대age를 사전고정할 때만 가능; 미확인은0채움/임의대체하지 않음|
|A/B종가|A원본+45보완/B전체Excel 별도후보와파일SHA|실제공급처·추출·수정정책·18시 historical가용성 UNKNOWN; BOTH_UNVERIFIED; 주가격 PENDING|
|파생/채널 lineage|F1은각후보에서Train-only scaler와동결입력 유지|원형5피처전체의완전한PIT lineage는미확정; processed_regression_data는출처검증전기본입력제외|

기존 provenance를 재검토했을 뿐 새 공식 출처 증거를 얻었다고 주장하지 않는다. KRX https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd 와 Nasdaq https://www.nasdaqtrader.com/Trader.aspx?id=Calendar 는 공식 확인 경로이며 첨부 CSV의 공급처 증명은 아니다. 원천 불명이라는 이유로 새 데이터로 바꾸지 않는다. Production-PIT BLOCKED와 원형Ensemble 실행 BLOCKED를 유지한다.

확인일 2026-11-20 KST. 근거: 보존 STEP4D/5B/5C/6B/7B 보고서·execution manifest 및 checkpoint-level 요약. 신규 공식 원천확인·금융실험은 수행하지 않았다.

시차 계약: 미국 정규장16:00 America/New_York는 한국에서 표준시 다음날06:00, DST 다음날05:00이다. 조기폐장은 실제세션별 종료시각으로 따로 환산해야 한다. 이 환산은 장 종료시간이며 NASDAQ/SOX 최종 지수 확정·공급처 CSV 게시시각이 아니다. 시장 종료시각을 latency=0인 available_at으로 대입하지 않는다. 한국18시 예측에는 실제 게시/입수시각≤의사결정시각이 확인된 가장 최근 미국 세션만 허용한다.
