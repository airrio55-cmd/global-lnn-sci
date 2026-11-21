# STEP12 최종 권고와 열 가지 질문의 답

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

## 우선 검토할 문서

[교수 검토 메모](STEP12_SUPERVISOR_REVIEW_MEMO_KO.md), [RQ 근거표](STEP12_RQ_EVIDENCE_MATRIX_KO.md), [기여 후보](STEP12_ACADEMIC_CONTRIBUTIONS_KO.md), [목차 변경안](STEP12_DISSERTATION_OUTLINE_KO.md), [심사 질문22개](STEP12_DEFENSE_QA_KO.md), [보완 우선순위](STEP12_REMEDIATION_PRIORITIES_KO.md)를 함께 검토한다.

## 질문별 최종 답

| 질문 | 권고·확인된 사실 | 미검증/판단 필요 |
| --- | --- | --- |
| 1. 현재 결과로 어떤 논문을 쓸 수 있는가? | F1 기반5NN의 회고적 성능·안정성·레짐과 LTC 내부 동역학 진단 연구 | 공식 가격/PIT·확증 우월성 연구로는 인증되지 않음 |
| 2. 핵심 학문적 기여는? | 평균과 안정성 분리, LTC 퇴화의 체계적 진단, effective τ의 탐색적 연관이라는3후보 | 문헌상 차별성·학위 수준 충분성은 검토 필요 |
| 3. 퇴화·τ가 독창적 기여가 될 수 있는가? | 통합 진단의 실증 기여 후보가 될 수 있음 | 최초성 미확인, 원인·경제적 기억·구성독립 효과 미식별 |
| 4. 현재 통계 수준의 주장 범위는? | 기술적 관찰·탐색적 연관·한계가 명시된 기존 근사결과 | Primary BA 우월성 미확립, baseline NOT_TESTED, METHOD_NOT_VALIDATED |
| 5. 가장 심각한 학문적 위험은? | 증거 범위를 넘는 공식/PIT·모델 정체성·통계/인과 주장이 결론을 왜곡할 위험 | 가격 출처 미확정과 CfC/LTC 불일치부터 명시·정합화 필요 |
| 6. 데이터 증빙이 없으면? | 사용자 제공 최종 시계열 조건부 회고적 기술·탐색 범위로 제한 | 사용권한/출처를 학술적으로 수용할지는 교수·심사 판단; 수용 불가하면 제출 보류 |
| 7. 우선 제안할 방향은? | 최신 F1 성능·안정성·LTC 진단 중심 방향A, 원형 Ensemble은 Historical Baseline으로 구분 | 제목·RQ·기여 선택의 최종 교수 판단 필요 |
| 8. 무실험 최우선 보완은? | 원고–코드 모델명/선택 기준 정합, 문헌 기여 비교, 원본·수정 실행증빙 연결 | 새 p값은 이 공백을 해결하지 못함 |
| 9. 제목·RQ에 교수 판단이 필요한 곳은? | 제안 제목의 ‘내부 동역학’ 범위, ‘회고적/탐색적’ 명시, RQ4 인과 제한, 원형 위치 | 모두 검토안이며 승인 전 확정하지 않음 |
| 10. 완성을 위한 최소 필요조건은? | 기여의 문헌 근거, 모델·결과·원고의 버전 정합, 자료 이용/출처 증거 또는 명시적 수용 범위, 반대 증거·통계 한계, 제목/RQ 교수 합의 | 추가 학습 횟수 자체가 학위 충분성을 보장하지 않음 |

## 제출 전 의사결정

현재 F1 기술·탐색적 집필에는 신규 학습이 자동 필수는 아니다. 원형 Ensemble의 추가효과를 핵심 주장으로 유지하려면 별도 Bridge가 필요하며 현재는 증빙/사양/승인 전 차단 상태다. 데이터가 실제 바뀌는 경우 영향 산출물의 조건부 재평가부터 검토한다. 성공적 결과·새 유의성을 얻기 위한 사후 실험은 제안하지 않는다.

제안 제목은 **「KOSPI200 방향성 예측에서 신경망의 예측 안정성과 LTC 내부 동역학에 관한 실증연구」**다. 현재 확인된 실행 범위에 맞춘 방향이지 더 높은 Test 성능에 따른 선택이 아니다. 기존 목차·초안은 수정하지 않고 변경 제안만 제시했다. 교수 발송이나 승인은 이뤄졌다고 기록하지 않는다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
