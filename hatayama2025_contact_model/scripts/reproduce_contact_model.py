"""Generate baseline electrode and thickness comparisons."""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hatayama_contact import CONTACTS, HatayamaContactModel, ModelParameters  # noqa: E402


COLORS = {"Hf": "#2468d8", "W": "#20a65a", "Pt": "#e43d30"}


def _serializable(value: float | bool | None) -> float | bool | None:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    return value


def main() -> None:
    output_dir = ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    baseline = ModelParameters()
    results = {
        name: HatayamaContactModel(contact, baseline).sweep()
        for name, contact in CONTACTS.items()
    }

    fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.5))
    for name, result in results.items():
        color = COLORS[name]
        axes[0].semilogy(
            result.source_voltage_v,
            np.maximum(result.terminal_current_a, 1e-12),
            color=color,
            label=name,
        )
        axes[0].semilogy(
            result.source_voltage_v,
            np.maximum(result.pf_current_a, 1e-12),
            color=color,
            alpha=0.28,
            linestyle="--",
        )
        if result.onset_voltage_v is not None:
            axes[0].axvline(result.onset_voltage_v, color=color, alpha=0.25, linewidth=1)
        if result.threshold_voltage_v is not None:
            axes[0].scatter(
                [result.threshold_voltage_v],
                [np.interp(result.threshold_voltage_v, result.source_voltage_v, result.terminal_current_a)],
                color=color,
                edgecolor="black",
                zorder=5,
            )
        axes[1].semilogy(result.source_voltage_v, result.multiplication, color=color, label=name)
        axes[2].plot(
            result.source_voltage_v,
            result.physical_contact_drop_v,
            color=color,
            label=f"{name}: contact",
        )
        axes[2].plot(
            result.source_voltage_v,
            result.bulk_voltage_v,
            color=color,
            linestyle="--",
            label=f"{name}: bulk",
        )

    axes[0].set(title="Quasi-static terminal I-V", xlabel="Source voltage (V)", ylabel="Current (A)")
    axes[0].set_ylim(1e-8, 2e-3)
    axes[0].legend(title="solid: terminal\ndashed: PF baseline")
    axes[1].set(title="Impact-ionization multiplication", xlabel="Source voltage (V)", ylabel="M")
    axes[1].axhline(baseline.onset_multiplication, color="0.5", linestyle=":")
    axes[1].axhline(baseline.threshold_multiplication, color="0.2", linestyle="--")
    axes[1].legend()
    axes[2].set(title="Interpretive voltage partition", xlabel="Source voltage (V)", ylabel="Voltage (V)")
    axes[2].legend(fontsize=8, ncol=2)
    for axis in axes:
        axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "electrode_comparison.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4), sharey=True)
    thickness_summary: dict[str, dict[str, dict[str, float | bool | None]]] = {}
    for axis, thickness_nm in zip(axes, (100.0, 50.0, 25.0), strict=True):
        thickness_summary[str(int(thickness_nm))] = {}
        for name, contact in CONTACTS.items():
            model = HatayamaContactModel(contact, replace(baseline, thickness_nm=thickness_nm))
            result = model.sweep()
            axis.semilogy(
                result.source_voltage_v,
                np.maximum(result.terminal_current_a, 1e-12),
                color=COLORS[name],
                label=name,
            )
            thickness_summary[str(int(thickness_nm))][name] = {
                "switchable": result.switchable,
                "overlap_fraction": result.depletion_overlap_fraction,
                "effective_built_in_potential_v": result.effective_built_in_potential_v,
                "onset_voltage_v": result.onset_voltage_v,
                "threshold_voltage_v": result.threshold_voltage_v,
                "hold_voltage_v": result.hold_voltage_v,
            }
        axis.set_title(f"GeTe6 thickness = {thickness_nm:.0f} nm")
        axis.set_xlabel("Source voltage (V)")
        axis.grid(alpha=0.25)
        axis.legend()
    axes[0].set_ylabel("Terminal current (A)")
    axes[0].set_ylim(1e-8, 2e-3)
    fig.tight_layout()
    fig.savefig(output_dir / "thickness_comparison.png", dpi=180)
    plt.close(fig)

    with (output_dir / "electrode_sweeps.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "electrode",
                "source_voltage_v",
                "pf_current_a",
                "multiplied_current_a",
                "terminal_current_a",
                "multiplication",
                "physical_contact_drop_v",
                "bulk_voltage_v",
                "ionization_drive_voltage_v",
            ]
        )
        for name, result in results.items():
            for row in zip(
                result.source_voltage_v,
                result.pf_current_a,
                result.multiplied_current_a,
                result.terminal_current_a,
                result.multiplication,
                result.physical_contact_drop_v,
                result.bulk_voltage_v,
                result.ionization_drive_voltage_v,
                strict=True,
            ):
                writer.writerow([name, *row])

    summary = {
        "model_parameters": asdict(baseline),
        "contacts": {name: asdict(contact) for name, contact in CONTACTS.items()},
        "electrode_results_100nm": {
            name: {
                "onset_voltage_v": _serializable(result.onset_voltage_v),
                "threshold_voltage_v": _serializable(result.threshold_voltage_v),
                "hold_voltage_v": _serializable(result.hold_voltage_v),
                "effective_built_in_potential_v": result.effective_built_in_potential_v,
                "switchable": result.switchable,
            }
            for name, result in results.items()
        },
        "thickness_results": thickness_summary,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary["electrode_results_100nm"], indent=2))
    print(f"Wrote results to {output_dir}")


if __name__ == "__main__":
    main()
