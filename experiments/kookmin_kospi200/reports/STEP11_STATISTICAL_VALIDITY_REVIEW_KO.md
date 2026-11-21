# STEP11 기존 통계적 타당성 검토

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 기존 STEP5C가 검정한 대상

기존600행은 블록20·40·60 각각 Primary BA20, Secondary80, Origin BA100이다. Primary는 두 가격 후보에서 신경망5모델의10개 쌍 비교다. Secondary는 Macro F1/Brier/Recall0/Recall1이며, Origin100은 Origin별 BA 진단이다. **NN–baseline 비교가 아니다.** 기존 STEP9B1의 20/80 가족 초안과 수가 같아도 가설은 다르다.

기존 절차는 날짜를 모델·Seed 간 paired하게 재표집하고 각 Seed metric, Seed 평균, Origin 평균으로 집계한다. 10개 Seed는 서로 다른 학습 난수의 반복이며 같은 시장 날짜의 독립 관측10개가 아니다. Origin별 기간 내 블록을 만들었다는 구현 사실이 Origin 간 모든 종속성까지 보장하지 않는다. Train 중첩·공통 가격 경로·전방 label·후속 Origin 노출이 남는다. 실제 가설은 동결 예측의 특정 집계차에 관한 것이며 학습 알고리즘의 모든 미래 재학습 성능과 동일하지 않다.

| 기존 저장 결과 | 블록20 | 블록40 | 블록60 | 가능한 해석 |
| --- | --- | --- | --- | --- |
| Primary BA20 기각 수 | 0 | 0 | 0 | 기존 근사절차에서 차이 입증 못함; 동등성/효과0 입증 아님 |
| Origin BA100 기각 수 | 0 | 0 | 0 | Origin별 차이 미확립; 모든 환경에서 동일하다는 뜻 아님 |
| Secondary80 기각 수 | 3 | 2 | 3 | 특정 지표·방향의 기존 탐색적 신호; 합계8 독립 발견 아님 |

값은 `manifests/step5c_execution_summary.json#/families`의 저장 결과를 인용했다. 새 검정·Holm·CI를 계산하지 않았다. Secondary의 반대 방향 증거도 보존하고 LTC 전반 우월성으로 선별 해석하지 않는다.

## 보정과 표본 의존성

Holm은 **각 family × 각 block 설정**에서 적용됐다. 유효한 주변 p값이 있으면 가설 간 독립성 없이 그 가족 FWER를 통제할 수 있지만, 유효하지 않은 p값을 고치지는 못한다. 가족·블록·새 사후가설 전체를 통합한 단일5% 보장을 주장하지 않는다. 기존 percentile CI는 주변 구간이지 동시 구간이 아니다.

20세션 겹친 label, 확률·손실의 지속성, 클래스 희소성, 구조변화, Origin별 다른 학습모델, 공유 Seed/가격 경로는 유효 표본 수와 불확실성에 영향을 준다. 블록20이라는 길이 자체가 모든 의존성을 포착했다는 증명이 아니다. 비중첩38개 점검 역시 그 날짜들이 독립임을 보장하지 않는다.

## STEP9B1R의 반례와 해석 한계

`manifests/step9b1r_method_review.json`은 **BLOCKED_METHOD_NOT_VALIDATED**, 추천 금융 방법 없음, 9설정 모두 핵심 holdout 기준 미충족이다. 저장 검토는 pair 합성 데이터4680개와 family1200개를 포함한다. MBB20/40/60, stationary40/120, local block, BA 영향함수 HAC40/120, dependent multiplier120 등을 검토했다. 강한 의존성·희소 클래스·공통 구조변화 및 Gaussian latent AR와 binary Markov 오류를 구분해야 한다.

초기199draw family 검사에서 최소 p=.005는 Holm20/80 첫 임계값에 도달할 수 없어 FWER0이 기계적으로 나타날 수 있었다. 이를 PASS로 보지 않는다. 보완1999draw도 작은 꼬리의 Monte Carlo 정밀도에 제약이 있다. 유효 데이터셋/유효 draw 비율과 조건부 오류율을 함께 보고해야 하며, 실패를0으로 채우거나 통과 draw만 재충전해서는 안 된다.

이는 실제 STEP5C 개별 p값이 틀렸다는 직접 증명도, 모든 통계방법이 불가능하다는 판정도 아니다. 그러나 명목 크기·coverage가 검증됐다고 말할 근거도 아니다. 기존600행은 **EXISTING_APPROX_INFERENCE / INFERENCE_LIMITED**로 보존한다. STEP9B2 금융 검정은 NOT_EXECUTED다.

## 초기 McNemar와 구분

STEP10C가 읽은 Word 수정본은 n759의 대표Seed 단일 날짜검정과 n38 비중첩 점검을 주장한다. 제공 다중Seed Notebook의 pooling 코드와 다르며 수정 script/원예측 연결은 부족하다. 대표Seed의 Test F1 중앙값 선정도 Test 의존 선택이다. McNemar의 paired hard classification 가설과 최신 집계 BA/Brier 차이 가설은 달라 p값 크기를 직접 비교하지 않는다. 이 공백을 새 검정으로 임의 메우지 않는다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
