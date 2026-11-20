# STEP10 박사논문 Results / Discussion 한국어 초안

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 장 | 핵심 내용 | 연구질문 |
| --- | --- | --- |
| 제1장 서론 | 연구문제·기여 범위·반대 증거를 포함한 동기 | RQ1~5 |
| 제2장 이론·선행연구 | 재귀 NN/LTC/CfC·baseline·시간상수·의존적 추론의 한계 | RQ1~5 |
| 제3장 데이터와 재현성 | 가격 A/B·세션·정보시점·실패/복구 lineage | 전 RQ |
| 제4장 연구설계·통계방법 | F1·Rolling-Origin·purging·평가·기존 근사추론 | RQ1/RQ5 |
| 제5장 신경망·Baseline 성능 | 동결 성능표와 지표·Origin 반대 증거 | RQ1/RQ5 |
| 제6장 Seed/Origin 안정성 | 단일클래스 퇴화·checkpoint 선택·비독립 반복 | RQ2 |
| 제7장 수동/HMM 레짐 | 점유율·support·null·구성 차이 | RQ3 |
| 제8장 LTC τ 분석 | 99+1 보완100·conductance·탐색연관·억제 | RQ4 |
| 제9장 종합논의·한계 | 추론 미검증·가격/PIT·역사적 노출·정보이력 | 전 RQ |
| 제10장 결론 | 근거에 맞춘 기여·집필 및 후속 증빙 조건 | 전 RQ |


## 제5장 신경망 및 단순 기준모형의 회고적 Test 성능

### 5.1 연구 범위와 평균 성능

본 연구는 KOSPI200의 F1 국내 두 피처(Log_Ret, Disparity)를 사용한 회고적 Rolling-Origin 분석이다. 다섯 신경망에 대해 5개 Origin, 10개 Seed, 2개 가격후보를 조합한 500개 학습 결과와 동결된 500개 Test 평가를 사용하였다. 네 기준모형은 각 Origin과 가격후보에서 한 번씩 평가하여 총40개 결과를 구성하였다. 신경망 지표는 Origin 안에서10Seed 평균을 먼저 계산하고 다섯 Origin을 동일가중하는 기존 요약을 그대로 인용하였다. 이는 Seed를 독립 시장 관측으로 풀링한 성능이 아니다[Table3~5; STEP8BR candidate_primary].

평균 BA에서 LTC는 가격A0.532387, 가격B0.531292로 관측되었다. 그러나 이 순위를 모든 성능 기준의 우월성으로 해석할 수 없다. Momentum60의 평균 Macro F1은 두 가격후보에서0.491019로 모든 신경망의 평균보다 높았다. Brier가 가장 낮은 신경망도 가격A에서는 CfC(0.246920), 가격B에서는 LSTM(0.249889)으로 달랐다. 따라서 평균 BA, Macro F1, 확률오차는 서로 다른 관점을 제공하며, 어느 하나의 유리한 지표로 모델이나 가격후보를 선택하지 않았다[STEP8BR_NN_VS_BASELINE; STEP10_FROZEN_RESULT_TABLES].

### 5.2 Origin별 반대 증거와 정보이력의 차이

모든 신경망의5Origin 평균 BA는 Momentum60의0.504416보다 높았지만, Origin별 우열은 일관되지 않았다. Momentum60 대비 RNN의 BA가 높은 Origin은 두 가격후보 모두2/5였다. 이 사례는 평균 차이를 모든 시기에서의 우월성으로 일반화할 수 없음을 보여준다. LTC의 전체 Test 단일클래스 예측24개는 동일 코호트 Climatology와 BA가 모두0.5로 같았으나, F1과 Brier까지 모두 같지는 않았다. 부정적 결과를 삭제하지 않고 모델의 추가적 정보가 지표에 따라 달랐다는 반대 증거로 포함하였다[STEP8BR_NN_VS_BASELINE; STEP9A_BASELINE_INTERPRETATION].

평가일과 목표 정의는 맞추었지만 정보이력은 동일하지 않다. 신경망은20시점 F1 window, Logistic은 현재 시점의 F1, DMA200과 Momentum60은 각각 더 긴 종가 이력과 간격 정보를 사용한다. 그러므로 본 비교는 동일 날짜의 기술적 benchmark이며 모델 복잡도만 분리한 인과적 통제실험이 아니다. 0/1규칙의 Brier와 확률예측의 Brier를 함께 제시하되, 수익성이나 calibration 인증을 주장하지 않았다. 신경망과 baseline 사이의 새로운 금융 통계검정은 실시하지 않았다[STEP8BR_NN_VS_BASELINE].

### 5.3 기존 통계 결과의 제한적 해석

신경망 간 기존 STEP5C의 Primary BA20과 Origin BA100은 블록20·40·60 모두 Holm 유의 결과가0이었다. Secondary80의 유의 결과는 같은 순서로3·2·3이었다. 서로 다른 블록의 같은 가설을 독립 재현으로 해석하지 않았고, 비유의를 동등성이나 무효과의 증거로 바꾸지 않았다. A LSTM−LTC Recall1의 기존 반대 증거도 남아 있어 BA 평균순위만으로 종합 우열을 주장할 수 없다. 새 p값이나 CI는 이 집필 단계에서 생성하지 않았다[STEP5C; STEP10_STATISTICAL_EVIDENCE].

## 제6장 Seed 및 Origin에 따른 안정성

500개 학습과 저장된 Validation/Test 진단은 같은 설정에서도 초기화와 시기에 따라 결과가 달라질 수 있음을 기술적으로 보여준다. LTC는100개 결과 중24개에서 Validation과 Test의 단일클래스 예측이 함께 관찰되었다. LSTM은 Test2개, Validation4개에서 단일클래스 예측을 보였고, RNN·GRU·CfC의 전체 Test 단일클래스 예측은 각각0개였다. 이러한 기록은 특정 모델에 불리한 결과까지 유지한 전수 진단이며, 수치 발산이나 NaN 발생과 같은 의미로 묶지 않았다[STEP5B model_instability].

Seed와 Origin의 변동은 별개로 제시하되, 같은 가격·날짜에 대한 Seed10회는 독립적인 시장 실험10회를 뜻하지 않는다. Validation BA로 checkpoint를 선택했기 때문에 그 Validation 지표도 독립 일반화 성능이 아니다. 저장된 Origin별10Seed 평균·표본표준편차·범위는 기술적 변동성 지표로 사용하고, 금융 신뢰구간이나 인과적 안정성 효과로 해석하지 않았다. 불안정한 Seed를 다른 Seed로 교체하거나 지표가 낮은 Origin을 제외하지 않았다[STEP4D; STEP5B groups; Table6].

## 제7장 수동 변동성 및 HMM 레짐 분석

수동 변동성 레짐은 각 Origin의 유지된 Train 구간에서 정한 Vol_Regime q30/q70으로 Low/Mid/High를 구분하였다. HMM은 Train-only Gaussian2state100개 후보 중10개 모델을 선택하고 Train 기준 상태 이름을 고정한 뒤 forward filtering한 결과를 사용하였다. 두 방식은 상태 수와 정의가 다르므로 별도 표로 유지했다. Test 전체를 이용한 Viterbi 상태나 Test 분위수를 새로 계산하여 유리한 레짐을 구성하지 않았다[STEP6B; Table7a/7b].

HMM의 가격A와B 각각에서5Origin 동일가중 High 점유율은 기존 요약상 약0.753726, Low는0.246274였다. 이 비율은 전체 날짜를 풀링한 점유율이 아니다. Low의 일부 Origin은 실제 Target이 한 클래스뿐이어서 BA와 Macro F1이 정의되지 않았으며, 유효 결과는 모델·가격별40/50으로 High의50/50과 달랐다. 이 때문에 레짐 평균의 차이는 성능뿐 아니라 유효 Origin 및 클래스 구성의 차이를 포함한다. 표에는 저장된 n·클래스 support·유효지표 개수와 null 정책을 동반하고, confidential 세부표의 공개는 별도로 제한한다[STEP6B market_regime_profile_multi_Origin/model_regime_diagnostics].

레짐별 관측 차이는 시장 상태의 인과적 효과를 식별하지 않는다. 작은 Low 레짐, 상태 추정과 종가 시점 증빙의 한계, 중첩 label 및 반복 Seed의 의존성을 함께 고려해야 한다. 모든 레짐을 동일한 보고 원칙으로 유지하고, 성능이 높은 레짐이나 모델을 사후 선택하지 않았다[STEP10_REGIME_INTEGRATION].

## 제8장 LTC 시간상수와 퇴화의 탐색적 관계

LTC 시간상수 분석은 “99개 초기 계측 후 독립 복구로100개 통합을 완성했다”는 이력으로 보고한다. 원 STEP7B의99 PASS/1 BLOCKED 기록은 유지되고, 독립 STEP7B-R의1 PASS가 새 버전의 통합100개를 보완하였다. 기존99개는 다시 계측하지 않았으며, 보완 결과의 기존 확률 exact 재현과 parameter/RNG 보존 기록을 확인하였다. 통합 유효 분모는 퇴화24/24와 비퇴화76/76이다[STEP7BR execution/public summary].

기술적 방향으로 퇴화군의 effective τ가 비퇴화군보다 낮았고, 비교 가능한 Origin×가격8개 셀 모두 같은 방향이었다. 다만 이는 사후 탐색적 연관이다. 군 구성의 불균형, O5의 퇴화군 부재, Seed·Origin과 중첩 window·뉴런·solver substep의 의존성이 남아 있어 구성독립효과나 인과효과는 식별되지 않는다. effective τ의 단위는 model_observation_step이며 경제적 기억길이로 해석하지 않는다[STEP7BR_DEGENERACY_SENSITIVITY].

τ_raw와 effective τ는 구분한다. 전자는 양의 cm와 gleak의 비율이고, 후자는 입력 및 hidden 상태에 따른 sensory·recurrent conductance를 분모에 포함한다. observation-entry와 solver substep 역시 서로 다른 요약 수준이다. 신규100개 정량집계나 이전99개와의 정확한 차이는 복구된 단일 checkpoint의 값을 역산할 수 있으므로 공개하지 않는다. 논문 공개본은 완성 분모와 방향·정의·한계만 제시하며, 저장된 상세 수치표는 confidential 부록으로 별도 관리한다. 과거 STEP8A/STEP9A의99개 집계를100개처럼 바꾸지 않았다[STEP10_LTC_TAU100_INTEGRATION].

## 제9장 종합논의와 한계

본 연구의 결과는 예측 성능, 초기화·시기별 안정성, 레짐별 지표 정의 가능성, LTC 내부 동역학을 함께 평가할 필요성을 보여준다. 평균 BA의 상대적 높음은 Macro F1의 반대 증거, Origin별 불일관성 및 단일클래스 예측과 함께 해석되어야 한다. 이 통합 진단 구조가 기여 후보이며, 500회 학습이라는 실행 규모만을 학문적 독창성으로 주장하지 않는다[STEP10_RQ_CONCLUSION_MATRIX].

통계적 추론에는 별도 한계가 있다. STEP9B1R의 합성 재검토에서9개 설정은 강한 의존성·희소 클래스·구조변화에 대한 핵심 적격성 조건을 모두 충족하지 못했다. 이는 실제 STEP5C p값을 새로 계산하여 무효화한 결과도, 기존 검정을 완전히 인증한 결과도 아니다. 정상성·의존구조·class support·유한표본 근사 및 Monte Carlo 꼬리 정밀도의 타당성이 충분히 입증되지 않았다는 근거다. 기존 p값은 동결된 근사 추론 기록으로 유지하고, NN-baseline 금융 STEP9B2는 METHOD_NOT_VALIDATED/NOT_EXECUTED로 남겨둔다[STEP9B1R; STEP10_STATISTICAL_EVIDENCE].

자료의 출처와 정보시점도 미해결이다. 가격A/B는 BOTH_UNVERIFIED이며 주 분석 가격은 PENDING이다. historical18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 공식 세션과 파일 SHA의 일치는 가격 진실성이나 당시18시의 실시간 가용성을 증명하지 않는다. O1~O4의 historical Test가 후속 Origin Validation으로 이미 노출됐으므로, 이 Test를 완전히 미관측인 전향적 holdout으로 부를 수 없다. 지표에 따라 유리한 가격후보를 선택하는 것도 허용되지 않는다[STEP10_DATA_PIT_GAP_AUDIT].

현재 연구는 F1 국내 두 피처의 회고적 분석이다. Foreign_Net의 범위·단위·공표시각과 NASDAQ/SOX의 공급처 가용시각은 미확정이며, 원형 RAW5/LOG2 Ensemble은 실행·검증되지 않았다. 따라서 현재 F1 결과를 원형 Ensemble 재현이나 실시간 투자수익성의 증거로 확장하지 않는다. JOF 연구의 데이터·표·주장과 본 박사논문 연구를 분리한다[STEP9A_LIMITATIONS_AND_CLAIMS; STEP10_NEXT_GATES].

## 제10장 결론

동결된 회고적 결과에서 신경망의 일부 평균 BA 추가가 관찰되었지만, 지표·Origin·학습 안정성 전반의 일관된 우월성은 입증되지 않았다. 단순 기준모형의 반대 증거와 LTC 단일클래스 퇴화, 레짐의 유효분모 차이, τ의 탐색적 연관을 함께 보존했다. 이러한 관측은 특정 모델이 최고라는 주장보다 모델 진단과 재현성 중심의 증거 체계에 기여한다.

본 논문은 현재의 서술·탐색적 범위를 명시하고 집필을 시작할 수 있다. 다만 최종 학문적 기여와 문장 강도는 지도교수의 검토를 거쳐야 한다. 가격 공급처·개정·과거 가용시각 증빙과 검정방법 타당성은 별도의 미해결 항목으로 남으며, 새로운 금융 실험이나 통계검정을 자동 실행하지 않는다. 향후 수정은 문장 편집과 결과 변경을 구분하고, 결과·설정 변경에는 새 버전과 감사를 요구한다.

위 초안의 수치는 STEP10 동결표와 기존 source pointer로 추적한다. 문헌 관련 단정이나 신규 수치를 만들어 넣지 않았다. 최종 학위논문 공개본에 confidential support/단일 τ 상세가 포함되지 않도록 집필·공개 검토를 분리한다.

