# [1st / Ruby] コード要約 — submit_reproduce

**分析日:** 2026-08-08  
**順位:** Private **#1 / 5.639**  
**作者:** Ruby (@w5833946)  
**公開コード:** [submit-reproduce](https://www.kaggle.com/code/w5833946/submit-reproduce)  
**ローカル:** `retro/archive/others-notebook/post-comp-top-20260808/rank01-ruby-w5833946-submit-reproduce/`  
**writeup:** Discussion [733220](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220)

---

## 要約

- 公開物の中心は **推論オーケストレーション NB**。重みごとに private **Dataset 7本**（`rogii-07xx-v*-cv*`）をマウントし、各 bundle 内の `seq_NN_main.py` で test 予測を吐く。  
- 最終は **井戸単位の XY-neighbor 安全ゲート**で、`xy_based_combs` と `GR_only_combs` の重み付き平均を切替。  
- **学習コード本体は Dataset 側**（`seq_NN*` + `cfg.pkl`）。NB は BF16→FP32 の Kaggle 互換ハック付き。

---

## パイプライン（コード通り）

```
combs = 7 学習バージョン (marker, dataset_path, unused_weight)
    for each: copy dataset → fix cfg.amp_dtype=float32 → seq_NN_main.py --submit-mode
    → submission_details_{marker}.pqt / pred parquet
    clean workspace

ensemble:
    xy_stats from one model OOF/test details (geo_nbr_*)
    per well: if xy_safe → weighted mean(xy_based_combs)
               else      → weighted mean(GR_only_combs)
    → submission.csv (id, tvt)
```

### 7 メンバー（NB の `combs`）

| marker | dataset slug | 備考（writeup 対応） |
|---|---|---|
| 0719_V1 | rogii-0719-v1-cv509 | default GR 系 |
| 0724_V1 | ...cv486 | |
| 0729_V3 | ...cv553 | +PF チャンネル系 |
| 0801_V1 | ...cv516 | |
| 0801_V2 | ...cv480 | xy stats 参照元 |
| 0802_V2 | ...cv513 | |
| 0803_V2 | ...cv500 | |

### XY 安全条件（コード固定閾値）

すべて AND:

- `geo_nbr_distance < 2459`
- `geo_nbr_distance_q10 < 1426`
- `geo_nbr_path_alignment > 0.96`
- `geo_radial_extrap_score < 1.45`
- `geo_prefix_weight_ratio < 0.315`

### ブレンド重み（井ごと）

| セット | (marker, weight) |
|---|---|
| **xy_based** | 0719_V1×0.25, 0801_V1×0.25, 0724_V1×1, 0801_V2×1, 0803_V2×1 |
| **GR_only** | 0719_V1×1, 0729_V3×0.5, 0801_V1×1 |

val MODE では同一ロジックで OOF を合成し RMSE を print。

---

## 主要ファイル

| ファイル | 役割 |
|---|---|
| `submit-reproduce.ipynb` | 推論ループ + ensemble（本要約の対象） |
| `kernel-metadata.json` | dataset_sources / T4 / GPU ON / Internet OFF |
| `/kaggle/input/.../seq_NN_main.py` 等 | **各 weight dataset 内**（未pull） |
| `cfg.pkl` | 学習/推論設定 · amp_dtype を FP32 に書換 |

---

## 再現性

| 項目 | 評価 | メモ |
|---|---|---|
| コード入手 | **中** | Infer NB 公開 · train は dataset 同梱 |
| 重み | **要 DS pull** | 7 private datasets 公開前提 |
| 計算量 | 高 | T4 上で 7 本フル infer |
| 学習再現 | 中 | NB 末尾: `seq_full_train` · 4080S · BF16 必要と記載 |

---

## 改造・学習ポイント（自チーム向け）

1. **井単位の「事前が信用できるか」ゲート** — Pub で悪くても CV 改善なら残す writeup 方針と一致。  
2. **GR-only vs 地理チャネル の二レシピ**をハードに切替（ソフトな α より明確）。  
3. tip residual 一発より **複数 alignment チェックポイント + 条件付き bag**。  
4. Kaggle 実行制約: **BF16 不可 → cfg 上書き**の類の運用ハックが必須級。

---

## 未確認

- [ ] weight dataset 内 `seq_NN_cfg.py` / ConvNeXt 実装の pull  
- [ ] 学習の exact hyperparam を writeup 表と突き合わせ
