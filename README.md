# Elara X — DTM2020 Native

A licence-aware Python implementation and integration-oriented reference for the **operational DTM2020 thermosphere model**.

This repository is the public companion to the private, first-class DTM2020 implementation used by Elara X. It is intended to make the model interface, governing mathematics, input/output semantics, provenance, validation approach, and reproducibility contract understandable without redistributing the original SWAMI Fortran source.

## Important licence notice

DTM2020 is the property of the **Centre National d'Études Spatiales (CNES)**. The official DTM/SWAMI licence supplied with the model is included as [`LICENSE`](LICENSE). Read that licence before using this repository.

The official operational coefficient file is included at:

`data/DTM_2020_F107_Kp.dat`

It is distributed **together with the applicable DTM licence and provenance information**. No broader rights are asserted or granted by this repository.

The maintainer has retained written clarification from the DTM/CNES contact concerning public availability of an independently structured implementation and distribution of the model coefficients together with the licence. The original correspondence itself is retained privately; the operative provenance summary is recorded in [`docs/AUTHORIZATION_AND_LICENSING.md`](docs/AUTHORIZATION_AND_LICENSING.md).

## What is included

- a public Python-facing DTM2020 implementation layer;
- an external-resource interface;
- the official operational DTM2020 coefficient file;
- the applicable DTM/SWAMI licence;
- governing-mathematics and physical-process documentation;
- input/output and computation-flow documentation;
- validation and reproducibility guidance;
- provenance and publication notices;
- public tests.

## What is deliberately not included

- the original SWAMI/CNES Fortran source files;
- private Elara X implementation internals;
- private resource-authorisation machinery;
- private scientific acceptance locks;
- TU Delft source datasets;
- CelesTrak/GFZ managed space-weather datasets;
- private Elara X application code.

## Model scope

DTM2020 is a semi-empirical thermosphere model. The operational variant uses **F10.7** solar radio flux and **Kp** geomagnetic activity, together with position, local solar time, season/day of year and altitude, to predict thermospheric temperature, total density and constituent composition.

The official SWAMI documentation describes DTM2020 as providing point-wise temperature, density and composition predictions for the thermosphere and identifies F10.7 and Kp as the operational model drivers.

## Documentation

Start with:

- [`docs/MODEL_MATHEMATICS.md`](docs/MODEL_MATHEMATICS.md)
- [`docs/INPUTS_OUTPUTS_AND_PROCESS.md`](docs/INPUTS_OUTPUTS_AND_PROCESS.md)
- [`docs/WORKED_WORKFLOW.md`](docs/WORKED_WORKFLOW.md)
- [`docs/VALIDATION_AND_REPRODUCIBILITY.md`](docs/VALIDATION_AND_REPRODUCIBILITY.md)
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
- [`docs/AUTHORIZATION_AND_LICENSING.md`](docs/AUTHORIZATION_AND_LICENSING.md)

## Scientific basis

The implementation and documentation are grounded in the published DTM literature, including the DTM2020/SWAMI documentation and the analytical formulation work of Xu, Du & Cao (2025), *Singularity-Free Formulations for Drag Temperature Model and Its Analytical Gradient*, DOI `10.2514/1.J064156`.

The public implementation preserves the operational DTM formulation basis. The singularity-free analytical reformulation described by Xu et al. is useful for analysis and gradients, but is not silently substituted for the accepted operational production basis.

## Validation status

The private Elara X acceptance programme established:

- native/official equivalence over a 64-case campaign;
- 576 native/oracle field comparisons with zero acceptance failures;
- successful reference-position operation through the AMVS pathway;
- complete-day and daily-average density production;
- an authoritative Swarm-C 2022 annual run over **1,043,020** epochs with zero DTM model failures;
- 365 calendar-day daily means, including 344 complete native 30-second days and 21 explicitly labelled partial-source days;
- Combined Model Analysis and Heatmap interoperability;
- managed CSV and PNG/PDF/SVG presentation;
- controlled resource-authorisation behaviour.

Private/reference datasets used for those acceptance activities are not redistributed here.

## Attribution

DTM2020 and its official coefficients are attributed to CNES and the SWAMI project. This repository is an independent Elara X implementation/integration repository; it is not an official CNES or SWAMI repository and does not imply CNES endorsement.

See [`NOTICE.md`](NOTICE.md) and [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

<!-- ELARA_X_SCIENTIFIC_DOCUMENTATION_START -->
## Scientific documentation

The Elara X repository-enhancement programme provides a consistent scientific guide for this accepted model implementation:

- [Documentation index](docs/README.md)
- [Governing mathematics](docs/MODEL_MATHEMATICS.md)
- [Physical model and process](docs/PHYSICAL_MODEL_AND_PROCESS.md)
- [Inputs, outputs and computation process](docs/INPUTS_OUTPUTS_AND_PROCESS.md)
- [Worked workflow](docs/WORKED_WORKFLOW.md)
- [Validation and reproducibility](docs/VALIDATION_AND_REPRODUCIBILITY.md)
- [Provenance and scientific references](docs/PROVENANCE.md)

Equations in these documents use GitHub-native MathJax syntax.

This enhancement changes documentation only. The accepted scientific source, model resources, licences and validation identity remain unchanged.
<!-- ELARA_X_SCIENTIFIC_DOCUMENTATION_END -->
