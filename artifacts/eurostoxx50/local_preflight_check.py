"""Offline, real-training-data preflight; never evaluate test performance."""
import os
os.environ['OMP_NUM_THREADS']='2';os.environ['MKL_NUM_THREADS']='2'
import urllib.request
import nbformat
import yfinance

def forbidden(*args,**kwargs):
    raise RuntimeError('Network forbidden during offline preflight')
urllib.request.urlopen=forbidden
yfinance.download=forbidden
n=nbformat.read('artifacts/eurostoxx50/SCI_v1_4_WALKFORWARD_EUROSTOXX50.ipynb',4)
ns={}
for i in [1,3,5,7,9,11,13,14,16,25]:
    exec(compile(n.cells[i].source,f'cell-{i}','exec'),ns)
torch=ns['torch']; torch.set_num_threads(2)
X,y,*_=ns['audit_bundle']['folds'][0]['train']
for name in ['LNN','LSTM','Transformer']:
    for loss in ['CE','MILD_WCE','MILD_FOCAL']:
        model=ns['build_model'](name,11)
        criterion=ns['build_criterion'](loss,y)
        model.zero_grad()
        value=criterion(model(X[:64]),y[:64]);assert torch.isfinite(value)
        value.backward()
        assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
    print(name,'all 3 losses finite forward/backward PASS',flush=True)
print('OFFLINE PREFLIGHT PASS. No test metrics evaluated.',flush=True)
