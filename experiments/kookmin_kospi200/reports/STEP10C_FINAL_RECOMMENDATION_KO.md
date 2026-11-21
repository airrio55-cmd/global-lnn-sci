# STEP10C 최종 권고 및 다섯 질문의 답

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

| 질문 | 확인된 사실과 최종 답 | 남은 공백 |
| --- | --- | --- |
| 1. 초기1/5/10 수치는Notebook와일치하는가? | 5Seed 표6 학습모델 평균66/66,SD66/66이3자리표시반올림과호환. 표7/8 포함셀95/95·36/36일치. | 1Seed재실행·10Seed개별/대표검정은Word서술확인일뿐수정코드/원예측독립재현은미확인. 기준선3개도sourcegap |
| 2. 초기LNN정의와LTC구현이일치하는가? | 제공Notebook기준불일치:Word는CfC셀,최종활성코드는LTC. 별도CfC모델도존재. | Word수정실행버전/가중치가다른지연결필요. 같은LTC계열이라도RAW5와최신F1은동일학습모델아님 |
| 3. 결과차이의핵심설계변경은? | 단일Test→5Origin,RAW5/LOG2→F1,window t제외→포함,관측행→공식session label,기간/purge/scaler/집계/검정단위변경. | 성능차이의인과기여분해없음. 직접BA차감으로개선/악화라할수없음 |
| 4. 방향A/B중현재증거에맞는것은? | 추적가능한현재실행범위/RQ를근거로A(최신F1·안정성·레짐·LTCτ)권고. 성능이높아서선택한것아님. | 제목/RQ는지도교수최종검토. B를핵심으로유지하려면version/외부data/정보계약과추가효과근거필요 |
| 5. 추가실험은꼭필요한가? | A의기술·탐색적집필과문서정정에자동필수아님. B의원형추가효과claim에는조건부bridge필요. | 현재실행BLOCKED_PENDING_EVIDENCE. 최소2fit(원형Single/Ensemble) 또는3fit(F1포함)/한가격/한기간/한Seed제안;별도승인전0실행 |

## 교수 검토용 통합 결론

초기논문은원형앙상블의모든지표일관우월성을이미유보하고대표Seed·비중첩 검정으로초기pooling 문제를수정했다고기술한다. 그수정의도를인정하면서도제공Notebook에수정script가없다는version gap을명시해야한다. 원문CfC모델서술과LTC실행코드는정합이필요하며,SD차이는실험성과변화라기보다일관된표시반올림으로설명가능하다.

현재500결과를초기결과의단순성능하락/재현실패라고볼수없다. 서로다른데이터·정보·평가설계이므로동일하게맞춘새bridge 없이는직접우열을정하지않는다. 현재실행근거에맞는F1진단연구를주결과로,원형은한계와보완과제를붙인Historical Baseline으로구분하는방향A를권고한다. 원형Ensemble의기여가학위논문의핵심이면별도증빙/사양/승인을받아B의bridge를검토한다.

기존NN500/Test500·baseline40·HMM100/10·STEP5C600·τ100과원실패/복구기록은보존한다. 가격/PIT 및통계타당성차단은유지하고추가학습·추론·검정을자동시작하지않는다. 문서파일확보로STEP10B의‘원문미확보’만새version에서해소했으며이전보고서를소급수정하지않았다.

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
