"""Versioned synthetic-only LTC tau instrumentation. No financial checkpoint I/O.

Uses AST insertion into the pinned installed solver; never edits ncps/frozen sources.
"""
from pathlib import Path
import ast,copy,hashlib,inspect,textwrap,types
import numpy as np
import torch
from .data import BlockedError
from .tau import time_constants,REFERENCE_SHA
CELL_SHA='167a9d6e1f4dc653ce21420010709e1c995716e53ad0d8bbc2d53c19c40b123f'
WRAPPER_SHA='bbf3127013d3969994ecf0debf4eb37b56db750475ee71646a9decdf1aaf3026'
TAU_REFERENCE_RTOL=2e-6;TAU_REFERENCE_ATOL=2e-7

def source_sha():return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
def weights_fingerprint(model):
 h=hashlib.sha256()
 for name,tensor in sorted(model.state_dict().items()):
  x=tensor.detach().cpu().contiguous();h.update(name.encode());h.update(str(tuple(x.shape)).encode());h.update(str(x.dtype).encode());h.update(x.numpy().tobytes())
 return h.hexdigest()
def installed_source_audit():
 from ncps.torch import LTC
 from ncps.torch.ltc_cell import LTCCell
 paths={'cell':Path(inspect.getfile(LTCCell)),'wrapper':Path(inspect.getfile(LTC))};digests={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
 if digests!={'cell':CELL_SHA,'wrapper':WRAPPER_SHA}:raise BlockedError('Pinned installed LTC source mismatch')
 return digests

def validate_metadata(meta,expected):
 required=['data_domain','origin','candidate','seed','checkpoint_sha256','LTCCell_source_sha256','tau_source_sha256','source_commit','dt_unit','prediction_base_date','prediction_base_session_id','observation_date','observation_session_id','window_time_index','elapsed_time','ode_unfolds','implicit_param_constraints','window_dates','window_session_ids']
 if any(k not in meta for k in required):raise BlockedError('Missing snapshot lineage')
 if len(meta['window_dates'])!=20 or len(meta['window_session_ids'])!=20 or not np.all(np.diff(meta['window_session_ids'])==1) or meta['window_session_ids'][-1]!=meta['prediction_base_session_id'] or meta['window_dates'][-1]!=meta['prediction_base_date']:raise BlockedError('Window/base session lineage mismatch')
 if meta['data_domain']!='SYNTHETIC_FIXTURE':raise BlockedError('STEP7A synthetic-only; financial snapshots disabled')
 for k in ['origin','candidate','seed','checkpoint_sha256']:
  if meta[k]!=expected.get(k):raise BlockedError('Origin/Candidate/seed/checkpoint identity mixing')
 for k in ['checkpoint_sha256','LTCCell_source_sha256','tau_source_sha256']:
  if not isinstance(meta[k],str) or len(meta[k])!=64 or any(c not in '0123456789abcdef' for c in meta[k]):raise BlockedError('Invalid source/checkpoint SHA')
 if meta['LTCCell_source_sha256']!=CELL_SHA or meta['tau_source_sha256']!=source_sha() or meta['source_commit']!=REFERENCE_SHA or meta['implicit_param_constraints'] is not True or meta['ode_unfolds']!=6 or meta['dt_unit']!='model_observation_step':raise BlockedError('Unverified constraint/source/solver/unit')
 if not np.isfinite(meta['elapsed_time']) or meta['elapsed_time']<=0:raise BlockedError('Invalid elapsed_time')
 return True

def require_cell(cell):
 installed_source_audit()
 if cell.training:raise BlockedError('model.eval required for nonintrusive instrumentation')
 if cell._implicit_param_constraints is not True or cell._ode_unfolds!=6 or cell._input_mapping!='affine' or cell._output_mapping!='affine' or cell._epsilon!=1e-8:raise BlockedError('Not frozen F1 wrapper cell configuration')
 if any(p.device.type!='cpu' or p.dtype not in [torch.float32,torch.float64] for p in cell.parameters()):raise BlockedError('CPU floating-point cell required')
 return True

def checked_tau(cm,gleak,sensory,recurrent):
 denom=gleak+sensory+recurrent
 if any(not torch.isfinite(t).all() for t in [cm,gleak,sensory,recurrent,denom]) or torch.any(cm<=0) or torch.any(gleak<=0) or torch.any(sensory<0) or torch.any(recurrent<0) or torch.any(denom<=0):raise BlockedError('Invalid/nonpositive conductance denominator')
 raw=(cm/gleak).expand_as(denom);eff=cm/denom
 if not torch.isfinite(raw).all() or not torch.isfinite(eff).all() or torch.any(raw<=0) or torch.any(eff<=0):raise BlockedError('Invalid/nonpositive tau')
 return {'tau_raw':raw.detach().clone(),'tau_effective':eff.detach().clone(),'sensory_sum':sensory.detach().clone(),'recurrent_sum':recurrent.detach().clone()}

def cell_tau(cell,raw_inputs,hidden):
 require_cell(cell)
 if raw_inputs.ndim!=2 or hidden.ndim!=2 or len(raw_inputs)!=len(hidden) or raw_inputs.shape[1]!=cell.sensory_size or hidden.shape[1]!=cell.state_size:raise BlockedError('Input/hidden shape mismatch')
 if not torch.isfinite(raw_inputs).all() or not torch.isfinite(hidden).all():raise BlockedError('Nonfinite input/state')
 p=cell._params;mapped=cell._map_inputs(raw_inputs)
 sw=cell.make_positive_fn(p['sensory_w'])*cell._sigmoid(mapped,p['sensory_mu'],p['sensory_sigma'])*p['sensory_sparsity_mask']
 rw=cell.make_positive_fn(p['w'])*cell._sigmoid(hidden,p['mu'],p['sigma'])*p['sparsity_mask']
 return checked_tau(cell.make_positive_fn(p['cm']),cell.make_positive_fn(p['gleak']),sw.sum(1),rw.sum(1))

def numpy_reference(cell,raw_inputs,hidden):
 p={k:v.detach().cpu().numpy().copy() for k,v in cell._params.items()}
 result=time_constants(raw_inputs.detach().cpu().numpy(),hidden.detach().cpu().numpy(),p,input_mapping=cell._input_mapping,implicit_constraints=cell._implicit_param_constraints,dt_unit='model_observation_step',source_commit=REFERENCE_SHA)
 if not all(np.isfinite(result[k]).all() and np.all(result[k]>0) for k in ['tau_raw','tau_effective']):raise BlockedError('Frozen reference returned invalid tau')
 return result

def build_solver(capture):
 from ncps.torch.ltc_cell import LTCCell
 installed_source_audit();tree=ast.parse(textwrap.dedent(inspect.getsource(LTCCell._ode_solver)));fn=tree.body[0];original_ast=ast.dump(fn,include_attributes=False);fn.name='_step7a_instrumented_solver';loops=[n for n in fn.body if isinstance(n,ast.For)];
 if len(loops)!=1:raise BlockedError('Pinned solver AST loop structure changed')
 body=loops[0].body;indices=[i for i,n in enumerate(body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='v_pre' for t in n.targets)]
 if len(indices)!=1:raise BlockedError('Pinned solver update AST changed')
 i=indices[0];before=ast.parse('_step7a_capture(self, inputs, v_pre, t, elapsed_time, sensory_w_activation, w_activation, gleak, cm_t)').body[0];after=ast.parse('_step7a_after(self, v_pre, t)').body[0];body.insert(i,before);body.insert(i+2,after);ast.fix_missing_locations(tree)
 arithmetic=copy.deepcopy(fn);arithmetic.name='_ode_solver'
 for loop in [n for n in ast.walk(arithmetic) if isinstance(n,ast.For)]:loop.body=[n for n in loop.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id in ['_step7a_capture','_step7a_after'])]
 if ast.dump(arithmetic,include_attributes=False)!=original_ast:raise BlockedError('Instrumentation changed solver arithmetic AST/order')
 namespace={'torch':torch,'_step7a_capture':capture.capture_substep,'_step7a_after':capture.capture_after};exec(compile(tree,'<pinned-LTCCell-ODE-with-readonly-tau-taps>','exec'),namespace)
 return namespace[fn.name]

class SyntheticTauTap:
 def __init__(self,cell,*,metadata,expected_identity):
  require_cell(cell);validate_metadata(metadata,expected_identity);self.cell=cell;self.metadata=dict(metadata);self.expected=dict(expected_identity);self.records=[];self.observations=[];self.hidden_outputs=[];self.index=-1;self.before_fingerprint=weights_fingerprint(cell);self._forward=cell.forward;self._solver=cell._ode_solver;self.compiled=build_solver(self)
 def __enter__(self):
  owner=self
  def tapped_forward(cell,inputs,states,elapsed_time=1.0):
   if weights_fingerprint(cell)!=owner.before_fingerprint:raise BlockedError('Parameters changed after instrumentation freeze')
   if 'batch_window_dates' in owner.metadata and (len(owner.metadata['batch_window_dates'])!=len(inputs) or len(owner.metadata.get('batch_window_session_ids',[]))!=len(inputs)):raise BlockedError('Per-row window lineage batch shape mismatch')
   owner.index+=1;owner.raw=inputs.detach().clone();owner.entry=states.detach().clone();owner.elapsed=elapsed_time
   if isinstance(elapsed_time,torch.Tensor):
    if not torch.isfinite(elapsed_time).all() or torch.any(elapsed_time<=0):raise BlockedError('Invalid timespan')
   elif not np.isfinite(elapsed_time) or elapsed_time<=0:raise BlockedError('Invalid timespan')
   obs=cell_tau(cell,inputs,states);owner.observations.append({**obs,'hidden_before':states.detach().clone(),'raw_inputs':inputs.detach().clone(),'time_index':owner.index,'solver_substep':None,'level':'OBSERVATION_ENTRY','lineage':owner.lineage(owner.index,None,elapsed_time),'elapsed_time':float(elapsed_time) if not isinstance(elapsed_time,torch.Tensor) else elapsed_time.detach().clone()})
   out=owner._forward(inputs,states,elapsed_time);owner.hidden_outputs.append(out[1].detach().clone());return out
  self.cell.forward=types.MethodType(tapped_forward,self.cell);self.cell._ode_solver=types.MethodType(self.compiled,self.cell);return self
 def lineage(self,time_index,substep,elapsed):
  if time_index<0 or time_index>=20:raise BlockedError('Unapproved window time_index')
  result={**self.metadata,'observation_date':self.metadata['window_dates'][time_index],'observation_session_id':self.metadata['window_session_ids'][time_index],'window_time_index':time_index,'solver_substep':substep,'elapsed_time':float(elapsed) if not isinstance(elapsed,torch.Tensor) else elapsed.detach().cpu().tolist(),'capture_level':'OBSERVATION_ENTRY' if substep is None else 'SOLVER_SUBSTEP_PRE_UPDATE','input_shape':list(self.raw.shape),'hidden_shape':list(self.entry.shape)}
  if 'batch_window_dates' in self.metadata:
   days=self.metadata['batch_window_dates'];ids=self.metadata['batch_window_session_ids']
   if any(len(d)!=20 or len(i)!=20 or not np.all(np.diff(i)==1) for d,i in zip(days,ids)):raise BlockedError('Per-row session windows invalid')
   result.update(prediction_base_date=[d[-1] for d in days],prediction_base_session_id=[i[-1] for i in ids],observation_date=[d[time_index] for d in days],observation_session_id=[i[time_index] for i in ids],lineage_is_per_batch_row=True)
  return result
 def capture_substep(self,cell,mapped_inputs,hidden,t,elapsed_time,sensory_activation,recurrent_activation,gleak,cm_t):
  result=checked_tau(cell.make_positive_fn(cell._params['cm']),gleak,sensory_activation.sum(1),recurrent_activation.sum(1));self.records.append({**result,'hidden_before':hidden.detach().clone(),'mapped_inputs':mapped_inputs.detach().clone(),'time_index':self.index,'solver_substep':int(t),'level':'SOLVER_SUBSTEP_PRE_UPDATE','lineage':self.lineage(self.index,int(t),elapsed_time),'elapsed_time':float(elapsed_time) if not isinstance(elapsed_time,torch.Tensor) else elapsed_time.detach().clone(),'cm_t_diagnostic':cm_t.detach().clone()})
 def capture_after(self,cell,hidden,t):self.records[-1]['hidden_after']=hidden.detach().clone()
 def __exit__(self,*args):
  self.cell.forward=self._forward;self.cell._ode_solver=self._solver
  if weights_fingerprint(self.cell)!=self.before_fingerprint:raise BlockedError('Parameter mutation during instrumentation')

def financial_tau_entrypoint(*args,**kwargs):
 raise BlockedError('STEP7A financial checkpoint/forward/tau extraction is disabled; independent STEP7B release required')
