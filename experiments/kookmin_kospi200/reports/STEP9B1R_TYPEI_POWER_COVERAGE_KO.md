# STEP9B1R TYPEI_POWER_COVERAGE

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

오류율/Power와coverage는eligible dataset을분모로한조건부값이며Wilson95구간과MCSE를함께제공한다. 무효dataset을원래전체분모에서숨기지않고eligible비율/원인도같이보고한다. 관측추정량정의불가와추론부적격을구분하고bias_all_defined 및bias_eligible_only를별도로저장했다. HAC에는draw비율을null(해당없음)로두어부트스트랩499회를시도한것처럼세지않았다.

|DGP|방법|유효dataset/전체|Type I/Power(조건부)|coverage(조건부)|bias(정의가능전체)|평균CI폭|
|---|---|---:|---:|---:|---:|---:|
|AR07_delta002|MBB40|80/80|0.0875|0.9500|-0.0036|0.1462|
|AR07_delta002|STATIONARY40|80/80|0.0750|0.9500|-0.0036|0.1509|
|AR07_delta002|LOCAL40_W100|80/80|0.0875|0.8750|-0.0036|0.1298|
|AR07_delta002|HAC120|80/80|0.2625|0.7625|-0.0036|0.0942|
|AR07_delta002|MULTIPLIER120|80/80|0.2625|0.7625|-0.0036|0.0930|
|AR07_delta005|MBB40|79/80|0.1646|0.8987|-0.0068|0.1478|
|AR07_delta005|STATIONARY40|77/80|0.1558|0.9091|-0.0068|0.1537|
|AR07_delta005|LOCAL40_W100|79/80|0.2278|0.8734|-0.0068|0.1297|
|AR07_delta005|HAC120|80/80|0.4375|0.7500|-0.0068|0.0999|
|AR07_delta005|MULTIPLIER120|80/80|0.4000|0.7250|-0.0068|0.0988|
|AR07_delta010|MBB40|80/80|0.7750|0.9375|0.0029|0.1426|
|AR07_delta010|STATIONARY40|80/80|0.7750|0.9625|0.0029|0.1493|
|AR07_delta010|LOCAL40_W100|80/80|0.8750|0.9250|0.0029|0.1255|
|AR07_delta010|HAC120|80/80|0.9375|0.8500|0.0029|0.0952|
|AR07_delta010|MULTIPLIER120|80/80|0.9500|0.8500|0.0029|0.0943|
|AR095_delta002|MBB40|80/80|0.2000|0.7750|-0.0050|0.2590|
|AR095_delta002|STATIONARY40|80/80|0.1875|0.7875|-0.0050|0.2586|
|AR095_delta002|LOCAL40_W100|80/80|0.2500|0.7250|-0.0050|0.2280|
|AR095_delta002|HAC120|80/80|0.2875|0.6750|-0.0050|0.2042|
|AR095_delta002|MULTIPLIER120|80/80|0.3000|0.6625|-0.0050|0.2008|
|AR095_delta005|MBB40|80/80|0.1500|0.8375|-0.0045|0.2585|
|AR095_delta005|STATIONARY40|80/80|0.1500|0.8875|-0.0045|0.2586|
|AR095_delta005|LOCAL40_W100|80/80|0.2125|0.7875|-0.0045|0.2261|
|AR095_delta005|HAC120|80/80|0.3125|0.8000|-0.0045|0.2099|
|AR095_delta005|MULTIPLIER120|80/80|0.3000|0.7500|-0.0045|0.2076|
|AR095_delta010|MBB40|79/80|0.4557|0.7848|0.0132|0.2556|
|AR095_delta010|STATIONARY40|79/80|0.4810|0.7722|0.0132|0.2561|
|AR095_delta010|LOCAL40_W100|80/80|0.5125|0.7375|0.0132|0.2269|
|AR095_delta010|HAC120|80/80|0.5375|0.7375|0.0132|0.2068|
|AR095_delta010|MULTIPLIER120|80/80|0.5250|0.7250|0.0132|0.2046|


이표의power는nominal rejection probability이며TypeI가검증되지않은방법의'검증된검정력'이아니다. coverage는marginal95 CI에대한진단이고Holm동시CI가아니다. effect와CI/p의대상이가정변경에따라달라질수있다는점도설계검토조건이다.

full-family는실제BA/F1/Brier/Recall 함수를52합성예측기(5NN×10Seed+2baseline)에적용해20/80가족을구성했다. A/B는동일shared copy로강한공동의존을명시했으며두배의독립복제로세지않는다. 초기1000dataset×199draw의bootstrap FWER0은최소p=.005 때문에기계적으로Holm20/80기각불가여서 **정보없음** 이다. 이를오류율통제PASS로바꾸지않았다.

별도200holdout×1999draw 재검증에서MBB40의ρ.95 FWER는Primary.13/Secondary.12(각100eligible)였고ρ.7은.01/.01이었다. Stationary120은공통validmask에서eligible0이었다. analytic HAC120 full-family holdoutρ.95는Primary.45/Secondary.56(각200)로주변p왜곡을Holm이수리하지못했다. 각FWER의MCSE/Wilson구간과무효분모는JSON에있다. 1999draw도Holm80첫임계값에서기대tail count약1.25뿐이라MC정밀도는매우제한적이다. 실제금융가족의FWER보증이아니다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
