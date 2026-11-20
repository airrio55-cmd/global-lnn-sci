# STEP9A MASTER_EVIDENCE_MAP

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

|RQ|설계·직접관측|반대근거|근거수준·노출한계|가능 / 불가 결론|
|---|---|---|---|---|
|RQ1 후속Test 성능|F1 5NN×10Seed×5Origin×A/B,NN500Test;C01,C02|지표순위변경,C03 Recall1 차이|저장기술통계+기존STEP5C근사검정;historical Test노출|“BA우수성미입증” / “LNN동등·최고” 불가|
|RQ2 Seed·Origin 안정성|STEP4D고정500학습·early stopping기록,Test LTC24/100단일예측;C04|다른Seed/Origin·모델에서도수치차이;Validation선택사용|기술적학습진단;반복Seed비독립|“조건별퇴화반복” / “10Seed로미래안정성확증” 불가|
|RQ3 수동/HMM 레짐|Train-onlyq30/q70,Train-onlyHMM2+forwardfilter;C06|점유율/support다름,Low 일부BA null|층화기술통계;유효Origin집합차이·historical노출|“조건부분포차이” / “레짐인과효과·유리한군선택” 불가|
|RQ4 τ·퇴화|실제계측99/100,퇴화23·비퇴화76,공존7/7같은방향;C05|O3소표본/O5군부재/누락1/구성불균형|사후탐색연관;유효τ선택과neuron/window의존|“낮은effectiveτ와함께관측” / “낮은τ가원인” 불가|
|RQ5 단순baseline대비|새baseline40,LR10;C01,C07,C08|Momentum60 F1높음,Origin우열다름,퇴화LTC BA추가없음|기술적benchmark만;새p값없음·입력이력다름|“일부평균BA추가관측” / “통계/거래/복잡도인과우월성확증” 불가|

RQ1의BA/일부Secondary에만기존정의된통계검정이있다. RQ2~4도대부분기술·탐색수준이며RQ1~4를통틀어확증이라고하지않는다. RQ5에는baseline비교금융검정이전혀없다. 각행의C번호는traceability의실제report/JSONpointer와연결한다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
