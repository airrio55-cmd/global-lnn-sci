# STEP9A TAU_REGIME_SYNTHESIS

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

LTC전체Test퇴화는24/100이다. τ실제계측은99/100 PASS와중단1 BLOCKED,유효퇴화23·비퇴화76이다. effective τ checkpoint-median 평균은각각기존0.0290992786/0.0490221471이다. STEP8A의Origin×가격공존셀7/7에서같은음의방향을보였지만그중1개는극소표본이며6개만양군n≥2다. O3소표본/O5퇴화군부재/Seed·Origin불균형/누락1/neuron·overlappingwindow·substep의존/사후분석을모두유지한다. 전체구성독립효과는NOT_IDENTIFIABLE이다. 단일모델값역산을막는보완억제를이어가며상세분할수치는private에만둔다.

rawτ는positive(cm)/positive(gleak),effectiveτ는입력/hidden conductance합을포함한분모의진단량이다. 단위model_observation_step이며물리적초·경제적기억·Jacobian고유시간이아니다. 저장요약만으로감각/순환기여를분리하거나인과를추정하지않는다.

수동레짐Train-only q30/q70의Low/Mid/High와HMM Train-only2state Low/High는별도표다. HMM은선택후forward filtering,Test전체Viterbi/median대체없음. τ레짐은예측기준일HMM을연결하며window과거날짜별레짐과혼동하지않는다. Low일부실제한클래스는BA/F1=null이므로High/Low평균의유효Origin집합이다를수있다. 전체Test24퇴화와레짐부분집합단일예측은다른사건이며유리한레짐만선택하지않는다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
