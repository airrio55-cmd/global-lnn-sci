# 수정안 및 실험 프로토콜 — 승인 전 제안

버전: STEP2, 2026-11-16. 분석기간·모델·앙상블 사양은 사용자 지시로 확정. 18:00 KST 계약은 가용성 검증을 전제로 한 기본 제안. 학습/HMM fit/모델 forward/checkpoint 로드는 미승인·미실행. 기존 V14/V15 및 잠금 파일과 별개다.

## A. 사양을 먼저 고정

1. **사용자 확정 분석기간은 2010-01-01~2025-12-31이다.** 모든 원천 파일을 이 기간으로 먼저 필터링하고 그 파생 자료에서만 피처·label·fold·scaler·HMM·ablation·LTC 분석을 수행한다. 2026 관측은 입력 및 타깃 확인용으로도 절대 사용하지 않는다. 원본 바이트는 보존하며 원본을 읽어 SHA-256 및 제외 행 수를 세는 무결성 감사는 분석 이용과 구분한다. 2026 값을 이용한 타깃 보완 후보라는 이전 제안은 폐기한다.
2. 예측시각은 한국 거래일 t 18:00 KST를 제안한다. 한국 종가 t에서 t+20 KRX 세션까지 방향 `Close[t+20]>Close[t]`, 동률은0을 제안한다. **현재 원본은 window가 t-1에서 끝나므로 신규안은 window[t-19:t]로 한 세션 정렬을 바꾼다.** 원본 재현 사양은 그대로 별도 기록하고 두 성능을 같은 사양으로 비교하지 않는다. 이 타깃은 종가 이후 예측이므로 종가 t에서 거래 가능하다고 주장하지 않는다. 거래 전략을 평가하려면 다음 세션 진입 및 별도 수익률·비용 정의가 필요하다.
3. 각 feature에 event_time/available_at/timezone/source/age를 기록하고 available_at<=decision_time인 가장 최근 관측만 결합한다. 미국 지수는 원천 미국 거래달력/DST를 반영한 availability 기준 backward as-of join을 사용한다. 해외 휴일은 max_age와 함께 직전 알려진 지수만 유지한다. 결합 전 미국 관측을 보존하므로 한국 휴일 자료를 버리지 않는다. 단순 한국행 shift를 PIT 결합으로 간주하지 않는다.
4. 외국인 당일 순매수는 공표시각 증빙 전 사용하지 않는다. 검증된 전 세션 값만 쓰는 보수적 기본안과 외국인 제외 ablation을 제안한다. missing flow는 자동 ffill하지 않고 unavailable flag 및 제외/보수적 lag 규칙을 사전 고정한다.
5. 검증된 KRX 실제 세션 달력을 먼저 확보하고 재색인한다. label_end는 해당 달력에서 t 이후20번째 거래일이다. `Target=1(Close[t+20]>Close[t])`; 미래 종가가 없으면 nullable이며 0으로 변환하지 않는다. label_end가 2025-12-31을 넘거나 분석기간 안에 확정 가격이 없으면 평가 제외한다. 마지막20세션은 미확정으로 남긴다. 달력 중간 가격 누락도 채우지 않고 별도 제외/차단 사유로 기록한다. cutoff→캘린더 대조→feature/label→eligibility/window→purging 순서이며, 미확정 tail을 먼저 버려 알려진 과거 feature를 불필요하게 잘라내지 않는다. 미검증 observed-row shift는 진단용 후보 계산에만 허용하고 실험 입력으로 차단한다.
6. 입력 경로·SHA-256·source manifest를 명시하고 glob 첫 파일 로드는 폐기한다. 원본 파일은 보존하며 정제/파생물은 새 폴더에 쓴다. scaler는 각 origin train만 fit. 비유한값은 중단·기록하고 무조건0 치환하지 않는다.
7. 비교 사양은 RNN/LSTM/GRU/LTC/CfC, h128·1layer·dropout0.2·window20·batch64·AdamW0.005/wd1e-4·Focal(alpha0.25,gamma2)·OneCycle100·patience10·clip1·val BalAcc·threshold0.5로 사용자 지시에 따라 고정한다. 성능을 보고 이 수치를 변경하지 않는다. 모델 크기/파라미터 수를 보고하여 같은 hidden size가 같은 용량을 보장하지 않음을 명시한다.
8. FP32/AMP-off, seed 목록[2,12,22,32,42,52,62,72,82,92], raw offsets101/201/301/401/501, log offsets102/202/302/402/502로 고정한다. DataLoader generator도 동일 유효 시드로 고정한다. 환경변수는 프로세스 시작 전에 설정한다. ensemble은 각 raw/log 0.5, Hybrid는 다중 원본과 같은 `0.7*LNN_ensemble+0.3*RNN_raw`로 명시하여 단일 원본과의 차이를 숨기지 않는다.
9. 신규 학습·추론·레짐·통계는 별도 모듈로 분리하고 train 함수는 test 데이터/label을 받지 않는다. 최종 checkpoint 선택 완료 후 test는 고정된 평가에서만 처리한다.

## B. Rolling-Origin

순수 시간순 expanding train + 직전1년 validation + 다음1년 test를 제안한다. 적격 label 및 실제 거래일을 확정한 후 exact 날짜 manifest를 승인받는다.

| Origin | Train feature 기간 | Validation 기준연도 | Test 기준연도 |
|---|---|---|---|
| O1 | 2010~2019 | 2020 | 2021 |
| O2 | 2010~2020 | 2021 | 2022 |
| O3 | 2010~2021 | 2022 | 2023 |
| O4 | 2010~2022 | 2023 | 2024 |
| O5 | 2010~2023 | 2024 | 2025 |

train 표본은 label_end가 validation 시작보다 엄격히 이전, validation 선택 표본은 label_end가 test 시작보다 엄격히 이전이어야 한다. 실제 거래일 기준 보통 각 말단20개를 purge하되 timestamp assertion으로 결정한다. test2025는 label_end<=2025-12-31인 표본만 평가하며, 2026 종가로 보완하지 않는다. 현재 파일상 마지막 종가2025-12-30, 마지막 유효 기준일 후보2025-12-01, 2025-12-02~12-30의20개는 미확정이다. 경계 과거 feature context는 재사용하되 미래 label은 금지한다. 전체 과거에 한 번 fit한 scaler/HMM을 모든 origin에 재사용하지 않는다.

현재안은 train에 fit한 각 epoch를 validation으로 선택하고 train+valid 재학습은 하지 않는다. 그 재학습을 추가하면 epoch 규칙·fit 횟수·가용시각을 다시 승인받아야 한다. 다음 origin에서 과거 test가 학습 이력에 편입되는 것은 순차적으로 그 시점에 알려진 데이터이므로 허용하되, 연구자가 이전 test 결과를 보고 설계를 변경하지 않는다. 기존 자료·결과가 이미 관찰된 역사적 테스트임을 밝혀 완전 미관측 전향적 확인이라고 부르지 않는다.

주 지표는 balanced accuracy, 보조는 accuracy, macro-F1, class recall/precision, 확률 calibration/Brier를 제안한다. origin별·seed별·전체 날짜를 각각 보고하고 가장 좋은 seed/origin만 선택하지 않는다. label20일 중첩으로 관측 오차가 독립이 아니라는 점을 추론에 반영한다.

## C. 피처 ablation

미국 지수/외국인 데이터의 기여와 모델 종류 효과를 분리한다. 아래6개 사양은 동일 날짜·fold·label·모델 시드·학습 예산을 공유한다. 피처 결측 때문에 표본이 다르면 공통 교집합을 주 비교로 고정하고 가용 표본 결과는 별도다.

| 사양 | raw 채널 | log/local 채널 |
|---|---|---|
| F0 기본 | Log_Ret,Disparity,Foreign_Net,Nasdaq,SOX | Log_Ret,Disparity |
| F1 국내만 | Log_Ret,Disparity | Log_Ret,Disparity |
| F2 외국인 제외 | Log_Ret,Disparity,Nasdaq,SOX | Log_Ret,Disparity |
| F3 NASDAQ 제외 | Log_Ret,Disparity,Foreign_Net,SOX | Log_Ret,Disparity |
| F4 SOX 제외 | Log_Ret,Disparity,Foreign_Net,Nasdaq | Log_Ret,Disparity |
| F5 국내+외국인 | Log_Ret,Disparity,Foreign_Net | Log_Ret,Disparity |

F1은 같은 피처 두 채널을 다른 고정 시드로 학습한 ensemble이므로 '서로 다른 정보원 결합'으로 해석하지 않는다. 같은 local 채널의 재사용으로 예산을 줄일 수 있지만 무작위성·동일 checkpoint 계약을 별도 명시해야 한다. 여기 제시한3000 fit는 재사용 없는 상한이다. 지수 level→return 대체, 추가 macro feature, window 변경은 이번6개에 포함하지 않으며 결과를 보고 추가하지 않는다.

## D. HMM 민감도 — 신경망 예측 고정 후 별도 분석

주 레짐은 train Vol_Regime 30/70 분위수와 train-only HMM(full,2state,n_iter2000,tol1e-4,min_covar1e-4)을 제안한다. 초기화 후보는 모든 origin에서 공통10개 목록을 사용하고 train likelihood 최댓값을 선택한다. 수렴 여부·실패 이유·train state 점유율·transition·선택 seed를 보존한다. 부적격 후보 기준은 사전 확정하며 test 상태 개수를 보고 바꾸지 않는다. state 이름은 train posterior 가중 평균 변동성 또는 원단위로 역변환한 train state 평균으로 고정한다.

test는 train 마지막 filtering 분포를 validation·test의 알려진 과거를 통해 순차 전파해 `p(z_t|x_≤t)`만 쓴다. posterior smoothing 또는 test 전체 Viterbi는 retrospective 부록으로만 허용한다. collapse는 보고하고 억지로2개 상태를 만들지 않는다. train median을 이용한 단순 레짐은 HMM으로 이름 붙이지 않는다. 의사결정시각 이전 변동성만 레짐에 사용한다.

민감도는 모든 후보의 점유율·상태전환·entropy·레짐별 paired 차이를 보고하고 diag 대 full은 별도 비교로 지정한다. 신경망 checkpoint·확률은 그대로 둔다. 민감도 결과로 신경망 hyperparameter, HMM seed 목록, 레짐 임계값을 재조정하지 않는다.

## E. 통계 검정

동일 날짜에 대한 seed 반복은 새로운 시장 관측이 아니다. 원본의 seed-concatenated McNemar p-value는 확인적 근거로 사용하지 않는다. 단일 seed McNemar도 시간의존성을 없애지 못하므로 설명적 표로 한정한다.

주 추론은 각 날짜의 paired 정오차 차이를 seed 평균한 후 동일 날짜 block을 두 모델에 공통 재표집하는 paired moving-block bootstrap을 제안한다. block 길이20/40/60 KRX 세션은 사전 지정 민감도로 보고하며 가장 유리한 길이만 선택하지 않는다. balanced accuracy 차이는 bootstrap마다 클래스 비율·분모를 다시 계산한다. 단일 클래스 표본 처리 규칙도 고정한다. origin 경계를 넘는 가짜 연속 block을 만들지 않고 origin 내 재표집 후 고정 가중 집계한다. 10000 replicate와 고정 resampling seed를 제안한다.

시드별 효과 분포를 별도로 보고한다. 날짜/seed 양방향 불확실성을 다루려면 seed와 시간 block의 계층 bootstrap을 사전 선택하며, 소수 origin을 독립 큰 표본처럼 취급하지 않는다. primary family는 LNN Ensemble 기준 다른10개 보고 항목의 기본사양 비교로 고정하고 Holm 보정을 제안한다. ablation·regime·시간상수는 별도 family 또는 탐색적 분석으로 표시한다. Bonferroni/BH만 추가해 시계열·시드 의존성이 해결된다고 주장하지 않는다.

## F. LTC 시간상수 분석

원본에는 LTC 시간상수 추출·해석 코드가 없다. 승인 후 저장 checkpoint에 hook을 달아 train/validation/test forward-pass를 관측한다. ncps 정확한 버전·소스·solver substep·입력 timespan 단위를 고정하고 torch/no_grad 평가로 수집한다. 일별 규칙 시계열의 기본 dt=1이 실제 '1영업일'인지 확인한다. 주말·휴장 실제 경과시간으로 해석하려면 별도 timespan 입력 실험이 필요하다.

수동 회로 상수 `cm/gleak`와 상태·입력 의존 유효상수 `cm/(gleak+Σ recurrent conductance+Σ sensory conductance)`를 구분한다. 이는 해당 ncps 구현의 실제 ODE/solver에서 확인한 식으로만 계산하고 leak-only 값을 전체 memory 길이라고 부르지 않는다. 수치 적분의 cm/dt 항을 생물학적/경제적 시간상수로 오인하지 않는다.

unit×time×seed×origin별 분포(중앙값/IQR/5·95분위), 포화·극단값·비유한값·clamp 비율, 입력 민감도와 train-only 레짐별 분포를 제시한다. 레짐 차이에는 시간 block 불확실성을 적용하고 최적 unit/seed만 고르지 않는다. 효과와 성능의 연관은 탐색적이며 인과 설명으로 해석하지 않는다. neuron 단위 대응은 seed 간 임의적이므로 분포 기준 비교를 우선한다. clamp/시간상수 고정 개입, solver 변경, dt ablation은 새 모델 fit를 수반하므로 이번 제안에서 실행하지 않는다.

## G. 예상 실행 규모와 승인 조건

기본500 neural fit, 6사양 총3000 neural fit(기본 포함), 100epoch 상한으로 각각50000/300000 model-epochs. 기본10학습에서 11 보고 항목을 파생하므로 ensemble 자체 추가 fit는 없다. HMM 주 분석50 fit; full/diag 민감도를 모두 돌리면 합계100 fit. 반복 저장 checkpoint 분석은 추가 학습0회지만 forward-pass·저장 비용이 있다.

GPU 시간은 `Σ fit별 실제 epoch × epoch walltime + 평가/IO/HMM`으로 산출한다. 입력행 수와 LTC solver에 따라 큰 차이가 있으므로 임의의 GPU-hours를 약속하지 않는다. 승인 후 고정된 소규모 benchmark를 먼저 수행하고 전 규모 budget을 확인한다. 이번 단계의 실제 neural/HMM fit 횟수는 모두0이다.

분석기간, 모델 설정, seed, 피처6사양, Hybrid 고정식, 기본5 Origin, block20/40/60·10000회·Holm은 사용자 STEP2 지시로 고정했다. 남은 검토·증빙은 예측·진입시각과 실제 가용성, 외국인 metadata/보수적 lag·max_age, KRX 달력·누락 종가, runtime/ncps 단위 및 통계 family 세부 해석이다. 원천 가용성 증빙 및 정적 gate 통과 후에만 수정본을 구현·검토하고, 명시적인 학습 승인 후 실행한다. main 병합은 별도 승인 대상이다.

## H. STEP2 구현·실제 cutoff 진단

실행 비활성 설정은 `configs/experiment_config.json`, 원본 참조 사양은 `configs/original_reproduction_config.json`이다. 날짜 필터는 `src/kospi200/data.py:cutoff`, 실제 달력 target은 `labels_on_calendar`, PIT는 `us_schedule_records`와 `pit_join`, fold/scaler는 `folds.py`, HMM filtering은 `regimes.py`, 통계는 `statistics.py`, LTC snapshot 인터페이스는 `tau.py`에 있다. 실제 모델을 생성·forward하거나 HMM fit하는 함수는 제공하지 않는다.

KOSPI 3935→3894행(2026 41행 제외), 외국인5000→3939행(2010이전1020·2026 41 제외), NASDAQ/SOX 각각4067→4024행(2026 43 제외), 가공파일3854→3854행이다. KOSPI feature warmup40행 제외 후3854행, 관측행 기준 미확정 tail20개 제외 후3834개 후보, t포함20입력 window까지 요구하면3815개 후보(원본 t제외3814개)다. 이 수는 **공식 KRX 달력·PIT 검증 전 후보**이며 최종 실험 표본 수가 아니다.

외국인 파일에 있고 KOSPI에 없는 날짜가45개다. 실제 누락 세션 여부·가격을 공식 KRX 자료로 대조하기 전 `confirmed_samples`는 null/빈칸이며 Origin별 상태는 전부 BLOCKED다. `manifests/rolling_origin_manifest.csv`는 observed 경계와 candidate purge 수를 기록하고 **확정 KRX 경계라고 표시하지 않는다**. 예컨대 파일상2022 첫 관측은01-04이지만 외국인 파일에는01-03이 있어 경계 확정에 사용할 수 없다. 진단상 train/validation purge는 각 Origin20개씩이고 실제 수는 달력 검증 후 다시 산출한다.

KOSPI의 마지막 관측일12-30과12-31 휴장은 KRX KIND의 [2025년 공시 안내](https://kind.krx.co.kr/external/dst/notice/11158/%5B%ED%95%9C%EA%B5%AD%EA%B1%B0%EB%9E%98%EC%86%8C%5D%202025%EB%85%84%20%EC%98%AC%EB%B9%BC%EB%AF%B8%EA%B3%B5%EC%8B%9C%20%EC%95%88%EB%82%B4.pdf) 연말 일정과 부합한다. 이 안내는 전체2010~2025 KRX 세션 달력을 대신하지 않는다.

NASDAQ/SOX의 미국 source_date가2025-12-31이어도 그 종가가 한국2026-01-01에 가용하면 한국2025 의사결정에는 결합되지 않는다. 가용시각을 확인하지 못한 실제 자료는 모두 BLOCKED로 남긴다. 실제 per-sample lineage는 생성할 수 없으며 source ledger와 스키마만 보존한다.

LTC 식의 구현 기준은 [ncps LTC 소스 고정 커밋](https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py)이다. STEP2에서 이 소스를 읽어 식·입력 affine mapping·sparsity·softplus 제약을 확인했으나 런타임 ncps/torch 설치·실제 단위가 확정되지 않아 실자료 tau 분석은 BLOCKED다. 합성 숫자 snapshot 계산만 검증한다.
