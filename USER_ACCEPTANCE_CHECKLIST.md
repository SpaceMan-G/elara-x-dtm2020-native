# Manual Elara X DTM2020 user-acceptance gate

Complete this before making the repository public.

Use a **short historical interval that already has known-good TU Delft/reference
and managed GFZ coverage**. Do not acquire or invent a new science interval just
for this UI acceptance.

## 1. Catalogue / registry

- [ ] DTM2020 Operational is visible.
- [ ] It is selectable.
- [ ] The UI does not claim the SWAMI coefficient file is bundled.

## 2. AMVS

- [ ] Run DTM2020 Operational over the short known-good interval.
- [ ] Execution completes without adapter/resource errors.
- [ ] Density output is finite and physically populated.
- [ ] Result/provenance storage completes.
- [ ] DTM2020 appears alongside the other accepted AMVS models.

## 3. Combined Model Analysis

- [ ] Run the same short interval.
- [ ] DTM2020 executes rather than merely appearing in the selector.
- [ ] A `DTM2020_Density_kg_m3` result column is present.
- [ ] DTM2020 appears in the comparison plot.
- [ ] DTM2020 appears in the model metrics/ranking.
- [ ] Saved combined CSV retains DTM2020 columns.

## 4. Combined Atmospheric Heatmap

Test either fresh calculation plus cached reuse, or manual CSV load plus cached
reuse.

- [ ] DTM2020 density is merged into the Heatmap dataframe.
- [ ] The four density panels include Truth/JB2006/JB2008/DTM2020.
- [ ] DTM2020/Truth ratio is displayed.
- [ ] Managed GFZ resolution remains automatic.
- [ ] Saving/exporting the DTM-aware Heatmap works.
- [ ] Reopening via cached-result reuse still requires DTM2020.

## 5. External-resource boundary

- [ ] Normal authorised external coefficient configuration works.
- [ ] No coefficient/resource file appears inside the Elara X project.
- [ ] No coefficient/resource file appears inside this repository staging tree.
- [ ] A deliberately missing authorisation/path produces a controlled error
      rather than a crash or silent fallback. Restore the normal environment
      immediately after this negative test.

## Acceptance

Only after all applicable boxes pass should the public GitHub publication gate
be opened.
