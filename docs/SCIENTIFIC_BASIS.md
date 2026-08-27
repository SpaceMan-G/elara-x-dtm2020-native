# Scientific basis

DTM2020 is a semi-empirical thermospheric model providing point-wise
temperature, total density and constituent-density estimates as functions of
location, season, solar activity and geomagnetic activity.

The public Elara X interface contract describes the operational input semantics
without embedding fitted DTM coefficients:

- day of year;
- altitude;
- geodetic/geographic latitude and longitude;
- local solar time;
- F10.7 at t - 24 h;
- trailing 81-day F10.7 mean;
- Kp delayed by 3 h;
- prior 24-hour mean Kp.

The public-specification modules include generic angle, harmonic and associated
Legendre primitives and resource-boundary handling. They intentionally stop
short of embedding the fitted DTM parameterisation.

Primary controlled mathematical authority in the Elara X programme:
Xu, Du & Cao (2025), “Singularity-Free Formulations for Drag Temperature Model
and Its Analytical Gradient”, DOI 10.2514/1.J064156.

The production private implementation retains the original-coordinate model
basis; the transformed singularity-free formulation is not silently substituted
for production DTM2020.
