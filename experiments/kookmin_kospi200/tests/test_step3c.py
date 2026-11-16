"""Preparation-only checks. No model import, checkpoint load, learning or Test evaluation."""
from pathlib import Path
import sys,json,hashlib,unittest,itertools,importlib.metadata,tempfile
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R))
from kospi200.master_protocol import job_grid,comparison_family,require_execution_authorization
from kospi200.master_data import read_origin_prefix,prepare_origin
from kospi200.master_statistics import metric,correct_frozen_family
from kospi200.data import BlockedError

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class PreparedProtocol(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'configs/step3c_master_experiment_config.json').read_text());cls.g=json.loads((R/'manifests/step3c_prepared_inputs.json').read_text());cls.reuse=pd.read_csv(R/'manifests/step3c_reuse_check.csv');cls.plan=pd.read_csv(R/'manifests/step3c_job_plan.csv')
 def test_01_all_execution_disabled_and_authorization_rejected(self):
  for k in ['training_enabled','hmm_fit_enabled','gpu_enabled','pilot_execution_enabled','new_fit_execution_enabled','production_gate_override']:self.assertIs(self.c[k],False)
  with self.assertRaises(BlockedError):require_execution_authorization(self.c,{'approved':True},self.g,self.g['jobs'][0],'','','')
  self.assertNotIn('torch',sys.modules);self.assertNotIn('hmmlearn',sys.modules)
 def test_02_exact50040reuse460new_grid(self):
  self.assertEqual(len(job_grid(self.c['model_seed_offsets'])),500);self.assertEqual(len(self.g['jobs']),460);self.assertEqual(len(self.reuse),40);self.assertTrue(self.plan.run_id.is_unique);self.assertEqual(self.plan.action.value_counts().to_dict(),{'PLANNED_NOT_AUTHORIZED':460,'REUSE_COMPLETED':40});self.assertEqual(set(self.g['datasets']),{'O1','O2','O3','O4','O5'})
 def test_03_completed40_file_hashes_no_reexecution(self):
  records=self.g['reused_completed'];self.assertEqual(len(records),40)
  for x in records:
   q=R/x['source_directory'];v=x['record']
   for name,key in [('best.pt','best_checkpoint_sha256'),('latest.pt','latest_checkpoint_sha256'),('history.json','history_sha256'),('validation_predictions_private.npz','validation_predictions_sha256')]:self.assertEqual(sha(q/name),v[key])
   self.assertEqual(v['status'],'COMPLETED');self.assertEqual(self.g['datasets'][x['origin']][x['candidate']]['array_sha256'],v['input_data_sha256'])
 def test_04_learning_kernel_identical_and_artifacts_frozen(self):
  a=(R/'runtime/step3b_worker.py').read_text().split(' def equal(x,y):',1)[1];b=(R/'runtime/step3c_worker.py').read_text().split(' def equal(x,y):',1)[1];self.assertEqual(a,b);self.assertEqual(hashlib.sha256(a.encode()).hexdigest(),self.c['learning_kernel_sha256'])
  for x in self.c['implementation_artifacts']:self.assertEqual(sha(R/x['file']),x['sha256'])
 def test_05_original_settings_features_offsets_seeds(self):
  old=json.loads((R/'configs/step3b_pilot_config.json').read_text());self.assertEqual(self.c['model_settings'],old['model_settings']);self.assertEqual(self.c['original_definition_hashes'],old['original_definition_hashes']);self.assertEqual(self.c['model_seed_offsets'],old['model_seed_offsets']);self.assertEqual(self.c['seeds'],[2,12,22,32,42,52,62,72,82,92]);self.assertEqual(self.c['feature_order'],['Log_Ret','Disparity']);self.assertEqual(self.c['seed_offsets_full']['LOG']['LTC'],402)
 def test_06_dataset_shapes_finite_and_source_hashes(self):
  for origin,parts in self.g['datasets'].items():
   for candidate,d in parts.items():
    for filename,key in [('array_file','array_sha256'),('metadata_file','metadata_sha256'),('date_file','date_sha256'),('source_file','source_sha256')]:self.assertEqual(sha(R/d[filename]),d[key])
    with np.load(R/d['array_file'],allow_pickle=False) as z:
     for part in ['train','validation']:
      self.assertEqual(z[part+'_x'].shape,(d['metadata'][part+'_samples'],20,2));self.assertEqual(z[part+'_x'].dtype,np.float32);self.assertTrue(np.isfinite(z[part+'_x']).all());self.assertEqual(set(np.unique(z[part+'_y'])),{0,1})
 def test_07_official20session_endpoints_and_cutoffs(self):
  calendar=pd.read_csv(R/'manifests/krx_sessions_2010_2025.csv');self.assertEqual(len(calendar),3939);lookup=dict(zip(calendar.Date,calendar.session_id))
  for origin,parts in self.g['datasets'].items():
   for d in parts.values():
    meta=d['metadata'];dates=json.loads((R/d['date_file']).read_text());self.assertEqual(meta['train_purged'],20);self.assertEqual(meta['validation_unknown_excluded'],20)
    for part in ['train','validation']:
     for t,end in zip(dates[part]['dates'],dates[part]['label_end']):self.assertEqual(lookup[end]-lookup[t],20);self.assertLessEqual(end,f"{d['validation_year']}-12-31")
    self.assertLess(meta['train_max_label_end'],meta['validation_boundary_start']);self.assertEqual(meta['train_cutoff_violations'],0)
 def test_08_reconstructed_arrays_scaler_train_only(self):
  for origin,parts in self.g['datasets'].items():
   for d in parts.values():
    p=pd.read_csv(R/d['price_file'],float_precision='round_trip');dates=pd.to_datetime(p.Date);sessions=pd.DataFrame({'Date':dates,'session_id':np.arange(len(dates))});data,meta,di,reg=prepare_origin(p,sessions,origin=origin,calendar_source='verified_staged_prefix',calendar_sha256=self.g['calendar_sha256'])
    self.assertEqual(meta['scaler'],d['metadata']['scaler']);self.assertLess(meta['scaler']['fit_end'],meta['validation_boundary_start'])
    with np.load(R/d['array_file'],allow_pickle=False) as z:
     for part in ['train','validation']:self.assertTrue(np.array_equal(data[part][0],z[part+'_x']));self.assertTrue(np.array_equal(data[part][1],z[part+'_y']))
 def test_09_future_prefix_read_stops_before_postvalidation(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'sentinel.csv';p.write_text('Date,Close\n2024-12-27,1\n2024-12-30,2\n2025-01-02,FORBIDDEN\n2026-01-02,FORBIDDEN\n');self.assertEqual(len(read_origin_prefix(p,pd.to_datetime(['2024-12-27','2024-12-30']),2024)),2)
 def test_10_test_metadata_only_O5_unknown20(self):
  p=pd.read_csv(R/'manifests/step3c_origin_plan.csv');t=p[p.partition=='test_PLANNED_NOT_EVALUATED'];self.assertEqual(len(t),10);self.assertTrue(t.metadata_basis.str.contains('NO_TEST_EVALUATION').all());self.assertTrue(t[t.origin=='O5'].unknown_excluded.eq(20).all());self.assertTrue(t[t.origin=='O5'].samples.eq(222).all());self.assertEqual(self.g['Test_evaluations'],0)
 def test_11_fixed_statistical_families_no_seed_pooling(self):
  b=self.c['bootstrap'];self.assertEqual(len(comparison_family()),20);self.assertEqual(b['primary_family'],comparison_family());self.assertEqual(b['block_lengths'],[20,40,60]);self.assertEqual(b['replicates'],10000);self.assertEqual(b['secondary_family_size'],80);self.assertEqual(b['origin_diagnostic_family_size'],100)
  y=np.array([0,1,0,1]);p=np.repeat(np.array([.1,.8,.2,.9])[:,None],10,axis=1);self.assertEqual(metric(y,p,'balanced_accuracy'),1);self.assertEqual(metric(y,p,'macro_f1'),1);self.assertTrue(np.isnan(metric(np.ones(4),p,'macro_f1')))
  with self.assertRaises(BlockedError):correct_frozen_family([],expected_size=20)
 def test_12_budget_definitions_and_no_full_channel_reuse(self):
  b=pd.read_csv(R/'manifests/step3c_fit_budget.csv').set_index('scenario');self.assertEqual(b.loc['F1_AB','planned_new_fits'],460);self.assertEqual(b.loc['FULL_RAW_LOG_AB','planned_total_fits'],1000);self.assertEqual(b.loc['ABLATION6_TWO_CHANNELS_AB_NAIVE','planned_total_fits'],6000);self.assertEqual(b.loc['LTC_RAW_LOG_AB_SUBSET','planned_total_fits'],200);self.assertEqual(self.c['ensemble']['fit_cost'],0);self.assertFalse(self.c['ensemble']['F1_only_is_original_ensemble_reproduction'])
 def test_13_manual_reference_and_mask_no_input_vol(self):
  for parts in self.g['datasets'].values():
   for d in parts.values():
    m=d['metadata'];r=m['manual_reference'];self.assertEqual(r['quantiles'],[30,70]);self.assertEqual(r['partition'],'train');self.assertEqual(r['rows'],m['train_samples']);self.assertLess(r['train_end'],m['validation_boundary_start']);self.assertTrue(m['common_Vol_Regime_window_mask']);self.assertNotIn('Vol_Regime',m['feature_order'])
 def test_14_current_resources_and_reference_versions(self):
  r=self.c['resources_current'];self.assertEqual(Path('/sys/fs/cgroup/cpu.max').read_text().strip(),r['cpu_max']);self.assertEqual(int(Path('/sys/fs/cgroup/memory.max').read_text()),r['memory_max_bytes']);self.assertEqual({n:importlib.metadata.version(n) for n in self.c['environment_versions']},self.c['environment_versions'])
 def test_15_tau_does_not_certify_physical_day(self):
  from kospi200.master_tau import supplied_tau_snapshot
  with self.assertRaises(BlockedError):supplied_tau_snapshot(inputs=None,hidden=None,params={},lineage={})
  self.assertNotIn('torch',sys.modules)
 def test_16_existing575_files_unchanged(self):
  before={x['file']:x['sha256'] for x in json.loads((R/'provenance/step3c_preservation.json').read_text())['artifacts']}
  for p,h in before.items():self.assertEqual(sha(R/p),h,p)
 def test_17_original_ensemble_candidate_channel_and_seed_pairing(self):
  from kospi200.master_ensemble import original_lnn_composition
  from kospi200.specs import RAW,LOG
  rows=[]
  for candidate in ['A','B']:
   for model,features,offset,prob in [('LTC_RAW',RAW,401,.2),('LTC_LOG',LOG,402,.6),('RNN_RAW',RAW,101,.9)]:rows.append({'candidate':candidate,'origin':'O1','seed':2,'date':'2020-01-02','model':model,'feature_order':features,'effective_seed':2+offset,'probability':prob,'checkpoint_sha256':'fixture_only'})
  f=pd.DataFrame(rows);out=original_lnn_composition(f);self.assertEqual(len(out),2);self.assertTrue(np.allclose(out['LNN Ensemble'],.4));self.assertTrue(np.allclose(out.Hybrid_SOTA,.55))
  bad=f.copy();bad.at[0,'feature_order']=LOG
  with self.assertRaises(BlockedError):original_lnn_composition(bad)
 def test_18_holm_predeclared_whole_family(self):
  rows=[{'candidate':x['candidate'],'model_a':x['model_a'],'model_b':x['model_b'],'metric':'balanced_accuracy','block_length':20,'p_approx_centered':.5} for x in comparison_family()]
  self.assertEqual(len(correct_frozen_family(rows,expected_size=20)),20)
  with self.assertRaises(BlockedError):correct_frozen_family(rows[:-1],expected_size=20)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PreparedProtocol));fail={x._testMethodName:y for x,y in result.failures+result.errors};names=sorted(x for x in dir(PreparedProtocol) if x.startswith('test_'));record={'stage':'STEP3C','passed':result.testsRun-len(fail),'failed':len(fail),'scope':'data/synthetic mathematics/static source/byte hashes only; model loads/forward/fit/Test evaluation0','tests':[{'id':n,'status':'FAIL' if n in fail else 'PASS',**({'error':fail[n]} if n in fail else {})} for n in names]};(R/'manifests/step3c_test_results.json').write_text(json.dumps(record,indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
