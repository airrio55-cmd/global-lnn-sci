# STEP12 박사논문 연구 방향 검토안

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

## 우선 제안

**평균 예측 성능과 안정성을 분리하고 LTC 내부 동역학을 탐색적으로 진단하는 회고적 실증연구**를 주결과로 제안한다. 이는 STEP10C의 방향A와 STEP11의 제한된 증거 등급을 따른다. 높은 BA 또는 유리한 Test 결과를 근거로 주제·가격·모델을 사후 선택한 제안이 아니다. 현재 확보된 실행 범위와 논증 가능 범위를 일치시키려는 정리다.

국문 제목 검토안: **「KOSPI200 방향성 예측에서 신경망의 예측 안정성과 LTC 내부 동역학에 관한 실증연구」**.

영문 제목 검토안: **“An Empirical Study of Prediction Stability and LTC Internal Dynamics in Neural Network-Based KOSPI200 Direction Forecasting”**.

제목의 ‘실증’은 사용자 제공 최종 시계열에 대한 회고적 분석을 뜻한다. 실시간 정보 가용성·수익성·확증적 우월성을 암시하지 않도록 초록과 방법 절에 범위를 명시한다. ‘내부 동역학’도 τ가 시장을 설명하는 인과 메커니즘을 발견했다는 뜻으로 사용하지 않는다. 문헌 검토와 교수 의견에 따라 ‘회고적’ 또는 ‘탐색적 진단’을 제목에 추가하는 선택지도 있다.

## 원형 연구와 최신 연구의 경계

| 항목 | 초기 원형 | 최신 주결과 제안 |
| --- | --- | --- |
| 핵심 모형 | RAW5 LNN Single, RAW5/LOG2 LNN Ensemble | F1 두 피처 기반 RNN/LSTM/GRU/LTC/CfC |
| 구현 | 제공 Notebook의 최종 활성 LNNModel은 LTC; CfC는 별도 | 같은 계열 LTC를 포함하지만 원형과 동일 학습모델 아님 |
| 실험 설계 | 1·5·10Seed, 단일 Test, 초기 McNemar/HMM | 5Origin×A/B×10Seed×5NN, 안정성·레짐·τ 진단 |
| 비교 해석 | Historical Baseline 및 연구 전개 | 현재 동결 결과에 대한 기술·탐색적 주결과 |
| 미검증 부분 | 수정 통계 실행 버전, RAW5 외부 시점, 원고 모델명 | 국내 가격 출처/PIT, 추론 타당성, 인과/투자효과 |

최신500은 원형 Ensemble 재현이나 Ensemble 추가효과 검증이 아니다. 서로 다른 Test·입력·label·집계를 직접 차감해 개선/악화라고 쓰지 않는다. 초기 결과는 삭제하지 않고 연구 전개와 설계 변화의 배경으로 구분한다.

## 원문 확보와 확인 범위

초기 DOCX 수신본과 보존 Notebook3개는 이번 작업환경에 존재한다. DOCX SHA-256은 `1d97db639dd3164ab7ca83d74ddbb4df4ca5e4cc852bc17345bca3ab5b90599d`이며 ZIP/XML 정상 열기와 본문516문단을 확인했다. Notebook은 실행하지 않고 최종 클래스가 있는1-based cell8을 정적으로 읽었다.

Word §2.9 P0223·§3.2 P0344·결론 P0441의 CfC 서술과 제공 Notebook의 LTC 정의 불일치는 STEP10C 근거와 일치한다. 실제 집필 당시 다른 수정 실행본이 있었는지는 여전히 미확인이다. 원문을 수정하지 않았고 표 전체 재감사·검정도 반복하지 않았다. STEP10B의 당시 DOCX 부재 기록은 역사적 기록으로 유지하고 STEP10C 이후 확보 사실을 연결한다.

## 교수 판단이 필요한 사항

제목 변경, RQ의 기술·탐색적 범위, 원형 Ensemble의 Historical Baseline 배치, τ 진단을 주요 기여로 둘 수 있는 문헌상 근거, 출처 미해결 상태의 학술 수용 가능성을 검토받는다. 교수 검토 전 ‘방향 확정’·‘학위 요건 충족’으로 표현하지 않는다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
