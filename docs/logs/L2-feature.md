# L2 Log

Last updated: 2026-09-09 22:00

Use this file for L2-class changes only.


## 2026-09-29 - completed - Hatayama 2025 contact-aware model

- Added an independent nested Python package for the Schottky-interface interpretation of GeTe6 OTS devices.
- Kept paper-anchored values separate from calibration-only parameters.
- Generated Hf/W/Pt electrode and 100/50/25 nm thickness comparisons, CSV data, and JSON summaries.
- Added tests for electrode ordering, contact-independent PF transport, depletion-overlap suppression of 25 nm Pt, and current compliance.


## 2026-09-09 22:08 - completed - Create shareable Brunetti 2022 package

- Summary: Added formula and provenance documentation, standalone Python package metadata, reproduction script, tests, and regenerated dynamic OTS outputs.
- Level: L2
- Files changed: `MODEL.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `src/ots_brunetti2022`, `scripts/reproduce_brunetti2022.py`, `tests/test_brunetti2022.py`, `outputs/brunetti2022_dynamic`
- Docs updated: `MODEL.md`, `README.md`, `docs/PROJECT_INDEX.md`, `docs/change_log.md`
- Validation: not run
