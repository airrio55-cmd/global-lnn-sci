# STEP4D_LTC_DIAGNOSTICS 공개 집계 요약

국민대학교 BIT전문대학원 KOSPI200 LNN STEP4D 회고적·탐색적 CPU Train/Validation 진단이다. A/B=BOTH_UNVERIFIED, historical18:00 KST production-PIT=BLOCKED다. Validation은 checkpoint 선택에 사용돼 독립 일반화 성능이 아니다. Seed를 독립 시장 표본으로 연결하지 않았으며 결과로 가격·모델·Seed·설정을 선택하지 않았다.

Seed별 LTC 진단은5Origin×A/B의10개fit을 집계한 기술적 요약이다. 단일 클래스 예측은 수치 발산과 구분한다. 신규LTC30개도 같은 진단으로 집계했다.

| seed_group | fits_across_origins_candidates | best_degenerate_cases | mean_degenerate_epoch_ratio |
| --- | --- | --- | --- |
| Seed2 | 10 | 0 | 0.644950 |
| Seed12 | 10 | 6 | 0.805455 |
| Seed22 | 10 | 0 | 0.614035 |
| Seed32 | 10 | 2 | 0.674660 |
| Seed42 | 10 | 2 | 0.703676 |
| Seed52 | 10 | 4 | 0.754266 |
| Seed62 | 10 | 0 | 0.737299 |
| Seed72 | 10 | 4 | 0.675738 |
| Seed82 | 10 | 4 | 0.724938 |
| Seed92 | 10 | 2 | 0.546412 |

다른 네모델을 포함한10Seed 집계는 [모델 불안정성](../manifests/step4d_model_instability.csv)에 있다.

공개본은 여러 Seed의 집계와 비민감 해시만 포함한다. 개별 Seed/fit 성능·epoch 이력·클래스 support·실제 Train 분위수 임계값·상세 보고서와 그림은 로컬에 보존했다. 원본 가격·일별Target·확률·weights/checkpoint는 게시하지 않았다.
