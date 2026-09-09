"""Reproduce a parameterized 2.4 V step from Brunetti et al. (2022)."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ots_brunetti2022 import Brunetti2022Model, Brunetti2022Parameters


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "outputs" / "brunetti2022_dynamic"
    output.mkdir(parents=True, exist_ok=True)
    params = Brunetti2022Parameters()
    model = Brunetti2022Model(params)
    transient = model.simulate_step(2.4, stop_time_s=5e-9)
    source_triangle, triangle = model.simulate_triangle(
        peak_voltage_v=3.0,
        half_period_s=50e-9,
        series_resistance_ohm=50.0,
    )
    midpoint = len(source_triangle) // 2

    def steepest_voltage(section: slice) -> tuple[float, float]:
        voltage = source_triangle[section]
        current = triangle.current_a[section]
        slope = np.gradient(np.log10(np.maximum(current, 1e-30)), voltage)
        valid = np.flatnonzero(current > 1e-6)
        index = int(valid[np.argmax(np.abs(slope[valid]))])
        return float(voltage[index]), float(current[index])

    threshold_voltage, threshold_current = steepest_voltage(slice(0, midpoint))
    holding_voltage, holding_current = steepest_voltage(slice(midpoint, None))

    half_current = 0.5 * transient.current_a[-1]
    crossing = transient.time_s[transient.current_a >= half_current]
    delay_s = float(crossing[0]) if crossing.size else float("nan")
    summary = {
        "model": "Brunetti et al. 2022 reduced two-level dynamic model",
        "doi": "10.3389/fphy.2022.854393",
        "voltage_step_v": 2.4,
        "parameters": asdict(params),
        "final_carrier_temperature_k": float(transient.carrier_temperature_k[-1]),
        "final_mobile_fraction": float(transient.mobile_fraction[-1]),
        "final_current_a": float(transient.current_a[-1]),
        "half_current_delay_s": delay_s,
        "triangle_sweep": {
            "peak_source_voltage_v": 3.0,
            "half_period_s": 50e-9,
            "series_resistance_ohm": 50.0,
            "peak_current_a": float(triangle.current_a.max()),
            "threshold_voltage_v": threshold_voltage,
            "threshold_current_a": threshold_current,
            "holding_voltage_v": holding_voltage,
            "holding_current_a": holding_current,
        },
        "scope_note": (
            "Zero-dimensional reproduction of the paper's two-level dynamics; "
            "the published full model additionally resolves space and external circuit."
        ),
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.0), sharex=True, constrained_layout=True)
    time_ns = transient.time_s * 1e9
    axes[0].plot(time_ns, transient.current_a * 1e6, color="#1f5a94", lw=2.2)
    axes[0].set_ylabel("Current (µA)")
    axes[0].grid(True, alpha=0.25)
    axes[0].set_title("Brunetti 2022 reduced dynamic model — 2.4 V step")
    axes[1].plot(time_ns, transient.carrier_temperature_k, color="#c43b3b", lw=2.0, label="Te")
    axes[1].set_xlabel("Time (ns)")
    axes[1].set_ylabel("Carrier temperature Te (K)", color="#c43b3b")
    axes[1].tick_params(axis="y", labelcolor="#c43b3b")
    fraction_axis = axes[1].twinx()
    fraction_axis.plot(
        time_ns,
        transient.mobile_fraction,
        color="#2b8c5a",
        lw=2.0,
        label="mobile fraction",
    )
    fraction_axis.set_ylabel("Mobile fraction", color="#2b8c5a")
    fraction_axis.tick_params(axis="y", labelcolor="#2b8c5a")
    axes[1].grid(True, alpha=0.25)
    lines, labels = axes[1].get_legend_handles_labels()
    lines2, labels2 = fraction_axis.get_legend_handles_labels()
    axes[1].legend(lines + lines2, labels + labels2, frameon=False, loc="center right")
    fig.savefig(output / "step_response_2p4V.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 5.0), constrained_layout=True)
    ax.semilogy(
        source_triangle[:midpoint],
        np.maximum(triangle.current_a[:midpoint], 1e-12),
        color="#1f5a94",
        lw=2.0,
        label="up sweep",
    )
    ax.semilogy(
        source_triangle[midpoint:],
        np.maximum(triangle.current_a[midpoint:], 1e-12),
        color="#c43b3b",
        lw=2.0,
        label="down sweep",
    )
    ax.scatter(
        [threshold_voltage, holding_voltage],
        [threshold_current, holding_current],
        color=["#1f5a94", "#c43b3b"],
        edgecolor="white",
        zorder=4,
    )
    ax.annotate(f"Vth≈{threshold_voltage:.2f} V", (threshold_voltage, threshold_current), xytext=(-85, 18), textcoords="offset points")
    ax.annotate(f"Vhold≈{holding_voltage:.2f} V", (holding_voltage, holding_current), xytext=(12, 18), textcoords="offset points")
    ax.set(xlabel="Applied source voltage (V)", ylabel="Current (A)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)
    ax.set_title("Electronic-feedback threshold switching — Rs=50 Ω")
    fig.savefig(output / "triangle_iv_Rs50ohm.png", dpi=220)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
