# 公開 NB — 検証・教育系（最新版）

> analyzed: 2026-07-23  
> コード: `docs-en/others-notebook/<slug>-Ver-latest.py`

---

## fork-the-ruler-not-the-model（Georgy Mamarin）

### 使用するデータ
- コンペ `train/`（主に監査・oracle）
- 付帯: `georgymamarin/geosteering-world-cup-2021-expert-interpretations`（関連ノート参照）

### 前処理
- robust 多項式 fit · GR denoise（rolling median）
- typewell GR 補間 · heel 校正（`_calib`）
- 二峰コスト（`two_minima` · sep≈6）

### モデルの定義
- **提出モデルではない**。中心は **calibrated oracle ladder**（完全情報〜制約付き oracle の RMSE 階段）
- GR–typewell matching の品質天井 · leave-field-out
- コミュニティ主張（近傍コピー等）を **ruler で再検証**

### 学習の設定
- 学習なし（診断・可視化・再現実験）

### その他
- 結論メッセージ: **「モデルを fork するな、物差しを fork せよ」**
- 自チーム: Best 提出の **well-group / leave-field CV** をこの型で実装する CHK を最優先

---

## what-is-the-precision-of-a-manual-interpretation（Georgy）

### 使用するデータ
- コンペ train（ANCC 等の「描かれた線」の性質）
- **Geosteering World Cup 2021** tidy 表（専門家 176 名の解釈）

### 前処理
- m→ft 変換 · lateral（inc>85°）制限 · 勾配量子化テスト

### モデルの定義
- なし。人間ラベルの再現性・クラウド集約（**median ≫ mean**）

### 学習の設定
- なし

### その他
- **LB は改善しない**と著者明記。Final 2 の「別メカニズム」や hedge の哲学根拠に使う
- ライセンス: 出典 NORCE/UiS · CC BY 4.0（ノート記載）→ ledger 要確認

---

## rogii-honest-carry-forward-baseline-groupkfold（n0Rollback）

### 使用するデータ
- コンペ train/test のみ

### 前処理
- 評価区間 = `TVT_input` NaN · last known TVT · 軌道特徴（dist, dz, GR, gr_dev）

### モデルの定義
- Baseline: **carry-forward**
- 比較: HistGradientBoosting で residual（軌道のみ）

### 学習の設定
- GroupKFold(5) by well · 250 wells サンプル

### その他
- 主張: 軌道 GB **は carry-forward に負け**、真の信号は GR–typewell
- Discussion 726751（row-wise fails）と完全整合。**否定実験のテンプレ**

---

## rogii-geosteering-for-beginners-7-visuals / visual-eda（n0Rollback）

### 使用するデータ
- コンペ train（`*.png` 断面含む）· test

### 前処理 / モデル
- 可視化中心（typewell 指紋 · 軌道 · heel vs predict · formation surfaces · GR by geology）
- 末尾に謙虚な baseline（詳細は beginners ノート）

### その他
- 公式 png を読む習慣の SSOT。オンボーディング必須

---

## eda-starter / xgb-starter-cv-15（Chris Deotte）

### 使用するデータ
- コンペのみ

### 前処理
- heel 文脈特徴 · typewell GR 相関風特徴（簡易）
- residual = TVT − last known `TVT_input`

### モデルの定義
- XGBRegressor（hist / CUDA 想定）· GroupKFold by well

### 学習の設定
- 5-fold · CV 帯 ~15（タイトルどおり）→ **行寄り ML の天井デモ**

### その他
- 強さは再現可能な starter 規律。提出主軸にはしない（既知）
