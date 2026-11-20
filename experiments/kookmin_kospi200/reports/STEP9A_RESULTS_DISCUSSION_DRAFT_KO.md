# STEP9A Results / Discussion 본문 초안

아래 문단은 보존된 결과만으로 작성한 초안이다. 괄호의 C01~C09는 `step9a_evidence_traceability.json`의 실제 보고서와 결과 필드에 연결된다. 신규 금융 fit, forward, 성능 재계산 또는 p값 계산은 수행하지 않았다.

## Results 초안

본 연구는 KOSPI200의 F1 입력(Log_Ret, Disparity)을 사용하는 다섯 신경망을 두 가격 후보, 다섯 Rolling Origin, 열 개 Seed로 평가하였다. 기준모형은 Train climatology, Logistic regression, 200DMA 및 Momentum60이다. 신경망은 각 Origin에서 Seed별 성능을 동일 가중 평균한 뒤 다섯 Origin을 동일 가중 평균하였고, 기준모형은 각 Origin의 단일 결과를 평균하였다. 표의 모든 수치는 기존 저장 결과에서 직접 인용하였다.

이번 고정 설정의 후보별 평균 BA에서 모든 신경망은 Momentum60의 0.504416보다 높은 값을 보였다. 그러나 기간별 방향은 일치하지 않았다. 예를 들어 RNN은 두 가격 후보 모두 Momentum60보다 BA가 높은 Origin이 다섯 개 중 두 개였지만, 전체 Origin 평균은 더 높았다. 또한 Momentum60의 평균 Macro F1은 0.491019로 모든 신경망 평균보다 높았다. 따라서 평균 BA의 차이를 모든 기간과 지표에 걸친 우월성으로 확대하지 않았다. 규칙형 0/1 신호와 확률예측의 Brier는 예측값의 성격이 다르므로 함께 설명하였다(C01, C07).

기존 신경망 간 검정에서는 Primary BA 20가설과 Origin BA 100가설의 각 블록 길이(20, 40, 60)에서 Holm 보정 후 기각이 없었다. 이는 BA 우수성을 입증하지 못했다는 결과이며, 동등성이나 효과 부재를 증명하지 않는다. Secondary에서는 가격 A의 LSTM−LTC Recall1 차이 등 반대 증거가 남아 있다. Baseline 비교에는 새로운 금융 유의성 검정을 수행하지 않았으므로, 해당 비교는 기술통계로 구분하였다(C02, C03).

LTC는 전체 Test 100개 모델 결과 중 24개에서 단일클래스 예측을 보였다. 이들 24개는 동일 코호트의 Climatology와 BA=0.5로 같았지만, Macro F1과 Brier까지 모두 같지는 않았다. 단일클래스 예측은 NaN 또는 수치 발산과 별도의 진단으로 기록하였다. 같은 날짜를 예측하는 Seed의 반복을 독립된 시장 관측으로 세지 않았다(C04, C08).

시간상수 계측은 100개 중 99개에서 유효하였으며, 프로세스 중단 1개는 BLOCKED로 유지하였다. 유효한 퇴화 23개의 effective τ 중앙값 평균은 약 0.0291, 비퇴화 76개는 약 0.0490이었다. Origin×가격 공존 셀 일곱 개에서도 모두 같은 기술적 방향이 관측되었다. 다만 O3의 작은 표본, O5의 비교군 부재, 누락과 구성 불균형 때문에 전체 자료의 구성 독립 효과는 식별되지 않았다(C05).

수동 레짐과 HMM 레짐은 별도로 해석하였다. 수동 임계값과 HMM 적합·상태 명칭은 Train 자료로 고정되었고, HMM의 후속 상태는 forward filtering으로 얻었다. 일부 Low 레짐은 실제 Target이 한 클래스여서 BA와 Macro F1이 null이었다. 이에 따라 점유율, class support와 유효 모델 수를 함께 보존하고, High/Low 평균을 동일한 표본 구성의 비교로 취급하지 않았다(C06).

## Discussion 초안

평균 BA의 추가 관측과 기간·지표별 불일관성은 복잡한 모델의 가치를 하나의 순위로 요약하기 어렵다는 점을 보여준다. 본 연구의 기여는 학습 횟수 자체보다 예측 성능, Seed·시기별 안정성, 레짐별 유효 표본과 내부 동역학을 하나의 고정 평가체계로 연결한 구조에 있다. 단순 기준모형이 더 나은 결과나 실패·누락도 유지함으로써, 유리한 모델·가격·기간만을 선택하는 해석을 피하였다.

낮은 effective τ는 퇴화와 함께 관측된 conductance 기반 내부 진단량이다. 이 값은 입력과 은닉상태, 학습된 파라미터 및 Origin·Seed 구성의 영향을 함께 받는다. 저장 요약만으로 감각·순환 conductance의 개별 기여나 인과 경로를 분리할 수 없다. 단위 역시 model_observation_step이며 실제 영업일, 경제적 기억길이 또는 Jacobian 고유시간과 동일하지 않다(C05).

A/B 가격의 실제 공급처, 개정 이력과 과거 18:00 KST 가용성은 여전히 미확정이다. O1~O4 Test 기간은 후속 Origin의 Validation에 역사적으로 노출되었고, Seed와 중첩 Target도 독립적인 시장 복제가 아니다. NN, Logistic, 200DMA와 Momentum60의 정보 표현과 과거 이력 길이도 다르다. 따라서 이 비교는 모델 복잡도만 분리한 완전 통제 실험이나 전향적 미관측 시장 검증이 아니다.

원형 RAW5/LOG2 Ensemble과 Journal of Forecasting V16의 5개국 시장 연구 결과는 이번 F1 KOSPI200 실험과 분리한다. Production-PIT는 BLOCKED이며 실거래 수익성, 원형 Ensemble의 재현 또는 통계적 모델 우월성을 인증하지 않는다. 향후 baseline 검정을 하더라도 이미 확인한 Test에 대한 독립된 탐색 분석으로 명시해야 하며, 진정한 prospective preregistration으로 부를 수 없다(C09).

확인일: 2026-11-20 KST. 신규 금융 실험과 추가 금융 통계검정은 0이며, 실제 STEP9B는 자동 시작하지 않는다.
