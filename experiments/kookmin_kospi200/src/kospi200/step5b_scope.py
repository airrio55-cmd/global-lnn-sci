"""Fail-closed bounded Test-only approval; never inherits training/template approval."""
from .data import BlockedError
MODE='STEP5B_FROZEN500_AB_RETROSPECTIVE_TEST_CPU'
def require_scope(config,approval,*,config_sha,inputs_sha,jobs_sha,policy_sha,source_hashes,job,roster):
 expected={'execution_mode':MODE,'step5b_test_evaluation_enabled':True,'training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,'statistics_execution_enabled':False,'max_evaluations':500,'device':'cpu','dtype':'float32','amp':False,'feature_order':['Log_Ret','Disparity']}
 if any(config.get(k)!=v for k,v in expected.items()):raise BlockedError('Config scope mismatch')
 required={'approved':True,'scope':MODE,'config_sha256':config_sha,'inputs_manifest_sha256':inputs_sha,'job_roster_sha256':jobs_sha,'policy_sha256':policy_sha,'max_evaluations':500,'permits_training':False,'permits_GPU':False,'permits_HMM':False,'permits_statistics':False}
 if not approval.get('approval_reference') or not approval.get('request_sha256') or any(approval.get(k)!=v for k,v in required.items()):raise BlockedError('Independent STEP5B approval missing or altered')
 if config['source_hashes']!=source_hashes or approval['source_hashes']!=source_hashes:raise BlockedError('Evaluator source mismatch')
 if len(roster)!=500 or len({j['evaluation_identity'] for j in roster})!=500 or job not in roster:raise BlockedError('Unapproved/missing/duplicate evaluation roster')
 if job['checkpoint_file'] not in config['allowed_checkpoint_reads'] or config['output_root']!=approval['output_root']:raise BlockedError('Unapproved I/O lineage')
 return True
