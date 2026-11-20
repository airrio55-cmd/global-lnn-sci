# STEP6B_HMM_SELECTION_AUDIT_KO

회고적 HMM 상태 분해와 고정 Test 예측의 기술적 분석이다. HMM 후보 실제fit100/100, 적격100, 부적격0, 실패0, 최종선택/순차filtering10/10, 연결한 기존신경망Test500/500이다. HMM은 새 신경망이 아니며 기존NN500fit에 더하지 않는다. 신경망학습·재추론/checkpoint forward,새금융bootstrap/Holm/p값,RAW5·LOG2 Ensemble,GPU,τactual,2026사용은모두0이다.

동결된GaussianHMM2/full/n_iter2000/tol1e-4/min_covar1e-4,Vol_Regime만관측했다. 각코호트의purge후유지된Train기준일만HMM전용StandardScaler.fit과model.fit에썼다. NN입력window합집합이나F1 scaler를대신쓰지않았다. 100후보의seed는고정10개목록에서각코호트공통으로사용했다.

적격조건: finite final Train model.score LL,finite파라미터/전이·초기확률,공분산양의정부호,Train forward hard-state두개,고정data/source/environment/seed 증거. 수렴은monitor_converged=true와유한history≥2,0≤마지막LL증분<1e-4를동시에요구했다. maxiter도달이나음의증분을수렴으로바꾸지않았다.

모든후보를기록한뒤TrainLL최댓값/정확한동률시작은seed로1개선택했다. 10개선택과명명을모두먼저동결한후에만Validation/Test가격을읽었다. 최종rawTrain경험적상태평균이낮은상태Low,높은상태High다. 표준화emissionmean과원단위경험적평균은private기록에서분리했다. Test성능·occupancy·확률·Target은선택입력0이다.

금융 후보별동일seed 재적합은예산을100초과시키므로하지않았다. 실행환경/seed/Train/scaler/source SHA및동결합성재현시험PASS를연결했다. 실제금융반복적합을완료했다고주장하지않는다. 후보가부적격이거나코호트적격0이면BLOCKED하고새seed/상태수/tol완화/수동레짐대체를하지않는경로를유지했다. 이번에는그러한코호트0개다.

A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING을 유지한다. O1~O4 Test의 후속 Validation 노출 한계를 인정하며 이 결과를 전향적 미관측시장/PIT 인증으로 주장하지 않는다.

개별 Train 날짜/행 수/input·scaler·HMM parameter·posterior·Test Target/확률/identity·SHA 매핑은 ignored private에만 보존했다. 공개본은 여러fit/Origin의 집계·구조적 방법·비민감 해시만 포함한다. n/support0/support1의 개별 상세표는 private 감사자료에 있다.
