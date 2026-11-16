"""Static source extraction and inert smoke plan. Never imports/constructs a model."""
import ast, hashlib
from .data import BlockedError
from .specs import validate_config


def extract_original_definitions(notebook):
    """AST extracts definitions as TEXT, never eval/exec or notebook execution.

    Source fidelity is retained; unsafe original training/evaluation routines are
    audit references only. A future approved runner must isolate test selection.
    """
    sources={}
    for cell_number,names in [(6,['FocalLoss']),(8,['init_weights','RecurrentModel','LNNModel','CfCModel','EarlyStopping']),
                              (12,['train_model','calculate_metrics'])]:
        source=''.join(notebook['cells'][cell_number-1]['source']);tree=ast.parse(source)
        for name in names:
            found=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
            if len(found)!=1:raise BlockedError('Ambiguous original definition '+name)
            n=found[0];segment=ast.get_source_segment(source,n)
            sources[name]={'source':segment,'cell':cell_number,'line_start':n.lineno,'line_end':n.end_lineno,
                           'sha256':hashlib.sha256(segment.encode()).hexdigest()}
    return sources


def static_parameter_count(model,input_size,h=128):
    """One layer, 2 logits; LTC/CfC reference ncps1.0.1 only, not runtime proof."""
    if model in ['RNN','LSTM','GRU']:
        g={'RNN':1,'LSTM':4,'GRU':3}[model]
        trainable=g*(h*input_size+h*h+2*h)+2*h+2;fixed=0
    elif model=='LTC':
        trainable=4*h*h+4*input_size*h+7*h+2*input_size+2;fixed=h*h+input_size*h
    elif model=='CfC':
        trainable=5*h*h+h*input_size+7*h+2;fixed=0
    else:raise BlockedError('Unknown model')
    return {'trainable':trainable,'nontrainable_registered':fixed,'total_registered':trainable+fixed,
            'status':'STATIC_FORMULA_ONLY','runtime_verified':False}


def smoke_plan(config, gates):
    validate_config(config)
    if config.get('training_enabled') is not False or config.get('hmm_fit_enabled') is not False:
        raise BlockedError('Disabled flags required')
    required=['data_validation','input_time_contract','label_purging','full_excel_comparison',
              'model_environment','protocol_frozen','explicit_step3_execution_approval']
    # Fail closed even when callers omit a gate. This function only returns data.
    return {'training_enabled':False,'hmm_fit_enabled':False,'gpu_enabled':False,
            'executable':False,'status':'BLOCKED_NO_EXECUTION',
            'unmet_gates':[k for k in required if gates.get(k)!='PASS'],
            'origin':'O1','feature_spec':'F1','seed':config['seeds'][0],
            'models':config['models'],'channels':['RAW','LOG'],
            'features':{'RAW':['Log_Ret','Disparity'],'LOG':['Log_Ret','Disparity']},
            'model_settings':dict(config['model']),
            'future_smoke_limit':{'training_batches':1,'validation_batches':1,'test_access':False},
            'limitation':'Future batch limit is an implementation smoke, not a performance experiment; no Test access'}
