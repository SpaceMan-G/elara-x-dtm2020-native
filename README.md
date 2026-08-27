# Elara X DTM2020 Native — licence-safe public companion

This repository is the licence-safe public companion to the private Elara X
DTM2020 Operational integration.

## What is public here

The repository contains independently developed public-specification components:

- external-resource boundary and path policy;
- public DTM2020 state/input primitives;
- F10.7/Kp operational vector semantics and generic mathematical basis helpers;
- unit tests for those public-safe components;
- scientific/provenance/validation documentation.

## What is deliberately not included

This repository does **not** contain or redistribute:

- CNES DTM source code;
- SWAMI DTM Fortran source;
- the `DTM_2020_F107_Kp` / `DTM_2020_F107_Kp.dat` coefficient resource;
- coefficient values or supporting DTM data;
- the private Elara X operational numerical core;
- the private Elara X application, UI, AMVS implementation, CFD/DSMC code, or
  manuscript tooling.

The official SWAMI/CNES resource must be obtained and used only under the
applicable upstream licence. This repository does not grant rights to any
third-party DTM software or data.

## Scientific status

The complete **private** Elara X operational implementation associated with
this public companion has passed:

- 64 native real-resource cases;
- 64 official SWAMI-oracle cases;
- 576 field comparisons;
- zero equivalence failures;
- final first-class Elara X integration for AMVS, Combined Model Analysis and
  Combined Atmospheric Heatmap.

That acceptance applies to the private operational implementation. It must not
be read as a claim that the public-safe skeleton in this repository contains the
restricted/complete DTM numerical kernel.

## Operational drivers

The DTM2020 operational model uses:

- instantaneous F10.7 evaluated at t - 24 h;
- the prior/trailing 81-day mean F10.7;
- Kp delayed by 3 h;
- mean Kp over the preceding 24 h.

DTM2020 predicts thermospheric temperature, total mass density and composition.

## External resource

See `resources/README.md`.

## Licensing

See `LICENSING.md`. The upstream SWAMI/CNES licensing boundary is separate
from the repository-authored public-specification material.

## Validation and provenance

See `validation/ACCEPTANCE_SUMMARY.json`, `PROVENANCE.json` and the `docs/`
directory.
