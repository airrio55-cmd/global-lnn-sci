"""Run prior 90 data/static regressions and post-run controls in a separate process.

Does not call synthetic runner again; never rewrites historical test manifests.
"""
from pathlib import Path
import sys,json,unittest,importlib.util
ROOT=Path(__file__).resolve().parents[1]
class Capture(unittest.TextTestResult):
 def startTest(self,t):super().startTest(t);self.rows=getattr(self,'rows',[])
 def addSuccess(self,t):super().addSuccess(t);self.rows.append({'test':t.id(),'status':'PASS'})
 def addFailure(self,t,e):super().addFailure(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
 def addError(self,t,e):super().addError(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
def load(names):
 suite=unittest.TestSuite()
 for name in names:
  spec=importlib.util.spec_from_file_location(name,ROOT/'tests'/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
 return suite
if __name__=='__main__':
 old=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(load(['test_step2','test_step25','test_step26','test_step27','test_step28']))
 control=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(load(['test_step29']))
 smoke=json.loads((ROOT/'manifests/step29_smoke_results.json').read_text())
 def report(r):return {'passed':r.testsRun-len(r.failures)-len(r.errors),'failed':len(r.failures)+len(r.errors),'tests':r.rows}
 out={'checked_stage':'STEP2.9','historical_90_regression':report(old),'post_run_control_tests':report(control),
      'synthetic_execution_checks':{'counts':smoke['check_counts'],'model_checks':[{'model':r['model'],'status':r['status'],'checks':r['checks']} for r in smoke['models']]},
      'regression_scope':'Existing data-only/static/synthetic-array audit tests; separate process from synthetic NN smoke. No financial data fed to models.',
      'synthetic_runner_reexecuted_by_tests':False,'production_training_enabled':False,'hmm_fit_enabled':False,'real_data_training':'BLOCKED',
      'RAW_5feature_execution':'BLOCKED_NOT_AUTHORIZED','HMM_fit':'BLOCKED_NOT_AUTHORIZED','GPU_execution':'BLOCKED_NOT_AUTHORIZED'}
 (ROOT/'manifests/step29_test_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 sys.exit(0 if old.wasSuccessful() and control.wasSuccessful() and smoke['status']=='PASS' else 1)
