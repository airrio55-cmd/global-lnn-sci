# STEP13 33편의 근거 범위별 비교표

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 판독 계약

저자/연도·정확한 제목·학술지/학회·DOI는 L번호의 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md) 행과 일대일 연결한다. 각 카드의 구체 필드는 표시한 출처·관련 절 범위에 한정된다. UNKNOWN은 미확인, NOT_REPORTED는 **판독한 관련 절**에 해당 보고가 없다는 뜻이다. N/A는 비금융 task 등 해당 비교축 자체가 적용되지 않는 경우다. UNKNOWN을 ‘분석하지 않았다’고 바꿔 읽지 않는다. 코드를 실행하거나 저자들의 성능/통계를 재현하지 않았다.

18편은 전문 관련 절 심층 비교, 나머지15편은 제한 검토 카드다. 제목에 LNN이 있어도 구현 LTC/CfC를 임의로 채우지 않는다.


## L01 — Hasani, Lechner, Amini, Rus & Grosu (2021)

원천: [L01](https://ojs.aaai.org/index.php/AAAI/article/view/16936). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 비금융11개 시계열 benchmark |
| 예측기간 | 과제별; 금융20일 아님 |
| 사용 모델 | LTC, LSTM, CT-RNN 등 |
| LTC/CfC 실제 구현 확인 | LTC ODE/fused solver 정의; 현재 ncps 실행동일성은 미검증 |
| Seed 반복 | Table3 n=5 반복; seed 목록 UNKNOWN |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 시간상수 τ 분석 | 상태/입력 의존 τ 및 bounds |
| 레짐 분석 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 평가 지표 | Accuracy/F1 등 과제별 mean/SD |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | LTC 구조·유계 동역학·표현력 |
| 주요 한계·우리 연구와 차이 | 유계상태는 단일클래스 방지 정리 아님 |
| 근거 위치/확인 범위 | Eq1·동역학 bounds·Experimental Evaluation/Table3 |

## L02 — Hasani et al. (2022)

원천: [L02](https://www.nature.com/articles/s42256-022-00556-7). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 비금융 이벤트/물리/의료 등 |
| 예측기간 | 과제별 |
| 사용 모델 | CfC, LTC, ODE/RNN 비교 |
| LTC/CfC 실제 구현 확인 | CfC 근사 폐쇄형; LTC와 다른 실행 셀 |
| Seed 반복 | 일부 결과 n=5 mean/SD |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 시간상수 τ 분석 | LTC 유도와 CfC 시간의존 표현 |
| 레짐 분석 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 평가 지표 | Accuracy/AUC/MSE·실행시간 등 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 수치 solver 부담을 줄인 연속시간 모델 |
| 주요 한계·우리 연구와 차이 | 현재 LTC τ를 CfC 셀의 동일 파라미터로 볼 수 없음 |
| 근거 위치/확인 범위 | Explicit time dependence·Methods·Extended Data |

## L03 — 고영보·안현철 (2025)

원천: [L03](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003273926). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | KOSPI(전체지수; KOSPI200과 구별) |
| 예측기간 | 초록: 미래7일; 실제 거래세션 정의 UNKNOWN |
| 사용 모델 | LTC, RNN/LSTM/GRU |
| LTC/CfC 실제 구현 확인 | 초록 LTC 표기; 최종 클래스/라이브러리 UNKNOWN |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | 국면 포착 서술은 있음; 명시적 HMM/레짐 평가는 UNKNOWN |
| 평가 지표 | 초록 AUC/Accuracy/Recall/Precision/F1/BA |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 이미 KOSPI 이진 방향에 LTC 적용 |
| 주요 한계·우리 연구와 차이 | 전문 미확보; 기간/지표를 현재20session 결과와 직접 비교 불가 |
| 근거 위치/확인 범위 | KCI 초록·서지 L03; 본문 미확보 |

## L04 — Gajjar, Saxena, Acharya, Shah, Bhatt & Nguyen (2024)

원천: [L04](https://link.springer.com/article/10.1007/s41870-023-01506-1). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 인도 NSE 개별주3종 |
| 예측기간 | UNKNOWN(초록에 정확 지평 없음) |
| 사용 모델 | LTC/양방향 계열, RNN/GRU/LSTM/BiLSTM |
| LTC/CfC 실제 구현 확인 | 초록 LTC 표기; 코드/최종 cell UNKNOWN |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 정확도·계산 효율 비교라는 초록; 상세 metric UNKNOWN |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 이미 주가에 LTC/양방향 구조 적용 |
| 주요 한계·우리 연구와 차이 | 구독 preview; 회귀/방향·seed·τ 세부 판단 보류 |
| 근거 위치/확인 범위 | Springer/Monash 초록·서지; 전문 미확보 |

## L05 — Papyan, Han & Donoho (2020)

원천: [L05](https://pmc.ncbi.nlm.nih.gov/articles/PMC7547234/). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지 분류 benchmark |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | 여러 supervised deep classifier |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | Neural Collapse NC1~4 geometry |
| 시간상수 τ 분석 | LTC τ 분석 아님 |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 분류오류·표현/분류기 geometry |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | terminal training에서 class-wise 기하구조 관찰 |
| 주요 한계·우리 연구와 차이 | 전체 Test 단일 label과 다른 관측 정의 |
| 근거 위치/확인 범위 | 본문 NC1~4·training/experiments |

## L06 — Levchenko, Rappos, Ataee, Nigro & Robert-Nicoud (2025)

원천: [L06](https://link.springer.com/article/10.1007/s41060-024-00690-y). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 일본·독일·미국 금융 고객 데이터 |
| 예측기간 | 5일/10일 방향 |
| 사용 모델 | MLP/CNN/RNN/LSTM/TFT 계열 NAS |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 탐색15회, 최종50회 |
| Walk-forward 평가 | 고정 시간순70/20/10;5Origin walk-forward와 다름 |
| 클래스/퇴화 진단 | 상수예측의 accuracy 문제 논의; LTC 진단 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | 미국 시기 변화 해석; HMM 층화 아님 |
| 평가 지표 | AUC/BA/F1·Seed SD |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 금융 분류에서 seed 분산을 이미 상세 분석 |
| 주요 한계·우리 연구와 차이 | 사유 데이터; 시드 반복만으로 저신호 해결 못함 |
| 근거 위치/확인 범위 | §2,§5.2~5.4,§6~7 |

## L07 — Coakley & Gundersen (2026)

원천: [L07](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328564/). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지·일반 시계열 예측 |
| 예측기간 | 데이터/과제별 |
| 사용 모델 | ResNet/ViT 및 Autoformer/iTransformer/NLinear/TSMixer |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 186설정×100seed 반복 |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 극단적 저성과 꼬리; LTC label 진단 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 평가 지표 | 평균·spread/skew/tail·과제별 오차 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 평균 성능과 robustness가 다름을 이미 검토 |
| 주요 한계·우리 연구와 차이 | 금융 LTC 원인이나 동일실험 재현 증거 아님 |
| 근거 위치/확인 범위 | Experimental Design·Evaluation Metrics·Results/Discussion |

## L08 — Buckmann & Joseph (2022)

원천: [L08](https://www.bankofengland.co.uk/working-paper/2022/an-interpretable-machine-learning-workflow-with-an-application-to-economic-forecasting). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 미국 거시 FRED-MD 실업률 |
| 예측기간 | 1년 앞 변화 |
| 사용 모델 | NN/SVR/tree/linear |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 10seed 예측 변동·평균 |
| Walk-forward 평가 | 시간별 OOS 및 blocked/hv-block 비교 |
| 클래스/퇴화 진단 | 분류 퇴화 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | 기간/위기 전후 비교; HMM 아님 |
| 평가 지표 | MAE·예측범위·Shapley |
| 검정 방법 | Shapley 회귀 등; 현재 금융검정과 별개 |
| 실제 기여(이 검토의 요약) | 경제예측에서 성능–안정성 tradeoff 선행 |
| 주요 한계·우리 연구와 차이 | 회귀·working paper; 현재 통계 타당성 인증 못함 |
| 근거 위치/확인 범위 | PDF pp22~24/FigVI 및 workflow |

## L09 — Bouthillier et al. (2021)

원천: [L09](https://proceedings.mlsys.org/paper_files/paper/2021/hash/0184b0cd3cfb185989f858a1d9f5c1eb-Abstract.html). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 복수 ML benchmark |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | 여러 task/architecture |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 초기화·표본·HPO 변동 분해 |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | NOT_REPORTED(이번에 확인한 관련 절 범위) |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 성능 차이·변동·오류율 |
| 검정 방법 | benchmark 비교 추정/검출 성질 연구 |
| 실제 기여(이 검토의 요약) | 반복Seed만 아니라 여러 변동원 고려 |
| 주요 한계·우리 연구와 차이 | 현재5Origin 의존성 검정의 자동 대체 아님 |
| 근거 위치/확인 범위 | benchmarking model·variance sources·comparison |

## L10 — Henderson, Islam, Bachman, Pineau, Precup & Meger (2018)

원천: [L10](https://ojs.aaai.org/index.php/AAAI/article/view/11694). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 강화학습 MuJoCo |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | TRPO/DDPG/PPO 등 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 기본5 trials, seed10 분할 예 |
| Walk-forward 평가 | RL 평가; 금융 walk-forward N/A |
| 클래스/퇴화 진단 | 성능 불안정·재현성; label 퇴화와 구별 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | return·학습곡선·seed 변동 |
| 검정 방법 | t검정/KS/bootstrap 제시(원 논문) |
| 실제 기여(이 검토의 요약) | Seed/구현 조건이 결과를 바꿀 수 있음 |
| 주요 한계·우리 연구와 차이 | RL 검정 권고를 현재 종속 금융자료에 이식 불가 |
| 근거 위치/확인 범위 | Random Seeds and Trials·reporting sections |

## L11 — Pascanu, Mikolov & Bengio (2013)

원천: [L11](https://proceedings.mlr.press/v28/pascanu13.html). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 합성/시퀀스 학습 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | RNN |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | vanishing/exploding gradient; 단일 label 증명 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 학습오차·gradient 동역학 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | gradient norm clipping·학습 난점 설명 |
| 주요 한계·우리 연구와 차이 | 현재 퇴화 원인을 관측만으로 연결 불가 |
| 근거 위치/확인 범위 | gradient analysis·clipping·experiments |

## L12 — Tallec & Ollivier (2018)

원천: [L12](https://arxiv.org/abs/1804.11188). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 장기 의존 시퀀스 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | gated RNN/LSTM/GRU |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | gradient/장기 의존; 단일 label 아님 |
| 시간상수 τ 분석 | gate의 시간척도·chrono 초기화 |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 시퀀스 학습오차 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 시간척도와 gating은 이미 이론적 선행 |
| 주요 한계·우리 연구와 차이 | LTC effective τ 수치/단위와 동일 아님 |
| 근거 위치/확인 범위 | time-warp theory·chrono initialization |

## L13 — Kapoor & Narayanan (2023)

원천: [L13](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856/). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | ML 과학·내전예측 사례 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | 복잡 ML 및 logistic 등 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | 시간순 누출 위험 논의 |
| 클래스/퇴화 진단 | label 퇴화 연구 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 재현성과 성능 과장 사례 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 누출 taxonomy·model info sheets |
| 주요 한계·우리 연구와 차이 | 누출 방지 절차 존재가 현재 PIT 인증은 아님 |
| 근거 위치/확인 범위 | taxonomy·civil-war reproduction·limitations |

## L14 — Chen & He (2021)

원천: [L14](https://openaccess.thecvf.com/content/CVPR2021/html/Chen_Exploring_Simple_Siamese_Representation_Learning_CVPR_2021_paper.html). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지 자기지도 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | SimSiam/ResNet |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 상수 표현 해·stop-gradient 효과 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 표현 std·linear evaluation accuracy |
| 검정 방법 | ablation 비교; 현재 금융검정과 별개 |
| 실제 기여(이 검토의 요약) | representation collapse의 개념 선행 |
| 주요 한계·우리 연구와 차이 | 같은 predicted label만으로 표현 collapse 판정 불가 |
| 근거 위치/확인 범위 | §3~4,stop-gradient ablation |

## L15 — Bardes, Ponce & LeCun (2022)

원천: [L15](https://openreview.net/forum?id=iWpcWZ8phD). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지 자기지도 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | VICReg/ResNet |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 상수/비정보 embedding 방지 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 표현 variance/covariance·downstream accuracy |
| 검정 방법 | ablation; 현재 금융검정과 별개 |
| 실제 기여(이 검토의 요약) | variance/covariance 정규화로 표현 진단 |
| 주요 한계·우리 연구와 차이 | 금융 LTC의 hidden rank를 계측한 증거 아님 |
| 근거 위치/확인 범위 | §3~4 및 implementation/ablation |

## L16 — Buczyński (2026)

원천: [L16](https://www.mdpi.com/2073-4441/18/17/2169). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 덴마크 배수 수문(비금융) |
| 예측기간 | 10분 ahead |
| 사용 모델 | SB/DB 계층 LNN, LSTM/GRU/TCN/MLP |
| LTC/CfC 실제 구현 확인 | 직접 bounded τ를 둔 relaxation/exponential cell; ncps conductance와 동일 아님 |
| Seed 반복 | SB seed42/43/44; 다른 주결과42 |
| Walk-forward 평가 | 고정2010~17Train/2018Val/2019Test(원문 분할) |
| 클래스/퇴화 진단 | 펌프 구간 성능저하; 이진 label collapse 아님 |
| 시간상수 τ 분석 | fast-path τ·레짐별 내부 진단 |
| 레짐 분석 | 강우/펌프 레짐 분석 |
| 평가 지표 | NSE/RMSE/MAE 등 |
| 검정 방법 | 기술 비교; 별도 검정 상세 UNKNOWN |
| 실제 기여(이 검토의 요약) | τ·seed·레짐을 함께 진단한 직접 선행 |
| 주요 한계·우리 연구와 차이 | 회귀/셀·시간단위가 달라 τ 크기 직접 비교 불가 |
| 근거 위치/확인 범위 | §2.3~2.4,§3.5~3.6,AppendixB |

## L17 — Cerqueira, Torgo & Mozetič (2020)

원천: [L17](https://link.springer.com/article/10.1007/s10994-020-05910-7). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 174실측·3합성 시계열 |
| 예측기간 | 과제별; 금융20일 아님 |
| 사용 모델 | 여러 forecast learner/평가법 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | holdout 반복/prequential/blockedCV 비교 |
| 클래스/퇴화 진단 | 분류 퇴화 연구 아님 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | 정상성/비정상성 구분 |
| 평가 지표 | 성능추정 오차 |
| 검정 방법 | 실증 평가법 비교; 현재 검정 대체 아님 |
| 실제 기여(이 검토의 요약) | 시간 종속·비정상성에 평가법 선택 중요 |
| 주요 한계·우리 연구와 차이 | 특정방법의 모든 조건 타당성 보장 아님 |
| 근거 위치/확인 범위 | evaluation methods·empirical/synthetic studies |

## L18 — Goodfellow et al. (2014)

원천: [L18](https://papers.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지 생성 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | GAN |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 생성 분포 게임; 원 논문과 후속 mode-collapse 구분 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 생성 품질/likelihood 추정 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | adversarial generative modeling 원전 |
| 주요 한계·우리 연구와 차이 | binary 방향분류의 label 퇴화와 문제 자체 다름 |
| 근거 위치/확인 범위 | minimax objective·experiments |

## L19 — Gu, Kelly & Xiu (2020)

원천: [L19](https://www.nber.org/papers/w25398). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 미국 자산수익 |
| 예측기간 | 월별 수익 예측(공식 초록/기록) |
| 사용 모델 | NN/tree/linear ML |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | 출판사 색인에 복수seed averaging; 상세 UNKNOWN |
| Walk-forward 평가 | 공식 기록의 OOS; 세부 계약 UNKNOWN |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | OOS 예측·포트폴리오 성능 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 자산가격 ML·예측 변동 완화 선행 |
| 주요 한계·우리 연구와 차이 | 2020전문 심층 미포함; 투자 결과를 현재 방향 BA와 직접 비교 불가 |
| 근거 위치/확인 범위 | NBER/출판사 색인·초록 |

## L20 — Fischer & Krauss (2018)

원천: [L20](https://www.sciencedirect.com/science/article/pii/S0377221717310652). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | S&P500 구성주 |
| 예측기간 | 공개 초록상 방향/시장 예측; 정확 horizon 이번확인 UNKNOWN |
| 사용 모델 | LSTM 및 비교모형 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | OOS 실험 서술;세부 UNKNOWN |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 분류/전략평가의 세부 이번 UNKNOWN |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 대규모 금융 LSTM 선행 |
| 주요 한계·우리 연구와 차이 | 원문 심층 미포함; 신경망 적용/시간분할 자체의 신규성 근거 아님 |
| 근거 위치/확인 범위 | 출판사 초록·서지 |

## L21 — Krauss, Do & Huck (2017)

원천: [L21](https://www.sciencedirect.com/science/article/pii/S0377221716308657). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | S&P500 구성주 |
| 예측기간 | 정확 target 시점 이번 UNKNOWN |
| 사용 모델 | DNN/GBT/RF 및 ensemble |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | OOS 시장실험;세부 UNKNOWN |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 주로 전략 성과 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 여러 모형·앙상블 금융 비교 |
| 주요 한계·우리 연구와 차이 | 거래수익과 현재 BA의 직접 비교 불가 |
| 근거 위치/확인 범위 | 출판사 초록·서지 |

## L22 — He & Garcia (2009)

원천: [L22](https://dblp.org/rec/journals/tkde/HeG09.html). 확인 범위: **METADATA_ONLY**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 일반 불균형 학습 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | 복수 분류 방법 survey |
| LTC/CfC 실제 구현 확인 | UNKNOWN(서지 검토만) |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | UNKNOWN(확인 근거 부족) |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 불균형 학습이 확립된 선행 영역 |
| 주요 한계·우리 연구와 차이 | 전문 미검토; 정확 원인/처방을 인용해 적용하지 않음 |
| 근거 위치/확인 범위 | 서지 DB만 |

## L23 — Lechner, Hasani, Amini, Henzinger, Rus & Grosu (2020)

원천: [L23](https://www.nature.com/articles/s42256-020-00237-3). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 자율주행 제어 |
| 예측기간 | 제어 task |
| 사용 모델 | Neural Circuit Policies |
| LTC/CfC 실제 구현 확인 | 초록의 continuous-time sparse circuit; 실제 code별 UNKNOWN |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | 구체 τ 분석 이번 UNKNOWN |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 제어/감사 가능성 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 연속 신경회로 감사 가능성 선행 |
| 주요 한계·우리 연구와 차이 | 초록만 확인;금융 분류나 현재 τ 재현 증거 아님 |
| 근거 위치/확인 범위 | Nature 초록·서지 |

## L24 — G. Joshita Reddy, Rahul Kumar Sahani & S. P. Raja (2025)

원천: [L24](https://dblp.org/rec/journals/tcss/ReddySR25.html). 확인 범위: **METADATA_ONLY**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | UNKNOWN(확인 근거 부족) |
| 예측기간 | UNKNOWN(확인 근거 부족) |
| 사용 모델 | 제목상 Boruta+LNN |
| LTC/CfC 실제 구현 확인 | UNKNOWN(LNN 명칭만으로 LTC/CfC 확정 불가) |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | UNKNOWN(확인 근거 부족) |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 금융 LNN hybrid 선행 후보 |
| 주요 한계·우리 연구와 차이 | 전문·공식 초록 세부 미확보;내용 부재 판단 금지 |
| 근거 위치/확인 범위 | DBLP 저자/DOI/권호 |

## L25 — Jammal, Srour, Salman, Owayjan, Ayoub, Rottondi & Achkar (2025)

원천: [L25](https://iris.polito.it/handle/11583/3001333). 확인 범위: **INDEXED_ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | Tesla/Apple(기관 색인 초록) |
| 예측기간 | UNKNOWN |
| 사용 모델 | LNN 대 incremental learning |
| LTC/CfC 실제 구현 확인 | UNKNOWN(최종 cell 미확인) |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | UNKNOWN(확인 근거 부족) |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 개별주 LNN 비교 선행 |
| 주요 한계·우리 연구와 차이 | 원 landing/PDF403;색인을 전문으로 취급하지 않음 |
| 근거 위치/확인 범위 | 기관 색인 초록·서지 |

## L26 — Ozbayoglu, Gudelek & Sezer (2020)

원천: [L26](https://www.sciencedirect.com/science/article/pii/S1568494620303240). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 복수 금융응용 survey |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | deep learning 전반 |
| LTC/CfC 실제 구현 확인 | 특정 LTC/CfC 이번 UNKNOWN |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | UNKNOWN(확인 근거 부족) |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 금융DL응용의 폭넓은 선행 |
| 주요 한계·우리 연구와 차이 | 초록 검토만;모든 포함논문을 읽었다고 세지 않음 |
| 근거 위치/확인 범위 | 출판사 초록·서지 |

## L27 — Bailey, Borwein, López de Prado & Zhu (2017)

원천: [L27](https://escholarship.org/uc/item/4w1110bb). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 금융 backtest |
| 예측기간 | 전략 설정별 |
| 사용 모델 | CSCV/선택위험 분석 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | 선택·OOS 분할;정확세부 UNKNOWN |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 과적합 확률 |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 전략 탐색/선택의 위험 선행 |
| 주요 한계·우리 연구와 차이 | 현재 METHOD_NOT_VALIDATED를 이 논문으로 해결하지 않음 |
| 근거 위치/확인 범위 | 기관/출판사 서지·초록 |

## L28 — 김태민·안현철 (2025)

원천: [L28](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003249779). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 니켈 가격 |
| 예측기간 | 초록상1~10개월 시차 탐색;예측 horizon UNKNOWN |
| 사용 모델 | LNN, RNN/GRU/LSTM/RF/OLS |
| LTC/CfC 실제 구현 확인 | UNKNOWN(초록 LNN;실제 cell 미확인) |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | 정확도 비교;상세 metric UNKNOWN |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 국내 원자재 LNN 예측 선행 |
| 주요 한계·우리 연구와 차이 | 초록의 인과 해석을 현재 인과 근거로 차용하지 않음 |
| 근거 위치/확인 범위 | KCI 초록·서지 |

## L29 — Lim, Arık, Loeff & Pfister (2021)

원천: [L29](https://arxiv.org/abs/1912.09363). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 다양한 실측 시계열 |
| 예측기간 | multi-horizon |
| 사용 모델 | TFT |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | 해석성·regime 표현;명시적 HMM여부 UNKNOWN |
| 평가 지표 | 예측/해석성;세부 UNKNOWN |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 다중지평·시간 해석성 선행 |
| 주요 한계·우리 연구와 차이 | 이번에는 arXiv 초록·서지만 |
| 근거 위치/확인 범위 | arXiv 초록 및 학술지 서지 |

## L30 — Sezer, Gudelek & Ozbayoglu (2020)

원천: [L30](https://aperta.ulakbim.gov.tr/records/7737). 확인 범위: **ABSTRACT_METADATA**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 금융 시계열 survey2005~2019 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | deep learning 전반 |
| LTC/CfC 실제 구현 확인 | 이번 검토에서 UNKNOWN |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | UNKNOWN(확인 근거 부족) |
| 클래스/퇴화 진단 | UNKNOWN(확인 근거 부족) |
| 시간상수 τ 분석 | UNKNOWN(확인 근거 부족) |
| 레짐 분석 | UNKNOWN(확인 근거 부족) |
| 평가 지표 | UNKNOWN(확인 근거 부족) |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 금융 예측 연구의 기존 폭·범주 |
| 주요 한계·우리 연구와 차이 | survey 서지/초록만;포함연구 전수검토 아님 |
| 근거 위치/확인 범위 | 기관/출판사 서지·초록 |

## L31 — Saito & Rehmsmeier (2015)

원천: [L31](https://pmc.ncbi.nlm.nih.gov/articles/PMC4349800/). 확인 범위: **FULLTEXT_AVAILABLE_ABSTRACT_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 일반/생물정보 불균형 분류 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | 분류기 평가 |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 희소 클래스 평가의 metric 문제 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | PR/ROC |
| 검정 방법 | UNKNOWN(확인 근거 부족) |
| 실제 기여(이 검토의 요약) | 불균형에서 지표 해석 주의 |
| 주요 한계·우리 연구와 차이 | 이번 심층18수에 미포함;BA우월성 정리로 차용 금지 |
| 근거 위치/확인 범위 | PMC 초록/도입 |

## L32 — Fang, He, Long & Su (2021)

원천: [L32](https://arxiv.org/abs/2101.12699). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 불균형 supervised benchmark |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | layer-peeled surrogate·deep classifier |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | minority classifier geometry collapse |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 각도·분류오류·기하학 |
| 검정 방법 | 이론/계산실험;현재 금융검정과 별개 |
| 실제 기여(이 검토의 요약) | 소수클래스 붕괴의 직접 선행 개념 |
| 주요 한계·우리 연구와 차이 | 전체Test한label과 동등 정의 아님;현재원인설명 불가 |
| 근거 위치/확인 범위 | balanced/imbalanced theory·minority experiments |

## L33 — Salimans, Goodfellow, Zaremba, Cheung, Radford & Chen (2016)

원천: [L33](https://proceedings.neurips.cc/paper/2016/hash/8a3363abe792db2d8761d6403605aeb7-Abstract.html). 확인 범위: **FULLTEXT_SECTION_REVIEW**. 서지의 정확 제목/학술지는 해당 ID 행 참조.

| 비교 항목 | 확인 내용 |
| --- | --- |
| 연구대상 시장/영역 | 이미지 생성/준지도 분류 |
| 예측기간 | N/A(금융 방향예측 연구 아님) |
| 사용 모델 | GAN training variants |
| LTC/CfC 실제 구현 확인 | LTC/CfC 아님 |
| Seed 반복 | UNKNOWN(확인 근거 부족) |
| Walk-forward 평가 | N/A(금융 방향예측 연구 아님) |
| 클래스/퇴화 진단 | 생성기가 한 point/mode로 모이는 문제 |
| 시간상수 τ 분석 | N/A(금융 방향예측 연구 아님) |
| 레짐 분석 | N/A(금융 방향예측 연구 아님) |
| 평가 지표 | 생성 품질·분류오류 |
| 검정 방법 | 실험비교;현재금융검정과 별개 |
| 실제 기여(이 검토의 요약) | mode-collapse와 minibatch discrimination 선행 |
| 주요 한계·우리 연구와 차이 | 분류label·representation collapse와 구분 |
| 근거 위치/확인 범위 | §3.2 및 실험 |
## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
