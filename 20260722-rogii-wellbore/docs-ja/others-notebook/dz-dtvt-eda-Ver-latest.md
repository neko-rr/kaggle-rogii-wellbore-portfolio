# dz-dtvt-eda — 日本語要約

> analyzed: 2026-07-25  
> source: `connortynan/dz-dtvt-eda`  
> 原文フォルダ: `others-notebook/public-useful-refresh-20260725/dz-dtvt-eda/`  
> コード抽出: `docs-en/others-notebook/dz-dtvt-eda-Ver-latest.py`  
> 索引: [public-useful-refresh-20260725.md](public-useful-refresh-20260725.md)

## 家系判定（1行）

**純幾何の研究ログ**（提出用 tip スタックではない）。GR を意図的に使わず、`dTVT ≈ −dZ + drift` の天井を測る。

## 使用するデータ

- 公式コンペ train laterals（773）+ test trajectory（GR は本編では未使用）
- Volume-2 GR fusion / typewell decode は別ノート参照として言及（v3/v4）

## 前処理

- ステップ単位で `−dZ → dTVT` を当て、**積分して** TVT を進める（cumsum 同士の当てはめは hysteresis を隠すため避ける）
- 各 train 井を K=16 の定数 drift セグメントに圧縮 → heading で脱投影 → Gaussian kNN（k=15, h=500 ft）で空間場化
- `kappa`（0–1）で donor 距離・進行に応じて「動かさない」側へブレンド
- near-strike では tops 由来の局所 dip 方向に切り替え（回転が大きいと hold）

## モデルの定義

- 地域 dip: `b ≈ D·cos(az − θ₀)`（例: D≈0.035, θ₀≈118°）
- ローカル drift 場 + kappa 信頼ダイヤル
- GR fusion（v3）は「幾何の残り」を埋める別経路（本 NB の主眼外）

## 学習の設定 / 検証

- 報告スコアは **LOO / buffered-LOO**（oracle TVT を予測に入れない）
- placebo · holdout で kappa 構造を監査
- 失敗談を残す: PS 非対応の endErr 代理指標で最適化した時代（Ch.3→4）

## その他（LB・自チーム）

| 項目 | 内容 |
|---|---|
| Public LB 梯子 | hold 15.88 → v1 10.79 → v2 10.356 → v3 10.098（幾何+軽い GR） |
| 含意 | 幾何だけだと ~10 ft 帯。sub-6 は **自井 GR / 整合** の価値 |
| 戦略 | EDA 拘束（TVT identity · field 近傍）と整合。**Final コード採用なし** |
| 優先 | **S（必読・教育）** |
