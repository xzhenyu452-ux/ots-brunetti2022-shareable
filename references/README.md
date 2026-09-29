# Reference papers

## Clima et al. 2023

S. Clima, T. Ravsher, D. Garbin, R. Degraeve, A. Fantini, R. Delhougne,
G. S. Kar, and G. Pourtois, "Ovonic Threshold Switch Chalcogenides:
Connecting the First-Principles Electronic Structure to Selector Device
Parameters," *ACS Applied Electronic Materials* 5, 461-469 (2023).

- DOI: https://doi.org/10.1021/acsaelm.2c01458
- Local file: `papers/Clima_et_al_2023_OTS_Electronic_Structure_Device_Parameters.pdf`
- The local publisher PDF is intentionally ignored by Git and is not redistributed in the public repository.

### What the paper establishes

The authors compare nine Si-Ge-As-Te/Se OTS compositions. For each material,
they combine electrical measurements with ten independent 300-atom amorphous
DFT models. The main result is a correlation map rather than a closed-form
transport model:

- larger mobility gaps correlate with higher first-fire, threshold, holding
  voltages, and holding current;
- pristine leakage and experimentally extracted defect concentration form a
  conductive group that anticorrelates with the insulating group;
- threshold switching is interpreted as field-assisted energy alignment,
  tunneling, overlap, and spatial delocalization of localized tail/gap states;
- the ON state is maintained by occupied higher-energy traps, while turn-off
  occurs when those states depopulate and relax back to localized
  configurations;
- tetrahedral local environments correlate with insulating behavior, whereas
  over-coordinated environments correlate with conductive behavior.

### Important limitations

- The relationships are correlations across nine compositions, not proof of a
  unique microscopic switching mechanism.
- The trap-gap-to-threshold-voltage correlation is weak in the reported set;
  mobility gap is the stronger predictor.
- ON current was limited by an integrated series resistor of about 10 kOhm, so
  the study focuses on holding current rather than intrinsic high-field ON
  conductance.
- The DFT cells are about 2 nm while the experimental films are 20 nm, and the
  authors explicitly acknowledge model-size and local-variation uncertainty.
