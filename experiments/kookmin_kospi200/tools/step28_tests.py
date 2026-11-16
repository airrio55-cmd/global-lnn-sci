"""Rerun all prior 72 plus STEP2.8 tests without changing historical test manifests."""
from pathlib import Path
import sys,unittest,importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
class Capture(unittest.TextTestResult):
 def startTest(self,t):super().startTest(t);self.rows=getattr(self,'rows',[])
 def addSuccess(self,t):super().addSuccess(t);self.rows.append({'test':t.id(),'status':'PASS'})
 def addFailure(self,t,e):super().addFailure(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
 def addError(self,t,e):super().addError(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
if __name__=='__main__':
 suite=unittest.TestSuite()
 for name in ['test_step2','test_step25','test_step26','test_step27','test_step28']:
  spec=importlib.util.spec_from_file_location(name,ROOT/'tests'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(m))
 result=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(suite);g=json.loads((ROOT/'manifests/step28_gate_results.json').read_text());mandatory=g['mandatory_A']
 out={'scope':'72 retained +18 STEP2.8; data/static/synthetic only; smoke executor NEVER called',
 'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors),'tests':result.rows,
 'mandatory_A_counts':{status:sum(r['status']==status for r in mandatory.values()) for status in ['PASS','FAIL','PARTIAL','BLOCKED']},
 'separate_execution_approval':'BLOCKED','extension_B_blocked':sum(r['status']=='BLOCKED' for r in g['extensions_B'].values()),
 'model_lifecycle_runtime_checks':'BLOCKED_NOT_EXECUTED','raw_input_PIT_validation':'BLOCKED','training_enabled':False,'hmm_fit_enabled':False,
 'model_forward_executed':False,'smoke_executor_called':False,'new_empirical_model_performance_generated':False}
 (ROOT/'manifests/step28_test_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
