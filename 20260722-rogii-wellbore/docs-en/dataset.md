# Dataset — ROGII Wellbore Geology Prediction (source + local measure)

> Updated: 2026-07-23 — local files under `dataset/` measured  
> Japanese SSOT: `docs-ja/dataset.md`  
> Machine summary: `exp/work/dataset-eda-20260723.json`

## Summary

Predict **TVT** on the eval zone (`TVT_input` NaN) with **RMSE**.

| Item | Measured |
|---|---|
| Train wells | **773** (hw + typewell + png each) |
| Local test wells | **3** (IDs overlap train; example only) |
| Train horizontal rows | ~5.09M |
| Eval rows (`TVT_input` NaN) | ~3.78M (~73%) |
| TVT range | 9245.19 – 12893.89 |
| sample_submission | 14151 rows / 3 wells |
| Hidden test | ~200 wells (not local) |

## Columns (measured)

Train horizontal CSV has **no `WELLNAME` column** (id from filename):

`MD, X, Y, Z, ANCC, ASTNU, ASTNL, EGFDU, EGFDL, BUDA, TVT, GR, TVT_input`

Local test horizontal: `MD, X, Y, Z, GR, TVT_input` only (no `TVT`, no formation tops).

Typewell: `TVT, GR, Geology`

## Carry-forward proxy (train labels)

Per-well RMSE of constant last-known `TVT_input` on eval zone (n=773):

- mean **12.81**, median **10.67**, p90 **22.97**, max **70.64**
- Hard wells include `86454a6f` (also cited in Discussion)

## License

Competition use only — do not commit `dataset/` to Git.
