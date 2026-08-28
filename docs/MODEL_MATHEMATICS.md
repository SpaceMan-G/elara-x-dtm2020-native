# DTM2020 Operational — Governing Mathematics

## Purpose

Operational F10.7/Kp-driven DTM2020 thermosphere model used for temperature, composition and neutral-density prediction.

The equations below explain the physical and mathematical structure of the model. They are intentionally separated from the accepted implementation source: documentation must not silently become a second, divergent implementation.

## Empirical state dependence

A thermospheric empirical model can be represented schematically as a mapping

```math
\mathcal{M}:
(t,\mathbf{r},\mathbf{s})
\longrightarrow
(T,\rho,\mathbf{n}),
```

where $`t`$ is epoch, $`\mathbf{r}`$ is position, $`\mathbf{s}`$ contains the required space-weather drivers, $`T`$ is temperature, $`\rho`$ is total mass density and $`\mathbf{n}`$ denotes constituent densities where provided.


## Constituent representation

For constituent $`i`$, a schematic DTM representation is

```math
n_i = A_i
\exp\!\left(G_i(\mathbf{x})\right)
f_i(z),
```

where $`A_i`$ is a constituent baseline coefficient, $`G_i`$ contains the fitted environmental variations, $`\mathbf{x}`$ is the environmental state, and $`f_i(z)`$ is the altitude/thermal structure.

## Total mass density

The constituent contributions form total neutral mass density:

```math
\rho = \sum_i m_i n_i.
```

The operational species set used by the accepted Elara X implementation is H, He, O, N, N2 and O2.

## Temperature structure

DTM2020 uses fitted exospheric and lower-boundary thermal parameters including $`T_\infty`$, $`T_{120}`$ and $`T'_{120}`$. These determine the altitude-dependent local temperature $`T(z)`$ and the constituent scale-height structure.

## Environmental variations

A schematic decomposition of a fitted quantity $`Q`$ is

```math
Q = Q_0
\left[
1
+ G_{\mathrm{solar}}
+ G_{\mathrm{geomag}}
+ G_{\mathrm{season}}
+ G_{\mathrm{latitude}}
+ G_{\mathrm{local\ time}}
+ G_{\mathrm{longitude}}
\right].
```

The official coefficient file defines the amplitudes of the operational terms. This schematic expression documents the structure; it does not replace the accepted numerical kernel.

## Daily aggregation

For $`N_d`$ valid samples on UTC day $`d`$,

```math
\bar{\rho}_d =
\frac{1}{N_d}
\sum_{k=1}^{N_d}\rho_k.
```

Missing trajectory samples are not invented. Partial-source days must be identified as partial rather than promoted to complete-day means.


## Unit discipline

Density is normally exposed by the Elara X public interfaces in SI units of kg m$`^{-3}`$ unless the interface explicitly documents a model-native unit. Angles, altitude and space-weather indices must follow the repository interface contract. Do not infer units from a variable name alone.

## Scientific reference

Official SWAMI DTM2020 documentation and Xu, Du & Cao (2025), Singularity-Free Formulations for Drag Temperature Model and Its Analytical Gradient, DOI 10.2514/1.J064156.
