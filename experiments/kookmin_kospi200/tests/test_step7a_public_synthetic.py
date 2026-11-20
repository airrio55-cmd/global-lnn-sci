"""Synthetic LTC only: conductance algebra, real solver taps and bitwise parity."""
from pathlib import Path
import copy, datetime, hashlib, inspect, json, random, sys, unittest
from unittest.mock import patch
import numpy as np, torch
from torch import nn
from ncps.torch import LTC, CfC
from ncps.torch.ltc_cell import LTCCell
from ncps.wirings import FullyConnected
R = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(R / 'src'), str(R)]
from kospi200.step7a_tau import *

def metadata(model):
    ds = [str(datetime.date(2018, 1, 1) + datetime.timedelta(days=i)) for i in range(20)]
    return {'data_domain': 'SYNTHETIC_FIXTURE', 'origin': 'O1', 'candidate': 'A', 'seed': 2, 'checkpoint_sha256': weights_fingerprint(model), 'LTCCell_source_sha256': CELL_SHA, 'tau_source_sha256': source_sha(), 'source_commit': REFERENCE_SHA, 'dt_unit': 'model_observation_step', 'prediction_base_date': ds[-1], 'prediction_base_session_id': 119, 'observation_date': ds[0], 'observation_session_id': 100, 'window_time_index': 0, 'window_dates': ds, 'window_session_ids': list(range(100, 120)), 'elapsed_time': 1.0, 'ode_unfolds': 6, 'implicit_param_constraints': True}

def identity(meta):
    return {k: meta[k] for k in ['origin', 'candidate', 'seed', 'checkpoint_sha256']}

def make_cell():
    torch.manual_seed(2)
    return LTC(2, 4).eval().rnn_cell

class TauSynthetic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        torch.use_deterministic_algorithms(True)
        torch.manual_seed(2)
        np.random.seed(2)
        random.seed(2)
        cls.wrapper = LTC(2, 4).eval()
        cls.baseline = copy.deepcopy(cls.wrapper)
        cls.instrumented = copy.deepcopy(cls.wrapper)
        cls.x = torch.randn(3, 20, 2)
        cls.meta = metadata(cls.wrapper)
        cls.rng_before = torch.get_rng_state().clone()
        cls.python_rng_before = random.getstate()
        cls.numpy_rng_before = np.random.get_state()
        with torch.no_grad():
            cls.y0, cls.h0 = cls.baseline(cls.x)
        cls.rng_baseline = torch.get_rng_state().clone()
        with torch.no_grad(), SyntheticTauTap(cls.instrumented.rnn_cell, metadata=cls.meta, expected_identity=identity(cls.meta)) as tap:
            cls.y1, cls.h1 = cls.instrumented(cls.x)
        cls.tap = tap
        cls.rng_after = torch.get_rng_state().clone()
        cls.python_rng_after = random.getstate()
        cls.numpy_rng_after = np.random.get_state()

    def test_01_raw_tau_positive_once(self):
        c = make_cell()
        p = c._params
        t = cell_tau(c, self.x[:, 0], torch.zeros(3, 4))
        expected = c.make_positive_fn(p['cm']) / c.make_positive_fn(p['gleak'])
        self.assertTrue(torch.equal(t['tau_raw'], expected.expand(3, 4)))

    def test_02_effective_definition(self):
        c = make_cell()
        t = cell_tau(c, self.x[:, 0], torch.zeros(3, 4))
        p = c._params
        want = c.make_positive_fn(p['cm']) / (c.make_positive_fn(p['gleak']) + t['sensory_sum'] + t['recurrent_sum'])
        self.assertTrue(torch.equal(t['tau_effective'], want))

    def test_03_double_softplus_not_used(self):
        c = make_cell()
        with torch.no_grad():
            c._params['cm'].fill_(-0.2)
            c._params['gleak'].fill_(-0.4)
        t = cell_tau(c, self.x[:, 0], torch.zeros(3, 4))
        once = torch.nn.functional.softplus(c._params['cm']) / torch.nn.functional.softplus(c._params['gleak'])
        twice = torch.nn.functional.softplus(torch.nn.functional.softplus(c._params['cm'])) / torch.nn.functional.softplus(torch.nn.functional.softplus(c._params['gleak']))
        self.assertTrue(torch.equal(t['tau_raw'][0], once))
        self.assertFalse(torch.allclose(once, twice))

    def test_04_sensory_gate_actual_source(self):
        c = make_cell()
        x = self.x[:, 0]
        p = c._params
        mapped = x * p['input_w'] + p['input_b']
        g = torch.sigmoid(p['sensory_sigma'] * (mapped.unsqueeze(-1) - p['sensory_mu']))
        want = (c.make_positive_fn(p['sensory_w']) * g * p['sensory_sparsity_mask']).sum(1)
        self.assertTrue(torch.equal(cell_tau(c, x, torch.zeros(3, 4))['sensory_sum'], want))

    def test_05_recurrent_gate_actual_source(self):
        c = make_cell()
        h = torch.randn(3, 4)
        p = c._params
        want = (c.make_positive_fn(p['w']) * torch.sigmoid(p['sigma'] * (h.unsqueeze(-1) - p['mu'])) * p['sparsity_mask']).sum(1)
        self.assertTrue(torch.equal(cell_tau(c, self.x[:, 0], h)['recurrent_sum'], want))

    def test_06_masks_zero_remove_conductance(self):
        c = make_cell()
        with torch.no_grad():
            c._params['sparsity_mask'].zero_()
            c._params['sensory_sparsity_mask'].zero_()
        t = cell_tau(c, self.x[:, 0], torch.randn(3, 4))
        self.assertTrue(torch.equal(t['tau_raw'], t['tau_effective']))

    def test_07_affine_mapping_exactly_once(self):
        c = make_cell()
        with torch.no_grad():
            c._params['input_w'].fill_(2.0)
            c._params['input_b'].fill_(0.3)
        t = cell_tau(c, self.x[:, 0], torch.zeros(3, 4))
        ref = numpy_reference(c, self.x[:, 0], torch.zeros(3, 4))
        self.assertTrue(np.allclose(t['tau_effective'].numpy(), ref['tau_effective'], rtol=TAU_REFERENCE_RTOL, atol=TAU_REFERENCE_ATOL))

    def test_08_hidden_shape_and_step_timing(self):
        self.assertEqual(len(self.tap.observations), 20)
        self.assertTrue(torch.equal(self.tap.observations[0]['hidden_before'], torch.zeros(3, 4)))
        for i in range(1, 20):
            self.assertTrue(torch.equal(self.tap.observations[i]['hidden_before'], self.tap.hidden_outputs[i - 1]))
        with self.assertRaises(BlockedError):
            cell_tau(make_cell(), torch.zeros(3, 2), torch.zeros(3, 5))

    def test_09_six_real_substeps_and_timing(self):
        self.assertEqual(len(self.tap.records), 120)
        for t in range(20):
            records = self.tap.records[t * 6:(t + 1) * 6]
            self.assertEqual([r['solver_substep'] for r in records], list(range(6)))
            for j in range(1, 6):
                self.assertTrue(torch.equal(records[j]['hidden_before'], records[j - 1]['hidden_after']))
            self.assertTrue(torch.equal(records[-1]['hidden_after'], self.tap.hidden_outputs[t]))

    def test_10_elapsed_time_cm_t_and_nonunit_timespans(self):
        c = make_cell()
        meta = metadata(c)
        x = self.x[:, 0]
        h = torch.zeros(3, 4)
        with torch.no_grad(), SyntheticTauTap(c, metadata=meta, expected_identity=identity(meta)) as tap:
            c.forward(x, h, 0.5)
        expected = c.make_positive_fn(c._params['cm']) / (0.5 / 6)
        self.assertTrue(torch.equal(tap.records[0]['cm_t_diagnostic'], expected))
        self.assertEqual(tap.records[0]['elapsed_time'], 0.5)

    def test_11_ode_unfolds_and_constraints(self):
        self.assertEqual(self.wrapper.rnn_cell._ode_unfolds, 6)
        self.assertTrue(self.wrapper.rnn_cell._implicit_param_constraints)
        self.assertFalse(LTCCell(FullyConnected(4), in_features=2)._implicit_param_constraints)

    def test_12_cm_t_not_double_counted(self):
        c = make_cell()
        meta = metadata(c)
        x = self.x[:, 0]
        h = torch.zeros(3, 4)
        with torch.no_grad(), SyntheticTauTap(c, metadata=meta, expected_identity=identity(meta)) as a:
            c.forward(x, h, 1.0)
        with torch.no_grad(), SyntheticTauTap(c, metadata=meta, expected_identity=identity(meta)) as b:
            c.forward(x, h, 0.5)
        self.assertTrue(torch.equal(a.records[0]['tau_effective'], b.records[0]['tau_effective']))

    def test_13_finite_positive_and_NaN_rejection(self):
        for r in self.tap.records:
            self.assertTrue(torch.isfinite(r['tau_raw']).all() and torch.isfinite(r['tau_effective']).all())
            self.assertTrue((r['tau_raw'] > 0).all() and (r['tau_effective'] > 0).all())
        with self.assertRaises(BlockedError):
            cell_tau(make_cell(), torch.full((3, 2), float('nan')), torch.zeros(3, 4))

    def test_14_forward_bitwise_equivalent(self):
        self.assertTrue(torch.equal(self.y0, self.y1))

    def test_15_final_and_all_step_hidden_bitwise(self):
        self.assertTrue(torch.equal(self.h0, self.h1))
        hidden = []
        original = self.baseline.rnn_cell.forward

        def trace(*a, **k):
            out = original(*a, **k)
            hidden.append(out[1].clone())
            return out
        self.baseline.rnn_cell.forward = trace
        with torch.no_grad():
            self.baseline(self.x)
        self.baseline.rnn_cell.forward = original
        self.assertTrue(all((torch.equal(a, b) for a, b in zip(hidden, self.tap.hidden_outputs))))

    def test_16_same_weight_input_tau_reproducible(self):
        c = copy.deepcopy(self.wrapper.rnn_cell)
        meta = metadata(c)
        with torch.no_grad(), SyntheticTauTap(c, metadata=meta, expected_identity=identity(meta)) as b:
            c.forward(self.x[:, 0], torch.zeros(3, 4), 1.0)
        for a, r in zip(self.tap.records[:6], b.records):
            self.assertTrue(torch.equal(a['tau_effective'], r['tau_effective']))

    def test_17_input_dependence(self):
        c = make_cell()
        h = torch.zeros(3, 4)
        a = cell_tau(c, torch.zeros(3, 2), h)
        b = cell_tau(c, torch.ones(3, 2), h)
        self.assertFalse(torch.equal(a['tau_effective'], b['tau_effective']))

    def test_18_hidden_dependence(self):
        c = make_cell()
        x = torch.zeros(3, 2)
        self.assertFalse(torch.equal(cell_tau(c, x, torch.zeros(3, 4))['tau_effective'], cell_tau(c, x, torch.ones(3, 4))['tau_effective']))

    def test_19_constraint_mode_wrong_blocked(self):
        c = LTCCell(FullyConnected(4), in_features=2)
        with self.assertRaises(BlockedError):
            cell_tau(c, torch.zeros(3, 2), torch.zeros(3, 4))
        with self.assertRaises(BlockedError):
            validate_metadata({**self.meta, 'implicit_param_constraints': False}, identity(self.meta))

    def test_20_metadata_SHA_missing_blocked(self):
        for key in ['checkpoint_sha256', 'tau_source_sha256', 'elapsed_time', 'window_session_ids']:
            m = dict(self.meta)
            del m[key]
            with self.assertRaises(BlockedError):
                validate_metadata(m, identity(self.meta))
        with self.assertRaises(BlockedError):
            validate_metadata({**self.meta, 'LTCCell_source_sha256': 'a' * 64}, identity(self.meta))

    def test_21_parameter_mutation_detected(self):
        c = make_cell()
        m = metadata(c)
        tap = SyntheticTauTap(c, metadata=m, expected_identity=identity(m))
        with torch.no_grad():
            c._params['cm'].add_(0.1)
        with self.assertRaises(BlockedError):
            with torch.no_grad(), tap:
                c.forward(self.x[:, 0], torch.zeros(3, 4), 1.0)

    def test_22_ordinary_hook_cannot_see_substeps(self):
        model = copy.deepcopy(self.wrapper)
        cell_calls = []
        wrapper_calls = []
        a = model.rnn_cell.register_forward_hook(lambda *x: cell_calls.append(1))
        b = model.register_forward_hook(lambda *x: wrapper_calls.append(1))
        with torch.no_grad():
            model(self.x)
        a.remove()
        b.remove()
        self.assertEqual(cell_calls, [])
        self.assertEqual(wrapper_calls, [1])
        self.assertEqual(len(self.tap.records), 120)

    def test_23_identity_mix_blocked(self):
        for key, value in [('origin', 'O2'), ('candidate', 'B'), ('seed', 12)]:
            with self.assertRaises(BlockedError):
                validate_metadata({**self.meta, key: value}, identity(self.meta))

    def test_24_financial_load_forward_blocked(self):
        with patch('torch.load', side_effect=AssertionError('No financial checkpoint load')), patch('builtins.open', side_effect=AssertionError('No financial read')):
            with self.assertRaises(BlockedError):
                financial_tau_entrypoint(approved=True, financial_tau_enabled=True)

    def test_25_RNG_and_all_parameters_unchanged(self):
        self.assertTrue(torch.equal(self.rng_before, self.rng_baseline))
        self.assertTrue(torch.equal(self.rng_baseline, self.rng_after))
        self.assertEqual(weights_fingerprint(self.wrapper), weights_fingerprint(self.instrumented))
        self.assertEqual(weights_fingerprint(self.wrapper), weights_fingerprint(self.baseline))

    def test_26_every_substep_numpy_reference(self):
        for r in self.tap.records:
            ref = numpy_reference(self.wrapper.rnn_cell, self.x[:, r['time_index']], r['hidden_before'])
            self.assertTrue(np.allclose(r['tau_effective'].numpy(), ref['tau_effective'], rtol=TAU_REFERENCE_RTOL, atol=TAU_REFERENCE_ATOL))

    def test_27_observation_entry_is_substep0(self):
        for obs in self.tap.observations:
            self.assertTrue(torch.equal(obs['tau_effective'], self.tap.records[obs['time_index'] * 6]['tau_effective']))
            self.assertIsNone(obs['solver_substep'])

    def test_28_reversal_does_not_enter_fixed_state_conductance(self):
        c = make_cell()
        x = self.x[:, 0]
        h = torch.zeros(3, 4)
        a = cell_tau(c, x, h)
        with torch.no_grad():
            c._params['erev'].mul_(-1)
            c._params['sensory_erev'].mul_(-1)
        self.assertTrue(torch.equal(a['tau_effective'], cell_tau(c, x, h)['tau_effective']))

    def test_30_lineage_shape_substep_and_two_dates(self):
        r = self.tap.records[7]
        l = r['lineage']
        self.assertEqual(l['window_time_index'], 1)
        self.assertEqual(l['solver_substep'], 1)
        self.assertEqual(l['observation_session_id'], 101)
        self.assertEqual(l['prediction_base_session_id'], 119)
        self.assertEqual(l['hidden_shape'], [3, 4])
        self.assertEqual(l['input_shape'], [3, 2])

    def test_31_per_batch_row_distinct_session_lineage(self):
        c = make_cell()
        m = metadata(c)
        m['batch_window_dates'] = [[str(datetime.date(2018, 1, 1) + datetime.timedelta(days=i + j)) for i in range(20)] for j in range(3)]
        m['batch_window_session_ids'] = [list(range(100 + j, 120 + j)) for j in range(3)]
        with torch.no_grad(), SyntheticTauTap(c, metadata=m, expected_identity=identity(m)) as tap:
            c.forward(self.x[:, 0], torch.zeros(3, 4), 1.0)
        l = tap.records[0]['lineage']
        self.assertEqual(l['observation_session_id'], [100, 101, 102])
        self.assertEqual(l['prediction_base_session_id'], [119, 120, 121])
        self.assertTrue(l['lineage_is_per_batch_row'])

    def test_32_python_numpy_RNG_not_consumed(self):
        self.assertEqual(self.python_rng_before, self.python_rng_after)
        a = self.numpy_rng_before
        b = self.numpy_rng_after
        self.assertEqual(a[0], b[0])
        self.assertTrue(np.array_equal(a[1], b[1]))
        self.assertEqual(a[2:], b[2:])

    def test_33_training_mode_blocked(self):
        c = make_cell()
        c.train()
        with self.assertRaises(BlockedError):
            cell_tau(c, torch.zeros(3, 2), torch.zeros(3, 4))

if __name__ == "__main__":
    unittest.main(verbosity=2)
