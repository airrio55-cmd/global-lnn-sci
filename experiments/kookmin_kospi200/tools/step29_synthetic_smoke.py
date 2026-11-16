"""Independent authorized synthetic-only entry point. No financial-data arguments."""
from pathlib import Path
import sys,argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from runtime.step29_synthetic_smoke import execute_synthetic
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['config-path','approval-path','notebook-path','output-dir']:p.add_argument('--'+name,required=True)
 a=p.parse_args()
 prior=ROOT/'manifests/step29_smoke_results.json'
 if prior.is_file() and json.loads(prior.read_text()).get('authorization_sha256')==hashlib.sha256(Path(a.approval_path).read_bytes()).hexdigest():
  p.error('This authorization has already been executed; no additional optimizer updates are authorized')
 result=execute_synthetic(root=ROOT,**vars(a));print(result['status'],result['check_counts'],'synthetic optimizer updates:',result['optimizer_updates_total']);sys.exit(0 if result['status']=='PASS' else 1)
