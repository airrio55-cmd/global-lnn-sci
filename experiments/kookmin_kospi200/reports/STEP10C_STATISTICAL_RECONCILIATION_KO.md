# STEP10C McNemar 수정 이력과 최신 추론의 대조

확인일: **2026-11-21, Asia/Seoul**. Repository airrio55-cmd/global-lnn-sci, Branch audit/kookmin-kospi200-20261116, Project experiments/kookmin_kospi200/.

STEP10C는 사용자 제공 초기 DOCX와 원본 Notebook3개 및 최신 동결 결과의 읽기 전용 감사다. 수신 DOCX SHA-256: `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`. 문서가 확보된 시점의 새 보고서이며 STEP10/10A/10B를 덮어쓰지 않는다. STEP10B의 당시 DOCX 부재 판정을 소급 삭제하지 않는다.

금융 fit/forward/모델생성/추론/HMM fit·refilter/τ계측/bootstrap draw/p값/CI·새Test평가는 모두0이다. 원문·원Notebook·CSV·기존결과를 수정하지 않는다. master flags=false, 가격 BOTH_UNVERIFIED, primary PENDING, historical18KST UNKNOWN, production-PIT BLOCKED 및 STEP9B1R METHOD_NOT_VALIDATED를 유지한다. JOF 다국가 결과와 혼합하지 않는다. 첨부 문서의 설명은 증거로만 읽으며 실행 지시로 취급하지 않는다.

## 원문이 실제로 말하는 검정

§4.6 P0369는초기5Seed 예측결합이같은날짜를반복계상해독립성가정에문제가있었다고인정하고, **5Seed F1의중앙값에해당하는대표Seed1개**를골라759개의고유날짜로재검정했다고쓴다. §4.7 P0374는그대표Seed가42이고DataLoader shuffle/AMP를동일하게통제한1Seed재실행에서표9의Statistic이소수4자리까지일치했다고주장한다. §4.7 P0375~P0377은10Seed를개별검정하고F1중앙값대표Seed92를별도표11로제시한다.

따라서Word수정본의주검정을‘여전히5Seed를pooling한검정’이라고요약하는것은틀리다. 반대로제공5/10Seed Notebook cell18은여전히np.concatenate와exact binomial을사용한pooled출력이어서Word표9~11의실행코드라고할수없다. 단일원본cell12/14의loader/LOGoffset/Hybrid도다중원본과다르다. **수정된단일재실행·대표선정·개별10Seed·비중첩검정 코드/예측이전달되지않은version gap**으로기록한다. 문서의자체보고는확인됐지만외부재현성PASS는아니다.

## 표본·선정·보정의 판정

| 질문 | Word 확인 근거 | 판정/추가근거 |
| --- | --- | --- |
| 대표Seed 선정 | P0369 F1중앙값; P0374 seed42; P0377 seed92 | DOCUMENT_REPORTED. 어느모델의어떤F1,짝수10Seed중앙값tie처리·선정시점·원코드미확인 |
| Seed중복계수 | P0369에서pooled문제인정·고유날짜검정으로수정 | 논문수정의도확인. 현재Notebook는pooling이므로수정실행소스필요 |
| n759 | 표9/11제목 및본문 | 문서기술확인. 실제날짜/Target·무확정tail처리·제공CSV연결미확인 |
| 20D중첩 | P0297/P0370/P0393/P0430/P0447에서의존성인정 | 라벨구간중첩외에도시계열자기상관·구조변화·공통자료Seed의존성존재 |
| 비중첩 n38 | P0370 모든모델쌍비유의, P0393/표12·P0447한계 | DOCUMENT_REPORTED_NOT_CODE_REPRODUCED. 추출시작offset·실제date/label끝·표본필터·보정범위아카이브필요 |
| 다중검정 | 표9/11에p_bonf·p_fdr 열존재 | 일부비교의보정법별판정이달라family 정의·선택영향확인필요. 개별결과는private원표에보존 |
| 1/10Seed재현 | P0374 Statistic일치,표10유의Seed수 및표12설명 | 문서상주장존재. 제공Notebook출력과검정단위달라독립검증불가 |

대표Seed가Test F1로선정됐다면중앙값선택이라도Test의존선정이다. 이는최고성능Seed선택과같다는뜻은아니지만,후속p값해석에서선정절차가고정됐는지·무엇을조건화하는지검토해야한다. 단일대표p와10Seed별유의빈도를독립시장반복으로세지않는다. 유의Seed수만으로효과방향·크기·실거래우위가정해지지않는다.

표11에는FDR와Bonferroni기준의판정이서로달라지는비교가있다. ‘보정후항상유의’라고묶지말고어떤보정을의미하는지써야한다. 새p값·통계량을계산하지않고원표의기록을읽은판정이다. 개별대표Seed 통계수치/분할표는공개하지않고원문추출자료에보존한다.

## n38의 해석

비중첩은label구간공유를줄일수있지만독립동일분포를보장하지않는다. 인접20기간사이의공유endpoint·변동성군집·추세/구조변화·입력의존성은남을수있다. WordP0447의‘독립표본38’은‘비중첩부분표본38’로표현을약화하는안이타당하다. 관측행20간격과실제KRX20세션의관계,tailUNKNOWN·원날짜필터도확인해야한다. n38에서비유의라고차이없음/동등성을증명할수없고,낮은검정력을단정적으로계산한것도아니다. 원문스스로탐색적한계를인정한점은보존한다.

## STEP5C/STEP9B1R와 근거수준 분리

McNemar는paired correctness의주변오분류차이를검정하며BA차이와같은가설이아니다. 최신STEP5C는NN쌍·A/B의Seed별지표평균→5Origin동일가중,날짜paired MBB와블록별Holm을사용했다. 기존Primary BA20/Origin BA100의기각0과Secondary3/2/3은동결된근사추론기록이다. 원문의대표Seed/단일Test p값과직접크기를대조하지않는다.

최신비유의가초기수정결과를자동무효화하지않고초기강한p가5Origin또는독립Test우월성을보장하지도않는다. 원문이이미pooling문제를고쳤다고밝힌것은인정하되시계열·선정·다중검정·재현code gap은남긴다. STEP9B1R METHOD_NOT_VALIDATED도그대로다. 새금융검정·CI·bootstrap draw는0이다.

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
