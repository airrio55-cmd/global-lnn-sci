# STEP8B BASELINE_MASTER_PROTOCOL

이번 결과는 **실제 기준모형 평가 전 BLOCKED**다. 동결40개 단위 모두 입력 재읽기에서 차단됐으며 완료0/BLOCKED40, Logistic fit0/10, Climatology 추정0, 규칙 평가0이다. 성능값을0으로 만들지 않고 null/NOT_EVALUATED로 유지한다. 기존 NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED와 이전9678파일을 보존한다. NN 재학습/checkpoint load/forward, HMM fit/refilter, τ추가계측, 금융bootstrap/Holm/p값, Ensemble/GPU/2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED. 회고적 비교 승인과 실시간 인증은 구분하며 O1~O4 Test와 후속Validation의 역사적 중복/Origin·Seed·중첩label 의존성을 유지한다.

사양은 금융 baseline 성능을 보기 전에 동결했다. 프로토콜SHA: `d7ff05bdfa45691d7f2535c240dd7f522c429b521974aa7ba1b31e82eb512bf2`.

|기준모형|동결 계약|
|---|---|
|Climatology|purge 후 Train Target 평균 상수 p; p>.5만1, 동률0; Train단일클래스도0/1확률로 적격·flag기록|
|Logistic|t의 [Log_Ret,Disparity]만; window flatten없음. C1,L2,lbfgs,max_iter1000,interceptTrue,class_weightNone,random_state20261120,tol1e-4. Train단일클래스/비수렴/비유한계수BLOCKED|
|별도LR scaler|purging후 유지된Train의현재t행만StandardScaler.fit. 신경망의window입력범위scaler를재사용하지 않음. Test transform만 허용|
|200DMA|공식session순서 t포함200개종가평균보다Close[t]가크면1, 아니면0|
|Momentum60|Close[t]>Close[t−60]이면1; 정확60공식세션차이,61관측점, 동률0|

Train/Validation/Test와20session Target·Train label_end<Validation start purge 및 기존Test날짜/label/session/endpoint를 유지한다. O5말단20UNKNOWN제외,2026자료금지. 날짜감소/shift/bfill/임의ffill/미래보간으로우회하지않는다. 기존 STEP5B_TEST_METRICS_V1 함수를 직접 재사용한다. 실제단일클래스BA/MacroF1=null, 미지원Recall=null; 실제양클래스+단일예측은BA/F1계산하고DEGENERATE표시. 확률threshold엄격>.5, 동률0. 규칙0/1의Brier는degenerate probability forecast이며 calibrated 확률이 아니다. Validation을이용한튜닝없음. NN은기존10Seed를Origin내동일가중평균, baseline은seed반복없는1회로계획했으며이번실제baseline평가는실행되지않았다.

확인일:2026-11-20 KST. 근거:동결STEP5B/5C/6B/7B/8A보고서와저장manifest·이번실패ledger. 새공식가격/PIT증빙을확보했다고주장하지않는다.
