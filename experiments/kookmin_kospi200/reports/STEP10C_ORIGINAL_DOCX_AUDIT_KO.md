# STEP10C 초기 DOCX 원문·식별·버전 검증

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

## 파일 확보와 정상 열기

제공파일명: `[국민대 학위논문 체제] LNN 앙상블 기반 KOSPI 200 지수 방향성 예측 모델에 관한 연구 (박사학위논문).docx`.

실제 로컬 attachment 경로와 원본identity는 비공개 완료기록에 남겼다. 공개보고서에 attachment UUID·사용자 개인이름·비공개경로를 게시하지 않는다. 크기 **99,238 bytes**, ZIP CRC 검사 PASS, document.xml/관계 구조 읽기 PASS다. python-docx Document로 실제 열어 **516개 본문문단 / 13개 물리표 / 1개 section**을 확인했다. Word GUI 렌더링이나 인쇄 페이지의 정확성까지 검증했다는 뜻은 아니다.

패키지에는 docProps/core.xml이 없으므로 created/modified/revision/version은 **UNKNOWN**이다. 내부 버전을 만들어 넣지 않았다. 본 감사의 수신본 식별자는 `STEP10C_DOCX_RECEIVED_v1`과 위 byte SHA이며, 이는 문서의 원래 작성버전·최초작성일을 인증하는 표기가 아니다. 수신본이 사용자 제공 원문이라는 사실과 그 이전 편집이력은 구분한다. 원본을 수정하지 않았다.

## 요청 절·표의 실제 추출

| 대상 | 원문 anchor | 추출·대조 상태 |
| --- | --- | --- |
| 제4.3절 5Seed성능 | P0357~P0360, T007(표6) | 원문추출완료; 모델평균66/66 직접일치, SD표시반올림호환66/66 |
| 제4.6절 McNemar | P0368~P0371,T010(표9) | pooling수정·대표Seed·n759·비중첩38의 서술확인; 실행코드연결미확인 |
| 제4.7절 1/10Seed | P0372~P0378,T011/12(표10/11) | 동일Seed재현 및 per-Seed검정 주장추출; 보존Notebook와 versiongap |
| 제4.8~4.10절 | P0379~P0396,T013(표12) | 강건성/비유의/Seed빈도/한계 문장원문추출 |
| 표7 수동레짐 | P0361~P0363,T008 | 포함19행의95지표 셀 일치; 전체33행중 발췌 |
| 표8 HMM레짐 | P0364~P0367,T009 | 포함6행의36지표 셀 일치; 전체22행중 발췌 |

정확한 문장과 표를 원래 순서·표시값 그대로 비공개에 추출했다. public에는 원본 전체 DOCX나 상세금융표를 업로드하지 않는다. 문서에 pykrx 수집(§4.1 P0351),62.06% 상승편중(§4.2 P0356),Test2022~2025(§2.27 P0326/§5한계 P0447)라는 **서술이 존재**함을 확인했다. 원 공급처 취득로그·code/SHA 연결이 검증됐다는 뜻은 아니다.

## STEP10B에서 해소된 공백과 남은 공백

DOCX_NOT_AVAILABLE과‘그 문장이 있는지’는 해소됐다. 실제‘LNN은CfC셀’ 서술과대표Seed/비중첩 검정 수정 서술을 이제확인할수있다. 반면 논문작성버전↔실행소스↔예측·날짜·환경 아카이브 연결은 아직 미확인이다. 이번 파일존재 PASS를 초기1Seed 독립재학습재현 PASS나 historical PIT PASS로 확대하지 않는다.

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
