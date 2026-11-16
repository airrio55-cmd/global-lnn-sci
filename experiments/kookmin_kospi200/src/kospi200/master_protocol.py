"""Frozen STEP3C job identities and fail-closed authorization; no model imports."""
import hashlib,json,itertools
from .data import BlockedError
MODELS=['RNN','LSTM','GRU','LTC','CfC']
SEEDS=[2,12,22,32,42,52,62,72,82,92]
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def job_grid(offsets):
 return [{'run_id':f'{origin}_seed{seed}_{candidate}_{model}','origin':origin,'seed':seed,'candidate':candidate,'model':model,'effective_seed':seed+offsets[model]} for origin in ['O1','O2','O3','O4','O5'] for seed in SEEDS for candidate in ['A','B'] for model in MODELS]
def comparison_family():
 return [{'candidate':p,'model_a':a,'model_b':b,'alternative':'two-sided','estimand':'equal-Origin mean of seed-wise metric differences'} for p in ['A','B'] for a,b in itertools.combinations(MODELS,2)]
def require_execution_authorization(c,a,g,job,config_sha,worker_sha,preflight_sha):
 # The frozen STEP3C config has this flag false. No override/force path exists.
 if c.get('new_fit_execution_enabled') is not True:raise BlockedError('STEP3C preparation only: new fits disabled; a separately approved release is required')
 from pathlib import Path
 observed_cpu=Path('/sys/fs/cgroup/cpu.max').read_text().strip();observed_memory=int(Path('/sys/fs/cgroup/memory.max').read_text())
 if observed_cpu!=c['resources_current']['cpu_max'] or observed_memory!=c['resources_current']['memory_max_bytes']:raise BlockedError('Resource contract changed; revalidate before execution')
 if not a.get('approval_reference'):raise BlockedError('Missing explicit user approval reference')
 if c.get('execution_mode')!='STEP3C_RETROSPECTIVE_F1_CPU' or c.get('training_enabled') is not False or c.get('hmm_fit_enabled') is not False or c.get('gpu_enabled') is not False or c.get('production_gate_override') is not False:raise BlockedError('Production/GPU/HMM scope mismatch')
 if c.get('seeds')!=SEEDS or c.get('models')!=MODELS or c.get('feature_order')!=['Log_Ret','Disparity']:raise BlockedError('Frozen roster/order mismatch')
 if not g.get('all_preflight_PASS') or len(g.get('jobs',[]))!=460 or len(g.get('reused_completed',[]))!=40:raise BlockedError('Preflight/budget/reuse mismatch')
 planned={j['run_id']:j for j in job_grid(c['model_seed_offsets'])};done={x['run_id'] for x in g['reused_completed']}
 if len(done)!=40 or {x['run_id'] for x in g['jobs']}!=set(planned)-done or any(x!=planned[x['run_id']] for x in g['jobs']):raise BlockedError('500/40/460 identity grid drift')
 if job not in g['jobs'] or job['run_id'] in {x['run_id'] for x in g['reused_completed']}:raise BlockedError('Completed/unapproved identity')
 if not all(a.get(k)==v for k,v in {'approved':True,'approved_by':'user','scope':c['execution_mode'],'config_sha256':config_sha,'worker_sha256':worker_sha,'preflight_sha256':preflight_sha,'max_new_fits':460,'permits_Test':False,'permits_HMM_fit':False,'permits_GPU':False,'old40_refit_authorized':False,'acknowledges_BOTH_UNVERIFIED':True,'retrospective_only':True}.items()):raise BlockedError('Separate execution approval absent or invalid')
 return True

def training_fingerprint(job,dataset,config):
 return digest({'identity':job,'array_sha256':dataset['array_sha256'],'dates_sha256':dataset['date_information_sha256'],'price_source_sha256':dataset['source_sha256'],'model_settings':config['model_settings'],'original_definition_hashes':config['original_definition_hashes'],'environment_sha256':config['environment_sha256'],'feature_order':config['feature_order'],'contract':config['prediction_contract'],'common_Vol_Regime_mask':True})
