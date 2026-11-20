"""Independent recovery scope; original blocked identities cannot be promoted."""
from .data import BlockedError
PROTOCOL_SHA='d7ff05bdfa45691d7f2535c240dd7f522c429b521974aa7ba1b31e82eb512bf2'
def require_scope(c,a,*,config_sha,roster_sha,source_hashes,identity):
 if c.get('scope')!='STEP8BR_RECOVERY40' or c.get('protocol_sha256')!=PROTOCOL_SHA or c.get('max_evaluations')!=40 or c.get('max_Logistic_fits')!=10 or c.get('NN_execution') is not False or c.get('HMM_execution') is not False:raise BlockedError('Invalid recovery-only scope')
 if a.get('approved') is not True or a.get('scope')!=c['scope'] or a.get('config_sha256')!=config_sha or a.get('roster_sha256')!=roster_sha or a.get('request_sha256')!=c.get('request_sha256') or a.get('source_hashes')!=source_hashes:raise BlockedError('Unbound/tampered recovery approval')
 ids=c.get('identities',[])
 if len(ids)!=40 or len(set(ids))!=40 or identity not in ids or not identity.endswith('_STEP8BR_V1'):raise BlockedError('Wrong/reused baseline identity')
 if c.get('prior_STEP8B_status')!='BLOCKED40_PRESERVED' or c.get('prior_evaluations')!=0:raise BlockedError('Original blocked ledger cannot be rewritten')
 return True
