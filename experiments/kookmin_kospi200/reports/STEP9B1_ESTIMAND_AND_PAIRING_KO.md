# STEP9B1 ESTIMAND_AND_PAIRING

이번 단계는 통계 설계·방법론 감사·독립 합성 검증뿐이다. 금융 bootstrap/예측배열 재표집/p값/CI/fit/forward/Test재계산/HMM/τ/Ensemble/GPU/2026관측 사용은 모두0이다. 기존 NN500/Test500·baseline40/LR10·통계600·HMM100/최종10·τ99 PASS/1 BLOCKED·원STEP8B BLOCKED40과master flags=false를보존했다. 기존STEP9A초안은DRAFT/NOT_APPROVED/FAMILIES_NOT_FROZEN인그대로이며새9B1사양만별도동결했다. 이미본Test에대한향후검정은retrospective exploratory analysis이고prospective preregistration/독립확증이아니다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_atUNKNOWN,production-PIT BLOCKED와역사적Test노출한계는유지한다.

각Origin/Candidate에서동일날짜의metric을10개Seed별로각각계산→산술평균→baseline1개metric을뺀다. 그뒤5Origin동일가중평균한다. BA/F1/Recall의양수, Brier의음수가NN에유리하다. 확률평균Ensemble metric이나Seed행연결·표본10배확대는금지한다. 이정의는기존8BR과같다.

한draw의원공식session 인덱스를모든모델쌍·Seed·A/B에공통적용한다. 각재표집관측은원날짜의Origin membership과원Target/label_end를유지한다. 누락Origin을빼서다른estimand로바꾸지않는다. Test연도는달라도20session endpoint공유와학습/Validation노출이있어Origin5개를독립재표집하지않는다. A/B는같은시장의후보이지독립replication이아니다. 원8BR동일가중기술차이와의금융배열정합확인은9B2승인후별도gate이며이번에는금융metric을다시계산하지않았다.

확인일:2026-11-20 KST. 합성결과는실제금융결과가아니다.
