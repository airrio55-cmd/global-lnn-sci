"""Exact100 HMM-only financial scope; no inherited STEP6A template release."""
from .data import BlockedError
MODE='STEP6B_TRAIN_ONLY_HMM100_FORWARD_AND_EXISTING_TEST_DESCRIPTIVE'
def require_scope(c,a,*,config_sha,inputs_sha,roster_sha,source_hashes,job,roster):
 expected={'execution_mode':MODE,'step6b_hmm_execution_enabled':True,'training_enabled':False,'neural_forward_enabled':False,'statistics_execution_enabled':False,'gpu_enabled':False,'max_candidate_fits':100,'max_selected_HMMs':10,'observation':['Vol_Regime']}
 if any(c.get(k)!=v for k,v in expected.items()):raise BlockedError('HMM scope/config mismatch')
 required={'approved':True,'scope':MODE,'config_sha256':config_sha,'input_manifest_sha256':inputs_sha,'roster_sha256':roster_sha,'source_hashes':source_hashes,'max_candidate_fits':100,'max_selected_HMMs':10,'permits_neural_fit':False,'permits_neural_forward':False,'permits_statistics':False,'permits_GPU':False}
 if not a.get('approval_reference') or not a.get('request_sha256') or any(a.get(k)!=v for k,v in required.items()) or c['source_hashes']!=source_hashes:raise BlockedError('Independent STEP6B approval absent/changed')
 if len(roster)!=100 or len({j['job_id'] for j in roster})!=100 or job not in roster:raise BlockedError('Frozen100 roster identity missing/changed')
 if a['output_root']!=c['output_root']:raise BlockedError('Output lineage mismatch')
 return True
