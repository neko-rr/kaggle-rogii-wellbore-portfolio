# Raunak — ROGII Ultra Sub-6（1井 shape residual）

> analyzed: 2026-08-06  
> source: [`raunakdey07/rogii-ultra-sub-6-rmse`](https://www.kaggle.com/code/raunakdey07/rogii-ultra-sub-6-rmse)  
> 原文 pull: `others-notebook/public-useful-refresh-20260806/raunakdey07-rogii-ultra-sub-6-rmse/`  
> コード: `docs-en/others-notebook/raunakdey07-rogii-ultra-sub-6-rmse-Ver-latest.py`  
> lastRun: **2026-08-05 06:55 UTC** · votes ≈119

## 1 行結論

**Public 専用・1井パッチ**実験。ベース tip 軌跡を残し、井 `00e12e8b` だけに PF/branch 由来の **shape residual 10%** を加算（±0.40 ft キャップ · mean 0 保存）。  
evansussex / prvsiyan Frontier と同型の **Public 座標探索** · **F013/公開スコア系** · **Final 不可**。

## 使用するデータ

- 多数: koolbox · mpkg · fleongg · ravaghi · tabicl 等（tip スタック）

## 前処理 / 実験機構

1. Anchor: Ridge/PF + physical/PF selector  
2. 破棄候補 PF-1.3 を **shape 信号のみ**使用  
3. target 井 residual = learned_w0.60 − contact_before_branch_hedge  
4. 平滑・中心化後 **0.10×** を 6.594 予測に加算 · 他井 bit 同一

## 判定

| 項目 | 判定 |
|---|---|
| tip 同家系 | **はい**（アンカー + 1井 Public パッチ） |
| Final | **不可**（Public 追い · Trust 無） |
| 自チーム | farvol/Q0522 系の再発明 · **追跡のみ** |
| Active | **不要** |
