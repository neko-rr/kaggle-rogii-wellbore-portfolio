# CHK-245 結果 — TVT diversity prune → soft lik

> date: 2026-07-28 · GPU · `kazeneko77/tip-cv-gpu-prune16-r1p5-h20` · keep=16 · rad=1.5 · T=0.15

## 判定

**NO-GO**（tip-cv 採択閾値未達 · **提出なし**）

| 面 | RMSE | vs 凍結 T0.15 (29.899) |
|---|---:|---:|
| tip-cv hard20 | **29.951** | **−0.052** |
| 閾値（≥+0.30） | ≤29.599 | — |
| ローカル mid-bank screen | — | **+0.317**（偽陽性） |

## 含意

- mid-bank の PF soft-lik 改善が **tip-cv selector 面に転移しない**（P2 の別形態）。
- 多様性 prune を tip CFG に載せる根拠なし。再スイープしない。

出典: `chk245-gpu-prune16-r1p5-score.json` · `chk245-prune-grid.json`
