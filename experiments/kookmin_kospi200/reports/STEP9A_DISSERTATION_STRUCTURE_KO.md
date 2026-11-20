# STEP9A DISSERTATION_STRUCTURE

STEP9A는보존결과의읽기전용통합·주장감사·논문초안·합성설계검증이다. 신규금융NN/Logistic fit, checkpoint load/forward, Test예측/성능재계산, HMM fit/refilter, τ계측, Bootstrap/p값/Holm, Ensemble, 외부금융입력 및2026시장관측사용은모두0이다. 기존NN500fit/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED·baseline40/Logistic10 및원STEP8B BLOCKED40을보존한다. master flags=false.

A/B BOTH_UNVERIFIED,primary price PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED. O1~O4 Test와후속Validation의역사적중복,동일시장Origin/Seed/중첩window·20session label의존성을명시한다. F1 LTC를원형RAW5/LOG2 Ensemble로,또는KOSPI200연구를JOF V16 5개국연구로대체/혼합하지않는다. 새주장에맞춘가격/모델/Seed/threshold 선택과기존결과수정은없다.

|장|RQ|핵심표|핵심그림 계획|반대근거/한계|본문용요약문단|
|---|---|---|---|---|---|
|1 서론|RQ1~5|연구질문·증거수준map|재현성/의존성전체흐름도|baseline/F1반대근거를서론부터명시|통합된진단구조가목표이며학습500회자체가독창성은아니다.|
|2 이론·선행연구|RQ1~5|LTC/CfC/재귀NN·단순rule의정보이력표|LTC conductance 개념도(원시값공개없음)|경제적기억과model step분리|LTC시간상수는모델내부진단량이며시장인과시정수로동일시하지않는다.|
|3 데이터·재현성감사|전RQ|A/B출처·cutoff·PIT·실패/복구표|session label/purge다이어그램|BOTH_UNVERIFIED/UNKNOWN|저장복구와원천가격/PIT검증은별개이며원실패기록을보존한다.|
|4 설계·통계방법론|RQ1/5|500NN·40baseline설계,원5C가족과9B초안구분|Train/Val/Test와역사적중복도|Test이미열람·의존성|동일평가기준일을유지하되상이한입력이력과탐색적검정수준을명시한다.|
|5 NN·baseline예측성능|RQ1/5|A/B6지표18모델행·차이표|저장5Origin평균지표별rank plot|MomentumF1우세·Origin불일관|NN의평균BA추가는관측됐으나모든지표/기간의우월성은일관되지않았다.|
|6 Seed·시기별안정성|RQ2|Seed/Origin저장집계·단일예측수|집계BA변동·퇴화빈도도|Validation선택·다른모델문제도보고|LTC의단일클래스예측은학습안정성진단이며Seed를독립시장반복으로세지않았다.|
|7 수동/HMM레짐|RQ3|레짐별유효BA·support/null·점유율표|유효모델수와레짐성능요약도|Low일부실제한클래스|레짐별차이는유효집합과시장구성의차이를반영하는기술적분해다.|
|8 τ·퇴화진단|RQ4|99/100·퇴화23/비퇴화76·공존7/7표|집계τ분포·observation/substep설명도|O3/O5·누락1·사후선택|낮은effectiveτ와퇴화가함께관측됐지만구성독립효과와인과메커니즘은식별되지않았다.|
|9 종합논의·한계|전RQ|주장가능/금지·반대증거matrix|증거수준/미해결gate지도|원형Ensemble미검증·PIT·역사적노출|성능·안정성·레짐·내부동역학을동일평가체계에연결한구조를기여로정리한다.|
|10 결론|전RQ|검증된범위·후속승인조건표|필요시연구로드맵(실행아님)|인과/전향성/실거래우월성주장불가|현재자료가뒷받침하는회고적결론을제시하고추가금융실험은자동시작하지않는다.|

그림은계획이며새금융데이터계산/그림생성은하지않았다. 기존Journal of Forecasting V16의5개국시장모델·데이터·결과·검정과본KOSPI200박사실험의주장/표/식별자를분리한다. 원HistoricalBaseline을수정된F1실험결과로덮어쓰지않는다.

확인일:2026-11-20 KST. 수치출처는step9a_evidence_traceability.json의실제기존report/manifest pointer를참조한다. 외부가격공식인증·새금융추론은수행하지않았다.
