"""Independent user-authorized O3 pilot budget. No production flag override."""
from pathlib import Path
import json,hashlib
from .data import BlockedError
MODE='STEP4A2_O4_O5_AB_SEEDS2_12_F1_CPU'
def planned_jobs():return [{'run_id':f'{origin}_seed{s}_{p}_{m}','origin':origin,'seed':s,'candidate':p,'model':m,'effective_seed':s+o} for origin in ['O4','O5'] for s in [2,12] for p in ['A','B'] for m,o in [('RNN',101),('LSTM',201),('GRU',301),('LTC',401),('CfC',501)]]
def require_scope(c,a,g,job,config_sha,worker_sha,preflight_sha):
 expected={'execution_mode':MODE,'training_enabled':False,'hmm_fit_enabled':False,'new_fit_execution_enabled':False,'o4_o5_pilot_execution_enabled':True,'gpu_enabled':False,'production_gate_override':False,'origins':['O4','O5'],'seeds':[2,12],'price_candidates':['A','B'],'models':['RNN','LSTM','GRU','LTC','CfC'],'max_new_fits':40,'feature_order':['Log_Ret','Disparity']}
 for k,v in expected.items():
  if c.get(k)!=v:raise BlockedError('Unapproved scope/config: '+k)
 if g.get('jobs')!=planned_jobs() or job not in planned_jobs() or not g.get('all_preflight_PASS'):raise BlockedError('O4/O5-only40 identity/preflight mismatch')
 keys={'approved':True,'approved_by':'user','scope':MODE,'config_sha256':config_sha,'worker_sha256':worker_sha,'preflight_sha256':preflight_sha,'max_new_fits':40,'permits_Test':False,'permits_HMM_fit':False,'permits_GPU':False,'old60_refit_authorized':False,'acknowledges_BOTH_UNVERIFIED':True}
 if not a.get('approval_reference') or any(a.get(k)!=v for k,v in keys.items()):raise BlockedError('Independent O4/O5 authorization mismatch')
 root=Path(c['project_root']);master=root/'configs/step3c_master_experiment_config.json';base=json.loads(master.read_text())
 if hashlib.sha256(master.read_bytes()).hexdigest()!=c['master_config_sha256'] or any(base[k] is not False for k in ['training_enabled','hmm_fit_enabled','new_fit_execution_enabled']):raise BlockedError('Frozen master/production flags changed')
 if Path('/sys/fs/cgroup/cpu.max').read_text().strip()!=c['resources_current']['cpu_max'] or int(Path('/sys/fs/cgroup/memory.max').read_text())!=c['resources_current']['memory_max_bytes']:raise BlockedError('CPU/memory contract changed')
 return True
