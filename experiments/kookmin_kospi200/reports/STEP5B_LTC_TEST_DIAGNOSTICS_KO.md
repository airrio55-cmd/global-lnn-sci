# STEP5B_LTC_TEST_DIAGNOSTICS_KO

회고적 Rolling-Origin F1 A/B Test-only 평가. 기존500fit 보존; 실제완료500, 실패0, BLOCKED0. 신규학습/재학습0, HMM0, Ensemble0, GPU0, τactual0, 금융bootstrap/Holm/p값0,2026관측 사용0. A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, 주가격 PENDING이다. Validation으로선택한best checkpoint를고정해사용했으며Test결과로사양·모델·Seed·가격을바꾸지않았다.

LTC Test단일클래스예측은완료100개중24개다. Validation과Test모두단일클래스24개,Test에서만발생0개다. 이집계는예측클래스퇴화이며NaN/발산/실행실패와구분한다. 단일클래스예측도BA/F1정의조건에따라그대로계산했고제거/교체하지않았다. 수치오류/실패는execution summary의실제값으로별도보존한다.

| model | completed | Validation_degenerate | Test_degenerate | Validation_and_Test_degenerate | Test_only_degenerate |
| --- | --- | --- | --- | --- | --- |
| CfC | 100.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| GRU | 100.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| LSTM | 100.000000 | 4.000000 | 2.000000 | 2.000000 | 0.000000 |
| LTC | 100.000000 | 24.000000 | 24.000000 | 24.000000 | 0.000000 |
| RNN | 100.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

Origin/후보별LTC점수와변화는Test결과·gap표의모든LTC행을참조한다. Validation불안정성과Test퇴화의동시발생은연관기술이며원인/일반화우위주장이아니다.
공개 범위: 다중 fit 집계만 포함한다. 개별identity/checkpoint/input매핑·일별확률/Target·원가격·실제scaler/Train임계값·개별상세지표·레짐classsupport는ignored로컬에보존한다. 원본/기존보고서/논문표/main/JOF는변경하지않았다.

Test에서 퇴화한 LTC24개는 모두 Validation에서도 퇴화한 동일 checkpoint였으며, Test에서 새롭게 퇴화한 LTC는0개였다. 완료100개 중 이24개를 제외하지 않았다. LTC의 Origin 동일가중 평균 BA는 A0.532387/B0.531292, Macro F1은 A0.452154/B0.453225로 지표별 해석이 다르다. BA 한 값만으로 안정성이나 모델 우위를 주장하지 않는다. 모든500개 결과가 유한값 검증을 통과했으며 수치 발산으로 실패한 identity는0개다.
