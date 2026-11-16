"""Rebind config/source/preparation hashes; never grants execution permission."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
c=json.loads((R/'configs/step3c_master_experiment_config.json').read_text());c['independent_Test_price_cutoffs']={f'O{i}':f'{2019+i}-12-31' for i in range(1,6)}
c['bootstrap']['ensemble_primary_family_size']=6
c['bootstrap']['origin_secondary_pvalues']='NOT_PLANNED_DESCRIPTIVE_ONLY'
c['Test_history_exposure']='O1 Test2021 already observed as STEP3B O2 Validation; historical paper Test outcomes also exist; no pristine prospective holdout claim'
c['execution_status']='PREPARED_NOT_AUTHORIZED';c['specification_status']='FROZEN_CONDITIONAL_PRICE_AND_RESEARCH_DESIGN_PENDING';c['hypothesis_registration_limit']='Historical paper outcomes and Pilot Validation already observed; this freeze is before new independent Test evaluation, not evidence of previously unseen data'
c['fit_budget_definition']='500 AB one-F1-stream base fits; 40 exact-contract reuse;460 planned new; excludes full RAW5/LOG2, ensembles,HMM,Ablation'
c['learning_kernel_scope']='STEP3B substring from def equal through end unchanged; scope validation, metadata and dynamic Validation length adapted; whole orchestration file SHA differs and is recorded'
extra=['src/kospi200/master_ensemble.py','tools/step3c_freeze.py','src/kospi200/master_statistics.py','src/kospi200/master_tau.py','src/kospi200/tau.py','src/kospi200/statistics.py','src/kospi200/regimes.py','src/kospi200/specs.py']
files=[x['file'] for x in c['implementation_artifacts']]+extra;c['implementation_artifacts']=[{'file':p,'sha256':sha(R/p)} for p in dict.fromkeys(files)]
save(R/'configs/step3c_master_experiment_config.json',c)
p=R/'manifests/step3c_prepared_inputs.json';g=json.loads(p.read_text());g['config_sha256']=sha(R/'configs/step3c_master_experiment_config.json');save(p,g);save(R/c['run_directory']/'prepared_inputs_private.json',g)
p=R/'provenance/step3c_execution_approval_TEMPLATE.json';a=json.loads(p.read_text());a.update({'config_sha256':g['config_sha256'],'worker_sha256':sha(R/'runtime/step3c_worker.py'),'manager_sha256':sha(R/'runtime/step3c_manager.py'),'preflight_sha256':sha(R/'manifests/step3c_prepared_inputs.json'),'approval_reference':None});save(p,a)
print('Frozen config',g['config_sha256'],'new fits disabled')
