# Worked Workflow

This is a process-level worked example showing how an operational DTM2020 calculation should be organised without inventing unavailable driver data.

## Example request

Evaluate DTM2020 at a spacecraft position near 300 km altitude at a known UTC epoch.

## Step 1 — establish the point

Provide:

- UTC epoch;
- altitude;
- geodetic/geocentric latitude convention required by the interface;
- longitude;
- local solar time if the selected interface requires it explicitly.

## Step 2 — establish operational drivers

Obtain the correct operational F10.7 and Kp quantities for that epoch.

Do not substitute a single daily Ap/Kp value into every operational history slot. DTM2020 distinguishes the delayed/current geomagnetic quantity from its recent-history quantity.

## Step 3 — load the official coefficients

Use:

`data/DTM_2020_F107_Kp.dat`

The coefficient resource is model data, not a set of tunable Elara X parameters.

## Step 4 — evaluate thermal parameters

The model evaluates fitted variations controlling:

- exospheric temperature;
- the 120 km reference temperature;
- the reference temperature-gradient parameter.

## Step 5 — evaluate constituent profiles

The thermal structure and constituent coefficient families are used to evaluate H, He, O, N, N2 and O2.

## Step 6 — form total density

The constituent mass contributions are summed to form total mass density.

## Step 7 — report with provenance

A reproducible result should record:

- epoch and position;
- input driver values;
- coefficient-file identity/hash;
- implementation commit;
- output units;
- total density and temperatures;
- any external space-weather source identity.

## Step 8 — time-series aggregation

For an orbit time series, repeat the point evaluation at each authoritative spacecraft epoch/position. Daily means are then formed from the valid pointwise results; the DTM equations themselves are not replaced by a separate daily model.

The accepted Elara X annual test followed this pointwise-then-aggregate pattern for more than one million Swarm-C epochs.
