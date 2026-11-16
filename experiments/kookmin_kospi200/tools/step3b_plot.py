"""Plot aggregate validation diagnostics only; no market data or model execution."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];d=pd.read_csv(R/'manifests/step3b_runs.csv');out=R/'reports/assets';out.mkdir(exist_ok=True)
models=['RNN','LSTM','GRU','LTC','CfC'];colors={2:'#2060a7',12:'#cf5c24'}
fig,axs=plt.subplots(2,2,figsize=(10,7),sharex=True,sharey=True)
for ax,(origin,price) in zip(axs.flat,[(o,p) for o in ['O1','O2'] for p in ['A','B']]):
 for seed,delta in [(2,-.1),(12,.1)]:
  a=d[(d.origin==origin)&(d.candidate==price)&(d.seed==seed)].set_index('model').reindex(models)
  ax.scatter(np.arange(5)+delta,a.validation_BA,label=f'Seed {seed}',s=45,color=colors[seed],zorder=3)
 ax.axhline(.5,color='.6',linewidth=.8,linestyle='--');ax.set_title(f'{origin} | candidate {price}');ax.set_xticks(np.arange(5),models);ax.set_ylim(min(.35,float(d.validation_BA.min())-.03),max(.75,float(d.validation_BA.max())+.03));ax.grid(axis='y',alpha=.2);ax.set_ylabel('Selected Validation balanced accuracy')
axs[0,0].legend();fig.suptitle('Retrospective CPU pilot: 2 seeds; descriptive only\nO1 seed2 reuses STEP3A; Validation selected checkpoints',fontsize=11);fig.tight_layout();fig.savefig(out/'step3b_validation_BA.svg');plt.close(fig)
h=pd.read_csv(R/'manifests/step3b_epoch_history.csv');fig,axs=plt.subplots(2,2,figsize=(10,7),sharex=True)
for ax,(origin,price) in zip(axs.flat,[(o,p) for o in ['O1','O2'] for p in ['A','B']]):
 for seed in [2,12]:
  a=h[(h.origin==origin)&(h.candidate==price)&(h.seed==seed)&(h.model=='LTC')];ax.plot(a.epoch,a.validation_BA,color=colors[seed],marker='.',label=f'Seed {seed}');bad=a[a.prediction_status=='DEGENERATE_PREDICTION'];ax.scatter(bad.epoch,bad.validation_BA,marker='x',color=colors[seed],s=34)
 ax.axhline(.5,color='.6',linewidth=.8,linestyle='--');ax.set_title(f'{origin} | candidate {price}');ax.grid(alpha=.2);ax.set_xlabel('Epoch');ax.set_ylabel('Validation BA');ax.set_ylim(min(.35,float(h[h.model=='LTC'].validation_BA.min())-.03),max(.75,float(h[h.model=='LTC'].validation_BA.max())+.03))
axs[0,0].legend();fig.suptitle('LTC epoch diagnostics: x = single-class prediction\nFixed settings; no replacement seeds; no Test evaluation',fontsize=11);fig.tight_layout();fig.savefig(out/'step3b_LTC_epoch_diagnostics.svg');plt.close(fig)
print('Wrote two aggregate-only SVG figures')
