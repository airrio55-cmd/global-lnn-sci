# STEP13 금융 LTC·CfC 선행과 직접 비교의 한계

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 가장 가까운 선행과 확인 수준

| ID | 이번 확인 사실 | 현재 연구와 구분 | 남은 공백 |
| --- | --- | --- | --- |
| [L03](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003273926) | KOSPI 이진방향·LTC 적용을 이미 보고 | 전체 KOSPI/7일·다변수와 현재 KOSPI200/20session·F1은 다름 | 본문·최종 cell·Seed·walk-forward·퇴화/τ 진단 UNKNOWN |
| [L04](https://link.springer.com/article/10.1007/s41870-023-01506-1) | NSE 개별주·LTC/양방향 재귀 비교 | 개별주 가격/추세와 현재 지수 이진방향 진단 구별 | 전문 구독; 정확 horizon·출력·진단 UNKNOWN |
| [L24](https://dblp.org/rec/journals/tcss/ReddySR25.html) | Boruta+LNN 금융 논문의 서지 확인 | hybrid feature/model 제안과 고정 F1 진단은 목적 다름 | 실제 LTC/CfC·평가설계 미확인 |
| [L25](https://iris.polito.it/handle/11583/3001333) | 기관 색인에 Tesla/Apple LNN 대 incremental 비교 | 동일 시장·같은 셀이라고 간주 불가 | landing/PDF403, 최종 cell 미확인 |
| [L28](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003249779) | 국내 원자재 LNN 비교 연구 | 니켈 회귀/시차분석은 KOSPI200 방향 진단과 다름 | 초록 LNN을 LTC/CfC로 확정하지 않음 |
| [L19](https://www.nber.org/papers/w25398), [L20](https://www.sciencedirect.com/science/article/pii/S0377221717310652), [L21](https://www.sciencedirect.com/science/article/pii/S0377221716308657) | 금융 ML/재귀모형·OOS 비교의 폭넓은 선행 | 예측 단위·시장·정보·수익/분류지표가 다름 | 원 성과와 현재 BA를 차감해 우열 판정 불가 |

L03은 저자 고영보·안현철, 국민대학교 소속으로 확인된다. 지도교수와 가까운 출판물이라는 사실과 현재 학위논문의 같은 연구/데이터라는 추정은 구분한다. 학위논문의 선행 출판분·추가 실증분과 원고/코드 version 관계를 저자에게 확인하고 인용해야 한다. 이를 독립된 외부 재현으로 계수하지 않는다. 현재 제공 DOCX와 그 학술지 원문이 같은 문서라는 증거도 없다.

## 금융에서 안정성 분석이 없었다는 주장에 대한 반례

[L06](https://link.springer.com/article/10.1007/s41060-024-00690-y)는 금융 방향 분류에서 반복Seed와 불리한 시기 변화, 상수예측 평가 문제를 이미 논의한다. [L08](https://www.bankofengland.co.uk/working-paper/2022/an-interpretable-machine-learning-workflow-with-an-application-to-economic-forecasting)은 경제예측에서10seed의 예측 변동과 성능–안정성 tradeoff를 다룬다. 따라서 ‘금융에서 Seed/시간별 안정성을 처음 고려’라는 표현은 사용할 수 없다. 현재의 추가분은 **고정5NN·A/B·5Origin·10Seed의 단일예측 진단과 LTC 내부 계측을 연결한 제한된 실증 구성**이다.

## CfC 검색의 해석

원전 L02는 LTC와 CfC를 연결하지만 동일 셀이라고 하지 않는다. 검색에 나온 CfC 금융사기 분류나 비금융 연속시간 연구를 주가지수 방향성 실증으로 섞지 않았다. 금융 CfC 논문이 전혀 없다는 결론도 내리지 않는다. 새로운 금융 LNN 제목만으로 최종 구현을 판단할 수 없고, 현재 제공 코드의 LTC 정체성은 STEP10C 근거를 따른다.

## 퇴화·τ의 직접 선행에 관한 판정

검토한 금융 원문/공개 초록에서 **현재와 동일한20session F1 분류·전체 Test 단일 label·모델별 반복 진단·conductance effective τ와의 연관**을 확인하지 못했다. 그러나 가장 가까운 L03/L04/L24/L25의 전문이 없으므로 동일 진단의 부재는 **UNKNOWN**이다. 이 공백은 잠재 차별성의 범위를 좁히는 자료이지 최초성 인증이 아니다. 원문이 확보되면 동일 definition·최종 cell·반복 단위·시간상수 요약을 다시 대조할 수 있으나 금융 실행을 새로 할 필요는 없다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
