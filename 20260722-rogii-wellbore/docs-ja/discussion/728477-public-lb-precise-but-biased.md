# The public LB is a precise ruler and a biased one

> Topic ID: **728477**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/728477  
> 投稿者: **souldrive** · **2026/07/23** UTC · 票 2 · コメント **2**（2026-07-28 時点）  
> 原文: `docs-en/discussion/728477-raw.md` · refresh: `728477-refresh-20260729-raw.md`  
> **実験統合先:** [`docs-ja/cv-lb-private-relation.md`](../cv-lb-private-relation.md)  
> **関連 NB:** [`georgy-noise-floor-lever-Ver`](../others-notebook/georgy-noise-floor-lever-Ver.md)

## 要約（必読）

一見矛盾する2主張が両立する:

1. Public は CV とほぼ完全に並ぶ  
2. Public は再提出で 0.2〜0.5 動くほどノイジー  

**切り分け:** Public ~26%（≈52 wells）は **毎回同じ固定集合**。オフセットは定数なので **同一集合上の比較**ではキャンセルされ、yu4u の5組で r≈0.999 · 傾き≈1 · オフセット≈+0.32 · 残差≈0.028。  
ノイズの主因は井の再抽選ではなく **自パイプラインの非決定性**（seed / GPU）。

**別質問「Private で持つか」** ではオフセットがキャンセルされず、SE(RMSE)≈ RMSE/√(2n) ≈0.78 ft（n=52, RMSE=8）級。well 内相関で実効 n はさらに小さい。

Tucker の「CV&lt;6 で相関消失」は、改善幅が seed バンド以下になり **分解能不足**になった読み。

## 投稿者の運用ルール

1. 同一 NB を2回出して **自 seed バンド**を測る  
2. CV 同士・LB 同士で比較（+0.3 オフセットは split の性質）  
3. **選抜は CV（773）**、LB は構造破綻の検知  
4. 密集帯の順位変動をスキルと読まない  

## コメント追記（2026-07-27〜28）

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Georgy Mamarin** | 2026/07/27 14:55 | 機構は認めるがスレ未決着。自アカウントで **無編集14回**再提出し seed 帯にサイズを付けた → NB [noise-floor](../others-notebook/georgy-noise-floor-lever-Ver.md)（σ≈0.03） |
| **souldrive** | 2026/07/28 10:41 | Georgy の「2回ではσ不足」を受け入れ、**4–5回分の再提出コストを払った**（本文は CLI で途中切れ · 詳細は Web 要確認） |
| **Georgy**（続） | 2026/07/30 09:28 | souldrive 最終段への返信（沈黙は最悪、と言う趣旨 · CLI 途中切れ）· **方針変更なし** |

## 自チームへの示唆

- tip smoke と Best の **0.05 差はバンド内**扱い（Georgy σ≈0.03 でさらに強化）  
- Final 2 は Public 上位2本ではなく **CV + 多様性**  
- 詳細: `cv-lb-private-relation.md` · refresh: [`20260729-refresh`](20260729-refresh.md)
