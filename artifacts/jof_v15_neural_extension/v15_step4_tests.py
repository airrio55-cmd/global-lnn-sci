"""Final pre-lock tests; no gradients, optimizer, AUC, H1-H3 execution or model fit."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,json,tempfile,time,io,hashlib,resource,os,platform
from unittest.mock import patch
import numpy as np,pandas as pd,torch
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import v15_locked_runner as runner
import v15_preflight_readonly as preflight
import v15_smoke_no_fit as smoke
from v15_environment import verify
from v15_job_manifest import build
from v15_common import sha

def forbidden(*a,**kw):raise AssertionError('Forbidden training/backward/AUC/statistical execution')
def audit(root,out):
 root=Path(root).resolve();out=Path(out);folder=root/'artifacts/jof_v15_neural_extension';out.mkdir(parents=True,exist_ok=True)
 for file in folder.glob('*.py'):ast.parse(file.read_text(),filename=str(file))
 # Explicit imports cannot fit or evaluate AUC. Statistics are statically reviewed, not called.
 import v15_analysis_draft,v15_representation_gate,v15_locking,v15_audit_only
 assert v15_analysis_draft.ARCH==('LSTM','LTC_RAW','CfC_RAW')
 verify(folder/'V15_ENVIRONMENT.lock.json')
 reports=[];perf=[];torch.set_num_threads(2)
 with patch('torch.optim.AdamW',side_effect=forbidden),patch.object(torch.Tensor,'backward',side_effect=forbidden),patch.object(LogisticRegression,'fit',side_effect=forbidden),patch.object(LGBMClassifier,'fit',side_effect=forbidden),patch('sklearn.metrics.roc_auc_score',side_effect=forbidden),patch.object(v15_analysis_draft,'roc_auc_score',side_effect=forbidden):
  data=preflight.audit(root);forward=smoke.audit(root);jobs=build(root)
  assert jobs==json.loads((folder/'step4/job_manifest.json').read_text())
  manifest=json.loads((root/'artifacts/jof_phase1_benchmark_expansion/data_manifest.json').read_text())
  with torch.inference_mode(),tempfile.TemporaryDirectory(prefix='v15-forward-only-') as tmp:
   for market in ['SP500','NASDAQ100','NIKKEI225','EUROSTOXX50','KOSPI200']:
    dims=len(next(m['Feature_names'] for m in manifest['markets'] if m['Market']==market))
    for arch,rep,dim in [('LSTM','RAW',dims),('LTC','RAW',dims),('CfC','RAW',dims),('CfC','LOG',2)]:
     runner.configure_seed(42);model=runner.build_model(arch,dim).eval();x=np.linspace(-.5,.5,64*20*dim,dtype=np.float32).reshape(64,20,dim);tensor=torch.from_numpy(x)
     model(tensor);times=[]
     for _ in range(3):
      t=time.perf_counter();model(tensor);times.append(time.perf_counter()-t)
     p=torch.softmax(model(tensor),1)[:,1];ck={'state_dict':model.state_dict(),'architecture':arch,'input_size':dim,'seed':42,'epochs':0,'loss':'NOT_TRAINED_FORWARD_FIXTURE','probabilities':p};path=Path(tmp)/'synthetic.pt';torch.save(ck,path);replay=runner.replay_checkpoint(path,x);np.testing.assert_allclose(replay,p.numpy(),atol=1e-7,rtol=0)
     reports.append({'Market':market,'Architecture':arch,'Representation':rep,'random_initialization_only':True,'epochs_trained':0,'state_dict_bytes':path.stat().st_size,'max_replay_error':float(np.max(abs(replay-p.numpy()))),'safe_tensor_only_load':True})
     perf.append({'Market':market,'Architecture':arch,'Representation':rep,'Input_dim':dim,'Batch':64,'Window':20,'median_forward_seconds':float(np.median(times)),'parameters':sum(v.numel() for v in model.parameters())})
  # No original statistical routines are called in this test path.
 for name,contents in [('preflight_results.json',data),('forward_results.json',forward),('synthetic_checkpoint_replay.json',reports),('forward_only_timings.json',perf)]:
  (out/name).write_text(json.dumps(contents,indent=2)+'\n')
 weightbytes=0;equiv=0.;rows=0;trainingsteps=0
 for j in jobs['jobs']:
  timing=next(r for r in perf if r['Market']==j['Market'] and r['Architecture']==j['Architecture'] and r['Representation']==j['Representation'])
  ck=next(r for r in reports if r['Market']==j['Market'] and r['Architecture']==j['Architecture'] and r['Representation']==j['Representation'])
  steps=60*((j['TrainN']+63)//64);trainingsteps+=steps;equiv+=steps*timing['median_forward_seconds'];weightbytes+=ck['state_dict_bytes'];rows+=j['EvalN']
 # Evaluation-independent resource estimate; broad multiplier is not a training benchmark.
 resource_est={'method':'64sample forward-only median3 after1warmup; all1080 planned train sizes/60epochs/batch64; no backward or training benchmark','cpu_threads_per_job':2,'training_forward_equivalent_hours':equiv/3600,'estimated_training_hours_range':[equiv*3/3600,equiv*8/3600],'multiplier_assumption':'3to8x forward-only time for autograd,backward,optimizer,checkpoint and I/O; uncalibrated and hardware-dependent','optimizer_steps_planned':trainingsteps,'state_dict_total_bytes_estimated':weightbytes,'per_fit_eval_rows_total':rows,'checkpoint_and_metadata_disk_reserve_bytes':max(3*weightbytes+rows*500,3*1024**3),'recommended_RAM_per_serial_job_GiB':[8,16],'RAM_basis':{'LTC_dense_float32_intermediate_GiB':64*128*128*4*20*6/1024**3,'retained_intermediate_multiplier_assumption':[4,12],'note':'20steps x6 default ODE unfolds; backward retention not measured.8to16GiB is a conservative reservation, not observed training usage'},'observed_peak_audit_RSS_GiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024/1024**3,'machine':{'cpu_count_visible':os.cpu_count(),'cpu_quota':Path('/sys/fs/cgroup/cpu.max').read_text().strip() if Path('/sys/fs/cgroup/cpu.max').exists() else None,'platform':platform.platform()},'no_runtime_guarantee':True,'concurrency_not_benchmarked':True}
 (out/'resource_estimate.json').write_text(json.dumps(resource_est,indent=2)+'\n')
 result={'status':'PASS','syntax_import':True,'environment_version_code_binary_hashes':True,'V14_scoring_date_groups':60,'V14_refit_folds':90,'forward_determinism_checks':60,'synthetic_untrained_checkpoint_replay_checks':20,'all_1080_manifest_jobs_unique_and_match_runtime_plan':True,'checkpoint_save_restore_static_review':True,'H1_H1b_H2_H3_static_review_only':True,'model_training_calls':0,'AUC_calls':0,'H1_H3_execution_calls':0,'optimizer_backward_calls':0,'actual_experiment_checkpoints_created':0,'temporary_random_checkpoint_fixtures_removed':True}
 (out/'check_results.json').write_text(json.dumps(result,indent=2)+'\n');print('STEP4_TESTS_PASS: no fit/AUC/statistical analysis',flush=True)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();audit(a.repo,a.out)
