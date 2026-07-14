--------------------
GENERAL INFORMATION
--------------------
Title of Dataset: PALEOS composite equation-of-state tables
Description: Phase-aware, thermally responsive composite equations of state
  for iron, magnesium silicate, and water, from the PALEOS toolkit
  (Planetary Assemblage Layers: Equations Of State). Each material is a
  single self-consistent composite over all of its phases, with continuous
  phase boundaries and one reference-state calibration per material.
Principal Investigator: Mara Attia
Companion paper: Attia et al. (2026), in revision
Code: https://github.com/maraattia/PALEOS
Data (concept DOI, resolves to latest version):
  EoS lookup tables (Fe, MgSiO3, H2O): https://doi.org/10.5281/zenodo.19000315
  PROTEUS-specific MgSiO3 table:       https://doi.org/10.5281/zenodo.18924170

-------------
FILE OVERVIEW
-------------
The catalog entries here (attia2026_{Fe,MgSiO3,H2O}_eos.toml) hold metadata
for the composite EoS. The tabulated grids themselves are released on Zenodo
(link above) rather than committed here, following the convention used by the
canoamoros2026 entry. The Fe and MgSiO3 tables are additionally available at
600 points per decade for tighter derivative accuracy.

 File                                    Grid            Domain
 ---------------------------------------------------------------------------
 paleos_iron_eos_table_pt.dat            1351 x 380      1 bar-100 TPa, 300-1e5 K
 paleos_mgsio3_eos_table_pt.dat          1351 x 380*     1 bar-100 TPa, 300-1e5 K
 paleos_water_eos_table_pt.dat           2251 x 451      0.1 Pa-100 TPa, 100-1e5 K
 ---------------------------------------------------------------------------
 * nonrectangular: nodes in the low-P, high-T vapor/supercritical regime,
   where the RTpress liquid does not converge, are omitted (~65% valid).

------------------------
DATA-SPECIFIC INFORMATION
------------------------
Each .dat file is whitespace-delimited with a commented (#) header and ten
columns:
  P         Pa           Pressure (log-uniform)
  T         K            Temperature (log-uniform)
  rho       kg/m^3       Density
  u         J/kg         Specific internal energy
  s         J/(kg K)     Specific entropy
  cp        J/(kg K)     Isobaric heat capacity
  cv        J/(kg K)     Isochoric heat capacity
  alpha     1/K          Thermal expansion coefficient
  nabla_ad  ---          Adiabatic gradient
  phase     ---          Stable phase label at (P, T)

Interpolate bilinearly in (log10 P, log10 T). For MgSiO3, reconstruct the
full rectangle with NaN fill before building an interpolator.
