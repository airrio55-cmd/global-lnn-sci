# STEP5C_STATISTICAL_RESULTS_KO

이번 결과는 retrospective rolling-origin statistical analysis다. 가격 A/B는 별도 보고하며 BOTH_UNVERIFIED, historical18:00 available_at UNKNOWN, production-PIT BLOCKED, 주가격 PENDING을 유지한다. 모델/가격/Seed/기간/가설을 결과에 따라 선택하지 않았다. finite-replication 중심화 bootstrap p값은 근사값이며 percentile95%CI는 동시 신뢰구간이 아니다. Seed와 Origin을 독립 시장 반복으로 간주하지 않는다.

기존 학습500개와 Test500개를 보존하고 저장된 예측만 사용했다. 신규 학습/재학습/Test추론/checkpoint load·forward/HMM/RAW5·LOG2 Ensemble/GPU/τactual/2026관측 사용은 모두0이다.

블록20/40/60 각각 가설별10000회 계산 완료. Primary20, Secondary80, Origin-specific100 가설을 각블록에서 평가해 총600개 가설×블록 결과행을 남겼다. 모든9가족에서 Holm 보정을 완료했고 row/family BLOCKED는 0/0다. 무효 재표집은 실제횟수를 보존했으며 최대4/10000(0.04%)로10% 차단기준을 넘지 않았다.

| family | block_length | hypotheses | draws_per_hypothesis | Holm_status | rows_BLOCKED | Holm_approx_p_below_0_05 | invalid_draws_max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| primary | 20 | 20 | 10000 | PASS | 0 | 0 | 0 |
| secondary | 20 | 80 | 10000 | PASS | 0 | 3 | 0 |
| origin | 20 | 100 | 10000 | PASS | 0 | 0 | 0 |
| primary | 40 | 20 | 10000 | PASS | 0 | 0 | 2 |
| secondary | 40 | 80 | 10000 | PASS | 0 | 2 | 2 |
| origin | 40 | 100 | 10000 | PASS | 0 | 0 | 4 |
| primary | 60 | 20 | 10000 | PASS | 0 | 0 | 1 |
| secondary | 60 | 80 | 10000 | PASS | 0 | 3 | 1 |
| origin | 60 | 100 | 10000 | PASS | 0 | 0 | 2 |

Primary BA20가족과 Origin별 BA100진단가족은 세블록 모두 Holm조정p<.05인 가설0개다. **모델 간 BA의 유의한 차이를 입증하지 못했다.** 이는 차이가 없거나 동등성이 입증됐다는 뜻이 아니다.

Secondary에서는 블록20/40/60에서 각각3/2/3행이 Holm조정p<.05였다. 여러블록의 같은가설 반복을 독립 재현횟수로 세지 않으며 유리한 블록을 대표결과로 선택하지 않는다. 전체240행은 Secondary보고서/공개JSON에 모두 제공한다.

| candidate | model_a | model_b | metric | Holm_p_block20 | Holm_p_block40 | Holm_p_block60 |
| --- | --- | --- | --- | --- | --- | --- |
| A | LSTM | CfC | recall0 | 0.0079992 | 0.0320032 | 0.008 |
| A | LSTM | LTC | recall1 | 0.0311969 | 0.0473953 | 0.0157984 |
| A | RNN | CfC | brier | 0.321168 | 0.136786 | 0.0389961 |
| B | LTC | CfC | recall1 | 0.0236976 | 0.070193 | 0.0835916 |

LTC 대 다른모델의 지표별 비교(방향은 동결된 model_a−model_b 그대로 유지)다. Brier는 음수일수록 model_a에 유리하고 나머지 지표는 양수일수록 model_a에 유리하다. 지표 간 우위를 혼동하지 않는다.

| candidate | model_a | model_b | metric | observed_difference | Holm_p_20 | Holm_p_40 | Holm_p_60 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | RNN | LTC | BA | -0.0139892 | 1 | 1 | 1 |
| A | RNN | LTC | macro_f1 | -0.00731278 | 1 | 1 | 1 |
| A | RNN | LTC | brier | 0.00104517 | 1 | 1 | 1 |
| A | RNN | LTC | recall0 | -0.0906727 | 1 | 1 | 1 |
| A | RNN | LTC | recall1 | 0.0626944 | 1 | 1 | 1 |
| A | LSTM | LTC | BA | -0.0143782 | 1 | 1 | 1 |
| A | LSTM | LTC | macro_f1 | 0.0177967 | 1 | 1 | 1 |
| A | LSTM | LTC | brier | -0.00193835 | 1 | 1 | 1 |
| A | LSTM | LTC | recall0 | -0.132834 | 0.227977 | 0.285029 | 0.1554 |
| A | LSTM | LTC | recall1 | 0.104078 | 0.0311969 | 0.0473953 | 0.0157984 |
| A | GRU | LTC | BA | -0.00454236 | 1 | 1 | 1 |
| A | GRU | LTC | macro_f1 | 0.0257494 | 1 | 1 | 1 |
| A | GRU | LTC | brier | 0.00182154 | 1 | 1 | 1 |
| A | GRU | LTC | recall0 | -0.0659348 | 1 | 1 | 1 |
| A | GRU | LTC | recall1 | 0.0568501 | 1 | 1 | 1 |
| A | LTC | CfC | BA | 0.000274796 | 1 | 1 | 1 |
| A | LTC | CfC | macro_f1 | -0.0346788 | 1 | 1 | 1 |
| A | LTC | CfC | brier | 0.00350749 | 1 | 1 | 1 |
| A | LTC | CfC | recall0 | 0.0697304 | 1 | 1 | 0.8004 |
| A | LTC | CfC | recall1 | -0.0691808 | 0.161684 | 0.115488 | 0.0615938 |
| B | RNN | LTC | BA | -0.0111577 | 1 | 1 | 1 |
| B | RNN | LTC | macro_f1 | -0.00503422 | 1 | 1 | 1 |
| B | RNN | LTC | brier | 0.00103137 | 1 | 1 | 1 |
| B | RNN | LTC | recall0 | -0.0796858 | 1 | 1 | 1 |
| B | RNN | LTC | recall1 | 0.0573704 | 1 | 1 | 1 |
| B | LSTM | LTC | BA | -0.0117577 | 1 | 1 | 1 |
| B | LSTM | LTC | macro_f1 | 0.0199076 | 1 | 1 | 1 |
| B | LSTM | LTC | brier | -0.000338153 | 1 | 1 | 1 |
| B | LSTM | LTC | recall0 | -0.0783236 | 1 | 1 | 1 |
| B | LSTM | LTC | recall1 | 0.0548083 | 1 | 1 | 1 |
| B | GRU | LTC | BA | -0.00339564 | 1 | 1 | 1 |
| B | GRU | LTC | macro_f1 | 0.0225775 | 1 | 1 | 1 |
| B | GRU | LTC | brier | 0.00164709 | 1 | 1 | 1 |
| B | GRU | LTC | recall0 | -0.0587167 | 1 | 1 | 1 |
| B | GRU | LTC | recall1 | 0.0519255 | 1 | 1 | 1 |
| B | LTC | CfC | BA | 0.0123732 | 1 | 1 | 1 |
| B | LTC | CfC | macro_f1 | -0.0211976 | 1 | 1 | 1 |
| B | LTC | CfC | brier | -0.00130759 | 1 | 1 | 1 |
| B | LTC | CfC | recall0 | 0.102999 | 0.310769 | 0.386939 | 0.15 |
| B | LTC | CfC | recall1 | -0.0782522 | 0.0236976 | 0.070193 | 0.0835916 |

LTC Test 단일 클래스예측24/100 사례를 제거하지 않았다. A에서 LSTM−LTC Recall1 차이+0.104078은 세블록 모두 Secondary80가족 Holm조정p<.05였으나, LTC BA 우위나 MacroF1/Brier 우위를 뜻하지 않는다. 이미 관찰한 Test결과를 사후 우수Seed/유리한레짐 가족으로 확장하지 않았다.

공개본은 사전 가설의 다중fit 집계·방법·비민감 SHA만 포함한다. 개별 금융일자/Target/확률·민감 identity/SHA매핑·draw벡터·checkpoint·실제scaler/Train임계값은 로컬 비공개로 보존했다.
