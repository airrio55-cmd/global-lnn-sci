"""Synthetic/structural tests only. Never open financial Test or weights."""
from pathlib import Path
import ast,copy,hashlib,itertools,json,sys,unittest
from unittest.mock import patch
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from kospi200.data import BlockedError
from kospi200.step5a_evaluation import *
from kospi200.master_statistics import metric,correct_frozen_family
from kospi200.statistics import holm
from kospi200.master_protocol import comparison_family

def fixture():
 out=[]
 for origin,offset in [('O1',0),('O2',200)]:
  ds=pd.bdate_range('2018-01-01',periods=120);y=np.arange(120)%2
  for model in ['RNN','LTC']:
   for j,seed in enumerate(SEEDS):
    p=np.where(y==1,.7,.2).astype(float)
    if model=='LTC':p[np.arange(120)%(3+j%3)==0]=1-p[np.arange(120)%(3+j%3)==0]
    out.extend({'origin':origin,'date':date,'session_id':offset+i,'candidate':'A','model':model,'seed':seed,'y':int(y[i]),'probability':p[i]} for i,date in enumerate(ds))
 return pd.DataFrame(out)
class SyntheticPreparation(unittest.TestCase):
 def test_01_threshold_strict_and_confusion(self):
  m=synthetic_metrics([0,1,1,0],[.5,.5,.8,.2],domain='SYNTHETIC_FIXTURE');self.assertEqual(m['confusion_matrix'],[[2,0],[1,1]]);self.assertEqual(m['balanced_accuracy'],.75)
 def test_02_known_metrics(self):
  m=synthetic_metrics([0,1,1,0],[.1,.8,.9,.2],domain='SYNTHETIC_FIXTURE');self.assertEqual(m['balanced_accuracy'],1);self.assertEqual(m['macro_f1'],1);self.assertAlmostEqual(m['brier'],.025)
 def test_03_single_true_class_null(self):
  m=synthetic_metrics([0,0],[.1,.7],domain='SYNTHETIC_FIXTURE');self.assertIsNone(m['balanced_accuracy']);self.assertIsNone(m['macro_f1']);self.assertIsNone(m['recall_class1']);self.assertEqual(m['recall_class0'],.5);self.assertIsNotNone(m['brier'])
 def test_04_empty_null(self):
  m=synthetic_metrics([],[],domain='SYNTHETIC_FIXTURE');self.assertIsNone(m['accuracy']);self.assertIsNone(m['brier'])
 def test_05_missing_invalid_no_zero_fill(self):
  for p in [[np.nan,.5],[np.inf,.5],[-.1,.5],[1.1,.5]]:
   with self.assertRaises(BlockedError):synthetic_metrics([0,1],p,domain='SYNTHETIC_FIXTURE')
  with self.assertRaises(BlockedError):synthetic_metrics([0,np.nan],[.1,.8],domain='SYNTHETIC_FIXTURE')
 def test_06_domain_guard(self):
  with self.assertRaises(BlockedError):synthetic_metrics([0],[.1],domain='FINANCIAL')
 def test_07_seed_metrics_then_mean_no_probability_ensemble(self):
  y=np.array([0,1]);p=np.array([[.9,.1]*5,[.6,.1]*5]);z=synthetic_seed_scores(y,p,seeds=SEEDS,domain='SYNTHETIC_FIXTURE');self.assertEqual(z['market_dates'],2);self.assertEqual(z['mean']['balanced_accuracy'],.5);self.assertFalse(z['probability_ensemble_created'])
  with self.assertRaises(BlockedError):synthetic_seed_scores(y,p[:,:9],seeds=SEEDS[:-1],domain='SYNTHETIC_FIXTURE')
 def test_08_alignment_same_dates_allseeds(self):
  z=synthetic_aligned_packet(fixture(),'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE');self.assertEqual(len(z),2);self.assertEqual(z[0]['a'].shape,(120,10));self.assertEqual(z[0]['b'].shape,(120,10))
 def test_09_missing_seed_date_rejected(self):
  f=fixture().iloc[1:]
  with self.assertRaises(BlockedError):synthetic_aligned_packet(f,'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE')
 def test_10_A_B_mixing_rejected(self):
  f=fixture();f.loc[0,'candidate']='B'
  with self.assertRaises(BlockedError):synthetic_aligned_packet(f,'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE')
 def test_11_duplicate_and_future_rejected(self):
  f=fixture()
  for d in [pd.concat([f,f.iloc[:1]]),f.assign(date='2026-01-02')]:
   with self.assertRaises(BlockedError):synthetic_aligned_packet(d,'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE')
 def test_12_unique_monotone_session_required(self):
  f=fixture();f.loc[f.date==f.date.min(),'session_id']=5000
  with self.assertRaises(BlockedError):synthetic_aligned_packet(f,'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE')
 def test_13_same_bootstrap_indices_all_models_seeds(self):
  f=fixture();z=synthetic_aligned_packet(f,'RNN','LTC',candidate='A',domain='SYNTHETIC_FIXTURE');self.assertEqual(z[0]['a'].shape[1],10)
  # Spy on frozen metric arguments. Every replicate uses the same y and date-row indices for a/b, all10 columns retained.
  calls=[]
  def spy(y,p,name):calls.append((y.copy(),p.copy()));return .5
  with patch('kospi200.master_statistics.metric',side_effect=spy):bootstrap_effect(z[:1],metric_name='balanced_accuracy',block_length=20,replicates=10000,seed=20261116)
  self.assertEqual(len(calls),20002)
  for i in [0,2,100,20000]:self.assertTrue(np.array_equal(calls[i][0],calls[i+1][0]));self.assertEqual(calls[i][1].shape,(120,10))
 def test_14_bootstrap_lengths_and_rng_reproducible(self):
  f=fixture();results=[]
  for length in [20,40,60]:
   x=synthetic_bootstrap(f,'RNN','LTC',candidate='A',metric_name='balanced_accuracy',block_length=length,domain='SYNTHETIC_FIXTURE');self.assertEqual(x['market_dates'],240);self.assertEqual(x['seed_count'],10);self.assertEqual(x['valid_replicates']+x['invalid_replicates'],10000);results.append(x)
  y=synthetic_bootstrap(f,'RNN','LTC',candidate='A',metric_name='balanced_accuracy',block_length=20,domain='SYNTHETIC_FIXTURE');self.assertEqual(results[0],y)
 def test_15_discontinuous_sessions_no_cross_gap_block(self):
  f=fixture();f['session_id']=f.session_id*2
  with self.assertRaises(BlockedError):synthetic_bootstrap(f,'RNN','LTC',candidate='A',metric_name='balanced_accuracy',block_length=20,domain='SYNTHETIC_FIXTURE')
 def test_16_equal_origin_and_seed_metric_order(self):
  y=np.array([0,0,0,1]);p=np.array([[.2,.8],[.2,.2],[.2,.2],[.8,.2]])
  manual=np.mean([synthetic_metrics(y,p[:,i],domain='SYNTHETIC_FIXTURE')['balanced_accuracy'] for i in range(2)])
  self.assertEqual(metric(y,p,'balanced_accuracy'),manual)
  # Existing algorithm explicitly averages each Origin effect, independent of its date count.
  import inspect
  source=inspect.getsource(bootstrap_effect);self.assertIn('np.mean([effect(z,np.arange',source)
 def test_17_invalid_resample_threshold(self):
  f=fixture();first=f.date.min();f['y']=(f.date==first).astype(int)
  with self.assertRaises(BlockedError):synthetic_bootstrap(f,'RNN','LTC',candidate='A',metric_name='balanced_accuracy',block_length=20,domain='SYNTHETIC_FIXTURE')
 def test_18_holm_numeric_reproducible(self):
  self.assertTrue(np.allclose(holm([.01,.04,.03]),[.03,.06,.06]));self.assertTrue(np.array_equal(holm([.01,.04,.03]),holm([.01,.04,.03])))
 def test_19_holm_exact20_80_100_no_deletion(self):
  pairs=comparison_family()
  for size in [20,80,100]:
   rows=[dict(x,origin=o,metric=m,block_length=20,p_approx_centered=.01) for x in pairs for o in (['O1','O2','O3','O4','O5'] if size==100 else ['ALL']) for m in (['macro_f1','brier','recall0','recall1'] if size==80 else ['balanced_accuracy'])]
   self.assertEqual(len(correct_frozen_family(copy.deepcopy(rows),expected_size=size)),size)
   with self.assertRaises(BlockedError):correct_frozen_family(rows[:-1],expected_size=size)
 def test_20_checkpoint_metadata_identity_fixture(self):
  x={'origin':'O1','candidate':'A','seed':2,'model':'LTC','effective_seed':403,'feature_order':['Log_Ret','Disparity'],'best_checkpoint_sha256':'a'*64,'master_sha256':'b'*64,'data_sha256':'c'*64,'environment_sha256':'d'*64};self.assertTrue(validate_checkpoint_identity(x,x))
  for k,v in [('candidate','B'),('seed',12),('feature_order',['Disparity','Log_Ret']),('best_checkpoint_sha256','x')]:
   with self.assertRaises(BlockedError):validate_checkpoint_identity(x,{**x,k:v})
 def test_21_financial_entrypoint_zero_reads_even_flag_flip(self):
  with patch('builtins.open',side_effect=AssertionError('I/O forbidden')),patch.object(Path,'open',side_effect=AssertionError('I/O forbidden')):
   with self.assertRaises(BlockedError):financial_test_entrypoint(test_evaluation_enabled=True,approved=True,checkpoint='forbidden',Test_data='forbidden')
 def test_22_duplicate_evaluation_ledger(self):
  done=set();reserve_fixture_evaluation('O1_A_2_LTC',done,candidate='A',domain='SYNTHETIC_FIXTURE')
  with self.assertRaises(BlockedError):reserve_fixture_evaluation('O1_A_2_LTC',done,candidate='A',domain='SYNTHETIC_FIXTURE')
 def test_23_frozen_null_discrepancy_is_explicit(self):
  self.assertTrue(np.isnan(metric(np.array([0,0]),np.array([[.1]*10,[.2]*10]),'recall0')))
  gates=json.loads((R/'manifests/step5a_gate_results.json').read_text());self.assertEqual(next(x for x in gates['checks'] if x['id']=='statistics_null_policy_consistency')['status'],'BLOCKED')
 def test_24_calendar_only_test_structure(self):
  c=json.loads((R/'manifests/step5a_test_calendar_contract.json').read_text());self.assertEqual([x['planned_known_calendar_bases'] for x in c['origins']],[248,246,245,244,222]);self.assertEqual(c['origins'][-1]['unknown_calendar_bases'],20);self.assertFalse(c['actual_Test_eligibility_validated'])
 def test_25_execution_flags_and_zero_counts(self):
  c=json.loads((R/'configs/step5a_test_evaluation_config.json').read_text());a=json.loads((R/'provenance/step5a_test_approval_TEMPLATE.json').read_text());self.assertFalse(c['test_evaluation_enabled']);self.assertFalse(a['approved']);self.assertEqual(a['allowed_read_paths'],[])
 def test_26_no_torch_or_model_loading_in_new_evaluator(self):
  t=ast.parse((R/'src/kospi200/step5a_evaluation.py').read_text());names=[n.module for n in ast.walk(t) if isinstance(n,ast.ImportFrom)];self.assertFalse(any(n and 'torch' in n for n in names));self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ['load_state_dict','forward','fit'] for n in ast.walk(t)))
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SyntheticPreparation));bad={x._testMethodName:e for x,e in result.errors+result.failures};names=sorted(x for x in dir(SyntheticPreparation) if x.startswith('test_'));(R/'manifests/step5a_synthetic_test_results.json').write_text(json.dumps({'domain':'SYNTHETIC_OR_STRUCTURAL_ONLY','passed':result.testsRun-len(bad),'failed':len(bad),'financial_Test_inputs_loaded':0,'financial_statistical_tests':0,'tests':[{'id':n,'status':'FAIL' if n in bad else 'PASS',**({'error':bad[n]} if n in bad else {})} for n in names]},indent=2)+'\n');sys.exit(not result.wasSuccessful())
