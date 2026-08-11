# New to ROGII? A beginner's map — why row-wise ML fails

> Topic ID: **726751**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/726751  
> 投稿者: **n0Rollback**（一般参加者）  
> 投稿日時: **2026/07/16** UTC  
> 最新コメント: **2026/07/17** UTC（n0Rollback 返信）  
> 票: 15  
> 原文: `docs-en/discussion/726751-beginners-map-why-rowwise-ML-fails.md`

## 要約

初心者向け Notebook（7 visuals）の宣伝＋**否定結果**が本体。

- タスクの本質: 水平坑井のビット垂直位置（TVT）を、Typewell の垂直 GR と照合して推定（ジオステアリング）
- 各 train well の `{id}.png` 断面図が最重要アーティファクトだが開かれにくい
- **anchor-hold**（最後の既知 TVT を水平に保持）: OOF RMSE **≈16.1**
- 行単位 LightGBM（GR shape + 軌道）: **17.463** — **ベースラインより悪化**

教訓: **系列問題**。1 行の GR だけでは上下数 ft の判別がほぼ不可。信号は系列と Typewell 整合にある。

コメント（2026/07/17）: 本命は type-well alignment · state-space / HMM 系（Notebook 後半）。

## スコア向上への示唆

- 最初のゲートは **anchor-hold 超え**
- 行単位 ML を「本命」にしない（Bets と整合）

## 効果が薄かった取り組み

- 素直な row-wise LightGBM
