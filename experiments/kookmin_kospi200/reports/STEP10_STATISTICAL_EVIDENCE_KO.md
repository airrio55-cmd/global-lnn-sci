# STEP10 통계적 증거 최종 감사

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 기존 가족 | 블록별 가설 수 | 블록20 | 블록40 | 블록60 |
| --- | --- | --- | --- | --- |
| Primary BA | 20 | 0 | 0 | 0 |
| Origin BA | 100 | 0 | 0 | 0 |
| Secondary | 80 | 3 | 2 | 3 |

위 수치는 STEP5C의 기존 Holm p<.05 결과 개수이며 총600행에서 저장 p값을 읽어 계수한 값이다. p값·CI·Holm을 새로 산출하지 않았다. Primary20/Origin100 BA 기각0은 우수성을 입증하지 못했다는 뜻이며 동등성 또는 효과 없음의 증거가 아니다. 다른 블록의 같은 가설을 독립 재현으로 세지 않는다. Secondary3/2/3을 합해 8개 독립 발견이라고 쓰지 않는다.

기존 반대 증거로 A LSTM−LTC Recall1 차이0.1040777874와 블록20/40/60 Holm p=0.0311968803/0.0473952605/0.0157984202가 보존돼 있다(STEP9A_STATISTICAL_EVIDENCE, STEP5C_SECONDARY_METRICS). 이는 Recall1 비교이며 BA·전반적 우열로 확대할 수 없다. 기존 percentile CI는 동시 신뢰구간이 아니다.

STEP9B1R에서는 독립 합성 pair 데이터셋4680개·family1200개와 9개 설정을 검토했다. 강한 시계열 의존성·희소 클래스·구조변화의 모든 핵심 기준을 통과한 설정은 없었다. block 길이가 의존성을 충분히 포착하는지, 정상성/약한 의존성·유효 class support, ratio metric의 유한표본 근사, Origin 간 이질성, 공통 유효 draw 선택, 꼬리 p값의 Monte Carlo 정밀도는 실제 금융자료에서 미검증이다. Seed 반복과 중첩20세션 label은 독립 시장 반복이 아니다.

초기199draw family FWER0은 최소 p=.005가 Holm 첫 임계값보다 커 기계적으로 기각할 수 없었던 결과여서 타당성 PASS가 아니다. 1999draw 보완도 작은 꼬리의 정밀도가 제한적이다. 이러한 합성 반례는 실제 STEP5C의 특정 p값이 틀렸다는 직접 판정이 아니며, 반대로 기존 절차의 완전한 확증적 타당성을 인증하지도 않는다. 기존 결과는 EXISTING_APPROX_INFERENCE로 인용하고 가정의 미검증을 함께 밝힌다.

STEP9B2=NOT_EXECUTED, METHOD_NOT_VALIDATED, FINANCIAL_PVALUE_COUNT=0. Baseline 대비 통계적 우월성=NOT_TESTED. STEP9B1의 joint Primary20 / Secondary80 각각 α=.05 설계는 보존하지만, 전체100 가설 FWER5% 보장을 주장하지 않는다. STEP5C의 별도 Origin100을 후속 baseline 가설 가족과 혼동하지 않는다. 신규 금융 검정 없이 서술·탐색적 논문으로 집필할 수 있다.

출처: manifests/step5c_public_aggregate_summary.json#/rows, step5c_execution_summary.json#/families; reports/STEP9B1R_MASTER_REVIEW_KO.md, STEP9B1R_TYPEI_POWER_COVERAGE_KO.md; manifests/step9b1r_method_review.json.


같은 가족 크기라도 STEP5C의 신경망 간 비교와 STEP9B1의 NN–baseline 비교 초안은 서로 다른 가설이다. 기존20/80/100과 후속20/80을 합치거나 후속 검정이 실행된 것으로 표시하지 않는다.
