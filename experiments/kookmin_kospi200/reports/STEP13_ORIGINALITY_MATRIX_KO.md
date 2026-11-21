# STEP13 세 기여 후보의 독창성 판정

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 판정은 주장의 크기에 따라 달라진다

A PRIOR_ART_ESTABLISHED=일반 개념/방법의 선행 확립. B INCREMENTAL_EXTENSION=기존 접근의 범위 확장. C DISTINCTIVE_EMPIRICAL_COMBINATION=현재 자료/조건에서 진단을 결합한 실증 구성. D POTENTIAL_NOVEL_FINDING=더 좁은 관측 연관의 잠재적 새 발견이나 우선성 미인증. E INSUFFICIENT_EVIDENCE=문헌 접근/원인 식별 등의 근거가 부족함이다. 이들은 점수 서열이나 학위 요건 통과 등급이 아니다.

| 기여 후보 | 이번 주 판정 | 가장 가까운 선행 | 중복되는 부분 | 추가하는 지식·차별성 근거 | 반론과 허용 표현 |
| --- | --- | --- | --- | --- | --- |
| 1. 평균과 안정성 분리 | **B. INCREMENTAL_EXTENSION**; 일반 원칙은 A | L06/L08/L07, L09/L10/L17 | 금융·경제/시계열의 Seed 분산·시간 구간 평가가 이미 존재 | 고정5NN·A/B·5Origin·10Seed에서 평균과 단일예측을 함께 보존한 F1 사례 | 반복규모만 새 방법 아님. ‘기존 안정성 평가를 고정 사양 금융 분류에 체계적으로 적용’ |
| 2. LTC 단일클래스 진단 | **C. DISTINCTIVE_EMPIRICAL_COMBINATION**(제한부); 보편 현상의 신규성은 E | L03/L04 금융 LTC, L06 상수예측/Seed, L32 불균형 collapse | 금융 LTC 적용·상수예측 위험·클래스 퇴화 개념 모두 선행 | 동일 관측 정의에서 LTC24/LSTM2/다른3모델0, 불리한 실행을 보존한 조건별 진단 | 핵심 금융 전문 공백, 특정 사양 효과·baseline bias 가능. ‘동결 F1 사양에서 차별적인 단일예측 패턴을 관찰’ |
| 3. effective τ–퇴화 연관 | **D. POTENTIAL_NOVEL_FINDING**(조건부); 최종 우선성은 E | L01/L12 시간척도, L16 τ/Seed/레짐 진단, L03/L04 | 유효 τ 이론·모형 행동/레짐 해석은 이미 존재 | ncps LTC 이진출력 퇴화와 model-level 시간상수 방향을8개 공존 셀에서 연결 | 인과/구성독립 미식별·금융 핵심 전문 미확보. ‘제한된 조건에서 탐색적 연관을 제시’ |

각 선행의 정확한 출처는 [33편 비교](STEP13_PRIOR_ART_COMPARISON_KO.md)와 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md)의 동일 L번호로 연결한다. C/D는 ‘선행문헌에 없다’는 확정 판정이 아니다. 새 알고리즘·고유 τ 이론·최초 KOSPI 적용·보편 LTC 결함이라는 주장은 모두 지원되지 않는다.

## 독창성을 높이는 논증과 낮추는 위험

방어 가능한 추가 지식은 **평균으로 설명되지 않는 출력행동을 전수 보존하고, 특정 LTC 내부량과의 연관을 구성효과·실패 이력과 함께 보여준 사례**다. 성능순위나 유의 p값 개수로 독창성을 판정하지 않는다. 소스/평가/자료가 달라진 초기 결과와의 직접 성능차감도 근거가 아니다.

반론은 중요하다. 같은 사양이 특정 모델에 불리했을 가능성, class support·decision threshold·공통 F1 정보의 영향, 이웃한 Test/Seed/Origin 종속성, 현재 τ 요약이 새로운 메커니즘이 아닌 결과적 표지일 가능성이 남는다. 이를 제거했다고 쓰지 않는다. 원문 미확보 연구에서 같은 분석이 있을 가능성도 남으므로 D를 ‘novelty verified’로 바꾸지 않는다.

## 최종 판정까지 필요한 문헌 작업

L03/L04/L24/L25 원문과 코드의 실제 cell·평가·Seed·단일예측·τ 항목 확인, 선행 출판분/학위 추가분 연결, 다른 키워드/인용 네트워크 확장이 필요하다. 이 작업은 금융 재학습 없이 진행할 수 있다. 현재 제목·논문 충분성은 교수 검토 사항이며 세 기여 모두 승인됐다고 말하지 않는다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
