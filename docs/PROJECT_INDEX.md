# PROJECT_INDEX

Last updated: 2026-09-29

## Quick Links

- `README.md`
- `AGENTS.md`
- `docs/change_log.md`
- `docs/logs/`

## Managed Tree

<!-- project-tree:start -->
```text
ots-brunetti2022-shareable/
|- .pytest_cache/
|- docs/
|  |- logs/
|  |  |- L1-architecture.md
|  |  |- L2-feature.md
|  |  |- L3-maintenance.md
|  |- change_log.md
|  |- PROJECT_INDEX.md
|- outputs/
|- hatayama2025_contact_model/
|  |- outputs/
|  |- scripts/
|  |- src/hatayama_contact/
|  |- tests/
|  |- MODEL.md
|  |- README.md
|  |- pyproject.toml
|  |- requirements.txt
|- scripts/
|- src/
|- tests/
|- AGENTS.md
|- CLAUDE.md
|- MODEL.md
|- pyproject.toml
|- README.md
|- requirements.txt
```
<!-- project-tree:end -->

## Key Entrypoints

- `scripts/reproduce_brunetti2022.py`: Brunetti dynamic reproduction.
- `hatayama2025_contact_model/scripts/reproduce_contact_model.py`: Hatayama contact-aware quasi-static reproduction.

## Ownership Notes

- `src/`, `scripts/`, `tests/`, and `outputs/` at the repository root belong to the Brunetti reproduction.
- `hatayama2025_contact_model/` is a standalone nested package with its own source, tests, documentation, and generated outputs.
- `references/papers/` contains local-only publisher PDFs and is ignored by Git.
