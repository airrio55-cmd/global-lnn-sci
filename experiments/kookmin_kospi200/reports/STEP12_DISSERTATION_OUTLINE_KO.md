# STEP12 기존 초안에 대한 목차·표·그림 변경 제안

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

## 기존 원고와 이번 산출물의 관계

기존 `STEP10_RESULTS_DISCUSSION_DRAFT_KO.md`의 제5~10장 초안과 `STEP10_DISSERTATION_TABLE_FIGURE_PLAN_KO.md`의 표10개·그림8개 명세를 유지한다. 여기서는 장별 배치·해석 수정만 제안하며 전체 논문 본문이나 표/그림을 새로 계산·중복 작성하지 않는다. 아래 표/그림 ID는 STEP10 명세를 참조한다. 상세 민감 결과의 공개 허가는 별도이며 기존 비공개 표를 여기서 복제하지 않는다.

| 장 | RQ·사용 표/그림 | 핵심 내용·기여 | 기존 초안에 대한 변경 제안·주의 |
| --- | --- | --- | --- |
| 제1장 서론 | RQ1~5; 그림1 연구흐름 | 평균 성능과 안정성을 함께 평가할 필요 | 원형 앙상블 ‘성능개선’ 중심에서 현재 진단 목적 중심으로 문제정의 수정 |
| 제2장 이론적 배경 및 선행연구 | RQ1~5; 표2의 모델 구분 참조 | RNN/LSTM/GRU/LTC/CfC, 안정성, 레짐, τ, 의존적 추론 | LTC/CfC 이론 분리; 기여3개별 선행연구 대조표는 문헌 근거 확보 후 작성 |
| 제3장 연구모형 및 실험설계 | RQ1/2/4; 표2, 그림1/2 |5NN·500fit·고정 설정·Origin/Seed, LTC 진단 구조 | 원형 RAW5/LOG2는 배경·Historical Baseline; 최신500과 동일 실험이라 하지 않음 |
| 제4장 데이터와 평가방법 | RQ1~5; 표1/9/10, 그림2 | A/B·F1·20session label·purging/scaler·지표·추론 한계 | 가격/PIT/반복 노출을 방법 절부터 명시; family별 Holm과 METHOD_NOT_VALIDATED 병기 |
| 제5장 신경망 예측 성능 비교 | RQ1/5; 표3/4/5, 기존 성능 비교 그림 명세 | 동결 평균 성능·기준모형의 지표별 반대 증거 | 기존 제5장 문단 재사용; 우월·동등·복잡성 인과 해석 삭제 |
| 제6장 Seed/Origin 안정성 분석 | RQ2; 표6, 기존 안정성 그림 명세 | 단일클래스24/100과 변동/epoch 진단 | 기존 제6장 재사용; Validation/Test·epoch 퇴화·NaN/발산을 구분 |
| 제7장 시장 레짐별 성능 분석 | RQ3; 표7aHMM/7bManual, 기존 레짐 그림 명세 | Train q30/q70·Train HMM·forward filtering·유효 분모 | 기존 제7장 재사용; 민감 support 상세는 비공개 부록, null·분모 차이는 본문 고지 |
| 제8장 LTC 내부 동역학과 예측 퇴화 | RQ4; 표8, 기존 τ 그림 명세 | raw/effective τ·99+1·24/76·8/8방향 | 기존 제8장 재사용; 구성효과·단위·단일τ 역산 공개 제한 명시 |
| 제9장 종합논의 및 연구한계 | RQ1~5; 표9/10 | 세 기여 후보·반대 증거·통계/출처/PIT 위험 | 기존 제9장에 STEP10C 모델 정체성 및 STEP11 등급 연결; 확증 표현 줄임 |
| 제10장 결론 및 향후 연구 | RQ1~5; 기존 RQ 대응표 참조 | 허용 결론·조건부 보완·후속 설계 | 기존 제10장 갱신 제안만 제시; 새 기간·bridge·검정은 별도 승인 전 실행하지 않음 |

## 장 구성 변경의 이유

권장 제3장은 모델/실험 설계, 제4장은 데이터/평가방법으로 구분한다. 기존 STEP10의 ‘제3장 데이터·연구모형/제4장 연구설계·통계방법’ 배치와 달라지는 부분은 목차 재배치 제안으로 표시한다. 제5~10장의 기존 결과 설명을 반복 작성하지 않고 같은 근거를 사용한다.

표3·4의 평균값은 학습 Seed 평균과 Origin 가중치를 명시한다. 표7은 manual/HMM을 합쳐 하나의 참 상태 결과처럼 만들지 않는다. 표8은100개 신규정량 요약을 공개하지 않으며 기존99 공개값에서 복구1개를 역산할 수 있는 분할을 추가하지 않는다. 표9는600행 전부의 확증 인증표가 아니라 기존 근사결과/방법 한계표다. 표10은 기술적 완료와 과학적 차단을 구분한다.

최종 장명·제목·RQ 문구·문헌 기반 독창성 인정은 교수 검토 대상으로 남긴다. 원고 정정 자체는 이번에 수행하지 않았다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
