# STEP13 교수 검토용 문헌 비교 요약

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 교수님께 제안드리는 판단

STEP12의 최신 F1 진단 방향을 유지하되, 세 기여의 ‘새 방법/최초 적용’ 표현을 좁힐 필요가 있습니다.33개 후보를 확인하고18편의 전문 관련 절을 비교했습니다. KOSPI/금융 LTC 적용은 이미 존재하고, 금융·경제예측에서 Seed 변동과 평균–안정성을 나눈 연구도 있습니다. 적응 시간상수와 행동·레짐을 연결한 비금융 연구도 확인됐습니다. 따라서 기존 방법을 활용한 **조건부 실증 진단과 좁은 내부량–출력행동 연관**이 가장 방어 가능한 범위입니다.

## 가까운 근거와 공백

- [L03 KOSPI 선행](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003273926)은 고영보·안현철2025로 등재돼 있습니다. 현재 학위논문과의 출판/실험 중첩 관계는 원문과 저자 확인이 필요합니다. 최신 F1을 단순 첫 적용으로 제시할 수 없습니다.
- [L04 금융 LTC](https://link.springer.com/article/10.1007/s41870-023-01506-1)는 주가·양방향 구조를 다룹니다. L03/L04 전문이 없으므로 같은 퇴화·τ 진단이 없다고 확정하지 않았습니다.
- [L06 금융Seed 분석](https://link.springer.com/article/10.1007/s41060-024-00690-y), [L07 성능분포 연구](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328564/), [L08 경제예측 workflow](https://www.bankofengland.co.uk/working-paper/2022/an-interpretable-machine-learning-workflow-with-an-application-to-economic-forecasting)은 기여1의 선행입니다.
- [L16 내부 τ/레짐 연구](https://www.mdpi.com/2073-4441/18/17/2169)는 내부 시간상수 해석 자체의 신규성을 제한합니다. 셀·출력과 단위가 달라 현재 ncps τ 숫자와 직접 비교하지 않습니다.

## 기여 등급 제안

평균–안정성 분리는 **INCREMENTAL_EXTENSION**입니다. 모델별 단일예측 진단은 **DISTINCTIVE_EMPIRICAL_COMBINATION**으로 제한해 제안합니다. effective τ 연관은 **POTENTIAL_NOVEL_FINDING** 후보이나 최종 우선성은 **INSUFFICIENT_EVIDENCE**입니다. 우리 LTC24/100은 Neural Collapse·GAN mode collapse와 같은 정의가 아닙니다. 성능 순위로 독창성을 판정하지 않았습니다.

## 논문 주장과 교수 검토사항

“고정 F1 회고적 사양에서 평균 성능과 안정성을 분리하고, 일부 LTC의 전체 Test 단일클래스 예측과 effective τ의 탐색적 연관을 진단했다”는 문장을 우선 제안합니다. 특정 조건의 결과이며 일반 LTC 결함·인과·실시간 투자가 아닙니다. 출처/PIT·METHOD_NOT_VALIDATED·baseline NOT_TESTED는 그대로입니다.

교수님께 (1) 이 실증 구성과 잠재 연관이 학위 수준 기여로 충분한지, (2) L03 선행 출판분과 추가분을 어떻게 구분할지, (3) 핵심 구독 원문 확보와 추가 문헌 확장의 우선순위, (4) 제목에 ‘회고적/탐색적’을 명시할지를 검토 요청드립니다. 이는 발송되지 않은 검토자료이며 교수 승인 전입니다. 신규 금융 실행 없이 문헌·모델 정체성·논증을 먼저 보완할 수 있습니다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
