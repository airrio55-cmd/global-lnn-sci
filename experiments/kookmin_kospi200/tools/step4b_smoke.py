"""New-worker runtime smoke on synthetic data only; never runs a market fit."""
from pathlib import Path
import ast, copy, hashlib, json, os, random, sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from runtime import step4b_worker as worker
from kospi200.step4b_scope import planned_jobs
from kospi200.data import BlockedError
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 cp=R/'configs/step4b_pilot_config.json';ap=R/'manifests/step4b_authorization.json';gp=R/'manifests/step4b_preflight_private.json'
 c,a,g=[json.loads(p.read_text()) for p in [cp,ap,gp]];job=g['jobs'][0]
 assert worker.validate_scope(c,a,g,job,sha(cp),sha(R/'runtime/step4b_worker.py'),sha(gp))
 for key,value in [('seeds',[22,32,42]),('max_new_fits',101),('training_enabled',True),('gpu_enabled',True)]:
  changed=copy.deepcopy(c);changed[key]=value
  try:worker.validate_scope(changed,a,g,job,sha(cp),sha(R/'runtime/step4b_worker.py'),sha(gp))
  except BlockedError:pass
  else:raise RuntimeError('Scope rejection failed: '+key)
 try:worker.execute_job(root=R,config_path=cp,approval_path=ap,preflight_path=gp,job_id='O1_seed42_A_RNN')
 except ValueError as e:assert 'Unapproved fit identity' in str(e)
 else:raise RuntimeError('Unapproved worker entrypoint accepted')
 run=R/c['run_directory'];out=run/'synthetic_smoke_private';out.mkdir(exist_ok=False);notebook=(R/c['source_notebook_file']).resolve()
 assert sha(notebook)==c['source_notebook_sha256']
 # The exact new barrier is installed in this disposable process. Intentional
 # rejected opens never read a byte from another Origin or a Test price source.
 access=worker.barrier(R,run,out,'O1',notebook)
 rejected=0
 for origin in ['O2','O3','O4','O5']:
  path=R/g['datasets'][origin]['A']['array_file']
  try:path.open('rb')
  except PermissionError:rejected+=1
  else:raise RuntimeError('Cross-Origin barrier failed')
 assert rejected==4
 import torch
 from torch import nn
 from ncps.torch import LTC,CfC
 from runtime.step29_synthetic_smoke import verified_definition_sources
 from kospi200.smoke_preparation import static_parameter_count
 assert str(torch.__version__)=='2.10.0+cpu' and torch.version.cuda is None and os.environ['PYTHONHASHSEED']=='2'
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 sources=verified_definition_sources(json.loads(notebook.read_text()),c);ns={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':.2}
 for name in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']:exec(compile(sources[name]['source'],'<original-smoke-definition>','exec'),ns)
 tree=ast.parse((R/'runtime/step4b_worker.py').read_text());execute=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='execute_job')
 nested={x.name:x for x in execute.body if isinstance(x,ast.FunctionDef)}
 result=[]
 for name in ['RNN','LSTM','GRU','LTC','CfC']:
  job=next(j for j in planned_jobs() if j['origin']=='O1' and j['candidate']=='A' and j['seed']==22 and j['model']==name)
  seed=job['effective_seed'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
  context={'torch':torch,'np':np,'random':random,'ns':ns,'job':job,'static_parameter_count':static_parameter_count}
  # Compile and execute the actual new worker helper AST, not a substitute model.
  for fname in ['equal','rng_state','restore_rng','bundle']:
   node=ast.Module(body=[nested[fname]],type_ignores=[]);exec(compile(ast.fix_missing_locations(node),'<new-step4b-worker-helper>','exec'),context)
  gen=torch.Generator().manual_seed(seed);x=torch.randn(64,20,2);y=torch.arange(64,dtype=torch.int64)%2
  model,opt,sch=context['bundle'](38);criterion=ns['FocalLoss'](gamma=2,alpha=.25)
  model.train();opt.zero_grad(set_to_none=True);logits=model(x);loss=criterion(logits,y);assert logits.shape==(64,2) and torch.isfinite(loss)
  loss.backward();assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters() if p.requires_grad)
  norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.);assert torch.isfinite(norm);opt.step();sch.step();model.eval()
  with torch.no_grad():expected=model(x)
  rng=context['rng_state'](gen);payload={'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':sch.state_dict(),'RNG':rng};path=out/(name+'.pt');torch.save(payload,path);saved=torch.load(path,map_location='cpu',weights_only=True)
  restored,ro,rs=context['bundle'](38);restored.load_state_dict(saved['model']);ro.load_state_dict(saved['optimizer']);rs.load_state_dict(saved['scheduler']);context['restore_rng'](saved['RNG'],gen);restored.eval()
  with torch.no_grad():observed=restored(x)
  assert torch.equal(expected,observed) and context['equal'](opt.state_dict(),ro.state_dict()) and context['equal'](sch.state_dict(),rs.state_dict()) and context['equal'](rng,context['rng_state'](gen))
  result.append({'model':name,'status':'PASS','input_shape':[64,20,2],'output_shape':[64,2],'parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'loss_finite':True,'gradient_finite':True,'checkpoint_restore_exact':True,'RNG_restore_exact':True,'synthetic_optimizer_updates':1,'market_optimizer_updates':0})
 summary={'stage':'STEP4B_NEW_RUNNER_SMOKE','status':'PASS','config_sha256':sha(cp),'worker_sha256':sha(R/'runtime/step4b_worker.py'),'smoke_source_sha256':sha(__file__),'models':result,'unapproved_entrypoint_rejected':True,'scope_mutations_rejected':4,'crossOrigin_opens_rejected':rejected,'financial_market_inputs_used':0,'synthetic_only':True,'GPU':0,'HMM_fit':0,'master_training_enabled':False,'runner_scope':'New worker entrypoint rejection, valid approval, actual bundle/RNG helper AST, original definitions, forward/backward/optimizer/scheduler/checkpoint on one synthetic batch per model. Full real fit loop not executed by smoke.'}
 worker.write(R/'manifests/step4b_runner_smoke.json',summary);print(json.dumps(summary))

if __name__=='__main__':main()
