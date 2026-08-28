# DTM2020 Governing Mathematics and Physical Model

## 1. Purpose

The Drag Temperature Model (DTM) is a semi-empirical thermosphere model designed to predict neutral atmospheric temperature, mass density and constituent composition as functions of location, time/season, solar activity and geomagnetic activity.

The operational DTM2020 variant used here is driven by F10.7 and Kp.

## 2. Constituent representation

The production formulation represents the principal neutral species:

- H
- He
- O
- N
- N2
- O2

For constituent \(i\), the number-density structure can be written schematically as

\[
n_i = A_i \exp\!\left(G_i(L)\right) f_i(h),
\]

where:

- \(A_i\) is a constituent-specific baseline coefficient;
- \(G_i(L)\) collects the fitted environmental variations;
- \(L\) denotes the model's environmental/periodic driver basis;
- \(f_i(h)\) represents the altitude-dependent diffusive/thermal structure.

The exact fitted coefficients are supplied in the official operational coefficient file.

## 3. Total mass density

The total neutral mass density is assembled from the constituent number densities:

\[
\rho = N_A^\ast \sum_i m_i n_i,
\]

where \(m_i\) denotes constituent molecular/atomic mass and the conversion factor \(N_A^\ast\) represents the unit/conversion convention used by the DTM formulation.

The implementation preserves the accepted DTM constituent-to-total-density calculation semantics.

## 4. Temperature structure

The operational formulation uses the characteristic temperatures:

- \(T_\infty\): exospheric temperature;
- \(T_{120}\): temperature at the 120 km reference boundary;
- \(T'_{120}\): temperature-gradient parameter at the reference boundary.

These quantities determine the thermal structure used by the altitude-dependent constituent profiles and the local temperature \(T(z)\).

## 5. Environmental variation basis

The fitted variation functions account for combinations of:

- solar activity;
- geomagnetic activity;
- annual and semi-annual variation;
- latitude dependence;
- local solar time / diurnal and semidiurnal structure;
- longitude-dependent terms where present in the operational formulation.

The operational driver contract uses:

- F10.7 at the appropriate delayed epoch;
- an 81-day mean F10.7 quantity;
- Kp with the operational delayed/recent-history semantics.

## 6. Operational coefficient groups

The official operational coefficient resource is structured around coefficient groups corresponding to thermospheric temperature and constituent terms. The accepted Elara X parser identified the operational header semantics as:

`TT H HE O N2 O2 N T0 TP`

corresponding to:

- `TT` → exospheric-temperature coefficient family;
- `H`, `HE`, `O`, `N2`, `O2`, `N` → constituent coefficient families;
- `T0` → reference-boundary temperature family;
- `TP` → reference-boundary temperature-gradient family.

## 7. Original versus singularity-free formulation

Xu, Du & Cao (2025) derive singularity-free formulations and analytical gradients for DTM. Those formulations are valuable for analytical work and optimisation.

The Elara X production implementation does not silently replace the accepted operational formulation with a transformed approximation. The accepted production basis remains the operational DTM structure, while the published singularity-free work is treated as an analytical reference.

## 8. Units

The official DTM implementation historically expresses total and partial densities in g/cm³ internally/output-side, with model wrappers often converting to SI kg/m³.

This public repository documents both the model-level physical semantics and the Python interface semantics. Always follow the public interface docstrings/tests for the exact units expected by a particular function.
