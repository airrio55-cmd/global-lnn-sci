"""V15.1 dispatch adapter. Original fit_predict executes every cache miss unchanged.
This is explicitly a procedural extension,not the unmodified V15.0 CLI.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,datetime
sys.path.insert(0,'/repo/artifacts/jof_v15_neural_extension')
import v15_locked_runner as runner
import base_v15_0_ops as ops
from prepare import verify_code

def make_adapter(original,jobs,reused,out,ledger):
 byid={j['fit_id']:j for j in jobs}
 def dispatch(name,train,eval_rows,frame,cols,seed,epochs,device,*,cfg=None,artifact_dir=None,execution_authorized=False):
  import torch,numpy as np
  jid=Path(artifact_dir).name;j=byid[jid]
  if (name,seed,epochs,device)!=(j['Architecture'],j['Seed'],60,'cpu'):raise ValueError('Dispatch settings mismatch')
  if len(cols)!=j['Input_dim'] or len(train)!=j['TrainN'] or len(eval_rows)!=j['EvalN']:raise ValueError('Dispatch dataset mismatch')
  if jid in reused:
   meta=json.loads((Path(artifact_dir)/'fit_metadata.json').read_text())
   if meta['columns']!=list(cols) or meta['train_dates']!=[r['Date'] for r in train] or meta['evaluation_dates']!=[r['Date'] for r in eval_rows]:raise ValueError('Cached training/evaluation dates differ')
   for name_,digest in reused[jid]['files_sha256'].items():
    if ops.sha(Path(artifact_dir)/name_)!=digest:raise ValueError('Cached bytes changed:'+jid)
   ck=torch.load(Path(artifact_dir)/'checkpoint.pt',map_location='cpu',weights_only=True);prob=ck['probabilities'].numpy().copy()
   if ck['seed']!=seed or ck['architecture']!=name or ck['epochs']!=60 or ck['loss']!='CE' or not np.isfinite(prob).all():raise ValueError('Cached checkpoint mismatch')
   ledger({'fit_id':jid,'action':'REUSE_NO_TRAINING','source_run_id':reused[jid]['source_run_id'],'utc':ops.now()});return prob
  if Path(artifact_dir).exists():raise ValueError('Unplanned existing job;prepare a new recovery attempt instead of overwriting')
  ledger({'fit_id':jid,'action':'NEW_FIT_START','utc':ops.now()})
  p=original(name,train,eval_rows,frame,cols,seed,epochs,device,cfg=cfg,artifact_dir=artifact_dir,execution_authorized=execution_authorized)
  ledger({'fit_id':jid,'action':'NEW_FIT_COMPLETE','utc':ops.now()});return p
 return dispatch

def main():
 verify_code();root=Path('/repo');out=Path('/runs/results');auth=Path('/authorization/record.json');cfgpath=root/'artifacts/jof_v15_neural_extension/V15_CONFIG_LOCKED.json'
 cfg,anchor=runner.check_lock(root,cfgpath,auth,require_execution=True);plan=json.loads(Path('/runs/recovery_plan.json').read_text());ready=json.loads(Path('/runs/preparation_complete.json').read_text())
 if ready['recovery_plan_sha256']!=ops.sha('/runs/recovery_plan.json') or plan['code_manifest_sha256']!=ops.sha(Path(__file__).with_name('version_manifest.json')) or plan['base_payload_commit']!=anchor:raise ValueError('Recovery readiness/plan drift')
 jobs=json.loads((root/'artifacts/jof_v15_neural_extension/step4/job_manifest.json').read_text())['jobs'];reused=plan['reused_jobs']
 if {p.name for p in (out/'fits').iterdir() if p.is_dir()}!=set(reused):raise ValueError('New fit artifacts already exist;no in-place restart')
 for jid,entry in reused.items():
  for name,digest in entry['files_sha256'].items():
   if ops.sha(out/'fits'/jid/name)!=digest:raise ValueError('Prepared copied artifact changed')
 def ledger(entry):
  with Path('/runs/dispatch_ledger.jsonl').open('a') as stream:stream.write(json.dumps(entry)+'\n')
 original=runner.fit_predict;runner.fit_predict=make_adapter(original,jobs,reused,out,ledger)
 try:runner.run(root,cfg,out,cfgpath=cfgpath,lockpath=auth)
 finally:runner.fit_predict=original
 print('RECOVERY_WORKER_COMPLETE',len(reused),'reused;',1080-len(reused),'new fits',flush=True)
if __name__=='__main__':
 if '--execute' not in sys.argv:raise SystemExit('Explicit --execute required')
 main()
