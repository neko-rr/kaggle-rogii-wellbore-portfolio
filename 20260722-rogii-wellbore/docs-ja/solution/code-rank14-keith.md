# [14th / keithtyser] コード要約 — hierarchical U-Net stack

**分析日:** 2026-08-08  
**順位:** Private **#14 / 6.329**（README）· writeup CV **6.252**  
**作者:** keithtyser (ktyser) · Discussion [733201](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733201)  
**訓練コード:** https://github.com/keithtyser/rogii-wellbore-geology-solution  
**提出:** [private-14th-…-submit](https://www.kaggle.com/code/keithtyser/private-14th-rogii-construction-a-v1-submit)  
**ローカル:**  
- 学習: `retro/archive/solutions/code/keithtyser-rogii-wellbore-geology-solution/`  
- 提出: `retro/archive/others-notebook/post-comp-top-20260808/rank14-keithtyser-private-14th-construction-a-v1-submit/`

---

## 要約

- **最もしっかり読めるフル学習 repo**（README + recipe + folds + frozen coeffs）。  
- 階層: **(1) multi U-Net blend** → **(2) abs-frame XGB margin + well gate** → **(3) W96–W48 scale direction** → **(4) W64 seed-average direction**。  
- 提出 script は **係数・シード名簿をハードコード**し、複数 private checkpoint DS を読み hidden test のみ予測。

---

## パイプライン

```
U-Net bank (trajectory_*/shifted_path_rank · widths 32/48/64/96)
        +
ABS_FRAME_ROW_XGB_V1 (row engineered features)
        →
ABS_FRAME_WELL_GATE_V2 (per-well choose UNet vs XGB side via pG)
        +
d96 = raw_coef_f * (pred_W96_block16 - pred_W48_block16)   # scale-normalized in train receipt
        +
w64 = raw_seed_coef_f * mean(seed width64 best.pt per fold) - base
        →
average 5 outer folds → submission
```

### 提出 script の固定値（抜粋）

- `FOLD_P0_WEIGHTS`: 5 folds × 6 U-Net members  
- `D96_RAW_COEFFICIENTS` + `D96_TRAINING_SCALES`  
- `W64_SEED_RAW_COEFFICIENTS`（**scale で割らない**とコメント警告）  
- `W64_SEED_ROSTER` per fold（fold 1,3 は seed 2 本のみ）  
- Frozen CV pin: **6.251777…**

### repo モジュール要点

| パス | 役割 |
|---|---|
| `scripts/train_unet.py` | 1D U-Net 学習 |
| `src/rogii_research/tucker_unet.py` 他 | path/U-Net 拡張・損失 |
| `features/abs_frame_row_xgb.py` | 143 特徴 XGB |
| `features/fit_gate_v2.py` | well gate |
| `stack/fit_seed_direction.py` | seed 方向係数 fit |
| `folds/folds_random.csv` | **773 wells · 5 fold whole-well** |
| `submissions/recipes/*.json` | 提出レシピ |

---

## 再現性

| 項目 | 評価 |
|---|---|
| 学習 | **高**（手順 README 完備 · GPU 長時間） |
| 提出 | 高 · ただし **checkpoint DS 6本** 必須 |
| 自前移植 | 中–高 · レシピ/係数の厳密性とスケール規約に注意 |

---

## 改造・学習ポイント

1. **direction stacking** — base の差 `(W96−W48)` に **fold 固定係数**だけで量を足す（α スイープより安定運用向き）。  
2. **well gate** — 行 ensemble ではなく **井全体で UNet 系 vs 表形式側**を選ぶ。  
3. **seed roster を途中凍結**しても金圏 — 完璧な均等 seed より **receipt 固定**。  
4. CV: **grouped whole-well pooled-row** を真実の物差しに pin。

---

## 自チームとの差分（コード視点）

| | keith #14 | Kazeneko |
|---|---|---|
| 本体 | multi 1D U-Net + XGB + directions | tip + residual α |
| 階層 | 4-stage construction 領収書 | Final 2 面 |
| 係数 | fold 固定 · 検証 identity | dual residual 機構実験 |

---

## 未確認

- [ ] `docs/RECIPE.md` 全 hyperparam 転記  
- [ ] U-Net 入出力テンソル形状の図解
