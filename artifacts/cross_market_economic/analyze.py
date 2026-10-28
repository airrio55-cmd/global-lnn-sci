"""Fixed-prediction Long/Cash accounting; no fitting or signal optimization."""
from pathlib import Path
import json,hashlib,itertools
from datetime import datetime,timezone
import numpy as np,pandas as pd
from sklearn.metrics import accuracy_score,balanced_accuracy_score
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
MARKETS={'SP500':'artifacts/sp500_rerun','NASDAQ100':'artifacts/nasdaq100','NIKKEI225':'artifacts/nikkei225','EUROSTOXX50':'artifacts/eurostoxx50','KOSPI200':'artifacts/kospi200'}
BEST={'SP500':('LNN','MILD_WCE'),'NASDAQ100':('Transformer','CE'),'NIKKEI225':('LNN','CE'),'EUROSTOXX50':('LNN','MILD_FOCAL'),'KOSPI200':('LSTM','CE')}
COSTS=[0,10,25,50];STRATEGIES=['Best_Model','Persistence','Buy_Hold','Always_Cash'];B=2000;L=20;SEED=20261028;inputs={}
def read(p,**kw):
 p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,**kw)
def save(x,name):pd.DataFrame(x).to_csv(OUT/name,index=False,float_format='%.17g')
protocol={'markets':MARKETS,'frozen_best':BEST,'prediction_rule':'Original saved per-seed threshold (strict probability > threshold); five-seed majority (>=3), matching cross-market statistics; no reselection','execution':'Close-only: signal at t, execute at next frozen observed close t+1, earn price return from t+1 to t+2 onward. Same signal-date close execution forbidden. Fees charged at execution-date close.','accounting':'net_return_t = position_at_previous_close * close_to_close_return_t - per_side_fee * abs(position_at_close - previous_position). Final liquidation fee at last close.','evaluation':'Per-market common window: first saved prediction date + one observed date through last frozen 2025 observation. Start flat before first execution; no 2026 rows. All benchmarks use identical dates.','daily_tail':'Last available signal held through evaluation end; tail dates flagged as stale. No new predictions fabricated.','nonoverlap':'Schedule signals every 20 frozen raw observation dates starting at first prediction; execute next close; hold at most 20 observed intervals, then next scheduled signal or cash if absent. No favorable schedule phase selection.','cost_round_trip_bps':COSTS,'primary_round_trip_bps':10,'per_side':'Half round-trip cost, charged per unit one-way turnover; index tracking ETF/future stylized fee, not index tradability','cash_return':0,'risk_free_rate':0,'leverage_max':1,'return_basis':'Frozen Close price returns in local index currency; no dividends, FX conversion, financing, taxes, tracking error or explicit slippage beyond fixed stylized costs','annualization':252,'trades':'Number of one-way entries/exits; round trips separately; average holding period in observed close intervals','hit_rate':'Fraction positive net daily returns among days with previous-close equity exposure >0; not forecast accuracy','bootstrap':{'method':'paired noncircular moving date-block bootstrap of realized primary daily net returns; no extra trades invented at block joins','block_length':L,'resamples':B,'seed':SEED,'CI':'95% percentile, exploratory; no formal multiple-comparison significance claim'},'regime':'Use saved causal HMM label on realized return date, no HMM refit, no regime-conditioned signal changes; conditional annualized return is geometric mean over regime dates raised to252, not contiguous-regime CAGR','predictive_training':False,'threshold_tuning':False,'HMM_training':False}
(OUT/'economic_protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
reg=read(ROOT/'artifacts/cross_market_hmm/regime_assignments_all_markets.csv');reg.Date=pd.to_datetime(reg.Date)
besttable=read(ROOT/'artifacts/cross_market_statistics/market_best_models.csv').set_index('Market')
daily=[];performance=[];comparisons=[];regresults=[];boot=[];align=[];disagreements=[]
rng=np.random.default_rng(SEED)
def metrics(net,gross,pos,changes,dates,costs):
 n=len(net);wealth=np.cumprod(1+net);grosswealth=np.prod(1+gross);ann=float(np.prod(1+net)**(252/n)-1);vol=float(np.std(net,ddof=1)*np.sqrt(252));down=float(np.sqrt(np.mean(np.minimum(net,0)**2))*np.sqrt(252));mean=float(np.mean(net));peak=np.maximum.accumulate(np.r_[1.,wealth]);mdd=float(np.min(np.r_[1.,wealth]/peak-1));sh=mean*252/vol if vol>0 else np.nan;so=mean*252/down if down>0 else np.nan
 entries=np.where(changes>0)[0];exits=np.where(changes<0)[0];hold=[e-s for s,e in zip(entries,exits)]
 monthly=pd.Series(net,index=dates).groupby(dates.to_period('M')).apply(lambda x:np.prod(1+x)-1)
 active=pos>0
 return {'N':n,'Total_return':wealth[-1]-1,'CAGR':ann,'Annualized_volatility':vol,'Sharpe':sh,'Sortino':so,'Maximum_drawdown':mdd,'Calmar':ann/abs(mdd) if mdd<0 else np.nan,'Hit_rate':float(np.mean(net[active]>0)) if active.any() else np.nan,'Exposure':float(pos.mean()),'Number_of_trades':int(np.abs(changes).sum()),'Round_trips':len(exits),'Turnover':float(np.abs(changes).sum()),'Annualized_turnover':float(np.abs(changes).sum()*252/n),'Average_holding_period':float(np.mean(hold)) if hold else np.nan,'Transaction_cost_drag':grosswealth-wealth[-1],'Sum_cost_debits':float(costs.sum()),'Final_wealth':wealth[-1],'Downside_deviation':down,'Mean_daily_return':mean,'Monthly_return_mean':monthly.mean(),'Monthly_return_volatility':monthly.std(ddof=1)}
for market,folder in MARKETS.items():
 directory=ROOT/folder;raw=read(directory/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');idx=raw.index;close=raw.Close.to_numpy();assert idx.is_unique and idx.is_monotonic_increasing and (close>0).all()
 model,loss=BEST[market];assert (besttable.loc[market,'Best_Model'],besttable.loc[market,'Loss'])==(model,loss)
 results=read(directory/'seed_results.csv');votes=[];sdates=None;y=None
 for seed in [42,52,62,72,82]:
  f=read(directory/'predictions'/f'{model}_{loss}_{seed}.csv',float_precision='round_trip');d=pd.DatetimeIndex(pd.to_datetime(f.Date));yy=f.Y_true.to_numpy(int)
  if sdates is None:sdates=d;y=yy
  else:assert d.equals(sdates) and np.array_equal(y,yy)
  r=results[(results.Model==model)&(results.Loss==loss)&(results.Seed.astype(str)==str(seed))].iloc[0]
  assert np.allclose(f.Threshold,r.Threshold,atol=1e-14,rtol=0)
  vote=(f.Probability.to_numpy()>r.Threshold).astype(int);assert np.isclose(balanced_accuracy_score(y,vote),r.Balanced_Accuracy,atol=1e-12,rtol=0);votes.append(vote)
 majority=(np.array(votes).sum(axis=0)>=3).astype(int);loc=idx.get_indexer(sdates);assert (loc>=20).all()
 persistence=(close[loc]>close[loc-20]).astype(int)
 saved=read(ROOT/f'artifacts/cross_market_statistics/{market}_majority_predictions.csv');assert np.array_equal(saved.Majority_prediction,majority) and np.array_equal(saved.Persistence_prediction,persistence) and np.array_equal(pd.to_datetime(saved.Date),sdates)
 start=loc[0]+1;end=int(np.where(idx<='2025-12-31')[0][-1]);dates=idx[start:end+1];T=len(dates);marketret=np.r_[0.,close[1:]/close[:-1]-1]
 regimes=reg[reg.Market==market].set_index('Date').loc[dates,'Regime'].to_numpy()
 paths={}
 for mode in ['Daily','Nonoverlap20']:
  for strategy in STRATEGIES:
   atclose=np.zeros(len(idx));origin=np.full(len(idx),-1,int);effective=np.full(len(idx),-1,int)
   if strategy=='Buy_Hold':atclose[start:end+1]=1;effective[start:end+1]=start
   elif strategy in ['Best_Model','Persistence']:
    signals=majority if strategy=='Best_Model' else persistence;lookup=dict(zip(loc,signals));scheduled=loc if mode=='Daily' else np.arange(loc[0],loc[-1]+1,20)
    for signal_i in scheduled:
     if signal_i not in lookup:continue
     exec_i=signal_i+1
     if exec_i>end:continue
     stop=end+1 if mode=='Daily' else min(exec_i+20,end+1)
     atclose[exec_i:stop]=lookup[signal_i];origin[exec_i:stop]=signal_i;effective[exec_i:stop]=exec_i
   # Flatten at terminal close; fees apply after earning the last day's previous-close position.
   atclose[end]=0
   lag=np.r_[0.,atclose[:-1]];change=atclose-np.r_[0.,atclose[:-1]]
   earned=lag[start:end+1];gross=earned*marketret[start:end+1];chg=change[start:end+1]
   src=np.r_[-1,origin[:-1]][start:end+1];eff=np.r_[-1,effective[:-1]][start:end+1]
   if strategy in ['Best_Model','Persistence']:
    valid=src>=0
    assert (src[valid]<eff[valid]).all() and (eff[valid]<np.arange(start,end+1)[valid]).all()
    # validate.py independently rebuilds execution and perturbs future prices/returns.
    if mode=='Nonoverlap20':assert ((np.arange(start,end+1)[valid]-eff[valid])<=20).all()
    for j in range(T):
     align.append({'Market':market,'Mode':mode,'Strategy':strategy,'Return_date':str(dates[j].date()),'Signal_date':str(idx[src[j]].date()) if src[j]>=0 else '', 'Position_effective_date':str(idx[eff[j]].date()) if eff[j]>=0 else '', 'Position_previous_close':earned[j],'Position_at_close':atclose[start+j],'One_way_turnover':abs(chg[j]),'Current_signal_date':str(idx[origin[start+j]].date()) if origin[start+j]>=0 else '', 'Current_position_effective_date':str(idx[effective[start+j]].date()) if effective[start+j]>=0 else '', 'Trade_date':str(dates[j].date()) if chg[j]!=0 else '', 'Trade_trigger':('terminal_liquidation' if j==T-1 and chg[j]<0 else ('signal' if origin[start+j]>=0 else 'scheduled_expiry')) if chg[j]!=0 else 'none','Signal_age_observations':int(start+j-src[j]) if src[j]>=0 else np.nan,'After_last_prediction':bool(dates[j]>sdates[-1]),'Causal':bool(src[j]<eff[j]<start+j) if src[j]>=0 else True})
   for bps in COSTS:
    costs=np.abs(chg)*(bps/2/10000);net=gross-costs;assert np.isfinite(net).all() and (net>-1).all() and ((earned>=0)&(earned<=1)).all()
    paths[(mode,strategy,bps)]=(net,gross,earned,chg,costs)
    perf={'Market':market,'Mode':mode,'Strategy':strategy,'Round_trip_bps':bps,**metrics(net,gross,earned,chg,dates,costs)};performance.append(perf)
    wealth=np.cumprod(1+net)
    for j,date in enumerate(dates):daily.append({'Market':market,'Date':str(date.date()),'Mode':mode,'Strategy':strategy,'Round_trip_bps':bps,'Position_previous_close':earned[j],'Position_at_close':atclose[start+j],'Index_return':marketret[start+j],'Gross_return':gross[j],'Cost_debit':costs[j],'Net_return':net[j],'Wealth':wealth[j],'Regime':regimes[j]})
 for mode in ['Daily','Nonoverlap20']:
  for bps in COSTS:
   p=[r for r in performance if r['Market']==market and r['Mode']==mode and r['Round_trip_bps']==bps];base={r['Strategy']:r for r in p}
   for bench in ['Persistence','Buy_Hold']:
    comparisons.append({'Market':market,'Mode':mode,'Round_trip_bps':bps,'Benchmark':bench,**{'Delta_'+k:base['Best_Model'][k]-base[bench][k] for k in ['CAGR','Sharpe','Sortino','Maximum_drawdown','Final_wealth']}})
 # Primary regime economics, conditional return-date labels, not trading filters.
 for regime in ['Low','Normal','High']:
  mask=regimes==regime;outcomes={}
  for strategy in STRATEGIES:
   net,gross,exposure,chg,costs=paths[('Daily',strategy,10)];r=net[mask];n=len(r);vol=np.std(r,ddof=1)*np.sqrt(252);sh=np.mean(r)*252/vol if vol>0 else np.nan
   outcomes[strategy]={'Mean_strategy_return':np.mean(r),'Conditional_annualized_return':np.prod(1+r)**(252/n)-1,'Sharpe':sh,'Hit_rate':np.mean(r[exposure[mask]>0]>0) if (exposure[mask]>0).any() else np.nan,'Exposure':exposure[mask].mean(),'Turnover':np.abs(chg[mask]).sum(),'Cost_debit_sum':costs[mask].sum(),'Mean_daily_cost_drag':costs[mask].mean(),'N':n}
  bm=outcomes['Best_Model'];regresults.append({'Market':market,'Regime':regime,'Model':model,'Loss':loss,**bm,'Delta_mean_return_vs_Persistence':bm['Mean_strategy_return']-outcomes['Persistence']['Mean_strategy_return'],'Delta_mean_return_vs_Buy_Hold':bm['Mean_strategy_return']-outcomes['Buy_Hold']['Mean_strategy_return'],'Delta_Sharpe_vs_Persistence':bm['Sharpe']-outcomes['Persistence']['Sharpe'],'Delta_Sharpe_vs_Buy_Hold':bm['Sharpe']-outcomes['Buy_Hold']['Sharpe'],'Persistence_Sharpe':outcomes['Persistence']['Sharpe'],'Buy_Hold_Sharpe':outcomes['Buy_Hold']['Sharpe']})
 primary={s:next(r for r in performance if r['Market']==market and r['Mode']=='Daily' and r['Strategy']==s and r['Round_trip_bps']==10) for s in STRATEGIES}
 for benchmark in ['Persistence','Buy_Hold']:
  samples=[]
  for _ in range(B):
   starts=rng.integers(0,T-L+1,size=int(np.ceil(T/L)));ix=(starts[:,None]+np.arange(L)).ravel()[:T]
   a=paths[('Daily','Best_Model',10)][0][ix];b=paths[('Daily',benchmark,10)][0][ix]
   def triple(r):
    sd=np.std(r,ddof=1);return np.array([np.mean(r),np.mean(r)/sd*np.sqrt(252) if sd>0 else np.nan,np.prod(1+r)**(252/T)-1])
   samples.append(triple(a)-triple(b))
  samples=np.array(samples)
  for j,name in enumerate(['Mean_daily_return','Sharpe','CAGR']):
   boot.append({'Market':market,'Benchmark':benchmark,'Metric':'Delta_'+name,'Estimate':primary['Best_Model'][name]-primary[benchmark][name],'CI_low':np.nanquantile(samples[:,j],.025),'CI_high':np.nanquantile(samples[:,j],.975),'Resamples':B,'Block_length':L,'Exploratory':True})
 ba_delta=balanced_accuracy_score(y,majority)-balanced_accuracy_score(y,persistence);acc_delta=accuracy_score(y,majority)-accuracy_score(y,persistence);econ=primary['Best_Model']['CAGR']-primary['Persistence']['CAGR']
 disagreements.append({'Market':market,'Majority_BA_delta_vs_Persistence':ba_delta,'Five_seed_mean_BA_delta_vs_Persistence':besttable.loc[market,'Delta_BA'],'Majority_accuracy_delta_vs_Persistence':acc_delta,'Delta_CAGR':econ,'Delta_Sharpe':primary['Best_Model']['Sharpe']-primary['Persistence']['Sharpe'],'Delta_MDD':primary['Best_Model']['Maximum_drawdown']-primary['Persistence']['Maximum_drawdown'],'A_BA_better_CAGR_worse':bool(ba_delta>0 and econ<0),'B_BA_worse_CAGR_better':bool(ba_delta<0 and econ>0),'C_accuracy_better_Sharpe_or_MDD_worse':bool(acc_delta>0 and (primary['Best_Model']['Sharpe']<primary['Persistence']['Sharpe'] or primary['Best_Model']['Maximum_drawdown']<primary['Persistence']['Maximum_drawdown']))})
 print('FINISHED',market,flush=True)
save(daily,'daily_strategy_returns.csv');save(performance,'transaction_cost_sensitivity.csv');pf=pd.DataFrame(performance);pf[pf.Round_trip_bps==10].to_csv(OUT/'performance_summary.csv',index=False);pf[pf.Mode=='Nonoverlap20'].to_csv(OUT/'nonoverlap_20d_results.csv',index=False);save(comparisons,'benchmark_comparison.csv');save(regresults,'regime_economic_results.csv');save(boot,'economic_bootstrap_ci.csv');save(align,'prediction_return_alignment_audit.csv');save(disagreements,'predictive_economic_disagreement.csv')
for name,digest in inputs.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
(OUT/'analysis_manifest.json').write_text(json.dumps({'status':'completed','completed_at_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':inputs,'predictive_training':False,'HMM_refitting':False,'threshold_changes':False,'source_files_unchanged':True,'packages':{n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['numpy','pandas','scipy','scikit-learn']}},indent=2)+'\n')
