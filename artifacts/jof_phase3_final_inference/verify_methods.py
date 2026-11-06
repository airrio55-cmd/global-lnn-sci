"""Independent numerical checks before production inference."""
import json
from pathlib import Path
import numpy as np
from scipy import stats
from statsmodels.stats.sandwich_covariance import S_hac_simple
from arch.bootstrap import SPA
from statistical_methods import hac,dm,holm,spa
rng=np.random.default_rng(381);x=rng.normal(size=(1200,4));x[1:]+=.4*x[:-1]
np.testing.assert_allclose(hac(x,19),S_hac_simple(x-x.mean(0),nlags=19)/len(x),atol=1e-14)
a=rng.normal(size=1200);b=rng.normal(size=1200);r=dm(a,b);assert np.sign(r['DM_stat'])==np.sign((a-b).mean());rr=dm(b,a);assert r['raw_two_sided_p']==rr['raw_two_sided_p']
assert dm(np.ones(100),np.ones(100))['Status']=='degenerate_variance'
np.testing.assert_allclose(holm([.01,.04,.03,.002]),[.03,.06,.06,.008]);assert np.isnan(holm([.01,np.nan])[1]) and holm([.01,np.nan])[0]==.02
# Custom studentized SPA equals arch's raw-difference SPA after a fixed scale transform.
# Archive package-source limitation: arch8 studentize flag affects metadata but not _simulate_values scaling.
loss=rng.uniform(size=(350,5));r,means,mu=spa(loss,benchmark_index=0,reps=1000,block=20,seed=20261106);sigma=np.sqrt(r['LR_variance']);g=loss[:,[0]]-loss[:,1:];scaled=g/sigma
ref=SPA(np.zeros((350,1)),-scaled,block_size=20,reps=1000,bootstrap='stationary',studentize=False,seed=20261106);ref.compute()
# Same bootstrap, recentering sign and scaling; compare simulated statistics including zero truncation.
center=np.where(mu>=-sigma/np.sqrt(350)*np.sqrt(2*np.log(np.log(350))),mu,0.)
np.testing.assert_allclose(ref._simulated_vals[:,:,1].T,(means-center)/sigma,atol=1e-13)
Path(__file__).with_name('diagnostics').joinpath('method_verification.json').write_text(json.dumps({'status':'passed','HAC_matches_statsmodels':True,'DM_sign_symmetry_and_degenerate_status':True,'Holm_known_example_and_fixed_family_NaN':True,'studentized_SPA_matches_arch_on_fixed_scaled_differentials':True,'SPA_zero_truncation_and_plus_one_p':'intentional conventional finite-bootstrap differences from arch raw strict-inequality implementation'},indent=2)+'\n')
print('METHOD VERIFICATION PASSED')
