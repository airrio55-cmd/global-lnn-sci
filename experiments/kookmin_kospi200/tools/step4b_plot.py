"""Standalone aggregate-only figures; no prices, daily labels or probabilities."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
def main():
 frame=pd.read_csv(R/'manifests/step4b_all200_diagnostic_metrics.csv',float_precision='round_trip')
 out=R/'reports/assets';out.mkdir(exist_ok=True)
 models=['RNN','LSTM','GRU','LTC','CfC'];seeds=[2,12,22,32];origins=['O1','O2','O3','O4','O5'];colors=['#0072B2','#E69F00','#009E73','#CC79A7']
 fig,axes=plt.subplots(2,5,figsize=(16,7),sharey=True)
 for row,candidate in enumerate(['A','B']):
  for col,origin in enumerate(origins):
   ax=axes[row,col];part=frame[(frame.origin==origin)&(frame.candidate==candidate)&frame.status.eq('COMPLETED')]
   for i,seed in enumerate(seeds):
    t=part[part.seed==seed].set_index('model');ys=pd.to_numeric(t.reindex(models).validation_BA,errors='coerce').to_numpy();ax.scatter(np.arange(5)+(i-1.5)*.13,ys,color=colors[i],s=23,label=f'Seed {seed}',zorder=3)
   means=[];std=[]
   for model in models:
    v=part[part.model==model].validation_BA.dropna();means.append(v.mean() if len(v) else np.nan);std.append(v.std(ddof=1) if len(v)>1 else np.nan)
   ax.errorbar(np.arange(5),means,yerr=std,fmt='_',color='black',capsize=3,linewidth=1,label='Mean +/- sample SD')
   ax.axhline(.5,color='#888888',linestyle='--',linewidth=.8);ax.set_xticks(np.arange(5),models,rotation=35);ax.set_title(f'{origin} / {2019+int(origin[1])} / price {candidate}');ax.grid(axis='y',alpha=.18);ax.set_ylim(0,1)
 axes[0,0].set_ylabel('Validation balanced accuracy');axes[1,0].set_ylabel('Validation balanced accuracy')
 h,l=axes[0,0].get_legend_handles_labels();fig.legend(h,l,ncol=5,loc='lower center');fig.suptitle('STEP4B: descriptive validation diagnostics; four seeds are not independent market samples');fig.tight_layout(rect=[0,.08,1,.94]);fig.savefig(out/'step4b_seed_validation.svg');plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(11,5),sharey=True)
 for ax,candidate in zip(axes,['A','B']):
  t=frame[(frame.model=='LTC')&(frame.candidate==candidate)];ratio=np.full((5,4),np.nan)
  for i,o in enumerate(origins):
   for j,s in enumerate(seeds):
    v=t[(t.origin==o)&(t.seed==s)]
    if len(v) and v.iloc[0].status=='COMPLETED':ratio[i,j]=v.iloc[0].degenerate_epoch_ratio
  image=ax.imshow(np.ma.masked_invalid(ratio),vmin=0,vmax=1,cmap='YlOrRd',aspect='auto')
  for i,o in enumerate(origins):
   for j,s in enumerate(seeds):
    v=t[(t.origin==o)&(t.seed==s)]
    if not np.isfinite(ratio[i,j]):label='N/A'
    else:label=f'{ratio[i,j]:.0%}'+('\nBEST single class' if v.iloc[0].prediction_status=='DEGENERATE_PREDICTION' else '')
    ax.text(j,i,label,ha='center',va='center',fontsize=8,color='white' if np.isfinite(ratio[i,j]) and ratio[i,j]>.7 else 'black')
  ax.set_xticks(np.arange(4),[f'Seed {s}' for s in seeds]);ax.set_yticks(np.arange(5),origins);ax.set_title(f'LTC / price {candidate}')
 fig.colorbar(image,ax=axes.ravel().tolist(),label='Fraction of epochs with single-class predictions',shrink=.8);fig.suptitle('STEP4B LTC instability: complete fits only; failed/missing cells remain N/A');fig.subplots_adjust(top=.86,bottom=.12,wspace=.3,right=.82);fig.savefig(out/'step4b_LTC_degenerate.svg');plt.close(fig)
 print('Two aggregate-only STEP4B SVG figures written')
if __name__=='__main__':main()
