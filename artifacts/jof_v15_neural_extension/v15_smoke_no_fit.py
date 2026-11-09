"""Real feature dimensions, synthetic forward only. No fitting, gradients or AUC."""
import argparse,json,platform,hashlib,inspect,importlib.metadata
from pathlib import Path
import numpy as np
from v15_common import MARKETS,SEEDS
import v15_locked_runner as runner

def audit(repo):
 import torch,nbformat
 from torch import nn
 from ncps.torch import LTC,CfC
 torch.set_num_threads(2);root=Path(repo);manifest=json.loads((root/'artifacts/jof_phase1_benchmark_expansion/data_manifest.json').read_text());reports=[]
 for market,folder in MARKETS.items():
  dim=len(next(r['Feature_names'] for r in manifest['markets'] if r['Market']==market))
  notebook=nbformat.read(root/'artifacts'/folder/f'SCI_v1_4_WALKFORWARD_{market}.ipynb',4)
  ns={'nn':nn,'NUM_LAYERS':1,'DROPOUT':.2,'HIDDEN_SIZE':128,'LTC':LTC,'CfC':CfC};exec(compile(notebook.cells[13].source,'original-model-cell13','exec'),ns)
  with torch.inference_mode():
   for arch,representation,d in [('LSTM','RAW',dim),('LTC','RAW',dim),('CfC','RAW',dim),('CfC','LOG',2)]:
    for seed in SEEDS:
     x=torch.arange(4*20*d,dtype=torch.float32).reshape(4,20,d)/1000
     runner.configure_seed(seed);model=runner.build_model(arch,d).eval();output=model(x)
     runner.configure_seed(seed);replay=runner.build_model(arch,d).eval();assert torch.equal(output,replay(x))
     runner.configure_seed(seed);original=ns['build_model']('LNN' if arch=='LTC' else arch,d).eval()
     assert all(torch.equal(a,b) for a,b in zip(model.parameters(),original.parameters())) and sum(p.numel() for p in model.parameters())==sum(p.numel() for p in original.parameters())
     assert torch.equal(output,original(x));assert output.shape==(4,2) and torch.isfinite(output).all()
     probs=torch.softmax(output,1);assert torch.isfinite(probs).all();torch.testing.assert_close(probs.sum(1),torch.ones(4))
     reports.append({'Market':market,'Model':arch,'Representation':representation,'Seed':seed,'Input_dim':d,'deterministic_forward':True,'original_topology_parameters_and_outputs_identical':True,'parameters':sum(p.numel() for p in model.parameters())})
 return {'status':'SMOKE_PASS','forward_checks':len(reports),'no_training':True,'no_gradients':True,'no_AUC':True,'CPU_only':True,'versions':{name:importlib.metadata.version(name) for name in ['torch','ncps','numpy','pandas','scikit-learn']},'Python':platform.python_version(),'torch_source_sha256':hashlib.sha256(Path(inspect.getfile(torch)).read_bytes()).hexdigest(),'ncps_class_source_sha256':{c.__name__:hashlib.sha256(Path(inspect.getfile(c)).read_bytes()).hexdigest() for c in [LTC,CfC]},'models':reports}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=audit(a.repo);a.out.write_text(json.dumps(r,indent=2)+'\n');print('SMOKE_PASS60forwardchecks;no fit/no gradients/no AUC')
