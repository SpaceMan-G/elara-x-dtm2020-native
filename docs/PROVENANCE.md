# Provenance

## Official model authority

DTM2020 is a CNES thermosphere model developed in the SWAMI programme.

Official SWAMI MCM repository:

`https://github.com/swami-h2020-eu/mcm`

Official DTM2020 documentation:

`https://swami-h2020-eu.github.io/mcm/dtm2020.html`

The accepted Elara X implementation baseline used SWAMI MCM commit:

`a488a7c9d030bfbe86e88ab3d28a7ec5589b92e0`

## Official operational coefficient resource

Public repository path:

`data/DTM_2020_F107_Kp.dat`

The publication controller copies this file from the authorised local SWAMI MCM provenance root and records its SHA-256 in `PUBLICATION_MANIFEST.json`.

## Official licence

The repository-root `LICENSE` is copied verbatim from the official local SWAMI MCM provenance root used for publication.

Its SHA-256 is recorded in `PUBLICATION_MANIFEST.json`.

## Implementation provenance

The public Python implementation is an independently structured Elara X implementation. It was developed from the scientific publications and checked against official operational behaviour.

The public repository deliberately excludes:

- the original SWAMI/CNES Fortran source;
- private Elara X DTM parser/bridge/runtime internals;
- private resource authorisation data;
- private model-validation source datasets.

## Scientific references

### SWAMI / DTM2020

SWAMI project documentation and DTM2020 documentation, CNES/SWAMI.

### Analytical DTM formulation

Xu, Du & Cao (2025), *Singularity-Free Formulations for Drag Temperature Model and Its Analytical Gradient*, DOI `10.2514/1.J064156`.

## Validation provenance

The private Elara X acceptance lineage includes locked native/official equivalence, real reference-position evaluation, daily aggregation, annual Swarm-C operation, Combined Model Analysis and Heatmap acceptance.

Only publication-safe summaries are included here.
