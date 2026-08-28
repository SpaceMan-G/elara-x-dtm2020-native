# Inputs, Outputs and Computation Process

## Model inputs

Operational DTM2020 requires the physical state and environmental drivers needed to evaluate one thermospheric point:

- epoch/day of year;
- altitude;
- latitude;
- longitude;
- local solar time;
- F10.7 solar flux;
- mean/centred F10.7 quantity required by the operational contract;
- delayed/recent-history Kp quantities.

The official operational model is applicable above the lower thermospheric boundary used by DTM2020; the accepted Elara X operational contract treats the DTM domain as above approximately 120 km.

## Space-weather semantics

The accepted Elara X operational mapping preserves the official operational distinction between:

- instantaneous/delayed F10.7;
- 81-day mean F10.7;
- Kp delayed by the operational interval;
- the recent Kp-history quantity used by DTM2020.

These values must not be replaced by arbitrary daily replication.

## Computational sequence

A point evaluation follows this conceptual sequence:

1. Validate epoch, position and domain.
2. Resolve or accept the operational environmental drivers.
3. Load the official coefficient resource.
4. Evaluate fitted periodic/environmental variation functions.
5. Determine exospheric and reference-boundary thermal parameters.
6. Construct the altitude-dependent temperature field.
7. Evaluate constituent number/mass densities for H, He, O, N, N2 and O2.
8. Sum constituent contributions to total mass density.
9. Return local temperature, exospheric temperature, total density and available constituent fields.

## Outputs

The physical model provides:

- total neutral mass density;
- local temperature;
- exospheric temperature;
- mean molecular mass;
- constituent densities for H, He, O, N, N2 and O2.

Public Python wrappers may normalise density to SI kg/m³ while retaining the physical identity of each model output.

## Daily and annual products

A daily mean used by Elara X is an arithmetic mean of all valid high-resolution DTM samples for that UTC day:

\[
\bar{\rho}_{d} = \frac{1}{N_d}\sum_{k=1}^{N_d}\rho_k.
\]

No missing source samples are invented.

For the accepted Swarm-C 2022 annual product:

- 365 calendar days contained source observations;
- 344 were complete 30-second UTC days;
- 21 contained source gaps and were explicitly labelled as partial-day available-sample means;
- no missing samples were interpolated.
