# Wave-31 overnight / resume LB — 2026-07-31

> participant: Kazeneko · metric: Public RMSE（低いほど良い）· σ≈0.03  
> **αグリッド確定後:** [`ops-lb-wave31-farvol-alpha-public-2026-08-01.md`](ops-lb-wave31-farvol-alpha-public-2026-08-01.md)（表示Best **6.190**）

## 確定スコア（診断提出 · Final枠は未差替）

| ref | 仮説 | Public | vs OPS-C 6.237 | vs tip 6.269 |
|---|---|---:|---:|---:|
| **55118587** | tip×farvol 0.90/0.10 | **6.226** | **−0.011** | **−0.043** |
| 55094041 | OPS-C tip×SUB-9 0.90/0.10 | 6.237 | 0 | −0.032 |
| 55117902 | tip×SUB-13 0.90/0.10 | 6.247 | +0.010 | −0.022 |
| 55118915 | CHK-437 post-unlock | 6.250 | +0.013 | −0.019 |
| 55006677 | SUB-14 tip T0.15 | 6.269 | +0.032 | 0 |
| 55118585 | tip×compound 0.90/0.10 | 6.284 | +0.047 | +0.015 |
| 55117901 | OPS-C×SUB-13 | 6.353 | +0.116 | +0.084 |
| 55122006 | tip×SUB-13 0.80/0.20 | PENDING | — | — |
| 55148128 | tip×farvol 0.95/0.05 | PENDING | — | — |
| 55148153 | tip×farvol 0.85/0.15 | PENDING | — | — |
| 55148271 | tip×farvol 0.88/0.12 | PENDING | — | — |
| 55148294 | tip×farvol 0.80/0.20 | PENDING | — | — |

## 解釈

- **farvol 薄ブレンド**は Public 上 Best（OPS-C）をわずかに下回る（**6.226** 確定）。σ帯のため確定改善ではないが、compound より明確に良い。
- compound は tip/OPS-C より悪化 → **パートナー NO-GO**。
- tip-cv proxy screen（CPU）: `farvol_like` のみ tip を微改善（Δ≈−0.003〜−0.006）。CF/midpoint は悪化。
- **αグリッド追加提出（2026-08-01）** は採点待ち。これ以上の farvol α 連打は Stop。
- Final2 差替はユーザー選択（OPS-C vs farvol）。

## 次

- αグリッド4本 + 55122006 harvest
- CHK-421 farvol候補化 · CHK-448 selector本番 tip-cv（Wave-31b）
