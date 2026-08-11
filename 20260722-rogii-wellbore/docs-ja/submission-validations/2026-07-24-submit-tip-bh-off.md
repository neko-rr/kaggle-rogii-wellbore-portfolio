# Submission Validation — SUB-2 tip BH-off

> date: 2026-07-24  
> profile: csv  
> status: **PASS**

## Artifact

- kernel: `kazeneko77/tip-bh-strength-off` Ver1
- file: `submission.csv`
- rows: 14151 · `id,tvt`
- vs smoke tip: n_changed **4301** · mean abs diff ≈0.61

## Hypothesis

`_BH_STRENGTH=0`（PF seed-branch midpoint hedge OFF）が Public に効くか。

## L2

- [x] Notebook 紐づけ `-k/-v/-f`
- [x] Private · GPU COMPLETE
- [x] tip 同一再提出ではない（hedge 消込）
