"""Post-run expansion audits. Uses only stored Origin-specific Validation diagnostics."""
from pathlib import Path
import sys,json,hashlib,unittest
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.manual_evaluation import supplied_prediction_metrics
class ExpansionResults(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((R/'manifests/step3b_execution_manifest.json').read_text());cls.g=json.loads((R/'manifests/step3b_preflight.json').read_text());cls.d=pd.read_csv(R/'manifests/step3b_runs.csv');cls.run_directory=R/cls.m['run_directory']
 def test_01_40_unique_and30new10reused(self):
  self.assertEqual(len(self.d),40);self.assertTrue(self.d.run_id.is_unique);self.assertEqual(self.d.source_stage.value_counts().to_dict(),{'STEP3B_NEW':30,'STEP3A_REUSED':10});self.assertFalse(self.m['old10_reexecuted'])
 def test_02_original_completion_and_checkpoints_unchanged(self):
  for row in self.g['preserved_hash_checks']:self.assertEqual(hashlib.sha256((R/row['file']).read_bytes()).hexdigest(),row['sha256'])
 def test_03_no_new_O1_seed2_and_exact_grid(self):
  new=self.d[self.d.source_stage=='STEP3B_NEW'];self.assertFalse(((new.origin=='O1')&(new.seed==2)).any());self.assertEqual(set(new.seed),{2,12});self.assertEqual(set(new.origin),{'O1','O2'});self.assertEqual(self.d.groupby(['origin','seed','candidate']).size().tolist(),[5]*8)
 def test_04_origin_cutoffs_purge_scaler_and_support(self):
  for origin in ['O1','O2']:
   for p in ['A','B']:
    meta=self.g['datasets'][origin][p]['metadata'];self.assertEqual(meta['train_purged'],20);self.assertEqual(meta['validation_unknown_excluded'],20);self.assertEqual(meta['train_cutoff_violations'],0);self.assertEqual(meta['validation_future_endpoint_violations'],0);self.assertLess(meta['scaler']['fit_end'],meta['validation_boundary_start']);self.assertEqual(sum(meta['class_counts']['validation'].values()),228)
 def test_05_best_first_max_and_frozen_earlystop(self):
  for row in self.d.itertuples():
   if row.status!='COMPLETED':continue
   h=json.loads((R/row.source_directory/'history.json').read_text());maximum=max(x['validation_BA'] for x in h);best=next(x['epoch'] for x in h if x['validation_BA']==maximum);self.assertEqual(best,row.best_epoch);self.assertLessEqual(len(h),100);self.assertEqual(len(h),row.epochs)
   score=-1.;counter=0
   for x in h:
    if x['validation_BA']>score:score=x['validation_BA'];counter=0
    else:counter+=1
    self.assertEqual(counter,x['early_stopping_counter']);self.assertLessEqual(counter,10)
   if len(h)<100:self.assertEqual(counter,10)
 def test_06_every_case_reported_no_failed_seed_replacement(self):
  self.assertEqual(len(self.m['new_records']),30);self.assertEqual(self.m['new_completed']+self.m['new_failed']+self.m['new_blocked']+self.m['new_interrupted'],30)
  self.assertTrue(self.d.status.isin(['COMPLETED','FAILED_EXCEPTION','FAILED_DIVERGENCE','BLOCKED']).all())
 def test_07_new_checkpoints_epoch_batch_rng_hashes(self):
  import torch
  for j in self.m['new_records'].values():
   if j['status']!='COMPLETED':continue
   p=self.run_directory/'jobs'/j['run_id'];self.assertTrue(j['checkpoint_restore']);self.assertTrue(j['RNG_restore_exact']);self.assertTrue(j['epoch1_resume_roundtrip'])
   for file,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:self.assertEqual(hashlib.sha256((p/file).read_bytes()).hexdigest(),j[key])
   payload=torch.load(p/'latest.pt',map_location='cpu',weights_only=True);self.assertEqual(payload['batch_position'],0);self.assertEqual(payload['job']['origin'],j['origin']);self.assertEqual(payload['job']['seed'],j['seed']);self.assertEqual(set(payload['RNG']),{'Python','NumPy','Torch_CPU','DataLoader'});self.assertIn('environment_sha256',payload)
 def test_08_worker_origin_barriers_and_scope(self):
  for j in self.m['new_records'].values():
   if j['status']!='COMPLETED':continue
   self.assertEqual(j['file_access_barrier']['forbidden_access_attempts'],0);self.assertEqual(j['independent_Test_rows_used'],0);self.assertEqual(j['2026_used'],0)
  for key in ['Test_evaluation','GPU','HMM_fit','full_5Origin10Seed','Ablation','model_hyperparameters_changed_after_results','source_model_seed_selected_using_validation']:self.assertFalse(self.m[key])
 def test_09_degenerate_ratio_and_flags(self):
  for row in self.d.itertuples():
   if row.status!='COMPLETED':continue
   h=json.loads((R/row.source_directory/'history.json').read_text());bad=sum(x['prediction_status']=='DEGENERATE_PREDICTION' for x in h);self.assertEqual(row.degenerate_prediction_epochs,bad);self.assertAlmostEqual(row.degenerate_epoch_ratio,bad/len(h))
 def test_10_manual_support_and_singleclass_null(self):
  m=pd.read_csv(R/'manifests/step3b_manual_regime_metrics.csv');self.assertEqual(set(m.regime_type),{'manual'});self.assertTrue(m.threshold_partition.eq('train').all());self.assertFalse(m.thresholds_refit_on_validation.any());self.assertTrue(m.groupby('run_id').n.sum().eq(228).all());self.assertTrue((m.n==m.n_class0+m.n_class1).all());one=(m.n_class0==0)|(m.n_class1==0);self.assertTrue(m.loc[one,'balanced_accuracy'].isna().all());self.assertTrue(m.loc[one,'macro_f1'].isna().all())
 def test_11_manual_metrics_same_probabilities_and_date_keys(self):
  table=pd.read_csv(R/'manifests/step3b_manual_regime_metrics.csv')
  for row in self.d.itertuples():
   if row.status!='COMPLETED':continue
   with np.load(R/row.source_directory/'validation_predictions_private.npz',allow_pickle=False) as z:dates=z['dates'].copy();y=z['y_true'].copy();p=z['probability'].copy()
   info=self.g['datasets'][row.origin][row.candidate];expected=json.loads((R/info['date_file']).read_text())['validation']['dates'];self.assertEqual(dates.tolist(),expected)
   masks=pd.read_csv(R/info['regime_file'],dtype={'Date':str}).set_index('Date').regime.reindex(dates)
   for regime in ['Low_Vol','Mid_Vol','High_Vol']:
    take=masks.to_numpy()==regime;stats=supplied_prediction_metrics(y[take],(p[take]>.5).astype(int));record=table[(table.run_id==row.run_id)&(table.regime==regime)].iloc[0]
    if stats['balanced_accuracy'] is None:self.assertTrue(pd.isna(record.balanced_accuracy))
    else:self.assertAlmostEqual(record.balanced_accuracy,stats['balanced_accuracy'],places=14)
 def test_12_seed_std_ddof1_n2_and_no_confirmatory_claim(self):
  summary=pd.read_csv(R/'manifests/step3b_seed_stability.csv')
  for s in summary.itertuples():
   x=self.d[(self.d.origin==s.origin)&(self.d.candidate==s.candidate)&(self.d.model==s.model)&(self.d.status=='COMPLETED')].validation_BA.dropna();self.assertEqual(len(x),s.completed_seeds)
   if len(x)==2:self.assertAlmostEqual(s.validation_BA_std,x.std(ddof=1),places=14)
   else:self.assertTrue(pd.isna(s.validation_BA_std))
  a=json.loads((R/'manifests/step3b_analysis_summary.json').read_text());self.assertTrue(a['two_seed_std_is_exploratory_only']);self.assertFalse(a['source_model_seed_selected'])
 def test_13_reused_metrics_exactly_step3A(self):
  old=pd.read_csv(R/'manifests/step3a_pilot_metrics.csv');d=pd.read_csv(R/'manifests/step3b_metrics.csv');reused=d[d.source_stage=='STEP3A_REUSED']
  for x in old.itertuples():
   r=reused[(reused.candidate==x.candidate)&(reused.model==x.model)].iloc[0]
   for key in ['validation_BA','macro_f1','accuracy','recall0','recall1','brier','prediction_positive_rate']:self.assertAlmostEqual(r[key],getattr(x,key),places=14)
 def test_14_frozen_sources_production_flags_and_source_status(self):
  for row in self.m['implementation_artifacts']:self.assertEqual(hashlib.sha256((R/row['file']).read_bytes()).hexdigest(),row['sha256'])
  c=json.loads((R/'configs/experiment_config.json').read_text());self.assertFalse(c['training_enabled']);self.assertFalse(c['hmm_fit_enabled']);self.assertEqual(self.m['source_status'],'BOTH_UNVERIFIED');self.assertEqual(self.m['production_PIT_status'],'BLOCKED');self.assertIsNone(self.m['main_price_candidate_selected'])
 def test_15_rebuild_origin_arrays_scaler_and20session_labels(self):
  from kospi200.rolling_pilot_data import prepare_origin
  for origin in ['O1','O2']:
   for candidate in ['A','B']:
    info=self.g['datasets'][origin][candidate];prices=pd.read_csv(R/info['price_file'],float_precision='round_trip');dates=pd.to_datetime(prices.Date);sessions=pd.DataFrame({'Date':dates,'session_id':np.arange(len(dates))})
    rebuilt,meta,date_information,regimes=prepare_origin(prices,sessions,origin=origin,calendar_source='audit_rebuild_staged_official_prefix',calendar_sha256=self.g['full_calendar_sha256'])
    with np.load(R/info['array_file'],allow_pickle=False) as z:
     for part in ['train','validation']:
      self.assertTrue(np.array_equal(rebuilt[part][0],z[part+'_x']));self.assertTrue(np.array_equal(rebuilt[part][1],z[part+'_y']))
    self.assertEqual(meta['scaler'],info['metadata']['scaler']);self.assertEqual(date_information,json.loads((R/info['date_file']).read_text()))
 def test_16_allowed_prefix_future_perturbation_and_exact_update_budget(self):
  from kospi200.data import local_features,labels_on_calendar,Calendar
  for origin in ['O1','O2']:
   for candidate in ['A','B']:
    info=self.g['datasets'][origin][candidate];p=pd.read_csv(R/info['price_file']);dates=pd.DatetimeIndex(pd.to_datetime(p.Date));close=pd.Series(p.Close.to_numpy(),index=dates);cutoff=pd.Timestamp(info['metadata']['validation_first_sample']);changed=close.copy();changed.loc[changed.index>cutoff]*=1.12345
    self.assertTrue(local_features(close).loc[:cutoff].equals(local_features(changed).loc[:cutoff]))
    cal=Calendar(dates,'staged_official_prefix',self.g['full_calendar_sha256'],True);a=labels_on_calendar(close,cal,20);b=labels_on_calendar(changed,cal,20);past=a.label_end.le(cutoff);self.assertTrue(a.loc[past].equals(b.loc[past]));self.assertEqual(a.Target.tail(20).isna().sum(),20)
  for row in self.d[self.d.source_stage=='STEP3B_NEW'].itertuples():
   if row.status!='COMPLETED':continue
   h=json.loads((R/row.source_directory/'history.json').read_text());expected=(row.train_samples+63)//64
   self.assertTrue(all(x['optimizer_steps_this_epoch']==expected for x in h));self.assertEqual(h[-1]['scheduler_steps_total'],expected*len(h))
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExpansionResults))
 failures={case._testMethodName:message for case,message in result.failures+result.errors}
 names=sorted(name for name in dir(ExpansionResults) if name.startswith('test_'))
 tests=[{'id':name,'status':'FAIL' if name in failures else 'PASS',**({'error':failures[name]} if name in failures else {})} for name in names]
 (R/'manifests/step3b_postrun_tests.json').write_text(json.dumps({'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors),'scope':'Stored Origin-specific Validation/checkpoint/aggregation checks; no refit or Test evaluation','tests':tests},indent=2)+'\n')
 sys.exit(0 if result.wasSuccessful() else 1)
