"""Explicit package import inspection only; no model creation or fit. Run in isolated venv."""
from pathlib import Path
import importlib.metadata as md,inspect,json,hashlib,sys,platform
import torch,ncps,hmmlearn
from ncps.torch import LTC,CfC
from ncps.torch.ltc_cell import LTCCell
from hmmlearn.hmm import GaussianHMM
root=Path(__file__).resolve().parents[1]
versions={n:md.version(n) for n in ['torch','ncps','hmmlearn','numpy','pandas','scikit-learn','scipy','future','sympy','networkx','filelock','fsspec','jinja2','MarkupSafe']}
expected={'torch':'2.10.0+cpu','ncps':'1.0.1','hmmlearn':'0.3.3'};assert all(versions[n]==v for n,v in expected.items())
files={}
for cls in [LTC,LTCCell,CfC,GaussianHMM]:
 p=Path(inspect.getsourcefile(cls));files[cls.__name__]={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'constructor_signature':str(inspect.signature(cls))}
assert files['LTC']['source_sha256']=='bbf3127013d3969994ecf0debf4eb37b56db750475ee71646a9decdf1aaf3026'
assert files['LTCCell']['source_sha256']=='167a9d6e1f4dc653ce21420010709e1c995716e53ad0d8bbc2d53c19c40b123f'
ref=inspect.signature(LTC).parameters['implicit_param_constraints'].default;assert ref is True
out={'checked_date':'2026-11-16','authorization':'User requested installation during STEP2.7; installation/import only','environment':'separate venv /workspace/venvs/kookmin-step27 with system-site-packages','python':platform.python_version(),'versions':versions,'status':'PASS_INSTALL_AND_IMPORT_ONLY','source_evidence':files,'wrapper_implicit_param_constraints':ref,'cuda_build':torch.version.cuda,'GPU_queried':False,'model_constructed':False,'model_forward':False,'neural_training':False,'hmm_fit':False,'checkpoint_loaded':False,'original_ncps_hmmlearn_version_verified':False,'pin_rationale':{'torch':'Stored notebook output 2.10.0+cpu','ncps':'Previously audited official reference wheel 1.0.1, not proven original version','hmmlearn':'0.3.3 verification candidate; original version unknown'},'source_urls':['https://download.pytorch.org/whl/cpu/torch/','https://pypi.org/pypi/ncps/1.0.1/json','https://pypi.org/pypi/hmmlearn/0.3.3/json'],'limitations':['Import success does not certify architecture behavior, deterministic training, checkpoint compatibility or original environment','venv reuses existing numerical dependencies; full environment reconstitution not certified']}
(root/'provenance/step27_isolated_environment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(root/'requirements-step27.txt').write_text('# Candidate verification environment; original ncps/hmmlearn versions UNKNOWN.\n# Install torch from https://download.pytorch.org/whl/cpu ; others from https://pypi.org/simple\n'+'\n'.join(n+'=='+v for n,v in versions.items())+'\n')
print(json.dumps({'status':out['status'],'packages':expected,'cuda_build':torch.version.cuda,'model_constructed':False}))
