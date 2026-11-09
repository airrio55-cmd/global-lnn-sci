"""Safety/integrity regression tests. AUC, optimizer and backward calls are traps."""
import unittest,json,ast,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np,pandas as pd
import v15_locked_runner as runner
import v15_analysis_draft as analysis
import v15_preflight_readonly as preflight
from v15_common import require_training,validate_config,reference_dates,SEEDS
ROOT=Path(__file__).resolve().parents[2]
class AuditTests(unittest.TestCase):
 def test_draft_blocks_training_and_analysis_before_calls(self):
  cfg=json.loads((ROOT/'artifacts/jof_v15_neural_extension/V15_CONFIG_DRAFT.json').read_text());validate_config(cfg)
  with self.assertRaises(RuntimeError):require_training(cfg)
  with patch.object(analysis,'roc_auc_score',side_effect=AssertionError('AUC forbidden')) as auc:
   with self.assertRaises(RuntimeError):analysis.analysis(ROOT,'not-read.csv','not-created')
   self.assertFalse(auc.called)
  with self.assertRaises((ValueError,RuntimeError)):runner.fit_predict('CfC',[],[],None,[],42,60,'cpu')
  with self.assertRaises(RuntimeError):runner.run(ROOT,cfg,Path('/tmp/not-created'))
 def test_config_rejects_changed_protocol(self):
  cfg=json.loads((ROOT/'artifacts/jof_v15_neural_extension/V15_CONFIG_DRAFT.json').read_text())
  for key,value in [('epochs',61),('loss','MILD_FOCAL'),('seeds',[42]),('device','cuda')]:
   bad={**cfg,key:value}
   with self.assertRaises(ValueError):validate_config(bad)
 def test_inventory_tampering_rejected(self):
  from v15_representation_gate import validate_representation
  cfg=ROOT/"artifacts/jof_v15_neural_extension/V15_CONFIG_DRAFT.json"
  self.assertTrue(validate_representation(cfg,ROOT))
  with self.assertRaises(ValueError):validate_representation(cfg,ROOT,require_locked=True)
  with patch.object(preflight,'sha',return_value='0'*64):
   with self.assertRaises(ValueError):preflight.audit(ROOT)
 def test_scaler_and_excluded_target(self):
  frame=pd.DataFrame({'A':np.arange(150,dtype=float),'B':np.arange(150,dtype=float)**2});tr=[{'index':i} for i in range(20,60)];ev=[{'index':100}]
  x,e,s,used=runner.window_tensors(tr,ev,frame,['A','B']);self.assertEqual(used.max(),58);self.assertEqual(used.min(),0)
  changed=frame.copy();changed.loc[100:]+=1e7;xx,ee,ss,_=runner.window_tensors(tr,ev,changed,['A','B']);np.testing.assert_array_equal(x,xx);np.testing.assert_array_equal(e,ee);np.testing.assert_array_equal(s.mean_,ss.mean_)
  bad=frame.copy();bad.loc[99,'A']=np.nan
  with self.assertRaises(RuntimeError):runner.window_tensors(tr,ev,bad,['A','B'])
  with self.assertRaises(ValueError):runner.window_tensors(tr,[{'index':70}],frame,['A','B'])
 def fixture(self):
  # Tiny synthetic date universe, not actual predictive outcomes; no AUC is computed.
  ref=pd.DataFrame([{'Market':m,'Origin':'O1','Period':period,'Date':f'2020-01-0{j}'} for m in analysis.MARKETS for period,j in [('Validation',1),('Test',2)]]);rows=[]
  for r in ref.to_dict('records'):
   for model in analysis.MODELS:
    for seed in SEEDS:rows.append({**r,'Model':model,'Seed':seed,'Probability':.4,'Y_true':1,'s200':0,'s60':1,'s20':0})
  return ref,pd.DataFrame(rows)
 def test_prediction_completeness_and_ensemble(self):
  ref,frame=self.fixture()
  with patch.object(analysis,'reference_dates',return_value=ref),patch.object(analysis,'roc_auc_score',side_effect=AssertionError('AUC forbidden')) as auc:
   self.assertTrue(analysis.validate_predictions(ROOT,frame))
   for bad in [frame.iloc[:-1],pd.concat([frame,frame.iloc[:1]],ignore_index=True),frame.assign(Probability=np.nan)]:
    with self.assertRaises((ValueError,AssertionError)):analysis.validate_predictions(ROOT,bad)
   bad=frame.copy();bad.loc[bad.Model=='CfC_ENSEMBLE','Probability']=.8
   with self.assertRaises(AssertionError):analysis.validate_predictions(ROOT,bad)
   bad=frame.copy();bad.loc[0,'Y_true']=0
   with self.assertRaises(ValueError):analysis.validate_predictions(ROOT,bad)
   self.assertFalse(auc.called)
 def test_static_hypothesis_scope(self):
  self.assertEqual(analysis.ARCH,('LSTM','LTC_RAW','CfC_RAW'));self.assertEqual(analysis.MODELS,('LSTM','LTC_RAW','CfC_RAW','CfC_LOG','CfC_ENSEMBLE'))
  source=Path(analysis.__file__).read_text();ast.parse(source)
  self.assertIn('if not result["H1_alignment_prerequisite"]["met"]',source)
  self.assertIn('v14.perm_p(df,pred,direction,20261109)',source);self.assertIn('v14.rotate_p(df,pred,direction)',source);self.assertIn('(3-i)*p',source)
if __name__=='__main__':unittest.main(verbosity=2)
