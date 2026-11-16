"""Collect old10+new30 without refitting; compute exploratory seed/origin/manual diagnostics."""
from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.manual_evaluation import supplied_prediction_metrics
METRICS=['validation_BA','macro_f1','accuracy','recall0','recall1','brier','prediction_positive_rate','best_epoch','degenerate_epoch_ratio']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
 m=json.loads((ROOT/'manifests/step3b_execution_manifest.json').read_text());g=json.loads((ROOT/'manifests/step3b_preflight.json').read_text());c=json.loads((ROOT/'configs/step3b_pilot_config.json').read_text());run=ROOT/m['run_directory']
 if m['new_interrupted']:raise RuntimeError('Resume unfinished identities before final collection')
 entries=[]
 for old in g['reused_STEP3A']:
  entries.append((old['run_id'],'O1',2,old['candidate'],old['model'],'STEP3A_REUSED',ROOT/old['source_directory'],old['record']))
 for j in g['jobs']:
  record=m['new_records'][j['run_id']];entries.append((j['run_id'],j['origin'],j['seed'],j['candidate'],j['model'],'STEP3B_NEW',run/'jobs'/j['run_id'],record))
 entries.sort(key=lambda x: (x[1],x[2],x[3],c['models'].index(x[4])))
 rows=[];histories=[];manual=[]
 for identifier,origin,seed,candidate,model,stage,folder,record in entries:
  data=g['datasets'][origin][candidate];meta=data['metadata'];hfile=folder/'history.json';history=json.loads(hfile.read_text()) if hfile.exists() else []
  count=record.get('epochs_completed',0);bad=record.get('epochs_with_degenerate_prediction',sum(r['prediction_status']=='DEGENERATE_PREDICTION' for r in history))
  row={'run_id':identifier,'source_stage':stage,'origin':origin,'seed':seed,'effective_seed':seed+c['model_seed_offsets'][model],'candidate':candidate,'model':model,'status':record['status'],
       'train_samples':meta['train_samples'],'validation_samples':meta['validation_samples'],'validation_class0':meta['class_counts']['validation']['0'],'validation_class1':meta['class_counts']['validation']['1'],
       'epochs':count,'best_epoch':record.get('best_validation_epoch'),'degenerate_prediction_epochs':bad,'degenerate_epoch_ratio':bad/count if count else np.nan,
       'stopped_early':count<100 if count else None,'checkpoint_restore':record.get('checkpoint_restore',False),'RNG_restore_exact':record.get('RNG_restore_exact',False),
       'prediction_status':record.get('prediction_status'),'error':record.get('error'),'input_data_sha256':record.get('input_data_sha256'),
       'code_sha256':record.get('worker_sha256',record.get('code_sha256')),'model_settings_sha256':hashlib.sha256(json.dumps(c['model_settings'],sort_keys=True).encode()).hexdigest(),
       'best_checkpoint_sha256':record.get('best_checkpoint_sha256'),'latest_checkpoint_sha256':record.get('latest_checkpoint_sha256'),'history_sha256':record.get('history_sha256'),
       'source_directory':str(folder.relative_to(ROOT)),'elapsed_training_seconds':record.get('elapsed_training_seconds')}
  row.update(record.get('metrics',{}));rows.append(row)
  for h in history:histories.append({'run_id':identifier,'source_stage':stage,'origin':origin,'seed':seed,'candidate':candidate,'model':model,**h})
  if record['status']!='COMPLETED':continue
  pp=folder/'validation_predictions_private.npz'
  if sha(pp)!=record['validation_predictions_sha256']:raise ValueError('Stored probability checksum mismatch')
  with np.load(pp,allow_pickle=False) as z:dates=z['dates'].copy();y=z['y_true'].copy();prob=z['probability'].copy()
  expected=json.loads((ROOT/data['date_file']).read_text())['validation']['dates']
  if dates.tolist()!=expected:raise ValueError('Prediction date map mismatch')
  masks=pd.read_csv(ROOT/data['regime_file'],dtype={'Date':str}).set_index('Date').regime.reindex(dates)
  if masks.isna().any():raise ValueError('Missing frozen manual mask')
  for regime in ['Low_Vol','Mid_Vol','High_Vol']:
   selected=masks.to_numpy()==regime
   stats=supplied_prediction_metrics(y[selected],(prob[selected]>.5).astype(int))
   manual.append({'run_id':identifier,'source_stage':stage,'origin':origin,'seed':seed,'candidate':candidate,'model':model,'regime_type':'manual','regime':regime,
                  'threshold_partition':'train','thresholds_refit_on_validation':False,**stats})
 df=pd.DataFrame(rows);df.to_csv(ROOT/'manifests/step3b_runs.csv',index=False)
 idcols=['run_id','source_stage','origin','seed','effective_seed','candidate','model','status','train_samples','validation_samples','validation_class0','validation_class1','epochs','best_epoch','degenerate_prediction_epochs','degenerate_epoch_ratio','stopped_early','prediction_status']
 values=['validation_BA','macro_f1','accuracy','recall0','recall1','brier','prediction_positive_rate']
 for k in values:
  if k not in df:df[k]=np.nan
 df[idcols+values].to_csv(ROOT/'manifests/step3b_metrics.csv',index=False)
 pd.DataFrame(histories).to_csv(ROOT/'manifests/step3b_epoch_history.csv',index=False)
 manualdf=pd.DataFrame(manual);manualdf.to_csv(ROOT/'manifests/step3b_manual_regime_metrics.csv',index=False)
 completed=df[df.status=='COMPLETED'].copy()
 # Every planned group appears even when a member fails. No missing metric is filled with zero.
 seed_rows=[]
 for origin in ['O1','O2']:
  for candidate in ['A','B']:
   for model in c['models']:
    sub=df[(df.origin==origin)&(df.candidate==candidate)&(df.model==model)];valid=sub[sub.status=='COMPLETED']
    row={'origin':origin,'candidate':candidate,'model':model,'planned_seeds':2,'completed_seeds':len(valid),'status':'PASS_DESCRIPTIVE_N2' if len(valid)==2 else 'INCOMPLETE','std_ddof':1}
    for metric in METRICS:
     valueset=pd.to_numeric(valid[metric],errors='coerce').dropna();row[metric+'_mean']=float(valueset.mean()) if len(valueset) else None;row[metric+'_std']=float(valueset.std(ddof=1)) if len(valueset)>1 else None
     for seed in [2,12]:
      item=valid[valid.seed==seed];row[metric+'_seed'+str(seed)]=float(item[metric].iloc[0]) if len(item) and pd.notna(item[metric].iloc[0]) else None
     a=row[metric+'_seed2'];b=row[metric+'_seed12'];row[metric+'_delta_12_minus_2']=b-a if a is not None and b is not None else None
    seed_rows.append(row)
 pd.DataFrame(seed_rows).to_csv(ROOT/'manifests/step3b_seed_stability.csv',index=False)
 origin_rows=[];price_rows=[]
 for candidate in ['A','B']:
  for seed in [2,12]:
   for model in c['models']:
    sub=completed[(completed.candidate==candidate)&(completed.seed==seed)&(completed.model==model)];row={'candidate':candidate,'seed':seed,'model':model,'completed_origins':len(sub),'causal_or_confirmatory_claim':False}
    for metric in METRICS:
     vals={o:float(sub[sub.origin==o][metric].iloc[0]) if len(sub[sub.origin==o]) else None for o in ['O1','O2']}
     for o,value in vals.items():row[metric+'_'+o]=value
     row[metric+'_delta_O2_minus_O1']=vals['O2']-vals['O1'] if all(v is not None for v in vals.values()) else None
    origin_rows.append(row)
 pd.DataFrame(origin_rows).to_csv(ROOT/'manifests/step3b_origin_stability.csv',index=False)
 for origin in ['O1','O2']:
  for seed in [2,12]:
   for model in c['models']:
    sub=completed[(completed.origin==origin)&(completed.seed==seed)&(completed.model==model)];row={'origin':origin,'seed':seed,'model':model,'completed_prices':len(sub),'price_choice_made':False}
    for metric in METRICS:
     v={p:float(sub[sub.candidate==p][metric].iloc[0]) if len(sub[sub.candidate==p]) else None for p in ['A','B']}
     row[metric+'_A']=v['A'];row[metric+'_B']=v['B'];row[metric+'_delta_B_minus_A']=v['B']-v['A'] if all(x is not None for x in v.values()) else None
    price_rows.append(row)
 pd.DataFrame(price_rows).to_csv(ROOT/'manifests/step3b_price_sensitivity.csv',index=False)
 df[df.model=='LTC'].to_csv(ROOT/'manifests/step3b_LTC_diagnostics.csv',index=False)
 if len(manualdf):
  aggregate=[]
  for keys,group in manualdf.groupby(['origin','candidate','model','regime']):
   row=dict(zip(['origin','candidate','model','regime'],keys));row['reported_seeds']=len(group);row['metric_valid_seeds']=int(group.balanced_accuracy.notna().sum());row['n_per_seed']=int(group.n.iloc[0]);row['n_class0_per_seed']=int(group.n_class0.iloc[0]);row['n_class1_per_seed']=int(group.n_class1.iloc[0])
   for name in ['balanced_accuracy','macro_f1','recall_class0','recall_class1']:
    v=pd.to_numeric(group[name],errors='coerce').dropna();row[name+'_mean']=float(v.mean()) if len(v) else None;row[name+'_std_ddof1']=float(v.std(ddof=1)) if len(v)>1 else None
   aggregate.append(row)
  pd.DataFrame(aggregate).to_csv(ROOT/'manifests/step3b_manual_regime_summary.csv',index=False)
 write_summary={'all_combinations':40,'reused_STEP3A':10,'new_planned_STEP3B':30,'completed_total':int((df.status=='COMPLETED').sum()),'failed_total':int(df.status.str.startswith('FAILED').sum()),'blocked_total':int(df.status.eq('BLOCKED').sum()),'source_stage_counts':df.source_stage.value_counts().to_dict(),'manual_metric_rows':len(manualdf),'manual_single_class_or_empty_rows':int(manualdf.status.ne('PASS').sum()) if len(manualdf) else 0,'sample_std_ddof':1,'two_seed_std_is_exploratory_only':True,'source_model_seed_selected':False,'HMM_fit':False,'independent_Test_evaluation':False,'original_and_new_results_separated':True}
 (ROOT/'manifests/step3b_analysis_summary.json').write_text(json.dumps(write_summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(write_summary))
