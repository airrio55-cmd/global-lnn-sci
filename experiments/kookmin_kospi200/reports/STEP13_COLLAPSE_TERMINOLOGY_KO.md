# STEP13 단일클래스 예측과 collapse 개념의 구분

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 현재 연구의 관측 정의

LTC24/100은 **동결 checkpoint가 전체 해당 Test 구간에서 하나의 클래스만 예측한 결과**다. 확률 threshold는 기존 `p > 0.5`다.100은5Origin×A/B×10Seed의 fit identity이며 독립 시장100회가 아니다. LSTM2/100, RNN/GRU/CfC 각0/100을 같은 정의로 보고한다. 이번에는 확률 배열·hidden activation·gradient를 새로 읽거나 계산하지 않았다.

| 개념 | 정의·필요 증거 | 현재24/100과의 관계 | 선행 근거 |
| --- | --- | --- | --- |
| 전체 Test 단일클래스 예측 | 모든 결정 label이0 또는1; 구간·threshold 명시 | 현재 직접 확인된 관측 정의 | STEP5B/STEP12의 저장 진단 |
| 다수클래스 편향 | 다수 집단으로 오분류/예측이 치우침; 실제 support 비교 필요 | 가능한 관련 현상이나 단일예측이 반드시 다수클래스라는 뜻은 아님 | L22, L31 및 L06 metric 논의 |
| 최적화 실패·수치 발산 | NaN/Inf·비정상 loss/gradient·업데이트 기록 등 | 단일 label만으로 원인 판정 불가; 유한 수치에서도 발생 가능 | [L11](https://proceedings.mlr.press/v28/pascanu13.html) |
| 예측 확률 포화 | 확률이0/1에 극단적으로 몰림 | label 한 종류가 포화를 뜻하지 않음;0.5 한쪽의 가변 확률도 가능 | 일반 확률분류의 정의; 현재 새 진단 없음 |
| Neural Collapse | terminal training의 class-wise feature·classifier geometry NC1~4 | 모든 입력을 한 label로 예측한다는 뜻이 아님 | [L05](https://pmc.ncbi.nlm.nih.gov/articles/PMC7547234/) |
| GAN Mode Collapse | 생성기가 다양한 target mode를 덜 생성/한 mode에 집중 | 생성분포의 문제; supervised 방향 label과 별개 | [L18](https://papers.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html), [L33](https://proceedings.neurips.cc/paper/2016/hash/8a3363abe792db2d8761d6403605aeb7-Abstract.html) |
| Constant predictor | 출력 함수를 상수로 두는 예측기; label/확률 차원 명시 | constant label과 constant probability는 다름 | L06의 trivial classifier 논의; 현재Climatology 비교 |
| Representation collapse | 입력이 달라도 embedding이 같거나 정보/차원이 소실 | label만으로 hidden representation 붕괴를 알 수 없음 | [L14](https://arxiv.org/abs/2011.10566), [L15](https://arxiv.org/abs/2105.04906) |

추가로 [L32](https://arxiv.org/abs/2101.12699)의 **Minority Collapse**는 불균형 조건에서 소수클래스 분류기 기하가 수렴하는 이론/실증 현상이다. 현재의 이진 Test 한 label과 같은 판정 기준이 아니며 원인 설명을 자동 제공하지 않는다. 일반적인 클래스 불균형과 퇴화 문제가 선행됐다는 점은 인정한다.

## 권장 용어와 표현

본문은 처음에 “전체 Test 구간 단일클래스 예측(이하 본 연구의 관측적 예측 퇴화)”로 정의한다. 그 뒤에도 Neural Collapse·mode collapse·representation collapse의 동의어로 사용하지 않는다. ‘LTC24개가 발산했다’ 대신 ‘24개가 해당 전체 Test에서 한 클래스로 예측됐다’고 쓴다. 일부 epoch의 현상과 선택된 checkpoint의 전체 Test 현상도 구별한다.

τ와 label 퇴화의 관계는 관측적 탐색연관이며 embedding rank 감소·확률 포화·gradient 원인을 확인한 것이 아니다. 새로운 원인 진단이나 이를 막는 처방을 이번 문헌검토로 실행하지 않는다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
