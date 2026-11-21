# STEP11 누출 위험과 증거 범위

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 코드 계약과 실행 아카이브에 대한 판정

VERIFIED는 해당 내부 계약·기존 저장 검사에 대한 확인이다. 실제 모든 historical 가격이 당시에 도착했다는 뜻이 아니다. 새로운 학습·입력 재구성·Test 평가로 검증 범위를 확장하지 않았다.

| 항목 | 판정 | 기존 근거·위치 | 잔여 위험/해결조건 |
| --- | --- | --- | --- |
| Train-only scaling | VERIFIED | STEP3C master, STEP3A~4D 입력/실행 감사; 유지된 Train window의 허용 입력 시점 합집합으로 fit | 보존 아카이브 계약 범위. 수정 vintage의 유입까지 인증하지 않음 |
| label endpoint purging | VERIFIED | STEP3C/STEP5A label 계약; Train label_end < Validation 시작, 선택용 Validation label_end < Test 시작 | 20세션 purge·마지막 UNKNOWN 규칙은 같은 구간 내 label 직렬의존을 제거하지 않음 |
| t 포함 window와 forward label | VERIFIED | local_features 및 master t-19~t, 공식20session | 원본 t 제외 window와 다른 설계. t 종가 historical availability는 BLOCKED |
| Validation checkpoint 선택 | VERIFIED | strict Validation BA 개선, 동률 최초 최고 epoch | Validation은 선택에 사용됐으므로 독립 일반화 평가가 아님 |
| Rolling-Origin 중복·노출 | PARTIALLY_VERIFIED | STEP10/STEP10B와 O1~O5 고정 경계 | Train 중첩, 이전 Test가 후속 Train/Validation 역사에 들어감. 사후 결과 노출을 소급 제거할 수 없음 |
| horizon20 label 중첩 | PARTIALLY_VERIFIED | 공식 session endpoint 계약, STEP5C 의존성 논의 | 날짜는 독립 표본이 아님. 연도별 Test label endpoint가 다음 연도로 이어질 수 있음 |
| HMM Train-only fit | VERIFIED | STEP6B 실행·선택 아카이브 및 runtime 정적 코드 | Train 내 동일 후보 집합/선택/상태 명명 계약. 시장의 참 레짐 인증은 아님 |
| Test regime filtering | VERIFIED | STEP6B forward filtering, 경계 posterior 전달 | Test 전체 Viterbi·Test median fallback과 구분. 선택된 모형 불확실성은 별도 |
| 수동 레짐/예측 threshold | VERIFIED | Train Vol q30/q70, p>0.5 고정 | Test 분위수 재추정 금지. 실제 Train 임계값은 공개하지 않음 |
| 가격 후보 선택 | VERIFIED (병렬 유지) | STEP10A BOTH_UNVERIFIED/primary PENDING | 출처 UNKNOWN; Test 성능으로 하나를 고르면 사후 선택 문제가 추가됨 |
| 국내 입력 historical PIT | BLOCKED | STEP10A/STEP11_HISTORICAL_PIT_STATUS | 실제 수신/vintage UNKNOWN. 코드상 causal join과 동일하지 않음 |
| 초기 RAW5 외부 변수 | BLOCKED | STEP10B/10C, STEP25~29 | 초기 결합/시점/공표 문제; 최신 F1과 혼합하지 않음 |
| 2026 관측 제외 | VERIFIED (최신 고정 계약) | 연구 cutoff 및 STEP10 보존 감사 | 초기 Notebook 제공 데이터의 기간 문제는 따로 남겨둠. 새 관측 사용0 |

HMM100 후보에서 최종10을 선택한 것이므로 추가10fit로 합산하지 않는다. STEP3D O3 재사용은 중복 fit가 아니다. 완료 모델 수와 독립 시장 표본 수를 구분한다.

## 초기 논문과 현재 계약의 차이

STEP10C는 Word가 pooling을 인정하고 대표Seed/비중첩 검정으로 수정했다고 기술한 사실을 확인했다. 현재 제공 Notebook cell18에는 이전 pooling 코드가 남아 있어 수정 실행 아카이브가 필요하다. 초기 Word CfC 서술과 최종 활성 LTC, Validation loss 서술과 실제 BA 선택, HMM 전체기간 서술과 코드 Train fit/Test Viterbi도 정합이 필요하다. 이 문서상 불일치를 최신 코드가 곧 누출됐다는 증거로 확대하지 않는다.

공식 session label/Train scaler/forward filtering 등 개선은 구현 위험을 줄이지만, Test를 이미 여러 단계에서 읽고 해석한 사후 연구가 최초 독립 확증 연구로 바뀌지는 않는다. 내부 일관성·PIT·확증적 통계 판단을 각각 보고한다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
