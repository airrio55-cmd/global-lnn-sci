"""Independent portfolio accounting, temporal alignment and future-return tests."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
import pandas as pd,numpy as np
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
protocol=json.loads((OUT/'economic_protocol.json').read_text());manifest=json.loads((OUT/'analysis_manifest.json').read_text())
daily=pd.read_csv(OUT/'daily_strategy_returns.csv',float_precision='round_trip');audit=pd.read_csv(OUT/'prediction_return_alignment_audit.csv');perf=pd.read_csv(OUT/'transaction_cost_sensitivity.csv',float_precision='round_trip')
assert len(perf)==160 and len(pd.read_csv(OUT/'performance_summary.csv'))==40
assert len(pd.read_csv(OUT/'economic_bootstrap_ci.csv'))==30
assert len(pd.read_csv(OUT/'regime_economic_results.csv'))==15
assert not daily.duplicated(['Market','Mode','Strategy','Round_trip_bps','Date']).any()
assert audit.Causal.all()
v2=audit.Current_signal_date.notna();s2=pd.to_datetime(audit.loc[v2,'Current_signal_date']);e2=pd.to_datetime(audit.loc[v2,'Current_position_effective_date']);r2=pd.to_datetime(audit.loc[v2,'Return_date']);assert (s2<e2).all() and (e2<=r2).all()
tr=audit.Trade_trigger.eq('signal');assert (pd.to_datetime(audit.loc[tr,'Current_position_effective_date'])==pd.to_datetime(audit.loc[tr,'Trade_date'])).all()
v=audit.Signal_date.notna();sig=pd.to_datetime(audit.loc[v,'Signal_date']);eff=pd.to_datetime(audit.loc[v,'Position_effective_date']);ret=pd.to_datetime(audit.loc[v,'Return_date']);assert (sig<eff).all() and (eff<ret).all()
for market,folder in protocol['markets'].items():
 raw=pd.read_csv(ROOT/folder/'market_input.csv',index_col=0,parse_dates=True,float_precision='round_trip');dates=raw.index;close=raw.Close.to_numpy();f=pd.read_csv(ROOT/f'artifacts/cross_market_statistics/{market}_majority_predictions.csv');loc=dates.get_indexer(pd.to_datetime(f.Date));start=loc[0]+1;end=np.where(dates<='2025-12-31')[0][-1];T=end-start+1
 def reconstruct(prices,mode,strategy):
  events={};positions=np.zeros(len(prices))
  if strategy=='Buy_Hold':events[start]=1
  if strategy in ['Best_Model','Persistence']:
   signals=f.Majority_prediction if strategy=='Best_Model' else f.Persistence_prediction;lookup=dict(zip(loc,signals));scheduled=loc if mode=='Daily' else np.arange(loc[0],loc[-1]+1,20)
   for s in scheduled:
    if s not in lookup:continue
    ex=s+1
    if mode=='Nonoverlap20':events[ex+20]=0
    events[ex]=int(lookup[s])
  events[end]=0
  held=0
  for j in range(len(prices)):
   held=events.get(j,held);positions[j]=held
  previous=np.r_[0.,positions[:-1]];changes=positions-previous;returns=np.r_[0.,prices[1:]/prices[:-1]-1]
  return positions[start:end+1],previous[start:end+1],changes[start:end+1],returns[start:end+1]
 for mode in ['Daily','Nonoverlap20']:
  for strategy in ['Best_Model','Persistence','Buy_Hold','Always_Cash']:
   pos,prev,chg,r=reconstruct(close,mode,strategy)
   # Re-run same execution/accounting with future prices modified: positions cannot depend on returns.
   changed=close.copy();changed[dates>='2024-01-01']*=1.5
   p2,pr2,ch2,r2=reconstruct(changed,mode,strategy)
   assert np.array_equal(pos,p2) and np.array_equal(prev,pr2) and np.array_equal(chg,ch2)
   earlier=dates[start:end+1]<'2024-01-01';np.testing.assert_allclose(r[earlier],r2[earlier],atol=0,rtol=0)
   for cost in [0,10,25,50]:
    z=daily[(daily.Market==market)&(daily.Mode==mode)&(daily.Strategy==strategy)&(daily.Round_trip_bps==cost)]
    assert len(z)==T and np.array_equal(pd.to_datetime(z.Date),dates[start:end+1])
    fees=abs(chg)*cost/2/10000;net=prev*r-fees
    np.testing.assert_allclose(z.Position_at_close,pos,atol=0,rtol=0);np.testing.assert_allclose(z.Position_previous_close,prev,atol=0,rtol=0)
    np.testing.assert_allclose(z.Net_return,net,atol=1e-14,rtol=0);np.testing.assert_allclose(z.Wealth,np.cumprod(1+net),atol=1e-12,rtol=0)
    row=perf[(perf.Market==market)&(perf.Mode==mode)&(perf.Strategy==strategy)&(perf.Round_trip_bps==cost)].iloc[0]
    assert abs(row.Final_wealth-np.prod(1+net))<1e-12
    assert row.Number_of_trades==abs(chg).sum()
    assert np.all((prev>=0)&(prev<=1))
    if strategy=='Always_Cash':assert (z.Wealth==1).all()
 # Monotonicity: higher costs cannot improve final wealth for same fixed path.
 for _,g in perf[perf.Market==market].groupby(['Mode','Strategy']):assert (np.diff(g.sort_values('Round_trip_bps').Final_wealth)<=1e-12).all()
for p,digest in manifest['input_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest
required=['economic_protocol.json','daily_strategy_returns.csv','performance_summary.csv','benchmark_comparison.csv','transaction_cost_sensitivity.csv','nonoverlap_20d_results.csv','regime_economic_results.csv','economic_bootstrap_ci.csv','prediction_return_alignment_audit.csv','results_report.md','methodology_notes.md','analysis_manifest.json']
assert all((OUT/p).exists() for p in required)
for n in ['cumulative_wealth_by_market.png','sharpe_comparison.png','transaction_cost_sensitivity.png','regime_economic_heatmap.png']:assert (OUT/n).stat().st_size>1000
check={'status':'validated','validated_at_utc':datetime.now(timezone.utc).isoformat(),'markets':5,'performance_combinations':160,'primary_summary_rows':40,'bootstrap_CIs':30,'same_signal_close_execution':False,'signal_effective_return_order_verified':True,'independent_execution_and_accounting_reconstruction_passed':True,'future_price_return_perturbation_positions_invariant':True,'past_returns_unaffected_by_future_perturbation':True,'unit_leverage_verified':True,'entry_and_terminal_exit_costs_verified':True,'cost_wealth_monotonicity_passed':True,'source_inputs_unchanged':True,'predictive_and_HMM_training':False}
(OUT/'completion_check.json').write_text(json.dumps(check,indent=2)+'\n')
manifest['script_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.py')};manifest['protocol_sha256']=hashlib.sha256((OUT/'economic_protocol.json').read_bytes()).hexdigest();(OUT/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(check,indent=2))
