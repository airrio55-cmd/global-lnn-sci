# STEP9B1R METHOD_COMPARISON

STEP9B-1R은 방법론 재검토와 독립 합성 실험이다. 실제 금융 예측·Target·가격 배열을 수치로 열거나 재표집하지 않았고, 신규 금융 fit/forward/draw/p값/CI·NN/Logistic 재학습·HMM·τ·Ensemble·GPU·2026시장자료 사용은 모두0이다. 보존 검증의 byte SHA 읽기만 수행했다. NN500/Test500·baseline40/LR10·STEP5C600행·HMM100/최종10·보완 τ100/100, 원STEP7B99 PASS/1BLOCKED 및 원STEP8B BLOCKED40을 보존한다. 원STEP9B1은 τ99 당시 기록으로 수정하지 않았다. Primary joint20/Secondary joint80 Holm 각각alpha.05를 유지하며 전체100의FWER5%를 주장하지 않는다. master flags=false, A/B BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED 및 과거Test노출·Origin/Seed/20D label 중첩 한계도 그대로다.

|방법|적용 조건/BA·F1 적합성|희소·겹침·구조변화/정보량|구현·power 비용/실패|
|---|---|---|---|
|MBB|약정상성·적절한mixing, L증가/L÷n감소 등; ratio분모가양수로안정적|20session겹침을블록내부분보존,접합은손실;Origin의존재/클래스소실가능|정확metric 재계산;끝단포함빈도편향;큰L은유효정보/검정력손실|
|Stationary|geometric 길이,원순환표본;stationary/weakdependence가정|원끝→시작 인공접합;평균L120에서여러Origin이누락되는draw가많음|큰L이해결책아님;희소/Origin공통mask에서거의전부BLOCKED|
|Tapered|원래taper변환과적합한smoothfunctional 조건 필요|단순가중confusion table을정식taperedBB라고부를수없음|별도검증된BA/F1구현없음: 검토만/미실행|
|Local block|위치별국소정상·서서히변하는법칙/충분한local표본 필요|급격한break를창안에서섞음;원5Origin시간평균과local empirical법칙의관계검토필요|Origin존재는개선해도TypeI/coverage는실패;bandwidth는사전고정|
|Calendar/Origin aware|공식session·원membership·동일date인덱스,5Origin동일가중|연말20세션label공유 보존은부분적;5Origin을독립bootstrap하지않음|그자체로추론법아님;Origin별class강제층화는시계열법칙을바꿈|
|IF-HAC|BA/Recall 비율의delta method; class분모가0에서멀고CLT/LRV존재·bandwidth조건|F1는tp/(2tp+fp+fn)+tn/(2tn+fp+fn)의gradient 필요;rare에서미분/정규근사불안정|관측class support≥10 사전제약;Gaussian-Wald이지bootstrap-t가아님;큰bw/짧은Origin에서불안정|
|Dependent multiplier|동일날짜의공통MA Gaussian weight,IF의약정상/CLT조건|Seed/가격/모든쌍에공동weight;현재는원metric의정확유한표본재표집이아님|Bartlett-HAC covariance와일치하는구현확인;지원도제약/IF근사실패를고치지못함|
|Studentization대안|진정한bootstrap-t면draw마다분산/ratio지원도를재추정해야함|분모불안정·degenerate variance 위험;현재fixed-HAC scaling과구분|추가이론/계산필요,현재금융적격판정없음|

BA influence ψ는각Origin의class-conditional indicator 차이를중심화하고 N/(5n_o)로가중했다. HAC는lag≤q의Bartlett 공분산, multiplier는길이q+1의Gaussian MA로같은조건부covariance를구현했다. full20/80family에는F1/Brier/Recall의관측confusion비율gradient도적용해finite-contamination derivative와검증했다. 이구현일치가CLT나coverage를보증하지않는다. 희소class분모가커지는경우의가정은여전히미해결이다.

참고문헌 확인 범위: CrossRef에서 Künsch(1989) https://doi.org/10.1214/aos/1176347265 , Politis–Romano(1994) https://doi.org/10.1080/01621459.1994.10476870 , Paparoditis–Politis Local block bootstrap(2002) https://doi.org/10.1016/S1631-073X(02)02578-5 의 서지 metadata를 2026-11-20 KST에 확인했다. full text의 증명/현 금융자료 적용을 인증한 것은 아니다. Tapered/HAC/dependent-wild 검색은 HTTP429로 차단돼 원문 확인 완료로 처리하지 않았다. 세부 metadata·실패 이력은 합성summary에 보존했다.


확인일:2026-11-20 KST. 모든새추론수치는합성결과이며실제금융결과가아니다.
