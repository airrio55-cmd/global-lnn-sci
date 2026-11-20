# STEP9B1R STRUCTURAL_BREAK

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

|DGP|방법|유효dataset/전체|Type I/Power(조건부)|coverage(조건부)|bias(정의가능전체)|평균CI폭|
|---|---|---:|---:|---:|---:|---:|
|shared_break_null|MBB40|499/500|0.0982|0.8918|0.0002|0.1315|
|shared_break_null|STATIONARY40|497/500|0.0865|0.9095|0.0002|0.1360|
|shared_break_null|LOCAL40_W100|500/500|0.1340|0.8520|0.0002|0.1153|
|shared_break_null|HAC120|500/500|0.2480|0.7520|0.0002|0.0879|
|crossing_break_null|MBB40|80/80|0.0000|1.0000|-0.0007|0.1471|
|crossing_break_null|STATIONARY40|80/80|0.0000|1.0000|-0.0007|0.1589|
|crossing_break_null|LOCAL40_W100|80/80|0.0000|1.0000|-0.0007|0.1284|
|crossing_break_null|HAC120|80/80|0.0000|1.0000|-0.0007|0.1582|
|prevalence_shift_null|MBB40|80/80|0.0875|0.9125|0.0004|0.1612|
|prevalence_shift_null|STATIONARY40|80/80|0.1000|0.9000|0.0004|0.1665|
|prevalence_shift_null|LOCAL40_W100|80/80|0.1250|0.8500|0.0004|0.1408|
|prevalence_shift_null|HAC120|80/80|0.2375|0.7625|0.0004|0.1105|
|advantage_reversal_null|MBB40|80/80|0.0625|0.8875|-0.0014|0.0622|
|advantage_reversal_null|STATIONARY40|80/80|0.0250|0.9625|-0.0014|0.0680|
|advantage_reversal_null|LOCAL40_W100|80/80|0.1000|0.8750|-0.0014|0.0554|
|advantage_reversal_null|HAC120|80/80|0.2750|0.7250|-0.0014|0.0440|
|unequal_Origin_sizes_null|MBB40|29/80|0.1034|0.8966|0.0006|0.1466|
|unequal_Origin_sizes_null|STATIONARY40|46/80|0.0652|0.9348|0.0006|0.1595|
|unequal_Origin_sizes_null|LOCAL40_W100|73/80|0.1370|0.7808|0.0006|0.1339|
|unequal_Origin_sizes_null|HAC120|78/80|0.3333|0.6667|0.0006|0.0898|


공유성능break,모델별우위교차,클래스비율급변,시점/Origin별우위역전을분리해구성했다. 전역bootstrap은서로다른시기법칙을섞을수있고교차break에서지나친보수성/coverage1도관측됐다. local창은분포변화를조건화하는추가가정이며동일한관측metric을계산해도원5Origin효과의반복표집법칙과동일하다는보장은없다. 원membership과5Origin가중은유지했지만sampling-law의동등성은미검증이다. 달력/Origin정렬과통계적타당성은별개다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
