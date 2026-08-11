# CHK-214 結果 — tip-cv selector · init_spr=12 ± T

> date: 2026-07-26 · GPU harvest · **提出なし**  
> kernels: [T=1.0](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-spr12-t1p0-h20) · [T=0.5](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-spr12-t0p5-h20)  
> 数値: [`chk214-score.json`](../../exp/work/wave20-upstream/chk214-score.json)  
> 物差し: CHK-211 baseline **33.178** · PASS ≤ 33.178 − 0.30

## 1 行

**NO-GO。** spr12 は seed-oracle では最良（213 +2.50）だが、tip selector 面では **悪化**（T1.0 Δ−0.23 · T0.5 Δ−0.25）。209 combo と同型。

## 数値（hard20 · selector 面）

| 面 | RMSE | vs 211 |
|---|---:|---:|
| **211 baseline** 4.5×128 | **33.178** | — |
| spr12 · T=1.0 | **33.413** | **−0.235** |
| spr12 · T=0.5 | **33.428** | **−0.250** |

- 全行が baseline と異なる（maxabs ≈33）→ ノブは面を動かしているが、方向が悪い
- PASS 条件（≥+0.30）未達

## 判定

| 仮説 | 判定 |
|---|---|
| init_spr=12 が tip selector を ≥+0.30 | **NO-GO** |
| spr12+T0.5 複合 | **NO-GO** |
| tip CFG に spr12 を載せる（CHK-215） | **作らない** |

## 分岐（確定）

- spr12 は **命中専用**（oracle screen）· tip には載せない
- tip 軸は **T0.5（SUB-13）** を維持
- CHK-215 は **cancelled**（214 NO-GO）

## Explicit Stop

- spr12 / combo を tip CFG に載せない（209/214）
- oracle↑ を tip 面成功と誤認しない
