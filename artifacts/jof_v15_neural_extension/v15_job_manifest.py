"""Enumerate plans and source dates without creating labels or fitting a model."""
import json
from pathlib import Path
from v15_common import MARKETS,ORIGINS,SEEDS,sha
from v15_locked_runner import v14_module

def build(repo):
 root=Path(repo);v14=v14_module(root);jobs=[]
 for market in MARKETS:
  raw,frame,cols,_=v14.load_market(root,market)
  for vy,ty in ORIGINS:
   origin=f'O{vy-2012}'
   for start,end in [(vy,vy),(vy+1,vy+1),(ty,ty+1)]:
    train=v14.records(frame,raw,cols,'2010-01-01',f'{start-1}-12-31',preflight=True);ev=v14.records(frame,raw,cols,f'{start}-01-01',f'{end}-12-31',preflight=True)
    for seed in SEEDS:
     for arch,representation,tag in [('LSTM','RAW','LSTM'),('LTC','RAW','LTC_RAW'),('CfC','RAW','CfC_RAW'),('CfC','LOG','CfC_LOG')]:
      jobs.append({'fit_id':f'{market}_{origin}_{start}_{tag}_{seed}','Market':market,'Origin':origin,'Stage':start,'Period':'Validation' if start==end else 'Test','Eval_end_year':end,'Model':tag,'Architecture':arch,'Representation':representation,'Seed':seed,'Epochs':60,'Loss':'CE','TrainN':len(train),'EvalN':len(ev),'Input_dim':2 if representation=='LOG' else len(cols),'Train_end':f'{start-1}-12-31','Evaluation_dates_sha256':__import__('hashlib').sha256('\n'.join(r['Date'] for r in ev).encode()).hexdigest()})
 assert len(jobs)==1080 and len({j['fit_id'] for j in jobs})==1080
 assert sum(j['Period']=='Validation' for j in jobs)==720 and sum(j['Period']=='Test' for j in jobs)==360
 return {'status':'PLAN_ONLY_NOT_EXECUTED','fit_jobs':1080,'validation_fit_jobs':720,'test_fit_jobs':360,'independent_units_at_most':30,'seeds_are_not_independent_samples':True,'ensemble_fits':0,'jobs':jobs}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();a.out.write_text(json.dumps(build(a.repo),indent=2)+'\n');print('MANIFEST_PASS1080planned/0executed')
