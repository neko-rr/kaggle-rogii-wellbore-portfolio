# 自動研究エージェントの限界 — 733099

> Topic ID: **733099**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733099  
> 投稿者: **Just A game on your lips**  
> 投稿日時: **2026/08/05 20:18** UTC  
> 最新コメント: **Tucker Arrants · 2026/08/05 20:29** UTC  
> 票/コメ: **1 / 3**  
> 原文: `docs-en/discussion/733099-refresh-20260806-raw.md`

## 要約

1週間 **自動 research-agent** pipeline。初期 **CV〜6.2 / LB 8.x**。  
最終 24h は人手で方向を誘導（epoch · optimizer · 数学修正等）→ **CV〜6.8 / LB〜6.0** · **全 200 井で 4–5 分**（サブミッション全体も同程度、との返答）。

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| SireeshLimbu | 2026/08/05 20:25 | 4–5 分は提出パイプライン全体か？（自分は ~8.5h） |
| 著者 | 2026/08/05 20:27 | 200 wells + Kaggle full submission も 4–5 min |
| **Tucker** | 2026/08/05 20:29 | 井を画像扱いなら **モデル 1 本あたり ~200 forward** で速くて当然 |

## 示唆

| 判断 | 内容 |
|---|---|
| 中 | 自動探索単体は **exploitation 不足** · 人手ガイドが効く、という一般論（自運用は既に checklist 型） |
| 運用 | 提出 runtime はアーキにより **数分〜9h** までばらつく（[732422](error/732422-private-lb-9h-runtime.md) · [732903](732903-inference-time-cpu.md)） |
| Active | **不要** |
