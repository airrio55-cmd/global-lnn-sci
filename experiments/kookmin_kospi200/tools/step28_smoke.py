"""Future STEP3 entry point. Never executed in STEP2.8; checked-in flags deny it."""
from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step28_smoke_runtime import execute_authorized_smoke
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['config-path','gates-path','approval-path','price-path','calendar-path','notebook-path','output-dir']:p.add_argument('--'+name,required=True)
 a=p.parse_args();execute_authorized_smoke(**vars(a))
