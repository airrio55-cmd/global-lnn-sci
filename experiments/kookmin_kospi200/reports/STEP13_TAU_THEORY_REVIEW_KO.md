# STEP13 시간상수 이론과 구현·단위의 비교

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 원전에서 확립된 부분

[L01](https://ojs.aaai.org/index.php/AAAI/article/view/16936)의 Eq1은 LTC를 입력·상태에 따라 감쇠율이 달라지는 연속시간 재귀계로 정의하며 유효 시간상수의 개념과 유계성 분석을 이미 제시한다. [L12](https://arxiv.org/abs/1804.11188)의 gating/시간변환·chrono 초기화도 시간척도 해석의 선행이다. 따라서 ‘입력 의존 τ’나 ‘시간상수를 추출했다’는 일반 개념을 새 방법으로 주장하지 않는다.

## 현재 ncps conductance 진단의 의미

기존 STEP7A/7B/7BR의 정의를 인용하면 leak-only 원시량은 `τ_raw = cm / gleak`, 국소 유효량은 `τ_eff = cm / (gleak + Σ recurrent_conductance + Σ sensory_conductance)`다. 실제 값은 양의 제약·입력과 hidden state·solver 평가 위치에 의존하며, 이번에 파라미터/forward/τ를 새로 계산하지 않았다.

이 정의는 입력/상태를 국소적으로 고정했을 때의 감쇠 시간척도다. 모든 recurrent gate의 상태 미분까지 포함한 전체 시스템 Jacobian의 고유시간이나 예측 horizon과 동일하지 않다. `τ_raw`가 모델의 유일한 고정 기억길이인 것도 아니다. observation-entry와 solver substep에서 평가한 τ를 구별하고 동일 checkpoint의 뉴런/window/substep을 독립 표본으로 늘리지 않는다.

`dt=1`은 기존 모델에서 관측 step의 정규화된 시간이다. 거래일 표본 간 주말/휴장 간격이나 실제 wall-clock day를 모두 동일하게 물리화한 인증이 아니다.20session forecast horizon과 τ를 동일 척도라고 놓을 수 없으며 ‘며칠의 경제적 기억’으로 직역하지 않는다. 유한·유계 상태라는 성질도 balanced class prediction·좋은 optimizer 결과·금융 일반화를 보장하지 않는다.

## 가까운 내부 동역학 실증과 차이

[L16](https://www.mdpi.com/2073-4441/18/17/2169)의 §3.5/3.6은 적응 시간상수·Seed·강우/펌프 레짐을 분석한다. 이 때문에 ‘τ와 모형 행동의 연결을 처음 분석했다’는 넓은 주장은 지원되지 않는다. 그 연구의 hierarchical fast/slow relaxation cell과 단위 설정은 현재 ncps conductance cell과 다르다. 이론적 계열 유사성이 τ 숫자의 직접 비교나 동일 물리단위를 뜻하지 않는다. AppendixB의 구현–원전 연결도 별도로 읽어야 한다.

[L02](https://www.nature.com/articles/s42256-022-00556-7)는 LTC 유도에서 근사 폐쇄형 CfC를 제시한다. 현재 LTC wrapper를 CfC라 부르거나 CfC의 explicit-time gate를 ncps LTC의 conductance τ와 같은 값으로 대입해서는 안 된다. MIT 기관 PDF로 관련 절을 확인했으며 현행 correction 전문까지 검증했다고 쓰지 않는다.

## 현재 관측이 더하는 좁은 질문

현재100개 LTC에서 퇴화24/비퇴화76, 공존8셀 모두의 낮은 effective τ 방향이라는 저장된 결과를 이진 출력행동의 진단과 연결하는 것이다. 서로 다른 Origin·가격·Seed 구성, O5 퇴화군 부재와 사후 탐색이 남아 **인과·구성독립·경제적 기억** 해석은 불가하다. 실제 동일 금융 조합의 선행 부재도 핵심 구독 원문 확보 전에는 미확인이다. τ100 신규평균·정량분할은 단일 복구값 역산 방지를 위해 공개하지 않는다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
