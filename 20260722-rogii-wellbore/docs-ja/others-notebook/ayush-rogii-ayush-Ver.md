# Ayush — Rogii_Ayush（CatBoost tabular starter）

> analyzed: 2026-08-06  
> source: [`ayushtiwariiitg/rogii-ayush`](https://www.kaggle.com/code/ayushtiwariiitg/rogii-ayush)  
> 原文 pull: `others-notebook/public-useful-refresh-20260806/ayushtiwariiitg-rogii-ayush/`  
> コード: `docs-en/others-notebook/ayushtiwariiitg-rogii-ayush-Ver-latest.py`  
> lastRun: **2026-08-05 11:26 UTC** · votes ≈2 · コンペ DS のみ

## 1 行結論

**tip/Q0522 以外**の **行寄り CatBoost** 初級スターター。天井は低く **Final / Active 不要**。教育用のみ。

## 使用するデータ

- `/kaggle/input/competitions/rogii-wellbore-geology-prediction/train` の `*__horizontal_well.csv` 等
- 外部 DS なし

## 前処理

- 水平井 CSV を列挙して行結合
- 基本的な feature 組み立て（軌道・検層寄り tabular）
- GroupShuffleSplit（well group）

## モデルの定義

- **CatBoostRegressor**（絶対 TVT または簡易特徴から直接回帰）

## 学習の設定

- GroupShuffleSplit · RMSE
- 提出 `submission.csv` 生成セルあり

## その他

| 項目 | 判定 |
|---|---|
| tip 同家系 | **いいえ** |
| Final 採用 | **いいえ** |
| 自チーム | CatBoost residual 路線（roman / CHK-070）の **薄型再発明** · 新 CHK 不要 |
| Active | **不要** |
