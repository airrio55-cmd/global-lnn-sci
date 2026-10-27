"""Render figures and report from completed analysis outputs only."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
REG=['Low','Normal','High'];MARKETS=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200']
d=pd.read_csv(OUT/'regime_distribution.csv');b=pd.read_csv(OUT/'regime_best_model_comparison.csv');m=pd.read_csv(OUT/'regime_metrics_all_configs.csv');ci=pd.read_csv(OUT/'regime_bootstrap_ci.csv');con=pd.read_csv(OUT/'hmm_convergence_log.csv');a=pd.read_csv(OUT/'regime_assignments_all_markets.csv')
d['All_test_calendar_share']=d.All_test_calendar_N/d.groupby('Market').All_test_calendar_N.transform('sum');d.to_csv(OUT/'regime_distribution.csv',index=False)
colors=['#3288bd','#fdae61','#d53e4f']
pivot=d.pivot(index='Market',columns='Regime',values='Share').loc[MARKETS,REG]
ax=pivot.plot.bar(stacked=True,color=colors,figsize=(9,5),rot=0);ax.set_ylabel('Share of saved test prediction dates');ax.set_ylim(0,1);ax.set_title('Causal HMM regime distribution (within-market relative states)');ax.legend(title='Regime',bbox_to_anchor=(1.01,1));plt.tight_layout();plt.savefig(OUT/'regime_distribution.png',dpi=180);plt.close()
fig,ax=plt.subplots(figsize=(11,5));width=.24;x=np.arange(5)
for j,r in enumerate(REG):
 z=b[b.Regime==r].set_index('Market').loc[MARKETS];c=ci[ci.Regime==r].set_index('Market').loc[MARKETS];xx=x+(j-1)*width
 ax.bar(xx,z.Delta_BA_vs_Persistence,width,color=colors[j],label=r)
 ax.vlines(xx,c.CI_low,c.CI_high,color='black',lw=1);ax.scatter(xx,c.CI_low,color='black',marker='_',s=25);ax.scatter(xx,c.CI_high,color='black',marker='_',s=25)
ax.axhline(0,color='black',lw=.8);ax.set_xticks(x,MARKETS);ax.set_ylabel('Mean five-seed BA minus Persistence BA');ax.set_title('Frozen Best configuration by causal regime; 95% date-block CI');ax.legend();fig.tight_layout();fig.savefig(OUT/'best_model_delta_ba_by_regime.png',dpi=180);plt.close(fig)
cols=[(market,r) for market in MARKETS for r in REG];architectures=['LNN','LSTM','Transformer'];heat=np.array([[m[(m.Market==market)&(m.Regime==r)&(m.Model==arch)&(m.Loss=='CE')].Delta_BA_vs_Persistence.iloc[0] for market,r in cols] for arch in architectures]);limit=max(.01,float(np.nanmax(np.abs(heat))))
fig,ax=plt.subplots(figsize=(15,4));image=ax.imshow(heat,aspect='auto',cmap='RdBu',vmin=-limit,vmax=limit);ax.set_yticks(range(3),architectures);ax.set_xticks(range(15),[market+'\n'+r for market,r in cols],rotation=45,ha='right');ax.set_title('CE-only architecture comparison: delta BA vs Persistence (no loss selection)')
for i in range(3):
 for j in range(15):ax.text(j,i,f'{heat[i,j]:+.3f}',ha='center',va='center',fontsize=8,color='white' if abs(heat[i,j])>.65*limit else 'black')
fig.colorbar(image,ax=ax,label='Delta BA');fig.tight_layout();fig.savefig(OUT/'architecture_regime_heatmap.png',dpi=180);plt.close(fig)
notes='''# Methodology and limitations

Predictive models, features, thresholds and seed results are read-only. The only fitted objects are the requested explanatory 3-state Gaussian HMMs, monthly expanding, fixed seed 20261028, diag covariance, max 300 iterations, tolerance 1e-4 and min covariance 1e-4. No HMM setting was selected from performance.

Frozen raw Close generates Log_Ret=log(Close).diff and Vol20=rolling(20).std(ddof=1)*sqrt(252), matching the base feature definitions. HMM uses only these two inputs. Scalers fit on pre-month history only. Initial history is 2010–2021 and grows with past test observations; labels never enter HMM fitting.

Every test month refits strictly before its first frozen observation, using history through the previous observed date. Component labels are sorted by posterior-weighted mean original Vol20 over training history only. Training-history smoothing for component interpretation uses no out-of-history data and is not used to assign test regimes. State mappings are market/month specific, not globally comparable volatility bands.

For a target date t, regime uses the filtered state at the most recent frozen observation strictly before t. This is intentionally conservative: target-date Close is not used. Forward recursion log alpha_t = emission_t + logsumexp(log alpha_(t-1) + log transition) normalizes at every step; no full-month Viterbi or backward smoothing is used. Each refit recomputes the past filter under the newly fitted model then streams available observations. Later emissions cannot alter earlier filtered states; prefix invariance is asserted. Refit/model/scaler/mapping use no future-month observations.

Regime assignments cover all frozen 2022–2025 observation dates, whereas primary distribution and metric N use exactly the intersection with saved test predictions. All_test_calendar_N/share are reported separately. Log_Ret/Vol20 summaries refer to the previous-observation classifier inputs, not forward target returns. Positive_label_rate refers to saved 20-observation forecast labels.

All nine fixed model/loss combinations use all five original seeds and original thresholds (probability > threshold). Metrics in regime_metrics_all_configs.csv are arithmetic five-seed metric means plus SD; not majority-vote metrics. Seed rows are retained separately. Persistence is deterministic Close(t)>Close(t-20) and is verified against frozen saved full-test baseline BA. Macro F1 fixes binary labels [0,1], zero_division=0; BA is undefined for a single-class regime and is saved NaN. Empty regimes remain reported, not silently dropped. Best configurations are read unchanged from the completed cross-market statistics file; they were originally selected by test BA, so these are exploratory post-selection comparisons.

Bootstrap: 2000 circular date-block resamples of the complete saved test chronology per market, block length 20 observations fixed to the forecast horizon. Apply the original regime mask after sampling; do not stitch regime-only rows into an artificial continuous series. All five seed predictions, Persistence and labels share the same sampled date indices. Statistic is the arithmetic mean of five seed BAs minus baseline BA. CI is percentile 95%, conditional on the fitted regime labels; HMM is not refit inside bootstrap. Samples with fewer than 20 regime rows or one class are excluded and valid counts are reported. This preserves within-block dependence approximately, not all dependence; circular wrap is an assumption. HMM estimation uncertainty, test-based Best selection and between-market correlation are not included. N<50 or minority class<10 is flagged small. CI exclusion of zero is descriptive, not a multiple-comparison-adjusted significance test. No p-values or confirmatory significance claims are made.

HMM convergence monitor, max-iteration hit, likelihood decrease and warnings are saved per month. A monitor converged flag can also reflect iteration exhaustion; inspect Hit_iteration_limit and Last_gain. Failed fits halt analysis instead of silently changing settings or filling regimes. Monthly state relabeling means realized test averages need not be monotonically ordered Low/Normal/High.

KOSPI200 retains its authorized empirical observation calendar; the 45-day XKRX discrepancy is not confirmed missing KRX observations. Monthly foreign rate forward-fill and all base inputs remain unchanged. Vendor revisions and actual historical release timestamps are not certified. Regime patterns and class-imbalance associations are descriptive and do not establish mechanisms or tradable profitability.
'''
notes += '\n## Reproduction\n\nUse Python and package versions in analysis_manifest.json. Run analyze.py, then report.py with matplotlib installed, then validate.py from repository root. These scripts only read frozen base artifacts. All HMM/CI settings are in hmm_protocol.json; source hashes in analysis_manifest.json.\n'
(OUT/'methodology_notes.md').write_text(notes)
lines=['# Five-market causal HMM regime analysis','','No predictive retraining, tuning, threshold changes, feature changes or regime-based model reselection. SP500 uses reproducible rerun only.','',f'Monthly HMM fits: {len(con)}; iteration-limit hits: {int(con.Hit_iteration_limit.sum())}; negative final likelihood gains: {int(con.Numerical_decrease.sum())}. All 3-state specifications fixed before fitting.','','## Frozen Best configuration by regime','','|Market|Model / Loss|Regime|N|Positive label rate|Delta BA|Delta Macro F1|95% date-block CI|Small sample|','|---|---|---|---:|---:|---:|---:|---|---|']
for r in b.itertuples():
 c=ci[(ci.Market==r.Market)&(ci.Regime==r.Regime)].iloc[0]
 lines.append(f'|{r.Market}|{r.Model} / {r.Loss}|{r.Regime}|{r.N}|{r.Positive_label_rate:.3f}|{r.Delta_BA_vs_Persistence:+.4f}|{r.Delta_Macro_F1_vs_Persistence:+.4f}|[{c.CI_low:+.4f}, {c.CI_high:+.4f}]|{r.Small_sample}|')
lines+=['','## RQ1: Does LNN relative performance vary with regime?','','The following compares each fixed LNN loss separately; no within-regime winner is selected. Values are delta BA vs Persistence in Low / Normal / High order.']
for market in MARKETS:
 for loss in ['CE','MILD_FOCAL','MILD_WCE']:
  z=m[(m.Market==market)&(m.Model=='LNN')&(m.Loss==loss)].set_index('Regime').loc[REG]
  lines.append(f'- {market}, LNN {loss}: '+ ' / '.join(f'{v:+.4f}' for v in z.Delta_BA_vs_Persistence)+'.')
lines+=['','## RQ2–RQ4: Market-specific localization','','Signs below refer to five-seed mean BA differences, not statistical proof.']
for market in MARKETS:
 z=b[b.Market==market].set_index('Regime').loc[REG]
 vals='; '.join(f'{r}: delta BA {z.loc[r,"Delta_BA_vs_Persistence"]:+.4f} (N={int(z.loc[r,"N"])})' for r in REG)
 rq='RQ2' if market in ['NIKKEI225','EUROSTOXX50'] else ('RQ3' if market in ['SP500','NASDAQ100'] else 'RQ4')
 lines.append(f'- {rq}, {market}: {z.Model.iloc[0]} {z.Loss.iloc[0]} — {vals}.')
lines += ['', 'Descriptive localization (not a test of differences between regimes):']
for market in MARKETS:
 z=b[b.Market==market].set_index('Regime').loc[REG]
 valid=z.Delta_BA_vs_Persistence.dropna()
 if valid.empty:
  lines.append(f'- {market}: BA undefined across regimes; no localization claim.');continue
 positive=[r for r in REG if z.loc[r,'Delta_BA_vs_Persistence']>0]
 if market in ['SP500','NASDAQ100']:
  worst=valid.idxmin();lines.append(f'- {market}: strongest Persistence BA advantage is in {worst}, delta BA {valid[worst]:+.4f}; positive Best-model BA deltas occur in {positive or "none"}.')
 else:
  strongest=valid.idxmax();lines.append(f'- {market}: largest fixed Best-model BA delta is in {strongest}, {valid[strongest]:+.4f}; positive deltas occur in {positive or "none"}. Interpret together with regime N, CIs and Macro F1; maximum effect alone is not evidence of concentration.')
lines+=['','## RQ5: BA improvement versus Macro F1 deterioration','','Inspect Positive_label_rate and N in the table together with both deltas. Regimes with improved BA but worse Macro F1:']
flags=b[(b.Delta_BA_vs_Persistence>0)&(b.Delta_Macro_F1_vs_Persistence<0)]
for r in flags.itertuples():lines.append(f'- {r.Market}, {r.Regime}: positive-label share {r.Positive_label_rate:.3f}; delta BA {r.Delta_BA_vs_Persistence:+.4f}; delta Macro F1 {r.Delta_Macro_F1_vs_Persistence:+.4f}; N={r.N}.')
if flags.empty:lines.append('- None among the fixed Best configuration regime means.')
lines+=['','This is an observed association, not proof that imbalance causes the metric disagreement. Balanced accuracy averages class recalls while Macro F1 also depends on precision and prediction prevalence; Pred_Pos_Rate and per-seed metrics are saved for diagnosis.','','## Interpretation limits','','Regimes are within-market, relative and month-remapped. Block CIs are conditional/exploratory, with small-regime flags and no multiple-comparison-adjusted significance claim. Class imbalance, label overlap, post-test Best selection, possible HMM nonconvergence and KOSPI empirical-calendar limitations must accompany any paper claim. See methodology_notes.md for full causal timing and bootstrap specification.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n')
print(b[['Market','Regime','N','Delta_BA_vs_Persistence','Delta_Macro_F1_vs_Persistence']].to_string(index=False))

(OUT/"README.md").write_text((OUT/"results_report.md").read_text())
manifest=json.loads((OUT/"analysis_manifest.json").read_text());manifest["plot_packages"]={n:__import__("importlib.metadata",fromlist=["version"]).version(n) for n in ["matplotlib","pillow"]};(OUT/"analysis_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
