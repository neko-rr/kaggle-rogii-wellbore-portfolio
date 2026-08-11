# Working Note Award - winners!!!

> Topic ID: **727171**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/727171  
> 投稿者: **Igor Kuvaev**（Competition Host / ROGII）  
> 投稿日時: **2026/07/18** UTC  
> 最新コメント: なし（コメント 0）  
> 票: 38  
> 原文: `docs-en/discussion/Competition-Host_727171-Working-Note-Award-winners.md`

## 要約

Host が Working Note Award の **2 受賞**を発表。スコア帯が近い候補が多く、決定要因は **coverage（探索の広さ）と honesty（失敗の開示）**。Public LB 過適合の指摘を含むノートを高く評価。

### 受賞

| 著者 | ノート題名 | Host が強調した点 |
|---|---|---|
| **@radiantallomancer** | *When Better CV Scores Worse* | **検証規律**。Local CV が Public と **逆相関**しても Public を追わず、shuffle / no-op / leave-spatial-out で主張を検証 |
| **@malyshevdanil** | *The Wiggle Is Free the Trend Is the Wall* | 問題分解。**高周波 wiggle は軌道由来で「無料」**、誤差は **低周波トレンド（datum/slope）**。単一 well の GR では datum が取れないことを数値で証明。失敗した GR matching も明記 |

## スコア向上への示唆

1. **低周波トレンド（datum / slope）** が本命。高周波の細かい合わせ込みだけでは足りない
2. **CV と Public LB の相関を盲信しない** — 空間リーク監査・shuffle 対照が必須
3. 受賞ノートを読む価値が高い（Host 曰く「実ジオステアリング pipeline のマニュアル」）

## 効果が薄かった取り組み（Host 講評から）

- Public LB 差分だけを根拠にした改善主張
- GR matching の表層的成功報告（否定実験の方が評価された）

## 次アクション（自チーム）

- [x] 低周波トレンド優先 · Public 追い禁止（既適用）
- [x] GR 機器制限と wiggle 無料を統合 → [`gr-instrument-limits-cv.md`](gr-instrument-limits-cv.md) · checklist Explicit Stop
- Working Note 原文は `exp-intel` 経由で参照

## 関連追記（2026-08-05）

コミュニティ: **GR 欠損多・水平揺動 = 機器制限**。本 Host 講評（wiggle 無料・低周波）と **矛盾しない**。  
実験キュー差し替えなし · GR 本命強化禁止。
