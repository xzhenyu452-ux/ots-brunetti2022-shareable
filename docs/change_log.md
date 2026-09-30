# Change Log

Last updated: 2026-09-30

Append new entries at the top or bottom, but keep the format consistent.


## 2026-09-30 - completed - Add GeSe electrode-interface reference

- Summary: Archived Seo et al. 2017 locally and documented its Mo/Al/W/TiN threshold-voltage comparison, interface-trap extraction, hopping interpretation, and modeling limitations.
- Level: L3
- Files changed: `references/README.md`, `docs/change_log.md`, `docs/logs/L3-maintenance.md`
- Validation: archive SHA-256 matches the supplied four-page PDF; all pages and figures were visually inspected.


## 2026-09-30 - completed - Add Pt/GeSe/Pt OTS scalability reference

- Summary: Archived Ahn et al. 2013 locally and documented its area and thickness scaling results, contact-voltage interpretation, and limits of the critical-power argument.
- Level: L3
- Files changed: `references/README.md`, `docs/change_log.md`, `docs/logs/L3-maintenance.md`
- Validation: archive SHA-256 matches the supplied PDF; bibliographic data, equations, device dimensions, and plotted trends checked against the article.


## 2026-09-30 - completed - Add GeSe thickness and area scaling reference

- Summary: Archived Zhao et al. 2024 locally and added a reference note covering thickness, electrode-size, leakage, threshold-field, and variability trends.
- Level: L3
- Files changed: `references/README.md`, `docs/change_log.md`, `docs/logs/L3-maintenance.md`
- Validation: publisher PDF hash matches the supplied source; key figures 2-8 visually inspected.


## 2026-09-29 - completed - Make contact and bulk transport self-consistent

- Summary: Replaced the threshold-only empirical contact shift with common forward/reverse Schottky equations and current-continuous voltage partitioning across both contacts and the PF bulk.
- Level: L2
- Files changed: `hatayama2025_contact_model/src`, reproduction outputs, tests, and model documentation.
- Validation: outputs regenerated; 6 contact-model tests and 2 root tests passed.


## 2026-09-29 - completed - Add Hatayama 2025 contact-aware OTS reproduction

- Summary: Added a standalone quasi-static GeTe6/Hf-W-Pt model combining contact band bending, Poole-Frenkel transport, lucky-drift impact ionization, engineering ON-state compliance, and depletion-overlap thickness effects.
- Level: L2
- Files changed: `hatayama2025_contact_model`, `README.md`, `docs/PROJECT_INDEX.md`, `docs/change_log.md`, `docs/logs/L2-feature.md`
- Docs updated: model assumptions, parameter provenance, limitations, run instructions, and project index.
- Validation: standalone reproduction generated successfully; 4 standalone tests and 2 root tests passed.


## 2026-09-09 22:08 - completed - Create shareable Brunetti 2022 package

- Summary: Added formula and provenance documentation, standalone Python package metadata, reproduction script, tests, and regenerated dynamic OTS outputs.
- Level: L2
- Files changed: `MODEL.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `src/ots_brunetti2022`, `scripts/reproduce_brunetti2022.py`, `tests/test_brunetti2022.py`, `outputs/brunetti2022_dynamic`
- Docs updated: `MODEL.md`, `README.md`, `docs/PROJECT_INDEX.md`, `docs/change_log.md`
- Validation: not run
