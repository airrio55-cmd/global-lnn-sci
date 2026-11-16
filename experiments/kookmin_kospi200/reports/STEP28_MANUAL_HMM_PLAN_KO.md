# STEP2.8 수동 레짐 / HMM 평가 계획

확인일 2026-11-16. STEP27_MANUAL_REGIME_AUDIT_KO.md를 기준으로 고정한다. 기존 수동99행/HMM66행 저장 성능표와 다중seed 개별값 미보유495칸은 수정하지 않는다. 이번 단계 새 실제 모델 성능은0개다.

## 수동 레짐

Log_Ret=ln(C/C.shift1); Vol_Regime=Log_Ret.rolling(40).std(ddof1). 각 Origin의 purge후 유지Train 기준일(기존 공통window 마스크)에서30/70분위수(linear)를 결정한다. Low<=q30, Mid는q30<x<q70, High>=q70으로 고정한다. q30>=q70이면분석BLOCKED이며 Testmedian/jitter로 대체하지 않는다. Validation/Test에서 참조를 재계산하거나 Test 성능을 보고 임계값을 조정하지 않는다.

A/B별 Train 참조를 민감도 진단으로 계산했으며 최종 자료 선택 후 해당 참조·자료해시를 동결한다. A/B중유리한Test레짐 표를 보고 자료나참조를 고르지 않는다. 미래 관측을 바꿔도 과거피처/Train참조가 바뀌지 않는지 검사했다.

## HMM 계획 (fit 미실행)

2-state GaussianHMM/full covariance, Train-only fit/scaler, 후보[2,12,22,32,42,52,62,72,82,92], n_iter2000/tol1e-4/min_covar1e-4를 기존사양 그대로 쓴다. 후보 선택은Train log likelihood만, 같은사전후보 집합을모든Origin에 적용한다. 신경망 seed와별개로Origin별 fit결과를 cache해 동일 예측에 적용한다.

Train 상태별 평균Vol_Regime으로 낮은/높은변동성 명칭을고정한다. Validation→Test에서직전filtered posterior를 이어받는forward filtering p(z_t|x_<=t)가기본이다. Test 전체 Viterbi·smoothing을실시간상태로 쓰지 않는다. fit실패/수렴실패/상태 붕괴는실패로기록하고Testmedian이나임의분할로대체하지 않는다. Test에서한상태만관측된것과Train 모델상태 붕괴의원인은분리진단하며임의 구제하지 않는다.

## 공통 평가 인터페이스

src/kospi200/paired_regime_evaluation.py의 evaluate_same_predictions는Origin/Seed/Model/date로키를가진**동일한 저장 확률**을받는다. manual과HMM은Origin/date유일키map으로각각결합하며날짜가누락되면차단한다. 모델별>0.5분류를동일하게적용하고두 결과표를별도반환한다. Train-only/forward/가용성provenance가없으면차단한다. 이인터페이스가실제PIT증빙을대신하지는않는다.

각 표는Balanced Accuracy, MacroF1, Recall0/Recall1, n/n0/n1을Origin/Seed/Model/Regime단위로보고한다. BA=(Recall0+Recall1)/2, MacroF1은고정labels[0,1]평균이다. 한클래스레짐은BA/MacroF1=null·SINGLE_CLASS_NOT_ESTIMABLE, 존재클래스Recall과support만보고한다. 빈레짐은EMPTY·n0·두지표null이다. seed별날짜를연결해독립표본수를늘리지않으며수동/HMM표도합치지않는다.

실제 예측값은생성/로드하지않았다. 평가함수와HMM필터는합성fixture로만검사했다. 신경망학습과HMM fit는계속비활성이다. HMM계획이준비됐다는판정은HMM fit/실증평가를승인한다는뜻이아니다.
