from dataclasses import replace

import numpy as np

from hatayama_contact import CONTACTS, HatayamaContactModel, ModelParameters


def test_electrode_ordering_at_100_nm() -> None:
    values = {}
    for name, contact in CONTACTS.items():
        result = HatayamaContactModel(contact).sweep()
        assert result.switchable
        assert result.onset_voltage_v is not None
        assert result.threshold_voltage_v is not None
        values[name] = result

    assert values["Hf"].onset_voltage_v > values["W"].onset_voltage_v > values["Pt"].onset_voltage_v
    assert values["Hf"].threshold_voltage_v > values["W"].threshold_voltage_v > values["Pt"].threshold_voltage_v
    assert values["Hf"].hold_voltage_v > values["W"].hold_voltage_v > values["Pt"].hold_voltage_v


def test_pf_parameters_are_contact_independent() -> None:
    voltage = np.linspace(0.0, 0.6, 20)
    curves = [HatayamaContactModel(contact).poole_frenkel_current(voltage) for contact in CONTACTS.values()]
    assert np.allclose(curves[0], curves[1])
    assert np.allclose(curves[1], curves[2])


def test_overlap_reduces_effective_barrier_and_suppresses_25_nm_pt() -> None:
    baseline = ModelParameters()
    model_100 = HatayamaContactModel(CONTACTS["Pt"], baseline)
    model_25 = HatayamaContactModel(CONTACTS["Pt"], replace(baseline, thickness_nm=25.0))
    result_25 = model_25.sweep()

    assert model_25.overlap_fraction > 0.0
    assert model_25.effective_built_in_potential_v < model_100.effective_built_in_potential_v
    assert not result_25.switchable
    assert result_25.threshold_voltage_v is None


def test_current_is_finite_and_compliance_limited() -> None:
    result = HatayamaContactModel(CONTACTS["Hf"]).sweep()
    assert np.all(np.isfinite(result.terminal_current_a))
    assert np.all(result.terminal_current_a >= 0.0)
    assert result.terminal_current_a.max() <= ModelParameters().compliance_current_a
