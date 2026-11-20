# STEP9B1R STRONG_DEPENDENCE

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

원ρ=.95·rareclass 실패 6행은 보존된DGP/PCG64 SeedSequence를 그대로 재실행해 **정확 일치** 했다. 기존80dataset의MC불확실성은원보고서Wilson구간과함께보존했다. 새stream/새표본의다른값은실패사례불일치가아니라독립MC차이다.

주 campaign의ρ는Gaussian수익률 AR계수가아니라 **이진예측오류 Markov process의lag1 persistence** 다. 혼동하지않도록 Gaussian latent AR.95/.98 확장도추가했다. 라벨은여러시나리오에서독립생성수익률의20session미래합으로만들어겹침을유지했다. 이들은실제금융모델을학습한예측이아닌합성oracle-error 예측구성이다.

|DGP|방법|유효dataset/전체|Type I/Power(조건부)|coverage(조건부)|bias(정의가능전체)|평균CI폭|
|---|---|---:|---:|---:|---:|---:|
|overlap20_AR095_null|MBB20|500/500|0.2980|0.6920|-0.0056|0.2085|
|overlap20_AR095_null|MBB40|496/500|0.1915|0.8004|-0.0056|0.2573|
|overlap20_AR095_null|MBB60|390/500|0.1513|0.8308|-0.0056|0.2781|
|overlap20_AR095_null|STATIONARY40|499/500|0.1924|0.8056|-0.0056|0.2582|
|overlap20_AR095_null|HAC120|500/500|0.3120|0.6880|-0.0056|0.2087|
|overlap20_AR095_null|MULTIPLIER120|500/500|0.3020|0.6820|-0.0056|0.2067|
|overlap20_AR098_null|MBB20|80/80|0.4500|0.5250|-0.0126|0.1978|
|overlap20_AR098_null|MBB40|80/80|0.3625|0.6250|-0.0126|0.2611|
|overlap20_AR098_null|MBB60|69/80|0.3043|0.6812|-0.0126|0.2957|
|overlap20_AR098_null|STATIONARY40|80/80|0.3500|0.6500|-0.0126|0.2675|
|overlap20_AR098_null|HAC120|80/80|0.4000|0.6000|-0.0126|0.2439|
|overlap20_AR098_null|MULTIPLIER120|80/80|0.3750|0.6000|-0.0126|0.2424|
|Gaussian_latent_AR950_null|MBB20|500/500|0.2720|0.7200|0.0042|0.1848|
|Gaussian_latent_AR950_null|MBB40|499/500|0.1884|0.8116|0.0042|0.2242|
|Gaussian_latent_AR950_null|MBB60|386/500|0.1451|0.8342|0.0042|0.2400|
|Gaussian_latent_AR950_null|STATIONARY40|497/500|0.1871|0.8129|0.0042|0.2247|
|Gaussian_latent_AR950_null|HAC120|499/500|0.3006|0.6994|0.0042|0.1749|
|Gaussian_latent_AR950_null|MULTIPLIER120|499/500|0.2946|0.6934|0.0042|0.1725|
|Gaussian_latent_AR980_null|MBB20|80/80|0.4000|0.6125|-0.0076|0.1831|
|Gaussian_latent_AR980_null|MBB40|80/80|0.3375|0.6750|-0.0076|0.2335|
|Gaussian_latent_AR980_null|MBB60|59/80|0.3220|0.7288|-0.0076|0.2495|
|Gaussian_latent_AR980_null|STATIONARY40|80/80|0.3250|0.6625|-0.0076|0.2364|
|Gaussian_latent_AR980_null|HAC120|80/80|0.3875|0.6125|-0.0076|0.2038|
|Gaussian_latent_AR980_null|MULTIPLIER120|80/80|0.3625|0.6250|-0.0076|0.2040|


각TypeI·coverage의MCSE/Wilson95구간은JSON에있다. q=120가짧은Origin길이200에비해큰점,Origin별중심화/낮은유효정보/ratio분모변동이원인후보이나어느하나가왜곡을완전히설명했다고인증하지않는다. 블록만길게하거나p반복만늘려해결됐다고보지않는다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
