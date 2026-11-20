# STEP6A_HMM_MASTER_PROTOCOL_KO

STEP6A는 설계·동결·정적 감사·합성 시험 단계다. 실제 금융 HMM fit/filtering, 신경망 학습·재학습, Test 재추론, checkpoint load/forward, 금융 p값·bootstrap 재실행, RAW5/LOG2 Ensemble, LTC τactual, GPU 및2026가격 사용은 모두0이다. HMM100후보/최종10개는 계획이며 학습 완료가 아니다. hmm_fit_enabled=false/hmm_filtering_enabled=false를 유지한다.

GaussianHMM, n_components2/covariance_type full/n_iter2000/tol1e-4/min_covar1e-4. hmmlearn0.3.3를 고정한다. 관측은 **Vol_Regime=Log_Ret.rolling(40).std(ddof=1) 한 변수**뿐이다. 미래 종가·Target·신경망 확률·다른 수익률을 관측에 추가하지 않는다. STEP3C의 HMM 설정과 일치함을 검사했고, STEP5C BA/Secondary 결과를 설정 선택에 사용하지 않았다.

5 Origin×A/B×HMM 초기화Seed[2,12,22,32,42,52,62,72,82,92]=100후보. Origin/Candidate마다 적격후보 중1개만 선택해 최종10개다. 신경망 Seed와 HMM 초기화Seed는 목적과 ledger를 분리한다. HMM fit을 기존500개 신경망 fit에 더하지 않는다.

기존 purging 후 유지된 **Train 기준일**만 HMM scaler.fit/HMM.fit/후보선택에 사용한다. 신경망의20일 입력window 날짜합집합과 구분하고, F1용 scaler를 HMM에 재사용하지 않는다. HMM용 별도 StandardScaler를 해당 Train의 Vol_Regime만으로 fit한다. Validation/Test는 transform과 forward filtering만 허용한다. 이번에는 실제 금융 Vol_Regime/scaler 수치를 열거나 생성하지 않았다.

상세 Train 기준일·코호트별 행 수·세션별 bridge/filtering 경로는 비공개 로컬 계획에 보존한다. 공개본에는 해당 매핑이나 코호트별 수치를 싣지 않는다.

A/B의 Train 날짜 수·경계는 같지만 관측값과 scaler/HMM은 독립이다. 전체 일별 날짜·session ID 연결은 로컬 private plan에 보존한다. 실제 금융 입력 SHA는 STEP6B 승인 후 데이터빌더 검사로만 확정한다.

상태는 Train hard-forward-filter로 배정된 원단위 Vol_Regime의 상태별 경험평균 순서로 Low_Vol/High_Vol을 명명한다. 표준화 emission means를 역변환한 값과 경험적 상태평균을 구분해 후속 감사에 기록하며, 명명은 경험적 Train 상태평균 기준이다. 평균이 정확히 같으면 경제적 순서가 모호하므로 BLOCKED다.

상세 금융 input/date/checkpoint/identity 매핑과 비공개 SHA 관계는 로컬 ignored 경로에만 보존한다. 공개본은 코드·구조적 계약·합성 결과·집계·비민감 해시만 포함한다.
