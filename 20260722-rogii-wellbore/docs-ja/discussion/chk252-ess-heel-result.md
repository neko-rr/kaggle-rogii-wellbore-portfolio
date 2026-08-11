# CHK-252 — ESS-gated heel reseeding（NO-GO）

> date: 2026-07-28 · tip-cv GPU `tip-cv-gpu-ess-heel-h20`

## 結果

| 面 | 値 |
|---|---|
| mid-bank soft Δ | **+0.225**（偽陽性候補） |
| tip-cv hard20 | **29.921** |
| vs 凍結 T0.15 (29.899) | **−0.022** |
| acceptance ≤29.599 | **FAIL** |

## 判定

**rejected** · **F023 再確認**（mid PASS ≠ tip-cv）。GPU E2E へ進めない。

## 成果物

- `kernels-output-chk252/`
- `chk252-tipcv-score.json`
