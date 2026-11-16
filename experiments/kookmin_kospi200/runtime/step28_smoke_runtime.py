"""Future STEP3 CPU smoke implementation. STEP2.8 NEVER calls execute_authorized_smoke.

Only NumPy/pandas/data code imports at module load. Torch/ncps, model construction,
forward/backward, optimizer steps and checkpoint I/O occur after explicit gates.
"""
from pathlib import Path
import hashlib,json,os,random
import numpy as np
import pandas as pd
from kospi200.data import BlockedError,Calendar,labels_on_calendar,local_features
from kospi200.folds import window_dates,train_only_scaler,transform_checked
from kospi200.smoke_preparation import extract_original_definitions,static_parameter_count

REQUIRED_A=['final_price_source','calendar_labels','domestic_input_time_contract','model_library_compatibility','protocol_frozen']
FEATURES=['Log_Ret','Disparity']


def require_smoke_authorization(config,gates,approval,*,config_sha256,gates_sha256):
    if config.get('training_enabled') is not True or config.get('hmm_fit_enabled') is not False:
        raise BlockedError('STEP2.8 execution disabled; a separately approved STEP3 config is required')
    if config.get('gpu_enabled') is not False or config.get('device')!='cpu':
        raise BlockedError('Only explicitly approved CPU smoke is supported')
    if any(gates.get('mandatory_A',{}).get(k,{}).get('status')!='PASS' for k in REQUIRED_A):
        raise BlockedError('All mandatory F1 gates A must PASS; extensions B are not F1 prerequisites')
    if (not approval or approval.get('approved') is not True or approval.get('approved_by')!='user'
        or approval.get('scope')!='STEP3_F1_O1_SEED2_CPU_SMOKE_ONLY'
        or approval.get('config_sha256')!=config_sha256 or approval.get('gates_sha256')!=gates_sha256
        or not approval.get('approval_reference')):
        raise BlockedError('Separate user execution approval bound to config and gate hashes required')
    if (config.get('origin')!='O1' or config.get('seed')!=2 or config.get('feature_spec')!='F1'
        or config.get('features')!={'RAW':FEATURES,'LOG':FEATURES}
        or config.get('models')!=['RNN','LSTM','GRU','LTC','CfC']
        or config.get('channels')!=['RAW','LOG'] or config.get('test_access') is not False
        or config.get('train_batches')!=1 or config.get('validation_batches')!=1
        or config.get('reproducibility_repetitions')!=2
        or config.get('selected_candidate') not in ['A','B']):
        raise BlockedError('Frozen smoke scope violated')
    if config.get('prediction_contract')!={'time':'18:00','timezone':'Asia/Seoul','include_t':True}:
        raise BlockedError('Prediction contract change needs a new approved protocol')
    if gates['mandatory_A']['final_price_source'].get('selected_candidate')!=config['selected_candidate']:
        raise BlockedError('Candidate selection conflicts with approved gate')
    return True


def prepare_o1_arrays(prices,calendar):
    """Data-only diagnostic/helper. Drop 2021+ BEFORE target/feature construction.

    No Test price/label is needed to construct this O1 implementation smoke.
    Primary mask remains STEP27's common local-feature-window mask, predeclared.
    """
    from kospi200.reconciliation import validate_prices
    frame,_=validate_prices(prices);s=calendar.checked();s=s[s.year<=2020]
    frame=frame[frame.Date.dt.year<=2020]
    if not pd.DatetimeIndex(frame.Date).equals(s):raise BlockedError('O1 history/calendar mismatch')
    c=frame.set_index('Date').Close;cal=Calendar(s,calendar.source,calendar.sha256,True)
    y=labels_on_calendar(c,cal);x=local_features(c)
    ready=x.notna().all(axis=1).rolling(20,min_periods=20).sum().eq(20)
    validation_start=s[s.year==2020][0];test_start=calendar.checked()[calendar.checked().year==2021][0]
    train=y.index[(y.index.year<=2019)&ready&y.Target.notna()&y.label_end.lt(validation_start)]
    valid=y.index[(y.index.year==2020)&ready&y.Target.notna()&y.label_end.lt(test_start)]
    if min(len(train),len(valid))<64:raise BlockedError('Insufficient O1 batch rows')
    windows=window_dates(s,train,window=20,include_t=True)
    fit_dates=pd.DatetimeIndex(sorted({d for v in windows.values() for d in v}))
    scaler,lineage=train_only_scaler(x[FEATURES],fit_dates,validation_start)
    # Initial rolling warm-up is excluded; no bfill/zero imputation.
    finite=x[FEATURES].notna().all(axis=1);scaled=transform_checked(scaler,x.loc[finite,FEATURES])
    arrays={}
    for key,dates in [('train',train),('validation',valid)]:
        ws=window_dates(s,dates,window=20,include_t=True)
        if any(len(v)!=20 or v.max()>t for t,v in ws.items()):raise BlockedError('Future/invalid window')
        xx=np.stack([scaled.loc[ws[t]].to_numpy(dtype=np.float32) for t in dates])
        yy=y.loc[dates,'Target'].to_numpy(dtype=np.int64)
        if not np.isfinite(xx).all():raise BlockedError('Invalid model input')
        arrays[key]=(xx,yy)
    lineage.update({'train_samples':len(train),'validation_samples':len(valid),'test_samples_accessed':0,
                    'maximum_source_date':str(frame.Date.max().date()),'feature_order':FEATURES,
                    'window':20,'include_t':True,'status':'DATA_ONLY_NOT_PIT_CERTIFICATION'})
    return arrays,lineage


def _original_namespace(notebook,config):
    # This function is reached only AFTER authorization in the sole executor.
    import torch
    from torch import nn
    from ncps.torch import LTC,CfC
    definitions=extract_original_definitions(notebook)
    names=['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']
    if any(definitions[k]['sha256']!=config['original_definition_hashes'][k] for k in names):
        raise BlockedError('Original architecture/loss source changed')
    namespace={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':config['model_settings']['dropout']}
    # Only exact hash-verified definitions, NEVER an entire notebook/cell runner.
    for name in names:exec(compile(definitions[name]['source'],'<verified-original-definition>','exec'),namespace)
    return namespace


def execute_authorized_smoke(*,config_path,gates_path,approval_path,price_path,calendar_path,notebook_path,output_dir):
    """Future, deliberately uncalled in STEP2.8. No Test scoring, no HMM."""
    def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    config=json.loads(Path(config_path).read_text());gates=json.loads(Path(gates_path).read_text())
    approval=json.loads(Path(approval_path).read_text()) if Path(approval_path).is_file() else None
    require_smoke_authorization(config,gates,approval,config_sha256=digest(config_path),gates_sha256=digest(gates_path))
    # All execution imports and all experimental I/O occur below the gate.
    import importlib.metadata as metadata
    import torch
    if torch.version.cuda is not None:raise BlockedError('CPU-only Torch build required; no GPU fallback')
    for name,version in config['runtime_versions'].items():
        if metadata.version(name)!=version:raise BlockedError('Runtime version mismatch: '+name)
    root=Path(__file__).resolve().parents[1]
    base=json.loads((root/'configs/experiment_config.json').read_text())
    if config['model_settings']!=base['model'] or config['seed_offsets']!=base['seed_offsets']:
        raise BlockedError('Frozen model settings/offsets changed')
    for path,key in [(price_path,'selected_price_sha256'),(calendar_path,'calendar_sha256'),(notebook_path,'source_notebook_sha256')]:
        if digest(path)!=config.get(key):raise BlockedError('Input hash mismatch: '+key)
    freeze=json.loads((root/'manifests/step28_protocol_freeze.json').read_text())
    for item in freeze['implementation_artifacts']:
        if digest(root/item['file'])!=item['sha256']:raise BlockedError('Frozen implementation changed')
    if os.environ.get('PYTHONHASHSEED')!='2':raise BlockedError('Set PYTHONHASHSEED=2 before launching the process')
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    prices=pd.read_csv(price_path,float_precision='round_trip')[['Date','Close']]
    sessions=pd.DatetimeIndex(pd.read_csv(calendar_path,parse_dates=['Date']).Date,name='Date')
    cal=Calendar(sessions,base['calendar']['source'],digest(calendar_path),True)
    arrays,lineage=prepare_o1_arrays(prices,cal)
    ns=_original_namespace(json.loads(Path(notebook_path).read_text()),config)
    dest=Path(output_dir).resolve()
    if not dest.is_relative_to((root/'data/derived').resolve()):raise BlockedError('Smoke artifacts must stay in ignored local derived directory')
    dest.mkdir(parents=True,exist_ok=False) # never overwrite an existing experiment
    settings=config['model_settings'];results=[]
    def construct(name):
        if name in ['RNN','LSTM','GRU']:return ns['RecurrentModel'](2,settings['hidden_size'],name,settings['layers'],dropout=settings['dropout'])
        return ns['LNNModel' if name=='LTC' else 'CfCModel'](2,settings['hidden_size'],dropout=settings['dropout'])
    def equal_nested(a,b):
        if isinstance(a,torch.Tensor):return torch.equal(a,b)
        if isinstance(a,dict):return a.keys()==b.keys() and all(equal_nested(a[k],b[k]) for k in a)
        if isinstance(a,(list,tuple)):return len(a)==len(b) and all(equal_nested(x,y) for x,y in zip(a,b))
        return a==b
    def one_pass(name,channel,save_checkpoint):
        seed=2+config['seed_offsets'][f'{name}_{channel}'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
        model=construct(name).to(device='cpu',dtype=torch.float32)
        expected=static_parameter_count(name,2)
        actual_trainable=sum(p.numel() for p in model.parameters() if p.requires_grad)
        actual_total=sum(p.numel() for p in model.parameters())
        if actual_trainable!=expected['trainable'] or actual_total!=expected['total_registered']:
            raise BlockedError('Runtime parameter count differs from the frozen reference')
        if name=='LTC' and getattr(model.ltc.rnn_cell,'_implicit_param_constraints',None) is not True:
            raise BlockedError('Unexpected LTC positive constraint mode')
        train_x,train_y=arrays['train'];valid_x,valid_y=arrays['validation']
        generator=torch.Generator().manual_seed(seed)
        loader=torch.utils.data.DataLoader(torch.utils.data.TensorDataset(torch.from_numpy(train_x),torch.from_numpy(train_y)),batch_size=64,shuffle=True,generator=generator,num_workers=0)
        bx,by=next(iter(loader));vx,vy=torch.from_numpy(valid_x[:64]),torch.from_numpy(valid_y[:64])
        if bx.shape!=(64,20,2) or bx.dtype!=torch.float32 or by.dtype!=torch.int64 or bx.device.type!='cpu':
            raise BlockedError('Input shape/dtype/device contract failed')
        optimizer=torch.optim.AdamW(model.parameters(),lr=settings['lr'],weight_decay=settings['weight_decay'])
        scheduler=torch.optim.lr_scheduler.OneCycleLR(optimizer,max_lr=settings['lr'],epochs=settings['max_epochs'],steps_per_epoch=len(loader))
        criterion=ns['FocalLoss'](gamma=settings['focal_gamma'],alpha=settings['focal_alpha'])
        model.train();optimizer.zero_grad(set_to_none=True);logits=model(bx)
        if logits.shape!=(64,2):raise BlockedError('Output shape mismatch')
        loss=criterion(logits,by)
        if not torch.isfinite(loss):raise BlockedError('Nonfinite training loss')
        loss.backward();norm=torch.nn.utils.clip_grad_norm_(model.parameters(),settings['gradient_clip'])
        if not torch.isfinite(norm):raise BlockedError('Nonfinite gradients')
        optimizer.step();scheduler.step()
        model.eval()
        with torch.no_grad():
            val_logits=model(vx);val_loss=criterion(val_logits,vy)
        if not torch.isfinite(val_logits).all() or not torch.isfinite(val_loss):raise BlockedError('Nonfinite validation')
        checkpoint_ok=False
        if save_checkpoint:
            path=dest/f'{name}_{channel}.pt';payload={'model':model.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
                  'rng':torch.get_rng_state(),'effective_seed':seed,'config_sha256':digest(config_path),'feature_order':FEATURES,'lineage':lineage}
            torch.save(payload,path);loaded=torch.load(path,map_location='cpu',weights_only=True)
            restored=construct(name).to(dtype=torch.float32,device='cpu');restored.load_state_dict(loaded['model'])
            opt2=torch.optim.AdamW(restored.parameters(),lr=settings['lr'],weight_decay=settings['weight_decay'])
            sched2=torch.optim.lr_scheduler.OneCycleLR(opt2,max_lr=settings['lr'],epochs=settings['max_epochs'],steps_per_epoch=len(loader))
            opt2.load_state_dict(loaded['optimizer']);sched2.load_state_dict(loaded['scheduler']);torch.set_rng_state(loaded['rng']);restored.eval()
            with torch.no_grad():restored_logits=restored(vx)
            checkpoint_ok=(torch.equal(val_logits,restored_logits) and equal_nested(optimizer.state_dict(),opt2.state_dict()) and equal_nested(scheduler.state_dict(),sched2.state_dict()))
            if not checkpoint_ok:raise BlockedError('Checkpoint save/restore mismatch')
        return {k:v.detach().clone() for k,v in model.state_dict().items()},val_logits.detach().clone(),checkpoint_ok
    for name in config['models']:
        for channel in config['channels']:
            first,v1,checkpoint_ok=one_pass(name,channel,True);second,v2,_=one_pass(name,channel,False)
            reproducible=equal_nested(first,second) and torch.equal(v1,v2)
            if not reproducible:raise BlockedError('Exact CPU smoke repeat mismatch; do not tune to repair Test results')
            results.append({'model':name,'channel':channel,'status':'PASS_IMPLEMENTATION_ONLY','shape':[64,20,2],'dtype':'float32','device':'cpu',
                            'parameters_verified_against_frozen_reference':True,'backward_optimizer_scheduler':True,'checkpoint_roundtrip':checkpoint_ok,'exact_reproducibility':True,'performance_metric_generated':False})
    report={'scope':'STEP3_F1_CPU_IMPLEMENTATION_SMOKE_ONLY','one_train_batch_and_one_validation_batch_per_repetition':True,
            'repetitions':2,'model_channels':results,'data_lineage':lineage,'test_accessed':False,'hmm_fit':False,'empirical_performance_claim':False}
    (dest/'smoke_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
