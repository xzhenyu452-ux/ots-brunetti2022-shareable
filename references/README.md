# Reference papers

## Ahn et al. 2013

H.-W. Ahn, D. S. Jeong, B.-k. Cheong, S.-d. Kim, S.-Y. Shin,
H. Lim, D. Kim, and S. Lee, "A Study on the Scalability of a Selector
Device Using Threshold Switching in Pt/GeSe/Pt," *ECS Solid State Letters*
2, N31-N33 (2013).

- DOI: https://doi.org/10.1149/2.011309ssl
- Local file: `papers/Ahn_et_al_2013_Pt_GeSe_Pt_OTS_Scalability.pdf`
- The local publisher PDF is intentionally ignored by Git and is not
  redistributed in the public repository.

### Reported scaling observations

- The crossbar devices use Pt/GeSe/Pt stacks. For the area study, the GeSe
  thickness is 100 nm and the overlap area ranges from 2 x 2 to 50 x 50
  um2. The measured film composition is Ge:Se = 62:38 at.%.
- Subthreshold current is described by a Poole-Frenkel-like relation,
  `I = I0 exp(sqrt(alpha V))`, and OFF resistance scales approximately as
  inverse area.
- ON resistance scales approximately as inverse line width rather than inverse
  area. Control structures without GeSe show that the measured ON resistance
  is dominated by the Pt electrode resistance in this geometry.
- As area decreases, the reported threshold voltage, holding voltage, and
  holding-current density increase. The maximum-current-density projection is
  a lower-bound extrapolation because the pulse generator, rather than
  irreversible device damage, limits the measured current.
- At fixed 5 x 5 um2 area, threshold voltage decreases from 100 to 40 nm and
  then saturates or slightly rises at 20 nm. For thickness above 40 nm, the
  authors fit `V_th proportional to sqrt(t)` and interpret it with a constant
  critical total power, `P_th = V_th^2/R proportional to V_th^2/t`.
- The thin-film saturation is attributed to an approximately
  thickness-independent contact/interface voltage, such as a Schottky
  barrier. The authors therefore propose combining a thin switching film with
  electrode engineering.

### Mechanistic interpretation and limitations

- A useful compact decomposition is `V_th = V_contact + V_bulk(t)`. The paper
  motivates a contact-controlled floor at small thickness and a bulk term at
  larger thickness.
- The observed square-root thickness law is not unique proof of thermal
  runaway. It assumes resistance proportional to thickness and a constant
  *total* critical power. A constant critical power density would instead
  give `V_th proportional to t` under the same uniform-current assumptions.
- Only the thicker-film points support the square-root fit, while interface
  voltage, current localization, and nonuniform heating can produce similar
  apparent exponents over a limited range.
- Area scaling is not purely intrinsic in these structures: ON resistance is
  electrode-limited, the switching pulse contains capacitive overshoot, and
  the active conduction area need not equal the lithographic overlap area.
- The increase of threshold voltage at smaller area is compatible with a
  weakest-link or first-fire picture, in which larger devices have more
  chances to contain a low-barrier switching path. An ideal uniform
  critical-field model would instead predict nearly area-independent
  threshold voltage.

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

## Zhao et al. 2024

J. Zhao, Z. Zhao, Z. Song, and M. Zhu, "GeSe ovonic threshold switch: the
impact of functional layer thickness and device size," *Scientific Reports*
14, 6685 (2024).

- DOI: https://doi.org/10.1038/s41598-024-57029-7
- Local file: `papers/Zhao_et_al_2024_GeSe_OTS_Thickness_Device_Size.pdf`
- License stated in the article: CC BY 4.0.
- The local PDF is intentionally ignored by Git.

### Scaling observations

- For 44, 29, and 15 nm GeSe films on 200 nm TiN electrodes, threshold
  voltage decreases approximately linearly with thickness while the extracted
  threshold field remains near 105 V/um. Holding voltage changes much less.
- Leakage measured at one-half of each device's own threshold voltage remains
  around tens of nA without a monotonic thickness dependence. Because the
  sampling voltage scales with threshold voltage, this is approximately a
  comparison at fixed normalized field rather than at fixed terminal voltage.
- Reducing TiN electrode diameter from 200 to 60 nm has little systematic
  effect on threshold voltage, holding voltage, threshold field, or 7-10 ns
  switching speed. The 60 nm devices show noticeably wider threshold-voltage
  scatter.
- Absolute leakage decreases from 56.5 to 23.5 nA as diameter shrinks from
  200 to 60 nm. This is much weaker than ideal area scaling: area falls by
  about 11.1 times while current falls by only about 2.4 times, so leakage
  current density increases by about 4.6 times.

### Interpretation and limitations

- The thickness result supports a bulk critical-field picture,
  `V_th approximately E_th t + V_offset`, over the measured range. A nonzero
  contact/access-voltage offset is still compatible with the data.
- Area-independent threshold voltage is expected for a local field criterion;
  area should primarily affect total current and statistical variability.
- Sub-area scaling of leakage suggests that current is not simply uniform over
  the lithographic electrode area. Edge/perimeter conduction, current
  crowding, a fixed parasitic floor, or a smaller effective active area remain
  plausible explanations and are not separated by this paper.
- The study demonstrates correlations and scaling trends but does not solve a
  contact-aware Poisson/transport model or independently extract interface
  barrier parameters.
