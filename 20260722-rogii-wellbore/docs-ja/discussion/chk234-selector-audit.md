# CHK-234 T4 監査 — tip-cv selector BIN routing

> date: 2026-07-28 · **提出なし**

## 発見

tip-cv は `SELECTOR_GLOBAL_VARIANT` ではなく **`selector_well_code` → `SELECTOR_BIN_VARIANTS`** で variant を選ぶ。

| hold | hard20 井数 | pooled tip-cv RMSE（参考） |
|---:|---:|---:|
| **0.05** | **13** | 29.11 |
| 0.15 | 6 | 32.53 |
| 0.20 | 1 | 22.77 |

code 4/5（薄い hold + beam）が hard20 の過半。これが CHK-231c（GLOBAL だけ差し替え → ≡baseline）の説明。

## Graft（実行中）

全 BIN → `pf_scale_8_hold_0.2`（選択のみ · generator 不変 · F015）  
GPU: `tip-cv-gpu-sel-force-global-h20`

出典: `chk234-selector-audit-report.json` · `chk234-selector-audit-per-well.csv`
