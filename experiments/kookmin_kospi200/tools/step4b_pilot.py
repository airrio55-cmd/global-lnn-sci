"""Exactly100 authorized Seeds22/32 across five Origins CPU fits; production/master execution flags stay false."""
from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step4b_manager import execute_expansion
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for k in ['config-path','approval-path','preflight-path']:p.add_argument('--'+k,required=True)
 p.add_argument('--resume',action='store_true');a=p.parse_args();r=execute_expansion(root=ROOT,**vars(a));print('STEP4B FINISHED',r['new_completed'],'completed',r['new_failed'],'failed',r['new_blocked'],'blocked')
