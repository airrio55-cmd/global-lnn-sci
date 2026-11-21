# STEP10C 표6~12 원문·Notebook 저장결과 검증

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

| 논리표/물리표 | Word내용 | 보존Notebook대조 | 최종범위 판정 |
| --- | --- | --- | --- |
| 표6/T007 | 5Seed 전체11학습모델 및3단순기준선 | 학습11×6 평균66/66 exact, SD exact9/66·3자리반올림호환66/66 | MODEL_MEANS_MATCH; DISPLAY_ROUNDING_COMPATIBLE; 기준선3개는코드아카이브미확인 |
| 표7/T008 | High11모델/Mid4/Low4의발췌19행 | 5Seed cell16 포함95지표셀95/95 일치 | INCLUDED_CELLS_MATCH; 생략행을0/실패로추정하지않음 |
| 표8/T009 | 2HMM상태×RNN/LNN Single/LNN Ensemble=6행 | 5Seed cell17 포함36지표셀36/36 일치 | INCLUDED_CELLS_MATCH; HMM학습범위서술은별도불일치 |
| 표9/T010 | 대표Seed의759고유날짜 McNemar와Bonferroni/BH | 제공5Seed cell18은연결pooled검정 | DIFFERENT_STATISTICAL_ARTIFACT; 수정코드·원예측미확보 |
| 표10/T011 | 10Seed별개별검정의median Statistic/p·유의Seed수 | 제공10Seed cell18은pooled출력 | DOCUMENT_REPORTED_NOT_CODE_REPRODUCED |
| 표11/T012 | 대표Seed92의759날짜검정 | 제공10Seed pooled아카이브와동일출력아님 | DOCUMENT_REPORTED_NOT_CODE_REPRODUCED |
| 표12/T013 | 1Seed재현/5Seed주실험/10Seed확장/n38비중첩의역할 | 개념적주장과실행version연결을구분 | TEXT_CONFIRMED; fresh재현검사NOT_RUN |

## SD 차이의 증거 기반 판정

표6의 LNN Single은 BA `0.5420±0.0260`, Macro F1 `0.5305±0.0400`이고, 5Seed cell15 저장출력은 같은평균과SD `0.0258 / 0.0404`다. 11모델의66개평균이모두같고66개SD전체가 다음표시연산과호환된다.

`Notebook에표시된4자리SD → 소수3자리ROUND_HALF_UP → 소수4자리로표시`

예컨대0.0258→0.026→0.0260,0.0404→0.040→0.0400이다. exact로같은SD는9개이고나머지도이규칙으로설명된다. 원예측으로SD를계산하지않고기존숫자문자열과Decimal 표시규칙만대조했다. 원본cell15의np.std는ddof=0이다.

판정은 **표시반올림으로설명가능한일관된패턴(가장직접적인설명)**이다. 그러나원시SD·문서buildscript·수정로그가없어실제편집자가그절차를썼다는사실까지입증한것은아니다. 금융실험버전이달라SD가변했다고볼직접증거는없고,정밀도차이를곧기술오류로판정할근거도없다. ‘반올림호환’과‘작성과정확정’을구분한다. 원문숫자는수정하지않는다. 논문보완안은“SD는원시값에서일관된소수자리로반올림하며ddof를명시”하는것이다. 원시값미확보상태에서노트북표시값을원시SD로대체하지않는다.

표7·8은 **문서에실린부분**만일치한다. 모든모델·레짐을전부확인했다거나대표행선정의중립성이입증됐다고확대하지않는다. 표6기준선3개,표9~11수정통계및n38검정의원코드/예측아카이브가필요하다. 기존Notebook통계의pooled출력과Word수정대표Seed표를같은표라고섞지않는다.

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
