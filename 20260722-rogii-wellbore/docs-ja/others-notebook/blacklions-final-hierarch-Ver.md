# blacklions Final Hierarch — 日本語分析

> analyzed: 2026-07-30  
> source: [`blacklions/rogii-wellbore-geology-prediction-final-hierarch`](https://www.kaggle.com/code/blacklions/rogii-wellbore-geology-prediction-final-hierarch)  
> 原文: `others-notebook/public-useful-refresh-20260730/blacklions-final-hierarch/`  
> 関連: [evansussex Q0522](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md) · [GBDT-gate](../discussion/20260729-refresh.md)  
> license: **T034**

## 1 行結論

**Contact-Gated / Q0522 同家系**の終盤ツール。提出の既定は **アップロード済み 6.390 Q0522 チャンピオン固定**。その上に、井を1本ずつずらす **Public LB 向け座標探索**（定数 datum · ゼロ平均 slope · PF-shape プローブ）を載せる。  
自動 GBDT 上書きはしない（前回 well-level-gbdt-gate より「探針」寄り）。**別予測面ではない** → Final / Active CHK 化しない。

## 使用するデータ

Q0522 と同型 artifact DS（koolbox · pilkwang model-package · fleongg · ravaghi）。GPU OFF。

## 前処理 / パイプライン

1. tip 同型スタック（SP45/Ridge · PF · Beam · visible-prefix · contact guard · model-package · PF seed-branch · **Q0522**）  
2. **Champion lock:** `submission.csv` 既定 = 検証済 Q0522 6.390 ベクトル  
3. **Coordinate search:** 挑戦 CSV は **1井・低次元方向**だけ変更 · SHA で重複除去 · 報告 LB は二次診断用  
4. `LB_FINAL_SELECTION` を明示変更しない限りチャンピオンを上書きしない  

## モデルの定義

新規学習なし（新層で PF/Beam 再学習なし）。メタ: `champion_lock_coordinate_search`。

## 学習の設定

提出モード。重い CV OFF。

## 自チームへの示唆

| 判断 | 内容 |
|---|---|
| Public 評価 | 井単位 LB プローブは **σ≈0.03 ルール**に直撃しやすい · Private 非推奨 |
| Final | **不可**（tip/Q0522 同家系 · Public 座標探索） |
| 監視 | 「終盤の公開ツールが champion lock + probe」になった、という状況証拠のみ |
| CHK | **追加しない** |
