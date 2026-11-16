# 국민대학교 박사학위논문 KOSPI 200 정적 감사

감사일: 2026-11-16 (Asia/Seoul). 상태: **수정안 검토용 / 학습 미실행**.
저장소: airrio55-cmd/global-lnn-sci. 기준 main 커밋: `3324ead54266b07df176d312b6604289b50523a8`.
별도 브랜치: `audit/kookmin-kospi200-20261116`; 별도 경로: `experiments/kookmin_kospi200/`.
V14/V15 Journal of Forecasting, 기존 잠금 파일, 기존 노트북 및 워크플로는 수정 대상이 아니다.

## 1. 범위와 증거

처음 확인한 /workspace, library-files, shared/downloads에는 원본이 없었다. 이후 사용자가 첨부한 노트북 3개와 CSV 5개를 모두 실제 환경으로 다운로드했다. 노트북은 각각 18셀이다. JSON·AST·셀 소스·데이터만 읽었고 셀 실행, torch 모델 생성, optimizer step, HMM fit, 전체 실험은 하지 않았다. 첨부 문서의 지시·주석은 감사 대상이며 사용자 지시로 실행하지 않았다. 저장된 과거 출력은 이번 실행 결과로 사용하지 않았다.

원본 SHA-256과 바이트 수는 `evidence/input_manifest.json`, 각 셀 해시와 텍스트 동일 여부는 `cell_comparison.csv`, 셀별 소스는 `*_cells.txt`, 전체 비교는 `*.diff`, 데이터 감사는 `data_inventory.json`, 재현 수치는 `data_only_checks.json`에 있다. 전체 셀 소스와 diff는 작업 환경 전용으로 보존하고 공개 브랜치에는 게시하지 않는다. 위치는 **노트북의 실제 1부터 시작하는 셀 번호와 해당 셀 내부 행 번호**다. 노트북 주석의 [Cell N]은 실제 번호와 다르므로 사용하지 않았다.

## 2. 18셀 비교

| 실제 셀 | 내용 | 단일 → 5개 시드 | 5개 → 10개 시드 |
|---|---|---|---|
| 1 | 안내 Markdown | 동일 | 동일 |
| 2 | 환경 출력 | 동일 | 동일 |
| 3 | imports, 경고 전체 무시 | 동일 | 동일 |
| 4 | DEVICE | 동일 | 동일 |
| 5 | 설정·시드 | [42] → [42,52,62,72,82], CUBLAS_WORKSPACE_CONFIG 추가 | [2,12,22,32,42,52,62,72,82,92] |
| 6 | FocalLoss·이전 EarlyStopping·초기화 | 동일 | 동일 |
| 7 | 이전 모델 정의 | 동일 | 동일 |
| 8 | 최종 모델·초기화·EarlyStopping 재정의 | 동일 | 동일 |
| 9 | CSV 로드·feature·target·분할 | 계산 동일, 안내문 변경 | 계산 동일, 5-day → 20-day 안내문 |
| 10 | scaler·window tensor | 동일 | 동일 |
| 11 | HMM | 함수 정의 → 최상위에서 즉시 fit; diag→full 등 | **동일: 10개판도 후보 5개** |
| 12 | 학습 함수 | AMP 자동 활성 → 기본 비활성; seeded DataLoader generator | 동일 |
| 13 | 결과 저장 | McNemar 저장 구조 추가 | 주석만 변경 |
| 14 | 주 학습·예측·레짐 | 시드 offset·Hybrid 수식 변경, HMM 함수 중복·반복 fit | 함수 내부 HMM 후보 5→10개 |
| 15 | 평균±표준편차 | 동일 | 동일 |
| 16 | 수동 레짐 결과 | 단일은 여기서 HMM 실행, 다중은 이미 계산한 결과 출력 | 동일 |
| 17 | HMM 결과 출력 | 안내문 변경 | 동일 |
| 18 | McNemar | 단일 첫 시드 근사 검정 → 시드 연결·정확 이항·다중보정 | 안내문만 변경 |

모델 정의(최종 셀 8)는 모두 동일하다. RNN/LSTM/GRU, LTC를 쓰는 LNN, CfC의 5개 아키텍처에 5-feature/2-feature 채널 각각을 학습한다. 원본의 '11종'은 신경망 11개가 아니라 **기본 학습 10회 + 조합으로 만든 11개 보고 항목**이다. TFTLite는 정의되지만 학습 목록에 없다. h=128, layer=1, dropout=0.2, window=20, batch=64, 최대100 epoch, patience=10, threshold=0.5가 공통이다.

입력은 raw=[Log_Ret,Foreign_Net,Nasdaq,SOX,Disparity], log=[Log_Ret,Disparity]. 이름과 달리 log 채널은 raw의 부분집합이다. Vol_Regime은 모델 입력이 아니라 레짐용이다. StandardScaler는 train만 fit하고 valid/test에는 transform하여 이 부분은 적절하다. 다만 nan_to_num으로 비정상 입력을 조용히 0으로 바꾼다.

손실은 셀6 FocalLoss, 셀12에서 gamma=2, alpha=0.25를 공통 사용한다. alpha가 클래스별 가중치가 아니라 모든 샘플의 손실을 동일 배율로 줄이므로 불균형 클래스 보정이라고 해석하면 안 된다. optimizer=AdamW(lr=0.005,weight_decay=1e-4), scheduler=OneCycleLR(max_lr=0.005,100 epochs 기준 batch별 step), gradient clip=1.0은 동일하다. 최종 EarlyStopping은 셀8 정의이며 validation balanced accuracy 최대화, deepcopy checkpoint, 동점은 patience 증가다. 셀6의 val_loss·참조 state_dict 구현은 순서대로 실행하면 덮어써진다.

단일은 CUDA에서 AMP=True, 다중은 use_amp=False다. raw offset은 101/201/301/401/501 공통이나 log offset은 단일 111/211/311/411/511, 다중 102/202/302/402/502다. Hybrid도 단일 `0.7*LNN_ensemble+0.3*RNN_ensemble`, 다중 `0.7*LNN_ensemble+0.3*RNN_raw`로 다르다. 따라서 단일 대 다중 결과 차이를 시드 수 효과로만 설명할 수 없다.

## 3. 발견 사항과 수정 위치

CRITICAL은 주요 성능·유의성 또는 실시간 해석을 무효화할 수 있는 항목, MAJOR는 비교 공정성·재현성·데이터 품질에 중요한 항목, MINOR는 문서·표시상의 항목이다. 확정 사실과 조건부 위험을 구분했다.

| ID | 수준 | 위치·확인 증거 | 수정안 |
|---|---|---|---|
| C01 | CRITICAL | 전 노트북 셀9 L34: `(Close.shift(-20)>Close).astype(int)`; 미래가격 없는 마지막20행이 False→0, dropna도 제거 못함 | future_close/label_end를 먼저 만들고 nullable Target, 확정 label만 평가 |
| C02 | CRITICAL | 셀9 L24–28: 미국 지수를 날짜만으로 결합; 시간대·available_at·shift 없음 | 원천 미국 세션 종료·발표시각을 한국 의사결정시각과 backward as-of 결합 |
| C03 | CRITICAL(분할시각 계약 미정) | 셀9 L42–45: 원자료 60/20/20 뒤 purging 없음; train/valid 말단 label은 다음 파티션 가격 사용 | fold fit/선택 cutoff를 명시하고 label_end < cutoff만 허용; 아래 경계 해석 참조 |
| C04 | CRITICAL | 다중 셀18 L97/107/127: 동일 날짜 정답을 시드별 복제한 concatenate; exact binomial도 독립성 회복 못함 | 날짜별 paired 차이와 block bootstrap, 시드는 반복성 요인으로 분리 |
| C05 | CRITICAL(실시간 레짐 주장 시) | 단일 셀11 `best_hmm.predict`, 다중 셀11 L74/셀14 L75: test 전체 Viterbi 경로 | train에만 fit, 순방향 filtering p(z_t|x_≤t), 미래 불변성 검증 |
| M01 | MAJOR | 셀9 L28 `.bfill()`은 미래 채움 가능. **이번 입력의 실제 적용은 0건** | bfill 제거; 초반 결측은 제외하거나 train-only 규칙; feature별 ffill 유효기간 |
| M02 | MAJOR | 단일 셀11 및 다중 셀11 L13–14/셀14 L27–28: test 30/70 분위수; 상태 이름도 test 평균 변동성으로 정렬 | train 분위수와 train state 평균으로 고정; retrospective 표는 명확히 구분 |
| M03 | MAJOR | 다중 셀11 L96/셀14 L73,L86: HMM 실패·collapse 시 test median으로 대체 | HMM 실패를 실패로 보고; train 기준 대체 레짐은 별도 명칭; 실패 횟수 기록 |
| M04 | MAJOR | 셀11·14: HMM 공분산/반복수/후보 집합·실행 위치 차이 | 신경망 시드와 HMM 초기화 집합 분리, 예측 고정 후 민감도 검증 |
| M05 | MAJOR | 셀12·14: AMP·loader·log offset·Hybrid 조합식 차이 | 독립 프로젝트에서 하나의 명시적 사양으로 고정 후 승인 |
| M06 | MAJOR | 셀10 L17: X=[t-20,t-1], y=Target[t]; label은 Close[t]→Close[t+20], 레짐은 x[t] 사용 | 예측시각, 진입시각, label_start/end, regime_available_at의 계약 및 date-key 검증 |
| M07 | MAJOR | 셀9 smart_load glob 첫 파일, absent→None, 인코딩 분기 실효 없음 | 정확한 경로·해시 manifest, 0개/복수 파일 시 중단, 컬럼·단위·날짜 검증 |
| M08 | MAJOR | CSV는 공표시각·공급처 메타데이터 없음; 외국인 데이터 시장범위·단위도 불명 | PIT provenance와 개정정책 확보; 확인 전 당일 값 가용성 주장 금지 |
| M09 | MAJOR | KOSPI 2026-03-05 OHLC 일부와 거래량0, SOX Volume 전행0; 2026 데이터 포함 | 비결측과 유효 관측을 분리 검사; 사용기간·필드·제외 규칙 사전 승인 |
| M10 | MAJOR | 셀3 경고 전체 무시, deterministic 실패 무시, 런타임 PYTHONHASHSEED 설정 | HMM 수렴/공분산 경고 보존, 실패 로그, 실행 전 환경변수, 패키지·GPU 버전 기록 |
| M11 | MAJOR | 단일 셀18 미보정 10비교; 다중 exact·Bonferroni/BH도 시계열 의존성 미처리 | paired block 추론을 주 분석으로, 비교 family·Holm 등 사전 명시 |
| N01 | MINOR | 셀7 미정의 LNN을 참조하는 구 정의가 셀8로 덮임; EarlyStopping·init_weights 중복 | 신규 코드에서는 단일 정의, 원본 보존 |
| N02 | MINOR | 5개판 셀9/14 5-day 표기, 셀10 WINDOW_SIZE=50 주석; 실제는 모두20 | 표시·사양 일치 |
| N03 | MINOR | 셀15 np.std ddof=0; 단일 시드 ±0 | 표준편차 정의와 시드 수 표기; CI로 오해하지 않도록 분리 |

C05·M02·M03은 현재 예측에 레짐을 입력하지 않는 후처리이므로 그 자체가 신경망 예측값을 바꾼다는 증거는 아니다. 문제는 미래를 사용하는 그룹별 성능표를 실시간 레짐 예측이나 거래 가능한 결과로 해석하는 것이다. HMM 후보 선택 기준은 **train log-likelihood**이며 test 성능으로 HMM을 선택하는 코드는 발견되지 않았다.

## 4. Target, 시차, 결합의 실제 데이터 영향

원자료 3,935행 중 rolling40 등 초기 계산 후 3,895행이 남는다(2010-03-04~2026-03-05). 마지막 2026-02-02~2026-03-05의 20행은 정답 미확정인데 전부 0이다. 현재 test 759개 평가 중 20개(약2.64%)가 해당하며 실제 성능 변화 방향은 예측이 없으므로 계산·추정하지 않았다. 20은 현재 KOSPI 파일의 **20행**으로 구현되어 있고 KRX 거래일 완전성 확인 전 '20영업일'과 동일하다고 확정할 수 없다.

원본5파일은 셀 값 NaN·날짜 중복이 모두0이다. KOSPI 날짜 기준 join 이후 Nasdaq/SOX 각각101개가 NaN이 되고 모두 ffill로 채워진다. Foreign_Net은 결합 결측0, 실제 bfill0. KOSPI에 없는 미국 거래일233개는 left join 시 사라진다. 따라서 미국의 가장 최근 거래일이 한국 휴일이었던 경우, 결합 후 ffill은 그 관측을 건너뛰고 더 오래된 값을 쓸 수도 있다. 단순 `shift(1)`은 시간대·다른 거래달력을 완전히 해결하지 못한다.

미국 정규장 종가는 통상 뉴욕16:00, 한국 다음날05:00(서머타임)/06:00(표준시)에 대응한다. CSV의 미국 날짜 d 종가를 한국 d일 피처로 쓰면 한국 d일 장중/종가에는 아직 알 수 없다. 현재 window가 하루 전까지 끝나므로 '정답일 t 장 시작 전 예측'으로 정의하면 전날 미국 값이 가용할 수도 있다. 반대로 '입력 마지막 날 t-1 한국 종가 예측'이면 그날 미국 종가는 미래다. **의사결정시각이 없으므로 전 관측이 확정 누출이라고 단정하지 않지만, 현재 same-date 결합에는 실시간 정당화가 없다.**

외국인 순매수는 날짜만 있고 잠정/확정 공표시각·단위·시장범위가 없다. 한국 종가에 바로 확정됐다고 가정하면 안 된다. 우선 보수적으로 다음 한국 세션부터 사용하는 안을 제시하되, 원천 공표시각과 수집 latency로 최종 lag를 정해야 한다. 일별 순매수는 flow이므로 휴장·결측일을 ffill하면 전일 flow를 재사용한다. 집계에서는 중복 계상 위험이 있으며, 결측은 휴장/미수집으로 구분해야 한다.

`processed_regression_data.csv`는 세 노트북에서 읽지 않는다. 감사상 보조파일로 분리했다. KOSPI200은 원본 종가와 부동소수점 오차 내 일치, Target_Ret20은 원본20행 선행수익률과 최대오차 약2.0e-16으로 일치한다. SOX_Lag1은 이 가공파일 내 직전 행 SOX와 일치하지만 이것은 미국 세션 lag나 PIT 가용성의 증명이 아니다. 생성 코드와 데이터 lineage가 없어 NASDAQ/외국인20일 집계의 정확한 생성·보간 규칙은 미확인이다.

## 5. 분할과 purging의 정확한 해석

| 구간 | 원시 분할 범위 | 행 수 | 평가 label 수 | 첫 평가 label 날짜 |
|---|---|---:|---:|---|
| Train | 2010-03-04~2019-10-24 | 2337 | 2317 | 2010-04-01 |
| Validation | 2019-10-25~2022-12-20 | 779 | 759 | 2019-11-22 |
| Test | 2022-12-21~2026-03-05 | 779 | 759 | 2023-01-19 |

train 마지막 label의 끝은2019-11-21로 validation 원자료 구간 안이다. validation 마지막 label의 끝은2023-01-18로 test 원자료 구간 안이다. 분할 시작일을 model fit/선택 cutoff로 해석하면 각각 마지막20개 label을 purge해야 한다. validation을 사용한 early stopping 또한 label_end가 test cutoff 이전인 표본으로 제한해야 한다.

단, 각 파티션에서 window20개를 버려 첫 평가 label이 뒤로 밀리므로 train label 끝(11-21)과 첫 valid scored label 시작(11-22), valid label 끝(01-18)과 첫 test scored label 시작(01-19)은 겹치지 않는다. **따라서 평가 label끼리 직접 겹친다고 주장하면 부정확하다.** 실제 fit/선택 시각을 이 뒤 시점으로 두는 설계라면 일부 경계 사용은 가용할 수 있다. 이 경우 파티션·cutoff·사용한 feature context를 명시적으로 다시 정의해야 한다. 현재 코드에는 그런 계약·assertion이 없다.

권장 규칙: 거래일 캘린더에 label_start/label_end와 available_at을 명시하고, 다음 fit/평가 경계 c에 대해 이전 집합의 `label_end < c`를 요구한다. 날짜 고정 후 purge하며, purge 후 60/20/20 비율을 다시 맞춰 경계를 이동하지 않는다. 이미 알려진 과거20일 feature context는 다음 구간의 window를 만드는 데 재사용 가능하나 그 label을 이전 학습에 추가하면 안 된다. 시간순 확장 학습에는 미래 샘플을 훈련하지 않으므로 별도 사후 embargo가 항상 필요한 것은 아니다. 비순차 검증 또는 겹치는 fold 사용 시 정보구간 교차를 제거하고 추가 embargo 길이는 사전 등록한다.

## 6. HMM과 모델 비교를 분리

| 사양 | 단일 | 5개 | 10개 |
|---|---|---|---|
| 셀11 후보 | [42] (함수, 셀16에서 실행) | [42,52,62,72,82] | **[42,52,62,72,82] 그대로** |
| 셀14 함수 후보 | 해당 없음 | [42,52,62,72,82] | [2,12,22,32,42,52,62,72,82,92] |
| covariance | diag | full | full |
| n_iter | 200 | 2000 | 2000 |
| tol/min_covar | 라이브러리 기본값 | 1e-4/1e-4 | 1e-4/1e-4 |
| collapse/fail | 실패 raise, 별도 median fallback 없음 | test median fallback | test median fallback |

순서대로 전체 실행 시 HMM fit 시도는 단일1회, 5개35회(셀11 5 + 루프5×5 + 마지막5), 10개115회(셀11 5 + 루프10×10 + 마지막10)다. 같은 train 자료와 같은 HMM 후보를 신경망 시드마다 반복 fit하므로 불필요한 중복이다. 결과 표에 보이는 HMM은 마지막에 재계산한 것이다.

주 모델 비교: 공통 데이터·피처·신경망 시드·정밀도·Hybrid·하나의 고정 train-only 레짐 사양으로 수행한다. HMM은 fold별 한 번 fit/cache한다. 별도 민감도: 신경망 예측을 고정하고 HMM 초기화/공분산만 바꿔 state 점유율·수렴·transition·레짐별 성능 변동을 보고한다. 후보 train likelihood 최댓값 선택을 포함한 절차 전체를 고정하며 test를 보고 후보를 늘리지 않는다. 기존 단일/5개/10개 결과는 서로 다른 사양의 역사적 결과로 보존한다.

## 7. 데이터 실재성과 출처

| 파일 | 행 | 날짜 범위 | 원본 결측/중복날짜 | 판단 |
|---|---:|---|---|---|
| KOSPI_200.csv | 3935 | 2010-01-04~2026-03-05 | 0/0 | 종가 양수, 마지막 행 OHLC 일부·거래량0 |
| Foreigner_Net.csv | 5000 | 2005-11-24~2026-03-05 | 0/0 | 단위·시장범위·공표시각 불명 |
| Nasdaq.csv | 4067 | 2010-01-04~2026-03-05 | 0/0 | 미국 날짜/시간대 표기 없음 |
| SOX.csv | 4067 | 2010-01-04~2026-03-05 | 0/0 | Volume 4067행 모두0; 종가 사용과 구분 |
| processed_regression_data.csv | 3854 | 2010-02-01~2025-12-01 | 0/0 | 현 노트북 미사용; 생성 코드 불명 |

8개 입력의 바이트 단위 SHA-256은 manifest에 전부 기록했다. CSV는 모두 UTF-8 계열로 읽히고, 숫자 컬럼 비유한값0·날짜 파싱 실패0이다. 모든 입력은 사용자 첨부로 받았으나 원천 공급처를 뜻하지 않는다. pykrx import만으로 CSV가 KRX 원천이라고 확인할 수 없다.

저장소 `data/KOSPI200_provenance.json`은 기존 사용자 원본 KOSPI_200.csv를 보존했다고 서술하며 SHA-256 `7612a3ea53427dcf0148ab6b1e22f34500e6bff6fe1f23e2da793e40b0b82c50`를 기재한다. 이번 첨부 KOSPI 파일과 정확히 일치한다. 이는 동일 파일이라는 증거이지 원천 공급처·거래일 완전성 증거는 아니다. 기존 provenance의2010~2025 기간 규칙은 **기존 실험의 규칙**이며 이번 별도 박사학위 실험에 자동 적용하지 않았다. 이번 기간은 승인안에서 별도로 제시한다.

추가 요구: 원천 URL/서비스·symbol·다운로드일·추출 코드·조정주가 여부·라이선스, KRX 거래일 캘린더, 미국 세션 캘린더·DST·available_at, 외국인 순매수 단위·현물/선물 및 시장·잠정/확정 공개시각·개정 이력, 0값 행 설명, 가공파일 생성 코드. 미확정 마지막20일을 평가하려면 이후 최소20 KRX 세션의 검증된 가격이 필요하다. 확보하지 못하면 해당 label을 평가에서 제외한다. 검증용 미래가격은 타깃 전용이며 입력 피처에 사용할 수 없다.

## 8. 수정 전후 테스트·실행 규모

상세는 `TEST_PLAN_KO.md`, `PROTOCOL_KO.md` 참조. 이번 단계에서 독립 데이터 재현·합성 regression 검사7개만 수행했고 모두 통과했다. 이것은 학습 코드 수정 완료 또는 모델 성능 검증을 의미하지 않는다. 원본은 수정하지 않았다.

원본 세 노트북을 모두 돌리는 가상 규모는 기본 신경망160회(10+50+100), 최대16000 model-epochs, HMM151 fit 시도다. 현재 train tensor2317개, batch64이므로 epoch당37 batch; 최대592000 batch update 시도에 해당한다(early stopping에 따라 감소). 실제로 실행하지 않았다.

제안 신규 기본 프로토콜은 5 origin×10 seed×10 기본 모델=500 fit, 최대50000 model-epochs이며, 6개 피처 사양을 전부 포함하면 총3000 fit, 최대300000 model-epochs다. HMM 5 origin×공통후보10개=50 fit를 cache하여 신경망 시드와 분리한다. LTC 시간상수 관측은 기존 checkpoint 분석으로 추가 fit0회, 사전 지정 개입 실험을 추가한다면 별도 승인이 필요하다. GPU 시간·VRAM은 LTC solver·자료길이·early stopping에 의존하므로 측정 없이 시간 수치를 만들지 않았다. 승인 후 소규모 사양 고정 benchmark로 추정한다.

승인 전 금지: 결과 기반 하이퍼파라미터/가중치/임계값 변경, 모델/HMM 재학습, 원본 결과 덮어쓰기, main 병합. 새 설정은 training_enabled=false이며 학습 진입점·자동 실행 workflow를 추가하지 않는다.
