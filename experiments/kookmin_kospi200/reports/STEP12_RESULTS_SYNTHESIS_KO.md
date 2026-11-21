# STEP12 기존 동결 결과 통합 요약

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

## 규모와 집계 계약

5Origin × 가격A/B ×10Seed ×5NN = **500 fits / 500 Test evaluations**다. 500은 독립 시장표본500개가 아니다. 기준모형40결과, HMM100후보/선택10, STEP5C600행, versioned LTC τ100을 별도 산출물로 보존한다. HMM선택10은100의 일부이며 τ는 원99+복구1이다. STEP3D O3 재사용20개는 중복 계수하지 않는다.

NN 평균은 Origin 안에서10Seed를 평균하고5Origin을 같은 가중치로 합친 기존 요약이다. baseline은 Origin별 결과의 동일5Origin 평균이다. 날짜 수로 전체 panel을 풀링하거나 Seed 확률을 Ensemble한 결과가 아니다.

| 동결 사실 | 기존 저장값 | 증거 위치 | 해석 한계 |
| --- | --- | --- | --- |
| LTC 평균 BA | A0.532387 / B0.531292 | step8br_public_aggregate_summary.json#/candidate_primary | 미세 순위·지표 차이를 우월성 인증으로 쓰지 않음 |
| 전체 Test 단일클래스 예측 | LTC24/100, LSTM2/100, 나머지3모델0/100 | step5b_public_aggregate_summary.json#/model_instability | Validation의 LSTM4/100과 혼동 금지; 수치발산 아님 |
| LTC τ 완성 분모 |100개, 퇴화24/비퇴화76 | step7br_public_aggregate_summary.json | 원99 기록을100으로 덮어쓴 것 아님 |
| τ 공존 셀 방향 |8/8셀 퇴화군 effective τ 낮은 방향 | 같은 manifest의 common_Origin_price_cells/lower_degenerate_tau_in_all_common_cells |8독립 발견·인과/구성독립 효과 아님 |
| Primary BA / Origin BA | 각 블록20/40/60에서 기각0 | step5c_execution_summary.json#/families | 동등성·차이0 입증 아님 |
| Secondary 기각수 | 블록20=3,40=2,60=3 | 같은 summary | 독립적인8개 발견으로 합산 불가 |
| Momentum60 | 평균 BA0.504416 / MacroF10.491019 | step8br_public_aggregate_summary.json#/candidate_primary | 높은 F1은 NN 전반 우월성 주장에 대한 반대 증거 |

이번 작업은 위 저장 집계의 요청값 일치와 인용만 확인했으며 금융 metric을 재계산하지 않았다. 개별 fit별·Origin별 민감 수치표나 복구된 단일 τ를 역산할 새100개 평균·분포는 게시하지 않는다.

## 일관된 결과 서술

LTC의 평균 BA는 이 회고적 고정 사양에서 관찰된 수치다. 동시에 전체 Test 단일예측24건, 다른 지표·Origin의 반대 증거가 존재한다. 평균 성능과 안정성을 분리해야 한다는 논의가 가능하며 ‘LTC가 가장 우수하다’고 결론내릴 수 없다.

레짐 분석은 Train-only 수동 경계 및 HMM filtering을 사용하지만 레짐 간 표본·클래스·유효 Origin 구성이 다르다. τ 분석의8/8방향은 구성효과를 완전히 제거하지 못한 탐색적 근거다. Baseline 대비 금융 통계검정은 NOT_TESTED다. 이러한 한계를 포함한 통합 진단이 최신 논문의 주결과 후보이며 원형 RAW5/LOG2 Ensemble의 검증으로 바꾸지 않는다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
