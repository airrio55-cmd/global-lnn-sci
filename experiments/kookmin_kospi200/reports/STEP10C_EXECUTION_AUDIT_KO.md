# STEP10C 실행·원문 추출·보존·공개 감사

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

## 실제 파일과 정상 열기

첨부를로컬에다운로드한원파일은99,238bytes, SHA-256 `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`다. 실제attachment 경로는privateidentity기록과최종사용자링크로확인가능하다. 원문을변환/다시저장하지않았다. ZIP CRC,Word XML/관계파싱및python-docx열기로516문단·13표·1section을확인했다. docProps/core.xml이없어버전/작성일은UNKNOWN으로기록했고임의로값을생성하지않았다. 추출기의초기선택적속성가정은없는속성을UNKNOWN으로처리하도록정정했으며원문/금융코드는바꾸지않았다.

제4.3/4.6/4.7/4.8~4.10과논리표6~12의원문을그대로private JSON/text에추출했다. 문서물리표번호와논리표번호를구분했다. 개인이름·서명·표9/11의개별대표Seed 통계·체크포인트/입력매핑·classsupport·원자료·일별label/확률은공개하지않는다. 원DOCX전체는GitHub에업로드하지않는다.

## 수행한 비교와 수행하지 않은 계산

기존자료104개source entries와Notebook3개를정적으로검토했다. sourceSHA로cached Notebook가현재원본과같음을대조하고현재최종LTC/CfC/FocalLoss정의를기존master와연결했다. Word표6평균66개·SD66개,표7지표95개·표8지표36개를 **기존표시문자열**로대조했다. Decimal의3자리반올림호환검사는SD생성·금융metric재계산이아니다.

표9~12의수정대표/개별Seed/n38 검정은원문서술을확인했을뿐실행하지않았다. 모델/checkpoint/금융NPZ·NPY를수치로읽지않고원예측을재평가하지않았다. 새NN/Logistic/HMM fit·forward·τ·통계/p값/CI·Test예측·Ensemble·GPU·2026가격사용은0이다. 문서의데이터수집·기간·재현주장을그대로받아PIT를PASS로올리지않는다.

## 기존자료 보존과 신규경로

시작snapshot의기존 project **10,097개 파일**을종료때byte SHA로다시대조한다. 원DOCX의처음SHA도종료때재확인한다. STEP10/10B 보고서·manifest·학습/예측/평가·checkpoint와현재master flags는수정하지않는다. __pycache__외기존일반파일전체를포함하며NN500/Test500,baseline40,STEP5C600,HMM100/선택10,보완τ100의기록을유지한다. JOF다국가연구와표/주장을혼합하지않는다.

새repo파일은요청된STEP10C 보고서9개뿐이다. 전체원문·상세금융표·세부대조표·작업로그·byte snapshot은로컬private scratch에남기고공개allowlist에서제외한다. 이전자동승인에서거부된상세금융표/operational config/내부inventory를재전송하지않는다. source개별금융결과와원τ99→100에서singleton을역산할수있는새값을넣지않는다.

remote audit최신SHA를확인한expected_sha 보호로9개신규보고서만commit/push하며main·기존파일을보존한다. actualcommit은별도완료receipt와최종보고로연결한다. 종료보존·범위·공개검사결과는아래에기재한다. 원문읽기PASS와실행버전/재현성미확인·PIT BLOCKED를분리한다.

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

최종 종료검증: 기존 project 10,097개 파일의byte SHA 변경0, 원DOCX SHA 변경0, 신규repo경로는보고서9개뿐이다. 정상열기·원문/표대조·보존·범위·공개검사 52 PASS /0 FAIL이다. 이PASS는수정된대표Seed/n38 실행재현,SD작성과정,당시공급처/PIT의확증을뜻하지않는다. 해당 항목은DOCUMENT_REPORTED/UNKNOWN/BLOCKED로유지한다. 금융fit/forward/draw/pvalue/CI0이며후속학습은자동시작하지않는다.
