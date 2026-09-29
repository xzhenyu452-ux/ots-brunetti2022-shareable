"""Reduced contact-aware OTS model based on Hatayama et al. (2025).

The published equations cover depletion-layer band bending, Poole-Frenkel
transport, and lucky-drift impact ionization.  The paper does not provide a
closed ON-state equation.  This reproduction therefore keeps the published
OFF/preswitch equations and adds an explicitly labelled engineering ON branch
with current compliance for plotting a complete voltage sweep.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

K_B_EV = 8.617333262e-5


@dataclass(frozen=True)
class ContactSpec:
    name: str
    work_function_ev: float
    built_in_potential_v: float
    depletion_width_nm: float


CONTACTS: dict[str, ContactSpec] = {
    "Hf": ContactSpec("Hf", 3.90, 0.282, 28.8),
    "W": ContactSpec("W", 4.55, 0.218, 28.2),
    "Pt": ContactSpec("Pt", 5.65, 0.145, 23.0),
}


@dataclass(frozen=True)
class ModelParameters:
    # Paper-anchored GeTe6 parameters.
    thickness_nm: float = 100.0
    donor_density_cm3: float = 1.0e18
    permittivity_f_cm: float = 2.92e-12
    trap_depth_ev: float = 0.300
    ionization_energy_ev: float = 0.950
    temperature_k: float = 300.0

    # Baseline calibration parameters; not tabulated by the paper.
    pf_prefactor_a: float = 5.0e-2
    trap_spacing_nm: float = 18.0
    impact_prefactor_m_inv: float = 1.0e9
    mean_free_path_nm: float = 15.0
    contact_coupling_gain: float = 6.2
    contact_coupling_floor_v: float = 0.130
    onset_multiplication: float = 1.01
    threshold_multiplication: float = 1.50
    maximum_multiplication: float = 1.0e6
    minimum_switching_barrier_v: float = 0.090
    hold_base_v: float = 0.25
    hold_contact_gain: float = 1.80
    on_resistance_ohm: float = 1.5e3
    non_ots_resistance_ohm: float = 8.0e3
    series_resistance_ohm: float = 50.0
    compliance_current_a: float = 1.0e-3


@dataclass(frozen=True)
class SweepResult:
    source_voltage_v: np.ndarray
    pf_current_a: np.ndarray
    multiplied_current_a: np.ndarray
    terminal_current_a: np.ndarray
    multiplication: np.ndarray
    physical_contact_drop_v: np.ndarray
    bulk_voltage_v: np.ndarray
    ionization_drive_voltage_v: np.ndarray
    onset_voltage_v: float | None
    threshold_voltage_v: float | None
    hold_voltage_v: float | None
    effective_built_in_potential_v: float
    depletion_overlap_fraction: float
    switchable: bool


class HatayamaContactModel:
    """Quasi-static PF + impact-ionization model with Schottky contacts."""

    def __init__(
        self,
        contact: ContactSpec,
        params: ModelParameters | None = None,
    ) -> None:
        self.contact = contact
        self.params = params or ModelParameters()

    @property
    def overlap_fraction(self) -> float:
        """Fractional overlap of the two nominal depletion regions."""
        p = self.params
        total_depletion_nm = 2.0 * self.contact.depletion_width_nm
        return float(np.clip(1.0 - p.thickness_nm / total_depletion_nm, 0.0, 1.0))

    @property
    def effective_built_in_potential_v(self) -> float:
        """Barrier remaining after the paper's depletion-overlap correction."""
        return self.contact.built_in_potential_v * (1.0 - self.overlap_fraction)

    @property
    def switchable(self) -> bool:
        return self.effective_built_in_potential_v >= self.params.minimum_switching_barrier_v

    @property
    def effective_contact_penalty_v(self) -> float:
        """Calibrated shift of impact-ionization onset, not a literal voltage drop."""
        p = self.params
        excess_barrier = max(
            self.effective_built_in_potential_v - p.contact_coupling_floor_v,
            0.0,
        )
        return p.contact_coupling_gain * excess_barrier

    def physical_voltage_partition(self, voltage_v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Simple band-flattening partition used only for interpretation plots."""
        voltage = np.asarray(voltage_v, dtype=float)
        contact_drop = np.minimum(np.maximum(voltage, 0.0), self.effective_built_in_potential_v)
        return contact_drop, np.maximum(voltage - contact_drop, 0.0)

    def poole_frenkel_current(self, voltage_v: np.ndarray) -> np.ndarray:
        p = self.params
        voltage = np.maximum(np.asarray(voltage_v, dtype=float), 0.0)
        barrier_ev = p.trap_depth_ev - voltage * p.trap_spacing_nm / (2.0 * p.thickness_nm)
        exponent = -barrier_ev / (K_B_EV * p.temperature_k)
        return p.pf_prefactor_a * np.exp(np.clip(exponent, -80.0, 40.0))

    def impact_multiplication(self, voltage_v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        p = self.params
        voltage = np.maximum(np.asarray(voltage_v, dtype=float), 0.0)
        drive_voltage = np.maximum(voltage - self.effective_contact_penalty_v, 1.0e-12)
        field_v_m = drive_voltage / (p.thickness_nm * 1.0e-9)
        energy_gain_ev = p.mean_free_path_nm * 1.0e-9 * field_v_m
        alpha_m_inv = p.impact_prefactor_m_inv * np.exp(
            np.clip(-p.ionization_energy_ev / energy_gain_ev, -100.0, 0.0)
        )
        log_m = alpha_m_inv * p.thickness_nm * 1.0e-9
        multiplication = np.exp(np.clip(log_m, 0.0, np.log(p.maximum_multiplication)))
        return multiplication, drive_voltage

    @staticmethod
    def _first_crossing(voltage: np.ndarray, values: np.ndarray, target: float) -> float | None:
        indices = np.flatnonzero(values >= target)
        if indices.size == 0:
            return None
        idx = int(indices[0])
        if idx == 0:
            return float(voltage[0])
        x0, x1 = voltage[idx - 1], voltage[idx]
        y0, y1 = values[idx - 1], values[idx]
        if y1 == y0:
            return float(x1)
        return float(x0 + (target - y0) * (x1 - x0) / (y1 - y0))

    def sweep(self, stop_voltage_v: float = 3.0, points: int = 1201) -> SweepResult:
        p = self.params
        voltage = np.linspace(0.0, stop_voltage_v, points)
        pf_current = self.poole_frenkel_current(voltage)
        multiplication, drive_voltage = self.impact_multiplication(voltage)
        multiplied_current = pf_current * multiplication
        contact_drop, bulk_voltage = self.physical_voltage_partition(voltage)

        if self.switchable:
            von = self._first_crossing(voltage, multiplication, p.onset_multiplication)
            vth = self._first_crossing(voltage, multiplication, p.threshold_multiplication)
            vh = p.hold_base_v + p.hold_contact_gain * self.effective_built_in_potential_v
            terminal = multiplied_current.copy()
            if vth is not None:
                on_mask = voltage >= vth
                on_current = np.maximum(voltage - vh, 0.0) / (
                    p.on_resistance_ohm + p.series_resistance_ohm
                )
                terminal[on_mask] = np.maximum(terminal[on_mask], on_current[on_mask])
            terminal = np.minimum(terminal, p.compliance_current_a)
        else:
            von = None
            vth = None
            vh = None
            terminal = np.minimum(
                voltage / (p.non_ots_resistance_ohm + p.series_resistance_ohm),
                p.compliance_current_a,
            )

        return SweepResult(
            source_voltage_v=voltage,
            pf_current_a=pf_current,
            multiplied_current_a=multiplied_current,
            terminal_current_a=terminal,
            multiplication=multiplication,
            physical_contact_drop_v=contact_drop,
            bulk_voltage_v=bulk_voltage,
            ionization_drive_voltage_v=drive_voltage,
            onset_voltage_v=von,
            threshold_voltage_v=vth,
            hold_voltage_v=vh,
            effective_built_in_potential_v=self.effective_built_in_potential_v,
            depletion_overlap_fraction=self.overlap_fraction,
            switchable=self.switchable,
        )
