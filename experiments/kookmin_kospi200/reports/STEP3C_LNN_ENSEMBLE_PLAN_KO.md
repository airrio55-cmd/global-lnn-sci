# STEP3C LNN Single/Ensemble 별도 사양

이번 단계는 사양·데이터 준비와 소스 정적 검사만 수행했다. 신규 모델 fit·모델 생성/forward·checkpoint load·HMM fit·독립 Test 예측/성능 평가·GPU 실행은 모두0건이다. production training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지한다. 기존40개와 원본·논문 결과·JOF V14/V15·main을 보존한다.

원본10시드 Notebook SHA-256 `b9e8542fc5783bc5dc734ddfd7bdfe69db26d4b540cde93ae3a722596485c1e7`. 실제1부터 시작하는 cell9 lines38~39: RAW=[Log_Ret,Foreign_Net,Nasdaq,SOX,Disparity], LOG=[Log_Ret,Disparity]. LOG는 RAW의 부분집합이다. cell14 line17의 LTC offset은 RAW401/LOG402, line143은0.5*r_lnn+0.5*l_lnn, line148은 LNN Single=r_lnn, line150은0.7*lnn_ens+0.3*r_rnn이다. 최종 모델 정의 cell8/FocalLoss cell6의 source hashes는 master config에 저장했다. 원본 전체 Notebook은 실행하지 않았다.

| 보고 항목 | 학습 모델/입력 | 조합 |
| --- | --- | --- |
| LNN Single | LTC_RAW5, seed+401 | RAW 확률 그대로 |
| LTC_LOG comparator | LTC_LOG2, seed+402 | LOG 확률 그대로 |
| LNN Ensemble | 위 두 독립 모델 | 같은 Origin/Seed/date의 확률50:50 |
| Hybrid_SOTA | LNN Ensemble 및 RNN_RAW5(seed+101) | 0.7×LNN ensemble+0.3×RNN RAW |

단일시드 원본은 LOG offset411 및 Hybrid의 RNN ensemble 조합이라 다중시드 사양과 다르다. 과거 코드/결과를 고치지 않고 이번 계획은 다중시드의402/0.3RNN_RAW 사양을 별도로 고정한다. F1 현재 LTC는2피처·offset401이므로 LOG402와도 identity가 다르다. 2피처 하나의 학습이나 같은 확률 두 번 평균을 원본 RAW5/LOG2 ensemble 재현이라고 표현하지 않는다.

전체5모델 RAW/LOG는500fit/가격, A/B1000fit. LTC만 RAW/LOG=100fit/가격, A/B200fit이며1000의 부분집합이다. 확률 결합 자체는0fit. 현재40개 F1은5피처 RAW 입력이 아니고 LOG seed offset도 달라 원본채널 모델로 자동 재사용하지 않는다. 외부피처가 해결되지 않아5피처 학습은 BLOCKED다.

동일 Origin/Seed/date/label/평가 cutoff·공통 유한 window·Train-only scaler를 먼저 고정한다. 후보 A/B도 분리한다. 결합키에 candidate,origin,seed,date를 포함하고 RAW/LOG 값이나 날짜 하나라도 없으면 BLOCKED 처리한다. 새 master_ensemble.original_lnn_composition은 candidate별로 분리한 뒤 specs.keyed_ensemble을 호출하고, 피처 순서·유효seed·checkpoint lineage까지 검증한다. 원래 specs.keyed_ensemble을 단독 호출할 때는 후보별 분리가 필요하다. 다른 Seed/가격/날짜의 확률을 섞지 않는다. 비교 시 Single/LOG/Ensemble 모두 같은 공통 날짜를 사용하며 유리한 후보/가중치를 Validation/Test로 선택하지 않는다.

미래 통계 가족: 후보2×RAW/LOG/Ensemble 세 쌍비교3=6가설을 블록길이별 하나의 Holm 가족으로 사전 고정한다. Primary 관심은 Single_RAW 대 Ensemble이고 나머지도 함께 보존한다. 신경망5모델 F1의20가족과 분리된 확장 분석이다. 외부 PIT·사양/해시·공통표본·별도 실행 승인이 갖춰지기 전 학습/검정은 실행하지 않는다.
