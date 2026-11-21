# STEP12 논문에서 허용되는 통계 표현

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

## 표현 수준

| 수준 | 사용할 문장 예시 | 근거·금지되는 확대 |
| --- | --- | --- |
| A. 기술적으로 관찰됨 | “동결100개 LTC 중24개에서 전체 Test 단일클래스 예측이 관찰됐다.” | 학습 identity의 기술량; 미래 고장률·독립100실험 아님 |
| B. 탐색적으로 연관됨 | “비교 가능한8개 Origin×가격 셀에서 퇴화군의 effective τ가 낮은 방향이었다.” | 구성·사후 탐색 한계. ‘τ가 퇴화를 유발’ 금지 |
| C. 제한된 근사 추론 | “기존 근사절차에서 Primary BA Holm 기각은 세 블록 모두0이었다.” | METHOD_NOT_VALIDATED 동반; 비유의=동등 금지 |
| D. 확인되지 않음 | “NN의 baseline 대비 통계적 우월성은 검정하지 않았다.” | NOT_TESTED를 비유의·우월·열등으로 바꾸지 않음 |
| E. 현재 설계에서 검증 불가 | “관측된 τ 연관에서 인과효과와 최초 미관측 Test 일반화를 식별할 수 없다.” | 새 설계 없이 강건 표준오차만으로 해결 불가 |

## 기존 추론의 정확한 범위

STEP5C는 신경망 간 Primary20, Secondary80, Origin100 가설을 블록20/40/60별로 검토한600행이다. NN–baseline 가설이 아니다. Primary BA와 Origin BA 모두 기각0, Secondary3/2/3은 원결과로 보존한다. 블록별 같은 가설을 독립 발견으로 세지 않고 Secondary 반대 증거를 숨기지 않는다.

Holm은 각 가족·블록 설정에서 적용됐으며 모든 가족·블록·사후 비교를 합친 일괄 오류율 보장을 뜻하지 않는다. 보정은 유효하지 않은 원 p값을 고치지 않는다. 기존 percentile CI도 동시 구간이 아니다. STEP9B1R은9설정 모두 핵심 holdout 기준을 충족하지 못했고 추천 금융 방법이 없다. 실제600행 각각을 틀렸다고 재판정한 것은 아니지만 확증적 크기/coverage 인증도 아니다.

20일 label 중첩, 같은 날짜의 Seed 반복, Origin 간 Train 중복, 이전 Test의 후속 Origin 노출과 연구 중 반복 검토가 남는다. Seed10개나 Origin5개를 iid 시장반복으로 두지 않는다. Validation은 checkpoint 선택에 사용됐으며 독립 평가가 아니다. 평균·표본SD는 기술적 변동이지 모집단 CI가 아니다.

## 통계 보완과 집필의 관계

현재 RQ가 기술·탐색적이면 새 p값이 자동 필수는 아니다. 확증적 주장을 고집할 경우 estimand·단위·의존성·가족·크기/coverage 검증이 먼저 필요하다. STEP11의 Brier/HAC/block/기술적 효과/미래평가 후보는 방법 제안이며 채택·실행 승인이 아니다. 유의한 결과를 얻기 위한 사후 방법 선택이나 ‘성공할’ 추가 실험을 제안하지 않는다.

초기 Word의 대표Seed/비중첩 McNemar 수정 의도는 인정하되 제공 Notebook과 수정 실행본의 공백을 명시한다. Test F1 중앙값 대표선정도 Test 의존 선택이며 n38 비중첩이 자동 독립성을 보장하지 않는다. 최신 가설과 다르므로 p값을 직접 비교하지 않는다.

데이터 증빙이 없으면 ‘제공된 최종 시계열 조건부 회고적 관찰’로 범위를 제한한다. 통계기법은 공급처·PIT·이용권한을 인증하지 못한다. 실시간 예측·투자 수익성은 검증되지 않았다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
