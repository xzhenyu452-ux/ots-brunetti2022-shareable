"""Compare OTS voltage-sweep curves for several activation energies."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ots_brunetti2022 import Brunetti2022Model, Brunetti2022Parameters


def extract_knee(source: np.ndarray, current: np.ndarray, section: slice) -> tuple[float, float]:
    voltage = source[section]
    current_part = current[section]
    slope = np.gradient(np.log10(np.maximum(current_part, 1e-12)), voltage)
    valid = np.flatnonzero(current_part > 1e-6)
    if valid.size == 0:
        return float("nan"), float("nan")
    idx = int(valid[np.argmax(np.abs(slope[valid]))])
    return float(voltage[idx]), float(current_part[idx])


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "outputs" / "brunetti2022_dynamic"
    output.mkdir(parents=True, exist_ok=True)

    # Here activation energy means the two-level separation EB-ET. All other
    # parameters, scan rate, and series resistance are held fixed.
    activation_energies_ev = (0.30, 0.35, 0.375)
    base = Brunetti2022Parameters()
    colors = ("#168aad", "#1f5a94", "#c43b3b")
    summary: dict[str, object] = {
        "definition": "activation_energy_ev = mobile_energy_ev - trap_energy_ev",
        "fixed_series_resistance_ohm": 50.0,
        "peak_source_voltage_v": 3.0,
        "half_period_s": 50e-9,
        "curves": [],
    }

    fig, ax = plt.subplots(figsize=(7.4, 5.2), constrained_layout=True)
    for energy_ev, color in zip(activation_energies_ev, colors):
        params = replace(base, mobile_energy_ev=energy_ev, trap_energy_ev=0.0)
        source, response = Brunetti2022Model(params).simulate_triangle(
            peak_voltage_v=3.0,
            half_period_s=50e-9,
            series_resistance_ohm=50.0,
            points=1800,
        )
        midpoint = len(source) // 2
        vth, ith = extract_knee(source, response.current_a, slice(0, midpoint))
        vhold, ihold = extract_knee(source, response.current_a, slice(midpoint, None))
        ax.semilogy(source[:midpoint], np.maximum(response.current_a[:midpoint], 1e-12), color=color, lw=2.0, label=f"Ea={energy_ev:.2f} eV")
        ax.semilogy(source[midpoint:], np.maximum(response.current_a[midpoint:], 1e-12), color=color, lw=1.6, ls="--", alpha=0.9)
        ax.scatter([vth, vhold], [ith, ihold], color=color, s=26, edgecolor="white", zorder=4)
        summary["curves"].append({"activation_energy_ev": energy_ev, "vth_v": vth, "vhold_v": vhold, "ith_a": ith, "ihold_a": ihold})

    ax.set_xlabel("Applied source voltage (V)")
    ax.set_ylabel("Current (A)")
    ax.set_title("Activation-energy dependence of electronic OTS switching (Rs=50 Ω)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, title="solid: up / dashed: down")
    fig.savefig(output / "activation_energy_comparison.png", dpi=220)
    plt.close(fig)
    (output / "activation_energy_comparison.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
