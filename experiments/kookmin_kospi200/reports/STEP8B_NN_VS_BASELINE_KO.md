# STEP8B NN_VS_BASELINE

이번 결과는 **실제 기준모형 평가 전 BLOCKED**다. 동결40개 단위 모두 입력 재읽기에서 차단됐으며 완료0/BLOCKED40, Logistic fit0/10, Climatology 추정0, 규칙 평가0이다. 성능값을0으로 만들지 않고 null/NOT_EVALUATED로 유지한다. 기존 NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED와 이전9678파일을 보존한다. NN 재학습/checkpoint load/forward, HMM fit/refilter, τ추가계측, 금융bootstrap/Holm/p값, Ensemble/GPU/2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED. 회고적 비교 승인과 실시간 인증은 구분하며 O1~O4 Test와 후속Validation의 역사적 중복/Origin·Seed·중첩label 의존성을 유지한다.

기존NN저장성능만읽기전용재사용했다. 각Origin에서모델별10Seed동일가중평균→후보별5Origin동일가중평균이다. Seed를시장날짜복제로세지않는다. 아래값은기존STEP5B의참조값이며새NN평가가아니다. baseline성능이없어NN−baseline차이,순위,우월성,퇴화LTC와Climatology의실질비교를계산하지않았다.

|가격|기존NN|BA|MacroF1|Brier|Recall0|Recall1|
|---|---|---:|---:|---:|---:|---:|
|A|RNN|0.518397|0.444842|0.251472|0.371868|0.664927|
|A|LSTM|0.518008|0.469951|0.248489|0.329706|0.706311|
|A|GRU|0.527844|0.477904|0.252249|0.396606|0.659083|
|A|LTC|0.532387|0.452154|0.250427|0.462540|0.602233|
|A|CfC|0.532112|0.486833|0.246920|0.392810|0.671414|
|B|RNN|0.520134|0.448191|0.251259|0.369054|0.671214|
|B|LSTM|0.519534|0.473133|0.249889|0.370416|0.668652|
|B|GRU|0.527896|0.475803|0.251875|0.390023|0.665769|
|B|LTC|0.531292|0.453225|0.250228|0.448740|0.613843|
|B|CfC|0.518918|0.474423|0.251535|0.345741|0.692095|


확인일:2026-11-20 KST. 근거:동결STEP5B/5C/6B/7B/8A보고서와저장manifest·이번실패ledger. 새공식가격/PIT증빙을확보했다고주장하지않는다.
