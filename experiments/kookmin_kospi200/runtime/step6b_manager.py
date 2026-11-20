"""CPU-only bounded cohort scheduler, no retries or new seeds."""
from pathlib import Path
import fcntl,json,os,subprocess,sys,time
R=Path(__file__).resolve().parents[1]
def main():
 cp=R/'data/derived/step6b_config_private.json';ap=R/'data/derived/step6b_approval_private.json';c=json.loads(cp.read_text());run=R/c['output_root'];lock=(run/'manager.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);pending=[(o,p) for o in ['O1','O2','O3','O4','O5'] for p in ['A','B']];active=[];done=[]
 while active or pending:
  while pending and len(active)<2:
   o,p=pending.pop(0);f=(run/f'{o}_{p}_fit.log').open('a');proc=subprocess.Popen([sys.executable,str(R/'runtime/step6b_fit.py'),'--config',str(cp),'--approval',str(ap),'--origin',o,'--candidate',p],cwd=R,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT);active.append((o,p,proc,f));print('LAUNCH',o,p,proc.pid,flush=True)
  for t in active.copy():
   o,p,proc,f=t
   if proc.poll() is not None:
    done.append({'origin':o,'candidate':p,'returncode':proc.returncode});f.close();active.remove(t);print('COHORT_END',o,p,proc.returncode,flush=True)
    if proc.returncode!=0:(run/'manager_gate_failure.json').write_text(json.dumps({'origin':o,'candidate':p,'pending_not_launched':pending}));pending=[]
  counts={}
  for p in (run/'candidates').glob('*/result.json'):
   z=json.loads(p.read_text());counts[z['status']]=counts.get(z['status'],0)+1
  (run/'progress.json').write_text(json.dumps({'counts':counts,'active':[{'origin':o,'candidate':p,'pid':pr.pid} for o,p,pr,f in active],'pending_cohorts':pending,'completed_cohorts':done},indent=2))
  if active:time.sleep(2)
 (run/'fits_done.json').write_text(json.dumps({'cohorts':done,'counts':counts},indent=2));print('HMM_CANDIDATES_FINISHED',counts,flush=True)
if __name__=='__main__':main()
