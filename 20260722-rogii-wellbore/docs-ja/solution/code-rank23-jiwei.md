# [23rd / Kaggle Agent] コード要約 — alignment U-Net + residual + router

**分析日:** 2026-08-08  
**順位:** Private **#23 / 6.555**  
**作者:** Jiwei Liu · Team Kaggle Agent  
**公開コード:** [rogii-v5-run4-sr-dual-t4](https://www.kaggle.com/code/jiweiliu/rogii-v5-run4-sr-dual-t4)（script · ~2935 行）  
**ローカル:** `retro/archive/others-notebook/post-comp-top-20260808/rank23-jiweiliu-rogii-v5-run4-sr-dual-t4/`  
**writeup:** [733135](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733135)

---

## 要約

- **単一 self-contained 推論 script**。学習は private weight datasets 3本に固化。  
- 実装が writeup の三段（Core alignment · Residual · Structural/surface **router**）と直結。  
- クラス: `AlignmentUNet` · `AlignmentBlock` · `Well` · `SpatialReferenceStore` · `AnccReferenceStore` など。

---

## パイプライン（関数名より）

```
load test wells + typewell family
        ↓
make_alignment_example / sequence → AlignmentUNet family (narrow/wide/supervised/… weights)
        ↓ posterior mean / temperatures / member weights (constants at file head)
        ↓
c016 residual local nets (seeds, temperatures) + posterior planes
        ↓
run4_select_route · surface configs (neighbors, bandwidth, rotation 138°)
        →
spatially_correct / ancc_surface / residual_gr / gr_path corrections (sparse)
        →
submission
```

### ファイル先頭の運用定数（抜粋）

- 多数の **member weight**（WIDE_SUPERVISED_WEIGHT=0.5 など）  
- residual 窓 `C016_*` · `RUN4_CORRECTION_SCALE=0.60`  
- surface: `neighbor_count` 10/16/24 · cluster · decay · 回転  
- spatial analog / local / geometry / GR calibration の **小スケール**ゲイン  
- 明示: 「Conservative hedge · stop at 6.189485 accepted stack」

### 主要クラス

| クラス | 役割 |
|---|---|
| `AlignmentUNet` | 2D 整列本体 |
| `AlignmentBlock` | UNet ブロック |
| `SequenceConfig` | 位置サンプル・state 解像度 |
| `SpatialReferenceStore` | 近傍井 surface donor |
| `AnccReferenceStore` | ANCC 系 surface |

### 代表関数群

- 整列: `make_alignment_example`, `masked_alignment_views`, `c016_*`  
- 補正: `residual_viterbi`, `residual_gr_correction`, `spatially_correct_prediction`  
- ルート: `run4_select_route`, `run4_outer_prediction`, `run4_numeric_features`

---

## weight datasets（metadata）

1. `jiweiliu/rogii-compact-alignment-cv5-weights`  
2. `jiweiliu/rogii-v5-promoted-c016-weights`  
3. `jiweiliu/rogii-v5-run4-structural-surface-router`  

---

## 再現性

| 項目 | 評価 |
|---|---|
| 推論コード | **高** · script 1本で論理が読める |
| 重み | DS 3本必要 |
| 学習 | 中 · writeup の synth/nest CV · 本 script は infer 中心 |

---

## 改造・学習ポイント

1. **writeup とコードの名前が一致**（router / residual / alignment）→ 再現研究しやすい。  
2. **棄権可能な surface 補正**をスケール 0.6 と config 複数で制御。  
3. 多数ファミリを **固定重みで平均**（学習時 dual 後に固定）。  
4. tip residual 単層と対照的な **「整列分布 → 局所 residual → 構造候補」** 三段実装の完成形。

---

## 未確認

- [ ] AlignmentUNet の channel 数・state grid の定数  
- [ ] run4 XGB/ExtraTrees router の feature 列一覧
