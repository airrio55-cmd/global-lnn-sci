"""Prespecified additions: existing fully-connected CfC and PE-only Transformer."""
import math
import torch

def install(ns):
 base=ns['TransformerClassifier'];original=ns['build_model']
 class PETransformer(base):
  def __init__(self,input_size):
   super().__init__(input_size)
   position=torch.arange(20,dtype=torch.float32).unsqueeze(1)
   divisor=torch.exp(torch.arange(0,128,2,dtype=torch.float32)*(-math.log(10000.)/128))
   pe=torch.zeros(20,128);pe[:,0::2]=torch.sin(position*divisor);pe[:,1::2]=torch.cos(position*divisor)
   self.register_buffer('positional_encoding',pe.unsqueeze(0))
  def forward(self,x):
   z=self.in_proj(x);z=z+self.positional_encoding[:,:z.size(1)]
   z=self.encoder(z);return self.fc(self.norm(z[:,-1,:]))
 def build(name,dim):return PETransformer(dim) if name=='PE-Transformer' else original(name,dim)
 ns['build_model']=build

def audit(ns,x):
 ns['set_seed'](42);original=ns['build_model']('Transformer',x.shape[-1]).eval()
 ns['set_seed'](42);pe=ns['build_model']('PE-Transformer',x.shape[-1]).eval()
 for name,param in original.state_dict().items():assert torch.equal(param,pe.state_dict()[name]),name
 assert set(pe.state_dict())-set(original.state_dict())=={'positional_encoding'}
 assert pe.positional_encoding.shape==(1,20,128)
 assert torch.equal(pe.positional_encoding[0,0,0::2],torch.zeros(64))
 assert torch.equal(pe.positional_encoding[0,0,1::2],torch.ones(64))
 with torch.no_grad():
  saved=pe.positional_encoding.clone();pe.positional_encoding.zero_();torch.testing.assert_close(original(x),pe(x),rtol=0,atol=0);pe.positional_encoding.copy_(saved)
 cfc=ns['build_model']('CfC',x.shape[-1]);assert cfc.dropout.p==.2 and cfc.fc.in_features==128 and cfc.fc.out_features==2
