# Anubhav — ROGII Wellbore Prediction Challenge（LightGBM residual）

> analyzed: 2026-08-05  
> source: [`anubhavtyagi1212/rogii-wellbore-prediction-challenge`](https://www.kaggle.com/code/anubhavtyagi1212/rogii-wellbore-prediction-challenge)  
> 原文 pull: `others-notebook/public-useful-refresh-20260805/rogii-wellbore-prediction-challenge/`  
> コード抜粋: `docs-en/others-notebook/anubhav-wellbore-prediction-challenge-Ver-latest.py`  
> lastRun: **2026-08-04 21:34 UTC** · votes ≈1 · GPU ON · コンペ DS のみ

## 1 行結論

**tip / Q0522 同家系ではない** typewell 整合 + **LightGBM residual** の中級スターター。  
速度短縮（LSTM 削除 · 窓削減 · GroupKFold 3）が主題。**天井は高くない想定** · Final / Active **不要**（教育・系統多様性の参考のみ）。

## 使用するデータ

- コンペ `rogii-wellbore-geology-prediction` のみ（外部 DS なし）
- typewell CSV · 検層 · 軌道

## 前処理

1. typewell との GR 整合・補間経路  
2. GR 窓を **[25, 75]** に縮小（旧 [10,25,50,100] から削減）  
3. lag/lead GR · 重い DLS 曲率ループを削除  
4. 残り NaN は線形補間

## モデルの定義

- 主: **LightGBM residual**（ベース幾何 / typewell 由来 TVT 推定からの残差）  
- 過去案の LSTM は速度のため **除去**（コメントに dual / residual 接続の残骸）

## 学習の設定

- **GroupKFold · 3 folds**（5→3 に削減）  
- RobustScaler  
- GPU 可能環境想定

## その他

| 項目 | 判定 |
|---|---|
| tip 同家系 | **いいえ** |
| Final 採用 | **いいえ**（公開弱く · 独力 CV 未提示） |
| 自チーム示唆 | romanrozen CatBoost residual 系・CHK-070 近傍の **薄型再発明** · 既に residual レーンは自前 |
| Active CHK | **不要** |

## スコア向上にとって

| 判断 | 内容 |
|---|---|
| 低 | 新機構なし · 締め日に追い residual LGBM starter は不要 |
| 参考のみ | 「独自 tabular residual」も終盤は公開弱のまま残りやすい、という観測 |
