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
