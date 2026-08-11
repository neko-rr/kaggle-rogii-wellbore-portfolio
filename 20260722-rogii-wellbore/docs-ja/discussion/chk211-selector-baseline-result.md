# CHK-211 / 209 公平比較 — selector-face baseline vs combo

> baseline: [tip-cv-sel-face-base-h20](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-base-h20)（CHK-211）  
> combo: [tip-cv-sel-face-combo-h20](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-combo-h20)（CHK-209）  
> 数値: `exp/work/wave20-upstream/chk211-score.json` · **提出なし**

## 1 行

**combo（init_spr9×seeds256）は tip lik-ensemble（selector 面）を改善しない。**  
hard20 RMSE **33.178 → 33.541**（Δ **−0.36** · 悪化）。  
seed-oracle は上がるが（208 Δ+1.25）、**現行の尤度重み付け面には乗らない**。

## 数値（hard20 · selector 面強制）

| 面 | RMSE | 備考 |
|---|---:|---|
| **211 baseline** 4.5×128 | **33.178** | 本番同型 PF 物差し |
| **209 combo** 9×256 | **33.541** | vs baseline **悪化** |
| tip-cv phys-blend（旧） | 14.870 | **リーク · 比較禁止** |

- 全行差異あり（maxabs 15.7）→ ノブは面を動かしている  
- 井単位: combo 良化 **11/20** · 悪化は `86454a6f`（Δ−2.70）が pooled を押し下げ

## 判定

| 仮説 | 判定 |
|---|---|
| tip-cv を selector 面で測れる（211） | **GO**（物差し確立） |
| combo が selector 面を ≥0.30 改善（209） | **NO-GO** |
| oracle↑ → tip 面↑ | **否**（208 PASS でも 209 悪化） |

## 次

1. **CHK-210** 物差し固定  
2. **CHK-205**（承認後）  
3. combo を本番 tip に載せない
