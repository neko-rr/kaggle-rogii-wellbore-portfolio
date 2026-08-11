# train/test 同 ID 時の train TVT 利用 — 732917

> Topic ID: **732917**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732917  
> 投稿者: **imnot xuanan**  
> 投稿日時: **2026/08/05 04:00** UTC  
> 最新コメント: **Ayush Khaire · 2026/08/05 06:50** UTC  
> 票/コメ: **0 / 1**  
> 原文: `docs-en/discussion/732917-refresh-20260806-raw.md`  
> 関連: [729837 train-copy](729837-train-copy-overlap.md)

## 要約

test 井 ID が train と一致する場合、**提供されている train の TVT ラベルを予測に使ってよいか**（hidden target ではない · 賞対象か）を Host に確認。公開 NB でその実装がある、という指摘。

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Ayush Khaire** | 2026/08/05 06:50 | 不明 · 自分は使っていない · **同名でも内部パターンが違う可能性** |

**Host 回答: なし**（08-06 CLI 時点）

## 示唆

| 判断 | 内容 |
|---|---|
| **高（リスク）** | hidden 重複コピー系は [729837](729837-train-copy-overlap.md) で Tucker が否定寄り · 本スレ **Host 無回答** · 賞金/medal ルートでは **使わない**方針維持 |
| Active | **不要** · 自チーム未採用で正しい |
