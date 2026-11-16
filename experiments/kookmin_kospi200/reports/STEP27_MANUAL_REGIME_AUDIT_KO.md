# STEP2.7 원본 수동 레짐 Balanced Accuracy 보존 감사

확인일2026-11-16. 실제 Notebook의1-based 셀번호를 사용한다. [Cell N] 주석 번호와 다르다. 단일·5·10seed의 실제 셀14~17과 upstream 정의6/8/9/11/12/13을 읽었고 실행하지 않았다. 중복된 사용자 요청은 같은 감사로 처리했다. 원본 source/출력 해시·정확한 셀 내부행은 provenance/step27_notebook_source_references.json, 원본전체 source는 로컬 evidence/*_cells.txt와 사용자 Notebook에 보존돼 있다.

## 실제 계산·출력 연결

실제 공통 함수는 **셀12 calculate_metrics**다. return 순서는 accuracy_score, balanced_accuracy_score, recall_score(positive1,zero_division0), precision_score, f1_score(average='macro'), f1_score(binary)다. 셀13 metrics_list의 두 번째 항목 ‘Bal Acc’와 대응한다. 공식은 두 정답 클래스가 있을 때 BA=(TP/(TP+FN)+TN/(TN+FP))/2다. 원본은 sklearn 함수 그대로이며 absent-class일 때의 평균/경고 처리를 명시하지 않았다. 빈 입력 함수는[0.0]*6을 반환하지만 호출부는 mask합>0일 때만 저장하고 빈 레짐 표는N/A로 출력한다.

단일은 셀11 compute_regime_masks를 정의하고 셀14에서 기본 확률을 저장한 뒤 **셀16에서 HMM과 manual mask를 계산**하고 모델→저장확률→레짐 루프로 calculate_metrics(y_test_true[mask],(probs[mask]>0.5).astype(int))를 저장한다. 다중은 셀14 compute_regime_masks가 매seed 후 실행되고 같은 mask별 함수를 regime_agg[name][reg]에 append한다. 셀16은 np.array(regime_agg[name][reg])를 axis0 평균한 mean_mets를4자리 문자열로 표시한다. 셀15는 전체 성능mean±np.std(ddof0), 셀17은 별도 HMM state 성능표다. 단일Hybrid는0.7LNNensemble+0.3RNNensemble, 다중은0.7LNNensemble+0.3RNN_RAW로 달라 직접적인 seed 수 효과 비교가 아니다.

## 레짐 변수·계산 기간

셀9 Vol_Regime=Log_Ret.rolling(40).std(ddof1), Log_Ret=ln(C/C.shift1). **test_vol=d_test_main['Vol_Regime'].values[WINDOW_SIZE:]**, np.percentile(test_vol,30/70)를 사용한다. Low는<=q30, High는>=q70, Mid는q30<x<q70다. 고정 수치 임계값이 아니라 Test 전체 분포의 분위수이며 원본의 예측 기준일 정렬값을 쓴다. 동일값 tie가 많으면30:40:30 비율을 보장하지 않고 q30=q70이면 Low/High가 겹칠 수 있다.

단일 정의는 실제 셀11, 다중에는 셀11과 셀14 내부에 중복 정의된다. 본 학습 이후 표는 각각 셀16/셀14 함수 경로를 따른다. 기존 AUDIT의 원본 split 계산에 따르면 score 기준일2023-01-19~2026-03-05·759개이며 새 연구기간 밖 관측을 포함할 수 있는 Historical Baseline이다. 이번에는2026년 값을 읽어 분위수나 성능을 재계산하지 않았다. **원본 임계값 숫자는 저장 출력에 없어 UNKNOWN**이며 임의 복원하지 않는다. 과거 출력의 Test-based 표를 실시간 레짐 성능으로 인증하지 않는다.

## 저장된 과거 값의 보존

다음은 원본 셀16의4자리 저장 출력만 복사한 값이다. 새 예측이나 새 성능 계산이 아니다. 단일 열은 seed42, 다중 열은 각5/10seed 평균이며 per-seed 값이 아니다.

| 수동 레짐 | 모델 | 단일(seed42) | 5seed 평균 | 10seed 평균 |
|---|---|---|---|---|
| High_Vol | RNN | 0.4873 | 0.4349 | 0.4557 |
| High_Vol | RNN Ensemble | 0.5110 | 0.4393 | 0.4530 |
| High_Vol | LSTM | 0.5000 | 0.4974 | 0.4997 |
| High_Vol | LSTM Ensemble | 0.4960 | 0.4852 | 0.4915 |
| High_Vol | GRU | 0.5175 | 0.4708 | 0.4721 |
| High_Vol | GRU Ensemble | 0.5064 | 0.4448 | 0.4319 |
| High_Vol | LNN Single | 0.4497 | 0.5079 | 0.5104 |
| High_Vol | LNN Ensemble | 0.4491 | 0.5093 | 0.5060 |
| High_Vol | CFC Single | 0.4840 | 0.4908 | 0.4804 |
| High_Vol | CFC Ensemble | 0.4684 | 0.4873 | 0.4604 |
| High_Vol | Hybrid_SOTA(L7:R3) | 0.4888 | 0.4913 | 0.4715 |
| Mid_Vol | RNN | 0.5063 | 0.5372 | 0.5352 |
| Mid_Vol | RNN Ensemble | 0.5126 | 0.5411 | 0.5374 |
| Mid_Vol | LSTM | 0.5080 | 0.5167 | 0.5135 |
| Mid_Vol | LSTM Ensemble | 0.5160 | 0.5215 | 0.5196 |
| Mid_Vol | GRU | 0.6092 | 0.5263 | 0.5255 |
| Mid_Vol | GRU Ensemble | 0.6283 | 0.5366 | 0.5340 |
| Mid_Vol | LNN Single | 0.5266 | 0.5297 | 0.5172 |
| Mid_Vol | LNN Ensemble | 0.5507 | 0.5233 | 0.5144 |
| Mid_Vol | CFC Single | 0.4749 | 0.5118 | 0.5140 |
| Mid_Vol | CFC Ensemble | 0.5475 | 0.5254 | 0.5271 |
| Mid_Vol | Hybrid_SOTA(L7:R3) | 0.5339 | 0.5089 | 0.5053 |
| Low_Vol | RNN | 0.5151 | 0.4742 | 0.4987 |
| Low_Vol | RNN Ensemble | 0.5294 | 0.4965 | 0.5264 |
| Low_Vol | LSTM | 0.5040 | 0.5083 | 0.5078 |
| Low_Vol | LSTM Ensemble | 0.5200 | 0.5097 | 0.5125 |
| Low_Vol | GRU | 0.4601 | 0.5025 | 0.5062 |
| Low_Vol | GRU Ensemble | 0.4875 | 0.5151 | 0.5167 |
| Low_Vol | LNN Single | 0.6207 | 0.5695 | 0.5358 |
| Low_Vol | LNN Ensemble | 0.5981 | 0.5276 | 0.5322 |
| Low_Vol | CFC Single | 0.5120 | 0.4947 | 0.5003 |
| Low_Vol | CFC Ensemble | 0.5977 | 0.5046 | 0.5100 |
| Low_Vol | Hybrid_SOTA(L7:R3) | 0.5483 | 0.5050 | 0.5182 |


전체6지표99행은 step27_historical_manual_metrics.csv에, HMM6지표66행은 step27_historical_hmm_metrics.csv에 **별도** 보존했다. 소스 Notebook/output hash를 각 행에 남겼다. 모델별·시드별 명시적 슬롯528행은 step27_historical_manual_per_seed.csv에 만들었고 단일33행만 저장값이 있다. 다중495행은 **BLOCKED_PER_SEED_OUTPUT_NOT_STORED**, 값은 null이다. 셀14 실행 로그의 seed/저장소 길이만으로 개별 성능을 복원할 수 없다. 평균을 개별seed 성능으로 복제하지 않았다. HMM의 seed별 슬롯도 별도 파일로 유지한다. 원본 raw predictions/seedmetrics가 제공돼야 완성할 수 있다.

## 새 Rolling-Origin에서 재사용할 부분과 변경 규칙

확률>0.5, 마스크로 같은 date의 정답/예측을 함께 선택,6지표 연결의 원리는 재사용한다. 원본 모델 정의를 변경하지 않는다. 새 src/kospi200/manual_evaluation.py는 원본 Vol_Regime의 **각 Origin에서 purge 후 유지된 Train 기준일**의30/70 분위수(linear)를 참조로 동결하고 Validation/Test에 그대로 적용한다. Test를 보고 임계값 재계산·수동 조정·분위수 변경을 금지한다. q30>=q70이면 해당 레짐 분석 BLOCKED이며 Test median이나 임의 jitter로 구제하지 않는다. 실제 후보 Train 임계값을 이번에 실험용으로 확정하지 않았으며 합성 fixture로 함수만 검증했다.

보고 단위는 Origin/Seed/Model/Regime별 BA·Macro F1·Recall0·Recall1·n·n0·n1이고 manual/HMM 표를 섞지 않는다. 둘 다 있는 경우 BA는두Recall의평균, MacroF1은고정labels[0,1]평균이다. 한 클래스만 있으면 **BA·MacroF1=null, SINGLE_CLASS_NOT_ESTIMABLE**, 해당support와 존재하는 클래스 Recall만 보고하고 없는 클래스Recall=null로 둔다. 빈 레짐은EMPTY·n0·BA/MacroF1=null이다. 빈 레짐을0성능으로 평균하지 않는다. 표준화된 이 정책 때문에 원본 absent-class 출력과 동등하다고 주장하지 않는다. 요약 시 유효 seed수·레짐 표본수·불확실성을 함께 보고하고 seed를 연결해 표본수를 늘리지 않는다.

새 수동 레짐은 과거 trailing feature와 Train 고정 임계값만 사용한다. HMM은 향후 Train-only fit/Train state naming+forward filtering으로 별도 분석하고 Test전체Viterbi·Test분위수·Testmedian fallback을 금지한다. 실제 HMM fit는0회다. 원본은 단일60/20/20, t이전20입력, observed-row horizon·Test 분위수지만 새 사양은5Origin,공식20세션 horizon,purging,t포함window,Train 분위수이므로 원본 성능표와 같은 조건이라고 주장하지 않는다.

## 원본 코드 위치

다음 행번호는 셀 내부1-based이며 source manifest에 대응 원문 구문과 해시가 있다. 전체 원본 source는 공개하지 않는다.

| Notebook | 실제 셀 | 선택 구문 행번호 |
|---|---|---|
| single | 11 | 11, 12, 13, 15, 16, 17, 70, 73, 77, 78, 79 |
| single | 12 | 63, 80, 85 |
| single | 14 | 87 |
| single | 16 | 15, 16, 24, 25, 32, 34 |
| single | 17 | 7, 9 |
| 10seed | 11 | 11, 13, 14, 16, 17, 18, 116, 119, 126 |
| 10seed | 12 | 66, 83, 88 |
| 10seed | 14 | 25, 27, 28, 30, 31, 32, 88, 91, 101, 162, 167, 170, 172, 173, 178, 179, 189 |
| 10seed | 16 | 9, 11 |
| 10seed | 17 | 7, 9 |
| 5seed | 11 | 11, 13, 14, 16, 17, 18, 116, 119, 126 |
| 5seed | 12 | 66, 83, 88 |
| 5seed | 14 | 25, 27, 28, 30, 31, 32, 88, 91, 101, 162, 167, 170, 172, 173, 178, 179, 189 |
| 5seed | 16 | 9, 11 |
| 5seed | 17 | 7, 9 |


검사는72 PASS/0 FAIL이며 합성 정답·예측을 사용한 metric/단일클래스 검사가 포함된다. 실제 연구자료의 새 모델 성능은 계산하지 않았다.
