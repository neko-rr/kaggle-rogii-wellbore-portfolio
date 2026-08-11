# Farhan — ROGII Best Score（tip プロファイル切替）

> analyzed: 2026-08-06  
> source: [`farhanabidtech786/rogii-best-score-wellbore-geology-prediction`](https://www.kaggle.com/code/farhanabidtech786/rogii-best-score-wellbore-geology-prediction)  
> 原文 pull: `others-notebook/public-useful-refresh-20260806/farhanabidtech786-rogii-best-score-wellbore-geology-prediction/`  
> コード: `docs-en/others-notebook/farhanabidtech786-rogii-best-score-wellbore-geology-prediction-Ver-latest.py`  
> lastRun: **2026-08-05 19:32 UTC** · votes ≈37

## 1 行結論

**古典 tip 同家系**。`SUBMISSION_PROFILE` で contact / vp_balanced / model_pkg 等 **11 プロファイル切替**。  
基盤クレジット: Дворкин 系 · 多数外部 artifacts（koolbox · fleongg · ravaghi · mpkg 等）。  
**F013 型** · **Final 不可** · **捨て/監視のみ**。

## 使用するデータ

- コンペ + `koolbox-offline` · `rogii-03` · `rogii-model-package` · `rogii-v10-fresh-artifacts` · `fleongg/claude-models` · `tabicl-mirror` · `ravaghi artifacts` 等

## 前処理 / モデル

- PF / contact gate / sp45 blend / model package residual を **プロファイル表**で合成
- アクティブ例: `vp_balanced_modelpkg_005`（balanced · sp45 0.60 · mpkg α≈0.004）

## 判定

| 項目 | 判定 |
|---|---|
| tip 同家系 | **はい**（改題+プロファイル） |
| Final | **不可** |
| 自チーム | F013 再スイープ禁止と一致 · 追跡のみ |
