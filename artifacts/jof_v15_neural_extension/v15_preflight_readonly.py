"""Read-only real-data integrity/scaler/causality audit; no fitting or AUC."""
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd
from v15_common import MARKETS,ORIGINS,LOGCOLS,BASE,sha,integrity,reference_dates
from v15_locked_runner import v14_module,window_tensors

def audit(repo):
 root=Path(repo).resolve();base=root/'artifacts/jof_phase1_benchmark_expansion';manifest=json.loads((base/'data_manifest.json').read_text());inventory=json.loads((root/BASE/'v14_input_inventory.json').read_text())['input_sha256'];ref=reference_dates(root);v14=v14_module(root)
 summary=[];folds=[];hashes={};formulas=[]
 for rel,expected in inventory.items():
  if sha(root/rel)!=expected:raise ValueError('V14 input hash mismatch: '+rel)
  hashes[rel]=expected
 for market,folder in MARKETS.items():
  info=next(m for m in manifest['markets'] if m['Market']==market);raw,frame,cols,loaded=v14.load_market(root,market);integrity(raw,frame,cols);hashes.update(loaded)
  for path,key in [(root/'artifacts'/folder/'market_input.csv','Market_input_sha256'),(base/'frozen_features'/f'{market}.csv','Feature_input_sha256')]:
   if sha(path)!=info[key]:raise ValueError('Phase1 input hash mismatch')
  if cols!=info['Feature_names'] or not set(LOGCOLS).issubset(frame):raise ValueError('Frozen feature order/LOG mismatch')
  np.testing.assert_allclose(frame.Log_Ret,np.log(raw.Close).diff(),atol=1e-12,rtol=1e-12,equal_nan=True)
  np.testing.assert_allclose(frame.Disparity20,raw.Close/raw.Close.rolling(20).mean()-1,atol=1e-12,rtol=1e-12,equal_nan=True)
  formulas.append({'Market':market,'Log_Ret':'diff(log(Close))','Disparity20':'Close/rolling_mean20(Close)-1','existing_values_match':True,'raw_features':cols})
  for vy,ty in ORIGINS:
   origin=f'O{vy-2012}';combined=[];combined_rows=[];period_rows={}
   for year,last in [(vy,vy),(vy+1,vy+1),(ty,ty+1)]:
    period='Validation' if last==year else 'Test';train=v14.records(frame,raw,cols,'2010-01-01',f'{year-1}-12-31',preflight=True);ev=v14.records(frame,raw,cols,f'{year}-01-01',f'{last}-12-31',preflight=True)
    if not train or not ev:raise ValueError('Empty fold')
    assert all('y' not in r for r in train+ev)
    assert all(raw.index[r['index']+20]<=pd.Timestamp(f'{year-1}-12-31') for r in train)
    assert all(raw.index[r['index']+20]<=pd.Timestamp(f'{last}-12-31') for r in ev)
    expected=ref[(ref.Market==market)&(ref.Origin==origin)&(ref.Period==period)].Date.tolist()
    if period=='Validation':expected=[d for d in expected if d.startswith(str(year))];combined.extend(r['Date'] for r in ev);combined_rows.extend(ev)
    if [r['Date'] for r in ev]!=expected:raise ValueError('V14 scoring dates differ')
    for features in [cols,LOGCOLS]:
     x,xe,scaler,used=window_tensors(train,[ev[0]],frame,features)
     assert np.isfinite(x).all() and np.isfinite(xe).all()
     np.testing.assert_allclose(scaler.mean_,frame[list(features)].iloc[used].mean().to_numpy(),atol=1e-12,rtol=1e-12)
     assert used.max()<min(r['index'] for r in ev)
     # Target row and all future features may be changed without affecting the training scaler or first forecast window.
     changed=frame.copy();changed.loc[changed.index[ev[0]['index']]:,list(features)]+=1e6
     xx,xxe,ss,u=window_tensors(train,[ev[0]],changed,features)
     np.testing.assert_array_equal(x,xx);np.testing.assert_array_equal(xe,xxe);np.testing.assert_array_equal(scaler.mean_,ss.mean_)
    folds.append({'Market':market,'Origin':origin,'Stage_year':year,'Stage_last_year':last,'Period':period,'TrainN':len(train),'EvalN':len(ev),'train_last_label_date':str(raw.index[train[-1]['index']+20].date()),'evaluation_first':ev[0]['Date'],'evaluation_last':ev[-1]['Date'],'train_only_scaler':True,'future_and_target_row_perturbation_passed':True,'RAW_LOG_all_eligible_windows_finite':True})
    # Check the entire LOG evaluation universe without computing targets.
    log=frame[list(LOGCOLS)].to_numpy(float)
    if any(not np.isfinite(log[r['index']-20:r['index']]).all() for r in train+ev):raise ValueError('LOG missing on RAW-eligible dates')
   period_rows={'Validation':combined_rows,'Test':ev}
   expected=ref[(ref.Market==market)&(ref.Origin==origin)&(ref.Period=='Validation')].Date.tolist()
   if combined!=expected:raise ValueError('Annual validation concatenation differs')
   for period in ['Validation','Test']:
    n=len(ref[(ref.Market==market)&(ref.Origin==origin)&(ref.Period==period)]);summary.append({'Market':market,'Origin':origin,'Period':period,'N':n,**{f'{sig}_N{value}':sum(r['signals'][sig]==value for r in period_rows[period]) for sig in ['200DMA','Momentum60','Persistence'] for value in [0,1]}})
 assert len(summary)==60 and len(folds)==90
 return {'status':'PREFLIGHT_PASS','groups':60,'annual_validation_plus_test_folds':90,'no_training':True,'no_AUC':True,'no_outcome_evaluation':True,'input_sha256':hashes,'formulas':formulas,'summary':summary,'folds':folds,'availability_limit':'Uses unchanged frozen external features and source as-of rules. Actual historical publication timestamps/vintages not independently certified; empirical market observation calendars unchanged.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();report=audit(args.repo);args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(report,indent=2)+'\n');print('PASS60 date groups/90folds; hashes,formulas,finite RAW/LOG,train-onlyscaler,target/future perturbation;no fit or AUC')
if __name__=='__main__':main()
