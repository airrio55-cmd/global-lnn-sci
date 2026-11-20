# STEP9A NEW_TEST_PROTOCOL_DRAFT

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

이 문서는 **DRAFT / NOT_APPROVED / FAMILIES_NOT_FROZEN**이다. 연구자는이미STEP5B/8BR Test결과를봤다. 후속9B는retrospective exploratory analysis이며prospective preregistration·독립확증이라고부르지않는다. 현재금융draw/fit/forward/p값예산0,금융entrypoint는무조건차단한다.

|설계항목|논의용제안·확정전결정사항|
|---|---|
|모델쌍|5NN모두vsMomentum60 BA를Primary후보로,5NN모두vsClimatology BA를추가후보로검토;유리한모델만선택하지않음|
|가족선택|Momentum10(5NN×A/B)jointHolm+Climatology10별도탐색가족,또는둘을묶은20가족. 후보별분리가족도선택지이나A/B동일시장·가족간FWER한계명시. 아직선택/확정안함|
|Secondary|F1/Brier/Recall0/1×5NN×2baseline×A/B=80후보;단일80가족또는분할설계의보정범위를선택전명시|
|estimand|각draw에서Origin별NN10Seed의metric평균−baseline1개metric,그뒤5Origin동일가중. probability평균Ensemble이나Seed행연결금지. Brier는낮음이유리|
|date paired|같은prediction date/Target/session/label_end를모든모델·Seed·후보에동일draw로적용;A/B는한시장후보이며독립복제아님|
|겹침·Origin|Test기준연도는서로다르지만20session endpoint가연도경계를넘어공유되고과거Test가후속Validation에노출됨. Origin5개를재표집독립단위로보지않음|
|block|전체공식session연대기에서동일moving-block stream을제안,원날짜의Origin membership유지. 연말에의존성을자동절단하지않음.20/40/60민감도,예시반복10000이나미동결/금융실행0|
|방법한계|noncircular MBB는끝단선택빈도/비정상성한계. circular는2025끝→2021처음의가상연결문제;자동대체하지않고민감도후보로만검토. 구조변화가심하면그추정타당성자체재검토|
|null·실패|Origin누락/실제한클래스/저장예측누락은해당family draw무효. 선택가족공통validity mask,invalid count보고.10%초과시BLOCKED 제안이나미확정. 무효Origin제외평균/0대체/유리한draw선택금지|
|추론|중심화paired bootstrap+plus-one근사p및percentile effect CI를후보로검토;복수metric/가족에맞는Holm범위사전선택. percentile은동시구간아님,다른block결과는독립재현아님|
|효과·검정력|p와원단위effect/불확실성을구분. 작은효과·큰의존성·5Origin의정보제약을명시;비유의는동등성아님. MDE/검정력은synthetic가정별설계로검토하며관측p로posthoc power를주장하지않음|
|독립release|9B에별도사용자승인·선택가족·모든쌍/지표/가격·RNG·draw예산·SHA·filepaths·ledger·무효기준/환경을동결해야함. 기존5C20/80/100가족은수정하지않음|

합성16검사는block내연속성·공통date pairing·재현성·Seed metric평균≠Ensemble·Origin보존·한클래스null·퇴화예측적격·plus-one p범위·Holm既知例·불완전가족차단·금융차단을검증했다. 실데이터의stationarity/명목오류율/검정력/CI coverage가검증됐다는뜻은아니다. 그타당성은현재BLOCKED_REQUIRES_DESIGN_REVIEW다. 금융입력은읽지않고독립생성배열만사용했다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.

추가로Origin표본수가달라도동일5Origin가중estimand를유지하는지,합성동일예측null에서20/40/60블록draw의효과가0인지확인했다. 이는명목오류율/검정력을보장하지않는다.
