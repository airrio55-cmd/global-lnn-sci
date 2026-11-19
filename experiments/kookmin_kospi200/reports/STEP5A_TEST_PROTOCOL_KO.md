# STEP5A_TEST_PROTOCOL_KO

확인시각(KST): 2026-11-20T08:10:41.245073+09:00. 기존 완료500fit, 이번 신규학습0/Test 예측0/Test 성능0/금융 통계검정0/checkpoint load0/모델forward0/HMM0/Ensemble0/τactual0/GPU0/2026관측 사용0. 기존 원본·결과·모델·master flags는 보존한다. 이 문서는 준비·동결 감사이며 계획은 실행 결과가 아니다.

설계2 A/B 병렬 F1 회고적 연구를 유지한다. Origins O1~O5, Seeds2/12/22/32/42/52/62/72/82/92, RNN/LSTM/GRU/LTC/CfC의500개 best checkpoint를 추후 각각 단1개 평가 identity에 연결한다. 현재500행은 PLANNED_NOT_EXECUTED/approved=false다.

연구기간2010-01-01~2025-12-31. 공식3939 KRX 세션의 전역0-based session_id, window t-19~t20세션, target I(Close[t+20]>Close[t]), threshold probability>0.5(동률0). 피처순서 Log_Ret,Disparity. Vol_Regime은 공통 window 유한 적격마스크/레짐보조이며 신경망입력 아님. bfill·미래보간·NaN0치환 금지. 보존된 Train window 합집합 scaler만 transform하고 재fit 금지. 수동q30/q70 Train-only 고정, Test 재계산 금지.

Train label_end<Validation 첫세션, Validation label_end<Test 첫세션. Test2021~2024의 기준일은 당해 연말까지이며 label_end는 다음해라도 연구종료일 이내면 허용한다. Test2025 말단20세션은 UNKNOWN/제외하며2026가격 타깃확인 금지. 이번에는 달력과 STEP3C 구조적 계획만 대조했으며 Test 가격·Target·확률을 열지 않았다.

| Origin | Test 기준일 시작~마지막 known | 계획 기준일 수 | UNKNOWN 제외 | 최대 label_end |
| --- | --- | ---: | ---: | --- |
| O1 | 2021-01-04~2021-12-30 | 248 | 0 | 2022-01-28 |
| O2 | 2022-01-03~2022-12-29 | 246 | 0 | 2023-01-31 |
| O3 | 2023-01-02~2023-12-28 | 245 | 0 | 2024-01-29 |
| O4 | 2024-01-02~2024-12-30 | 244 | 0 | 2025-02-04 |
| O5 | 2025-01-02~2025-12-01 | 222 | 20 | 2025-12-30 |

이 수치는 가격 없는 **달력 기준 계획 수**다. 실제 Test finite feature/window/가격 완전성·A/B 공통날짜 검증은 다음 별도 승인 단계에서 수행해야 한다. 현재 확정된 금융 Test 평가표본 수라고 보고하지 않는다.

Primary BA; Secondary MacroF1/Brier/Recall0/Recall1. Diagnostics Accuracy/positive rate/DEGENERATE_PREDICTION. confusion matrix labels=[0,1]. 한 실제 클래스면 BA/MacroF1 null, 지원이 없는 클래스 Recall null, 지원 있는 클래스 Recall 정의, Brier/Accuracy는 유한 입력이면 정의. 빈집합은 지표null. 누락/실패는0으로채우지 않는다. 모든 모델·Seed는 Origin/Candidate 안에서 동일 날짜벡터·Target과 session_id로 정렬한다. Seed별 지표 후 평균·ddof1표준편차·중앙값·범위를 기술적으로 보고하며 A/B 혼합/Seed 평균확률 Ensemble 금지. 저장된 Train/Validation 선택 결과를 Test로 모델선택하거나 수정하지 않는다.

공개 범위: 개별500개 identity와 체크포인트/입력/소스 해시를 연결한 동결 roster 및 상세 Test job plan은 자동 공개 승인 검토에서 외부 공개가 거부되어 로컬에만 보존한다. GitHub에는 코드·집계·구조적 달력 계약·요약 보고서만 게시한다. 거부된 개별 매핑을 다른 파일명으로 재게시하지 않는다.
