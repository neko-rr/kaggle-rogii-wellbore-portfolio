# 公開 NB — 物理・代替経路・祖先スタック（最新版）

> analyzed: 2026-07-23  
> コード: `docs-en/others-notebook/<slug>-Ver-latest.py`

---

## rogii-wellbore-tvt-physical-model（Sunnywu27）— **高優先**

### 使用するデータ
- コンペ train/test のみ（外部 DS なし）

### 前処理
- 物理: `tvt_from_contacts`（EGFDU 等の formation top と Z）
- GR の **interpolate(limit_direction=both)**（NaN 多い井で必須と明記）
- Savgol（beam 側）

### モデルの定義
- Train 既知部: 物理モデル（ノート主張 RMSE ~0.007 ft on visible）
- Hidden: **PF 500粒子 × 128 seeds · lik 加重（scale=5）** · init_spread=2.0
- Beam search 14 configs（補助）

### 学習の設定
- 教師あり GBM なし（追跡ベース）

### その他
- dual-track 公開スタックと **独立に見える** → Final 2 の多様性候補
- Discussion「非tabular / 物理」系と整合。自前 CV で現 Best(6.64) と比較すること

---

## physics-informed-baseline（Karnakbayev Artur）

### 使用するデータ
- コンペ + hill-climbing wheel 等

### 前処理 / モデル
- PF（ancc + z）ブレンド後処理 · LGBM/CatBoost/Ridge · Optuna · hill-climbing

### その他
- 初期物理+GBM 系の改良版。現 Public 上位スタックより古い世代。手法メモ用

---

## drift-targeting-ncc-tree-based-rogii-wellbore（Mitch）

### 使用するデータ
- コンペ + 付帯 `rogii-wellbore-models`（学習済み fold / KNN）

### 前処理
- **目標を absolute TVT ではなく drift**（TVT − last_anchor）
- multi-scale NCC · formation plane KNN · DWT GR · beam/PF 特徴

### モデルの定義
- XGB + CatBoost + HGB · NNLS blend（LB **8.905** 記載）

### 学習の設定
- GroupKFold 5 · Optuna（学習は別 NB · 本編は推論再現）

### その他
- writeup の **R3 drift 再定義**が最大ジャンプ。特徴アイデアの宝庫だがスコアは旧世代
- 姉妹: `gr-features-outlier-detection-…`（outlier / GR）

---

## rogii-another-approach / another-approch-2nd（Yusuke Togashi）

### 使用するデータ
- 公開 dual-track 系と同様（koolbox / artifacts / fleongg 痕跡）

### 前処理 / モデル
- タイトルは「Another」だが中身は **det-base + midpoint hedge（例: α=1.6 seplo=4）** 等の変種
- 冒頭に What worked / What failed の実験ログあり（有用）

### その他
- **アーキテクチャ多様性は期待しない**。実験メモとハイパラ差分だけ拾う

---

## wellbore-geology-prediction-ridge（Mahdi Ravaghi）

### 使用するデータ
- コンペ + `ravaghi/wellbore-geology-prediction-artifacts` + koolbox

### モデルの定義
- PF/beam selector · LGBM/CatBoost → Ridge · GroupKFold  
- 現在の公開 dual-track エコシステムの **祖先**

### その他
- Ver2 全家系が依存する artifacts の出発点。採用時 Tier R

---

## rogii-geology-aware-ensembling-lb-7-129（Roman Rozen）

### 使用するデータ
- koolbox · fleongg 系（dual-pipeline 近縁）

### モデルの定義
- Track A: PF + GBM · Track B: fleongg 系 · blend · per-well 校正 · geology gate

### その他
- LB ~7.1。自提出 dual-pipeline と同族 → Final 主軸の新味は薄い

---

## FOYSAL: pf-contact-gold-calibration-stack / experimental-notebook

### 使用するデータ
- 公開 rebuild ベース + fleongg / pilkwang 痕跡

### 前処理 / モデル
- heel/affine GR 校正 · contact/gold · PF スタック
- experimental: Base LB 7.153 → **実験 LB 9.615（悪化を開示）**

### その他
- Working Note（Anchors / Guarded）精神と一致する **失敗の公開**が価値
- 校正アイデアは B2 候補だが、数字だけで採用しない
