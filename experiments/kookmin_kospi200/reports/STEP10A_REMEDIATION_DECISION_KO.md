# STEP10A 기존 결과 사용·한계·추가검증·재실험 판단

감사일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci`, `audit/kookmin-kospi200-20261116`, `experiments/kookmin_kospi200/`.

STEP10A는 기존 가격 provenance와 historical PIT 증빙의 읽기 전용 감사다. 신규 금융 학습·checkpoint load/forward·Test 예측/성능 재평가·HMM fit/refilter·τ 계측·bootstrap/draw·p값/CI는0이며 원본·기존 결과·설정을 변경하지 않는다. master training_enabled=false / hmm_fit_enabled=false / new_fit_execution_enabled=false를 유지한다. 2026년 날짜가 있는 파일 속성은 입수·편집 메타데이터로만 읽으며 2026 시장 관측은 사용하지 않는다.

가격 상태는 **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**다. SHA 일치는 무결성 증거이지 외부 공급처·공표시각·과거 vintage 인증이 아니다. Test 성능으로 A/B를 고르지 않는다.

## A. 기존 결과를 그대로 논문에 사용할 수 있는 범위

현재 자료는 **사용자 제공 최종 시계열에 대한 회고적·탐색적 F1 연구**로 제한하여 기술할 수 있다. 기존 NN500 학습/Test500, Baseline40, HMM100후보/선택10, 보완 τ100, STEP5C600행의 동결 결과를 출처 한계와 함께 인용한다. 이는 무조건적인 데이터 적법성·가격 공식인증·논문심사 통과를 보증하는 말이 아니다. 원자료·상세수치의 제출/공개권한은 별도 확인한다.

A/B를 사전 지정된 병렬 후보로 함께 유지하고 유리한 Test 성능을 보인 후보를 주 분석으로 사후 지정하지 않는다. 기존 가격·checkpoint·성능표를 수정하지 않는다. 과거 원 Notebook Historical Baseline, 이후 F1 연구, 원형 RAW5/LOG2 Ensemble을 서로 같은 실험이라고 쓰지 않는다.

SHA 및 공식 세션 정렬, trailing 수식·purging·Train-only scaler는 내부 무결성/계약의 근거로 사용할 수 있다. 이들 근거만으로 공급처의 과거 공표·수신·개정 적격성까지 확인했다고 주장할 수 없다. 기존 STEP5C는 동결된 근사추론으로 보존하며 STEP9B1R의 METHOD_NOT_VALIDATED를 출처 감사로 해소했다고 하지 않는다. NN–baseline 통계적 우월성은 NOT_TESTED다.

## B. 사용 시 필요한 한계 표현 — 논문 삽입 초안

“본 연구는 사용자 제공 KOSPI200 가격후보 A/B의 동결된 최종 시계열에 근거한 회고적·탐색적 분석이다. 제공 파일의 무결성과 공식 세션 정렬은 확인했으나, 원 공급처·추출 이력·가격 수정/조정 정책 및 각 과거 기준일18:00 KST의 실제 배포·수신 버전은 충분히 입증되지 않았다. 두 후보의 가격 충돌과 수치 정밀도 차이는 기록으로 보존하였으며 Test 성능으로 주 가격후보를 선택하지 않았다. 따라서 본 결과를 실시간 이용 가능성, 미래정보 누출의 완전 배제, 전향적 일반화 또는 투자수익성의 검증으로 해석하지 않는다.”

추가 문장: “파일 생성·Refresh 및 패키지 수정시각은 행별 가격 공표시각이나 수신시각이 아니다. Hindsight revision 가능성과 역사적 Test 노출, 중첩label/반복Seed 의존성, 모형별 정보이력 차이가 남는다. F1 [Log_Ret, Disparity]의 결과는 외부5피처·RAW5/LOG2 Ensemble의 검증을 대체하지 않는다.”

τ100 보완 통합과 가격/PIT 증빙은 독립 gate다. 낮은 effective τ와 퇴화의 탐색적 연관을 경제적 기억길이나 인과효과로 바꾸지 않는다. 원τ99/1 실패와 보완1의 lineage, 원baseline BLOCKED40 및 복구40 기록도 그대로 남긴다.

## C. 원본 증빙 확보 후 추가 검증할 항목

STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md의 R01~R10을 순서대로 확보해야 한다. 같은 공급처라 해도 시리즈/필드/버전/정밀도/개정정책이 동일한지 확인하고, 공식 최신가격 일치와 historical18시 적격성을 각각 판정한다. 보완45일과 전체Excel이 같은 계열이면 독립 교차검증으로 세지 않는다. 두 충돌 날짜의 권위 있는 원 응답과 개정 공지가 없는 현재 원인 판정은 UNKNOWN이다.

새 증빙은 새 감사 version으로 추가한다. 확인된 사실의 날짜·범위를 기록하고 미확인 구간을 소급 VERIFIED로 채우지 않는다. 주 자료는 공급처 신뢰성·정의·시점·일관성에 따라 결정하고 실제 값/계약이 그대로인지 data-only 영향감사를 먼저 수행한다. 이 문서는 그 금융 계산이나 재실험을 실행하지 않는다.

## D. 실제 데이터가 달라 재실험이 필요한 조건

| 조건 | 발견된 변경 | 조치 원칙 | 반드시 구분할 점 |
| --- | --- | --- | --- |
| D1 | 증빙만 보완되고 동일한 시계열·시점·정의·입력·label·표본 계약이 유지 | 기존 결과의 출처 설명을 새version 주석으로 보완 가능; 재학습을 자동 요구하지 않음 | 동일성은 증빙 기반 data-only 감사로 확인; original과 과거한계 기록 유지 |
| D2 | 공식 가격·누락세션·지수필드·수정버전이 동결 A/B와 실제로 다름 | 기존 결과는 old-data version으로 보존. 바뀐 입력/label/표본을 쓰는 실험은 새 처리·동결·승인 후 재실행 필요 | 영향받는 Origin·Train/Valid/Test·피처/scaler·레짐 의존성을 추적; 모든500을 무조건 반복하거나 일부를 조용히 대체하지 않음 |
| D3 | 18시에는 t종가 또는 필요한 과거개정 버전이 미가용해 window/의사결정 계약 변경 | 기존F1을 production-PIT로 재명명 불가. 새 계약 실험에는 적절한 재학습/평가의 별도 승인 필요 | t제외/다음세션 대안의 target기준일·horizon·cutoff를 사전 고정; Test 성능으로 대안선택 금지 |
| D4 | 사후수정 종가를 당시값으로 쓴 것이 확인되어 as-of vintage로 교체 | 피처·Train-only scaler·checkpoint 선택·수동/HMM 레짐까지 영향 감사; 필요한 금융 재실험은 새version/예산/승인 후 | label이 같아도 학습입력과 선택경로가 달라질 수 있음; label일치로 재학습면제 단정 금지 |
| D5 | 단순 표시정밀도/단위 차이라고 주장되나 실제 계산입력 동일성이 미확인 | 재실험 불필요/동등이라고 먼저 선언하지 않음. 정의·수치처리·저장입력의 동일성 감사부터 | 소수2자리일치 또는 수식의 이론적 scale불변만으로 실제 scaler/float32 tensor일치를 인증하지 않음 |
| D6 | 입력·label은 같지만 표본 마스크/기간/레짐 기준이 변경 | 새 표본·레짐 계약에 따른 새version 분석 필요; 기존 결과에 혼합 불가 | 공통 Vol_Regime 적격 마스크 변경은 두피처 입력이라는 이유로 무시할 수 없음 |
| D7 | 값은 유지되지만 라이선스/재배포조건 미충족 | 공개·제출범위 재검토가 우선이며 그 자체가 수학적 재학습 사유는 아님 | 원자료/확률/weights/개별τ는 공개하지 않음; 증빙 없는 공개권한을 만들지 않음 |

변경된 한 종가는 해당 기준일과20세션 전 기준일의 Target, 다음 시점 수익률, trailing Disparity/Vol_Regime, 겹치는 입력 window, Train-only scaler·분위수·HMM 선정 및 checkpoint 선택으로 영향이 퍼질 수 있다. 이 영향은 단순히 두 날짜의 Test 결과만 바꾸어 고칠 수 없다. 반대로 원천증빙만 보완되고 실제 입력·label·사양이 같으면 새로운 학습을 자동 요구할 이유도 없다. 두 경우를 증빙·의존성 감사로 구분해야 한다.

정밀도/출처/시각 문제를 수정하려고 기존 Test를 반복 열람하여 모델·Seed·가격·cutoff를 최적화하지 않는다. 기존 결과는 historical version으로 보존하고 신규 결과에는 새로운 데이터/코드/설정 hash·승인·예산을 요구한다. **이번 단계의 후속 금융 실행 예산은0**이며 어떤 D조건도 자동 학습·HMM fit·추론·bootstrap 실행 승인이 아니다.

## 최종 의사결정

파일 입수·보존 및 내부수식 계약은 VERIFIED, Excel/보완 연결·코드/단위·표현정밀도의 제한된 증거는 PARTIALLY_VERIFIED, upstream 공급처·추출·수정·공표/수신 사실은 UNKNOWN, 최종 가격 인증과 historical18KST/production-PIT는 BLOCKED다. 따라서 현재는 한계를 명시한 회고적 집필을 지속할 수 있지만, source/PIT 인증 완료나 새 금융 검정 승인으로 승격할 근거는 없다.
