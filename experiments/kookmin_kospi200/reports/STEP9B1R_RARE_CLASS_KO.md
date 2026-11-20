# STEP9B1R RARE_CLASS

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

|DGP|방법|유효dataset/전체|Type I/Power(조건부)|coverage(조건부)|bias(정의가능전체)|평균CI폭|
|---|---|---:|---:|---:|---:|---:|
|rare03_null|MBB40|113/500|0.0796|0.9292|-0.0013|0.2126|
|rare03_null|STATIONARY40|23/500|0.0870|0.9130|-0.0013|0.2042|
|rare03_null|STATIONARY120|0/500|null/NOT_EVALUABLE|null/NOT_EVALUABLE|-0.0013|null/NOT_EVALUABLE|
|rare03_null|LOCAL40_W100|326/500|0.1135|0.8926|-0.0013|0.1960|
|rare03_null|HAC120|0/500|null/NOT_EVALUABLE|null/NOT_EVALUABLE|-0.0013|null/NOT_EVALUABLE|
|rare03_null|MULTIPLIER120|0/500|null/NOT_EVALUABLE|null/NOT_EVALUABLE|-0.0013|null/NOT_EVALUABLE|
|rare10_null|MBB40|80/80|0.0875|0.9125|0.0037|0.1650|
|rare10_null|STATIONARY40|80/80|0.0750|0.9250|0.0037|0.1706|
|rare10_null|STATIONARY120|0/80|null/NOT_EVALUABLE|null/NOT_EVALUABLE|0.0037|null/NOT_EVALUABLE|
|rare10_null|LOCAL40_W100|80/80|0.1625|0.8500|0.0037|0.1454|
|rare10_null|HAC120|80/80|0.2875|0.7125|0.0037|0.1159|
|rare10_null|MULTIPLIER120|80/80|0.2375|0.7125|0.0037|0.1151|
|Origin_support_imbalance_null|MBB40|59/80|0.0169|0.9831|0.0008|0.1800|
|Origin_support_imbalance_null|STATIONARY40|53/80|0.0000|1.0000|0.0008|0.1796|
|Origin_support_imbalance_null|STATIONARY120|0/80|null/NOT_EVALUABLE|null/NOT_EVALUABLE|0.0008|null/NOT_EVALUABLE|
|Origin_support_imbalance_null|LOCAL40_W100|72/80|0.0417|0.9444|0.0008|0.1611|
|Origin_support_imbalance_null|HAC120|0/80|null/NOT_EVALUABLE|null/NOT_EVALUABLE|0.0008|null/NOT_EVALUABLE|
|Origin_support_imbalance_null|MULTIPLIER120|0/80|null/NOT_EVALUABLE|null/NOT_EVALUABLE|0.0008|null/NOT_EVALUABLE|


원BA/F1정의를유지했고실제한클래스/누락Origin은무효이며null을0으로바꾸지않았다. 예측만한클래스이면원metric은계산가능하나IF분산이0등추론실패는따로BLOCKED한다. 공통drawmask에서무효10%초과시dataset/가족BLOCKED;관측지원도10미만인HAC/multiplier도사전제약으로BLOCKED했다. 이는희소문제를해결한것이아니라실행불가능범위를노출한것이다.

class-stratified 재표집이나희소class를강제로추가하는방식은사용하지않았다. validdraw가충분해질때까지재추출하지않았고정해진499시도만평가했다. 관측estimand 자체가정의안된경우NOT_IDENTIFIABLE,정의돼도추론이불안정하면BLOCKED다. 제외후TypeI/Power/coverage는조건부결과이며정의가능전체bias와eligible-only bias를구분했다. 작은eligible분모에서0오류/100%coverage를유효성증거로쓰지않는다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
