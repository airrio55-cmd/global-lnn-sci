"""Authorized, isolated synthetic-only CPU compatibility test.

No market-data path arguments, no production gate changes, no epochs or HMM fit.
Five architectures x two repetitions x one optimizer step = at most ten updates.
"""
from pathlib import Path
import ast,datetime,hashlib,importlib.metadata,json,os,platform,random,sys,traceback
from zoneinfo import ZoneInfo

MODELS=['RNN','LSTM','GRU','LTC','CfC']
DEFINITIONS={6:['FocalLoss'],8:['init_weights','RecurrentModel','LNNModel','CfCModel']}
PINNED={'torch':'2.10.0+cpu','ncps':'1.0.1','hmmlearn':'0.3.3'}
CHECK_NAMES=['constructor','parameter_count','forward','output_shape','focal_loss','backward',
             'gradient_finite','gradient_clipping','optimizer_step','scheduler_step',
             'checkpoint_save','checkpoint_restore','restored_logits_equal','same_seed_repeat_equal']

def file_sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def validate_synthetic_scope(config,approval,*,config_sha256,runner_sha256):
    required={'execution_mode':'STEP29_SYNTHETIC_CPU_ONLY','synthetic_execution_enabled':True,
              'training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,
              'market_data_access':False,'production_gate_override':False,'device':'cpu','dtype':'float32',
              'amp':False,'models':MODELS,'input_shape':[64,20,2],'target_shape':[64],
              'target_dtype':'int64','repetitions':2,'train_batches_per_repetition':1,
              'validation_batches_per_repetition':1,'optimizer_updates_per_repetition':1,
              'raw_log_experiment_executed':False}
    for key,value in required.items():
        if key not in config or config[key]!=value:raise ValueError('Invalid synthetic-only scope: '+key)
    if any(key in config for key in ['price_path','calendar_path','market_data_path','test_path']):
        raise ValueError('Financial-data paths are not accepted by synthetic mode')
    if (approval.get('scope')!='STEP29_SYNTHETIC_CPU_ONLY' or approval.get('approved') is not True
        or approval.get('approved_by')!='user' or not approval.get('approval_reference')
        or approval.get('config_sha256')!=config_sha256 or approval.get('runner_sha256')!=runner_sha256
        or approval.get('permits_production_training') is not False
        or approval.get('permits_HMM_fit') is not False or approval.get('permits_GPU') is not False):
        raise ValueError('Missing or mismatched independent synthetic-only authorization')
    return True


def verified_definition_sources(notebook,config):
    result={}
    for cell,names in DEFINITIONS.items():
        text=''.join(notebook['cells'][cell-1]['source']);tree=ast.parse(text)
        for name in names:
            found=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name]
            if len(found)!=1:raise ValueError('Definition absent/ambiguous: '+name)
            n=found[0];source=ast.get_source_segment(text,n);digest=hashlib.sha256(source.encode()).hexdigest()
            if digest!=config['original_definition_hashes'][name]:raise ValueError('Original source hash mismatch: '+name)
            result[name]={'source':source,'cell_1based':cell,'line_start_1based':n.lineno,'line_end_1based':n.end_lineno,'sha256':digest}
    return result


def install_financial_read_barrier(root,output,notebook):
    """CPython audit hook applies only to this standalone smoke process."""
    root,output,notebook=map(lambda p:Path(p).resolve(),[root,output,notebook])
    state={'financial_read_attempts':0,'financial_reads_allowed':0,'model_source_notebook_reads':0}
    def hook(event,args):
        if event!='open' or not args or isinstance(args[0],int):return
        try:path=Path(os.fsdecode(args[0])).resolve()
        except (TypeError,ValueError):return
        if path==notebook:
            state['model_source_notebook_reads']+=1;return
        forbidden=(path.is_relative_to(root/'data') and not path.is_relative_to(output)) or path.is_relative_to(root/'originals') or path.is_relative_to(Path('/workspace/attachments'))
        if forbidden:
            state['financial_read_attempts']+=1
            raise PermissionError('Synthetic process forbids financial input access: '+str(path))
    sys.addaudithook(hook)
    return state


def execute_synthetic(*,root,config_path,approval_path,notebook_path,output_dir):
    root=Path(root).resolve();config_path=Path(config_path);approval_path=Path(approval_path);notebook_path=Path(notebook_path).resolve()
    config=json.loads(config_path.read_text());approval=json.loads(approval_path.read_text())
    validate_synthetic_scope(config,approval,config_sha256=file_sha(config_path),runner_sha256=file_sha(__file__))
    if file_sha(notebook_path)!=config['source_notebook_sha256']:raise ValueError('Notebook identity mismatch')
    parent=json.loads((root/'configs/experiment_config.json').read_text())
    previous=json.loads((root/'configs/step28_smoke_config.json').read_text())
    if parent['training_enabled'] is not False or parent['hmm_fit_enabled'] is not False or previous['training_enabled'] is not False:
        raise ValueError('Production flags must remain disabled')
    if config['model_settings']!=parent['model']:raise ValueError('Frozen hyperparameters differ')
    if any(config['model_seed_offsets'][m]!=parent['seed_offsets'][m+'_RAW'] for m in MODELS):
        raise ValueError('Architecture seed offsets changed')
    if os.environ.get('PYTHONHASHSEED')!=str(config['base_seed']):raise ValueError('Set PYTHONHASHSEED before launch')
    out=Path(output_dir).resolve()
    if not out.is_relative_to(root/'data/derived') or out==root/'data/derived':raise ValueError('New ignored local output directory required')
    out.mkdir(parents=True,exist_ok=False)
    barrier=install_financial_read_barrier(root,out,notebook_path)
    versions={name:importlib.metadata.version(name) for name in config['environment_packages']}
    mismatch={k:{'expected':v,'actual':versions.get(k)} for k,v in config['expected_environment_versions'].items() if versions.get(k)!=v}
    environment={'checked_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'python':platform.python_version(),
                 'python_executable':sys.executable,'platform':platform.platform(),'machine':platform.machine(),
                 'versions':versions,'expected_version_differences':mismatch,'packages_updated':False,
                 'thread_environment':{k:os.environ.get(k) for k in ['PYTHONHASHSEED','OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']},
                 'production_training_enabled':False,'hmm_fit_enabled':False,'execution_mode':'STEP29_SYNTHETIC_CPU_ONLY'}
    write_json(out/'runtime_environment.json',environment)
    if mismatch:raise ValueError('Environment differs from approved pins; no automatic update')
    import numpy as np
    import torch
    from torch import nn
    from ncps.torch import LTC,CfC
    from ncps.torch.ltc_cell import LTCCell
    import inspect
    from kospi200.smoke_preparation import static_parameter_count
    if str(torch.__version__)!=PINNED['torch'] or torch.version.cuda is not None:raise ValueError('CPU-only pinned Torch required')
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    if torch.is_autocast_enabled('cpu') or torch.is_autocast_enabled():raise ValueError('AMP must be disabled')
    environment.update({'device':'cpu','dtype':'float32','AMP_enabled':False,'cuda_build':torch.version.cuda,
       'GPU_available_queried':False,'torch_num_threads':torch.get_num_threads(),'deterministic_algorithms':torch.are_deterministic_algorithms_enabled(),
       'LTC_wrapper_signature':str(inspect.signature(LTC)),'LTCCell_signature':str(inspect.signature(LTCCell)),
       'LTC_wrapper_source_sha256':file_sha(inspect.getsourcefile(LTC)),'LTC_cell_source_sha256':file_sha(inspect.getsourcefile(LTCCell)),
       'original_notebook_python_metadata':'3.12.0','historical_environment_equivalence':False})
    if environment['LTC_wrapper_source_sha256']!=config['ncps_reference_hashes']['LTC'] or environment['LTC_cell_source_sha256']!=config['ncps_reference_hashes']['LTCCell']:
        raise ValueError('ncps reference source mismatch')
    write_json(out/'runtime_environment.json',environment)
    sources=verified_definition_sources(json.loads(notebook_path.read_text()),config)
    # Exact verified class/function definitions only; no cell or notebook execution.
    namespace={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':config['model_settings']['dropout']}
    for name in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']:
        exec(compile(sources[name]['source'],'<hash-verified-original-definition>','exec'),namespace)
    source_lineage={name:{k:v for k,v in d.items() if k!='source'} for name,d in sources.items()}
    rng=np.random.default_rng(config['synthetic_data_seed']);arrays={}
    for partition in ['train','validation']:
        x=rng.standard_normal((64,20,2)).astype(np.float32);y=np.tile(np.array([0,1],dtype=np.int64),32);rng.shuffle(y)
        if not np.isfinite(x).all() or not np.isfinite(y).all() or set(np.unique(y))!={0,1}:raise ValueError('Invalid synthetic fixture')
        arrays[partition]=(x,y)
    np.savez(out/'synthetic_batches.npz',train_x=arrays['train'][0],train_y=arrays['train'][1],validation_x=arrays['validation'][0],validation_y=arrays['validation'][1])
    def array_sha(a):return hashlib.sha256(str(a.dtype).encode()+str(a.shape).encode()+a.tobytes()).hexdigest()
    fixture={p:{'input_shape':list(x.shape),'input_dtype':str(x.dtype),'target_shape':list(y.shape),'target_dtype':str(y.dtype),
                'finite':bool(np.isfinite(x).all() and np.isfinite(y).all()),'class_counts':{'0':int((y==0).sum()),'1':int((y==1).sum())},
                'input_sha256':array_sha(x),'target_sha256':array_sha(y)} for p,(x,y) in arrays.items()}
    def tensor_sha(t):return array_sha(t.detach().cpu().contiguous().numpy())
    def state_sha(state):
        h=hashlib.sha256()
        for name,value in sorted(state.items()):h.update(name.encode());h.update(tensor_sha(value).encode())
        return h.hexdigest()
    def equal(a,b):
        if isinstance(a,torch.Tensor):return isinstance(b,torch.Tensor) and torch.equal(a,b)
        if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
        if isinstance(a,(tuple,list)):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
        return a==b
    settings=config['model_settings']
    def construct(name):
        if name in ['RNN','LSTM','GRU']:return namespace['RecurrentModel'](2,128,name,1,dropout=.2)
        return namespace['LNNModel' if name=='LTC' else 'CfCModel'](2,128,dropout=.2)
    results=[];total_updates=0
    def one_repetition(name,rep,record):
        nonlocal total_updates
        seed=config['base_seed']+config['model_seed_offsets'][name]
        random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
        row={'repetition':rep,'effective_seed':seed,'optimizer_updates':0,'scheduler_steps':0,'checks':{},'status':'RUNNING'}
        record['repetitions'].append(row)
        checks=row['checks'];model=construct(name).to(device='cpu',dtype=torch.float32);checks['constructor']=True
        counts={'trainable':sum(p.numel() for p in model.parameters() if p.requires_grad),'total_registered':sum(p.numel() for p in model.parameters())}
        ref=static_parameter_count(name,2)
        row['parameters']=counts
        if counts!={'trainable':ref['trainable'],'total_registered':ref['total_registered']}:raise ValueError('Actual parameter count mismatch')
        checks['parameter_count']=True
        if any(p.device.type!='cpu' or (p.is_floating_point() and p.dtype!=torch.float32) for p in model.parameters()):raise ValueError('Parameter dtype/device mismatch')
        if name=='LTC':
            row['LTC_implicit_param_constraints']=bool(model.ltc.rnn_cell._implicit_param_constraints)
            row['LTC_positive_function']=type(model.ltc.rnn_cell.make_positive_fn).__name__
            row['LTC_solver_substeps']=model.ltc.rnn_cell._ode_unfolds
            if row['LTC_implicit_param_constraints'] is not True or row['LTC_positive_function']!='Softplus':raise ValueError('Unexpected LTC constraint mode')
        bx,by=[torch.from_numpy(a.copy()) for a in arrays['train']];vx,vy=[torch.from_numpy(a.copy()) for a in arrays['validation']]
        optimizer=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=1e-4)
        scheduler=torch.optim.lr_scheduler.OneCycleLR(optimizer,max_lr=.005,epochs=settings['max_epochs'],steps_per_epoch=1)
        criterion=namespace['FocalLoss'](gamma=2,alpha=.25)
        model.train();optimizer.zero_grad(set_to_none=True);logits=model(bx);checks['forward']=True
        row['input_shape']=list(bx.shape);row['output_shape']=list(logits.shape);row['input_dtype']=str(bx.dtype);row['device']=str(bx.device)
        if logits.shape!=(64,2) or logits.dtype!=torch.float32 or not torch.isfinite(logits).all():raise ValueError('Output shape/dtype/finite mismatch')
        checks['output_shape']=True;loss=criterion(logits,by)
        row['train_loss_finite']=bool(torch.isfinite(loss));row['train_loss_synthetic_only']=float(loss.detach())
        if not row['train_loss_finite']:raise ValueError('Nonfinite synthetic loss')
        checks['focal_loss']=True;loss.backward();checks['backward']=True
        trainable=[p for p in model.parameters() if p.requires_grad];grads=[p.grad for p in trainable if p.grad is not None]
        row['trainable_tensors']=len(trainable);row['gradient_tensors']=len(grads);row['gradient_finite']=bool(len(grads)==len(trainable) and all(torch.isfinite(x).all() for x in grads))
        if not row['gradient_finite']:raise ValueError('Nonfinite or missing gradient')
        checks['gradient_finite']=True
        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        after=torch.sqrt(sum((x.detach()*x.detach()).sum() for x in grads))
        row['gradient_norm_before_clip']=float(norm);row['gradient_norm_after_clip']=float(after)
        if not torch.isfinite(norm) or not torch.isfinite(after) or float(after)>1.+1e-6:raise ValueError('Gradient clipping failed')
        checks['gradient_clipping']=True
        optimizer.step();row['optimizer_updates']+=1;total_updates+=1;checks['optimizer_step']=True
        scheduler.step();row['scheduler_steps']+=1;checks['scheduler_step']=True
        row['scheduler_horizon']={'epochs_argument':100,'steps_per_epoch_argument':1,'total_steps':100,'performed_steps':1,'epoch_loop_executed':False}
        model.eval()
        with torch.no_grad():vlogits=model(vx);vloss=criterion(vlogits,vy)
        row['validation_loss_finite']=bool(torch.isfinite(vloss));row['validation_loss_synthetic_only']=float(vloss)
        if vlogits.shape!=(64,2) or not torch.isfinite(vlogits).all() or not row['validation_loss_finite']:raise ValueError('Invalid synthetic validation')
        checkpoint=out/f'{name}_repeat{rep}.pt'
        payload={'model':model.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),'torch_rng':torch.get_rng_state(),
                 'effective_seed':seed,'scope':'STEP29_SYNTHETIC_CPU_ONLY','config_sha256':file_sha(config_path),'source_notebook_sha256':config['source_notebook_sha256']}
        torch.save(payload,checkpoint);checks['checkpoint_save']=checkpoint.is_file()
        loaded=torch.load(checkpoint,map_location='cpu',weights_only=True)
        restored=construct(name).to(device='cpu',dtype=torch.float32);restored.load_state_dict(loaded['model'])
        opt2=torch.optim.AdamW(restored.parameters(),lr=.005,weight_decay=1e-4)
        sched2=torch.optim.lr_scheduler.OneCycleLR(opt2,max_lr=.005,epochs=100,steps_per_epoch=1)
        opt2.load_state_dict(loaded['optimizer']);sched2.load_state_dict(loaded['scheduler']);torch.set_rng_state(loaded['torch_rng'])
        checks['checkpoint_restore']=equal(model.state_dict(),restored.state_dict()) and equal(optimizer.state_dict(),opt2.state_dict()) and equal(scheduler.state_dict(),sched2.state_dict())
        if not checks['checkpoint_restore']:raise ValueError('Checkpoint state restore mismatch')
        restored.eval()
        with torch.no_grad():restored_logits=restored(vx) # SAME validation batch; no additional batch or update
        checks['restored_logits_equal']=torch.equal(vlogits,restored_logits)
        if not checks['restored_logits_equal']:raise ValueError('Restored logits differ')
        row.update({'train_logits_sha256':tensor_sha(logits),'validation_logits_sha256':tensor_sha(vlogits),
                    'trained_state_sha256':state_sha(model.state_dict()),'restored_state_sha256':state_sha(restored.state_dict()),
                    'checkpoint_file':str(checkpoint.relative_to(root)),'checkpoint_sha256':file_sha(checkpoint),'status':'PASS',
                    'new_train_batches':1,'new_validation_batches':1,'validation_replay_for_checkpoint':1,'test_batches':0})
        return row
    for name in MODELS:
        record={'model':name,'input_kind':'SYNTHETIC_2_FEATURES_NO_RAW_LOG_EXPERIMENT','repetitions':[],'checks':{},'status':'RUNNING'}
        try:
            for rep in [1,2]:one_repetition(name,rep,record)
            a,b=record['repetitions'];same=all(a[k]==b[k] for k in ['effective_seed','train_logits_sha256','validation_logits_sha256','trained_state_sha256','train_loss_synthetic_only','validation_loss_synthetic_only'])
            record['checks']={k:'PASS' if all(x['checks'].get(k) is True for x in record['repetitions']) else 'FAIL' for k in CHECK_NAMES[:-1]}
            record['checks']['same_seed_repeat_equal']='PASS' if same else 'FAIL'
            record['status']='PASS' if same else 'FAIL';record['error']=None if same else 'Same-seed deterministic repetition mismatch; no setting changed'
        except Exception as exc:
            trace=traceback.format_exc();(out/f'{name}_error.log').write_text(trace)
            record.update({'status':'FAIL','error_type':type(exc).__name__,'error':str(exc),'error_log':str((out/f'{name}_error.log').relative_to(root))})
            for key in CHECK_NAMES:
                vals=[row['checks'].get(key) for row in record['repetitions']]
                record['checks'][key]='PASS' if len(vals)==2 and all(v is True for v in vals) else 'BLOCKED'
            failed_stage=next((k for k in CHECK_NAMES if record['checks'][k]!='PASS'),None)
            if failed_stage:record['checks'][failed_stage]='FAIL'
        results.append(record);write_json(out/'partial_model_results.json',results)
    if total_updates>10:raise ValueError('Synthetic update budget exceeded')
    write_json(out/'runtime_environment.json',environment)
    report={'stage':'STEP2.9','checked_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
       'execution_mode':'STEP29_SYNTHETIC_CPU_ONLY','status':'PASS' if all(r['status']=='PASS' for r in results) else 'FAIL',
       'training_enabled':False,'hmm_fit_enabled':False,'synthetic_execution_authorized':True,
       'production_gate_override':False,'production_training_executed':False,'HMM_fit_executed':False,'GPU_executed':False,
       'actual_Test_accessed':False,'full_Notebook_executed':False,'epoch_loop_executed':False,
       'base_seed':2,'synthetic_data_seed':config['synthetic_data_seed'],'fixture':fixture,'models':results,
       'optimizer_updates_total':total_updates,'optimizer_updates_budget':10,'model_cases':5,'repetitions_per_model':2,
       'check_counts':{s:sum(v==s for row in results for v in row['checks'].values()) for s in ['PASS','FAIL','BLOCKED']},
       'source_notebook_sha256':config['source_notebook_sha256'],'original_source_lineage':source_lineage,
       'config_sha256':file_sha(config_path),'authorization_sha256':file_sha(approval_path),'runner_sha256':file_sha(__file__),
       'input_is_market_simulation':False,'financial_performance_metrics_generated':False,'RAW_5feature_runtime_status':'BLOCKED_NOT_AUTHORIZED',
       'RAW_5feature_static_parameter_counts':{model:static_parameter_count(model,5) for model in MODELS},
       'file_access_barrier':barrier,'local_output_directory':str(out.relative_to(root)),
       'checkpoint_and_npz_publication_allowed':False,'version_differences_changed_to_pass':False}
    write_json(out/'smoke_results.json',report)
    # Publish structured summaries only. Checkpoints and synthetic arrays stay ignored.
    write_json(root/'manifests/step29_smoke_results.json',report)
    write_json(root/'manifests/step29_runtime_environment.json',environment)
    return report
