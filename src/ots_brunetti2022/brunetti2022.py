"""Reduced dynamic two-level hot-carrier model after Brunetti et al. (2022).

This is a zero-dimensional reproduction of the paper's trap/mobile-state
model.  It keeps the two experimentally important relaxation times: carrier
temperature relaxation ``tau_T`` and mobile-carrier population relaxation
``tau_n``.  The full paper additionally solves the spatial transport and
external circuit equations.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

Q_E = 1.602176634e-19
K_B_J = 1.380649e-23
K_B_EV = 8.617333262e-5


@dataclass(frozen=True)
class Brunetti2022Parameters:
    trap_energy_ev: float = 0.0
    mobile_energy_ev: float = 0.35
    dos_ratio: float = 2.5e-3
    poole_gamma_c_m: float = 3.36e-28
    relative_permittivity: float = 15.0
    mobility_m2_v_s: float = 5.9e-4
    equilibrium_density_m3: float = 6.8e25
    temperature_relaxation_s: float = 1.5e-13
    population_relaxation_s: float = 0.6e-9
    length_m: float = 53e-9
    area_m2: float = 5_000e-18
    lattice_temperature_k: float = 298.0
    energy_coupling_efficiency: float = 0.60

    @property
    def level_separation_ev(self) -> float:
        return self.mobile_energy_ev - self.trap_energy_ev


@dataclass(frozen=True)
class BrunettiTransient:
    time_s: np.ndarray
    voltage_v: np.ndarray
    field_v_m: np.ndarray
    carrier_temperature_k: np.ndarray
    mobile_fraction: np.ndarray
    current_a: np.ndarray


class Brunetti2022Model:
    """Two-level, zero-dimensional transient approximation."""

    def __init__(self, params: Brunetti2022Parameters | None = None) -> None:
        self.params = params or Brunetti2022Parameters()

    def field_from_voltage(self, voltage_v: float) -> float:
        return float(voltage_v / self.params.length_m)

    def mobile_equilibrium_fraction(self, field_v_m: float, temperature_k: float) -> float:
        p = self.params
        barrier_ev = max(
            1e-4,
            p.level_separation_ev - p.poole_gamma_c_m * abs(field_v_m) / Q_E,
        )
        ratio = p.dos_ratio * np.exp(np.clip(barrier_ev / (K_B_EV * temperature_k), -80.0, 80.0))
        return float(np.clip(1.0 / (1.0 + ratio), 0.0, 1.0))

    def equilibrium_carrier_temperature(
        self, field_v_m: float, mobile_fraction: float
    ) -> float:
        """Local electronic energy balance including population feedback."""
        p = self.params
        heating = (
            p.energy_coupling_efficiency
            * (2.0 / 3.0)
            * Q_E
            * p.mobility_m2_v_s
            * field_v_m**2
            * p.temperature_relaxation_s
            / K_B_J
            * mobile_fraction
        )
        return float(p.lattice_temperature_k + heating)

    def _circuit_state(
        self, source_voltage_v: float, mobile_fraction: float, series_resistance_ohm: float
    ) -> tuple[float, float, float]:
        p = self.params
        conductance = (
            Q_E
            * p.mobility_m2_v_s
            * p.equilibrium_density_m3
            * p.area_m2
            / p.length_m
            * max(mobile_fraction, 0.0)
        )
        device_voltage = source_voltage_v / (1.0 + conductance * series_resistance_ohm)
        current = conductance * device_voltage
        return device_voltage, device_voltage / p.length_m, current

    def simulate_step(
        self,
        voltage_v: float,
        stop_time_s: float = 5e-9,
        *,
        initial_temperature_k: float | None = None,
        initial_mobile_fraction: float | None = None,
        points: int = 1800,
        series_resistance_ohm: float = 50.0,
    ) -> BrunettiTransient:
        p = self.params
        te0 = initial_temperature_k or p.lattice_temperature_k
        x0 = (
            initial_mobile_fraction
            if initial_mobile_fraction is not None
            else self.mobile_equilibrium_fraction(0.0, p.lattice_temperature_k)
        )

        def rhs(_time: float, state: np.ndarray) -> np.ndarray:
            te, mobile = state
            _, field, _ = self._circuit_state(voltage_v, mobile, series_resistance_ohm)
            xeq = self.mobile_equilibrium_fraction(field, max(te, 1.0))
            te_target = self.equilibrium_carrier_temperature(field, mobile)
            dte = (te_target - te) / p.temperature_relaxation_s
            dmobile = (xeq - mobile) / p.population_relaxation_s
            return np.array([dte, dmobile])

        time = np.linspace(0.0, stop_time_s, points)
        solution = solve_ivp(
            rhs,
            (0.0, stop_time_s),
            np.array([te0, x0]),
            t_eval=time,
            rtol=2e-7,
            atol=1e-10,
            method="BDF",
            max_step=min(stop_time_s / 200.0, p.population_relaxation_s / 30.0),
        )
        temperature = solution.y[0]
        mobile = np.clip(solution.y[1], 0.0, 1.0)
        device_voltage = np.empty_like(solution.t)
        field = np.empty_like(solution.t)
        current = np.empty_like(solution.t)
        for idx, fraction in enumerate(mobile):
            device_voltage[idx], field[idx], current[idx] = self._circuit_state(
                voltage_v, float(fraction), series_resistance_ohm
            )
        return BrunettiTransient(
            time_s=solution.t,
            voltage_v=device_voltage,
            field_v_m=field,
            carrier_temperature_k=temperature,
            mobile_fraction=mobile,
            current_a=current,
        )

    def simulate_triangle(
        self,
        peak_voltage_v: float = 3.0,
        half_period_s: float = 50e-9,
        *,
        series_resistance_ohm: float = 50.0,
        points: int = 3000,
    ) -> tuple[np.ndarray, BrunettiTransient]:
        """Triangular source sweep including electronic feedback and Rs."""
        p = self.params
        total_time = 2.0 * half_period_s

        def source_voltage(time: float) -> float:
            if time <= half_period_s:
                return peak_voltage_v * time / half_period_s
            return peak_voltage_v * (2.0 - time / half_period_s)

        x0 = self.mobile_equilibrium_fraction(0.0, p.lattice_temperature_k)

        def rhs(time: float, state: np.ndarray) -> np.ndarray:
            te, mobile = state
            _, field, _ = self._circuit_state(
                source_voltage(time), mobile, series_resistance_ohm
            )
            xeq = self.mobile_equilibrium_fraction(field, max(te, 1.0))
            te_target = self.equilibrium_carrier_temperature(field, mobile)
            return np.array(
                [
                    (te_target - te) / p.temperature_relaxation_s,
                    (xeq - mobile) / p.population_relaxation_s,
                ]
            )

        time = np.linspace(0.0, total_time, points)
        solution = solve_ivp(
            rhs,
            (0.0, total_time),
            np.array([p.lattice_temperature_k, x0]),
            t_eval=time,
            method="BDF",
            rtol=2e-6,
            atol=1e-9,
            max_step=total_time / 2500.0,
        )
        source = np.asarray([source_voltage(value) for value in solution.t])
        temperature = solution.y[0]
        mobile = np.clip(solution.y[1], 0.0, 1.0)
        device_voltage = np.empty_like(solution.t)
        field = np.empty_like(solution.t)
        current = np.empty_like(solution.t)
        for idx, fraction in enumerate(mobile):
            device_voltage[idx], field[idx], current[idx] = self._circuit_state(
                float(source[idx]), float(fraction), series_resistance_ohm
            )
        transient = BrunettiTransient(
            time_s=solution.t,
            voltage_v=device_voltage,
            field_v_m=field,
            carrier_temperature_k=temperature,
            mobile_fraction=mobile,
            current_a=current,
        )
        return source, transient
