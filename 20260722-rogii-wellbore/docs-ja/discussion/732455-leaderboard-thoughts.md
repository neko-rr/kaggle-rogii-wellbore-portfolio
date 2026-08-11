# Leaderboard thoughts — Public 密集帯と shake-up（732455）

> Topic ID: **732455**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732455  
> 投稿者: **Michael Timbs**  
> 投稿日時: **2026/08/03** UTC  
> 最新コメント: **Michael Timbs · 2026/08/04 03:11** UTC（Tucker 2026/08/04 への返信）  
> 票/コメ（08-05）: **20 / 9**（08-04 eve: 17/9 · **本文変化なし · 票のみ**）  
> 原文: `docs-en/discussion/732455-refresh-20260805-raw.md` · 旧 `...20260804-eve-raw.md`  
> 関連: [731550 Final2](731550-final-two-submissions-shakeup.md) · [cv-lb-private-relation](../cv-lb-private-relation.md) · Georgy [noise-floor](../others-notebook/georgy-noise-floor-lever-Ver.md) · [20260805-refresh](20260805-refresh.md)

## 要約

終盤参加の Michael の所感: 自分の OOF RMSE **≈7.1** から top が主張する **&lt;5** への道が見えない。  
一方 **Public 6.5–7.1 の大量クラスタ**は、公開 NB 由来が多く、自分の **OOF では ≈10** しか出ない → **約50井の Public 過適合**であり、Private では **≈9.5–10** へ落ちる、という予測。  
「上位数人は別物」・write-up への期待も述べている。

## コメント（重要者優先）

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Tony Li** | 2026/08/03 11:34（+11） | Public≈50井は **過適合しうる**が、終盤も **本物の信号を載せる**ことが多い、との両論 |
| **GG Ayo** | 2026/08/03 09:42（+3） | **5-fold · 773井** の pooled RMSE 表。fold0 ≈5.4–5.6 · fold2 ≈7.0–7.4 など **fold 間ギャップが大** |
| **Dylan Xue** | 2026/08/03 10:10（+2） | Public 50井が特定パターン/型を共有していないか疑問 |
| **Tucker Arrants** | **2026/08/04 01:38（+6）** | 計算コストは高いが、**モデルをスケールアップすると一貫して gains** があった |
| **Michael Timbs** | **2026/08/04 03:11（+1）** | 遅参で慎重にしすぎたかも · **現行 best の scale-up** を試す、と追随 |
| k256.dev / Dhir / ggyrssy | 2026/08/03 | 遅参・短検証で閉門が早い、など詰み共有（方針核ではない） |

## スコア・Final にとって重要か

| 判断 | 内容 |
|---|---|
| **高（方針追認）** | 「Public が良い公開フォーク密集帯」＝ **shake-up の主戦場**、というコミュニティ合意が明示された |
| **高** | GG Ayo の fold 分解は **単一 Public 点 ≠ 全井汎化** の実例。Trust CV / multi-seed の正当化 |
| **中（実装レーン）** | Tucker の scale-up 実測は **L 質改善 / 重い本流**の外部補強。**公開クローンの α いじりとは別物** |
| 自チーム | **変更不要**: 枠1 Trust CV · tip/Q0522 同家系 Final 不可 · Public は検査機（σ≈0.03） · 本命 **688 L** と整合 |
| Active CHK | **不要**（既方針の追認。新仮説を作らない）

## 効果が薄い／注意

- top 数名・真の &lt;5 経路は **write-up 待ち**（推測で真似ない）  
- OOF7 / Public6.5 を「まだ伸ばせる」根拠にしない · **機構なき LB 追い**を 732455 は戒めている  
- Tony の「信号もあり」は **枠2に Public を1本残す**ことと矛盾しない（全部 Public は非推奨）
