"""Reserved single-fit worker. Never manually launch an unreserved identity."""
from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step3b_worker import execute_job
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['config-path','approval-path','preflight-path','job-id']:p.add_argument('--'+key,required=True)
 p.add_argument('--resume',action='store_true');a=p.parse_args();r=execute_job(root=ROOT,**vars(a));sys.exit(0 if r['status']=='COMPLETED' else 1)
