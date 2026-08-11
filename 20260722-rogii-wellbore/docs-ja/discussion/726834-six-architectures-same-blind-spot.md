# Six independently-trained architectures, same blind spot

> Topic ID: **726834**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/726834  
> 投稿者: **OpPrime** · **2026/07/16** UTC · 票 3  
> 原文: `docs-en/discussion/726834-six-architectures-same-blind-spot.md`

## 要約

GRU/CNN/SDF 等 **6 独立モデル**が、ある区間で互いに収束しつつ **同じ大きな誤り**（例: ~2600 ft 区間で真値との差が単調に ~90 ft）。平均で直らない構造的ブラインドスポット（GR 周期曖昧性・オフセット不足など仮説）。

## 示唆

- 単純 ensemble では解けない区間がある
- Working Note の「低周波トレンド／モード誤収束」と整合
- 不確実性の高い区間の明示が Working Note 基準とも一致
