# STEP10C 박사논문 방향A/B의 증거 기반 비교

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

| 항목 | 방향A:최신F1·LTC진단 | 방향B:원형RAW5/LOG2앙상블 |
| --- | --- | --- |
| 학문적 초점 | F1 신경망비교·Seed/Origin안정성·레짐·LTCτ를통합진단 | RAW5/LOG2 LTC앙상블의정보결합·예측성향·추가효과 |
| 현재 실험근거 | 동결NN500/Test500·baseline40·HMM100/선택10·τ100과실행lineage | Word의5Seed성능/레짐은포함셀대조일치;1/10Seed수정통계는원문보고만확인 |
| 독창성 후보 | 실패/복구·반대지표·퇴화·conductance를연결한재현성진단;500횟수자체아님 | 상이한정보공간결합과레짐/Seed민감도;가중평균자체의독창성은문헌검토필요 |
| 통계한계 | 기존MBB/Holm근사타당성미확립,NOT_TESTEDbaseline비교·historicalTest노출 | 대표Seed의Test의존선정·n38/시간의존·수정코드미확보·보정기준차이 |
| 데이터/PIT | 국내가격source·개정·18시미확정;A/B둘다보존 | 국내가격에외국인범위/단위·미국시장as-of증빙이추가로필요 |
| 필요 보완 | 원문–코드식별/분할·loss/시차/HMM서술정리,제목/RQ범위정합 | 수정통계/원예측아카이브,RAW5/LOG2출처/정렬/사양;필요claim에한해bridge |
| 제목 적합성 | 신경망비교·LTC안정성/레짐/시간상수진단으로범위를표현 | 기존‘앙상블기반’제목과직접연결되나최신500을원형검증으로대체불가 |
| 현재권고 | 현재증거와추적가능한결과를기준으로방향A 권고 | 원형앙상블을핵심으로유지할명확한RQ와보완계획이있을때조건부검토 |

## 현재 증거에 가장 부합하는 권고

**방향A를현재집필의주축으로권고한다.** 이유는BA나p값이더좋아서가아니라,현재수행완료된500실험과실행·실패/복구·비교/레짐/τ근거의추적범위가A의RQ와맞기때문이다. 가격/PIT가검증됐다는뜻은아니며서술·탐색적회고연구라는한계를명시한다. A/B가격중승자를고르지않는다.

초기Word도P0369/P0383/P0395에서Ensemble의모든지표·Single대비일관우월성을부정하고목적별trade-off를인정한다. 이를부정적결과때문에폐기하지않고Historical Baseline과설계변경동기로보존한다. 방향B가학문적으로틀렸다는판정은아니다. 다만그핵심claim을최신F1의결과로뒷받침할수없고원문–코드불일치와수정통계의출처연결을먼저해소해야한다.

## 제목·RQ 제안 — 문서 자동 수정 아님

A의제목후보: “KOSPI200 지수 방향성 예측의 신경망 비교와 LTC 학습 안정성·레짐·시간상수 진단”. RQ는신경망간기술적성능,Seed/Origin변동,수동/HMM층화,τ와퇴화의탐색연관,단순baseline비교를중심으로유지한다. 앙상블추가효과를검증한제목/본문으로쓰지않는다.

B를택하면RAW5/LOG2 LTC형태와원문CfC서술을정합시키고,상승Recall/PositiveF1과BA/MacroF1을분리해‘Ensemble항상우위’가아닌정보결합의기여와trade-off를RQ로명확히해야한다. 다른시간/피처/버전의수치를같은성능표로붙여강건성확증이라고하지않는다. 지도교수의최종제목·주결과/RQ확정과후속실험승인은별개다.

## 근거·위치 계약

| ID | 근거 | 위치 | 한계 |
| --- | --- | --- | --- |
| D1 | 사용자 제공DOCX 수신본 | SHA1d97db…599d; 문단P0001~P0516, 물리표T001~T013 | 원문의 사실과 보고결과의 존재를 확인; 실행사실 독립 인증 아님 |
| N1 | 원 단일/5/10Seed Notebook | originals/의 보존3파일; 실제1-based cell6/8/9/10/12/14~18 | 현재소스·저장출력의 정적 감사; 실행/재학습 없음 |
| B1 | STEP10B 기존 감사 | STEP10B_MASTER_COMPARISON, MODEL_ARCHITECTURE_COMPARISON, METRIC_STATISTICS_COMPARISON | 당시DOCX 부재/미확인 상태는 역사적 기록으로 유지 |
| A1 | STEP10A 출처/PIT | STEP10A_PRICE_PROVENANCE_AUDIT, HISTORICAL_PIT_AUDIT | 문서의pykrx 주장만으로 공급처·historical available_at 인증하지 않음 |
| F1 | 최신F1 master·Test | STEP3C_MASTER_PROTOCOL, configs/step3c_master_experiment_config.json; STEP5B/STEP8BR 공개요약 | 현재F1은RAW5/LOG2 원형과 구분; source정의 SHA만 일치 |
| S1 | 기존통계·방법론 한계 | step5c_execution_summary.json; STEP10_STATISTICAL_EVIDENCE, STEP9B1R_EXECUTION_READINESS | 기존600행 보존; 새 검정0, 비유의≠동등성 |
| T1 | 보완τ100 | step7br_public_aggregate_summary.json; STEP10_LTC_TAU100_INTEGRATION | 99+독립복구1의 versioned100, singleton 역산 수치 공개 없음 |

P번호는 이 SHA의 word/document.xml 본문 직속문단 순서, T번호는 물리적 표 순서다. 서명표가 앞에 있어 논리표6~12는 물리표T007~T013이다. 렌더링 페이지번호를 새로 확정하지 않는다. 전체 원문/표·정밀 대조자료는 비공개 로컬 감사자료에 보존하고 공개본에는 민감한 개별금융결과/대표Seed별분할표/원자료/체크포인트/단일τ를 넣지 않는다.
