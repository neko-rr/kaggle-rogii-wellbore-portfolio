# Submission format error on valid file（730092）

> Topic ID: **730092**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/730092  
> 投稿者: **Anjana mohan**  
> 投稿日時: **2026/07/27** UTC  
> 最新コメント: **Sandy · 2026/07/29 05:01** UTC  
> 原文: `docs-en/discussion/730092-refresh-20260729-raw.md`

## 要約

手元では `submission.csv` が正しいように見える（**14151行** · `id,tvt` · NaNなし · Float64 · IDs が sample と一致）が、Submission format error。サンプル行の TVT 値が ~11747 と異常に大きく見える点も注意。

## コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Sandy** | 2026/07/29 05:01 | 過去の成功提出と比較 · **ハードコード禁止** · Submit 時は `test/` が実データに差し替わる |

## 自チームへの示唆

| 判断 | 内容 |
|---|---|
| 既知 | 729554 / sample_submission 依存と同じ系統の罠 |
| 運用 | 提出は hidden の id 集合に追従 · パス/行数の固定禁止 |
| CHK | **不要** |

## 効果が薄い／注意

- 「sample と一致」検証は **ダミー3井規模**の話になりやすい（EDA #4）
