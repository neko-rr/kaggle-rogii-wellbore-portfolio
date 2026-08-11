# CHK-260 結果 — 多 run soft median/mean

> 2026-07-28 · Kaggle CPU `chk260-multirun-cpu` Ver1 · **提出なし**

## 要約

**rejected（NO-GO）** · 5 run（96 seeds×seed_base）の median/mean は single より悪い。

| agg | pooled RMSE | Δ vs single |
|---|---|---|
| single (run0) | 17.731 | — |
| mean | 19.462 | **−1.73** |
| median | 20.244 | **−2.51** |

井間の mean pair RMSE ≈ **4.09**（run 間ばらつきは大きいが、集約は悪化）。

## 解釈

- 非決定性は大きいが、median/mean で尖りを消すと tip soft より悪化。
- tip-cv 多 run 選定は局所根拠なし。

## 成果物

`exp/work/wave22-candidates/chk260-multirun-cpu-harvest/`
