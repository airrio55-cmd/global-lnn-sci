"""Fixed transfer outputs to figures/report; no fitting or source selection."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
M=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'];R=['Low','Normal','High']
c=pd.read_csv(OUT/'transfer_comparison.csv').set_index('Market').loc[M];ci=pd.read_csv(OUT/'transfer_bootstrap_ci.csv');mc=pd.read_csv(OUT/'transfer_mcnemar.csv');reg=pd.read_csv(OUT/'regime_transfer_results.csv');econ=pd.read_csv(OUT/'transfer_economic_comparison.csv')
fig,ax=plt.subplots(figsize=(10,5));x=np.arange(5);z=ci[ci.Metric=='Balanced_Accuracy'].set_index('Market').loc[M];ax.bar(x,c.Mean_Delta_BA,color=['#2166ac' if v>=0 else '#b2182b' for v in c.Mean_Delta_BA]);ax.vlines(x,z.CI_low,z.CI_high,color='black');ax.scatter(x,z.CI_low,marker='_',color='black');ax.scatter(x,z.CI_high,marker='_',color='black');ax.axhline(0,color='black',lw=.8);ax.set_xticks(x,M);ax.set_ylabel('Mean BA Transfer − Scratch');ax.set_title('TRANSFER_COMMON LNN CE; 95% conditional seed-bootstrap CI');fig.tight_layout();fig.savefig(OUT/'transfer_delta_ba_by_market.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5));ax.bar(x-.18,c.Scratch_Balanced_Accuracy_mean,.36,label='Scratch',color='#999999');ax.bar(x+.18,c.Transfer_Balanced_Accuracy_mean,.36,label='Transfer',color='#2166ac');ax.axhline(.5,color='black',ls='--',lw=.8);ax.set_xticks(x,M);ax.set_ylabel('Five-seed mean test BA');ax.legend();ax.set_title('Same features, architecture and target optimization; initialization differs');fig.tight_layout();fig.savefig(OUT/'scratch_vs_transfer.png',dpi=180);plt.close(fig)
h=reg.pivot(index='Market',columns='Regime',values='Delta_BA').loc[M,R].to_numpy();lim=max(.01,float(np.nanmax(abs(h))));fig,ax=plt.subplots(figsize=(7,5));im=ax.imshow(h,cmap='RdBu',vmin=-lim,vmax=lim,aspect='auto');ax.set_xticks(range(3),R);ax.set_yticks(range(5),M)
for i in range(5):
 for j in range(3):ax.text(j,i,f'{h[i,j]:+.3f}',ha='center',va='center',color='white' if abs(h[i,j])>.65*lim else 'black')
ax.set_title('Exploratory regime delta BA: Transfer − Scratch');fig.colorbar(im,ax=ax);fig.tight_layout();fig.savefig(OUT/'transfer_regime_heatmap.png',dpi=180);plt.close(fig)
notes='''# Transfer methodology

This is a new TRANSFER_COMMON five-feature experiment, not a rerun of COMMON_LOCAL. Both Scratch and Transfer use original LNN/LTC architecture, hidden128, dropout0.2, one-layer recurrent design, CE, lookback/horizon20 and seeds42/52/62/72/82. No LSTM/Transformer transfer, loss search, local features, source reselection or target-specific tuning.

## Only initialization differs in target optimization
Both target methods use the same AdamW (weight_decay1e-4), OneCycleLR max_lr0.001 (fixed at one-fifth of pretraining LR0.005), batch64, gradient norm clip1, max100 epochs and patience10 in each walk-forward fit, with target validation BA at fixed0.5 for early stopping as in the original code. Final target fit uses fixed60 epochs through2021 without test early stopping. Both use identical seed-driven DataLoader and dropout RNG initialization. Scratch starts from original random initialization; Transfer loads ALL source-pretrained parameters, including classification head; no layer freezing/head search. Source pretraining differs by design; the target optimizer/budget is identical.

## Causal source cutoff
For each target, exclude that market entirely from pooled source fitting AND source validation. Four separate pretraining states per seed use cutoffs2018,2019,2020,2021. For cutoff C, source gradient training uses data through C−1 and internal validation is year C, with both partitions purged by20 observation labels and sequences generated within partitions. Source scalers fit only source gradient-training partition. Select best equal-market-average source validation BA at fixed0.5, max100 epochs, patience10. No target validation or test influences pretraining early stopping.

The cutoff2018 pretraining initializes target train<=2018/val2019; cutoff2019 initializes val2020; cutoff2020 initializes val2021. Only final target fit uses cutoff2021 pretraining. This is stricter than blindly reusing a through2021 pretrained state for earlier target validation folds, which would leak future cross-market information into threshold selection. Final source2021 serves internal validation, not source gradients. All source use is within2010–2021; no source2022–2025 observation enters any fit/scaler/early stopping.

## Balanced source batching
Each64-example minibatch contains exactly16 examples from each of four sources. Independent market permutations cycle/reshuffle smaller sources. Epoch steps=ceil(maximum source sample count/16); no market identity is supplied as a predictive feature. AdamW and OneCycleLR use max_lr0.005, fixed100 max epochs, patience10 and CE. Batch construction is preregistered, not selected on target results.

## Inputs, scaling and thresholds
Original frozen market Close histories generate exactly Log_Ret, Vol20, Momentum20, Disparity20 and RSI14 with original definitions. Every scaler is separate by market/role/cutoff and uses gradient training only. Target fold scaler fits that fold's target training rows; final scaler fits target2010–2021. Label horizon is purged at every boundary; input X[i−20:i] excludes target row. Future raw feature perturbation invariance and label end-date containment are asserted. KOSPI retains authorized empirical observation calendar; all other data limitations of base frozen inputs remain.

Target thresholds for each method/seed are selected from concatenated target2019/2020/2021 validation probabilities using original41-point0.30–0.70 grid and original selection/tie rules. Thresholds may legitimately differ across methods, since the PROCEDURE, not a numeric threshold, is fixed. Test predictions use frozen selected thresholds. Source validation thresholds are not tuned.

## Saved state and resume
100 source-pretraining states,150 target-fold states and50 final target states are stored with protocol hash; source curves, scalers, validation probabilities and final test probabilities/labels are saved. Five exact scaled test tensor packs support independent checkpoint inference verification. Resuming skips completed hash-matching jobs and does not rerun to improve outcomes. Test metrics never control model fitting, hyperparameters or source choice. Exact numeric reruns can still depend on environment; package/code/input hashes are recorded.

## Inference and limitations
Paired seed statistics use Transfer−Scratch BA and Macro F1 differences,10000 conditional seed bootstrap resamples, fixed seed20261028, exact two-sided Wilcoxon. Five-market Holm is applied separately to each metric; joint10 adjustment is also saved. Five seeds share the same test history; CI measures initialization variation, not independent market-history uncertainty. The smallest two-sided Wilcoxon p with five nonzero differences is0.0625. Majority votes use all five seeds with their own validation-selected thresholds; one McNemar per market, primary p=max(exact,continuity-corrected), Holm across five. McNemar tests accuracy, not BA; serial dependence and overlapping20-observation targets make nominal p-values exploratory.

Transfer-positive=mean Delta BA>0. Robust transfer-positive=at least4/5 positive seed BA deltas. Metric-consistent=mean Delta BA>0 AND mean Delta Macro F1>0. These are separate prespecified descriptors, not significance claims. Negative mean Delta BA is explicitly negative transfer.

Regime labels are reused unchanged from existing causal HMM; no HMM fitting or regime-based reselection. Regime metrics average five seed metrics, not majority-vote metrics. Small N and class imbalance limit interpretation; no formal regime significance tests. Economic robustness is computed ONLY for markets with positive mean Delta BA, as prespecified, using existing daily majority-vote Long/Cash protocol: signal t, next-close execution, earn returns from following interval, binary leverage<=1, cash0,10bps round trip (5bps each side), final liquidation, last signal carried through2025. This positive-market selection makes economic results secondary/exploratory; no new rules/costs.

LOMO pooled results cannot isolate a US→non-US mechanism or specifically Japan/Europe→Korea attribution: sources are pooled. No post-hoc source ablation is used to manufacture an attribution. Transfer/scratch budget matching is at the target stage; Transfer has additional source training by design. No economic or predictive success is guaranteed, and all negative results are reported unchanged.
'''
(OUT/'methodology_notes.md').write_text(notes)
lines=['# Leave-one-market-out LNN representation transfer','','New TRANSFER_COMMON experiment, not directly identical to COMMON_LOCAL base models. Fixed CE-only LNN, paired target training0.001 LR, identical budgets; initialization is the target-stage difference. Sources/folds/cutoffs fixed before training.','','## RQ11–RQ12: Paired transfer and negative transfer','','|Target|Scratch BA|Transfer BA|Mean delta BA|Delta Macro F1|Positive seeds|Transfer-positive|Robust-positive|Metric-consistent|Negative transfer|','|---|---:|---:|---:|---:|---:|---|---|---|---|']
for market,r in c.iterrows():lines.append(f'|{market}|{r.Scratch_Balanced_Accuracy_mean:.6f}|{r.Transfer_Balanced_Accuracy_mean:.6f}|{r.Mean_Delta_BA:+.6f}|{r.Mean_Delta_Macro_F1:+.6f}|{r.Seeds_positive_BA}/5|{r.Transfer_positive}|{r.Robust_transfer_positive}|{r.Metric_consistent_transfer}|{r.Negative_transfer}|')
lines+=['','## Seed uncertainty and majority-vote McNemar','','All tests are exploratory, two-sided alpha0.05. Seed CIs do not represent independent market histories; McNemar tests accuracy and assumes independent pairs despite overlapping labels.','', '|Target|Metric|95% seed-bootstrap CI|Wilcoxon raw p|Holm5 p|Holm10 p|','|---|---|---|---:|---:|---:|']
for r in ci.itertuples():lines.append(f'|{r.Market}|{r.Metric}|[{r.CI_low:+.6f}, {r.CI_high:+.6f}]|{r.raw_p:.6g}|{r.Holm_p:.6g}|{r.Holm_joint10_p:.6g}|')
lines+=['','|Target|Majority accuracy delta|McNemar primary p|Holm p|','|---|---:|---:|---:|']
for r in mc.itertuples():lines.append(f'|{r.Market}|{r.Accuracy_delta:+.6f}|{r.raw_p:.6g}|{r.Holm_p:.6g}|')
lines+=['','## RQ13: Exploratory regime dependence','','Frozen HMM labels are used unchanged. No classifier is selected by regime.','', '|Target|Regime|N|Delta BA|Delta Macro F1|','|---|---|---:|---:|---:|']
for r in reg.itertuples():lines.append(f'|{r.Market}|{r.Regime}|{r.N}|{r.Delta_BA:+.6f}|{r.Delta_Macro_F1:+.6f}|')
lines+=['','Prespecified focus regions:']
for market,state in [('NIKKEI225','High'),('EUROSTOXX50','High'),('KOSPI200','Low')]:
 z=reg[(reg.Market==market)&(reg.Regime==state)].iloc[0];lines.append(f'- {market} {state}: delta BA {z.Delta_BA:+.6f}, delta Macro F1 {z.Delta_Macro_F1:+.6f}, N={z.N}; exploratory, not evidence for a retuned model.')
lines+=['','## RQ14: Secondary economics in prespecified BA-positive markets','','No rules or costs changed: primary daily next-close Long/Cash at10bps round trip. Markets with nonpositive mean Delta BA are excluded by design and are not silently reclassified.','', '|Target|Delta CAGR|Delta Sharpe|Delta MDD|','|---|---:|---:|---:|']
for r in econ.itertuples():lines.append(f'|{r.Market}|{r.Delta_CAGR:+.6f}|{r.Delta_Sharpe:+.6f}|{r.Delta_MDD:+.6f}|')
if econ.empty:lines.append('|No BA-positive targets|NA|NA|NA|')
lines+=['','Pooled LOMO transfer can test target benefit but cannot isolate US vs foreign source contributions or Japan/Europe-to-Korea mechanisms. Negative transfer is a substantive result, not hidden. Feature compatibility is controlled by new Scratch baselines; no claim that these are identical feature experiments to archived COMMON_LOCAL results. See methodology_notes.md and transfer_protocol.json for frozen cutoffs, scaler/label audits, budgets and limits.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n');(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
