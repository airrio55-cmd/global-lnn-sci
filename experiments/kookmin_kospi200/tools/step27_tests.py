"""Retain prior tests/results; write only STEP2.7 results."""
from pathlib import Path
import unittest,importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1]
class Capture(unittest.TextTestResult):
 def startTest(self,t):super().startTest(t);self.rows=getattr(self,'rows',[])
 def addSuccess(self,t):super().addSuccess(t);self.rows.append({'test':t.id(),'status':'PASS'})
 def addFailure(self,t,e):super().addFailure(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
 def addError(self,t,e):super().addError(t,e);self.rows.append({'test':t.id(),'status':'FAIL','reason':self._exc_info_to_string(e,t)})
if __name__=='__main__':
 suite=unittest.TestSuite()
 for name in ['test_step2','test_step25','test_step26','test_step27']:
  spec=importlib.util.spec_from_file_location(name,ROOT/'tests'/f'{name}.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(mod))
 result=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(suite);a=json.loads((ROOT/'manifests/step27_data_validation.json').read_text());blocked=[{'gate':k,'status':v} for k,v in a['smoke_gates'].items() if v!='PASS']
 out={'scope':'Retained STEP2 23 + STEP2.5 11 + STEP2.6 19 + STEP2.7 19; data/static/synthetic only','passed':result.testsRun-len(result.errors)-len(result.failures),'failed':len(result.errors)+len(result.failures),'blocked_execution_gates':len(blocked),'BLOCKED':blocked,'tests':result.rows,'training_enabled':False,'hmm_fit_enabled':False,'gpu_executed':False,'new_model_performance_generated':False}
 (ROOT/'manifests/step27_test_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
