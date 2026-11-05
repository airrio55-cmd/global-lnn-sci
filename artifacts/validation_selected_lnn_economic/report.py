"""Validation-selected LNN outputs: exposure-aware economic reporting only."""
from pathlib import Path
import json,hashlib
import pandas as pd,numpy as np
from sklearn.metrics import balanced_accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
M=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'];S=['Validation_LNN','Persistence','Buy_Hold','Always_Cash'];R=['Low','Normal','High'];colors=['#2166ac','#ef8a62','#4d9221','#888888']
pf=pd.read_csv(OUT/'performance_summary.csv',float_precision='round_trip');pf['Exposure_category']=np.where(pf.Exposure<.35,'Low',np.where(pf.Exposure<=.70,'Moderate','High'));pf['Exposure_above_90_percent']=pf.Exposure>.90;pf.to_csv(OUT/'performance_summary.csv',index=False,float_format='%.17g')
daily=pd.read_csv(OUT/'daily_strategy_returns.csv',float_precision='round_trip');comp=pd.read_csv(OUT/'benchmark_comparison.csv');ci=pd.read_csv(OUT/'economic_bootstrap_ci.csv');reg=pd.read_csv(OUT/'regime_economic_results.csv');sel=pd.read_csv(OUT/'selected_lnn_configs.csv').set_index('Market');protocol=json.loads((OUT/'economic_protocol.json').read_text())
# These test-based diagnostics are computed only AFTER validation-only selection is frozen.
oldpf=pd.read_csv(ROOT/'artifacts/cross_market_economic/performance_summary.csv');oldbest=pd.read_csv(ROOT/'artifacts/cross_market_statistics/market_best_models.csv').set_index('Market');hmm=pd.read_csv(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv');hmm.Date=pd.to_datetime(hmm.Date)
consistency=[];diagnostic=[];regpredict=[]
for market in M:
 p=pd.read_csv(OUT/(market+'_operational_predictions.csv'));y=p.Y_true.to_numpy(int);votes=p[[f'Seed_{s}_prediction' for s in [42,52,62,72,82]]].to_numpy().T
 meanba=np.mean([balanced_accuracy_score(y,v) for v in votes]);majorityba=balanced_accuracy_score(y,p.LNN_majority_prediction);baseba=balanced_accuracy_score(y,p.Persistence_prediction)
 z=pf[(pf.Market==market)&(pf.Mode=='Daily')].set_index('Strategy');lnn=z.loc['Validation_LNN'];persist=z.loc['Persistence'];bh=z.loc['Buy_Hold'];delta=lnn.CAGR-persist.CAGR
 consistency.append({'Market':market,'Model':'LNN','Loss':sel.loc[market,'Loss'],'LNN_Test_BA':meanba,'Persistence_BA':baseba,'Delta_BA_vs_Persistence':meanba-baseba,'Delta_BA_vs_0_5':meanba-.5,'LNN_Majority_Test_BA':majorityba,'Majority_Delta_BA_vs_Persistence':majorityba-baseba,'LNN_CAGR':lnn.CAGR,'Persistence_CAGR':persist.CAGR,'Buy_Hold_CAGR':bh.CAGR,'LNN_Exposure':lnn.Exposure,'Exposure_category':lnn.Exposure_category,'Delta_CAGR_vs_Persistence':delta,'Delta_CAGR_vs_Buy_Hold':lnn.CAGR-bh.CAGR,'A_BA_better_CAGR_worse':bool(meanba>baseba and delta<0),'B_BA_worse_CAGR_better':bool(meanba<baseba and delta>0),'C_Exposure_above_90_percent':bool(lnn.Exposure>.9),'D_BA_above_0_5':bool(meanba>.5),'A_majority_BA_better_CAGR_worse':bool(majorityba>baseba and delta<0),'B_majority_BA_worse_CAGR_better':bool(majorityba<baseba and delta>0)})
 previous=oldpf[(oldpf.Market==market)&(oldpf.Mode=='Daily')&(oldpf.Strategy=='Best_Model')].iloc[0]
 diagnostic.append({'Market':market,'Previous_Test_Selected_Model':oldbest.loc[market,'Best_Model'],'Previous_Test_Selected_Loss':oldbest.loc[market,'Loss'],'Validation_Selected_Model':'LNN','Validation_Selected_Loss':sel.loc[market,'Loss'],'Previous_CAGR':previous.CAGR,'Validation_Selected_CAGR':lnn.CAGR,'Previous_Sharpe':previous.Sharpe,'Validation_Selected_Sharpe':lnn.Sharpe,'Previous_MDD':previous.Maximum_drawdown,'Validation_Selected_MDD':lnn.Maximum_drawdown,'Previous_Exposure':previous.Exposure,'Validation_Selected_Exposure':lnn.Exposure})
 labels=hmm[hmm.Market==market].set_index('Date').loc[pd.to_datetime(p.Date),'Regime'].to_numpy()
 for state in R:
  mask=labels==state;hasboth=len(np.unique(y[mask]))==2
  mb=np.mean([balanced_accuracy_score(y[mask],v[mask]) for v in votes]) if hasboth else np.nan;pb=balanced_accuracy_score(y[mask],p.Persistence_prediction.to_numpy()[mask]) if hasboth else np.nan
  regpredict.append({'Market':market,'Regime':state,'N':int(mask.sum()),'LNN_mean_seed_BA':mb,'Persistence_BA':pb,'Delta_mean_seed_BA':mb-pb,'Positive_label_rate':y[mask].mean() if mask.any() else np.nan})
pd.DataFrame(consistency).to_csv(OUT/'predictive_economic_consistency.csv',index=False,float_format='%.17g');pd.DataFrame(diagnostic).to_csv(OUT/'validation_vs_previous_test_selected.csv',index=False,float_format='%.17g');pd.DataFrame(regpredict).to_csv(OUT/'regime_predictive_context.csv',index=False,float_format='%.17g')
fig,axes=plt.subplots(3,2,figsize=(13,11));axes=axes.ravel()
for ax,market in zip(axes,M):
 for strategy,col in zip(S,colors):
  z=daily[(daily.Market==market)&(daily.Mode=='Daily')&(daily.Round_trip_bps==10)&(daily.Strategy==strategy)];ax.plot(pd.to_datetime(z.Date),z.Wealth,label=strategy,color=col,lw=1.3)
 ax.set_title(market);ax.set_ylabel('Wealth, initial capital = 1');ax.grid(alpha=.2)
axes[-1].axis('off');axes[-1].legend(*axes[0].get_legend_handles_labels(),loc='center');fig.suptitle('Validation-selected LNN: daily Long/Cash, 10bps round trip');fig.tight_layout();fig.savefig(OUT/'validation_selected_lnn_cumulative_wealth.png',dpi=170);plt.close(fig)
z=pf[pf.Mode=='Daily'].pivot(index='Market',columns='Strategy',values='CAGR').loc[M,S]
ax=(z*100).plot.bar(figsize=(10,5),rot=0,color=colors);ax.axhline(0,color='black',lw=.8);ax.set_ylabel('Net CAGR (%)');ax.set_title('Validation-selected LNN vs fixed benchmarks, 10bps');plt.tight_layout();plt.savefig(OUT/'validation_selected_lnn_cagr_comparison.png',dpi=180);plt.close()
x=pf[(pf.Mode=='Daily')&(pf.Strategy=='Validation_LNN')].set_index('Market').loc[M];fig,ax=plt.subplots(figsize=(10,5));ax.bar(M,x.Exposure*100,color=['#d53e4f' if v>.9 else '#2166ac' for v in x.Exposure]);ax.axhline(90,color='#d53e4f',ls='--',label='90% persistent-exposure warning');ax.axhline(70,color='grey',ls=':',lw=.8);ax.axhline(35,color='grey',ls=':',lw=.8)
for i,v in enumerate(x.Exposure):ax.text(i,v*100+1,f'{v:.1%}',ha='center')
ax.set_ylim(0,108);ax.set_ylabel('Time-long exposure (%)');ax.set_title('Exposure is descriptive; never a selection criterion');ax.legend();fig.tight_layout();fig.savefig(OUT/'validation_selected_lnn_exposure.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,5))
for ax,column,title,mult in [(axes[0],'Delta_mean_return_vs_Persistence','Delta mean net return (bps/day)',10000),(axes[1],'Delta_Sharpe_vs_Persistence','Delta conditional Sharpe',1)]:
 h=reg.pivot(index='Market',columns='Regime',values=column).loc[M,R].to_numpy()*mult;lim=max(.01,np.max(abs(h)));im=ax.imshow(h,cmap='RdBu',vmin=-lim,vmax=lim,aspect='auto');ax.set_xticks(range(3),R);ax.set_yticks(range(5),M);ax.set_title(title)
 for i in range(5):
  for j in range(3):ax.text(j,i,f'{h[i,j]:+.2f}',ha='center',va='center',color='white' if abs(h[i,j])>.65*lim else 'black')
 fig.colorbar(im,ax=ax)
fig.suptitle('Frozen HMM labels: evaluation only, no regime-conditioned signals');fig.tight_layout();fig.savefig(OUT/'validation_selected_lnn_regime_economic.png',dpi=180);plt.close(fig)
# Use the established complete accounting definitions, adding revised selection/exposure context.
base_notes=(ROOT/'artifacts/cross_market_economic/methodology_notes.md').read_text()
notes='''# Validation-selected LNN economic reanalysis

LNN loss selection used only 2019–2021 walk-forward validation BA (WF_Val_BA_mean). The selector reads only Model, Loss and WF_Val_BA_mean columns, filters LNN, and freezes the highest validation mean before opening any seed/test predictions or economic results. All five expected losses were verified. 2022–2025 test outcomes played no role in the computational loss-selection rule; no model, threshold or feature is changed.

This is the replacement for the manuscript's PRIMARY economic TABLE, while economic results remain secondary evaluations of the same validation-selected predictive LNNs. Earlier test-selected economics are preserved, not overwritten. The diagnostic comparison is computed after selection and is never used to alter a configuration. Since this is a manuscript revision after prior test inspection, it is not a new prospectively untouched holdout experiment; removing explicit test-based loss selection does not erase all research-design/post-selection uncertainty.

Operational predictions are five-seed majority votes of each seed's original strict Probability > Threshold labels. LNN_Test_BA in predictive_economic_consistency.csv is the arithmetic five-seed BA mean to align with base predictive tables; operational majority BA and its separate disagreement flags are explicitly included. Main A/B/D flags refer to seed-mean BA; C refers to operational exposure. This avoids conflating mean model metrics with ensemble metrics.

Exposure categories are descriptive only: Low<35%, Moderate35–70% inclusive, High>70%. Exposure>90% is separately flagged and requires persistent-long interpretation. High exposure can make a Long/Cash strategy economically similar to Buy & Hold; it is not evidence of timing skill. Categories never influence loss or signal selection.

Bootstrap intervals represent time-series uncertainty under the specified paired noncircular 20-observation, 2000-resample, seed20261028 block procedure, conditional on saved predictions and realized cost-adjusted paths. No HMM refit or prediction regeneration. Favorable point estimates do not establish economic superiority; no universal LNN-superiority claim is made. Price-index returns are stylized local-currency proxies, not directly investable total-return portfolios. Negative results are retained and may not be used for predictive retuning.

Nikkei differentiation is assessed from exposure below Buy & Hold, Sharpe and/or drawdown, and saved High-regime predictive BA—not assumed in advance. High-regime prediction metrics are on prediction dates; regime economics condition realized return dates after the execution delay, so their date sets are related but not interchangeable.

## Unchanged accounting specification (from previous analysis)

'''+base_notes
# Clarify old diagnostic selection descriptions are not current primary selection rules.
notes=notes.replace('Only existing saved prediction files, fixed model/loss selections and frozen Close histories are used.','Only existing saved prediction files, VALIDATION-selected LNN losses and frozen Close histories are used.')
notes=notes.replace('Best configurations were originally selected on test BA; this post-selection uncertainty, transaction-cost model uncertainty and multiple-market dependence are not covered.','Current LNN losses use validation BA only. Prior research-design choices, transaction-cost model uncertainty and multiple-market dependence are not fully covered.')
notes=notes.replace('No strategy chosen from economic outcomes.','No strategy chosen from economic outcomes.')
notes=notes.replace('Prediction disagreement flags use the majority-vote BA and accuracy of the actually traded signals; five-seed mean BA and its mismatch flags are separately retained. Economic performance uses primary 10bps daily CAGR for A/B and Sharpe or negative MDD deterioration for C. These definitions are fixed and transparent, not cherry-picked alternate economic criteria.','Current requested consistency flags use five-seed mean BA for A/B/D, and exposure>90% for C; operational majority BA is separately shown. This supersedes the previous analysis\'s differently named C flag (accuracy versus Sharpe/MDD). The previous files remain untouched.')
(OUT/'methodology_notes.md').write_text(notes)
lines=['# Validation-selected LNN primary economic reanalysis','','LNN losses were selected ONLY by five-seed mean 2019–2021 WF validation BA. 2022–2025 test outcomes were not used by the selection rule. All expected selections matched before any economic calculations. No predictive model/threshold/feature changes or HMM fitting. This folder replaces the manuscript primary economic table; all previous artifacts remain unchanged.','','## Validation-only selection','','|Market|Model|Loss|WF validation BA mean|','|---|---|---|---:|']
for market in M:lines.append(f'|{market}|LNN|{sel.loc[market,"Loss"]}|{sel.loc[market,"WF_Val_BA_mean"]:.6f}|')
lines+=['','## Primary daily net results (10bps round trip)','','|Market|Strategy|CAGR|Sharpe|MDD|Exposure|Category|','|---|---|---:|---:|---:|---:|---|']
for market in M:
 for strategy in S:
  r=pf[(pf.Market==market)&(pf.Mode=='Daily')&(pf.Strategy==strategy)].iloc[0];lines.append(f'|{market}|{strategy}|{r.CAGR:.2%}|{r.Sharpe:.3f}|{r.Maximum_drawdown:.2%}|{r.Exposure:.1%}|{r.Exposure_category}|')
lines+=['','## Exposure-aware interpretation and benchmark differences','']
for market in M:
 z=pf[(pf.Market==market)&(pf.Mode=='Daily')].set_index('Strategy');r=z.loc['Validation_LNN'];d=comp[(comp.Market==market)&(comp.Mode=='Daily')&(comp.Round_trip_bps==10)].set_index('Benchmark')
 lines.append(f'- {market}: LNN exposure {r.Exposure:.1%} ({r.Exposure_category}); delta CAGR vs Persistence {d.loc["Persistence","Delta_CAGR"]:+.2%}, vs Buy & Hold {d.loc["Buy_Hold","Delta_CAGR"]:+.2%}; delta Sharpe vs Persistence {d.loc["Persistence","Delta_Sharpe"]:+.3f}, vs Buy & Hold {d.loc["Buy_Hold","Delta_Sharpe"]:+.3f}.')
 if r.Exposure>.9:lines.append(f'  **{market}: exposure exceeds90%. Economic performance is substantially influenced by persistent market exposure and may resemble a long-heavy strategy. Favorable strategy performance is partly attributable to persistent long exposure and therefore should not be interpreted as strong evidence of timing skill.**')
 elif market in ['EUROSTOXX50','KOSPI200'] and r.Exposure>.7:lines.append(f'  {market}: exposure is high but below90%; favorable performance is partly attributable to persistent long exposure and should not be treated as strong evidence of timing skill.')
ni=pf[(pf.Market=='NIKKEI225')&(pf.Mode=='Daily')].set_index('Strategy');nip=pd.DataFrame(regpredict);hi=nip[(nip.Market=='NIKKEI225')&(nip.Regime=='High')].iloc[0];informative=ni.loc['Validation_LNN','Exposure']<.9 and (ni.loc['Validation_LNN','Sharpe']>ni.loc['Buy_Hold','Sharpe'] or ni.loc['Validation_LNN','Maximum_drawdown']>ni.loc['Buy_Hold','Maximum_drawdown']) and hi.Delta_mean_seed_BA>0
lines+=['','## Nikkei225 differentiated case','',f'Nikkei LNN exposure {ni.loc["Validation_LNN","Exposure"]:.1%} versus Buy & Hold {ni.loc["Buy_Hold","Exposure"]:.1%}; Sharpe {ni.loc["Validation_LNN","Sharpe"]:.3f} versus {ni.loc["Buy_Hold","Sharpe"]:.3f}; MDD {ni.loc["Validation_LNN","Maximum_drawdown"]:.2%} versus {ni.loc["Buy_Hold","Maximum_drawdown"]:.2%}; High-regime mean predictive BA delta vs Persistence {hi.Delta_mean_seed_BA:+.6f}.']
if informative:lines.append('These descriptive results support Nikkei225 as the strongest economically differentiated LNN case in this reanalysis: low exposure and drawdown protection with retained High-regime predictive advantage. This does not establish higher returns, universal superiority, or statistically supported timing skill.')
else:lines.append('The prespecified differentiated-case conditions are not all supported; Nikkei225 should not be elevated to that interpretation.')
lines+=['','## Predictive–economic consistency','','Test BA below is the five-seed mean; operational majority BA is separately stored.','', '|Market|LNN mean BA|Persistence BA|Delta BA|Delta vs0.5|LNN CAGR|Persistence CAGR|Buy & Hold CAGR|A|B|C>90%|D>0.5|','|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|']
for z in pd.DataFrame(consistency).itertuples():lines.append(f'|{z.Market}|{z.LNN_Test_BA:.6f}|{z.Persistence_BA:.6f}|{z.Delta_BA_vs_Persistence:+.6f}|{z.Delta_BA_vs_0_5:+.6f}|{z.LNN_CAGR:.2%}|{z.Persistence_CAGR:.2%}|{z.Buy_Hold_CAGR:.2%}|{z.A_BA_better_CAGR_worse}|{z.B_BA_worse_CAGR_better}|{z.C_Exposure_above_90_percent}|{z.D_BA_above_0_5}|')
lines+=['','## Nonoverlap20 robustness (same first phase and10bps costs)','','|Market|LNN CAGR|Persistence CAGR|Buy & Hold CAGR|LNN Sharpe|Persistence Sharpe|Buy & Hold Sharpe|LNN MDD|LNN exposure|','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for market in M:
 z=pf[(pf.Market==market)&(pf.Mode=='Nonoverlap20')].set_index('Strategy');a=z.loc['Validation_LNN'];p=z.loc['Persistence'];bh=z.loc['Buy_Hold'];lines.append(f'|{market}|{a.CAGR:.2%}|{p.CAGR:.2%}|{bh.CAGR:.2%}|{a.Sharpe:.3f}|{p.Sharpe:.3f}|{bh.Sharpe:.3f}|{a.Maximum_drawdown:.2%}|{a.Exposure:.1%}|')
lines+=['','## Frozen HMM regime economic evaluation','','No regime changes signals. Conditional annualized returns are not stand-alone regime-timing CAGR.','', '|Market|Regime|N|Mean net return|Conditional annualized return|Sharpe|Exposure|Delta mean vs Persistence|Delta Sharpe vs Persistence|Delta mean vs Buy & Hold|Delta Sharpe vs Buy & Hold|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in reg.itertuples():lines.append(f'|{r.Market}|{r.Regime}|{r.N}|{r.Mean_strategy_return:.6f}|{r.Conditional_annualized_return:.2%}|{r.Sharpe:.3f}|{r.Exposure:.1%}|{r.Delta_mean_return_vs_Persistence:+.6f}|{r.Delta_Sharpe_vs_Persistence:+.3f}|{r.Delta_mean_return_vs_Buy_Hold:+.6f}|{r.Delta_Sharpe_vs_Buy_Hold:+.3f}|')
lines+=['','## Paired moving-block uncertainty','','20 observations,2000 resamples, seed20261028; no HMM refit or prediction regeneration. Intervals represent time-series uncertainty under this specified conditional block procedure.','', '|Market|Comparator|Metric|Estimate|95% CI|','|---|---|---|---:|---|']
for r in ci.itertuples():lines.append(f'|{r.Market}|{r.Benchmark}|{r.Metric}|{r.Estimate:+.6f}|[{r.CI_low:+.6f}, {r.CI_high:+.6f}]|')
cagr_ci=ci[ci.Metric=='Delta_CAGR']
lines += ['', f'All {len(cagr_ci)} primary CAGR-difference intervals include zero: {bool(((cagr_ci.CI_low<=0)&(cagr_ci.CI_high>=0)).all())}. Positive net point estimates therefore do not establish economic superiority under this bootstrap.', '']
lines+=['','## Diagnostic comparison with previous test-selected economics','','Computed only after validation selections and new results are frozen; not used for selection.','', '|Market|Previous model/loss|New LNN loss|Previous CAGR|New CAGR|Previous exposure|New exposure|','|---|---|---|---:|---:|---:|---:|']
for r in pd.DataFrame(diagnostic).itertuples():lines.append(f'|{r.Market}|{r.Previous_Test_Selected_Model}/{r.Previous_Test_Selected_Loss}|{r.Validation_Selected_Loss}|{r.Previous_CAGR:.2%}|{r.Validation_Selected_CAGR:.2%}|{r.Previous_Exposure:.1%}|{r.Validation_Selected_Exposure:.1%}|')
lines+=['','## Revised manuscript conclusion','','The methodological basis is stronger because the economic configuration rule is validation-only and LNN-specific. The substantive conclusion is **different and narrower**, not universal LNN superiority: U.S. negative/weak results remain, Nikkei offers differentiated low-exposure drawdown behavior, and favorable European/Korean results require persistent-long exposure interpretation. The comparison also changes architecture in NASDAQ100 and KOSPI200, so differences cannot be attributed to validation-vs-test loss selection alone.', '', 'Economic outcomes remain secondary evaluations of the same saved validation-selected predictions. Favorable point estimates do not establish economic superiority; consult intervals for each comparison rather than interpreting a positive estimate as significance. Price-index returns are stylized, local-currency proxies, not directly investable total-return portfolios. High exposure can make Long/Cash similar to Buy & Hold. Negative results are retained; none may be used for retuning. This retrospective reanalysis does not create a new untouched test set.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n');(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
manifest=json.loads((OUT/'analysis_manifest.json').read_text());manifest['diagnostic_only_inputs_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'artifacts/cross_market_statistics/market_best_models.csv',ROOT/'artifacts/cross_market_economic/performance_summary.csv']};manifest['LNN_Test_BA_definition']='Five-seed mean; majority-vote BA separately included';(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(pd.DataFrame(consistency)[['Market','Loss','LNN_Test_BA','LNN_CAGR','LNN_Exposure','Exposure_category']].to_string(index=False))
