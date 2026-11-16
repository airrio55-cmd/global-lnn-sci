"""STEP2.8 data, static control-flow and synthetic contracts; NEVER run smoke."""
from pathlib import Path
import sys,json,unittest,copy,hashlib,ast
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R))
from kospi200.data import Calendar,BlockedError,local_features,labels_on_calendar
from kospi200.price_sensitivity import FEATURE_ORDER,CONFLICT_DATES,align_candidates,f1_structure
from kospi200.folds import train_only_scaler,window_dates
from kospi200.manual_evaluation import freeze_manual_reference,assign_manual_regimes
from kospi200.regimes import forward_filter,regime_status,hmm_training_plan
from kospi200.paired_regime_evaluation import evaluate_same_predictions
from runtime.step28_smoke_runtime import require_smoke_authorization,prepare_o1_arrays,REQUIRED_A
class Step28Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((R/'manifests/step28_price_sensitivity.json').read_text());cls.g=json.loads((R/'manifests/step28_gate_results.json').read_text());cls.c=json.loads((R/'configs/step28_smoke_config.json').read_text())
  cls.a=pd.read_csv(R/'data/derived/step28_candidate_A_close_private.csv',parse_dates=['Date'],float_precision='round_trip');cls.b=pd.read_csv(R/'data/derived/step28_candidate_B_close_private.csv',parse_dates=['Date'],float_precision='round_trip')
  sp=R/'manifests/krx_sessions_2010_2025.csv';cls.cal=Calendar(pd.DatetimeIndex(pd.read_csv(sp,parse_dates=['Date']).Date,name='Date'),'official KRX',hashlib.sha256(sp.read_bytes()).hexdigest(),True)
 def test_01_two_conflicts_recomputed_from_raw_sources(self):
  d=pd.read_csv(R/'data/derived/step28_two_price_conflicts_private.csv',parse_dates=['Date'],float_precision='round_trip');self.assertEqual(set(d.Date),set(CONFLICT_DATES));np.testing.assert_allclose(d.absolute_difference,(d.Close_excel-d.Close_original).abs(),rtol=0,atol=1e-12);np.testing.assert_allclose(d.relative_difference_original_denominator,d.absolute_difference/d.Close_original.abs());self.assertTrue(d.rounded_2dp_absolute_difference.gt(0).all());self.assertTrue(d.confirmed_supplier.eq('UNKNOWN').all())
 def test_02_remaining3892_float32_explanation(self):
  d=self.m['price_comparison'];self.assertEqual(d['remaining_dates_float32_roundtrip_matches'],3892);self.assertEqual(d['remaining_precision_only_differences'],3748);self.assertEqual(d['remaining_exact_matches'],144)
 def test_03_candidates_sessions_tail_and_label_invariance(self):
  a,b=align_candidates(self.a,self.b,self.cal);sa=f1_structure(a,self.cal);sb=f1_structure(b,self.cal);self.assertEqual(len(a),3939);self.assertEqual(sa['labels'].Target.notna().sum(),3919);pd.testing.assert_series_equal(sa['labels'].Target,sb['labels'].Target);pd.testing.assert_series_equal(sa['labels'].label_end,sb['labels'].label_end);self.assertTrue(sa['labels'].Target.tail(20).isna().all())
 def test_04_feature_sensitivity_attribution(self):
  self.assertEqual(self.m['known_label_differences'],0);self.assertEqual(self.m['label_end_differences'],0)
  self.assertEqual([self.m['features'][c]['over_1e_minus6'] for c in ['Log_Ret','Disparity','Vol_Regime']],[4,28,49]);p=self.m['attribution']['other_dates_precision_only'];self.assertTrue(all(v['over_1e_minus6']==0 for v in p['features'].values()));self.assertEqual(self.m['manual_thresholds'][0]['test_manual_membership_changes'],4)
 def test_05_origin_membership_purging_unchanged(self):
  self.assertEqual(len(self.m['origins']),15)
  for r in self.m['origins']:self.assertEqual(r['common_date_membership_changes'],0);self.assertEqual(r['F1_date_membership_changes'],0);self.assertEqual(r['common_regime_samples_A'],r['common_regime_samples_B'])
 def test_06_F1_inputs_and_O1_no_test_prices_labels(self):
  data,lineage=prepare_o1_arrays(self.a,self.cal);self.assertEqual(set(data),{'train','validation'});self.assertEqual(data['train'][0].shape,(2387,20,2));self.assertEqual(data['validation'][0].shape,(228,20,2));self.assertEqual(data['train'][0].dtype,np.float32);self.assertEqual(data['train'][1].dtype,np.int64);self.assertEqual(lineage['feature_order'],['Log_Ret','Disparity']);self.assertEqual(lineage['test_samples_accessed'],0);self.assertEqual(lineage['maximum_source_date'],'2020-12-30');self.assertLess(lineage['fit_end'],'2020-01-02')
 def test_07_future_test_and_2026_perturbation_no_batch_change(self):
  c=self.a.copy();c.loc[c.Date>'2020-12-30','Close']*=100
  c=pd.concat([c,pd.DataFrame({'Date':[pd.Timestamp('2026-01-02')],'Close':[1e30]})],ignore_index=True)
  a,_=prepare_o1_arrays(self.a,self.cal);b,_=prepare_o1_arrays(c,self.cal)
  for k in a:np.testing.assert_array_equal(a[k][0],b[k][0]);np.testing.assert_array_equal(a[k][1],b[k][1])
 def test_08_train_only_scaler_future_invariance(self):
  s=f1_structure(self.a,self.cal);dates=s['common_selected']['O1']['train'];ws=window_dates(self.cal.sessions,dates);fit=pd.DatetimeIndex(sorted({x for v in ws.values() for x in v}));x=s['features'][FEATURE_ORDER];a,pa=train_only_scaler(x,fit,'2020-01-02');changed=x.copy();changed.loc[changed.index>='2020-01-02']*=1e6;b,pb=train_only_scaler(changed,fit,'2020-01-02');np.testing.assert_array_equal(a.mean_,b.mean_);np.testing.assert_array_equal(a.scale_,b.scale_);self.assertEqual(pa,pb)
 def test_09_manual_references_train_only(self):
  s=f1_structure(self.a,self.cal);dates=s['common_selected']['O1']['train'];v=s['features'].Vol_Regime;r=freeze_manual_reference(v,dates,validation_start='2020-01-02',partition='train');changed=v.copy();changed.loc[changed.index>='2020-01-02']*=5;self.assertEqual(r,freeze_manual_reference(changed,dates,validation_start='2020-01-02',partition='train'))
  with self.assertRaises(BlockedError):freeze_manual_reference(v,dates,validation_start='2020-01-02',partition='test')
 def test_10_hmm_causal_filter_future_invariance_no_fit(self):
  params={'startprob':[.5,.5],'transmat':[[.9,.1],[.1,.9]],'means':[[0.],[2.]],'covars':[[1.],[1.]]};x=np.arange(12,dtype=float)[:,None]/10;a=forward_filter(x,**params);x[6:]+=100;b=forward_filter(x,**params);np.testing.assert_array_equal(a[:6],b[:6]);self.assertEqual(regime_status(None)['status'],'BLOCKED');self.assertEqual(regime_status([0,0])['status'],'BLOCKED')
 def test_11_shared_evaluation_single_class_and_separate_tables(self):
  rows=pd.DataFrame([dict(origin='O1',seed=s,model='RNN',date='2021-01-04',probability=.6,y_true=1) for s in [2,12]])
  manual=pd.DataFrame([dict(origin='O1',date='2021-01-04',regime='Low_Vol')]);hmm=pd.DataFrame([dict(origin='O1',date='2021-01-04',regime='HMM_0')]);p={'manual_reference_partition':'train','hmm_fit_partition':'train','hmm_decode':'forward_filter','hmm_state_naming_partition':'train','hmm_status':'PASS','availability_verified':True,'test_median_fallback':False};out=evaluate_same_predictions(rows,manual,hmm,provenance=p);self.assertEqual(set(out),{'manual','hmm'});self.assertTrue(out['manual'].balanced_accuracy.isna().all());self.assertTrue(out['hmm'].macro_f1.isna().all());self.assertEqual(out['manual'].n.max(),1)
  p['hmm_decode']='viterbi'
  with self.assertRaises(BlockedError):evaluate_same_predictions(rows,manual,hmm,provenance=p)
 def test_12_execution_denied_current_flags(self):
  with self.assertRaises(BlockedError):require_smoke_authorization(self.c,self.g,None,config_sha256='a'*64,gates_sha256='b'*64)
 def fixture_authorization(self):
  c=copy.deepcopy(self.c);c['training_enabled']=True;c['selected_candidate']='A';g=copy.deepcopy(self.g)
  for k in REQUIRED_A:g['mandatory_A'][k]['status']='PASS'
  g['mandatory_A']['final_price_source']['selected_candidate']='A'
  # SYNTHETIC guard fixture only, never persisted as actual execution approval.
  approval={'approved':True,'approved_by':'user','scope':'STEP3_F1_O1_SEED2_CPU_SMOKE_ONLY','config_sha256':'a'*64,'gates_sha256':'b'*64,'approval_reference':'SYNTHETIC_TEST_FIXTURE_NOT_REAL_APPROVAL'}
  return c,g,approval
 def test_13_extensions_B_do_not_unnecessarily_block_F1(self):
  c,g,p=self.fixture_authorization();self.assertNotIn('hmmlearn',c['runtime_versions']);self.assertTrue(all(r['status']=='BLOCKED' for r in g['extensions_B'].values()));self.assertTrue(require_smoke_authorization(c,g,p,config_sha256='a'*64,gates_sha256='b'*64))
 def test_14_each_A_gate_and_bound_approval_required(self):
  c,g,p=self.fixture_authorization()
  for key in REQUIRED_A:
   changed=copy.deepcopy(g);changed['mandatory_A'][key]['status']='BLOCKED'
   with self.assertRaises(BlockedError):require_smoke_authorization(c,changed,p,config_sha256='a'*64,gates_sha256='b'*64)
  p['config_sha256']='c'*64
  with self.assertRaises(BlockedError):require_smoke_authorization(c,g,p,config_sha256='a'*64,gates_sha256='b'*64)
 def test_15_scope_and_prediction_contract_cannot_drift(self):
  c,g,p=self.fixture_authorization()
  for key,value in [('test_access',True),('origin','O2'),('seed',12),('train_batches',2),('selected_candidate','B')]:
   changed=copy.deepcopy(c);changed[key]=value
   with self.assertRaises(BlockedError):require_smoke_authorization(changed,g,p,config_sha256='a'*64,gates_sha256='b'*64)
  c['prediction_contract']['include_t']=False
  with self.assertRaises(BlockedError):require_smoke_authorization(c,g,p,config_sha256='a'*64,gates_sha256='b'*64)
 def test_16_runtime_source_static_compile_and_guard_before_model_import(self):
  source=(R/'runtime/step28_smoke_runtime.py').read_text();tree=ast.parse(source);compile(tree,'runtime','exec') # compile only, no module/model execution
  fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute_authorized_smoke');gate=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='require_smoke_authorization');torch_import=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Import) and any(a.name=='torch' for a in n.names));self.assertLess(gate,torch_import)
  self.assertTrue(all(not isinstance(n,(ast.Import,ast.ImportFrom)) or not any(x.name in ['torch','ncps','hmmlearn'] for x in n.names) for n in tree.body))
  self.assertIn('loss.backward()',source);self.assertIn('optimizer.step();scheduler.step()',source);self.assertIn('weights_only=True',source);self.assertIn('torch.equal(v1,v2)',source);self.assertNotIn('GaussianHMM(',source)
 def test_17_prior_hashes_and_frozen_implementation(self):
  p=json.loads((R/'provenance/step28_preservation.json').read_text());self.assertTrue(p['all_unchanged'])
  for a in p['artifacts']:self.assertEqual(hashlib.sha256((R/a['file']).read_bytes()).hexdigest(),a['before_sha256'])
  f=json.loads((R/'manifests/step28_protocol_freeze.json').read_text());self.assertEqual(hashlib.sha256((R/f['config_file']).read_bytes()).hexdigest(),f['config_sha256'])
  for a in f['implementation_artifacts']:self.assertEqual(hashlib.sha256((R/a['file']).read_bytes()).hexdigest(),a['sha256'])
 def test_18_official_failure_not_certified_and_private_numbers_local(self):
  p=json.loads((R/'provenance/step28_source_checks.json').read_text());self.assertEqual(p['official_prices_retrieved'],0);self.assertEqual(p['official_crosscheck_status'],'BLOCKED');self.assertTrue(all(r['http_status']==403 for r in p['official_price_attempts']));self.assertTrue((R/'data/derived/STEP28_PRICE_CONFLICT_PRIVATE_KO.md').exists());self.assertFalse(self.m['raw_prices_published']);self.assertIsNone(self.m['final_source_selected'])
