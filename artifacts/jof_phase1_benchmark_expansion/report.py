"""Phase1 descriptive comparison, no configuration/rule selection."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
M=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'];ARCH=['LNN','LSTM','Transformer','GRU'];NEW=['GRU','LogisticRegression','LightGBM']
table=pd.read_csv(OUT/'benchmark_comparison_table.csv');non=pd.read_csv(OUT/'nonoverlap_results.csv');pt=pd.read_csv(OUT/'pt_results.csv');econ=pd.read_csv(OUT/'transaction_cost_results.csv');freq=pd.read_csv(OUT/'diagnostics/forecast_frequency.csv');det=pd.read_csv(OUT/'diagnostics/seed_determinism.csv');fr=pd.read_csv(OUT/'neural_architecture_friedman.csv');selection=pd.read_csv(OUT/'selected_configs.csv')
fig,axes=plt.subplots(1,2,figsize=(14,6))
for ax,metric,title in [(axes[0],'Test_BA','Operational representative test BA'),(axes[1],'Forecast_Up_Rate','Forecast Up rate (diagnostic)')]:
 z=table[table.Model.isin(ARCH+['LogisticRegression','LightGBM'])].pivot(index='Market',columns='Model',values=metric).loc[M,ARCH+['LogisticRegression','LightGBM']];z.plot.bar(ax=ax,rot=30,title=title);ax.axhline(.5,color='black',ls='--',lw=.7)
 if metric=='Forecast_Up_Rate':ax.axhline(.1,color='red',ls=':',lw=.7);ax.axhline(.9,color='red',ls=':',lw=.7)
ax=axes[0];ax.set_ylabel('Balanced Accuracy');axes[1].set_ylabel('Proportion');fig.tight_layout();fig.savefig(OUT/'figures/phase1_predictive_and_frequency.png',dpi=180);plt.close(fig)
notes='''# Journal of Forecasting Phase1 methodology

## Frozen experiment and information compatibility
GRU, LogisticRegression and LightGBM are new models, not replacements for existing LNN/LSTM/Transformer. Frozen market-specific COMMON_LOCAL inputs, H20 labels, expanding train/validation2019/2020/2021/test2022–2025, five seeds and original preprocessing/split functions are reused. SP500 uses sp500_rerun only. If a processed feature_input.csv exists it is read byte-for-byte (SP500); otherwise original market-specific feature-engineering code is applied exactly to the existing frozen market_input.csv and saved once. No Yahoo/FRED refresh. Data/code hashes and source availability audits are retained.

Sequence input X[i−20:i] excludes target row. Source StandardScaler fits the purged training date-feature matrix only. Logistic/LightGBM receive precisely the same standardized float32 W20 tensor flattened in C order (oldest timestep to latest, features in original order). The source per-feature StandardScaler is shared across all lags; there is no second per-lag scaler or engineered tabular feature. Fixed column order, scaler parameters, feature snapshots and exact tensors are saved. Label horizons are contained inside each split and test dates/labels match existing frozen LSTM rows.

## Strict validation-first execution
All375 validation fits (225 GRU=3losses*5seeds*3folds*5markets,75 logistic,75 LightGBM) complete before ANY new final model test prediction. GRU candidate loss scores are five-seed means of BA from concatenated2019/2020/2021 validation probabilities at that seed's validation-selected threshold, matching existing WF_Val_BA conventions. Tie: higher mean validation Macro F1, then smaller mean absolute threshold distance from0.5, then lexical loss. One GRU loss per market, never one chosen separately for each test seed. Logistic/LGB have one frozen parameter configuration, with only validation threshold selection. All selection/threshold tables and hashes are locked before the75 final test fits. Resuming reuses matching checkpoints, not retries for improved results.

## Models
GRU is the exact existing RecurrentModel GRU branch, torch.nn.GRU with hidden128, num_layers1, batch_firstTrue, internal dropout0; explicit Dropout0.2 on final timestep, Linear128→2 and original initialization. Existing CE/MILD_WCE/MILD_FOCAL code is reused unmodified. AdamW LR0.005, weight_decay1e-4, OneCycleLR, clip norm1, batch64, max100fold epochs, patience10; final60epochs on data through2021. Train-only scaling and deterministic seed handling match LSTM. EarlyStopping logging wrapper changes reporting only.

LogisticRegression: L2, lbfgs, C1, fit_interceptTrue, class_weightNone, max_iter5000, tol1e-4 and original seed IDs. lbfgs may ignore random_state and identical seed forecasts/metrics are retained, not represented as independent algorithmic variation. Solver warnings/iterations are recorded rather than silently changing settings.

LightGBM: objectivebinary,300estimators, LR0.03,31leaves, depth−1, min_child_samples20, subsample1, colsample1, reg_alpha0, reg_lambda0, no class weights. No early-stopping callback is used;300 rounds are prespecified. random_state/data_random_seed/feature_fraction_seed/bagging_seed/drop_seed/extra_seed all equal the original seed ID. CPU2 threads, deterministicTrue, force_col_wiseTrue are fixed reproducibility settings, not tuned parameters. With full row/column sampling, seed variation may be absent; all five independent run records remain, with exact probability/forecast identity diagnostics.

Thresholds for all learned models use original0.30–0.70 step0.01 validation grid and original sorting: maximum BA, then Macro F1, then closest0.5; remaining numeric-grid tie resolution is the original deterministic implementation. Prediction is strict Probability>Threshold. No threshold, hyperparameter, feature or loss chosen from test results.

## Rules and benchmarks
Primary200DMA uses P_t>mean(P_(t−199)..P_t), inclusive200observations. Optional lag1 diagnostic uses P_(t−1)>MA200_(t−1), separately labeled and excluded from primary ranking. Primary200DMA and Persistence use P_t while neural/tabular sequence models use information through t−1; this information-set difference is explicit. All economic executions are nevertheless next-close, never same-close.

Momentum20=P_t>P_(t−20) is mathematically identical to existing Persistence; equality is verified and no duplicate model/result/ranking is created. The prespecified additional momentum rule is Momentum60=P_t>P_(t−60). No alternate momentum or moving-average window is searched. Always-Up/Down and Persistence retain original definitions. Rule warmup uses frozen pre-test history, not test-driven filling. Existing validation-selected architecture losses are copied unchanged, not reselected.

## Aggregation and comparisons
Every model's five seed results are preserved. Neural representatives are3-of5 strict-threshold majority votes, never averaged probabilities. Logistic/LightGBM identical forecast consensus is equivalent to any one seed; no ensemble gain is claimed. Where seed forecasts vary, the same3-of5 rule is used. The primary benchmark table uses operational representative metrics; Mean_seed_Test_BA is separately supplied. All original sources remain unchanged.

Near-constant forecast is flagged only diagnostically when Up rate<0.10 or>0.90. abs(rate−0.5) and rate−actual Up are saved at seed and representative levels. No model/seed is removed on this basis. Descriptive ranks use operational representative BA/MacroF1/Accuracy, average ties, on11primary models/rules per market. Optional lag1 is not included in primary ranks. Four-neural Friedman uses five-seed mean BA/MacroF1, market blocks5, and LNN/LSTM/Transformer/GRU only; Logistic/LightGBM are separate. Kendall W=statistic/[5*(4−1)]. Five correlated markets limit power; ranks alone do not establish superiority.

## PT and reduced overlap
The existing validated PT function is AST-extracted WITHOUT executing previous scripts, with identical1992 variance formula and explicit constant-forecast undefined handling. PT uses conventional asymptotic reference and does not fully account for overlappingH20 labels. Raw positive one-sided and two-sided p-values are reported; negative PT is not positive skill. Reduced overlap uses row0,20,40,... from the same frozen dates, with no phase search and no redefinition. It lowers mechanical target overlap but does not establish statistical independence; N~47–49 limits power. No final expanded Holm family is defined in Phase1 and old Holm15 is unchanged. A diagnostic gives current15, hypotheticalGRU-only20, and afterPhase2=20+5*k since Phase2architecture list was not supplied. No final significance claim is drawn from unadjusted new-model p-values.

## Economics
All fixed operational model/rule signals use the existing daily single Long/Cash portfolio: signal t, next available close t+1 execution, returns begin t+1→t+2, leverage0/1, cash/RF0. Local-currency index price returns exclude dividends/FX/funding/taxes/tracking/additional slippage. Round-trip0/10/25/50bps correspond to half-cost per entry/exit; first entry and final liquidation charged. Same evaluation dates for all models; stale last prediction carried to final2025close exactly as existing daily protocol. Existing benchmark full net paths are independently reproduced. Costs are stylized implementation proxies, not direct index tradability. Economic point estimates do not establish superiority; no new economic rule or cost is selected.

## Reproducibility
protocol_lock.json predates test evaluation. Exact feature/tensor/scaler data, all125 validation candidate seed probability files,75 final seed probability files, final/fold checkpoints and tabular estimators are retained. New final checkpoint inference and stored metric/threshold agreement are verified. Original tracked artifact hashes, copied source-code/function hashes, package versions and selection hashes are checked before publication. All negative/null outcomes remain. No HMM fitting or final multiplicity-family replacement. This is a benchmark-expansion/evaluation-design analysis, not an attempt to rescue LNN.
'''
(OUT/'methodology_notes.md').write_text(notes)
lines=['# Journal of Forecasting Phase1 frozen benchmark expansion','','All new settings were frozen before test evaluation.375 validation fits and validation-only selection preceded75 final fits. No existing model, prediction, HMM, economic artifact or original Holm15 is replaced.','', '## Validation-selected GRU and tabular configurations', '', '|Market|Model|Selected loss/objective|Mean validation BA|','|---|---|---|---:|']
for r in selection[selection.Origin=='New_Phase1'].itertuples():lines.append(f'|{r.Market}|{r.Model}|{r.Loss}|{r.WF_Val_BA_mean:.6f}|')
lines+=['','## Primary operational benchmark comparison','','Representative BA/Accuracy/MacroF1 use majority or deterministic consensus; five-seed mean BA is separate. No configuration is selected by this table.','', '|Market|Model|Loss|Validation BA|Test BA|Accuracy|Macro F1|Forecast Up|Actual Up|Delta BA vs Persistence|Nonoverlap BA|Economic exposure|10bps CAGR|','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in table.itertuples():lines.append(f'|{r.Market}|{r.Model}|{r.Selected_Loss}|{r.Validation_BA:.6f}|{r.Test_BA:.6f}|{r.Test_Accuracy:.6f}|{r.Macro_F1:.6f}|{r.Forecast_Up_Rate:.3f}|{r.Actual_Up_Rate:.3f}|{r.Delta_BA_vs_Persistence:+.6f}|{r.Nonoverlap_BA:.6f}|{r.Economic_Exposure:.1%}|{r.Economic_CAGR_10bps:.2%}|')
lines+=['','## 1. Does GRU improve the neural benchmark set?','']
for market in M:
 g=table[table.Market==market].set_index('Model');gru=g.loc['GRU','Test_BA'];old=g.loc[['LNN','LSTM','Transformer'],'Test_BA'].max();lines.append(f'- {market}: GRU BA{gru:.6f}; highest existing validation-selected neural representative BA{old:.6f}; difference{gru-old:+.6f}. Descriptive, not reselection.')
lines+=['','## 2–3. Do Logistic and LightGBM outperform deep models?','']
for model in ['LogisticRegression','LightGBM']:
 count=0
 for market in M:
  g=table[table.Market==market].set_index('Model');delta=g.loc[model,'Test_BA']-g.loc[ARCH,'Test_BA'].max();count+=int(delta>0);lines.append(f'- {market} {model}: delta BA vs highest of four fixed neural representatives={delta:+.6f}.')
 lines.append(f'{model} exceeds all four neural representative BAs in{count}/5 markets. This is a descriptive comparison, not statistical superiority or a new winner-selection rule.')
lines+=['','## 4. Do simple rules challenge learned models?','']
for market in M:
 g=table[table.Market==market].set_index('Model');learned=g.loc[ARCH+['LogisticRegression','LightGBM'],'Test_BA'].max();lines.append(f'- {market}:200DMA BA{g.loc["Rule_200DMA","Test_BA"]:.6f}, Momentum60 BA{g.loc["Momentum60","Test_BA"]:.6f}; highest learned representative BA{learned:.6f}. Rules using P_t have more contemporaneous price information than sequence models; lag1 DMA diagnostic is saved separately.')
lines+=['','## 5–6. Forecast-frequency degeneration','']
flags=freq[freq.Model.isin(ARCH+['LogisticRegression','LightGBM'])&freq.Near_constant_forecast]
for r in flags.itertuples():lines.append(f'- {r.Market}, {r.Model}: forecast Up{r.Forecast_Up_Rate:.3f}, actual Up{r.Actual_Up_Rate:.3f}; retained unchanged.')
if flags.empty:lines.append('No learned representative crosses the prespecified near-constant diagnostic cutoffs.')
lines.append('These behaviors occur alongside validation-based threshold selection; this does not isolate thresholding as their cause. Probability learning, class imbalance and calibration can jointly matter. No near-constant case was excluded or retuned.')
for model in ['LogisticRegression','LightGBM']:
 n=int(det[(det.Model==model)&det.Identical_binary_forecasts_all_seeds].shape[0]);lines.append(f'{model}: identical binary predictions across all5seeds in{n}/5 markets; five run records retained and no algorithmic classification seed variability/ensemble gain claimed for those markets.')
lines+=['','## 7–8. PT and reduced-overlap evidence','','PT raw p-values are diagnostic in Phase1; expanded final multiplicity family is deliberately not yet frozen. Conventional PT does not resolve dependence fromH20 label overlap. A nominal positive test does not constitute final multiplicity-robust evidence.','', '|Market|Model|PT|Raw two-sided p|Positive one-sided p|Reduced-overlap BA|Reduced-overlap PT raw p|','|---|---|---:|---:|---:|---:|---:|']
for r in pt[pt.Model.isin(NEW+['Rule_200DMA','Momentum60'])].itertuples():
 z=non[(non.Market==r.Market)&(non.Model==r.Model)].iloc[0];lines.append(f'|{r.Market}|{r.Model}|{r.PT_statistic:.6f}|{r.PT_two_sided_p:.6g}|{r.PT_positive_one_sided_p:.6g}|{z.Balanced_Accuracy:.6f}|{z.PT_raw_p:.6g}|')
lines+=['','The reduced-overlap subset lowers mechanical target overlap but does not establish statistical independence. Sparse cells/constant forecasts are recorded as in the existing PT implementation. No favorable phase is searched.','','## 9. Predictive gains and economics','','All costs0/10/25/50bps are saved; the following uses10bps round trip.','', '|Market|Model|CAGR|Annual vol|Sharpe|MDD|Exposure|One-way trades|Turnover|','|---|---|---:|---:|---:|---:|---:|---:|---:|']
for r in econ[(econ.Round_trip_bps==10)&econ.Model.isin(NEW+['Rule_200DMA','Momentum60'])].itertuples():lines.append(f'|{r.Market}|{r.Model}|{r.CAGR:.2%}|{r.Annualized_volatility:.2%}|{r.Sharpe:.3f}|{r.Maximum_drawdown:.2%}|{r.Exposure:.1%}|{r.Number_of_trades}|{r.Turnover:.1f}|')
disagreement=[]
for market in M:
 g=table[table.Market==market].set_index('Model')
 for model in NEW:
  ba_delta=g.loc[model,'Test_BA']-g.loc['Persistence','Test_BA'];return_delta=g.loc[model,'Economic_CAGR_10bps']-g.loc['Persistence','Economic_CAGR_10bps'];disagreement.append({'Market':market,'Model':model,'Delta_BA_vs_Persistence':ba_delta,'Delta_CAGR_vs_Persistence':return_delta,'BA_positive_CAGR_negative':bool(ba_delta>0 and return_delta<0),'BA_negative_CAGR_positive':bool(ba_delta<0 and return_delta>0)})
pd.DataFrame(disagreement).to_csv(OUT/'diagnostics/predictive_economic_disagreement.csv',index=False)
lines += ['',f'Across15new market-model cases, BA-positive/CAGR-negative mismatches:{sum(r["BA_positive_CAGR_negative"] for r in disagreement)}; BA-negative/CAGR-positive mismatches:{sum(r["BA_negative_CAGR_positive"] for r in disagreement)}. Full differences are retained in diagnostics/predictive_economic_disagreement.csv.']
lines+=['','Predictive BA and return/Sharpe/drawdown need not agree. High exposure can resemble Buy & Hold and does not demonstrate timing skill; low exposure can suppress both risk and opportunity. Economic point estimates have no new confirmatory uncertainty claim in Phase1.','','## Neural-only Friedman and descriptive ranks','']
for r in fr.itertuples():lines.append(f'- {r.Metric}: statistic{r.Friedman_statistic:.6f}, raw p{r.raw_p:.6g}, Kendall W{r.Kendall_W:.6f}, five market blocks/four neural architectures. Logistic/LightGBM excluded from this family.')
near_new=int(freq[freq.Model.isin(NEW)].Near_constant_forecast.sum());sensitivity=0
for market in M:
 g=table[table.Market==market].set_index('Model')
 for model in NEW:
  p=non[(non.Market==market)&(non.Model==model)].iloc[0];sensitivity+=int(np.sign(g.loc[model,'Test_BA']-g.loc['Persistence','Test_BA'])!=np.sign(p.Balanced_Accuracy-non[(non.Market==market)&(non.Model=='Persistence')].Balanced_Accuracy.iloc[0]))
lines += ['',f'New-model near-constant representative cases:{near_new}/15; sign changes of BA advantage vs Persistence under fixed reduced overlap:{sensitivity}/15.']
lines+=['','Five correlated markets give low power. Descriptive per-market and cross-market ranks are saved but do not establish statistical superiority. No final expanded Holm correction replaces the prior15. Phase2architecture membership must be specified/frozen before defining a final family.', '', '## 10. Evaluation-design conclusion', '', 'Phase1 expands the benchmark universe without privileging LNN. The evidence should be interpreted market by market across validation selection, representative-vs-seed metrics, forecast-frequency degeneration, PT assumptions, reduced overlap and cost-adjusted exposure. Simple, neural, tree and rule models are all retained even when unfavorable. Any apparent isolated advantage is descriptive at this phase; neither a high rank nor unadjusted p-value establishes stable cross-market forecasting superiority. The final expanded-universe multiplicity interpretation remains pending Phase2.', '', 'All new settings, unchanged source hashes, independent checkpoint inference, original benchmark economics and momentum equivalence are audited. No existing artifact was overwritten.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n');(OUT/'README.md').write_text((OUT/'results_report.md').read_text())

if near_new or sensitivity:
 with (OUT/'results_report.md').open('a') as f:f.write('\nPhase1 strengthens the evaluation-design motivation in the limited descriptive sense that forecast-frequency degeneration and/or overlap sensitivity remain observable in the expanded benchmark set. It does not strengthen an LNN-superiority claim. Which model leads depends on market, representative metric and baseline; final adjusted inference remains pending.\n')
else:
 with (OUT/'results_report.md').open('a') as f:f.write('\nPhase1 adds benchmark context but does not materially strengthen a degeneration/overlap-instability claim for the new models: these diagnostics show no flagged cases. Positive stability is retained rather than forced into a negative conclusion; final adjusted inference remains pending.\n')
(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
