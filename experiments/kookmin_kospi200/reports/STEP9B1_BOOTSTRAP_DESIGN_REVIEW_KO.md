# STEP9B1 BOOTSTRAP_DESIGN_REVIEW

이번 단계는 통계 설계·방법론 감사·독립 합성 검증뿐이다. 금융 bootstrap/예측배열 재표집/p값/CI/fit/forward/Test재계산/HMM/τ/Ensemble/GPU/2026관측 사용은 모두0이다. 기존 NN500/Test500·baseline40/LR10·통계600·HMM100/최종10·τ99 PASS/1 BLOCKED·원STEP8B BLOCKED40과master flags=false를보존했다. 기존STEP9A초안은DRAFT/NOT_APPROVED/FAMILIES_NOT_FROZEN인그대로이며새9B1사양만별도동결했다. 이미본Test에대한향후검정은retrospective exploratory analysis이고prospective preregistration/독립확증이아니다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_atUNKNOWN,production-PIT BLOCKED와역사적Test노출한계는유지한다.

|방법|장점|제약·적격성|
|---|---|---|
|Noncircular MBB|실제순서의연속블록,시작끝인공접합없음|끝단선택확률불균등·stationarity/weak dependence가정,고정블록이긴지속성/구조변화에부적절|
|Calendar-aware common blocks|공식session gap을검사하고연말을자동절단하지않음|통계방법을보증하는별도기법이아니라MBB정렬제약. gap있으면BLOCKED|
|Circular|관측별포함빈도균형|Test끝과시작을허위연결,경제구조전환에서왜곡;미선택|
|Stationary/tapered/local blocks 등|가변길이/끝단/비정상성문제를검토할수있음|튜닝과추가가정필요,유리한p를보고선택금지|
|Dependent multiplier/HAC 계열|smooth estimand의의존강건대안|BA/F1비선형·threshold/rare class·5Origin자료에적절한유도와전문검토필요|

현재후보는공식session 연속성을검사한noncircular common-block stream이다. 블록은Origin/연말을넘을수있고원label_end를그대로참조한다. 연말t와t+1의20세션정답은19세션을공유한다. 원블록안에서는이를보존하지만서로다른재표집블록접합에서모든겹침의존성을정확히보존하는것은아니다. 블록20/40/60은세민감도이며금융결과에따라대표블록을고르지않는다.

제안미래실행은블록당10000 **attempted** common draw,PCG64 SeedSequence[20261120,block],chunk100이다. 동일draw는모든쌍/가격/Seed와두가족에서공유한다. 가족별공통validmask(5Origin모두있고실제두클래스/유한metric)를사용하며무효>10% 또는valid<9000이면가족BLOCKED. draw를채워유리한분포가될때까지반복하지않고무효분모를보고한다. 예측만단일클래스는양실제클래스가있으면적격이다.

비정상성/구조변화에서는전역block혼합자체가반사실시계열을만들수있다. 합성ρ.95에서Type I가크게증가하고rare class에서대부분dataset이무효조건을넘었다. 따라서기술적구현PASS를금융통계적적격성PASS로바꾸지않으며현재후보는전문설계검토가필요하다.

확인일:2026-11-20 KST. 합성결과는실제금융결과가아니다.
