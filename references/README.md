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

## Hatayama et al. 2025

S. Hatayama, K. Hamano, Y. Shuang, M. Kim, P. Fons, and Y. Saito,
"Unveiling the Significant Role of Schottky Interfaces for Threshold Voltage
in Ovonic Threshold Switching," *ACS Applied Electronic Materials* 7,
2650-2659 (2025).

- DOI: https://doi.org/10.1021/acsaelm.5c00292
- Local file: `papers/Hatayama_et_al_2025_Schottky_Interface_Threshold_Voltage_OTS.pdf`
- License stated in the article: CC BY-NC-ND 4.0.
- The local publisher PDF is intentionally ignored by Git and is not redistributed in the public repository.

### Physical explanation

The paper isolates the contact effect by pairing amorphous GeTe6 with Hf, W,
and Pt electrodes while checking that no significant interfacial reaction or
compound is formed. Angle-resolved HAXPES directly measures depth-dependent
band bending and identifies an n-type Schottky interface. Increasing the metal
work function reduces both the measured built-in potential and the OTS
threshold and hold voltages.

The proposed causal chain is:

`metal work function -> built-in potential and depletion width -> band
flattening under bias -> onset of impact ionization -> threshold voltage`.

Deep-subthreshold conduction remains a bulk Poole-Frenkel process, and the
extracted trap depth is nearly independent of electrode species. The contact
therefore mainly shifts the voltage at which the device reaches the
impact-ionization regime rather than changing the intrinsic bulk trap depth.

### Equations used in the model

The measured band-bending profile is fitted with the depletion approximation:

`V_in = q N_d W_d^2 / (2 epsilon_s) + const`,

with `N_d = 1e18 cm^-3` and `epsilon_s = 2.92e-12 F/cm` fixed in the paper.

The deep-subthreshold current is fitted by a Poole-Frenkel expression:

`I_PF = A exp[-(q Phi - q V Delta_z/(2 u_a))/(k_B T)]`,

so that the activation energy is

`E_A = q Phi - q V Delta_z/(2 u_a)`.

The impact-ionization coefficient and multiplication factor are written as

`alpha = B exp[-E_i/(q lambda E)]`,

`M = I/I_PF = exp(alpha u_a)`,

where `E = V/u_a`. The paper defines the onset voltage `V_on` where `M` first
exceeds unity and shows that `V_on`, unlike the trap depth `q Phi` and
ionization energy `E_i`, depends strongly on electrode work function.

### Thickness and scope

- At 100 nm, the two 20-30 nm depletion regions do not overlap, and the
  contact built-in potential is the main electrode-dependent contribution to
  threshold voltage.
- At 50 and 25 nm, depletion-region overlap modifies the apparent barrier and
  the threshold trend; a 25 nm GeTe6/Pt device loses OTS behavior because the
  barrier becomes too small to suppress transport before impact ionization.
- The paper estimates a 0.68-2.8 V threshold-tuning range for 100 nm GeTe6 by
  changing the metal, and about 1.5-2.6 V for practical amorphous-carbon/TiN
  work-function ranges.
- This is a quasi-static, contact-aware interpretation, not a complete
  time-dependent transport solver. It combines measured band bending with
  phenomenological Poole-Frenkel and lucky-drift impact-ionization equations.
- GeTe6 is used as a chemically clean model system and is not presented as a
  back-end-compatible production OTS material.
