# STEP9B1 HYPOTHESIS_FAMILIES

이번 단계는 통계 설계·방법론 감사·독립 합성 검증뿐이다. 금융 bootstrap/예측배열 재표집/p값/CI/fit/forward/Test재계산/HMM/τ/Ensemble/GPU/2026관측 사용은 모두0이다. 기존 NN500/Test500·baseline40/LR10·통계600·HMM100/최종10·τ99 PASS/1 BLOCKED·원STEP8B BLOCKED40과master flags=false를보존했다. 기존STEP9A초안은DRAFT/NOT_APPROVED/FAMILIES_NOT_FROZEN인그대로이며새9B1사양만별도동결했다. 이미본Test에대한향후검정은retrospective exploratory analysis이고prospective preregistration/독립확증이아니다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_atUNKNOWN,production-PIT BLOCKED와역사적Test노출한계는유지한다.

|안|범위·tradeoff|선택|
|---|---|---|
|Primary joint20|5NN×2baseline×A/B 전체에Holm;분할보다보수적이며A/B같은시장임을반영|선택|
|10+10 baseline분리|각가족내.05이나전체최대.10;가족분리로작은p를얻으려선택하면안됨|미선택|
|가격별10+10|각가격내통제뿐,A/B독립시장이아니며전체통제아님|미선택|
|Secondary joint80|4지표×전체쌍/후보80한가족. metric별분할보다보수적|선택|
|metric별20×4|각metric범위만통제;네가족합친FWER5%주장불가|미선택|

Primary와Secondary는각각5%가족이다. 두가족전체100개의FWER5%를주장하지않는다(단순합한상한10%). 전체5%가꼭필요하면.025/.025등alpha allocation이나joint100을별도버전으로검토해야하며결과를보고바꾸지않는다. 세블록은민감도이며독립재현/새로운유리한가족으로세지않는다. Holm은원p가유효할때의보정이지잘못된block p를수리하는장치가아니다.

확인일:2026-11-20 KST. 합성결과는실제금융결과가아니다.
