"""Versioned STEP5B Test policy v1; no statistics, model or data loading."""
import numpy as np
from .data import BlockedError
from .manual_evaluation import supplied_prediction_metrics
VERSION='STEP5B_TEST_METRICS_V1'
def test_metrics(y,probability):
 y=np.asarray(y);p=np.asarray(probability,dtype=float)
 if y.ndim!=1 or p.shape!=y.shape or not np.isin(y,[0,1]).all() or not np.isfinite(p).all() or ((p<0)|(p>1)).any():raise BlockedError('Invalid labels/probabilities; no null-to-zero conversion')
 pred=(p>.5).astype(np.int64);z=supplied_prediction_metrics(y,pred)
 return {'BA':z['balanced_accuracy'],'macro_f1':z['macro_f1'],'recall0':z['recall_class0'],'recall1':z['recall_class1'],'brier':float(np.mean((p-y)**2)) if len(y) else None,'accuracy':float(np.mean(pred==y)) if len(y) else None,'positive_rate':float(pred.mean()) if len(y) else None,'prediction_status':'EMPTY' if not len(y) else 'DEGENERATE_PREDICTION' if np.unique(pred).size==1 else 'TWO_CLASS_PREDICTION','n':len(y),'support0':z['n_class0'],'support1':z['n_class1'],'tn':int(((y==0)&(pred==0)).sum()),'fp':int(((y==0)&(pred==1)).sum()),'fn':int(((y==1)&(pred==0)).sum()),'tp':int(((y==1)&(pred==1)).sum())}
def check_job(job,roster):
 exact=[x for x in roster if x['run_id']==job.get('run_id')]
 if len(exact)!=1 or job!=exact[0]:raise BlockedError('Unapproved/altered frozen identity')
 return True
