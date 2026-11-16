"""Audit saved O3 results only. No model execution, Test data or statistical p-values."""
from pathlib import Path
import sys,json,hashlib,unittest
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
class O3Results(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((R/'manifests/step4a1_execution_manifest.json').read_text());cls.g=json.loads((R/'manifests/step4a1_preflight.json').read_text());cls.c=json.loads((R/'configs/step4a1_o3_pilot_config.json').read_text());cls.df=pd.read_csv(R/'manifests/step4a1_runs.csv');cls.folder=R/cls.m['run_directory']
 def test_01_exact20_new60_diagnostic(self):
  self.assertEqual(len(self.df),20);self.assertTrue(self.df.run_id.is_unique);self.assertTrue(self.df.identity_with_config_sha256.is_unique);a=pd.read_csv(R/'manifests/step4a1_all60_diagnostic_metrics.csv');self.assertEqual(len(a),60);self.assertTrue(a.run_id.is_unique);self.assertEqual(self.m['new_completed']+self.m['new_failed']+self.m['new_blocked']+self.m['new_interrupted'],20)
 def test_02_approved_origin_seed_model_offsets(self):
  self.assertEqual(set(self.df.origin),{'O3'});self.assertEqual(set(self.df.seed),{2,12});self.assertEqual(set(self.df.candidate),{'A','B'});self.assertEqual(set(self.df.model),set(self.c['models']))
  for x in self.df.itertuples():self.assertEqual(x.effective_seed,x.seed+self.c['model_seed_offsets'][x.model]);self.assertEqual(x.config_sha256,self.m['config_sha256'])
 def test_03_old40_hashes_unchanged(self):
  for x in self.g['old40_preserved_hashes']:self.assertEqual(sha(R/x['file']),x['sha256'])
  self.assertFalse(self.m['old40_reexecuted'])
 def test_04_master_and_frozen_sources_identical(self):
  self.assertEqual(sha(R/'configs/step3c_master_experiment_config.json'),self.c['master_config_sha256'])
  for x in self.c['implementation_artifacts']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_05_no_future_prices_or_label_end(self):
  for d in self.g['datasets']['O3'].values():
   dates=json.loads((R/d['date_file']).read_text());m=d['metadata'];self.assertEqual(m['price_end'],'2022-12-29');self.assertEqual(m['train_purged'],20);self.assertEqual(m['validation_unknown_excluded'],20);self.assertLess(m['train_max_label_end'],'2022-01-03')
   for part in dates.values():self.assertTrue(all(t<='2022-12-29' for t in part['dates']+part['label_end']))
 def test_06_scaler_only_retained_train_input_union(self):
  for d in self.g['datasets']['O3'].values():
   m=d['metadata'];self.assertEqual(m['scaler']['fit_rows'],2902);self.assertEqual(m['scaler']['fit_start'],'2010-03-03');self.assertEqual(m['scaler']['fit_end'],'2021-12-02');self.assertEqual(m['scaler']['feature_order'],['Log_Ret','Disparity'])
 def test_07_earlystop_first_max_BA_and_counter(self):
  for x in self.df.itertuples():
   if x.status!='COMPLETED':continue
   h=json.loads((R/x.source_directory/'history.json').read_text());score=-1.;count=0;be=None
   for y in h:
    if y['validation_BA']>score:score=y['validation_BA'];be=y['epoch'];count=0
    else:count+=1
    self.assertEqual(count,y['early_stopping_counter']);self.assertLessEqual(count,10)
   self.assertEqual(be,x.best_epoch);self.assertEqual(len(h),x.epochs);self.assertLessEqual(len(h),100)
   if len(h)<100:self.assertEqual(count,10)
 def test_08_history_finite_and_all_epoch_diagnostics(self):
  for x in self.df.itertuples():
   if x.status!='COMPLETED':continue
   h=pd.read_json(R/x.source_directory/'history.json');cols=['train_loss','validation_loss','validation_BA','macro_f1','recall0','recall1','brier','prediction_positive_rate'];self.assertTrue(np.isfinite(h[cols].to_numpy()).all());bad=int(h.prediction_status.eq('DEGENERATE_PREDICTION').sum());self.assertEqual(bad,x.degenerate_prediction_epochs);self.assertAlmostEqual(bad/len(h),x.degenerate_epoch_ratio)
 def test_09_optimizer_scheduler_budget46_per_epoch(self):
  for x in self.df.itertuples():
   if x.status!='COMPLETED':continue
   h=json.loads((R/x.source_directory/'history.json').read_text());self.assertTrue(all(y['optimizer_steps_this_epoch']==46 for y in h));self.assertEqual(h[-1]['scheduler_steps_total'],46*len(h))
 def test_10_checkpoint_reload_logits_rng_audit(self):
  for j in self.m['new_records'].values():
   if j['status']!='COMPLETED':continue
   self.assertTrue(j['checkpoint_restore']);self.assertTrue(j['RNG_restore_exact']);self.assertTrue(j['epoch1_resume_roundtrip']);v=j['postfit_checkpoint_audit'];self.assertEqual(v['status'],'PASS');self.assertTrue(v['best_checkpoint_logits_equal_two_independent_restores']);self.assertTrue(v['best_probability_equal_completed_fit']);self.assertTrue(v['full_model_optimizer_scheduler_earlystop_RNG_roundtrip']);self.assertEqual(v['additional_optimizer_updates'],0);self.assertEqual(v['logits_shape'],[226,2]);p=self.folder/'jobs'/j['run_id'];self.assertEqual(sha(p/'checkpoint_verification.json'),j['postfit_checkpoint_audit_sha256']);self.assertEqual(sha(p/'best.pt'),j['best_checkpoint_sha256']);self.assertEqual(sha(p/'latest.pt'),j['latest_checkpoint_sha256'])
 def test_11_manual_null_policy_and_support(self):
  a=pd.read_csv(R/'manifests/step4a1_manual_regime_metrics.csv');self.assertTrue(a.threshold_partition.eq('train').all());self.assertFalse(a.threshold_refit_on_validation.any());self.assertTrue(a.groupby('run_id').n.sum().eq(226).all());self.assertTrue((a.n==a.n_class0+a.n_class1).all());one=(a.n_class0==0)|(a.n_class1==0);self.assertTrue(a.loc[one,'balanced_accuracy'].isna().all());self.assertTrue(a.loc[one,'macro_f1'].isna().all())
 def test_12_no_Test_GPU_HMM_and_future_access(self):
  for key in ['Test_evaluation','GPU','HMM_fit','full_5Origin10Seed','Ablation','model_hyperparameters_changed_after_results','source_model_seed_selected_using_validation']:self.assertFalse(self.m[key])
  for x in self.m['new_records'].values():
   if x['status']!='COMPLETED':continue
   self.assertEqual(x['independent_Test_rows_used'],0);self.assertEqual(x['2026_used'],0);self.assertEqual(x['file_access_barrier']['forbidden_access_attempts'],0)
 def test_13_seed_summary_n2_ddof1_no_seed_pooling(self):
  a=pd.read_csv(R/'manifests/step4a1_seed_stability.csv')
  for x in a.itertuples():
   v=self.df[(self.df.candidate==x.candidate)&(self.df.model==x.model)&(self.df.status=='COMPLETED')].validation_BA.dropna();self.assertEqual(len(v),x.completed_seeds)
   if len(v)==2:self.assertAlmostEqual(v.std(ddof=1),x.validation_BA_std)
  s=json.loads((R/'manifests/step4a1_analysis_summary.json').read_text());self.assertFalse(s['price_source_selected']);self.assertEqual(s['confirmatory_pvalues'],0)
 def test_14_all_existing_files_preserved(self):
  before={x['file']:x['sha256'] for x in json.loads((R/'provenance/step4a1_preservation.json').read_text())['artifacts']}
  for p,h in before.items():self.assertEqual(sha(R/p),h,p)
if __name__=='__main__':
 z=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(O3Results));bad={t._testMethodName:e for t,e in z.failures+z.errors};names=sorted(n for n in dir(O3Results) if n.startswith('test_'));(R/'manifests/step4a1_postrun_tests.json').write_text(json.dumps({'passed':z.testsRun-len(bad),'failed':len(bad),'tests':[{'id':n,'status':'FAIL' if n in bad else 'PASS',**({'error':bad[n]} if n in bad else {})} for n in names]},indent=2)+'\n');sys.exit(0 if z.wasSuccessful() else 1)
