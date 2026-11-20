# STEP8B ORIGIN_SENSITIVITY

이번 결과는 **실제 기준모형 평가 전 BLOCKED**다. 동결40개 단위 모두 입력 재읽기에서 차단됐으며 완료0/BLOCKED40, Logistic fit0/10, Climatology 추정0, 규칙 평가0이다. 성능값을0으로 만들지 않고 null/NOT_EVALUATED로 유지한다. 기존 NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED와 이전9678파일을 보존한다. NN 재학습/checkpoint load/forward, HMM fit/refilter, τ추가계측, 금융bootstrap/Holm/p값, Ensemble/GPU/2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED. 회고적 비교 승인과 실시간 인증은 구분하며 O1~O4 Test와 후속Validation의 역사적 중복/Origin·Seed·중첩label 의존성을 유지한다.

O1~O5×A/B의 각4기준모형은 모두BLOCKED다. Origin/가격을제외하거나대체하지않았다. 각코호트warmup과기존NNTest표본alignment는확인했지만기준모형성능이없으므로Origin별상대성능/A-B수치민감도/BA·MacroF1·Brier방향일관성은NOT_EVALUATED다. Validation-Test차이도새baseline평가가없어산출하지않으며다른정책/기간지표를섞지않는다. 공개표는여러Origin집계만담고개별baseline1개결과/일별자료는공개하지않는다.

확인일:2026-11-20 KST. 근거:동결STEP5B/5C/6B/7B/8A보고서와저장manifest·이번실패ledger. 새공식가격/PIT증빙을확보했다고주장하지않는다.
