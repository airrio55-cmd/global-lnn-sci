"""Authorized statistics only. Shared paired blocks, transactional chunks, no models."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.metadata,json,os,platform,sys,time
from zoneinfo import ZoneInfo
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'src'),str(R)]
from kospi200.data import BlockedError
from kospi200.step5c_statistics import chunk_indices,metric_counts,observed_metrics,MODELS,METRICS

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def atomic(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
def environment(versions):return {'python':platform.python_version(),'versions':{k:importlib.metadata.version(k) for k in versions},'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip(),'memory_max':int(Path('/sys/fs/cgroup/memory.max').read_text()),'float':'float64','numpy_threads':1}
def validate(config_path,approval_path):
 c=read(config_path);a=read(approval_path);run=R/c['output_root']
 expected={'execution_mode':'STEP5C_FROZEN_RETROSPECTIVE_STATISTICS_ONLY','step5c_statistics_enabled':True,'training_enabled':False,'hmm_fit_enabled':False,'test_forward_enabled':False,'gpu_enabled':False,'block_lengths':[20,40,60],'replicates':10000,'seed':20261116,'family_sizes':[20,80,100],'chunk_size':250}
 if any(c.get(k)!=v for k,v in expected.items()):raise BlockedError('Frozen statistical scope mismatch')
 if a.get('approved') is not True or not a.get('approval_reference') or not a.get('request_sha256') or a.get('config_sha256')!=sha(config_path) or a.get('scope')!=expected['execution_mode'] or a.get('source_hashes')!=c['source_hashes'] or a.get('output_root')!=c['output_root']:raise BlockedError('Independent STEP5C authorization absent/mismatched')
 if a.get('replicates_per_block')!=10000 or a.get('block_lengths')!=[20,40,60] or a.get('seed')!=20261116 or a.get('hypothesis_budget_per_block')!=200 or a.get('planned_hypothesis_rows')!=600:raise BlockedError('Approval draw/family budget mismatch')
 if a.get('policy_contract_sha256')!=c['policy_contract_sha256'] or sha(run/'policy_contract.json')!=c['policy_contract_sha256']:raise BlockedError('Versioned null-policy contract mismatch')
 for k in ['permits_new_training','permits_new_inference','permits_HMM','permits_GPU','permits_Ensemble','permits_tau_forward']:
  if a.get(k) is not False:raise BlockedError('Forbidden execution permission')
 if any(sha(R/p)!=h for p,h in c['source_hashes'].items()):raise BlockedError('Statistical source changed')
 for name,key in [('packets_manifest_private.json','packets_manifest_sha256'),('families.json','families_sha256'),('preflight_private.json','preflight_sha256'),('environment.json','environment_sha256')]:
  if sha(run/name)!=c[key] or a.get(key)!=c[key]:raise BlockedError('Input/family/environment binding mismatch')
 env=read(run/'environment.json')
 if environment(env['versions'])!=env:raise BlockedError('Runtime CPU/memory/environment mismatch')
 master=R/'configs/step3c_master_experiment_config.json';m=read(master)
 if sha(master)!=c['master_sha256'] or any(m[k] is not False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']):raise BlockedError('Master/production flags changed')
 packets=read(run/'packets_manifest_private.json')
 for o,d in packets['groups'].items():
  for p,i in d.items():
   if sha(R/i['file'])!=i['sha256'] or i['file'] not in c['allowed_packet_reads']:raise BlockedError('Packet integrity/read-path mismatch')
 # SHA-only validation of original frozen predictions; never deserialize weights.
 for j in packets['lineage']:
  if sha(R/j['probability_file'])!=j['probability_sha256']:raise BlockedError('Original Test output changed')
 return c,a,run,packets

def main(config_path,approval_path,resume=False):
 c,a,run,packet_info=validate(config_path,approval_path);lock=(run/'statistics.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 # Subsequent numerical reads may access only authorized packet caches and this new output root.
 allowed={(R/p).resolve() for p in c['allowed_packet_reads']}
 def barrier(event,args):
  if event!='open' or not args or isinstance(args[0],int):return
  try:p=Path(os.fsdecode(args[0])).resolve()
  except (TypeError,ValueError):return
  if p.is_relative_to(run) or p in allowed:return
  if p.is_relative_to(R/'data') or p.is_relative_to(R/'originals') or p.is_relative_to('/workspace/attachments'):raise PermissionError('Statistics may read packet caches/write own output only')
 sys.addaudithook(barrier)
 packets={}
 for candidate in ['A','B']:
  packets[candidate]=[]
  for o in ['O1','O2','O3','O4','O5']:
   with np.load(R/packet_info['groups'][o][candidate]['file'],allow_pickle=False) as z:packets[candidate].append({k:z[k].copy() for k in ['y','probability','session_id']})
 observations=np.stack([[observed_metrics(z['y'],z['probability']) for z in packets[p]] for p in ['A','B']])
 np.save(run/'observed_metrics_private.npy',observations)
 sids=[z['session_id'] for z in packets['A']];block_status=[]
 for length in [20,40,60]:
  folder=run/'chunks'/f'block{length}';folder.mkdir(exist_ok=True);rng=np.random.default_rng(20261116);orig_rngs=[np.random.default_rng(20261116) for _ in sids];commits=[];next_draw=0
  existing=sorted(folder.glob('commit_*.json'))
  if existing and not resume:raise BlockedError('Committed chunks exist; explicit validated resume required')
  for file in existing:
   item=read(file)
   if item['start']!=next_draw or item['config_sha256']!=a['config_sha256'] or item['packets_manifest_sha256']!=c['packets_manifest_sha256'] or item['rng_global_before']!=rng.bit_generator.state or item['rng_origins_before']!=[r.bit_generator.state for r in orig_rngs] or sha(folder/item['array_file'])!=item['array_sha256']:raise BlockedError('Committed boundary/RNG/input mismatch')
   next_draw=item['end'];rng.bit_generator.state=item['rng_global_after']
   for r,state in zip(orig_rngs,item['rng_origins_after']):r.bit_generator.state=state
   commits.append(item)
  resumed_at=next_draw
  while next_draw<10000:
   start=next_draw;count=min(250,10000-start);before=json.loads(json.dumps(rng.bit_generator.state));before_o=json.loads(json.dumps([r.bit_generator.state for r in orig_rngs]));weights=chunk_indices(rng,sids,length,count);diagnostic_w=[chunk_indices(r,[sid],length,count)[0] for r,sid in zip(orig_rngs,sids)]
   global_metrics=np.empty((count,2,5,5,5),dtype=np.float64);origin_BA=np.empty((count,2,5,5),dtype=np.float64)
   for pi,candidate in enumerate(['A','B']):
    for oi,z in enumerate(packets[candidate]):
     global_metrics[:,pi,oi]=metric_counts(z['y'],z['probability'],weights[oi]);origin_BA[:,pi,oi]=metric_counts(z['y'],z['probability'],diagnostic_w[oi])[:,0,:]
   filename=f'draws_{start:05d}_{start+count:05d}_private.npz';dest=folder/filename
   if dest.exists():os.replace(dest,dest.with_name(dest.name+'.uncommitted_preserved'))
   tmp=dest.with_suffix('.tmp')
   with tmp.open('wb') as f:np.savez(f,global_metrics=global_metrics,origin_BA=origin_BA)
   os.replace(tmp,dest)
   item={'block_length':length,'start':start,'end':start+count,'array_file':filename,'array_sha256':sha(dest),'config_sha256':a['config_sha256'],'packets_manifest_sha256':c['packets_manifest_sha256'],'rng_global_before':before,'rng_global_after':rng.bit_generator.state,'rng_origins_before':before_o,'rng_origins_after':[r.bit_generator.state for r in orig_rngs]};atomic(folder/f'commit_{start:05d}.json',item);commits.append(item);next_draw+=count
   atomic(run/'progress.json',{'block_length':length,'committed_draws':next_draw,'target_draws':10000,'completed_blocks':block_status,'updated_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()})
   print('COMMITTED',length,next_draw,flush=True)
  block_status.append({'block_length':length,'draws_completed':next_draw,'chunks':len(commits),'resumed_at_draw':resumed_at,'status':'COMPLETED'})
 atomic(run/'bootstrap_done.json',{'blocks':block_status,'resume_requested':resume,'new_forwards':0,'new_training':0,'completed_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()});print('STEP5C_BOOTSTRAP_COMPLETE',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--approval',required=True);p.add_argument('--resume',action='store_true');args=p.parse_args();main(args.config,args.approval,args.resume)
