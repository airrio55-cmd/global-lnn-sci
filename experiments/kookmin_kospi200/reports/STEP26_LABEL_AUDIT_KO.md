# STEP2.6 레이블·피처 감사

기간은2010-01-01~2025-12-31이다. 원본에서 기간을 먼저 필터링했으며2026년 가격을 입력·타깃 확인에 사용하지 않았다. 아래 결과는 사용자 제공 종가의 수치·거래일 정합성 수준이며 공식 원천이나 PIT 인증은 아니다.

## 20세션 레이블

공식 KRX session_id 순서로 `label_end_id = session_id + 20`을 사용했다. `Target = int(Close[t+20] > Close[t])`이며 미래 종가가 없으면 UNKNOWN이다. known label은 **3919개**, 마지막20개는 UNKNOWN이다. 미확정 기준일은2025-12-02~12-30, 마지막 유효 기준일은2025-12-01이며 endpoint는2025-12-30이다.

`data/derived/kospi200_targets_20sessions_2010_2025.csv`에는 Target, label_end, 양쪽 session_id, 기준일·endpoint의 source SHA-256을 기록했다. known 상태도 USER_SUPPLIED_LABEL_KNOWN으로 표시했다. UNKNOWN을0으로 바꾸지 않았고2026년 자료로 보완하지 않았다.

기존 ‘20관측행 뒤’와 실제20세션의 날짜 차이 **664건**은 새 타깃의 session_id 차이 검사에서 **0건**이 됐다. 예전 날짜가 올바르게 바뀌었다는 뜻이 아니라, 새 타깃에서 관측행 기준 horizon을 폐기했다는 뜻이다.

## Historical Baseline 보호 및 비교

과거 논문 결과·원본 노트북·성능표·McNemar·HMM 분포는 그대로 보존했다. 이번 비교 reference는2025-12-31로 먼저 자른 기존3894행에서만 다시 계산했다. 2026년 종가를 참조하는 과거 실행을 재현한 결과가 아니다.

| 항목 | cutoff 원본 관측행 reference | 보완 후 실제 KRX20세션 |
|---|---:|---:|
| known label |3874|3919|
| 상승 |2156|2182|
| 하락·동률 |1718|1737|
| 상승 비율 |55.6531%|55.6775%|
| UNKNOWN |20|20|

공통known3874개에서 Target **47개**가 달라졌다. 0→1은21개, 1→0은26개다. 보완45개 기준일도 새로 추가됐으므로 전체 클래스 분포의 차이를 동일 표본 모델 성능 변화로 해석하지 않는다. 원본 버그를 그대로 따른 별도 감사 reference는 마지막20개를 잘못0으로 만들어0이1738개/1이2156개지만, 이를 새 Target으로 사용하지 않았다.

일별 old/new Target 비교는 로컬 `historical_baseline_label_comparison_private.csv`에 보존했다. 공개 `step26_historical_horizon_audit.csv`에는 날짜·horizon 차이만 두고 전체 일별 클래스를 재배포하지 않았다. 새 Balanced Accuracy·Macro F1·F1·McNemar p값은 생성하지 않았다.

## 기술적 피처와 window

계산식은 원래 노트북과 같다.

- Log_Ret = ln(C / C.shift(1))
- Disparity = C / C.rolling(20).mean() - 1
- Vol_Regime = Log_Ret.rolling(40).std(ddof=1)

식은 바꾸지 않았고 보완된 달력·가격 때문에 값과 적격 날짜가 달라졌다. bfill, 가격 ffill, 결측 자동0 치환은 사용하지 않았다. 초기40개 warm-up 제외 후 feature-ready3899개, known label까지3879개, t포함20입력 window까지 요구하면 **3860개**다. 신규 window는 t-19..t이며 원본 t-20..t-1과 구분한다. 외국인·NASDAQ·SOX는 결합하지 않았다.

같은 원본 날짜에서 기존 관측행 피처와 1e-12보다 큰 값 차이가 나는 수는 Log_Ret42개, Disparity638개, Vol_Regime1073개다. exact 차이와 수치 허용오차 차이는 JSON에 따로 기록했다. 매우 작은 rolling 부동소수점 차이를 모두 실질적 변화로 세지 않았다.

피처는 cutoff 뒤 가격을 바꿔도 cutoff까지 불변임을 검사했다. 타깃은 **label_end<=cutoff인 성숙 레이블**에 대해 cutoff 뒤 가격 변경 불변성을 검사했다. horizon 안의 미래 종가를 바꾸면 과거 기준일의 Target이 바뀌는 것이 정의상 정상이다. 이 경우까지 불변이라고 주장하지 않았다.

## 전체 Excel 수령 후 재검증 (2026-11-16)

전체 Excel 3939세션과 보완45일을 확인했고 공통3894일 가격을 대조했다. 기존 가격은 교체하지 않았으므로 종가·Target·피처 파생파일 및 본문의 국내 구조 표본 수는 그대로다. exact 차이3750건(소수2자리 차이2건)은 가격 대조 보고서에 기록했고 원천 판정은 BLOCKED다. 마지막20세션 UNKNOWN, 2026년 사용0, 외부5피처 PIT 및 STEP3 실행 BLOCKED를 유지한다. 학습이나 새로운 성능·p값 산출은 없었다.
