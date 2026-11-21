# STEP11 RQ별 주장과 증거 등급

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## RQ 식별 계약

RQ 번호는 기존 STEP10_RQ_CONCLUSION_MATRIX_KO.md를 그대로 따른다. 초기 Word의 절 번호와 혼동하지 않는다. 최종 원고의 RQ 문구는 지도교수 검토로 확정한다. 등급은 주장별로 적용하며 하나의 종합 PASS로 합치지 않는다.

| RQ/주장 | 등급 | 근거와 사용 가능한 서술 | 금지되는 확대 |
| --- | --- | --- | --- |
| RQ1: LTC를 포함한5NN의 평균 예측 성능·안정성 | DESCRIPTIVE_SUPPORTED | NN500/Test500 고정 집계에서 관측된 패턴을 보고 | 전체 미래시장·유의한 우월성으로 확대 불가; 추론은 INFERENCE_LIMITED |
| RQ2: LTC 단일클래스 예측/학습 안정성 | DESCRIPTIVE_SUPPORTED | LTC24/100의 전체 Test 단일클래스 예측이 동결 진단에 존재; NaN/발산과 구별 | 24개 독립 시장 사건·보편적 LTC 결함·인과적 학습실패율로 해석 불가 |
| RQ3: 수동/HMM 레짐별 성능 변화 | EXPLORATORY_SUPPORTED | Train q30/q70와 Train-only HMM/forward filtering로 같은 동결 예측을 층화 | 참 시장상태 발견·레짐별 확증 우월성·레짐 선택 전략 수익 주장 불가 |
| RQ4: τ와 퇴화의 관계 | EXPLORATORY_SUPPORTED | 원99+독립 복구1의 versioned100, 비교 가능한 Origin×가격8/8에서 저장된 방향을 탐색적으로 기술 | τ가 퇴화를 유발·매개했다거나 실제 경제적 기억시간이라는 인과 주장 불가 |
| RQ5: 단순 기준모형 대비 성능 | DESCRIPTIVE_SUPPORTED; 유의한 우월성 NOT_TESTED | Baseline40과 기존 저장 NN 비교의 기술적 차이만 보고 | STEP5C600을 baseline 유의성 검정으로 인용 금지; METHOD_NOT_VALIDATED 유지 |

## 교차 적용 등급

가격 공급처 인증과 historical18KST 사용 가능성 주장은 **BLOCKED_BY_EVIDENCE**다. 확증적 평균 성능 차이는 **INFERENCE_LIMITED**, 투자수익·τ 인과효과는 **NOT_TESTED**다. 이 등급은 RQ2/4의 관측 진단을 없애는 것이 아니라 연구 외삽 범위를 제한한다.

원본 초기 RAW5/LOG2 Ensemble은 최신 F1의 일부로 검증된 것이 아니다. 서로 다른 기간·입력·window·label·selection·통계 단위의 결과를 빼서 개선/악화나 재현 실패를 주장하지 않는다. STEP10C의 모델 정체성 충돌과 수정 통계 아카이브 공백도 남는다.

## τ 및 레짐 해석의 필수 한계

효과적 τ는 ncps LTC 구현의 입력·상태·conductance·solver 시간단위에 의존하는 내부 진단량이다. 같은 checkpoint의 날짜·window·hidden unit을 독립 표본으로 늘리지 않는다. Origin/가격/Seed 구성과 단일클래스 집단의 구성이 연관을 만들 수 있으며 개입·무작위화가 없다. 보완 복구1을 역산할 새100개 정량분할은 공개하지 않는다.

레짐별 클래스 support가 하나뿐이면 BA/MacroF1은 사전 null 정책을 적용한다. 수동 레짐과 HMM을 별도 표로 유지하고 Test 기반 경계 재선택을 하지 않는다. 저장된 탐색적 차이를 진짜 레짐의 인과효과로 표현하지 않는다.

기준모형과 NN은 같은 날짜·Target을 비교했더라도 NN20window, Logistic 현재F1, 규칙모형의 다른 가격 이력을 사용한다. 따라서 모형 복잡성만의 통제실험이 아니다. Seed 평균 손실과 확률 Ensemble도 구별한다. 이번에 새 성능·층화·연관 통계량을 만들지 않았다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
