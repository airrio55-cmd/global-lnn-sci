"""Inventory/representation gate. Draft audit is permitted; locking never occurs here."""
import json
from pathlib import Path
from v15_common import sha,required_inventory,validate_config

def validate_representation(config_path,repo_root,require_locked=False):
 cfg=json.loads(Path(config_path).read_text());validate_config(cfg);rep=cfg['log_representation_provenance']
 for key in ['formula','time_alignment_rule','source_description']:
  if not rep.get(key):raise ValueError('Missing LOG provenance: '+key)
 inventory=rep.get('source_file_sha256',{});root=Path(repo_root).resolve()
 if not set(required_inventory(root)).issubset(inventory):raise ValueError('Incomplete data/code inventory')
 for rel,expected in inventory.items():
  p=(root/rel).resolve()
  if not p.is_relative_to(root) or not p.is_file() or sha(p)!=expected:raise ValueError('Invalid or changed frozen source: '+rel)
 if require_locked and (cfg.get('status')!='LOCKED' or cfg.get('permission_to_train') is not True):raise ValueError('Draft config: full fit forbidden')
 return True
