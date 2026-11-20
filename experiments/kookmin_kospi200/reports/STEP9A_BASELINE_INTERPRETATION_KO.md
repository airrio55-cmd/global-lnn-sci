# STEP9A BASELINE_INTERPRETATION

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

NN의5Origin평균BA는A/B모두최고baseline Momentum60(0.504416)보다높았다. 그러나RNN은Momentum60대비BA우세Origin이2/5뿐이며평균상승을기간일관성으로바꾸면안된다. Momentum60 MacroF1=0.491019가모든NN평균보다높고,그Brier=0.425077은확률NN/Logistic/Climatology보다크다. 규칙0/1점수는degenerate probability이며calibration인증이아니다.

퇴화LTC24개(A/B12씩)는Climatology와모두BA0.5로같았다. F1은각후보4개더높고8개동률,Brier는8개더낮고4개더높아“추가BA가없음”과“모든측면무가치”를구분한다. 표본수는모델결과개수이며독립시장반복수가아니다.

NN의20시점F1,Logistic의현재t F1,DMA200의200종가,Momentum60의60session간격은정보이력/표현이다르다. 같은Test날짜·Target·결정시점을맞췄어도복잡도만분리한완전통제실험은아니다. Validation-Test차이는baseline Validation지표가없어새로만들지않는다. 가격/Origin/모델을부정적결과로제외하지않는다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
