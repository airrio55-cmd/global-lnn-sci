# STEP13 독창성 검토의 최종 답과 권고

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 열 가지 질문에 대한 답

| 질문 | 현재 답 | 근거 수준·남은 한계 |
| --- | --- | --- |
| 1. KOSPI LTC 적용만으로 독창성이 있는가? | 그 사실만으로는 부족하다. L03에 직접 선행이 있다. | KOSPI와KOSPI200/지평 차이는 있지만 최초 적용 근거가 되지 않음 |
| 2. 단일클래스 퇴화는 얼마나 다뤄졌는가? | 일반 상수예측·불균형·collapse 개념은 선행이 풍부하다. 현재와 같은 금융 LTC 진단은 검토 범위에서 확인 못했다. | 핵심 금융 전문 미확보여서 부재/최초성은 UNKNOWN |
| 3. τ 연관의 차이는? | 시간상수 이론·행동 해석은 선행됐고, 현재 추가분은 ncps LTC 이진 label 퇴화와 model-level 연관의 특정 조합이다. | 다른 cell·단위와 수치 직접 비교 불가;인과·구성독립 미식별 |
| 4. 가장 차별적인 관측은? | 같은 관측 정의의 모델별 단일예측 패턴과 τ100/공존8셀 방향을 연결한 제한된 실증 진단 |24/100이 보편적 결함률이나8독립 발견은 아님 |
| 5. 중복 요소는? | 금융 LTC 적용, 재귀모형 비교, Seed/시간분할 평가, τ 이론·추출·레짐 진단, 퇴화 개념 | 실행500회 자체나10Seed×5Origin은 새 방법 아님 |
| 6. 가장 방어 가능한 기여는? | 기존 방법을 사용해 평균·출력 안정성·LTC 내부량을 반대 증거와 함께 연결한 회고적 실증 구성 | 학위 충분성·문헌 대비 추가가치의 교수 판단 필요 |
| 7. 주장 불가능한 것은? | 최초 KOSPI 적용/최초 퇴화/보편 LTC 결함/τ인과/통계 우월/실시간 수익성 | 원천·PIT·방법 미검증 상태 유지 |
| 8. 핵심 공백·기여 문장은? | 고정 F1 금융분류에서 전체 Test 단일 label과 내부 effective τ를 함께 진단한 제한된 사례 | 검색·접근 범위 한정;최초성 확정 아님 |
| 9. 무실험 개선은? | 가까운 금융 전문 확보, 선행 출판분과 추가분 구분, collapse 용어·τ 단위 정리, 주장 축소와 문헌 연결 | 추가 p값/좋은 결과를 만드는 금융실험 불필요 |
| 10. 심사에서 가장 치명적인 문제는? | 출처·구현·추론을 미확인인데 확인됐다고 주장하는 증거–결론 불일치 | 데이터 정체성/이용권한은 핵심 근거의 전제, 통계 우월성은 현재 미지원;독창성도 넓은 최초성 주장을 철회해야 함 |

## 최종 기여 판정

기여1 **B INCREMENTAL_EXTENSION**. 기여2 **C DISTINCTIVE_EMPIRICAL_COMBINATION**(제한부). 기여3 **D POTENTIAL_NOVEL_FINDING**(조건부), 최종 최초성은 **E INSUFFICIENT_EVIDENCE**다. 일반 안정성/τ 개념은 **A PRIOR_ART_ESTABLISHED**다. 교수 승인이나 논문 독창성의 완전한 인증으로 바꾸지 않는다.

[핵심 주장 수정안](STEP13_DISSERTATION_CONTRIBUTION_REVISION_KO.md)은 “고정 F1 회고적 사양에서 평균 성능과 안정성을 구분하고, 일부 LTC의 전체 Test 단일클래스 예측과 effective τ 차이의 탐색적 연관을 제시한다”는 범위다. 모델 성능 순위로 독창성을 판단하지 않았으며 원형 RAW5/LOG2 Ensemble의 추가효과를 검증했다고 주장하지 않는다.

33후보/18전문 관련 절 비교라는 목표는 충족했지만 가장 가까운 금융 원문 공백은 해소되지 않았다. [교수 검토 요약](STEP13_SUPERVISOR_BRIEF_KO.md)과 [서지/접근 범위](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md)를 함께 제시한다. 출처/PIT와 METHOD_NOT_VALIDATED를 문헌으로 PASS로 바꾸지 않았고 새 금융실험을 시작하지 않았다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
