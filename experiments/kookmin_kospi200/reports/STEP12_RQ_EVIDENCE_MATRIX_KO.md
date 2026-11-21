# STEP12 RQ1~RQ5의 목적·근거·허용 결론

작성일: **2026-11-21, Asia/Seoul**. 국민대학교 BIT전문대학원 박사학위논문 연구, 안현철 지도교수 검토용 **제안서**. 제목·RQ·학위 적합성에 대한 교수 승인을 받은 문서가 아니다.

대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. STEP12는 기존 동결 근거의 집필·검토 패키지이며 새 실험이나 반복 금융 감사가 아니다. 신규 금융 fit/forward/Test 평가/HMM fit/τ 계측/bootstrap/p값·CI는 모두0, 기존 master 실행 flags=false를 유지한다. 2010-01-01~2025-12-31 연구범위와 2026 시장 관측 금지도 유지한다.

가격 A/B **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, 통계방법 **METHOD_NOT_VALIDATED**를 유지한다. 파일 SHA 보존·공식 세션 정렬은 가격 공급처/PIT 인증이 아니다. JOF 다국가 연구와 혼합하지 않는다.

RQ 번호는 STEP10/11 그대로 유지한다. 아래 문구는 사용자가 제안한 검토 문구이며 최종 승인 전이다.

## RQ1. RNN, LSTM, GRU, LTC, CfC의 평균 방향 예측 성능은 어떻게 다른가?

| 요소 | 정리 |
| --- | --- |
| 연구 목적·비교 대상 | 동일 F1 연구에서5NN의 지표별 기술적 차이 확인 |
| 데이터 단위 | Origin×가격×모델×Seed의 동결 예측; 같은 날짜의 Seed는 독립 관측 아님 |
| 적용 지표 | BA 주 지표, Macro F1, Accuracy, Recall0/1, Brier와 positive rate 보조 |
| 기존 결과 | LTC BA A0.532387/B0.531292; Origin 내 Seed 평균 후 동일5Origin 가중 |
| 반대 증거 | 지표별 순위 차이, LSTM−LTC Recall1의 기존 Secondary 반대 증거, BA 유의 차이 미확립 |
| 통계 수준 | DESCRIPTIVE_SUPPORTED / INFERENCE_LIMITED; Primary/Origin BA 세 블록 기각0 |
| 허용 결론 | 관측 평균 차이가 있다. LTC의 보편적·통계적 우월성은 확증되지 않음 |

## RQ2. Seed와 Rolling Origin에 따라 신경망의 예측 안정성과 단일 클래스 예측 현상은 어떻게 변화하는가?

| 요소 | 정리 |
| --- | --- |
| 연구 목적·비교 대상 |5모델의 초기화·시기별 변동과 실패 양상을 함께 기록 |
| 데이터 단위 | 모델별100개 fit identity, 고정 Seed/Origin별 저장 history와 동결 checkpoint |
| 적용 지표 | 기존 BA/F1/Brier 변동, best/total epoch, 단일예측 epoch 비율, 전체 Test positive rate·퇴화 수 |
| 기존 결과 | 전체 Test 단일예측 LTC24/100, LSTM2/100, RNN/GRU/CfC0/100 |
| 반대 증거 | LTC76개는 전체 Test 단일예측이 아니며 한클래스 예측은 NaN/발산과 다름 |
| 통계 수준 | DESCRIPTIVE_SUPPORTED; Seed/Origin SD는 미래시장 CI 아님 |
| 허용 결론 | 이 고정 사양에서 안정성 문제가 조건별로 관찰됨; 보편적 원인/발생확률은 미확인 |

## RQ3. 수동 변동성 레짐과 HMM 레짐에 따라 예측 성능과 클래스 구성은 어떻게 달라지는가?

| 요소 | 정리 |
| --- | --- |
| 연구 목적·비교 대상 | 같은 동결 예측을 Train 기준 수동/HMM 레짐으로 각각 층화 |
| 데이터 단위 | Origin×가격×레짐×모델의 평가일, Seed 반복; HMM선택10은100후보 부분집합 |
| 적용 지표 | BA/MacroF1·Recall0/1·표본/클래스 구성·유효 분모; 민감 support 상세는 비공개 |
| 기존 결과 | Train q30/q70 및 Train HMM/forward filtering의 저장 층화 결과 존재 |
| 반대 증거 | 일부 레짐은 한 클래스여서 BA/F1 null, 유효 Origin 집합·점유율 차이 |
| 통계 수준 | EXPLORATORY_SUPPORTED; 레짐 인과효과 검정 아님 |
| 허용 결론 | 레짐별 기술적 패턴과 구성 차이를 함께 보임; 유리한 레짐/모델을 선택하지 않음 |

## RQ4. LTC 내부 effective tau와 단일 클래스 예측 퇴화 사이에는 어떤 탐색적 연관성이 관찰되는가?

| 요소 | 정리 |
| --- | --- |
| 연구 목적·비교 대상 | LTC 퇴화군과 비퇴화군의 내부 동역학을 진단 |
| 데이터 단위 | checkpoint100개, 하위 뉴런/window/substep은 종속 계측 |
| 적용 지표 | raw/effective τ 정의 및 기존 비교 방향·유효 모델 수; 새100정량집계 공개 억제 |
| 기존 결과 |24/76, 공존8/8셀에서 퇴화군 effective τ가 낮은 방향 |
| 반대 증거 | Origin/가격/Seed 구성 차이, O5 퇴화군 부재, 공존하지 않는 셀 제외 한계 |
| 통계 수준 | EXPLORATORY_SUPPORTED; 구성독립·인과효과 미식별 |
| 허용 결론 | 이 자료에서 낮은 effective τ와 퇴화가 함께 관측됨; 원인·경제적 기억시간은 미확인 |

## RQ5. 신경망의 예측 성능은 단순 기준모형과 비교할 때 어떤 기술적 차이를 보이는가?

| 요소 | 정리 |
| --- | --- |
| 연구 목적·비교 대상 |5NN과 Climatology/Logistic/DMA200/Momentum60 비교 |
| 데이터 단위 | 같은 평가일·Target, NN은 Seed 평균/Origin 평균; baseline은 Origin별 결과 |
| 적용 지표 | BA/MacroF1/Brier·Recall·Accuracy·positive rate의 기존 요약 |
| 기존 결과 | Momentum60 BA0.504416, MacroF10.491019; NN 평균 BA와 다른 F1 패턴 |
| 반대 증거 | Momentum60 F1의 상대적 강점, 퇴화 LTC의 추가 BA 부재, 정보이력 차이 |
| 통계 수준 | DESCRIPTIVE_SUPPORTED; 통계적 우월성 NOT_TESTED |
| 허용 결론 | 같은 평가일의 benchmark 기술적 차이; 복잡성·투자·통계적 우월성은 미확인 |

## 기존 표현과의 차이·이유

STEP10 RQ1 ‘성능 비교’는 유지하고, STEP11 RQ1에 함께 쓰였던 ‘안정성’은 RQ2에 명시해 평균과 변동을 구별했다. RQ2는 LTC뿐 아니라5모델과 단일클래스 현상을 분명히 했다. RQ3는 클래스 구성·null을 추가해 성능차의 분모 문제를 드러냈다. RQ4는 ‘탐색적 연관’이라는 한계를 질문 자체에 명시했다. RQ5는 ‘어떤 기술적 차이’로 한정해 미실행 baseline 유의성 검정과 구분했다. 새 RQ를 결과에 맞춰 선별하거나 번호를 재배열하지 않았다.

## 근거와 관련 자료

[STEP10 연구질문·결론](STEP10_RQ_CONCLUSION_MATRIX_KO.md), [STEP10 기여와 한계](STEP10_LIMITATIONS_AND_CONTRIBUTIONS_KO.md), [STEP10C 최종 권고](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP11 증거 등급](STEP11_RQ_EVIDENCE_GRADING_KO.md), [STEP11 통계 타당성](STEP11_STATISTICAL_VALIDITY_REVIEW_KO.md), [STEP11 보완 우선순위](STEP11_DISSERTATION_REMEDIATION_PLAN_KO.md). 기존 문서를 수정하지 않고 제안과 확인된 사실을 구분했다. 금융 상세 결과·일별 배열·비공개 설정은 이 패키지에 포함하지 않는다.
