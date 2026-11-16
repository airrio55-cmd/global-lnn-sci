"""Stored O3 Validation diagnostics only; no learning, Test data or p-values."""
from pathlib import Path
import json,hashlib,sys
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.manual_evaluation import supplied_prediction_metrics
METRICS=['validation_BA','macro_f1','accuracy','recall0','recall1','brier','prediction_positive_rate','best_epoch','degenerate_epoch_ratio']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
 m=json.loads((R/'manifests/step4a2_execution_manifest.json').read_text());g=json.loads((R/'manifests/step4a2_preflight.json').read_text());c=json.loads((R/'configs/step4a2_o4_o5_pilot_config.json').read_text());run=R/m['run_directory'];assert m['new_interrupted']==0
 rows=[];histories=[];manual=[]
 for job in g['jobs']:
  r=m['new_records'][job['run_id']];folder=run/'jobs'/job['run_id'];info=g['datasets'][job['origin']][job['candidate']];meta=info['metadata'];history=json.loads((folder/'history.json').read_text()) if (folder/'history.json').exists() else [];n=len(history);bad=sum(x['prediction_status']=='DEGENERATE_PREDICTION' for x in history)
  row={**job,'identity_with_config_sha256':hashlib.sha256(json.dumps([job['candidate'],job['origin'],job['seed'],job['model'],c['master_config_sha256'],m['config_sha256']]).encode()).hexdigest(),'source_stage':'STEP4A2_NEW','status':r['status'],'train_samples':meta['train_samples'],'validation_samples':meta['validation_samples'],'train_class0':meta['class_counts']['train']['0'],'train_class1':meta['class_counts']['train']['1'],'validation_class0':meta['class_counts']['validation']['0'],'validation_class1':meta['class_counts']['validation']['1'],'epochs':n,'best_epoch':r.get('best_validation_epoch'),'degenerate_prediction_epochs':bad,'degenerate_epoch_ratio':bad/n if n else None,'stopped_early':n<100 if n else None,'prediction_status':r.get('prediction_status'),'checkpoint_restore':r.get('checkpoint_restore',False),'RNG_restore_exact':r.get('RNG_restore_exact',False),'postfit_checkpoint_audit_status':r.get('postfit_checkpoint_audit',{}).get('status','BLOCKED'),'master_config_sha256':c['master_config_sha256'],'config_sha256':m['config_sha256'],'code_sha256':m['worker_sha256'],'learning_kernel_sha256':c['learning_kernel_sha256'],'environment_sha256':c['environment_sha256'],'input_data_sha256':r.get('input_data_sha256'),'scaler_metadata_sha256':hashlib.sha256(json.dumps(meta['scaler'],sort_keys=True).encode()).hexdigest(),'best_checkpoint_sha256':r.get('best_checkpoint_sha256'),'latest_checkpoint_sha256':r.get('latest_checkpoint_sha256'),'history_sha256':r.get('history_sha256'),'postfit_checkpoint_audit_sha256':r.get('postfit_checkpoint_audit_sha256'),'source_directory':str(folder.relative_to(R)),'elapsed_training_seconds':r.get('elapsed_training_seconds'),'error':r.get('error',r.get('checkpoint_error'))};row.update(r.get('metrics',{}));row['feature_order_sha256']=hashlib.sha256(json.dumps(c['feature_order'],sort_keys=True).encode()).hexdigest();row['price_data_sha256']=info['price_sha256']
  if r['status']=='COMPLETED':
   binding={k:row[k] for k in ['run_id','identity_with_config_sha256','master_config_sha256','config_sha256','code_sha256','learning_kernel_sha256','environment_sha256','input_data_sha256','price_data_sha256','scaler_metadata_sha256','feature_order_sha256','best_checkpoint_sha256','latest_checkpoint_sha256']};bp=folder/'checkpoint_lineage_hashes.json';bp.write_text(json.dumps(binding,indent=2)+'\n');row['checkpoint_lineage_sidecar_sha256']=sha(bp)
  rows.append(row)
  best=-1.;be=None
  for h in history:
   if h['validation_BA']>best:best=h['validation_BA'];be=h['epoch']
   histories.append({'run_id':job['run_id'],'source_stage':'STEP4A2_NEW','origin':job['origin'],'candidate':job['candidate'],'seed':job['seed'],'model':job['model'],**h,'running_best_epoch':be,'running_best_validation_BA':best})
  if r['status']!='COMPLETED':continue
  if sha(folder/'validation_predictions_private.npz')!=r['validation_predictions_sha256']:raise ValueError('Private Validation probability checksum mismatch')
  with np.load(folder/'validation_predictions_private.npz',allow_pickle=False) as z:dates=z['dates'].copy();y=z['y_true'].copy();prob=z['probability'].copy()
  allowed=json.loads((R/info['date_file']).read_text())['validation']['dates'];assert dates.tolist()==allowed and max(allowed)<=meta['validation_boundary_end'];reg=pd.read_csv(R/info['regime_file'],dtype={'Date':str}).set_index('Date').regime.reindex(dates);assert not reg.isna().any()
  for name in ['Low_Vol','Mid_Vol','High_Vol']:
   take=reg.to_numpy()==name;stats=supplied_prediction_metrics(y[take],(prob[take]>.5).astype(int));manual.append({'run_id':job['run_id'],'source_stage':'STEP4A2_NEW','origin':job['origin'],'candidate':job['candidate'],'seed':job['seed'],'model':job['model'],'regime_type':'manual','regime':name,'threshold_partition':'train','threshold_refit_on_validation':False,**stats})
 df=pd.DataFrame(rows);df.to_csv(R/'manifests/step4a2_runs.csv',index=False)
 ids=['run_id','source_stage','origin','candidate','seed','effective_seed','model','status','train_samples','validation_samples','train_class0','train_class1','validation_class0','validation_class1','epochs','best_epoch','degenerate_prediction_epochs','degenerate_epoch_ratio','prediction_status','postfit_checkpoint_audit_status']
 for key in METRICS:
  if key not in df:df[key]=np.nan
 df[ids+['validation_BA','macro_f1','accuracy','recall0','recall1','brier','prediction_positive_rate']].to_csv(R/'manifests/step4a2_metrics.csv',index=False);pd.DataFrame(histories).to_csv(R/'manifests/step4a2_epoch_history.csv',index=False)
 manual=pd.DataFrame(manual);manual.to_csv(R/'manifests/step4a2_manual_regime_metrics.csv',index=False)
 agg=[]
 if len(manual):
  for keys,t in manual.groupby(['origin','candidate','model','regime']):
   row=dict(zip(['origin','candidate','model','regime'],keys));row.update({'reported_seeds':len(t),'n_per_seed':int(t.n.iloc[0]),'n_class0_per_seed':int(t.n_class0.iloc[0]),'n_class1_per_seed':int(t.n_class1.iloc[0]),'metric_valid_seeds':int(t.balanced_accuracy.notna().sum())})
   for k in ['balanced_accuracy','macro_f1','recall_class0','recall_class1']:
    v=pd.to_numeric(t[k],errors='coerce').dropna();row[k+'_mean']=float(v.mean()) if len(v) else None;row[k+'_std_ddof1']=float(v.std(ddof=1)) if len(v)>1 else None
   agg.append(row)
 pd.DataFrame(agg).to_csv(R/'manifests/step4a2_manual_regime_summary.csv',index=False)
 old=pd.read_csv(R/'manifests/step4a1_all60_diagnostic_metrics.csv');assert len(old)==60;allrows=pd.concat([old,df],ignore_index=True);assert len(allrows)==100 and allrows.run_id.is_unique;allrows.to_csv(R/'manifests/step4a2_all100_diagnostic_metrics.csv',index=False);allrows[allrows.model=='LTC'].to_csv(R/'manifests/step4a2_LTC_five_origin.csv',index=False);allrows[allrows.model=='CfC'].to_csv(R/'manifests/step4a2_CfC_five_origin.csv',index=False)
 price=[];seedrows=[]
 for origin in ['O4','O5']:
  for seed in [2,12]:
   for model in c['models']:
    t=df[(df.origin==origin)&(df.seed==seed)&(df.model==model)&(df.status=='COMPLETED')];v={'origin':origin,'seed':seed,'model':model,'completed_candidates':len(t),'price_selected':False}
    for k in METRICS:
     a=t[t.candidate=='A'][k];b=t[t.candidate=='B'][k];v[k+'_A']=float(a.iloc[0]) if len(a) else None;v[k+'_B']=float(b.iloc[0]) if len(b) else None;v[k+'_delta_B_minus_A']=v[k+'_B']-v[k+'_A'] if len(a) and len(b) else None
    price.append(v)
  for candidate in ['A','B']:
   for model in c['models']:
    t=df[(df.origin==origin)&(df.candidate==candidate)&(df.model==model)&(df.status=='COMPLETED')];v={'origin':origin,'candidate':candidate,'model':model,'completed_seeds':len(t),'std_ddof':1,'exploratory_only':True}
    for k in METRICS:
     x=pd.to_numeric(t[k],errors='coerce').dropna();v[k+'_mean']=float(x.mean()) if len(x) else None;v[k+'_std']=float(x.std(ddof=1)) if len(x)>1 else None
     for seed in [2,12]:
      z=t[t.seed==seed][k];v[k+'_seed'+str(seed)]=float(z.iloc[0]) if len(z) else None
    seedrows.append(v)
 pd.DataFrame(price).to_csv(R/'manifests/step4a2_price_sensitivity.csv',index=False);pd.DataFrame(seedrows).to_csv(R/'manifests/step4a2_seed_stability.csv',index=False)
 summary={'stage':'STEP4A2','old_completed_unchanged':60,'new_planned':40,'new_completed':m['new_completed'],'new_failed':m['new_failed'],'new_blocked':m['new_blocked'],'new_interrupted':m['new_interrupted'],'total_actual_completed':60+m['new_completed'],'new_epochs':len(histories),'new_optimizer_updates':int(sum(h['optimizer_steps_this_epoch'] for h in histories)),'new_best_checkpoint_degenerate_cases':int(df.prediction_status.eq('DEGENERATE_PREDICTION').sum()),'new_checkpoint_audits_PASS':int(df.postfit_checkpoint_audit_status.eq('PASS').sum()),'manual_rows':len(manual),'empty_or_single_actual_class_regime_rows':int(manual.status.ne('PASS').sum()) if len(manual) else 0,'price_status':'BOTH_UNVERIFIED','price_source_selected':False,'per_origin_Test_price_values_used':{'O4':0,'O5':0},'Test_evaluations':0,'HMM_fit':0,'GPU':0,'tau_forward':0,'confirmatory_pvalues':0,'2026_used':0};(R/'manifests/step4a2_analysis_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
