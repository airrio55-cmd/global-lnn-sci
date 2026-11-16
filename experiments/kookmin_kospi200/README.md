# 국민대학교 박사학위논문 KOSPI 200 별도 프로젝트

상태: 정적 감사와 프로토콜 초안. **학습·HMM fit·결과 기반 튜닝 금지.**
기준: `airrio55-cmd/global-lnn-sci@3324ead54266b07df176d312b6604289b50523a8`.
작업 브랜치: `audit/kookmin-kospi200-20261116`. 기존 V14/V15, lock, workflow에는 변경하지 않는다.

- `reports/AUDIT_KO.md`: 18셀 비교, 심각도, 코드 위치, 실제 데이터 재현.
- `reports/PROTOCOL_KO.md`: 수정안·Rolling-Origin·피처 ablation·LTC 시간상수·규모.
- `reports/TEST_PLAN_KO.md`: 수정 전후 gate.
- `evidence/input_manifest.json`: 첨부8파일 SHA-256·크기.
- `evidence/data_inventory.json`: CSV별 범위·결측·중복·0값·출처 상태.
- `evidence/data_only_checks.json`, `static_tests.json`: 학습 없는 재현·7검사.
- `evidence/cell_comparison.csv`: 셀 소스 해시·동일 여부. 전체 셀 소스(`*_cells.txt`)와 전체 diff는 작업 환경 전용이며 공개 브랜치에서 제외한다.
- `configs/proposed.json`: 비실행 사양; 승인 또는 preregistration lock가 아님.
- `CHANGELOG.md`: 이번 준비 작업과 미구현 수정안.

첨부 원본8개는 작업 환경의 `originals/`에 바이트 그대로 보존했다. 새 공개 브랜치에는 원본 데이터를 재업로드하지 않고 manifest와 감사 문서·정적 도구만 저장한다. 재현 시 manifest에 맞는 원본8개를 `originals/`에 배치한다. 저장소 기존 KOSPI CSV는 첨부 KOSPI 파일과 해시가 일치하지만 원천 공급처 증거는 별도 필요하다.

원본·증거의 과거 상태는 보존한다. 현재 재현 명령은 아래 STEP2 절을 따른다. 학습 진입점과 자동 workflow는 제공하지 않는다.

저장된 과거 notebook 출력은 새 실행 결과가 아니다. 미확정 target 제거·PIT 결합·purging 등 모델 코드 수정은 **제안** 상태다. main 병합·학습은 승인되지 않았다.

## STEP2 현재 상태

`reports/STEP2_REPORT_KO.md`, `STEP2_PREFLIGHT_KO.md`, `STEP2_BLOCKERS_KO.md`가 최신 상태다. 기간은2010-01-01~2025-12-31로사용자확정했고2026타깃보완도금지한다. `configs/experiment_config.json`이현재설정이며`proposed.json`은대체됐다.

검사는 `python experiments/kookmin_kospi200/tools/step2_preflight.py` 후 `python experiments/kookmin_kospi200/tests/test_step2.py`로 실행한다. 이전 `tools/static_audit.py`는전체기간재현을막기위해비활성화했다. 기존STEP1 evidence·AUDIT_KO.md는당시원본문제의역사적증거로보존하며새분석입력으로사용하지않는다.

구현검사23PASS/0FAIL이나실자료7BLOCKED다. 공식KRX달력·누락가격·실제공표시각·runtime단위없이는STEP3학습을시작할수없다. `manifests/`의candidate수와observed경계를확정실험표본/실제KRX경계로오해하지않는다. 원본3노트북과CSV5파일은공개브랜치에업로드하지않는다.

## STEP2.5 최신 상태

`reports/STEP25_DATA_VERIFICATION_KO.md`, `STEP25_BLOCKERS_KO.md`, `STEP25_READINESS_KO.md`와 `manifests/step25_gate_results.json`이 최신 판정이다. B01은 공식 KRX3939세션으로PASS, 나머지는PARTIAL/BLOCKED이며 STEP3 smoke는 시작할 수 없다. 원본/과거 보고는 역사적 기록으로 보존한다.

`tests/test_step25.py`는 확보한 evidence와 날짜·시각 규칙만 검사한다. `tools/step25_verify.py <local_source_directory>`는 로컬에 보존한 공식 조회 응답·공식 PDF의 검증 추출 metadata와 사용자원본으로 진단물을 재생성한다. raw자료/PDF/원본CSV/wheel은 공개 브랜치에 게시하지 않았다. source catalog의 URL·파라미터·해시로 출처를 추적한다. STEP2 preflight runner는 최신 manifest를 과거진단으로 덮어쓰지 않도록 차단한다.

## STEP2.6 최신 상태

전체 `KOSPI 200 종가.xlsx`를 수령하여3939세션과 공통3894일 가격 대조를 완료했다. 가격 차이의 원천 판정은 BLOCKED다. 보완 CSV/XLSX의45개 값은 서로 일치하므로 중복 합산 없이 기존 종가에 추가했다. 국내 파생물3939행은 USER_SUPPLIED 수준이며 공식 원천·PIT 인증은 아니다.

최신 문서: reports/STEP26_PRICE_RECONCILIATION_KO.md, STEP26_LABEL_AUDIT_KO.md, STEP26_ROLLING_ORIGIN_KO.md, STEP26_BLOCKERS_KO.md. 국내 수치·날짜·label 구조적격과 외부5피처 PIT 적격을 구분한다. 학습은 차단 상태다.

로컬 데이터 생성: `python experiments/kookmin_kospi200/tools/step26_reconcile.py --full-sheet Sheet1 --full-skiprows 16 --full-date-column Date --full-close-column Close`. 기존23+11검사를 보존하며 신규19검사를 함께 실행: `python experiments/kookmin_kospi200/tools/step26_tests.py`. 현재 공급처/라이선스 미확정이므로 data/user_supplied·data/derived의 가격·전체 일별 Target/피처는 공개 GitHub에 올리지 않는다. 공개 원천의 세션 달력, 날짜/상태 감사, 집계와 해시만 포함한다.

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
