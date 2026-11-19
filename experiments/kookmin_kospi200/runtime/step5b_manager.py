"""At most two CPU inference cohorts, shared LTC lock, no identity retry."""
from pathlib import Path
import datetime,fcntl,json,os,subprocess,sys,time
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parents[1]
def main():
 cpath=R/'data/derived/step5b_test_config_private.json';apath=R/'data/derived/step5b_approval_private.json';c=json.loads(cpath.read_text());run=R/c['output_root'];lock=(run/'manager.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 pending=[(o,p) for o in ['O1','O2','O3','O4','O5'] for p in ['A','B']];active=[];finished=[]
 while pending or active:
  while pending and len(active)<2:
   o,p=pending.pop(0);f=(run/f'{o}_{p}_execution.log').open('a');env={**os.environ,'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONHASHSEED':'2'};proc=subprocess.Popen([sys.executable,str(R/'runtime/step5b_worker.py'),'--config',str(cpath),'--approval',str(apath),'--origin',o,'--candidate',p],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT);active.append((o,p,proc,f));print('LAUNCH',o,p,proc.pid,flush=True)
  for item in list(active):
   o,p,proc,f=item
   if proc.poll() is not None:
    finished.append({'origin':o,'candidate':p,'returncode':proc.returncode});f.close();active.remove(item);print('COHORT_END',o,p,proc.returncode,flush=True)
    if proc.returncode!=0:
     (run/'execution_stopped_gate.json').write_text(json.dumps({'reason':'Cohort failed; no further cohort launch','origin':o,'candidate':p,'unlaunched':pending}));pending=[]
  statuses={};forward=0
  for p in (run/'jobs').glob('*/result.json'):
   x=json.loads(p.read_text());statuses[x['status']]=statuses.get(x['status'],0)+1;forward+=x['forward_calls']
  (run/'manager_status.json').write_text(json.dumps({'statuses':statuses,'reserved_or_attempted':sum(statuses.values()),'forward_calls':forward,'active':[{'origin':o,'candidate':p,'pid':proc.pid} for o,p,proc,f in active],'pending_cohorts':pending,'finished_cohorts':finished,'updated_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()},indent=2))
  if active:time.sleep(2)
 (run/'manager_done.json').write_text(json.dumps({'finished_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'cohorts':finished},indent=2));print('STEP5B_EVALUATIONS_FINISHED',statuses,flush=True)
if __name__=='__main__':main()
