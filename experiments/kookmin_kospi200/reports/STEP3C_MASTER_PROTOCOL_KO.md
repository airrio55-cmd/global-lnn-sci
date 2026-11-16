# STEP3C 본실험 마스터 프로토콜

동결 확인시각(KST): 2026-11-16T18:59:56.065162+09:00. 설정 SHA-256: `f4ea7a18d7812b00b8c581191a110f63a6799a22e066484ec251ee32f7912c5c`.

이번 단계는 사양·데이터 준비와 소스 정적 검사만 수행했다. 신규 모델 fit·모델 생성/forward·checkpoint load·HMM fit·독립 Test 예측/성능 평가·GPU 실행은 모두0건이다. production training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지한다. 기존40개와 원본·논문 결과·JOF V14/V15·main을 보존한다.

## 동결의 범위

설정·Origin·Seed·모델·피처 순서·학습/조기종료·평가·통계 가족·실행 예산을 동결한다. 주 가격과 연구설계 선택은 PENDING이라는 상태까지 명시적으로 동결하며 빈칸을 임의로 채우지 않는다. 사용자 결정은 외부 출처·연구 목적·범위에 근거하고 Validation/Test 우열로 선택하지 않는다. 사양 변경 시 이전 사양·해시·결과를 보존하고 새 버전/승인을 만든다.

연구기간2010-01-01~2025-12-31. KRX 공식3939세션에 정렬하고 Target=I(Close[t+20]>Close[t]), 동률0, 미래 종가 부재는 UNKNOWN이다. 2026년은 입력과 타깃 확인용으로도 금지다. 예측은 한국 거래일t 18:00 KST, window t-19~t의20세션을 유지한다. 국내 종가의 historical available_at은 UNKNOWN이므로 회고적 실험이며 production-PIT 인증은 BLOCKED다. 원본 t-20~t-1 사양과 동일 실험으로 주장하지 않는다.

F1=[Log_Ret,Disparity] 순서. Log_Ret=log(Close/Close.shift(1)), Disparity=Close/rolling20mean−1. Vol_Regime=Log_Ret.rolling(40).std(ddof=1)는 공통 window 적격 마스크와 레짐 보조 변수로만 사용한다. 원본 CSV를 바꾸거나 bfill/미래 보간/NaN 자동0 치환하지 않는다. 각 window의 모든20행에 세 국내 계산변수가 유한해야 한다. scaler는 purging 후 유지된 Train window 날짜의 합집합에만 fit하고 Validation/Test는 transform만 한다.

## Origin·Seed·학습

O1 Train2010~2019/Val2020/Test2021; O2 Train2010~2020/Val2021/Test2022; O3 Train2010~2021/Val2022/Test2023; O4 Train2010~2022/Val2023/Test2024; O5 Train2010~2023/Val2024/Test2025. Train label_end<Validation 시작, Validation label_end<Test 시작. 각각 말단20세션을 제외한다. Test의 label_end는 연구종료일 이내여야 하며 Test2021~2024 말단의 다음해 endpoint는 연구기간 안에서 허용한다. Test2025의 마지막20개는 UNKNOWN/평가 제외다. 경계/Origin/Seed는 결과나 클래스 비율에 따라 바꾸지 않는다.

Seeds=[2,12,22,32,42,52,62,72,82,92]. F1 유효 seed=base seed+RNN101/LSTM201/GRU301/LTC401/CfC501. DataLoader generator도 같은 유효 seed를 사용한다. 특정 Seed 실패·단일 클래스 예측을 제거하거나 다른 Seed로 교체하지 않는다.

RNN/LSTM/GRU/LTC/CfC, Hidden128/Layer1/Dropout0.2/Window20/Horizon20/Batch64/MaxEpoch100/Patience10, AdamW lr0.005 wd1e-4, OneCycleLR(max_lr0.005,계획100epoch,실제 Train batch 수), Focal gamma2 alpha0.25, clip1, FP32 AMP OFF, probability>0.5. 원본 Focal alpha는 전역 손실 배율이며 클래스별 가중치가 아니다. Validation BA의 strict 개선만 checkpoint 선택에 사용하고 동률은 patience 증가, 최초 최고 epoch를 유지한다. train+validation 재학습은 계획하지 않는다. NaN/비유한 gradient는 실패로 기록하고 설정 변경으로 구제하지 않는다.

## 기존40개 재사용과 예산

O1/O2×Seed2/12×A/B×5모델의40개가 COMPLETED이며 최적/최종 checkpoint·history·Validation probability의 SHA-256을 확인했다. O1/O2의 재계산 arrays/date/scaler는 기존과 정확히 같고 NPZ 원래 바이트를 유지했다. 원본 모델 정의/설정/환경 및 소스 파일 해시도 보존됐다. 따라서 현재 F1 계약에서40개를 재학습 없이 재사용한다. 전체 runner 파일 SHA는 STEP3A/3B/3C가 서로 다르다는 사실을 숨기지 않는다. STEP3C는 승인·Origin 범위·메타데이터·가변 Validation 길이만 확장했고 STEP3B의 학습/복원 kernel 부분은 바이트 동일함을 확인했다. 새로운 커널의 학습 실행을 했다는 의미는 아니다.

5Origin×10Seed×5Model=250fit/가격, A/B=500. 기존40 재사용 → 신규460. O1/O2 신규각80, O3/O4/O5 신규각100. 기존40의 Test 예측은 아직 생성하지 않았다. 가격·입력 배열·date·scaler·모델 소스·seed·환경·계약이 달라지면 재사용 판정을 무효화하고 새 identity/버전/예산 승인을 요청한다.

## 평가·통계 사전 사양

Primary=BA; Secondary=MacroF1/Brier/Recall0/Recall1, Accuracy와 positive prediction rate도 진단용으로 보존한다. Origin·Seed·가격별 결과를 모두 보고한다. 학습 중 모든 epoch의 단일 클래스 예측 비율, best epoch, 종료 epoch, 실패도 보존한다. Validation은 모델 선택에 사용됐으므로 독립 성능이 아니다.

날짜 paired moving-block bootstrap, 블록20/40/60,각10,000회, seed20261116을 고정한다. Origin 내부에서 실제 session_id가 연속인 블록만 재표집하며 모든 모델·Seed에 같은 날짜 index를 적용한다. 매 재표집에서 각 Seed의 지표를 계산한 뒤 Seed 평균, Origin은 동일 가중 평균한다. Seed를 시장 관측으로 연결하거나 확률 평균 앙상블로 바꾸지 않는다. 미완료 Seed는 임의 삭제하지 않고 추론을 BLOCKED로 둔다.

5모델의 모든10쌍×A/B=20 BA 가설을 하나의 가족으로 정하고 각 블록 길이별 Holm을 적용한다. Secondary4지표×20=80가족, Origin별 BA 진단은5×20=100가족으로 각각 고정한다. Origin별 Secondary와 레짐/τ는 기술적·탐색적 보고만 하고 새 p값 가족을 사후 추가하지 않는다. 모든 블록 길이를 보고하며 유리한 길이를 선택하지 않는다. 중심화 bootstrap p값은 근사값이고 percentile95%CI는 동시 신뢰구간이 아니다. 한 클래스 재표집은 BA/MacroF1 무정의로 세고, 무효율>10%면 해당 추론은 BLOCKED다. 실제 검정은 이번에 실행하지 않았다.

## 역사적 노출과 적용 한계

STEP3B O2 Validation2021은 O1 Test2021과 같은 역사적 연도다. 기존 논문 Test 결과도 존재한다. 이번 동결은 새로운 Test 성능 평가 전에 이루어졌지만 과거 결과를 전혀 보기 전의 등록이나 미관측 전향적 holdout이라고 주장하지 않는다. Origin 간 과거 데이터의 순차 편입은 허용하되 이미 관찰된 지표로 사양을 바꾸지 않는다. 가격/PIT 미확정과 함께 회고적 연구라는 한계를 유지한다.

상세: [가격/PIT](STEP3C_PRICE_AND_PIT_DECISION_KO.md), [실행계획](STEP3C_FULL_EXPERIMENT_PLAN_KO.md), [LNN](STEP3C_LNN_ENSEMBLE_PLAN_KO.md), [레짐/τ](STEP3C_REGIME_AND_TAU_PLAN_KO.md), [준비도](STEP3C_EXECUTION_READINESS_KO.md). 전체 가설은 config bootstrap.primary_family에20개 쌍으로 저장했다.
