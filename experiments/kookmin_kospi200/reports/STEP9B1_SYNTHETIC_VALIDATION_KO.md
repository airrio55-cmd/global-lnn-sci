# STEP9B1 SYNTHETIC_VALIDATION

이번 단계는 통계 설계·방법론 감사·독립 합성 검증뿐이다. 금융 bootstrap/예측배열 재표집/p값/CI/fit/forward/Test재계산/HMM/τ/Ensemble/GPU/2026관측 사용은 모두0이다. 기존 NN500/Test500·baseline40/LR10·통계600·HMM100/최종10·τ99 PASS/1 BLOCKED·원STEP8B BLOCKED40과master flags=false를보존했다. 기존STEP9A초안은DRAFT/NOT_APPROVED/FAMILIES_NOT_FROZEN인그대로이며새9B1사양만별도동결했다. 이미본Test에대한향후검정은retrospective exploratory analysis이고prospective preregistration/독립확증이아니다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_atUNKNOWN,production-PIT BLOCKED와역사적Test노출한계는유지한다.

합성 구조검사22개 PASS/0FAIL. 8가지DGP×80독립dataset=640개,각각20/40/60블록과399draw를검사했다. 금융반복10000회와혼동하지않는다. Primary BA의대표쌍에서10합성Seed metric 평균과baseline1개를비교했다. alternative의참Δ=.1, null은0이다. iid,20session forward-label overlap,AR오류.7/.95,공유구조변화,교차구조변화,97%희소클래스를포함했다. 모든원자료는독립생성합성이고학습한금융모델이아니다.

|DGP|블록|유효dataset/80|TypeI 또는Power|95%marginal CI coverage|무효draw평균|
|---|---:|---:|---:|---:|---:|
|iid_null|20|80/80|0.0500 (TypeI_diagnostic)|0.9250|0.03|
|iid_null|40|80/80|0.0500 (TypeI_diagnostic)|0.9250|3.80|
|iid_null|60|80/80|0.0500 (TypeI_diagnostic)|0.9125|19.95|
|overlap20_AR07_null|20|80/80|0.0500 (TypeI_diagnostic)|0.9500|0.90|
|overlap20_AR07_null|40|80/80|0.0500 (TypeI_diagnostic)|0.9375|9.82|
|overlap20_AR07_null|60|62/80|0.0484 (TypeI_diagnostic)|0.9355|34.11|
|overlap20_AR07_alt|20|80/80|0.7875 (power)|0.9375|1.16|
|overlap20_AR07_alt|40|78/80|0.7179 (power)|0.9744|11.53|
|overlap20_AR07_alt|60|61/80|0.6557 (power)|0.9344|36.16|
|shared_regime_break_null|20|80/80|0.0500 (TypeI_diagnostic)|0.9375|1.96|
|shared_regime_break_null|40|78/80|0.0256 (TypeI_diagnostic)|0.9487|12.75|
|shared_regime_break_null|60|57/80|0.0702 (TypeI_diagnostic)|0.9123|34.99|
|shared_regime_break_alt|20|80/80|0.8625 (power)|0.8875|1.31|
|shared_regime_break_alt|40|79/80|0.7975 (power)|0.9114|12.16|
|shared_regime_break_alt|60|52/80|0.8269 (power)|0.9423|37.38|
|crossing_regime_null|20|80/80|0.0000 (TypeI_diagnostic)|1.0000|0.03|
|crossing_regime_null|40|80/80|0.0000 (TypeI_diagnostic)|1.0000|3.77|
|crossing_regime_null|60|80/80|0.0000 (TypeI_diagnostic)|1.0000|19.65|
|rare_class_null|20|40/80|0.0750 (TypeI_diagnostic)|0.9250|52.64|
|rare_class_null|40|19/80|0.0000 (TypeI_diagnostic)|1.0000|72.70|
|rare_class_null|60|1/80|0.0000 (TypeI_diagnostic)|1.0000|100.09|
|overlap20_AR095_null|20|80/80|0.2500 (TypeI_diagnostic)|0.7250|0.91|
|overlap20_AR095_null|40|80/80|0.1750 (TypeI_diagnostic)|0.8250|10.15|
|overlap20_AR095_null|60|56/80|0.1250 (TypeI_diagnostic)|0.9107|34.16|

각비율의MCSE/Wilson95구간,CI폭,무효dataset수는합성summary JSON에있다. 80dataset의MC오차는크고무효dataset을제외한비율은조건부선택의영향을받는다. 특히rare클래스·블록60은유효1/80이라TypeI0/coverage1을성공근거로볼수없다. ρ.95의기각률20/40/60=25%/17.5%/12.5%,coverage72.5%/82.5%/91.1%는명목5%/95%를보장하지못하는구체적반대근거다. 구조변화alternative에서도coverage가낮아지는경우가있다. 실제시장의TypeI/Power/CI를보증하지않는다.

20/80가족에대해유효한주변정규p와공통요인상관0/.6을가진합성가족을각5000회검사했다. FWER는20가족 .0462/.0296,80가족 .0452/.0246이었다. 이검사는Holm구현/유효주변p가정아래의진단일뿐blockbootstrap원p의유효성보증이아니다.

합성driver 초안이alternative에서참Δ를영가설로차감하던오류를발견해중단·보존하고,검정은H0Δ=0/coverage만참Δ를사용하도록수정한뒤전체simulation을재실행했다. 코드·오류로그는private보존,금융실행0이며가족/금융결과에따른튜닝은없었다.

확인일:2026-11-20 KST. 합성결과는실제금융결과가아니다.
