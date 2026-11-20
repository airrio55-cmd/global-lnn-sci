# STEP9A LIMITATIONS_AND_CLAIMS

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

|사용가능 문장|필수제한/근거|금지되는 확대|
|---|---|---|
|“신경망은일부평균BA에서baseline보다높았지만기간과지표별상대우수성은일관되지않았다”|C01/C07,저장5Origin평균·Origin반대방향|“모든Origin에서NN>Momentum60”,“통계적으로최고”|
|“LTC특정조건의단일클래스예측은낮은effectiveτ와탐색적으로관련돼관찰됐다”|C04/C05,23/76유효분모·누락1·구성·중첩의존|“낮은τ가퇴화를유발”,“실제경제기억기간”|
|“기존검정은신경망간BA우수성을입증하지못했다”|C02,기존가족/보정/블록전체보고|“동등성/무효과증명”,“baseline우월성확증”|
|“회고적F1 benchmark다”|C09,가격/PIT·역사적중복·상이한이력|“미래수익예측력/실거래가능성검증”,“원형Ensemble재현”|

RAW5=[Log_Ret,Foreign_Net,Nasdaq,SOX,Disparity],LOG2=[Log_Ret,Disparity]는여전히미검증이다. Foreign_Net의시장/주체/집계·공급처·단위·공표·개정UNKNOWN,미국지수의시장종료/DST와공급처CSV available_at은별개이고과거전체세션/latency/max_age증빙부족이다. 같은날join/무조건shift1/bfill로PIT를인증하지않는다. A/B종가공급처/수정/18시가용성도UNKNOWN. 외부입력추가0,production-PIT BLOCKED다. F1의성과를원형Ensemble이나JOF V16 5개국시장성과로기술하지않는다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
