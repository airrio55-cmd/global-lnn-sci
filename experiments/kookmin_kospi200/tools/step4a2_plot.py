"""Aggregate Validation figures only; no financial rows, model loading or training."""
from pathlib import Path
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];out=R/'reports/assets';out.mkdir(exist_ok=True);d=pd.read_csv(R/'manifests/step4a2_runs.csv');models=['RNN','LSTM','GRU','LTC','CfC'];col={2:'#2060a7',12:'#cf5c24'}
fig,axes=plt.subplots(2,2,figsize=(11,7),sharey=True)
for ax,(origin,candidate) in zip(axes.flat,[(o,p) for o in ['O4','O5'] for p in ['A','B']]):
 for seed,offset in [(2,-.1),(12,.1)]:
  x=d[(d.origin==origin)&(d.candidate==candidate)&(d.seed==seed)].set_index('model').reindex(models);ax.scatter(np.arange(5)+offset,x.validation_BA,label=f'Seed{seed}',color=col[seed],s=45)
 ax.axhline(.5,color='.6',linestyle='--',linewidth=.8);ax.set_xticks(range(5),models);ax.set_title(f'{origin} Candidate{candidate}');ax.set_ylabel('Selected Validation BA');ax.grid(axis='y',alpha=.2);ax.set_ylim(min(.35,d.validation_BA.min()-.03),max(.75,d.validation_BA.max()+.03))
axes[0,0].legend();fig.suptitle('O4/O5 retrospective CPU Pilot | two seeds, descriptive only');fig.tight_layout();fig.savefig(out/'step4a2_validation_BA.svg');plt.close(fig)
a=pd.read_csv(R/'manifests/step3b_epoch_history.csv');b=pd.read_csv(R/'manifests/step4a1_epoch_history.csv');new=pd.read_csv(R/'manifests/step4a2_epoch_history.csv');h=pd.concat([a,b,new],ignore_index=True);h=h[h.model=='LTC'];fig,axes=plt.subplots(5,2,figsize=(11,15),sharex=True,sharey=True)
for ax,(origin,candidate) in zip(axes.flat,[(o,c) for o in ['O1','O2','O3','O4','O5'] for c in ['A','B']]):
 for seed in [2,12]:
  x=h[(h.origin==origin)&(h.candidate==candidate)&(h.seed==seed)];ax.plot(x.epoch,x.validation_BA,color=col[seed],marker='.',label=f'Seed{seed}');bad=x[x.prediction_status=='DEGENERATE_PREDICTION'];ax.scatter(bad.epoch,bad.validation_BA,marker='x',color=col[seed],s=32)
 ax.axhline(.5,color='.6',linestyle='--',linewidth=.8);ax.set_title(f'{origin} Candidate{candidate}');ax.set_xlabel('Epoch');ax.set_ylabel('Validation BA');ax.grid(alpha=.2);ax.set_ylim(min(.35,h.validation_BA.min()-.03),max(.75,h.validation_BA.max()+.03))
axes[0,0].legend();fig.suptitle('LTC diagnostics: x=single-class prediction\nO1/O2/O3 reused; O4/O5 new. Different validation years, no causal claim.');fig.tight_layout();fig.savefig(out/'step4a2_LTC_origin_epoch.svg');plt.close(fig)
print('Two aggregate-only SVG figures written')
