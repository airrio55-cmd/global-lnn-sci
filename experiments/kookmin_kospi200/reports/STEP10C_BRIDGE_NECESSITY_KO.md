# STEP10C Bridge 필요성·최소범위·실행 차단

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

## 판정의 층위

| 목적 | 판정 | 이유 |
| --- | --- | --- |
| 현재자료로F1진단중심집필/원문서술정정 | NO_BRIDGE_REQUIRED | 기존동결결과의범위를정직하게보고하는데새금융학습이자동필수아님 |
| 초기–최신을공통조건으로연결하는추가설명 | BRIDGE_OPTIONAL | 직접동등성주장을하지않으면문서/아카이브감사가먼저;선택적보완 |
| 원형RAW5/LOG2앙상블의추가효과를핵심claim으로유지 | BRIDGE_REQUIRED_FOR_CLAIM | 최신F1은그구조를실행하지않았으므로기여를대신인증할수없음 |
| 현재 bridge 실행 준비도 | BLOCKED_PENDING_EVIDENCE | 수정실행source/예측,공통data/date/target·외부피처/정보계약·별도승인부재 |

주된실행판정은 **BLOCKED_PENDING_EVIDENCE**다. 위표의논문필요성과실행준비도를섞지않는다. 새fit/forward/draw/pvalue 예산은모두0이다.

## 먼저 확보할 비실행 증거

Word표9~11/비중첩38/동일Seed재실행의수정script·실행환경·source/config/data/SHA·선정함수·원래date/Target/저장예측을받는다. 이아카이브로기존문서–코드의version gap을해소할수있다면,일부주장은새학습없이대조가능하다. 파일존재·hash 검증과새검정/모델forward는분리한다.

가격·지수정의·추출/수정정책,RAW5 외국인변수와미국시장정렬·available_at의증빙및회고적연구에서허용할한계조건을사전확정한다. 공통Train/Validation/Test와label/window/purge/Train-onlyscaler를새version으로고정한다. 원문의공통평가날짜는아카이브로확인하고성능이좋은시기를택하지않는다. 지금source/PIT를PASS로올리지않는다.

## 최소 학습 규모 — 제안이며 미승인

1. 원형Single対Ensemble의정보결합만보는좁은질문: 한가격후보·사전고정한공통기간/Origin·baseSeed42에서 **LTC_RAW5(offset401) + LTC_LOG2(offset402)의2fit**. 둘의확률0.5:0.5결합은추가fit0이다.
2. 최신F1정책까지명시적으로bridge: 위2개에 **F1_LTC2(offset401)** comparator를독립학습해 **3fit**. 이것이STEP10B의3fit 제안이다. LOG2와F1은두피처이지만offset/identity가달라자동재사용하지않는다.
3. Seed안정성까지주장하려면공통5Seed[42,52,62,72,82]의좁은질문10fit 또는완전bridge15fit/가격/기간이다. 양가격을사전병렬로두면각각20/30fit가된다. 한Seed로통계적강건성을인증하지않는다. 이는규모설계이며현재학습예산이아니다.

Seed42는성과로선택하는것이아니라초기1/5/10의공통식별자로구조점검에쓸수있다는제안이다. 현재500의F1 checkpoint를다른Train·window·label계약에재사용해공통조건이라부르지않는다. RNNHybrid나CfC비교가핵심RQ에별도로필요하면예산과사양을다시검토한다. 원문이실제CfC실행을뜻했다면해당source를먼저확보해야하며임의로LTC대신CfC를학습해문서를맞추지않는다.

## Test 노출과 결과 독립 해석

이미초기와최신Test를봤으므로bridge를전향적사전등록/미관측Test라고부를수없다. 공통기간은원날짜교집합과사전규칙으로정하고검정·검증성능에따라가격/Seed/가중치/threshold를바꾸지않는다. 모든사전모형을보고하고실패·퇴화도남긴다.

Ensemble이높아도해당회고적공통설계의기술적추가일뿐이고,같거나낮아도정보결합의한계로동일하게보고한다. 양쪽모두우월성/동등성/인과를자동주장하지않는다. STEP9B1R METHOD_NOT_VALIDATED가남아있으므로새금융p값/CI를붙이지않는다. 원형과수정pipeline 차이의모든요인별인과분해는2/3fit만으로완성되지않는다. 어떤방향도이번요청의신규금융실행승인이아니다.

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

재사용 조건: 최신F1 checkpoint의 원Train/Validation·피처/label·window·scaler·mask·유효Seed·환경·source가 bridge와 정확히 같음이 독립적으로 확인되면, 완료된 F1을 재학습하지 않고 동결 예측 재사용을 검토할 수 있다. 이 경우 세 모형 비교라도 신규 fit은 RAW5/LOG2의2개로 줄 수 있다. 어느 계약이든 다르면 동일 identity로 재사용할 수 없으며, 위3fit는 세모형 모두 새 공통계약으로 학습할 때의 제안이다. 지금은 그 동일성/승인/정보계약이 미확정이므로 어떤 예산도 활성화하지 않는다.
