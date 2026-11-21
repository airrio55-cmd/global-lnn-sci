# STEP10C 초기 LNN·LTC·CfC 정체성과 문서 수정안

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

| 원문위치 | 확인한문장/서술 | 실제보존코드 | 판정 |
| --- | --- | --- | --- |
| §2.9 P0223 | “본 연구의 LNN 구현은 CfC 셀을 사용하므로” | 세Notebook 최종cell8 LNNModel의self.ltc=LTC(...) | 동일버전가정에서명시적모델정체성불일치 |
| §3.2 P0344 | “각각 별도의 CfC 네트워크에 입력하여” | cell14 LNN Single=r_lnn, r_lnn은LNNModel/LTC_RAW5 | RAW/LOG 두LTC를CfC로설명한문장수정필요 |
| §5.1 P0441 및요약 | “LNN의 CfC 구조”라는서술 | 최신F1도같은LNNModel source를2피처로사용 | LTC진단τ와CfC이론을동일실행모델로혼합금지 |
| 원Notebook 앞선cell7 | LNN참조구정의 | 이후cell8에서LTC정의로덮임 | 앞선class만인용해CfC로인정할수없음 |
| 별도CfC Single/Ensemble | 원문도별도비교모델로열거 | 별도CfCModel.self.cfc=CfC(...) | CfC와LTC는다른셀/기본구조 |

STEP10B에서‘원문CfC서술존재’는미확인이었으나이제직접확인됐다. 제공Notebook의현재순차실행사양과문서가동일실험을설명한다는전제에서서술–코드불일치는확정적이다. 다만문서통계수정버전의실행코드가별도로있을가능성을배제할수없으므로문서작성자가실제로어떤weights를실행했는지독립재현한것은아니다.

세원본과최신master의최종모델정의AST SHA는일치한다. LNNModel은LTC이며정의SHA `ff2ec3b49fb1a96848b9a51aec6dbf4abfac5efdb02fa8fa10f48da77a7e0a7b`, 별도CfCModel은 `2907b0ff7cc2dd6da70b9f9da189004de8f5e2d1fd8f2a06d14aeb26f438ebef`다. 초기LNN Single=RAW5 LTC, Ensemble=RAW5/LOG2 LTC확률0.5:0.5다. 최신F1 LTC는동일core정의이지만2피처·다른기간·window정보·scaler/선택단위이며원형LOG402와도유효Seed identity가다르다. 동일계열/소스가동일학습모델/실험을뜻하지않는다.

### 논문 수정 제안 — 원문 자체는 변경하지 않음

“제공 실험 코드에서 LNN Single은 ncps.torch.LTC 셀을 이용한 다변량 입력 모형이며, LNN Ensemble은 RAW5 LTC와 LOG2 LTC의 상승확률을 동일가중 결합한 모형이다. CfC Single/CfC Ensemble은 ncps.torch.CfC를 사용하는 별도 비교모형이다. LTC와 CfC는 연속시간 신경망 계열이지만 실행 셀과 계산 방식이 다르다.”

§2의LTC/CfC일반이론은분리해유지할수있지만§3방법·§4결과·§5결론에서실제LTC를CfC폐쇄형솔버없는구조로설명해서는안된다. 당시ncps버전/수정코드·가중치가제공된뒤실험버전연결을최종확인해야한다. 최신τ100은LTC conductance의model_observation_step 진단이며초기CfC라는서술을정당화하는증거가아니다.

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
