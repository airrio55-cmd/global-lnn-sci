# STEP11 통계방법 개선 후보: 실행 전 검토

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 검토의 범위와 공통 추정대상

이 문서는 후보를 제안할 뿐 채택·타당성 통과·새 금융 통계량을 산출하지 않는다. 이미 Test를 반복 조회한 사후 방법론 검토라는 한계는 어떤 후보에서도 사라지지 않는다. 데이터 출처/PIT 문제를 표준오차로 해결할 수 없다.

먼저 동결된 모델·Seed 집합에 조건부인 비교와 미래 재학습 알고리즘의 성능을 구분해야 한다. 관측 패널의 유한평균 차이 자체는 기술량이다. CI/검정을 붙이려면 어떤 확률과정·시기·훈련 무작위성에 대해 일반화하는지 따로 선언해야 한다. A/B, baseline, metric, Origin 가중치, 방향·가족·α·실패 처리·방법 선택을 결과 재확인 전에 고정해야 한다.

## A. 날짜별 Brier 손실 차이

**Estimand:** Origin o, 날짜 t에서 `d[o,t] = mean_seed((p_NN[o,s,t]-y[o,t])²) - (p_baseline[o,t]-y[o,t])²`. 양수는 NN 손실이 더 큼을 뜻한다. Origin별 날짜평균을 동일 Origin 가중치로 합친 기대 차이를 후보 대상으로 한다. 이것은 Seed 확률을 먼저 평균한 Ensemble Brier와 다르며 새로운 Ensemble을 만들지 않는다. 전체 날짜 풀링 가중치와도 다르다. 이 식을 이번에 계산하지 않는다.

**H0:** 사전 선언한 조건부 모집단에서 가중 기대 손실차=0, 기본 양측. NN–baseline은 기존 STEP5C 신경망 간 가족과 별도다.

**필요 자료:** 기존 동결 예측·정답·날짜·Origin·모델/가격 identity 및 결측 사유의 비공개 연결. 새 추론 없이 검토만 한다.

**가정·제약:** 유계 손실의 평균은 BA/F1의 클래스 비율 분모 문제를 줄일 수 있지만 직렬의존·비정상성·Origin 이질성은 그대로다. 대략 연도별 수백 날짜와5Origin이며 Seed 수로 시장 n을 늘릴 수 없다. 규칙모형의0/1 확률과 확률모형의 Brier 비교 의미도 명시해야 한다.

**검증 계획·실패:** 독립 개발/holdout 합성 DGP에서 장기의존·break·희소 클래스·Origin 전환·동결 선택과 가족별 크기/coverage/유효성·꼬리 정밀도를 검사하도록 사전 계획한다. 기준 미달·퇴화 분산·모집단 정의 부재면 BLOCKED. 지금은 합성 생성/CI 계산도0이다.

**9B1R과 차이:** 주 추정량을 Brier 손실의 날짜평균으로 명시한다. 그러나 기존 family 검토에도 Brier가 포함돼 있었으므로 완전히 미검토된 해결책이 아니다. BA보다 단순한 평균이라는 이유로 PASS를 가정하지 않는다.

## B. 의존성 강건 표준오차·장기분산

**Estimand/H0:** A와 같은 고정 가중 손실차 기대값 또는 사전 정한 다른 additive contrast, H0=0. 어떤 metric을 사용했는지 바꾸어 해석하지 않는다.

**필요 자료:** 동기화된 날짜별 차이와 Origin 경계, 학습/선택 시점. HAC bandwidth/kernel, 경계 처리, 학생화 및 작은 표본 정책을 사전 지정해야 한다.

**가정·제약:** 약한 의존성·충분한 moment/장기분산·필요한 국소/구간 정상성 및 CLT가 필요하다. horizon20이라고 lag19 이후 공분산을0으로 놓을 근거는 없다. Origin5개만으로 일반 cluster-robust SE의 큰 cluster 수 근사를 신뢰하기 어렵다. 긴 bandwidth는 연도별 짧은 n에서 불안정할 수 있다. 모델 전환 경계·장기 기억·분산0이 핵심 위험이다.

**검증 계획·실패:** bandwidth를 유리한 금융 p값으로 고르지 않고 별도 합성 개발/holdout에서 크기·coverage·유효 분산 비율과 family FWER를 검사하도록 설계한다. 장기의존/break/variance 실패면 사용 중단한다. DM류 검정도 유한표본·추정모델 조건 확인 없이 자동 대체재가 아니다.

**9B1R과 차이:** 기존 BA 영향함수 HAC40/120의 실패를 인정하고 additive Brier·Origin 가중/전환을 명시한 별도 calibration 문제로 한정한다. ‘HAC면 강건’이라는 이름만으로 기존 실패를 해소하지 않는다.

## C. Block resampling

**Estimand/H0:** 고정된 Seed 집합의 모델/후보 간 사전 지정 집계 효과, H0 효과=0. 날짜 블록 안에서 모든 모델·Seed·가격을 동기화한 paired 구조가 필요하다.

**필요 자료:** 기존 예측 panel, session 순서, Origin 경계와 유효 클래스·결측 마스크, 비교 가족. resample 단위·블록·중심화·studentization·invalid draw 정책을 먼저 고정한다.

**가정·제약:** 선택한 bootstrap이 근사할 의존성/국소 정상성과 충분한 유효 블록 수가 필요하다. Origin 내부 block은 경계 간 의존을 생략할 수 있고, 전체 연속 block은 서로 다른 모델/구간을 섞을 수 있다. 희소 클래스의 BA/F1은 정의 불가 draw가 생긴다. 긴 block은 유효 반복정보를 줄인다.

**검증 계획·실패:** 9B1R 반례를 포함한 새로운 독립 holdout DGP와 실제 설계 경계에 맞춘 size/coverage·유효 draw 비율·family FWER/Monte Carlo tail 검사를 제안한다. 실패 draw를0으로 채우거나 성공할 때까지 보충하지 않는다. 모든 핵심 시나리오가 미달하면 금융 적용 BLOCKED.

**9B1R과 차이:** 새 block 이름이나 Origin 정렬은 자동 개선이 아니다. 기존 MBB/stationary/local/multiplier 실패를 재사용 가능한 반례로 삼고 변경 이유와 새 calibration 근거가 있어야 한다. 기존 frozen blocks20/40/60·10000rep·seed20261116 결과는 그대로 보존하며 이번 draw0이다.

## D. Origin별 효과크기와 기술적 불확실성

**Estimand:** 각 동결 Origin/가격에서 관측된 모델 차이와 Seed 변동. **H0:** 기술적 보고에는 검정 가설이 필요 없다. 모집단 효과·CI를 주장하려면 별도의 H0/표본추출 모형이 필요하다.

**필요 자료:** 기존 저장 집계·Seed별 진단, 결측/실패 기록. 공개는 허용된 다중 fit 집계에 한정한다. 이번에는 새 효과크기·SD·CI를 계산하지 않는다.

**가정·제약:** 관측된5개 연도의 차이와10개 Seed 변동을 보이는 데 그친다. Seed SD나5Origin 범위를 모집단 CI로 부르지 않는다. 중첩 학습/시장 경로 때문에 Origin을 iid5표본으로 보는 계층/메타분석은 검증이 필요하다.

**검증 계획·실패:** 기술적 표는 저장값·집계 가중치·실패 누락 여부를 확인한다. CI로 확장한다면 별도 size/coverage 검증 대상이 된다. 독립성을 전제한 유의성 표현으로 넘어가면 이 후보의 범위를 벗어난다.

**9B1R과 차이:** 실패한 추론을 새 방법으로 통과시키는 것이 아니라 추론 주장을 낮춰 동결 관측의 기술·탐색적 근거를 사용한다. 현재 논문 보완의 우선 후보지만 확증적 대안은 아니다.

## E. 독립 미래 평가 설계

**Estimand/H0:** 등록 이후 실제 운용 조건과 고정 정보집합에서의 기대 손실차. H0=0 및 실제 전략을 다룬다면 별도의 경제적 목표·비용 정의가 필요하다. 현재 결과가 이를 검정했다고 말하지 않는다.

**필요 자료:** 고정 코드/가격 제품·모델·수신/vintage 로그, 사전 등록된 미래 관측·평가기간과 endpoint 완료 기록, 검정 가족·실패 처리·표본 크기 계획.

**가정·제약:** 시간 분리만으로 날짜 독립성이 생기지는 않는다. 구조 변화·수신 실패·label 중첩을 고려하고 충분한 평가 길이를 확보해야 한다. 이전에 읽은 Test를 다시 ‘미래 holdout’이라 부를 수 없다.

**검증 계획·실패:** 실행 전 독립 합성 calibration과 prospective logging dry-run을 별도 승인 아래 계획하고, 실제 기간에는 중간 결과로 사양을 바꾸지 않는다. 사전 노출·임의 중단·endpoint 부족이면 목적한 확증 해석을 포기한다.

**9B1R과 차이:** 추론 도구만 바꾸는 것이 아니라 평가의 정보 노출·등록 시점을 새로 설계한다. 그러나 자동으로 방법론 PASS가 되는 것은 아니다. **현 연구 종료일2025-12-31/2026 관측 금지는 유지**한다. 새 미래기간 수집은 별도 연구·별도 승인 없이는 실행할 수 없다.

## 공통 채택 조건

어느 방법도 미리 통과한다고 가정하지 않는다. 사전 기준은 유효성 비율, 명목 크기·coverage 허용범위, family별 오류율, Monte Carlo 오차와 독립 holdout을 포함해야 한다. 개발 시나리오 반복 튜닝과 holdout 재사용도 기록한다. 작은 꼬리를 판정할 resample 수의 해상도까지 검토한다. Seed·Origin·가격·지표·방법 다중 선택을 통제하고 기존 Test 반복 탐색을 그대로 고지한다. 이 검토는 신규 실험 승인이나 새 방법의 선택이 아니다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
