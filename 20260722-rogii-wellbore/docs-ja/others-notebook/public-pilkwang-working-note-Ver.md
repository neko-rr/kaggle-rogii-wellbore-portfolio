# 公開 NB — Pilkwang Working Note / EDA（最新版）

> analyzed: 2026-07-23  
> kernels: `working-note-target-free-tvt-geosteering` · `rogii-eda-target-free-alignment-for-tvt`  
> コード: `docs-en/others-notebook/<slug>-Ver-latest.py`

---

## working-note-target-free-tvt-geosteering

### 使用するデータ
- コンペ + 公開スタック周辺 DS（koolbox / artifacts 等 · ノート規模大）

### 前処理
- **Target-free alignment**: 予測区間の真 TVT に依存しない整合（heel / typewell / GR）
- NCC · Savgol · heel 校正 · bimodal/midpoint 系の痕跡

### モデルの定義
- dual-track 近縁（PF + LGBM/CatBoost/XGB/Ridge）を含む実装・説明ノート
- Working Note としての「何が効いて何が効かない」叙述が主価値

### 学習の設定
- GroupKFold 等（実装ブロックに依存）

### その他
- Host 受賞の radiant/malyshev ノートとは別系統（Pilkwang 自作 Working Note）
- コードをそのまま Best に足すより、**整合手順の文章**を B2 CHK に落とす

---

## rogii-eda-target-free-alignment-for-tvt

### 使用するデータ
- 同上（EDA 寄り・巨大セル）

### 前処理 / 可視化
- typewell–lateral 整合の図 · drift · 物理参照との比較

### モデルの定義
- 提出パイプライン断片あり（koolbox 使用）

### その他
- EDA として読む。提出主軸は dual-track 本流（`rogii-dual-track-…`）側
