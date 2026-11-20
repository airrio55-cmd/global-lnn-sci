# STEP9B1R SIMULATION_RESULTS

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

개발용1160+확인용3520=총4680개독립 pair dataset,23개DGP,9개방법을실행했다. 핵심binaryAR.95/rare3%/sharedbreak는holdout각500,별도Gaussian latent AR.95도500을실행했다. 다른holdout은80이므로정밀도가낮음을명시한다. pair재표집은499draw;HAC는draw없는Gaussian-Wald,최소class지원도10미만이면실행차단이다.

method/kernel과선정기준을주 campaign 전에고정하고phase별PCG64 SeedSequence namespace를분리했다. 개발/holdout을동시에실행했으므로blind한사전등록이라고부르지않으며,이번에는선정된방법이없다. 결과후수식을튜닝하지않았다. Gaussian AR와누락된동일ρ×delta factorial확장은커버리지공백을메우는별도계획/새stream으로추가했으며원계획의독립확증이라고과장하지않는다. 최종δ=.02/.05/.10은각각ρ=.7/.95에서비교가능하다.

선정기준: 핵심Null마다eligible≥90%,TypeI점추정≤.075와Wilson95에.05포함,coverage≥.925와Wilson95에.95포함,validdraw≥90%를함께검토했다. δ.10의power목표.8도참조하되size가잘못된방법의큰power를장점으로선정하지않는다. 9개모두핵심조건을완전히충족하지못했다.

모든DGP×방법×phase의조건부오류율/Power/coverage·CI폭·bias·MCSE·Wilson구간·유효분모·무효원인·시간은simulation_summary JSON에있다. 큰자료에서불리한행을빼지않았고raw합성기록도private보존했다. 재현은root20261120과phase/scenario/rep/method namespace로고정했다.

계산은CPU2worker 이하/BLAS thread1로수행했다. 개발57.6초·기본holdout151.4초(병렬이므로합계wall아님),full-family93.0초와tail확장74.1초를기록했다. 관측된기본pair peakRSS는74.2/93.0MB,full-family101.3MB다. 미계측component의전역최대메모리를확인했다고주장하지않는다.

확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
