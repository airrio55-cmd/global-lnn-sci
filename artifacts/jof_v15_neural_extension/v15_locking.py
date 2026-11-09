"""Verify immutable payload anchor; protocol freeze is separate from run authorization."""
from pathlib import Path
import json,hashlib,subprocess
from v15_common import required_inventory,validate_config,sha
from v15_representation_gate import validate_representation
from v15_environment import verify as verify_environment
PREFIX='artifacts/jof_v15_neural_extension/'
def payload_paths(root):
 root=Path(root);folder=root/PREFIX
 metadata_only={'V15_LOCK_PAYLOAD.json','V15_LOCK_RECORD.md','V15_LOCK_RECORD.json','post_lock_verification.json','publication.json'}
 files=[str(p.relative_to(root)) for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name not in metadata_only]
 return sorted(set(required_inventory(root)+files))
def check(repo,config,record_path,*,require_execution=False,require_analysis=False):
 root=Path(repo).resolve();config=Path(config).resolve();record_path=Path(record_path).resolve()
 if record_path.is_relative_to(root):raise RuntimeError('Run lock/authorization record must be external to protected checkout')
 cfg=json.loads(config.read_text());validate_config(cfg)
 if cfg.get('status')!='LOCKED':raise RuntimeError('Protocol is not locked')
 validate_representation(config,root,require_locked=True)
 rec=json.loads(record_path.read_text());anchor=rec.get('locked_commit','')
 if len(anchor)!=40 or any(c not in '0123456789abcdef' for c in anchor):raise RuntimeError('Invalid immutable SHA')
 def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
 subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',anchor,'HEAD'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if git('status','--porcelain'):raise RuntimeError('Checkout is not clean')
 payload_bytes=subprocess.check_output(['git','-C',str(root),'show',f'{anchor}:{PREFIX}V15_LOCK_PAYLOAD.json'])
 if sha(root/PREFIX/'V15_LOCK_PAYLOAD.json')!=hashlib.sha256(payload_bytes).hexdigest():raise RuntimeError('Current payload manifest differs from immutable anchor')
 payload=json.loads(payload_bytes)
 if payload['sha256']!=rec.get('sha256') or set(payload_paths(root))!=set(payload['sha256']):raise RuntimeError('Frozen payload inventory changed')
 if str(config.relative_to(root)) not in payload['sha256']:raise RuntimeError('Config outside frozen payload')
 for rel,digest in payload['sha256'].items():
  path=(root/rel).resolve()
  if not path.is_relative_to(root) or not path.is_file() or sha(path)!=digest:raise RuntimeError('Current frozen file differs: '+rel)
  committed=subprocess.check_output(['git','-C',str(root),'show',f'{anchor}:{rel}'])
  if hashlib.sha256(committed).hexdigest()!=digest:raise RuntimeError('Anchor file differs: '+rel)
 verify_environment(root/PREFIX/'V15_ENVIRONMENT.lock.json')
 if require_execution and rec.get('execution_authorized') is not True:raise RuntimeError('Protocol locked, but this task does not authorize training')
 if require_analysis and rec.get('analysis_authorized') is not True:raise RuntimeError('Protocol locked, but this task does not authorize AUC/statistical analysis')
 return cfg,anchor

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--record',type=Path,required=True);a=p.parse_args()
 _,anchor=check(a.repo,a.config,a.record)
 print('LOCK_VERIFIED',anchor,'(verification only; no training/AUC/statistical analysis)')
