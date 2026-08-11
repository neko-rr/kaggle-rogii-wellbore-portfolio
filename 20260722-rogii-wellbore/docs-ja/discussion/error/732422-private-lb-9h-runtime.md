# Private LB 再採点にも 9h 制限は掛かるか（732422）

> Topic ID: **732422**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732422  
> 投稿者: **daulettoibazar**  
> 投稿日時: **2026/08/02** UTC  
> 最新コメント: **Andrey Chankin · 2026/08/02 20:04** UTC（+3）  
> 原文: `docs-en/discussion/732422-refresh-20260803-raw.md`  
> 関連 SSOT: [`../../conditions.md`](../../conditions.md) · [`../../submission-rules.md`](../../submission-rules.md)

## 要約

Rules の Notebook 実行上限 **9 hours** が、提出時の Public 採点だけか、**Private 再採点（Final 後）にも適用**されるかが不明、という質問。  
OP は「評価データの 26% で既に約 6 時間」と報告し、rescore 時の見込みを確認したい、と述べている。

## コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Andrey Chankin** | 2026/08/02 20:04 | **9h は全 test（public+private）に対して**。Private 結果は **隠されているだけ**（別枠で長時間走るわけではない） |

## スコア・運用にとって重要か

| 判断 | 内容 |
|---|---|
| **高（運用）** | 提出 NB の wall-clock は **見えている Public 断片ではなく全 hidden test** 基準で見積もる |
| 自チーム | tip / Trust 系が十分余裕なら変更不要。長時間学習・重いゲートを **提出同一 NB** に載せる設計は危険 |
| Active CHK | **不要**（方針変更ではなく制約の明文化） |

## 効果が薄い／注意

- 「Public 26% で 6h」→ 単純外挿すると全量で 9h を超えうる。OP 側は提出失敗リスクが高い  
- Exception / タイムアウトと混同しない（別スレ: [732296](732296-notebook-threw-exception.md) · [729554](729554-notebook-threw-exception.md)）
