"""Run retained 23+11 tests plus STEP2.6 tests without rewriting historical results."""
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
 for name in ['test_step2','test_step25','test_step26']:
  spec=importlib.util.spec_from_file_location(name,ROOT/'tests'/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
 result=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(suite)
 audit=json.loads((ROOT/'manifests/step26_cutoff_label_audit.json').read_text());blocked=[v for v in audit['gate_checks'] if v['status']=='BLOCKED']
 output={'scope':'Historical 23+11 implementation tests retained; 19 new price/label/feature/data-only tests; no model scoring',
  'passed':result.testsRun-len(result.errors)-len(result.failures),'failed':len(result.errors)+len(result.failures),'blocked_gates':len(blocked),
  'tests':result.rows,'BLOCKED':blocked,'training_enabled':False,'hmm_fit_enabled':False,'new_performance_metrics_generated':False}
 (ROOT/'manifests/step26_test_results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');sys.exit(0 if result.wasSuccessful() else 1)
