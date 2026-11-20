# STEP9A STATISTICAL_EVIDENCE

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

|기존STEP5C가족|블록20/40/60 각가설수|기존Holm<.05 결과수20/40/60|
|---|---:|---|
|Primary BA|20|0/0/0|
|Origin BA|100|0/0/0|
|Secondary|80|3/2/3|

원600행에서그대로확인했다. 다른블록의같은가설은독립재현이아니다. BA비유의는우수성미입증이며동등성/무효과증명이아니다. 기존중심화block-bootstrap 유한반복p는근사값이며기존percentile CI는동시구간이아니다. 이번에는재계산하지않는다.

반대근거:A LSTM−LTC Recall1의기존차이는0.1040777874,기존Holm p는20/40/60에서0.0311968803/0.0473952605/0.0157984202다. 이것을다른metric의열위나새검정결과로확장하지않는다. 기존다른Secondary결과도원600행을그대로유지하며유리한블록만대표로고르지않는다. STEP8BR NN-baseline 비교는금융유의성검정이아직없다. 새baseline가설을기존20/80/100가족에사후추가하지않았다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
