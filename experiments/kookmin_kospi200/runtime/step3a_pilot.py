"""Separately authorized retrospective O1 A/B F1 CPU Pilot; no Test/HMM/GPU.

Exactly ten registered fit identities. Full production flags stay false. Checkpoint
resume restores an existing fit at committed epoch boundaries, never refits a
completed identity or silently changes data/code/configuration.
"""
from pathlib import Path
import datetime,hashlib,importlib.metadata,json,os,platform,random,sys,time,traceback
from zoneinfo import ZoneInfo
MODELS=['RNN','LSTM','GRU','LTC','CfC']

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stamp():return datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
def write_json(path,value):
    p=Path(path);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)

def require_pilot_scope(c,a,g,*,config_sha,runner_sha,gates_sha):
    required={'execution_mode':'STEP3A_RETROSPECTIVE_O1_AB_F1_CPU_PILOT','pilot_execution_enabled':True,
        'training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,'production_gate_override':False,
        'origin':'O1','base_seed':2,'price_candidates':['A','B'],'models':MODELS,'feature_order':['Log_Ret','Disparity'],
        'device':'cpu','amp':False,'dtype':'float32','max_fit_attempts':10,'test_access':False,
        'pilot_price_cutoff':'2020-12-31','retrospective_only':True,'main_price_selection_allowed':False}
    for k,v in required.items():
        if c.get(k)!=v:raise ValueError('Pilot scope mismatch: '+k)
    if not g.get('all_execution_preflight_gates_PASS') or len(g['gates'])!=12 or any(row['status']!='PASS' for row in g['gates']):
        raise ValueError('Every operational preflight gate must PASS before training')
    if (a.get('approved') is not True or a.get('approved_by')!='user'
        or a.get('scope')!='STEP3A_RETROSPECTIVE_O1_AB_F1_CPU_PILOT'
        or a.get('config_sha256')!=config_sha or a.get('runner_sha256')!=runner_sha
        or a.get('preflight_sha256')!=gates_sha or not a.get('approval_reference')
        or a.get('permits_Test') is not False or a.get('permits_HMM_fit') is not False
        or a.get('permits_GPU') is not False or a.get('production_training_authorized') is not False):
        raise ValueError('Independent Pilot approval missing/mismatched')
    settings=c['model_settings']
    if settings['max_epochs']!=100 or settings['patience']!=10 or settings['selection_metric']!='balanced_accuracy':
        raise ValueError('Frozen early-stopping budget changed')
    return True

def install_pilot_barrier(root,run,notebook):
    root,run,notebook=[Path(p).resolve() for p in [root,run,notebook]]
    state={'forbidden_financial_access_attempts':0,'source_notebook_reads':0,'allowed_run_data_opens':0}
    def hook(event,args):
        if event!='open' or not args or isinstance(args[0],int):return
        try:p=Path(os.fsdecode(args[0])).resolve()
        except (ValueError,TypeError):return
        if p==notebook:state['source_notebook_reads']+=1;return
        if p.is_relative_to(run):state['allowed_run_data_opens']+=1;return
        if p.is_relative_to(root/'data') or p.is_relative_to(root/'originals') or p.is_relative_to('/workspace/attachments'):
            state['forbidden_financial_access_attempts']+=1
            raise PermissionError('Pilot only permits its isolated <=2020 staging: '+str(p))
    sys.addaudithook(hook);return state

def execute_pilot(*,root,config_path,approval_path,preflight_path,notebook_path,resume=False):
    root=Path(root).resolve();config_path=Path(config_path);approval_path=Path(approval_path);preflight_path=Path(preflight_path);notebook_path=Path(notebook_path).resolve()
    c=json.loads(config_path.read_text());a=json.loads(approval_path.read_text());g=json.loads(preflight_path.read_text())
    require_pilot_scope(c,a,g,config_sha=sha(config_path),runner_sha=sha(__file__),gates_sha=sha(preflight_path))
    base=json.loads((root/'configs/experiment_config.json').read_text())
    if base['training_enabled'] is not False or base['hmm_fit_enabled'] is not False or base['model']!=c['model_settings']:
        raise ValueError('Production flags or frozen model settings changed')
    for item in c['implementation_artifacts']:
        if sha(root/item['file'])!=item['sha256']:raise ValueError('Frozen implementation changed: '+item['file'])
    if sha(notebook_path)!=c['source_notebook_sha256']:raise ValueError('Original Notebook hash mismatch')
    if os.environ.get('PYTHONHASHSEED')!='2':raise ValueError('Set process PYTHONHASHSEED=2')
    versions={name:importlib.metadata.version(name) for name in c['environment_versions']}
    if versions!=c['environment_versions']:raise ValueError('Pinned environment changed; no automatic update')
    run=(root/c['run_directory']).resolve()
    if run!=Path(root/g['run_directory']).resolve() or not run.is_relative_to(root/'data/derived') or not run.is_dir():raise ValueError('Prepared Pilot directory mismatch')
    for candidate in ['A','B']:
        info=g['datasets'][candidate]
        for key,digest in [('price_file','price_sha256'),('array_file','array_sha256'),('date_file','date_sha256'),('metadata_file','metadata_sha256')]:
            path=(root/info[key]).resolve()
            if not path.is_relative_to(run) or sha(path)!=info[digest]:raise ValueError('Staged O1 artifact mismatch')
    barrier=install_pilot_barrier(root,run,notebook_path)
    import numpy as np
    import torch
    from torch import nn
    from ncps.torch import LTC,CfC
    from kospi200.pilot_data import validation_metrics
    from kospi200.smoke_preparation import static_parameter_count
    from runtime.step29_synthetic_smoke import verified_definition_sources
    if str(torch.__version__)!='2.10.0+cpu' or torch.version.cuda is not None:raise ValueError('CPU-only pinned Torch required')
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    if torch.is_autocast_enabled('cpu') or torch.is_autocast_enabled():raise ValueError('AMP forbidden')
    sources=verified_definition_sources(json.loads(notebook_path.read_text()),c)
    ns={'torch':torch,'nn':nn,'LTC':LTC,'CfC':CfC,'DROPOUT':c['model_settings']['dropout']}
    for name in ['init_weights','RecurrentModel','LNNModel','CfCModel','FocalLoss']:
        exec(compile(sources[name]['source'],'<verified-original-definition>','exec'),ns)
    source_lineage={n:{k:v for k,v in d.items() if k!='source'} for n,d in sources.items()}
    environment={'python':platform.python_version(),'versions':versions,'device':'cpu','dtype':'float32','amp':False,
                 'threads':1,'deterministic_algorithms':True,'GPU_queried':False,'packages_changed':False}
    expected_ids=[f'{p}_{model}' for p in ['A','B'] for model in MODELS];ledger_path=run/'fit_ledger.json'
    if ledger_path.exists():
        ledger=json.loads(ledger_path.read_text())
        if not resume:raise ValueError('Pilot already started; use explicit --resume for unfinished existing fits only')
        if ledger['config_sha256']!=sha(config_path) or ledger['runner_sha256']!=sha(__file__):raise ValueError('Cannot resume changed Pilot')
    else:
        if resume:raise ValueError('No existing Pilot to resume')
        ledger={'scope':c['execution_mode'],'config_sha256':sha(config_path),'runner_sha256':sha(__file__),
                'authorization_sha256':sha(approval_path),'started_at_kst':stamp(),'fit_budget':10,'fits':{},'completed':False}
        write_json(ledger_path,ledger)
    if any(k not in expected_ids for k in ledger['fits']) or len(ledger['fits'])>10:raise ValueError('Fit budget identity violation')
    def equal(x,y):
        if isinstance(x,torch.Tensor):return isinstance(y,torch.Tensor) and torch.equal(x,y)
        if isinstance(x,dict):return x.keys()==y.keys() and all(equal(x[k],y[k]) for k in x)
        if isinstance(x,(list,tuple)):return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
        return x==y
    def capture_rng(generator):
        n=np.random.get_state()
        return {'Python':random.getstate(),'NumPy':{'kind':n[0],'keys':n[1].tolist(),'pos':n[2],'has_gauss':n[3],'cached_gaussian':n[4]},
                'Torch_CPU':torch.get_rng_state(),'DataLoader':generator.get_state()}
    def restore_rng(state,generator):
        random.setstate(state['Python']);n=state['NumPy'];np.random.set_state((n['kind'],np.array(n['keys'],dtype=np.uint32),n['pos'],n['has_gauss'],n['cached_gaussian']))
        torch.set_rng_state(state['Torch_CPU']);generator.set_state(state['DataLoader'])
    def checkpoint(path,payload):
        tmp=path.with_suffix('.pt.tmp');torch.save(payload,tmp);os.replace(tmp,path)
    def construct(model_name):
        if model_name in ['RNN','LSTM','GRU']:return ns['RecurrentModel'](2,128,model_name,1,dropout=.2).to(dtype=torch.float32,device='cpu')
        return ns['LNNModel' if model_name=='LTC' else 'CfCModel'](2,128,dropout=.2).to(dtype=torch.float32,device='cpu')
    def make_bundle(model_name,steps):
        model=construct(model_name);ref=static_parameter_count(model_name,2)
        if sum(p.numel() for p in model.parameters() if p.requires_grad)!=ref['trainable']:raise ValueError('Parameter count mismatch')
        if model_name=='LTC' and model.ltc.rnn_cell._implicit_param_constraints is not True:raise ValueError('LTC constraint changed')
        opt=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=1e-4)
        sch=torch.optim.lr_scheduler.OneCycleLR(opt,max_lr=.005,epochs=100,steps_per_epoch=steps)
        return model,opt,sch
    def load_bundle(path,model_name,steps,generator):
        payload=torch.load(path,map_location='cpu',weights_only=True)
        if payload['config_sha256']!=sha(config_path) or payload['runner_sha256']!=sha(__file__):raise ValueError('Checkpoint identity mismatch')
        model,opt,sch=make_bundle(model_name,steps);model.load_state_dict(payload['model']);opt.load_state_dict(payload['optimizer']);sch.load_state_dict(payload['scheduler']);restore_rng(payload['RNG'],generator)
        return model,opt,sch,payload
    def export_progress():
        import pandas as pd
        runs=[];metrics=[];hist=[]
        for identifier in expected_ids:
            item=ledger['fits'].get(identifier)
            if not item:continue
            runs.append({k:item.get(k) for k in ['run_id','candidate','model','base_seed','effective_seed','status','epochs_completed','best_validation_epoch','train_samples','validation_samples','started_at_kst','finished_at_kst','error','prediction_status','checkpoint_restore','epoch1_resume_roundtrip','RNG_restore_exact','input_data_sha256','code_sha256','best_checkpoint_sha256','history_sha256','elapsed_training_seconds']})
            if item.get('metrics'):
                metrics.append({'run_id':identifier,'candidate':item['candidate'],'model':item['model'],'seed':2,'effective_seed':item['effective_seed'],
                                'epochs':item['epochs_completed'],'best_epoch':item['best_validation_epoch'],'train_samples':2387,'validation_samples':228,**item['metrics']})
            history_path=run/identifier/'history.json'
            if history_path.exists():
                for row in json.loads(history_path.read_text()):hist.append({'run_id':identifier,'candidate':item['candidate'],'model':item['model'],**row})
        pd.DataFrame(runs).to_csv(root/'manifests/step3a_pilot_runs.csv',index=False)
        pd.DataFrame(metrics).to_csv(root/'manifests/step3a_pilot_metrics.csv',index=False)
        pd.DataFrame(hist).to_csv(root/'manifests/step3a_epoch_history.csv',index=False)
        write_json(ledger_path,ledger)
    dataset_cache={}
    for candidate in ['A','B']:
        info=g['datasets'][candidate]
        with np.load(root/info['array_file'],allow_pickle=False) as f:
            arrays={k:f[k].copy() for k in ['train_x','train_y','validation_x','validation_y']}
        meta=json.loads((root/info['metadata_file']).read_text());dates=json.loads((root/info['date_file']).read_text())
        if arrays['train_x'].shape!=(2387,20,2) or arrays['validation_x'].shape!=(228,20,2):raise ValueError('Frozen O1 tensor shape mismatch')
        if any(not np.isfinite(x).all() for x in arrays.values()) or any(x.dtype!=np.float32 for k,x in arrays.items() if k.endswith('_x')):raise ValueError('Invalid input dtype/finite')
        if any(d>'2020-12-31' for row in dates.values() for key in ['dates','label_end'] for d in row[key]):raise ValueError('Test date/endpoints forbidden')
        dataset_cache[candidate]=(arrays,meta,dates)
    for candidate in ['A','B']:
        arrays,meta,dates=dataset_cache[candidate];tx,ty=torch.from_numpy(arrays['train_x']),torch.from_numpy(arrays['train_y']);vx,vy=torch.from_numpy(arrays['validation_x']),torch.from_numpy(arrays['validation_y'])
        for model_name in MODELS:
            identifier=f'{candidate}_{model_name}';existing=ledger['fits'].get(identifier)
            if existing and existing['status'] in ['COMPLETED','FAILED_EXCEPTION','FAILED_DIVERGENCE']:
                print(f'SKIP {identifier} {existing["status"]}',flush=True);continue
            if existing and not resume:raise ValueError('Resume flag required')
            if not existing:
                if len(ledger['fits'])>=10:raise ValueError('No remaining fit budget')
                item={'run_id':identifier,'candidate':candidate,'model':model_name,'base_seed':2,'effective_seed':2+c['model_seed_offsets'][model_name],
                    'status':'RUNNING','epochs_completed':0,'best_validation_epoch':None,'train_samples':2387,'validation_samples':228,
                    'started_at_kst':stamp(),'finished_at_kst':None,'error':None,'input_data_sha256':g['datasets'][candidate]['array_sha256'],
                    'code_sha256':sha(__file__),'epoch1_resume_roundtrip':False,'RNG_restore_exact':False,'checkpoint_restore':False}
                ledger['fits'][identifier]=item;write_json(ledger_path,ledger)
            else:item=existing;item['status']='RUNNING'
            fitdir=run/identifier;fitdir.mkdir(exist_ok=True);latest=fitdir/'latest.pt';bestpath=fitdir/'best.pt';history_path=fitdir/'history.json'
            print(f'START {identifier} seed={item["effective_seed"]} fit={len(ledger["fits"])}/10',flush=True)
            try:
                seed=item['effective_seed'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
                generator=torch.Generator().manual_seed(seed)
                loader=torch.utils.data.DataLoader(torch.utils.data.TensorDataset(tx,ty),batch_size=64,shuffle=True,generator=generator,num_workers=0,pin_memory=False)
                criterion=ns['FocalLoss'](gamma=2,alpha=.25)
                history=[];best_score=-1.;best_epoch=None;counter=0;start_epoch=1
                model,opt,sch=make_bundle(model_name,len(loader))
                if latest.exists():
                    model,opt,sch,payload=load_bundle(latest,model_name,len(loader),generator)
                    if payload['run_id']!=identifier or payload['input_data_sha256']!=item['input_data_sha256']:raise ValueError('Resume data identity changed')
                    history=payload['history'];best_score=payload['early_stopping']['best_score'];best_epoch=payload['early_stopping']['best_epoch'];counter=payload['early_stopping']['counter'];start_epoch=payload['completed_epoch']+1
                    item['epochs_completed']=payload['completed_epoch'];item['resume_from_committed_epoch']=payload['completed_epoch']
                for epoch in range(start_epoch,101):
                    if counter>=10:break
                    then=time.perf_counter();model.train();loss_sum=0.;observed=0;steps=0
                    for bx,by in loader:
                        opt.zero_grad(set_to_none=True);logits=model(bx);loss=criterion(logits,by)
                        if logits.shape!=(len(by),2) or not torch.isfinite(loss):raise FloatingPointError('Nonfinite training loss/output')
                        loss.backward();grads=[p.grad for p in model.parameters() if p.requires_grad]
                        if any(x is None or not torch.isfinite(x).all() for x in grads):raise FloatingPointError('Missing/nonfinite gradient')
                        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                        if not torch.isfinite(norm):raise FloatingPointError('Nonfinite gradient norm')
                        opt.step();sch.step();loss_sum+=float(loss.detach())*len(by);observed+=len(by);steps+=1
                    model.eval()
                    with torch.no_grad():vlogits=model(vx);vloss=criterion(vlogits,vy);probs=torch.softmax(vlogits,dim=1)[:,1]
                    if not torch.isfinite(vloss) or not torch.isfinite(probs).all():raise FloatingPointError('Nonfinite validation loss/probability')
                    metrics=validation_metrics(arrays['validation_y'],probs.numpy());improved=metrics['validation_BA']>best_score
                    if improved:best_score=metrics['validation_BA'];best_epoch=epoch;counter=0
                    else:counter+=1
                    row={'epoch':epoch,'train_loss':loss_sum/observed,'validation_loss':float(vloss),**metrics,
                         'optimizer_steps_this_epoch':steps,'scheduler_steps_total':int(sch.last_epoch),'learning_rate':float(opt.param_groups[0]['lr']),
                         'improved_validation_BA':improved,'early_stopping_counter':counter,'epoch_seconds':time.perf_counter()-then}
                    history.append(row)
                    payload={'scope':c['execution_mode'],'run_id':identifier,'Origin':'O1','Model':model_name,'candidate':candidate,'Seed':2,'effective_seed':seed,
                        'completed_epoch':epoch,'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':sch.state_dict(),
                        'early_stopping':{'best_score':best_score,'best_epoch':best_epoch,'counter':counter,'patience':10,'comparison':'strict greater, ties count as no improvement'},
                        'history':history,'feature_order':['Log_Ret','Disparity'],'scaler_metadata':meta['scaler'],'RNG':capture_rng(generator),
                        'input_data_sha256':item['input_data_sha256'],'source_price_sha256':g['datasets'][candidate]['price_sha256'],
                        'config_sha256':sha(config_path),'runner_sha256':sha(__file__),'environment':environment,'source_lineage':source_lineage,
                        'authorization_sha256':sha(approval_path),'Test_access':False,'resume_granularity':'committed epoch boundary'}
                    checkpoint(latest,payload)
                    if improved:checkpoint(bestpath,payload)
                    write_json(history_path,history)
                    item.update({'epochs_completed':epoch,'best_validation_epoch':best_epoch,'last_validation_BA':metrics['validation_BA'],
                                 'elapsed_training_seconds':float(sum(h['epoch_seconds'] for h in history))})
                    if epoch==1:
                        original_state=model.state_dict();original_opt=opt.state_dict();original_sch=sch.state_dict();saved_rng=payload['RNG']
                        restored,ropt,rsch,loaded=load_bundle(latest,model_name,len(loader),generator);restored.eval()
                        rng_exact=equal(capture_rng(generator),saved_rng)
                        with torch.no_grad():replay=restored(vx)
                        same=equal(original_state,restored.state_dict()) and equal(original_opt,ropt.state_dict()) and equal(original_sch,rsch.state_dict()) and torch.equal(vlogits,replay)
                        if not same or not rng_exact:raise RuntimeError('Epoch1 checkpoint/RNG continuation mismatch')
                        model,opt,sch=restored,ropt,rsch;item['epoch1_resume_roundtrip']=True;item['RNG_restore_exact']=True
                    write_json(ledger_path,ledger)
                    print(f'EPOCH {identifier} {epoch:03d} BA={metrics["validation_BA"]:.6f} best={best_score:.6f}@{best_epoch} wait={counter} pred_pos={metrics["prediction_positive_rate"]:.4f} seconds={row["epoch_seconds"]:.3f}',flush=True)
                    if epoch%5==0:export_progress()
                    if counter>=10:break
                selected_model,_,_,selected=load_bundle(bestpath,model_name,len(loader),generator);selected_model.eval()
                with torch.no_grad():selected_logits=selected_model(vx);selected_probs=torch.softmax(selected_logits,dim=1)[:,1].numpy()
                selected_metrics=validation_metrics(arrays['validation_y'],selected_probs)
                bestrow=next(h for h in history if h['epoch']==best_epoch)
                if any(selected_metrics[k]!=bestrow[k] for k in selected_metrics):raise RuntimeError('Selected best checkpoint metrics differ from history')
                np.savez(fitdir/'validation_predictions_private.npz',dates=np.array(dates['validation']['dates']),y_true=arrays['validation_y'],probability=selected_probs)
                item.update({'status':'COMPLETED','finished_at_kst':stamp(),'metrics':selected_metrics,'prediction_status':selected_metrics['prediction_status'],
                    'best_validation_epoch':best_epoch,'checkpoint_restore':True,'best_checkpoint_sha256':sha(bestpath),
                    'latest_checkpoint_sha256':sha(latest),'history_sha256':sha(history_path),
                    'validation_predictions_sha256':sha(fitdir/'validation_predictions_private.npz'),
                    'epochs_with_degenerate_prediction':int(sum(h['prediction_status']=='DEGENERATE_PREDICTION' for h in history)),
                    'full_fresh_retrain_reproducibility_executed':False,'early_stopping_selection_verified':True})
                print(f'DONE {identifier} epochs={item["epochs_completed"]} best={best_epoch} BA={selected_metrics["validation_BA"]:.6f} {item["prediction_status"]}',flush=True)
            except KeyboardInterrupt:
                item['status']='INTERRUPTED';item['error']='Interrupted; resume existing fit from latest committed epoch';export_progress();raise
            except Exception as exc:
                item.update({'status':'FAILED_DIVERGENCE' if isinstance(exc,FloatingPointError) else 'FAILED_EXCEPTION','error':str(exc),'error_type':type(exc).__name__,'finished_at_kst':stamp()})
                (fitdir/'error.log').write_text(traceback.format_exc());print(f'FAIL {identifier} {type(exc).__name__}: {exc}',flush=True)
            export_progress()
    ledger['completed']=all(ledger['fits'].get(i,{}).get('status') in ['COMPLETED','FAILED_EXCEPTION','FAILED_DIVERGENCE'] for i in expected_ids)
    ledger['finished_at_kst']=stamp();ledger['file_access_barrier']=barrier;export_progress()
    summary={'stage':'STEP3A','execution_mode':c['execution_mode'],'interpretation':'Retrospective exploratory implementation diagnostic; not production PIT, investment return, leakage-free or confirmatory generalization evidence',
        'run_directory':str(run.relative_to(root)),'started_at_kst':ledger['started_at_kst'],'finished_at_kst':ledger['finished_at_kst'],
        'fit_attempts':len(ledger['fits']),'maximum_fit_attempts':10,'completed_models':sum(i['status']=='COMPLETED' for i in ledger['fits'].values()),
        'failed_models':sum(i['status'].startswith('FAILED') for i in ledger['fits'].values()),'fit_ledger':ledger['fits'],
        'training_enabled':False,'hmm_fit_enabled':False,'pilot_execution_enabled':True,'production_gate_override':False,
        'source_status':'BOTH_UNVERIFIED','production_PIT_status':'BLOCKED','main_price_candidate_selected':None,
        'actual_Test_price_rows_read':0,'Test_predictions_generated':0,'test_dataframes_constructed':0,'2026_observations_used':0,
        'HMM_fit_executed':False,'GPU_executed':False,'full_RO_executed':False,'Ablation_executed':False,'full_Notebook_executed':False,
        'config_sha256':sha(config_path),'authorization_sha256':sha(approval_path),'preflight_sha256':sha(preflight_path),'runner_sha256':sha(__file__),
        'implementation_artifacts':c['implementation_artifacts'],'environment':environment,'original_definition_lineage':source_lineage,'data_provenance':g['datasets'],
        'file_access_barrier':barrier,'model_fit_repeated_to_select_A_B':False,'hyperparameters_changed_after_results':False,
        'checkpoints_predictions_raw_data_publication_allowed':False,'reproducibility_scope':'Epoch1 full-state/RNG exact continuation and final selected checkpoint validation reproduction; no additional full retraining'}
    write_json(root/'manifests/step3a_execution_manifest.json',summary);write_json(run/'execution_manifest_private.json',summary)
    return summary
