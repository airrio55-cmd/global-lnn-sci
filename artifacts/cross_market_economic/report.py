from pathlib import Path
import json
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
M=['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200'];S=['Best_Model','Persistence','Buy_Hold','Always_Cash'];R=['Low','Normal','High'];colors=['#2166ac','#ef8a62','#4d9221','#888888']
daily=pd.read_csv(OUT/'daily_strategy_returns.csv');perf=pd.read_csv(OUT/'performance_summary.csv');cost=pd.read_csv(OUT/'transaction_cost_sensitivity.csv');comp=pd.read_csv(OUT/'benchmark_comparison.csv');reg=pd.read_csv(OUT/'regime_economic_results.csv');boot=pd.read_csv(OUT/'economic_bootstrap_ci.csv');dis=pd.read_csv(OUT/'predictive_economic_disagreement.csv')
# Record both majority-vote BA (actual traded prediction) and five-seed mean BA mismatch flags.
dis['A_mean_BA_better_CAGR_worse']=(dis.Five_seed_mean_BA_delta_vs_Persistence>0)&(dis.Delta_CAGR<0)
dis['B_mean_BA_worse_CAGR_better']=(dis.Five_seed_mean_BA_delta_vs_Persistence<0)&(dis.Delta_CAGR>0)
dis.to_csv(OUT/'predictive_economic_disagreement.csv',index=False)
fig,axes=plt.subplots(3,2,figsize=(13,11));axes=axes.ravel()
for ax,market in zip(axes,M):
 for strategy,col in zip(S,colors):
  z=daily[(daily.Market==market)&(daily.Mode=='Daily')&(daily.Round_trip_bps==10)&(daily.Strategy==strategy)]
  ax.plot(pd.to_datetime(z.Date),z.Wealth,label=strategy,color=col,lw=1.3)
 ax.set_title(market);ax.set_ylabel('Wealth, initial capital = 1');ax.grid(alpha=.2)
axes[-1].axis('off');axes[-1].legend(*axes[0].get_legend_handles_labels(),loc='center');fig.suptitle('Daily Long/Cash, 10 bps round trip, next-close execution');fig.tight_layout();fig.savefig(OUT/'cumulative_wealth_by_market.png',dpi=170);plt.close(fig)
z=perf[perf.Mode=='Daily'].pivot(index='Market',columns='Strategy',values='Sharpe').loc[M,S[:3]]
ax=z.plot.bar(figsize=(10,5),rot=0,color=colors[:3]);ax.axhline(0,color='black',lw=.7);ax.set_ylabel('Annualized Sharpe, RF = 0');ax.set_title('Primary cost-adjusted strategies (cash Sharpe undefined)');plt.tight_layout();plt.savefig(OUT/'sharpe_comparison.png',dpi=180);plt.close()
fig,axes=plt.subplots(3,2,figsize=(12,10));axes=axes.ravel()
for ax,market in zip(axes,M):
 for strategy,col in zip(S[:3],colors[:3]):
  z=cost[(cost.Market==market)&(cost.Mode=='Daily')&(cost.Strategy==strategy)].sort_values('Round_trip_bps')
  ax.plot(z.Round_trip_bps,100*z.CAGR,marker='o',label=strategy,color=col)
 ax.set_title(market);ax.set_xlabel('Round-trip bps');ax.set_ylabel('CAGR (%)');ax.grid(alpha=.2)
axes[-1].axis('off');axes[-1].legend(*axes[0].get_legend_handles_labels(),loc='center');fig.suptitle('Fixed signal cost sensitivity; no signal optimization');fig.tight_layout();fig.savefig(OUT/'transaction_cost_sensitivity.png',dpi=170);plt.close(fig)
h=reg.pivot(index='Market',columns='Regime',values='Delta_mean_return_vs_Persistence').loc[M,R].to_numpy()*10000;lim=max(.1,np.abs(h).max());fig,ax=plt.subplots(figsize=(7,5));im=ax.imshow(h,cmap='RdBu',vmin=-lim,vmax=lim,aspect='auto');ax.set_xticks(range(3),R);ax.set_yticks(range(5),M)
for i in range(5):
 for j in range(3):ax.text(j,i,f'{h[i,j]:+.2f}',ha='center',va='center',color='white' if abs(h[i,j])>.65*lim else 'black')
ax.set_title('Primary daily strategy delta net mean return vs Persistence');fig.colorbar(im,ax=ax,label='bps per regime date');fig.tight_layout();fig.savefig(OUT/'regime_economic_heatmap.png',dpi=180);plt.close(fig)
notes='''# Methodology and interpretation limits

Only existing saved prediction files, fixed model/loss selections and frozen Close histories are used. No model fitting, threshold search, feature changes, HMM refit or economic-result-driven selection. Five-seed majority vote is the same representative rule as cross-market statistics. Per-seed saved validation-only thresholds remain unchanged; strict probability > threshold yields each vote. Nine additional configurations are not searched for better strategies.

## Clock and accounting
Only daily Close exists in frozen inputs. For prediction dated t, execution is at the next frozen observed close t+1. Position held after that close first earns Close(t+2)/Close(t+1)-1. This intentionally adds a conservative execution delay, rather than assuming immediate same-close or unavailable next-open fills. A prediction whose last input close precedes t still uses this delay. Prices are index-local-currency price returns, not total-return, and not directly tradable index fills.

Daily row return = previous-close position * index close-to-close return - current-close one-way turnover * half-round-trip fee. Fees occur when the trade executes, including the first entry and terminal liquidation. Initial capital is 1 immediately before the first eligible execution close; initial earned exposure is zero. Evaluation runs from first prediction + one frozen observation to final 2025 frozen observation. Buy & Hold enters on that same first execution close, exits on terminal close and pays the same per-side cost; Always Cash remains 1. Benchmarks share every evaluation date. Exposure is the fraction of return intervals with a previously held long position. No same-signal-close return is earned, no shorting and no leverage beyond a binary 0/1 portfolio state.

Daily signals maintain a single portfolio state, not overlapping 20-day leveraged sleeves. The last saved prediction remains in force through year-end; stale tail rows are explicitly identified in alignment audit. Nonoverlap schedule starts at the first saved prediction and repeats every 20 frozen observations, not 20 calendar days or 20 selectively chosen predictions. Every scheduled signal executes next close, holds no more than 20 observed intervals, then switches to the next scheduled signal or cash when no signal exists. Schedule phase is never optimized. Positions are flattened at final close.

Costs are stylized ETF/futures implementation assumptions, not the cost of buying an index. Round trips 0/10/25/50 bps mean per-side 0/5/12.5/25 bps, applied only to one-way position changes. Cash and RF are zero. Dividend income, currency conversion, funding, taxes, instrument tracking and explicit market impact are excluded. Transaction_cost_drag is gross compounded terminal wealth minus net wealth; Sum_cost_debits is also saved, since compounding makes them different.

## Metrics
CAGR = compounded wealth^(252/N)-1; annualization uses observed evaluation intervals, not actual calendar-year fractions. Annualized volatility uses sample SD * sqrt(252). Sharpe = mean daily net return / sample daily SD * sqrt(252), RF zero. Downside deviation = sqrt(mean(min(net_return,0)^2))*sqrt(252), including zero downside on nonnegative days; Sortino = mean*252/downside deviation. MDD is negative peak-to-trough wealth drawdown including initial capital 1. Delta MDD >0 means improvement (less negative). Calmar = CAGR/abs(MDD). Cash risk ratios are undefined (NaN), not forced to zero. Hit rate uses positive net-return days conditional on earned long exposure, not forecast label accuracy. Number_of_trades counts one-way entries plus exits; Round_trips and average observed holding intervals are also saved. Turnover is sum(abs(position changes)); annualized turnover multiplies by252/N. Monthly metrics compound each observed calendar-month slice, including partial first months.

## Bootstrap and regimes
Paired moving-block bootstrap samples full daily realized net-return sequences for model and comparator on identical dates: block length20, 2000 resamples, fixed seed20261028. Starts are noncircular uniform valid block starts, concatenated/truncated to original N. Existing cost-adjusted returns are resampled; no new rebalance fees are invented at block joins. Thus CIs are conditional on the realized trading path, not a fresh strategy replay. Mean-return, Sharpe and CAGR differences are saved; Sharpe/CAGR intervals are exploratory. Best configurations were originally selected on test BA; this post-selection uncertainty, transaction-cost model uncertainty and multiple-market dependence are not covered. No formal significance p-values or unadjusted multiple-comparison claims are made.

Saved HMM labels are joined on realized return date, never recomputed or used to filter trades. Labels were causal from prior observations. Regime annualized return compounds only the selected regime returns and raises to252/N_regime: a conditional geometric annualization, not a standalone tradable contiguous-regime CAGR. Regime metrics describe all return-date costs/exposure and compare benchmarks on exactly the same dates. Regime hit rate conditions on active exposure. Delta return is mean daily net return. Relative states are within-market/month; no globally equal volatility bands are asserted.

Prediction disagreement flags use the majority-vote BA and accuracy of the actually traded signals; five-seed mean BA and its mismatch flags are separately retained. Economic performance uses primary 10bps daily CAGR for A/B and Sharpe or negative MDD deterioration for C. These definitions are fixed and transparent, not cherry-picked alternate economic criteria.

KOSPI200 keeps the authorized empirical observation calendar. The 45 XKRX differences are not confirmed missing observations. Forecasts label 20-observation outcomes; executing later and maintaining daily states deliberately differs from direct horizon-return multiplication. A predictive BA advantage need not imply return or risk-adjusted advantage. No claim of economically significant superiority is made without adequate net results and uncertainty support.

Reproduce with analyze.py, report.py (matplotlib required), then validate.py. Original source SHA256 values and package versions are in analysis_manifest.json; economic settings are in economic_protocol.json.
'''
(OUT/'methodology_notes.md').write_text(notes)
lines=['# Frozen-prediction economic evaluation','','Primary: five-seed majority Long/Cash, daily single portfolio state, 10bps round trip, next-close execution with returns starting the following close-to-close interval. All model/threshold/HMM inputs unchanged. No strategy chosen from economic outcomes.','','## Primary cost-adjusted performance','','|Market|Strategy|CAGR|Sharpe|MDD|Exposure|Final wealth|','|---|---|---:|---:|---:|---:|---:|']
for market in M:
 for strategy in S:
  r=perf[(perf.Market==market)&(perf.Mode=='Daily')&(perf.Strategy==strategy)].iloc[0]
  lines.append(f'|{market}|{strategy}|{100*r.CAGR:.2f}%|{r.Sharpe:.3f}|{100*r.Maximum_drawdown:.2f}%|{100*r.Exposure:.1f}%|{r.Final_wealth:.3f}|')
lines+=['','## RQ6–RQ7: Economic translation and costs','','The statements below use the frozen primary daily strategy. Positive CAGR alone is not outperformance, and a point estimate alone is not economically significant evidence.']
for market in M:
 a=perf[(perf.Market==market)&(perf.Mode=='Daily')&(perf.Strategy=='Best_Model')].iloc[0]
 z=comp[(comp.Market==market)&(comp.Mode=='Daily')&(comp.Round_trip_bps==10)]
 zero=cost[(cost.Market==market)&(cost.Mode=='Daily')&(cost.Strategy=='Best_Model')&(cost.Round_trip_bps==0)].iloc[0]
 lines.append(f'- {market}: net CAGR {a.CAGR:.2%}, Sharpe {a.Sharpe:.3f}; CAGR cost drag from 0 to10bps {(zero.CAGR-a.CAGR):.2%}; delta CAGR vs Persistence {z[z.Benchmark=="Persistence"].Delta_CAGR.iloc[0]:+.2%}, vs Buy & Hold {z[z.Benchmark=="Buy_Hold"].Delta_CAGR.iloc[0]:+.2%}.')
lines+=['','## RQ8–RQ9: Prespecified high/low regime regions','','These are conditional realized-return summaries, not regime-timed strategies or independently established significance.']
for market,r in [('NIKKEI225','High'),('EUROSTOXX50','High'),('KOSPI200','Low')]:
 z=reg[(reg.Market==market)&(reg.Regime==r)].iloc[0]
 lines.append(f'- {market} {r}: N={z.N}; mean net daily return {z.Mean_strategy_return:.6f}; Sharpe {z.Sharpe:.3f}; delta Sharpe vs Persistence {z.Delta_Sharpe_vs_Persistence:+.3f}, vs Buy & Hold {z.Delta_Sharpe_vs_Buy_Hold:+.3f}; delta mean return vs Persistence {z.Delta_mean_return_vs_Persistence:+.6f}, vs Buy & Hold {z.Delta_mean_return_vs_Buy_Hold:+.6f}.')
lines+=['','## RQ10: Prediction/economic disagreement','','A/B use majority-vote BA vs Persistence and primary net CAGR; C uses majority accuracy versus Sharpe/MDD. Original five-seed mean BA flags are also saved.']
for z in dis.itertuples():lines.append(f'- {z.Market}: majority delta BA {z.Majority_BA_delta_vs_Persistence:+.4f}, delta accuracy {z.Majority_accuracy_delta_vs_Persistence:+.4f}, delta CAGR {z.Delta_CAGR:+.2%}; A={z.A_BA_better_CAGR_worse}, B={z.B_BA_worse_CAGR_better}, C={z.C_accuracy_better_Sharpe_or_MDD_worse}.')
lines+=['','## Nonoverlapping robustness','','|Market|Strategy|20-observation CAGR|Sharpe|MDD|','|---|---|---:|---:|---:|']
for market in M:
 for strategy in S[:3]:
  z=perf[(perf.Market==market)&(perf.Mode=='Nonoverlap20')&(perf.Strategy==strategy)].iloc[0]
  lines.append(f'|{market}|{strategy}|{z.CAGR:.2%}|{z.Sharpe:.3f}|{z.Maximum_drawdown:.2%}|')
lines+=['','## Exploratory uncertainty','','|Market|Comparator|Statistic|Estimate|95% moving-block CI|','|---|---|---|---:|---|']
for z in boot.itertuples():lines.append(f'|{z.Market}|{z.Benchmark}|{z.Metric}|{z.Estimate:+.6f}|[{z.CI_low:+.6f}, {z.CI_high:+.6f}]|')
lines += ['', 'All ten primary CAGR-difference 95% bootstrap intervals include zero. Net point-estimate improvements are not established economic superiority.']
lines+=['','## Limits','','No economic-significance claim is warranted solely from a positive point estimate or predictive BA. Read block intervals, costs and both benchmark comparisons jointly. Price-only local-currency indices, conservative close execution, stale prediction tails, empirical KOSPI observation dates, test-selected frozen Best configurations, and conditional HMM/return bootstraps limit interpretation. No models or regimes were reselected. methodology_notes.md documents metric definitions and alignment; prediction_return_alignment_audit.csv records signal, effective and return dates.']
(OUT/'results_report.md').write_text('\n'.join(lines)+'\n');(OUT/'README.md').write_text((OUT/'results_report.md').read_text())
print(perf[(perf.Mode=='Daily')&(perf.Strategy=='Best_Model')][['Market','CAGR','Sharpe','Maximum_drawdown','Final_wealth']].to_string(index=False))
