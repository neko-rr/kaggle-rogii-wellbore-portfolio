# The ±15 ft datum: why some wells are unsolvable

> Topic ID: **711878**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/711878  
> 投稿者: **souldrive** · **2026/06/22** UTC · 票 19  
> 原文: `docs-en/discussion/711878-pm15ft-datum-unsolvable-wells.md`

## 要約

誤差構造: 約半数は GR/構造モデルで per-well RMSE **&lt;~5**、重い尾が総誤差を支配。

**地質メカニズム（Eagle Ford）:**
- Milankovitch 周期の石灰岩–泥岩カップル（~15–25 ft）
- 長ラテラルでは Typewell と **約1バンドル離れた2位置**が同程度に合う → datum が **二峰（おおよそ ±15 ft）**
- 少数は小断層で 15–20 ft ステップ

**意思決定:**
- 真に 50/50 なら RMSE 最適は **どちらか一方ではなく中点**
- 一方にコミット → 期待 RMSE ≈21 ft、中点 → ≈15 ft
- 「正しいモードを当てる」はスコアを悪化させやすい

Notebook: `souldrive/decoding-eagle-ford-why-some-wells-are-hard`

## コメント要点

- Georgy: GR misfit が真値で decoy より悪くなりうる — 機構と一致。束間隔で曖昧性検出→hedge
- Tucker ~5（per-well only）が重要 — line-oracle 超えは可能
- **Private OOF 共有は Rules 違反**（Patrick 指摘 → 取り消し）

## スコア向上への示唆

1. 尾部井はモード当てより **中点 / 校正 hedge**  
2. 中央の solvable wells と構造スムージングで稼ぐ  
3. 二峰残差を CV 診断に入れる  

## 関連

- 727149 Georgy（unobservable）· 726834 同誤収束
