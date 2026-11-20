"""Train-only selection, causal continuation, then reuse frozen Test probabilities."""
from pathlib import Path
import hashlib,json,sys
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from runtime.step6b_fit import validate,read,write,sha
from kospi200.step6a_hmm import SEEDS,select_candidate,train_state_names,filter_sessions,align_regime_predictions
from kospi200.step5b_data import read_price_prefix
from kospi200.step5b_policy import test_metrics

def main():
 cp=R/'data/derived/step6b_config_private.json';ap=R/'data/derived/step6b_approval_private.json';c,a,run,inputs,jobs=validate(cp,ap);assert (run/'fits_done.json').exists();calendar=pd.read_csv(R/inputs['calendar_file'],parse_dates=['Date']);dates=pd.DatetimeIndex(calendar.Date);selections={};cohort_records=[]
 # Complete every Train selection/naming before reading any Validation/Test prices or probabilities.
 for origin in ['O1','O2','O3','O4','O5']:
  for candidate in ['A','B']:
   folder=run/'cohorts'/f'{origin}_{candidate}';folder.mkdir(exist_ok=True);items=[];records=[]
   for j in [x for x in jobs if x['origin']==origin and x['candidate']==candidate]:
    p=run/'candidates'/j['job_id']/'result.json';z=read(p) if p.exists() else {**j,'status':'BLOCKED_UNLAUNCHED','fit_calls':0};records.append(z)
    if z['status']=='ELIGIBLE':
     assert sha(p.parent/'parameters_private.npz')==z['parameter_sha256'];z=dict(z)
     with np.load(p.parent/'parameters_private.npz',allow_pickle=False) as q:z['parameters']={k:q[k].copy() for k in q.files}
     items.append(z)
    else:items.append({'seed':j['seed'],'train_log_likelihood':np.nan,'likelihood_history':[],'monitor_converged':False,'parameters':{},'train_hard_states':[],'reproducibility_evidence':{}})
   info=inputs['groups'][origin][candidate];cohort={'origin':origin,'candidate':candidate,'status':'BLOCKED','candidate_count':len(records),'eligible_count':sum(z['status']=='ELIGIBLE' for z in records),'ineligible_count':sum(z['status']=='INELIGIBLE' for z in records),'failed_count':sum(z['status']=='FAILED' for z in records),'selection_partition':'train','Test_values_read_during_selection':0}
   try:
    chosen,_=select_candidate(items);jid=f'{origin}_{candidate}_HMM_init{chosen["seed"]}';p=run/'candidates'/jid
    with np.load(R/info['Train_file'],allow_pickle=False) as q:raw=q['raw'].copy();train_ids=q['session_id'].copy()
    with np.load(p/'Train_posterior_private.npz',allow_pickle=False) as q:train_post=q['posterior'].copy();assert np.array_equal(q['session_id'],train_ids)
    names=train_state_names(raw,train_post);hard=train_post.argmax(1);cohort.update(status='SELECTED_TRAIN_ONLY',selected_seed=chosen['seed'],selected_job_id=jid,train_log_likelihood=chosen['train_log_likelihood'],state_names=names,Train_raw_state_means=[float(raw[hard==i].mean()) for i in [0,1]],standardized_emission_means=np.asarray(chosen['parameters']['means']).tolist(),parameter_sha256=chosen['parameter_sha256'],selection_tie_rule='exact max Train LL then smallest seed');selections[(origin,candidate)]={'cohort':cohort,'parameters':chosen['parameters'],'previous_posterior':train_post[-1],'raw_Train':raw}
   except Exception as e:cohort['block_reason']=str(e)
   write(folder/'selection_private.json',cohort);cohort_records.append(cohort)
 write(run/'all_Train_selections_frozen_private.json',cohort_records)
 # All states and labels selected from Train, then all post-Train sessions including purge bridges.
 for key,s in selections.items():
  origin,candidate=key;cohort=s['cohort'];info=inputs['groups'][origin][candidate];folder=run/'cohorts'/f'{origin}_{candidate}'
  try:
   assert sha(R/info['source_file'])==info['source_sha256'];prefix=dates[dates<=pd.Timestamp(info['filter_end'])];close=read_price_prefix(R/info['source_file'],prefix);vol=np.log(close/close.shift(1)).rolling(40).std(ddof=1);rawtrain=vol.loc[pd.to_datetime(info['Train_dates'])].to_numpy()[:,None];assert np.array_equal(rawtrain,s['raw_Train']);sm=read(R/info['scaler_file']);fd=pd.to_datetime(info['filter_dates']);raw=vol.loc[fd].to_numpy()[:,None];x=(raw-np.asarray(sm['mean']))/np.asarray(sm['scale']);ids=np.asarray(info['filter_session_ids'],dtype=np.int64);before={k:np.asarray(v).copy() for k,v in s['parameters'].items()}
   q=filter_sessions(x,ids,parameters=s['parameters'],expected_session_ids=ids,previous_posterior=s['previous_posterior'],previous_session_id=info['Train_last_session_id']);assert all(np.array_equal(v,s['parameters'][k]) for k,v in before.items());assert np.isfinite(q).all() and np.allclose(q.sum(1),1);names=cohort['state_names'];states=q.argmax(1);regime=np.array([names[int(i)] for i in states]);np.savez(folder/'forward_path_private.npz',dates=np.array(fd.strftime('%Y-%m-%d'),dtype='U10'),session_id=ids,posterior=q,regime=regime,Vol_Regime=raw[:,0]);cohort.update(status='FILTERED',filter_path_sha256=sha(folder/'forward_path_private.npz'),filter_sessions=len(ids),bridge_sessions=20,bridge_checked=True,first_filter_session=int(ids[0]),last_filter_session=int(ids[-1]),parameter_unchanged=True,filter_calls=1,filter_end=info['filter_end']);cohort['2026_used']=0
  except Exception as e:cohort.update(status='BLOCKED_FILTER',block_reason=str(e))
  write(folder/'cohort_result_private.json',cohort)
 # No new NN forward: use exactly stored500 predictions after every HMM selection/filter is frozen.
 bconfig=read(R/'data/derived/step5b_test_config_private.json');brun=R/bconfig['output_root'];nnjobs=read(brun/'jobs_private.json');results=[];distribution=[]
 for j in nnjobs:
  origin=j['origin'];candidate=j['candidate'];cohort=next(z for z in cohort_records if z['origin']==origin and z['candidate']==candidate);base={k:j[k] for k in ['run_id','origin','candidate','seed','model']}
  if cohort['status']!='FILTERED':results.append({**base,'status':'BLOCKED_HMM_COHORT','reason':cohort.get('block_reason')});continue
  folder=run/'cohorts'/f'{origin}_{candidate}';rp=brun/'jobs'/j['run_id']/'result.json';old=read(rp);predpath=rp.parent/'test_predictions_private.npz';assert sha(predpath)==old['probability_sha256']
  with np.load(folder/'forward_path_private.npz',allow_pickle=False) as q:path={k:q[k].copy() for k in q.files}
  with np.load(predpath,allow_pickle=False) as q:pred={k:q[k].copy() for k in ['dates','y','label_end','session_id','probability','regime']}
  expected=calendar.loc[(calendar.Date.dt.year==inputs['groups'][origin][candidate]['test_year'])&(calendar.session_id+20<len(calendar))];assert np.array_equal(pred['session_id'],expected.session_id.to_numpy()) and pred['dates'].tolist()==expected.Date.dt.strftime('%Y-%m-%d').tolist();path_index={int(v):i for i,v in enumerate(path['session_id'])};aligned_path_dates=path['dates'][[path_index[int(v)] for v in pred['session_id']]];pred.update(origin=origin,candidate=candidate);states={'origin':origin,'candidate':candidate,'session_id':path['session_id'],'regime':path['regime'],'evaluation_dates':aligned_path_dates,'evaluation_label_end':pred['label_end'],'evaluation_y':pred['y']};rows=align_regime_predictions(pred,states,origin=origin,candidate=candidate,expected_ids=pred['session_id']);assert test_metrics(pred['y'],pred['probability'])==old['metrics'];results.append({**base,'status':'COMPLETED','HMM_regimes':rows,'original_probability_sha256':old['probability_sha256'],'n_sum_verified':sum(x['n'] for x in rows)==len(pred['y'])})
  if j['seed']==2 and j['model']=='RNN':
   index={int(s):i for i,s in enumerate(path['session_id'])};ix=np.array([index[int(s)] for s in pred['session_id']]);vols=path['Vol_Regime'][ix];regs=path['regime'][ix]
   for method,labels,nameset in [('HMM',regs,['Low_Vol','High_Vol']),('MANUAL',pred['regime'],['Low_Vol','Mid_Vol','High_Vol'])]:
    for name in nameset:
     mask=labels==name;yy=pred['y'][mask];vv=vols[mask];distribution.append({'origin':origin,'candidate':candidate,'method':method,'regime':name,'n':int(mask.sum()),'support0':int((yy==0).sum()),'support1':int((yy==1).sum()),'occupancy':float(mask.mean()),'vol_mean':float(vv.mean()) if len(vv) else None,'vol_std':float(vv.std(ddof=1)) if len(vv)>1 else None,'actual_positive_fraction':float(yy.mean()) if len(yy) else None})
 write(run/'neural_HMM_regime_metrics_private.json',results);write(run/'manual_HMM_distribution_private.json',distribution);write(run/'cohort_results_private.json',cohort_records);write(run/'filter_evaluation_done.json',{'selected_cohorts':len(selections),'filtered_cohorts':sum(c['status']=='FILTERED' for c in cohort_records),'evaluated_NN_outputs':sum(r['status']=='COMPLETED' for r in results),'blocked_NN_outputs':sum(r['status']!='COMPLETED' for r in results),'new_NN_forwards':0,'new_financial_pvalues':0});print(json.dumps(read(run/'filter_evaluation_done.json')))
if __name__=='__main__':main()
