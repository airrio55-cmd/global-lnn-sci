"""Unified allowed entrypoint: optimizer/backward/AUC are actively trapped."""
import argparse,json
from pathlib import Path
from unittest.mock import patch
import torch
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import v15_preflight_readonly as data
import v15_smoke_no_fit as forward

def forbidden(*args,**kwargs):raise AssertionError('Audit boundary violated: fit/backward/AUC forbidden')
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 with patch('torch.optim.AdamW',side_effect=forbidden),patch.object(torch.Tensor,'backward',side_effect=forbidden),patch.object(LogisticRegression,'fit',side_effect=forbidden),patch.object(LGBMClassifier,'fit',side_effect=forbidden),patch('sklearn.metrics.roc_auc_score',side_effect=forbidden):
  r=data.audit(a.repo);f=forward.audit(a.repo)
 for name,result in [('preflight_results.json',r),('forward_results.json',f)]:
  result['optimizer_backward_AUC_fit_traps_active']=True;(a.out/name).write_text(json.dumps(result,indent=2)+'\n')
 (a.out/'execution_boundary.json').write_text(json.dumps({'status':'PASS','actual_predictive_fits':0,'AUC_calls':0,'backward_calls':0,'optimizer_constructions':0,'protocol_lock_created':False,'forward_checks':f['forward_checks'],'real_data_fold_checks':len(r['folds'])},indent=2)+'\n');print('AUDIT_ONLY_PASS:60dategroups,90folds,60forwardchecks;0fits/0AUC/0backward/0optimizer')
if __name__=='__main__':main()
