"""Pilot-only entry point; production training flags stay disabled."""
from pathlib import Path
import argparse,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step3a_pilot import execute_pilot
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['config-path','approval-path','preflight-path','notebook-path']:p.add_argument('--'+name,required=True)
 p.add_argument('--resume',action='store_true');a=p.parse_args();result=execute_pilot(root=ROOT,**vars(a));print('PILOT FINISHED',result['completed_models'],'completed',result['failed_models'],'failed',flush=True)
