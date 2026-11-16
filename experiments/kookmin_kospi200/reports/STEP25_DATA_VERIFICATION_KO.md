# STEP 2.5 데이터 검증

확인일: **2026-11-16, Asia/Seoul**. 기준 커밋: `81010974d4f56c5c02bc028af20e6bab356ae0e4`. 대상 브랜치/경로: `audit/kookmin-kospi200-20261116`, `experiments/kookmin_kospi200/`.

지정된 AUDIT·PROTOCOL·TEST_PLAN·STEP2 보고3개·cutoff/fold/gate manifest 및 구현을 먼저 읽었다. 기존 보고·원본·결과를 재작성하지 않았다. 모델/HMM fit, GPU, 모델 forward, checkpoint 로드, 패키지 설치는 **0회**다. 공식 소스·PyPI 배포물을 내려받아 텍스트/해시만 검사했다. 데이터 분석은2010-01-01~2025-12-31로 먼저 필터링했다. 현재2026년 문서는 절차/소스 참고자료로만 읽었으며2026 시장 관측을 입력/타깃에 쓰지 않았다.

## 판정 요약

| Gate | 증거 판정 | 실제 실행 gate | 확인 범위 / 남은 문제 |
|---|---|---|---|
| B01 | **PASS** | PASS | KRX 공식 연도별 휴장일과 평일 운영 규칙으로2010~2025 실제 세션3939개 확보 |
| B02 | **PARTIAL** | BLOCKED | 부재45개 모두 개장일·CSV 누락 확정. 각 날짜의 공식 KOSPI200 종가·실제 산출 응답 미확보 |
| B03 | **PARTIAL** | BLOCKED | KRX 제도·종가 정보상품 전송 안내 확보. 원본 CSV 공급처·수집·개정·18시 가용성 미증명 |
| B04 | **PARTIAL** | BLOCKED | 공식2021~2025 달력·조기폐장10개, 역사적 특이휴장·DST 규칙 확인.2010~2020 전체 달력·CSV 가용시각 미완 |
| B05 | **BLOCKED** | BLOCKED | 외국인 단위·시장범위·현물/선물·잠정/확정·공표/개정 불명 |
| B06 | **PARTIAL** | BLOCKED | 가공9개 열의 후보 계산식이3854행에서 수치상 일치. 생성 코드·개정·PIT 미증명, 기본 입력 제외 |
| B07 | **PARTIAL** | BLOCKED | 저장 출력torch2.10.0+cpu; ncps1.0.1과 고정 소스의 LTC 파일 동일. 실제ncps/hmmlearn 버전·checkpoint·단위 미확정 |

PARTIAL은 확인된 하위 사실이 있다는 뜻이며 실행 승인이 아니다. 전체 상태는 **BLOCKED**다. `manifests/step25_gate_results.json`이 현재 판정이며 STEP2 보고는 당시 상태로 보존했다.

## 1. B01 — 공식 KRX 세션

[KRX 공식 휴장일 화면](https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp)의 공개 조회 절차로 각2010~2025년 JSON 응답을 확보했다. 조회는 `gridTp=KRX`, `search_bas_yy=연도`, `bld=MKD/01/0110/01100305/mkd01100305_01`이며 CME/Eurex·야간시장을 쓰지 않았다. [KRX 매매거래 일반절차](https://regulation.krx.co.kr/contents/RGL/03/03010100/RGL03010100T1.jsp)의 월~금 운영 규칙에서 공식 휴장일을 제외했다. 일반 요일만으로 달력을 추정하거나 외국인 CSV를 공식 달력으로 대체한 것이 아니다.

16개 연도 응답은 공휴일·대체휴일·선거일·임시휴장·연말휴장을 포함한다. 예:2015-08-14,2016-05-06,2017-10-02,2020-08-17,2023-10-02,2024-10-01,2025-01-27/06-03. 각 응답의 추출시각·URL·매개변수·SHA-256은 `provenance/krx_calendar_provenance.json`에 있다. 원시 응답은 작업 환경에 보존하고 공개 저장소에는 가격 없는 날짜·출처 metadata만 저장했다. 페이지의 Eurex 재배포 제한 대상 자료는 조회·사용하지 않았다.

연도별 세션 수:2010 251,2011 248,2012 248,2013 247,2014 245,2015 248,2016 246,2017 243,2018 244,2019 246,2020 248,2021 248,2022 246,2023 245,2024 244,2025 242. 합계 **3939**. `krx_calendar_verification.csv`는 개장·휴장·주말을 분리하고 `krx_sessions_2010_2025.csv`는 순서가 고정된 session_id를 제공한다. 이 달력은 KRX 현물 정규 세션의 날짜이며 실제 가격이나 당시 공개시각의 증거는 아니다.

## 2. B02 — 45개 전수 대조와 label 영향

KOSPI의 기간내3894개 관측 날짜는 중복0·비거래일0이며, 공식 세션 중45개가 빠졌다. 이45개는 STEP2 외국인 비교로 발견한 날짜와 정확히 일치한다. `kospi_missing_dates_audit.csv`에 전수 기록했다. 개장 여부YES, KOSPI 파일 누락YES, 해당 날짜의 공식 지수 종가/산출 응답은UNKNOWN이다. 개장일이라는 이유만으로 지수 종가를 확인했다고 쓰지 않았다.

공식 가격 조회 `https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd`는 정상 공개 화면 경로·POST/GET에서 **HTTP400, 응답 LOGOUT**을 반환했다. 별도 index 화면도HTTP200이지만 실제 본문은 오류 화면이었다. [공식 Open API 이용방법](https://openapi.krx.co.kr/contents/OPP/INFO/OPPINFO003.jsp)은 인증키와 활용신청 승인을 요구한다. 접근 실패의 hash·URL·파라미터를 source catalog에 남겼다. 로그인·개인정보 제출·권한 우회는 하지 않았다. 대안은 승인된 KOSPI 시리즈 API, 또는 권한 있는 사용자의 공식 export와 출처 영수증이다.

보완 종가를 확보하지 못했으므로 `kospi_official_close_supplement.csv`는 헤더만 있고 **가격0행**이다. 원본 수정·가격 보간·ffill/bfill은 없다. 공식 캘린더로 재색인하면 중간45개 종가가 NaN이다. endpoint는 session_id+20으로 계산하며, 원본행 shift20과 endpoint 날짜가 다른 경우는 **664건**이다.

현재 원본 가격만 놓고 한 진단은 다음과 같다. 이는 공식 가격 대조나 최종 표본 인증이 아니다.

| 진단 | 수 |
|---|---:|
| 공식 세션 | 3939 |
| 원본 종가 관측 | 3894 |
| 기준일 종가 누락 | 45 |
| 기준일 종가는 있으나20세션 endpoint 종가 누락 | 41 |
| 기간 밖 horizon — 마지막 미확정 | 20 |
| 원본 기준일·endpoint 둘 다 있는 label 후보 | 3833 |
| 누락을 전파한 local feature-ready | 2781 |
| feature-ready이면서 label 있는 후보 | 2747 |
| t포함20window까지 유효한 후보 | 2467 |
| **공식 가격/PIT가 검증된 최종 모델 표본** | **미확정(null)** |

현재 feature-ready 수는 모델입력이 아닌 Log_Ret/Disparity/Vol_Regime의 날짜 자격 진단이다. 중간 가격 누락은 수익률·rolling40·window에 전파되므로 STEP2의 관측행 후보 수보다 감소했다. 이를 피하려고 누락을 채우거나 결과를 보고 제외 규칙을 바꾸지 않았다.

공식 달력의 마지막 관측 세션은2025-12-30, 마지막 확정 가능 기준일은2025-12-01이며 endpoint는12-30이다. **2025-12-02~12-30의20세션은 unknown**으로 유지한다. endpoint 날짜는 확인됐지만 해당 원본 가격의 공식 일치 인증은 B02/B03 해소 전 미완이다.2026 종가로 보완하지 않는다.

## 3. Rolling-Origin

공식 경계 날짜는 확정할 수 있지만 공식 종가·PIT가 미확정이므로 **최종 표본 수는 전 구간 빈칸**이다. 전체15구간은 `rolling_origin_manifest.csv`에 있다. 아래 수는 원본 미인증 가격으로 계산한 진단용으로만 표시한다.

| Origin | Train 종료 / Validation 범위 / Test 범위 | Train·Valid 진단 purge | Test 진단 후보 | Test 최대 label_end |
|---|---|---|---:|---|
| O1 | 2019-12-30 /2020-01-02~12-30 /2021-01-04~12-30 |20 /20 |247 |2022-01-28 |
| O2 | 2020-12-30 /2021-01-04~12-30 /2022-01-03~12-29 |20 /19 |125 |2023-01-31 |
| O3 | 2021-12-30 /2022-01-03~12-29 /2023-01-02~12-28 |19 /20 |245 |2024-01-29 |
| O4 | 2022-12-29 /2023-01-02~12-28 /2024-01-02~12-30 |20 /20 |244 |2025-02-04 |
| O5 | 2023-12-28 /2024-01-02~12-30 /2025-01-02~12-30 |20 /20 |222 |2025-12-30 |

모든 Train 시작은2010-01-04다.19건인 경우는 경계를 넘는20개 중1개가 endpoint 종가 누락으로 이미 unknown이어서, 알려진 label에서 실제로 제거한 수가19개라는 뜻이다. 규칙은 항상 train.label_end<valid_start, valid.label_end<test_start다.2021~2024 test의 horizon은 다음 해로 넘어갈 수 있으나 모두2025-12-31 이내다.2025 test는 마지막20개를 제외한다.

## 4. B03 — 종가와18시 가용성

원본 바이트의 기존 저장소 파일과 동일성은 확인되지만 이는 공급처 인증이 아니다. 노트북은 CSV를 읽기만 하고 수집 코드를 포함하지 않는다. float 표현·열 이름만으로 Yahoo 또는 KRX 추출이라고 확정하지 않았다. 공식 종가와3894개 원본 수치의 전수 비교도 미완이다.

KRX [종가 정보상품 안내](https://openapi.krx.co.kr/contents/OPP/DATA/OPPDATA002.jsp)는 주간종가 전송을16:00/18:10 등으로 구분한다. 이것을 첨부 CSV의 available_at으로 대입하지 않았다.15:30 정규장 종료, 지수 산출·수정 확정, 공급처 게시, 사용자의 수집완료는 서로 다른 사건이다.18:00 계약에서 어떤 버전을 쓸 수 있었는지 원천 영수증/개정정책이 필요하다. 현행 안내는 전체2010~2025 공급처 정책을 소급 증명하지 않는다.

## 5. B04 — 미국 달력·시각·mapping

[Nasdaq 공식 달력](https://www.nasdaqtrader.com/Trader.aspx?id=Calendar)에 연결된2021~2025 PDF를 확보했다. 범례의 휴장/13시 조기폐장을 색·좌표로 추출해 확인했고2025-01-09는 별도 [Carter 휴장 공지](https://www.nasdaqtrader.com/TraderNews.aspx?id=ETA2025-1)를 추가했다. 공식 시장 세션 수는 연도별252/251/250/252/250, 조기폐장은 총10일이다.2010~2020 연간 PDF 후보 URL은HTTP200이어도 실제는HTML 오류 페이지였으므로 성공으로 처리하지 않았다.2010-11-26·2020-11-27 조기폐장과Sandy/Bush 특이휴장은 별도 공식 공지로 확인했지만 전체 구간 달력 완료를 뜻하지 않는다.

[NIST DST 규칙](https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst)과America/New_York 시간대로2010~2025 전환주간64개 시각 probe를 검증했다. 정규16시의 한국 환산은 다음날05시/06시,13시 조기폐장은02시/03시다. probe는 시각 변환 확인이며 그 날짜의 개장 여부를 별도 증명하는 데이터가 아니다.

공식 달력이 검증된2021~2025 중 한국18시 의사결정에 앞선 미국 세션을 지정할 수 있는 날짜는1224개다. 해당 범위에서 시장 종료 기준 candidate와 다른 선택 날짜는 same-date+ffill1184건, 한국행 결합 후shift1 52건, 미국 source행shift1 후결합42건이다. 정확한 정의는 mapping_summary에 고정했다. 값이나 성능 비교는 하지 않았다. 한국/미국 휴일이 달라 단순shift가 달력 결합을 대신하지 못한다.

`us_market_availability_audit.csv`는 전체3939개 KRX 날짜의 mapping을 저장한다. Nasdaq/SOX 파일의 날짜 배열이 동일해 한 행에 두 변수를 표시했다.2021 이전 또는 직전 검증 세션이 없는 날의 candidate는 빈칸이다. **provider_available_at와 production_PIT_date는 전 행 빈칸**, input_status는BLOCKED다. 최신 완료 시장 세션은 공개지연0을 가정한 실제PIT 선택이 아니다.

공식 [COMP 방법론](https://indexes.nasdaq.com/docs/Methodology_COMP.pdf)과 [SOX 방법론](https://indexes.nasdaqomx.com/docs/methodology_SOX.pdf)은 종가 수정 가능 구간과 지수 전파를 장 종료와 구분한다. 확보한 문서가 현행본임을 명시하고 이를2010~2025 공급처 정책으로 소급하지 않았다. [역사적 조기폐장 feed 안내](https://www.nasdaqtrader.com/content/technicalsupport/dataproducts/GDPEarlyCloseSchedule.pdf)도 시장 종료·지수 settlement·feed 종료가 다름을 보여준다. 공급처 공개지연은UNKNOWN이며0으로 채우지 않았다.

시장 종료 candidate의 미래 schedule 삭제에 대한 과거 mapping 불변성은PASS다. 실제 CSV의 provider-PIT 미래 perturbation은 release 자료가 없어BLOCKED다. 양자를 같은 검증이라고 쓰지 않았다.

## 6. B05·B06 — 외국인과 가공파일

외국인 파일에는 날짜·개인·외국인·기관만 있고 scope/unit/release/revision 설명이 없다. 수집 코드는 찾지 못했으며 KRX 날짜와 일치한다는 이유로 KOSPI 현물·억원으로 인증하지 않았다. 당일 사용은 금지다. A(외국인 제외)는 기존 사전 지정 피처 사양 안에서 검토 가능하지만 다른 gate를 면제하지 않는다. B(이전 세션)는 실제 공개시각을 확인해야 사용 가능하다. 결과를 보고 A/B를 고르지 않았고, 이번에 임의로 주 분석을 바꾸지도 않았다.

가공파일의 KOSPI200/Vol/Foreigner/Nasdaq/SOX와4개 파생변수는 모두 원본의 관측행 기반 결합·ffill·rolling/shift 후보식과3854행에서 수치상 일치했다. `processed_formula_verification.json`에 식·오차·입력해시를 기록했다. **생성 코드를 발견했다는 뜻은 아니다.** 시차 결함과20행 horizon 문제를 그대로 물려받을 수 있어 기본 실험에서 계속 제외한다. 파일은 재생성하거나 덮어쓰지 않았다.

## 7. B07 — LTC·버전

원본3개 노트북의 저장된 셀2 출력은Python3.12.0·Torch2.10.0+cpu·CUDA=False다. 이번 실행환경으로 다시 확인한 결과가 아니며 ncps/hmmlearn 버전은 기록돼 있지 않다. 저장소 requirements도 버전을 고정하지 않는다. 새 런타임을 이 기록만으로 재현 가능하다고 인증하지 않았다.

[공식 ncps 소스 고정 커밋](https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py)과 [PyPI ncps1.0.1](https://pypi.org/project/ncps/1.0.1/) 배포물을 설치하지 않고 검사했다. 배포 wheel의SHA-256을 검증했으며 LTC wrapper/cell 파일이 고정 커밋과 바이트 단위로 동일했다. 단, 원본 노트북이 실제 이 버전을 썼다는 증거는 아니다.

cm은 capacitance, gleak는 leak conductance다. 입력 affine mapping·sensory/recurrent sigmoid gate·sparsity·양수 제약을 거쳐 τ_raw=cm/gleak, τ_effective=cm/(gleak+sensory+recurrent conductance)로 계산한다. 이는 상태를 고정한 conductance 시간상수이며 전체 비선형 Jacobian의 고유시간상수나 경제적 인과 기억길이와 동일하지 않다. elapsed_time을6개 solver substep으로 나누고 내부 cm/(dt/6)를 쓰며, timespans 생략 시 dt=1.0이다. 이1이 초/영업일이라는 물리적 해석은 입력 계약 없이는 확정할 수 없다. 실제 substep별 은닉상태가 달라 유효τ도 달라질 수 있다.

확인한 중요 차이: **LTC wrapper는 implicit_param_constraints=True, LTCCell 직접생성 기본값은False**다. STEP2 τ 인터페이스가False를 기본 가정하지 않도록 explicit bool을 필수로 만들었다. 실제 모델은 실행하지 않았고 합성 snapshot 검사만 재실행했다. checkpoint 호환성은 shape/key·wiring·mapping·constraint·버전 metadata를 받은 뒤 STEP3 승인 후 검증할 항목이다.

## 검증·보존

STEP2 회귀23개 및 STEP2.5 새 검사11개, 합계 **34 PASS/0 FAIL**. 공식 달력 해시·45개 전수·실제20세션endpoint·2022 경계·DST64·earlyclose10·미래schedule 불변·unknown 가용성·제약모드 차단을 확인했다. source URL·확인일·판정 기준·한계는 source catalog와 개별provenance에 있다. 개인정보·원본CSV·전체 notebook 소스·공식가격·유료자료·원문PDF/wheel은 공개 브랜치에 게시하지 않는다. 기존 V14/V15·lock·워크플로·main 변경은 없다.
