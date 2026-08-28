# DTM2020 Operational — Provenance and Scientific References

## Repository role

This repository is a standalone public companion to the accepted Elara X atmospheric-model implementation. It is intended to make the model understandable and reproducible without exposing private application internals.

## Scientific model

- Model: **DTM2020 Operational**
- Family: **Drag Temperature Model**
- Scope: Operational F10.7/Kp-driven DTM2020 thermosphere model used for temperature, composition and neutral-density prediction.
- Primary scientific reference: Official SWAMI DTM2020 documentation and Xu, Du & Cao (2025), Singularity-Free Formulations for Drag Temperature Model and Its Analytical Gradient, DOI 10.2514/1.J064156.

## Source authority

The numerical authority is the accepted public scientific source already present in the repository. This enhancement does not translate, rewrite or optimise that source.

## Licence authority

The existing repository licence and notice files remain unchanged. Where an external coefficient/parameter file is required, its existing licence/provenance boundary remains unchanged.


## DTM2020 licensing boundary

The official DTM2020 coefficient resource remains subject to the licence distributed in the repository. The original SWAMI Fortran source and private Elara X implementation internals are not part of this documentation enhancement. The existing `docs/AUTHORIZATION_AND_LICENSING.md` remains the publication-specific licensing record.


## Documentation status

The `docs/` files added/updated by the Elara X repository-enhancement phase are explanatory publication material. They are checked for GitHub-native MathJax delimiters and are hash-bound in `DOCUMENTATION_ENHANCEMENT_MANIFEST.json`.

## Citation

Cite both the repository commit used for the calculation and the underlying scientific model reference above.
