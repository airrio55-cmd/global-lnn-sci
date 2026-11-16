# CHANGELOG — draft

## 2026-11-16 / 준비·정적 감사

추가: 별도 프로젝트 경로, 원본 노트북3개·CSV5개의 manifest, 18셀 비교·diff·행번호 증거, 데이터 inventory, 실제 Target/fill/split 재현, 데이터 전용7개 regression 검사(PASS), 심각도별 감사, 수정안·Rolling-Origin·피처 ablation·HMM 분리·LTC 시간상수 프로토콜, 수정 전후 테스트 계획, 실행 비활성 config.

보존: 원본8개 바이트와 해시. V14/V15 Journal of Forecasting 실험, 기존 잠금 파일, main 및 워크플로 미수정.

미구현 제안: nullable20일 target, PIT/as-of 데이터 가용성, flow 결측 정책, date-key split 및 purging, 통합 모델·AMP·seed·Hybrid 사양, forward HMM filtering·train-only 임계값·collapse 처리, 시드 의존성을 반영한 block 통계, LTC 유효 시간상수 추출.

미실행: 모델/HMM 학습0, 전체 실험0, 성능 재평가0, 결과 기반 튜닝0, main 병합0. 이번 검사는 정적·데이터 전용이며 성능 향상을 주장하지 않는다.

## STEP2 / 2026-11-16

사용자 확정: 분석기간2010-01-01~2025-12-31,2026관측 모든 단계·타깃보완 제외. 원본 바이트 보존, 파생자료 cutoff 선적용. 이전의2026종가 보완 제안 폐기.

추가: cutoff/검증KRX달력 nullable target/PIT·US schedule/lineage/strict purge·5origin/Train-only scaler/10모델·6ablation 선언형사양/keyed ensemble/HMM forward·Train계획/date block bootstrap·Holm/LTC snapshot 인터페이스, config2개, manifest, 테스트23개, STEP2 보고3개.

통일: 원본 단일은 CUDA AMP자동·log offsets111/211/311/411/511·Hybrid=.7LNNensemble+.3RNNensemble. 원본 다중은 AMPoff·log offsets102/202/302/402/502·Hybrid=.7LNNensemble+.3RNNraw. 신규는 FP32/AMPoff·다중offset·다중Hybrid로 고정. RAW/LOG feature순서와동일seed 결합을검증. 원본 t-20..t-1와신규 t-19..t를config분리하며같은조건결과라고하지않음.

실행: 데이터·합성23PASS/0FAIL, 실자료7BLOCKED. KOSPI3935→3894,2026제외41,마지막unknown20,기준일후보2025-12-01. 공식KRX달력과공표시각미확정으로확정표본수null.

이전STEP1 전체기간재현 runner비활성화. STEP1 evidence·원본·기존결과·main·JOF V14/V15·lock·workflow미수정. 모델/HMM fit·GPU·실제model forward·checkpoint로드·실자료검정·결과기반튜닝0.

## STEP2.5 / 2026-11-16

- KRX 공식 연도별 휴장일16개 응답+평일규칙으로3939세션확정. B01 PASS. 원본3894날짜 중중복/비거래일0,45개부재모두개장일. 공식가격조회HTTP400 LOGOUT으로보완가격0행, B02 PARTIAL.
- 공식세션20 horizon에서 원본20행과 endpoint날짜664건차이. 중간가격NaN유지,확정표본수null. 실제2022시작01-03으로manifest경계수정.2025마지막20unknown·2026배제유지.
- 미국2021~2025공식calendar·조기폐장10일·특이휴장·2010~2025DST64probe 확인.1224개시장종료candidate에서same-date/shift1과날짜차이1184/52/42. provider available_at·생산PIT입력은미확정으로모두BLOCKED.
- 가공9열후보식3854행일치하나생성코드/출처확정아님. 외국인당일입력차단유지.
- 저장torch2.10.0+cpu확인,원본ncps/hmmlearn버전미상. ncps1.0.1공식배포와고정소스LTC파일동일검증. wrapper implicit=True/cell직접False차이때문에τ인터페이스의모드추정을금지하고explicit bool필수화.설치/모델forward없음.
- STEP2회귀23+STEP2.5검사11=34PASS/0FAIL.신경망/HMM fit/GPU/checkpoint로드/패키지설치0.새보고3개·manifest·provenance추가,현재gate갱신.원본·과거결과·V14/V15·lock·main불변.

## STEP2.6 / 2026-11-16

- 전체 KOSPI 200 종가.xlsx 부재를 확인했다. 공통3894일 신규 가격 대조0건, 충돌 건수UNKNOWN으로 남겼다. 전체 Excel이 존재한다고 가정하거나 보완 Excel의 출처 시트를 전체 데이터로 대체하지 않았다.
- 사용자 보완CSV/XLSX의45개 날짜·종가가 일치함을 확인하고 CSV를 한 번만 병합했다. 기존3894개 종가를 그대로 보존한3939행 로컬 파생물을 생성했다. 보완 상태는 USER_SUPPLIED_VERIFIED_MATCH, 공식가격인증은 아니다. OHLC/Volume은 생성하지 않았다.
- 실제 session_id+20으로3919known/20UNKNOWN. 끝20일은2025-12-02~12-30, 마지막 기준일12-01. 원본 관측행20 horizon과의 날짜차이664건을 새 타깃에서는0건으로 해소했다. 공통known3874개 중47개 Target이 달라졌다. 모델 성능/p값은 생성하지 않았다.
- 원래 local feature 식을 유지하여 warm-up40일 제외3899행, t포함20window·known label 적격3860개를 계산했다.5개 origin별 domestic supplied-value structural counts와 official/PIT 미확정을 별도로 기록했다.
- reports/STEP26_*.md4개, 요청 manifest·provenance·테스트·재현코드 추가. raw/derived 가격·전체 Target/피처는 로컬 보존하고 공개 GitHub에는 재배포하지 않는다. .gitignore로 보호한다. 원본8개와 보완2개 해시, 과거 보고/결과, Notebook·V14/V15·lock·main은 보존한다.

## STEP2.6 전체 Excel 추가 검증 — 2026-11-16

전체3939세션·보완45일 일치 확인. 공통3894일 exact144건, 소수2자리3892건 일치; 두 자리 불일치2건은 별도 기록하고 원본 가격 유지. 전체파일 부재 차단을 해제했으나 가격 원천·PIT·runtime·라이선스는 미확정이다. 원자료와 가격 상세표는 공개하지 않는다. 학습/HMM fit 비활성 유지.

## STEP2.7 / 2026-11-16

전체 Excel3939세션·공통3894일·누락45일을 다시 검증했다. exact 차이3750건, 소수2자리 차이2건은 미해결로 최종 데이터 확정 BLOCKED다. 기존 후보 가격·레이블·결과는 보존했다.5Origin 구조 진단과 F1 입력전용/변동성레짐 적격을 구분했다. 원본 수동레짐99행·HMM66행 저장출력을 별도 보존하고 다중시드 개별수동495행은 null/BLOCKED로 표시했다. Train-only 레짐/단일클래스 정책·비실행 Smoke config·사양해시를 추가했다. 사용자 요청으로 별도CPU venv에 torch2.10.0+cpu/ncps1.0.1/hmmlearn0.3.3 설치/import만 확인했다. 원본환경 동등성은 미인증.72 PASS/0 FAIL, 실행gate4 BLOCKED. 학습/HMM fit/모델생성·forward/GPU0, 원자료·가격상세 비공개, main/JOF V14/V15 불변. 최신 보고는 reports/STEP27_*.md5개, 검사는 tools/step27_tests.py다.

## STEP2.8 / 2026-11-16

A(원본+45일)·B(전체Excel)를로컬분리하고3919개known label·label_end 차이0을확인했다. 두실질적가격충돌은미해결이다. 나머지3892일은float32 roundtrip과일치하며3748일수치표현차이를구분했다. 피처·Train-only레짐임계값·5Origin·Scaler민감도를학습없이감사했다. 공식가격조회는두날짜모두403으로실패했고소스/PIT를인증하지않았다. 실제두날짜수치와전체후보시계열은공개하지않는다.

F1필수A와확장B gate를분리했다. 실제Smoke 실행코드를runtime/step28_smoke_runtime.py와tools/step28_smoke.py에작성했으나호출하지않았다. 원본정의/고정hyperparameter·CPU/시드·checkpoint·재현성·Test접근금지를포함하며현재flags=false와별도승인부재로차단된다. 순수감사src의기존비학습검사도그대로유지했다.90 PASS/0 FAIL, 필수A 2PASS·1PARTIAL·2BLOCKED,별도실행승인BLOCKED.외부B는F1 gate가아니지만F1자체가격/PIT/호환성은필수다. reports/STEP28_*.md5개와요청manifest/config를추가했고기존결과·main/JOF는보존했다.

## STEP2.9 / 2026-11-16

사용자의 독립 합성 CPU 승인 범위에서 5개 모델을 각각2회, 매번 합성 Train/Validation batch각1개·optimizer update1회로 검사했다. 실제 source/hash를 검증한 모델/FocalLoss를 재사용했고 전체Notebook·시장데이터모델·HMM·GPU는 실행하지 않았다. 생성/parameter count/forward/backward/finite gradients/clip/AdamW/OneCycle/checkpoint/정확재현성70판정 PASS, 총합성update10회다. 기존90개 회귀검사와 별도13개 제어검사도PASS다.

모든가격/PIT production gate와 training_enabled=false/hmm_fit_enabled=false는 유지했다. A/B는BOTH_UNVERIFIED, 자료선택미승인이다. RAW5피처는정적검사만이며2피처 합성실행을전체실험완료로표시하지않는다. 새 synthetic config·독립승인·runner·manifest와reports/STEP29_*.md4개를추가했다. 합성배열/checkpoint는새로컬ignored디렉터리에만보존한다. 기존158개 산출물·원본·JOF V14/V15·main은보존했다. 본실험준비체크리스트는manifests/step29_main_experiment_checklist.json이다.

## STEP3A / 2026-11-16

사용자가 별도로 승인한 회고적 CPU Pilot으로 O1/A-B/F1/Seed2의10 fit을 시작했고 10개 완료, 0개 실패했다. Train2387/Validation228, Train20purge·Validation20UNKNOWN 제외, Test/GPU/HMM/전체RO/Ablation0. 모든 설정과A/B source 미확정·production false gate를 유지했다. loss/Validation 진단·EarlyStopping·checkpoint/RNG 복원 기록을 새 로컬 경로에 보존했다. 원자료·일별Target·확률·모델 가중치는 공개하지 않는다. 집계CSV/곡선·STEP3A 보고서4개와 독립승인·코드/해시만 감사 브랜치에 게시한다.
