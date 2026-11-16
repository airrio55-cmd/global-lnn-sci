"""Synthetic/data-only tests: no neural model, HMM fit, checkpoint or GPU."""
import ast,json,sys,unittest,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from kospi200.data import *
from kospi200.folds import *
from kospi200.specs import *
from kospi200.regimes import *
from kospi200.statistics import *
from kospi200.tau import time_constants,REFERENCE_SHA

class Step2Tests(unittest.TestCase):
    def fixture_calendar(self):
        # Synthetic weekday fixture only; never certifies the real KRX calendar.
        return Calendar(pd.bdate_range('2010-01-04','2025-12-30'),'SYNTHETIC_TEST_ONLY','a'*64,True)
    def records(self):
        return pd.DataFrame({'source_date':pd.to_datetime(['2025-03-07','2025-03-10']),
          'observed_at':pd.to_datetime(['2025-03-07T21:00Z','2025-03-10T20:00Z']),
          'available_at':pd.to_datetime(['2025-03-07T21:01Z','2025-03-10T20:01Z']),
          'value':[10.,20.],'source':['synthetic']*2,'source_sha256':['a'*64]*2,'record_id':['a','b']})
    def join(self, r, d, **extra):
        kw=dict(variable='Nasdaq',max_age='5d',availability_verified=True,metadata={'availability_evidence':'synthetic_release_fixture'})
        kw.update(extra);return pit_join(d,r,**kw)
    def test_01_original_hashes(self):
        for item in json.loads((ROOT/'evidence/input_manifest.json').read_text()):
            self.assertEqual(hashlib.sha256((ROOT/'originals'/item['filename']).read_bytes()).hexdigest(),item['sha256'])
    def test_02_cutoff_before_labels_and_2026_perturbation(self):
        raw=pd.read_csv(ROOT/'originals/KOSPI_200.csv');dt=pd.to_datetime(raw.Date)
        changed=raw.copy();changed.loc[dt>'2025-12-31','종가']=1e30
        pd.testing.assert_frame_equal(cutoff(raw),cutoff(changed))
        pd.testing.assert_frame_equal(cutoff(raw),cutoff(raw.loc[dt<='2025-12-31']))
        self.assertEqual(len(cutoff(raw)),3894)
    def test_03_nullable_tail_and_actual_calendar_endpoint(self):
        cal=self.fixture_calendar();close=pd.Series(np.arange(len(cal.sessions))+100.,index=cal.sessions)
        prices=close.drop(cal.sessions[30]);lab=labels_on_calendar(prices,cal)
        self.assertEqual(lab.Target.tail(20).isna().sum(),20)
        self.assertEqual(lab.label_end.iloc[0],cal.sessions[20])
        self.assertTrue(pd.isna(lab.Target.iloc[10]))  # missing real endpoint; not shifted 20 observed rows
        self.assertEqual(lab.label_status.iloc[10],'missing_KRX_endpoint_close')
    def test_04_unverified_calendar_blocks(self):
        with self.assertRaises(BlockedError):labels_on_calendar(pd.Series([1.],index=pd.to_datetime(['2025-01-02'])),Calendar(pd.to_datetime(['2025-01-02']),'observed','a'*64,False))
    def test_05_release_dst_and_different_calendar(self):
        r=self.records();d=pd.DataFrame({'decision_at':pd.to_datetime(['2025-03-10 18:00','2025-03-11 18:00']).tz_localize('Asia/Seoul')})
        out=self.join(r,d);self.assertEqual(out.value.tolist(),[10.,20.])
        self.assertTrue((out.available_at<=out.decision_at).all());self.assertEqual(out.status.tolist(),['PASS','PASS'])
        self.assertEqual(out.observed_at.dt.tz_convert('Asia/Seoul').dt.hour.tolist(),[6,5])
    def test_06_future_perturbation(self):
        r=self.records();d=pd.DataFrame({'decision_at':pd.to_datetime(['2025-03-10 18:00']).tz_localize('Asia/Seoul')})
        changed=r.copy();changed.loc[1,'value']=1e20
        pd.testing.assert_frame_equal(self.join(r,d),self.join(changed,d))
        pd.testing.assert_frame_equal(self.join(r,d),self.join(r.iloc[:1],d))
    def test_07_stale_no_prior_and_no_bfill(self):
        d=pd.DataFrame({'decision_at':pd.to_datetime(['2025-03-07 18:00','2025-03-18 18:00']).tz_localize('Asia/Seoul')})
        o=self.join(self.records(),d,max_age='1d');self.assertTrue(o.value.isna().all());self.assertEqual(o.status.tolist(),['BLOCKED','BLOCKED'])
    def test_08_unknown_availability_and_foreign_block(self):
        d=pd.DataFrame({'decision_at':pd.to_datetime(['2025-03-11 18:00']).tz_localize('Asia/Seoul')})
        with self.assertRaises(BlockedError):self.join(self.records(),d,availability_verified=False)
        with self.assertRaises(BlockedError):self.join(self.records(),d,variable='Foreign_Net')
        bad=self.records();bad['available_at']=bad.available_at.dt.tz_localize(None)
        with self.assertRaises(BlockedError):self.join(bad,d)
    def test_09_schedule_handles_dst_early_close(self):
        days=pd.to_datetime(['2025-03-07','2025-03-10','2025-11-28'])
        sched=pd.DataFrame({'source_date':days,'market_close':pd.to_datetime(['2025-03-07 16:00','2025-03-10 16:00','2025-11-28 13:00']).tz_localize('America/New_York')})
        vals=pd.DataFrame({'source_date':days,'value':[1.,2.,3.]})
        r=us_schedule_records(vals,sched,schedule_verified=True,source='synthetic',source_sha256='a'*64,release_policy_verified=True,release_delay='1min')
        self.assertEqual(r.observed_at.dt.hour.tolist(),[21,20,18])
        with self.assertRaises(BlockedError):us_schedule_records(vals,sched,schedule_verified=False,source='synthetic',source_sha256='a'*64,release_policy_verified=True,release_delay='1min')
    def test_10_origins_purge_and_tail(self):
        cal=self.fixture_calendar();lab=labels_on_calendar(pd.Series(100.+np.arange(len(cal.sessions)),index=cal.sessions),cal)
        manifest,folds=rolling_origins(lab,cal)
        self.assertEqual(len(manifest),15)
        for i in range(1,6):
            f=folds[f'O{i}'];vstart=cal.sessions[cal.sessions.year==2019+i][0];tstart=cal.sessions[cal.sessions.year==2020+i][0]
            self.assertTrue((lab.loc[f['train'],'label_end']<vstart).all())
            self.assertTrue((lab.loc[f['validation'],'label_end']<tstart).all())
        self.assertEqual(manifest.query("partition=='train'").purged_labels.tolist(),[20]*5)
        self.assertEqual(manifest.query("partition=='validation'").purged_labels.tolist(),[20]*5)
        self.assertEqual(manifest.query("origin=='O5' and partition=='test'").unknown_labels.iloc[0],20)
    def test_11_window_contract_and_history_reuse(self):
        s=pd.bdate_range('2020-01-01',periods=60);t=s[40]
        new=window_dates(s,[t],include_t=True)[t];old=window_dates(s,[t],include_t=False)[t]
        self.assertEqual(len(new),20);self.assertEqual(new[-1],t);self.assertEqual(old[-1],s[39]);self.assertEqual(new[0],s[21])
    def test_12_train_only_scaler_future_invariance(self):
        s=pd.bdate_range('2019-01-01',periods=80);x=pd.DataFrame({'x':np.arange(80.)},index=s)
        a,meta=train_only_scaler(x,s[:40],s[40]);changed=x.copy();changed.loc[s[40]:,'x']=1e30
        b,_=train_only_scaler(changed,s[:40],s[40]);np.testing.assert_array_equal(a.mean_,b.mean_);self.assertEqual(meta['fit_rows'],40)
        with self.assertRaises(BlockedError):train_only_scaler(x,s[:41],s[40])
    def test_13_configuration_and_ensemble(self):
        c=json.loads((ROOT/'configs/experiment_config.json').read_text());self.assertTrue(validate_config(c))
        out=ensemble([.2],[.8],[.9]);np.testing.assert_allclose(out['LNN Ensemble'],[.5]);np.testing.assert_allclose(out['Hybrid_SOTA'],[.62])
        old=json.loads((ROOT/'configs/original_reproduction_config.json').read_text());self.assertFalse(old['include_t']);self.assertFalse(old['same_condition_comparison_with_corrected'])
    def test_14_ablation_common_dates_and_order(self):
        self.assertEqual(ABLATIONS['F0'],RAW);self.assertEqual(ABLATIONS['F5'],['Log_Ret','Disparity','Foreign_Net'])
        dates=pd.to_datetime(['2025-01-02','2025-01-03']);a=pd.DataFrame({'a':[1.,2.]},index=dates);b=a.copy();b.iloc[1,0]=np.nan
        self.assertEqual(common_ablation_dates({'F0':a,'F1':b}).tolist(),[dates[0]])
    def test_15_hmm_filter_future_invariance_and_continuation(self):
        p=dict(startprob=[.5,.5],transmat=[[.9,.1],[.1,.9]],means=[[-1.],[1.]],covars=[[[1.]],[[1.]]])
        x=np.array([[-1.],[-.5],[1.]])
        a=forward_filter(x,**p);changed=x.copy();changed[-1]=1e10;b=forward_filter(changed,**p)
        np.testing.assert_array_equal(a[:2],b[:2]);np.testing.assert_allclose(a.sum(1),1)
        continued=forward_filter(x[2:],previous_posterior=a[1],**p);np.testing.assert_allclose(continued,a[2:])
    def test_16_train_regime_reference_and_no_fallback(self):
        a=train_regime_reference([1,2,3,4],[.1,.4],partition='train');self.assertEqual(a['state_order'],[0,1])
        with self.assertRaises(BlockedError):train_regime_reference([1,2],[1,2],partition='test')
        self.assertEqual(regime_status([0,0])['status'],'BLOCKED');self.assertEqual(regime_status(None)['status'],'BLOCKED')
    def prediction_fixture(self,seeds):
        rows=[]
        for i,d in enumerate(pd.bdate_range('2025-01-02',periods=100)):
            for seed in seeds:
                for m in ['a','b']:rows.append(dict(origin='O5',date=d,seed=seed,model=m,y=i%2,pred=(i%2 if m=='a' else (i+1)%2)))
        return pd.DataFrame(rows)
    def test_17_no_seed_pseudoreplication(self):
        a=paired_dates(self.prediction_fixture([2]),'a','b');b=paired_dates(self.prediction_fixture([2,12,22]),'a','b')
        pd.testing.assert_frame_equal(a,b);self.assertEqual(len(b),100)
        duplicate=pd.concat([self.prediction_fixture([2])]*2)
        with self.assertRaises(BlockedError):paired_dates(duplicate,'a','b')
    def test_18_bootstrap_blocks_and_holm(self):
        dates=paired_dates(self.prediction_fixture([2]),'a','b')
        for length in [20,40,60]:
            r=moving_block_bootstrap(dates,block_length=length,replicates=30,seed=3)
            self.assertEqual(r['market_dates'],100);self.assertEqual(r['effect'],1.);self.assertEqual(r['ci95'],[1.,1.])
        np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])
    def test_19_tau_synthetic_algebra_only(self):
        p=dict(cm=np.ones(2)*2,gleak=np.ones(2),w=np.ones((2,2)),mu=np.zeros((2,2)),sigma=np.ones((2,2)),sensory_w=np.ones((1,2)),sensory_mu=np.zeros((1,2)),sensory_sigma=np.ones((1,2)),sparsity_mask=np.ones((2,2)),sensory_sparsity_mask=np.ones((1,2)),input_w=np.ones(1),input_b=np.zeros(1))
        a=time_constants([[0.]],[[0.,0.]],p,implicit_constraints=False,dt_unit='synthetic_step',source_commit=REFERENCE_SHA)
        np.testing.assert_allclose(a['tau_raw'],[[2.,2.]]);np.testing.assert_allclose(a['tau_effective'],[[.8,.8]])
        b=time_constants([[5.]],[[5.,5.]],p,implicit_constraints=False,dt_unit='synthetic_step',source_commit=REFERENCE_SHA)
        self.assertTrue((b['tau_effective']<a['tau_effective']).all())
        with self.assertRaises(BlockedError):time_constants([[0.]],[[0.,0.]],p)
    def test_20_no_training_imports_or_execution_paths(self):
        for p in (ROOT/'src/kospi200').glob('*.py'):
            tree=ast.parse(p.read_text())
            for n in ast.walk(tree):
                if isinstance(n,(ast.Import,ast.ImportFrom)):
                    modules=([n.module] if isinstance(n,ast.ImportFrom) else [x.name for x in n.names])
                    self.assertFalse(any(x and x.split('.')[0] in ['torch','ncps','hmmlearn'] for x in modules),p.name)
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
                    self.assertNotIn(n.func.attr,['backward','load_state_dict','predict_proba','bfill'],p.name)
                    if n.func.attr=='fit':self.assertEqual(p.name,'folds.py')  # StandardScaler only
    def test_22_period_gates_and_hmm_train_plan(self):
        with self.assertRaises(BlockedError):local_features(pd.Series([1.,2.],index=pd.to_datetime(['2025-12-30','2026-01-02'])))
        with self.assertRaises(BlockedError):window_dates(pd.to_datetime(['2025-12-30','2026-01-02']),[])
        x=pd.DataFrame({'Log_Ret':[.1,.2],'Vol_Regime':[.3,.4]},index=pd.to_datetime(['2019-12-26','2019-12-27']))
        plan=hmm_training_plan(x,x.index,'2020-01-02',partition='train');self.assertFalse(plan['fit_enabled'])
        with self.assertRaises(BlockedError):hmm_training_plan(x,x.index,'2020-01-02',partition='test')
        sc,_=train_only_scaler(x,x.index,'2020-01-02')
        self.assertEqual(transform_checked(sc,x).shape,(2,2))
        with self.assertRaises(BlockedError):transform_checked(sc,x[['Vol_Regime','Log_Ret']])

    def test_23_keyed_ensemble_and_declarative_jobs(self):
        c=json.loads((ROOT/'configs/experiment_config.json').read_text());jobs=experiment_plan(c)
        self.assertEqual(len(jobs),3000);self.assertTrue(all(j['training_enabled'] is False for j in jobs))
        rows=pd.DataFrame([dict(origin='O5',seed=2,date='2025-01-02',model=m,probability=p) for m,p in [('LTC_RAW',.2),('LTC_LOG',.8),('RNN_RAW',.9)]])
        self.assertAlmostEqual(keyed_ensemble(rows)['Hybrid_SOTA'].iloc[0],.62)
        rows.loc[0,'seed']=12
        with self.assertRaises(BlockedError):keyed_ensemble(rows)

    def test_21_production_manifests_remain_blocked(self):
        m=json.loads((ROOT/'manifests/data_cutoff_manifest.json').read_text());self.assertIsNone(m['confirmed_production_sample_count'])
        self.assertEqual(m['candidate_counts']['unknown_tail'],20);self.assertEqual(m['candidate_counts']['last_valid_prediction_base_candidate'],'2025-12-01')
        f=pd.read_csv(ROOT/'manifests/rolling_origin_manifest.csv');self.assertEqual(len(f),15);self.assertTrue(f.status.eq('BLOCKED').all())

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Step2Tests)
    class Capture(unittest.TextTestResult):
        def startTest(self,test):super().startTest(test);self.rows=getattr(self,'rows',[])
        def addSuccess(self,test):super().addSuccess(test);self.rows.append({'test':test.id().split('.')[-1],'status':'PASS'})
        def addFailure(self,test,err):super().addFailure(test,err);self.rows.append({'test':test.id().split('.')[-1],'status':'FAIL'})
        def addError(self,test,err):super().addError(test,err);self.rows.append({'test':test.id().split('.')[-1],'status':'FAIL'})
    result=unittest.TextTestRunner(verbosity=2,resultclass=Capture).run(suite)
    (ROOT/'manifests/step2_test_results.json').write_text(json.dumps({'scope':'synthetic/data-only; no neural/HMM fit or model forward','tests':result.rows,'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors)},indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
