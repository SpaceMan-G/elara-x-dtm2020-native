# Validation and Reproducibility

## Validation philosophy

The public implementation was accepted only after separating three questions:

1. Does the native implementation reproduce the official operational DTM behaviour?
2. Does it work through real Elara X reference-position/time-series workflows?
3. Can derived daily/annual products be generated without altering the pointwise model semantics?

## Native / official equivalence

The controlled private acceptance programme established a 64-case campaign with:

- 64 native operational evaluations;
- an official SWAMI oracle comparison;
- 576 compared output fields;
- zero acceptance failures at the locked tolerances.

The official oracle campaign is not redistributed in this repository, but the acceptance result is recorded as provenance.

## Reference-position acceptance

A Swarm-C TU Delft reference-position run evaluated 721 points over a six-hour interval at native 30-second cadence:

- adapter failures: 0;
- all DTM densities finite and positive;
- direct first-point/native-adapter agreement: accepted.

## Complete-day acceptance

Two consecutive complete UTC days were evaluated:

- 5,760 DTM2020 points;
- 2,880 samples per day;
- zero adapter failures;
- daily arithmetic means independently reproduced.

## Annual acceptance

An authoritative private TU Delft Swarm-C 2022 trajectory/reference population was used for the accepted annual run:

- 1,043,020 epochs;
- zero DTM model failures;
- 365 calendar-day means;
- 344 complete native 30-second days;
- 21 explicitly marked partial-source days;
- zero completely missing calendar days;
- no missing-sample interpolation.

The private TU Delft source data are not redistributed here.

## Reproducibility checklist

For a reproducible run record:

- repository Git commit;
- `data/DTM_2020_F107_Kp.dat` SHA-256;
- `LICENSE` SHA-256;
- exact epoch/position data source;
- F10.7/Kp source and mapping semantics;
- input units;
- output units;
- Python/environment versions;
- result CSV/figure hashes where relevant.

## Public tests

Run the repository's public tests using the Python version/environment described by the repository metadata. The public tests verify interface/contract behaviour without redistributing private Elara X science assets.
