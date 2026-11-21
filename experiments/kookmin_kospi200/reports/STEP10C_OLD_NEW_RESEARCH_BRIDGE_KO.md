# STEP10C 초기–최신 일관성 및 직접비교 범위

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

| 범주 | 대상 | 근거 | 해석제한 |
| --- | --- | --- | --- |
| A 직접비교가능 | 같은숫자/정의/서술의문서대조 | 표6저장평균·표7/8포함셀,RAW/LOG동일가중식,공통최종class source | 추론이아닌증거대조에한정 |
| B 제한적비교 | 정보설계·예측성향·기술적안정성의방법론논의 | 같은LTC계열,동일nominalhyperparameters,반복Seed의개념 | 표본·입력·환경/선택차이를병기;수치효과분해아님 |
| C 직접비교불가 | 초기5Seed 단일Test BA와최신5Origin/10Seed BA | RAW5/LOG2 대F1_2,다른시점/기간/Target·달력/집계 | 평균차이를성능개선/악화로해석금지 |
| D 증거부족 | 원문수정대표Seed·n38검정의독립재현,공급처/PIT/실행버전 | 수정코드/날짜/예측/SHA·배포수신로그미확보 | 문서보고확인은가능하나실행타당성PASS불가 |

## 원문 확보로 새로 확인된 설계·기록 차이

- **통계버전:** Word§4.6은과거Seed연결의문제를인정하고대표Seed 검정으로고쳤다고명시한다. 제공5/10Seed Notebook은여전히연결검정이다. 초기논문전체를‘현재도pooled결과만사용’한다고묘사하면부정확하다. 그렇다고수정Word표와제공코드를동일재현물로인정할수도없다.
- **수집·기간:** Word§4.1은pykrx,2010~2025를기술하지만그수집로그·버전·원응답SHA는없다. 제공CSV조합의과거진단은2026포함/관측행split이었다. 이는문서–제공데이터의lineage공백이며지금2026가격을읽거나당시논문에반드시포함됐다고단정하지않는다.
- **분할:** Word§2.27은Train2010~2018/Validation2019~2021/Test2022~2025,§4.1·표4는60/20/20과유효2340/780/759를기술한다. 제공코드의60/20/20 및기존진단의유효2317/759/759와정확히같지않다. 근사표기인지다른실행버전인지확인해야한다. n759일치만으로같은날짜·Target을인증할수없다.
- **early stopping:** Word§2.19 P0301/§4.1 P0353은validation loss를기준으로쓰지만최종코드cell8·12는Validation BA 최대화다. 원실행이앞선정의인지최종정의인지version연결없이문서만고쳐실행사실을만들지않는다.
- **HMM학습범위:** Word§3.1 P0335는전체분석기간학습을쓴다. 제공5/10코드는Train데이터에fit한후Test전체predict/Viterbi·Test이름/medianfallback을사용한다. 최신은Train-onlyfit/명칭·forwardfilter다. 문서/코드/최신3수준의차이를분리한다. HMM은후처리이므로이차이만으로NN기본BA변화를설명하지않는다.
- **미국시장시차:** Word§2.17.3 P0289는직전미국거래일정렬과누출방지를기술하나제공cell9는날짜join/ffill/bfill이다. 입력window가t-1까지라일부정보가용성은의사결정시각에따라달라질수있지만공급처as-of/PIT가입증된것은아니다.

## 최신 결과의 위치

최신은F1=[Log_Ret,Disparity],5Origin×A/B×10Seed×5NN의500fit/500Test다. 각Origin Seed지표평균뒤5Origin동일가중,공식20session label,2025끝20UNKNOWN,명시purging·Train-onlyscaler·t포함window다. 원문에기술된RAW5/LOG2 Ensemble은이500에서실행되지않았다. 최신τ100과baseline40도초기논문표의재산출물이아닌후속versioned분석이다.

동일broad연구주제안의설계변경·보완연구로연결할수있지만동일실험의단순재현성실패또는성능하락으로판정하지않는다. 원문원천과수정통계아카이브를받아도같은Test/Target/집계가되지않으면직접수치우열비교는C로남는다.

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
