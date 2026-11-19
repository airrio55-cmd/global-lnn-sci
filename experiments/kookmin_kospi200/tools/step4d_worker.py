"""One reserved STEP4D CPU fit and same-Validation checkpoint audit."""
from pathlib import Path
import sys,argparse,json,traceback
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step4d_worker import execute_job,write
from runtime.step4d_checkpoint_audit import audit_checkpoint
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for k in ['config-path','approval-path','preflight-path','job-id']:p.add_argument('--'+k,required=True)
 p.add_argument('--resume',action='store_true');a=p.parse_args();r=execute_job(root=ROOT,**vars(a))
 if r['status']=='COMPLETED':
  try:check,h=audit_checkpoint(ROOT,a.config_path,a.preflight_path,a.job_id,r);r.update({'postfit_checkpoint_audit':check,'postfit_checkpoint_audit_sha256':h})
  except Exception as e:r.update({'status':'FAILED_CHECKPOINT_VERIFICATION','checkpoint_error':str(e)});traceback.print_exc()
  c=json.loads(Path(a.config_path).read_text());write(ROOT/c['run_directory']/'jobs'/a.job_id/'result.json',r)
 sys.exit(0 if r['status']=='COMPLETED' else 1)
