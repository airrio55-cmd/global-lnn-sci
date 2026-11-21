# STEP13 문헌 검색 프로토콜·실제 접근 범위

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 질문과 검색 설계

세 기여 후보가 새 방법인지, 기존 방법의 실증 확장인지, 관측 결과의 잠재적 새 조합인지 비교한다. 원전부터2026-11-21까지를 검색 상한으로 두고,2024~2026 금융 LTC/CfC·Seed/시간 구간 안정성·시간상수/퇴화 논문을 우선 찾았다. 날짜는 게시/권호/프리프린트 연도를 구분하고 검색엔진의 상대 날짜를 출판일로 사용하지 않았다.

이번 검색은 **구조화된 범위 문헌검토**다. 모든 DB의 전수검색·이중 독립 screening·PRISMA systematic review를 수행한 것으로 표시하지 않는다. 논문 최초성·독창성의 완전한 인증이 목적 달성으로 자동 보장되지 않는다.

## 실제 사용 경로와 검색식

공개 웹 검색을 통해 DOI/AAAI, Nature·Springer, arXiv, MLSys/PMLR/NeurIPS/CVPR, PMC/PubMed, KCI/KISS/DBpia/RISS 검색 결과, 대학 저장소·Bank of England·NBER를 확인했다. Crossref API는 별도로 DOI 서지 대조에 사용했다. Google Scholar·Semantic Scholar·OpenAlex의 전체 색인 API를 모두 조회한 것은 아니다. IEEE는 일부 직접 접근418, 구독 문헌은 초록/서지에 그쳤다.

실제 사용한 검색식 묶음은 다음과 같다. 유사 검색결과의 중복 URL·동일 DOI는 한 후보로 합쳤다.

| 범위 | 실제 검색식 예 |
| --- | --- |
| 원전 | “Liquid Time-Constant Networks” Hasani2021; “Closed-form continuous-time neural networks” Hasani2022 |
| 국내 선행 | “ART003273926”; “액체 시간상수” “예측” 고영보; “액체 신경망을 활용한 니켈 원자재 가격 예측” |
| 금융 LTC | “LiquidT” “Stock Market”; “Liquid” “time-constant” “stock”2024 2025 2026; “liquid neural” “stock”2024 2025 IEEE |
| CfC 금융 | “closed-form continuous-time” stock prediction finance2024 2025 2026; “closed-form continuous-time” “financial” “2025” |
| 퇴화 | “liquid time-constant” “collapse”; “liquid” “single-class” prediction neural network; “LTC” “single class” classifier finance; “degenerate binary classifier” neural network finance |
| τ/개념 | “effective time constant” “collapse” neural network; “Prevalence of neural collapse”; “Minority collapse in imbalanced training” |
| 안정성 | neural network random seed variance financial forecasting; “Accounting for Variance in Machine Learning Benchmarks”; “Can recurrent neural networks warp time”; “On the difficulty of training recurrent neural networks” |
| 평가·누출 | “Leakage and the reproducibility crisis”; “Evaluating time series forecasting models”; “The probability of backtest overfitting” |
| 한국어 보완 | 신경망 주가 예측 시드 안정성 단일 클래스 퇴화 시간상수 |

특정 LTC/KOSPI/τ 관련 검색과 원전의 참고문헌을 이용한 후방 확장으로33개 서로 다른 논문을 비교 후보로 등록했다. 동일 연구의 arXiv·권호·온라인 선공개를 별도 논문으로 부풀리지 않았다. 예: L04 online2023/권호2024, L06 online2024/권호2025, L19 NBER2018/학술지2020이다. 이름에 LNN이 있다는 이유로 실제 셀을 LTC/CfC로 확정하지 않았다.

## 포함·제외 및 판독 수준

포함: 직접적인 LTC/CfC 이론/금융 적용, 반복학습/예측 안정성, 시간상수 해석, 분류·표현·생성 퇴화 개념, 금융/시계열 평가와 누출이다. 제외: 블로그·광고·코드 저장소만 있는 성능 주장, 금융기관 약어 CFC, 유동성 liquid의 단순 동음이의 결과, 특허를 동료평가 논문처럼 세는 경우다.

- 후보 **33편**: 신뢰할 서지/DOI/URL 수준 확인. 이 중 전문 관련 절 심층 비교 **18편**.
- 나머지 **15편**은 초록/서지 또는 전문 접근만 가능한 제한 검토다. 전문 전체를 읽었다고 세지 않는다.
- 심층18편에는 비금융 이론·평가·용어 원전도 포함된다. 금융 LTC 전문18편이라는 뜻이 아니다. 금융 핵심 L03/L04/L24/L25의 구현·Seed·τ/퇴화 세부는 여전히 공백이다.
- 18편 전문 원문을 로컬로 확보하고 관련 방법·실험·결론을 선별 판독했다. ‘관련 절 심층 비교’는 모든 문장·부록·소스 코드의 재현 검증이 아니다.

Crossref DOI 조회26건 중13건은 응답을 확보했고 나머지13건은 접근 실패였다. DOI 없는7편은 공식 URL을 사용했다. 실패 DOI는 공식 출판사/기관·KCI·신뢰 서지 경로로 보완했으며 실패를 성공으로 처리하지 않았다. 원 응답과 접근 로그는 비공개 로컬에 보존했다.

## 주요 접근 제한과 대안

| 자료 | 실제 접근 | 판정·대안 |
| --- | --- | --- |
| L03 KCI KOSPI | KCI 서지·초록 확인, DOI 직접 접근 실패 | ABSTRACT_METADATA; 원문은 저자/기관 접근 필요 |
| L04 Liquidt | Springer 구독 preview, Monash 서지·초록 | ABSTRACT_METADATA; 원문 없이 Seed/τ 부재 단정 금지 |
| L02 CfC | Nature 리다이렉트 오류 | MIT 연구기관의 같은 DOI PDF로 전문 확보 |
| L12/L15 OpenReview | 브라우저 challenge | 저자 arXiv PDF로 관련 절 검토 |
| L25 Jammal | 기관 landing/PDF403 | 기관 검색 색인과 DOI 기록만 확인; 전문 미확보 |
| L19 Gu | OUP 리다이렉트 오류 | 공식 NBER/출판사 색인으로 서지·초록; 전문 심층 수에 미포함 |
| L24 Boruta-LNN | DBLP DOI·저자·권호 확인 | METADATA_ONLY; 세부 방법 UNKNOWN |
| CVPR2026 LTC–Hopfield 검색 후보 | PDF403 | 추가 탐색 단서로만 보존; 검증33개/심층18개에 미포함 |

최근2024~2026 연구8편을 포함했으나 모든 최신 금융 LTC 문헌의 포괄성을 보장하지 않는다. KCI·Liquidt 등의 원문 확인 전에는 동일 퇴화/τ 조합이 보고되지 않았다고 확정할 수 없다. 따라서 좁은 실증 차별성은 제안할 수 있어도 ‘최초 발견’ 판정은 보류한다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
