# STEP5C_BOOTSTRAP_AUDIT_KO

이번 결과는 retrospective rolling-origin statistical analysis다. 가격 A/B는 별도 보고하며 BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, 주가격 PENDING을 유지한다. 모델/가격/Seed/기간/가설을 결과에 따라 선택하지 않았다. finite-replication 중심화 bootstrap p값은 근사값이며 percentile95%CI는 동시 신뢰구간이 아니다. Seed와 Origin을 독립 시장 반복으로 간주하지 않는다.

공식 KRX session_id가연속인 길이20/40/60의시작점만선택한다. 각 draw에서 start를 rng.choice(possible,size=ceil(n/L))로복원추출하고 blockindices를연결해원래n으로자른다. 날짜gap/중복/비단조session은차단한다. 같은Origin/Candidate의모든모델/10Seed가정확히같은indices를사용하며 A/B도고정된동일날짜목록안에서분리계산한다.

각Seed별지표→10Seed평균→5Origin동일가중평균→같은draw의두모델차이다. 확률평균 Ensemble이나 Seed행연결로 시장날짜를10배늘리지 않는다. Pooled는draw-major→Origin-major순 RNG, Origin진단은원래단일Origin 함수호출처럼별도seed초기화한다. 모두20261116이며모델/가설별유리한RNG를고르지않는다.

중심화근사p=(1+count(|draw−observed|≥|observed|))/(유효draw수+1). CI는유효draw의2.5%,97.5% percentile이다. p는finite replication 근사값,CI는비동시적이다. BA/MacroF1 한클래스draw와지원없는클래스Recall은NaN을유지해무효횟수로센다. Brier는그경우에도정의된다. 무효율>10%는해당추론BLOCKED,전체가족의유효p가모두있기전에는Holm판정을완성하지않는다.

250draw청크40개×3블록=120개를확정했다. 각청크는입력/config/source SHA,draw범위,출력SHA,RNG before/after를atomic commit으로저장한다. 미완성임시출력은확정draw로세지않고보존·격리한다. 재개는모든기존commit과RNG연속성을검증할때만가능하다. 이번실제실행의재개0회. 합성에서는청크분할과JSON RNG복원후indices/결과일치,기존 scalar bootstrap의pooled/단일Origin BA와동일CI/p값을검증했다. draw별금융벡터/RNG상태와개별lineage는ignored private에만보존했다.

블록별무효횟수/율은각600개결과행에모두보존한다. 최대무효횟수는pooled20:0,40:2,60:1;Origin진단20:0,40:4,60:2였다. 모두10%이하라row/family BLOCKED0이다.

공개본은 사전 가설의 다중fit 집계·방법·비민감 SHA만 포함한다. 개별 금융일자/Target/확률·민감 identity/SHA매핑·draw벡터·checkpoint·실제scaler/Train임계값은 로컬 비공개로 보존했다.
