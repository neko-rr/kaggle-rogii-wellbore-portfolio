# Submission stuck in Scoring / timeout

> Topic ID: **728152**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/728152  
> 投稿者: Vignesh Prasad  
> 投稿日時: **2026/07/22** UTC  
> 最新コメント: **2026/07/22** UTC（PC Jimmmy）  
> 原文: `docs-en/discussion/error/728152-submission-stuck-scoring-timeout.md`

## 要約

Save/実行は約 15 分で成功し `submission.csv` も出るが、提出後 Scoring が 9h+ でタイムアウト。

## 原因の合意（コメント）

| 日時 UTC | 誰 | 内容 |
|---|---|---|
| 2026/07/22 | **Y. Kim** [+2] | 実行時間は **可視 3 wells** 基準。hidden ≈**200 wells** なら単純比例で **~100倍** → 時間超過 |
| 2026/07/22 | PC Jimmmy | 予測を多数 well で試してから提出せよ |

## 対策

- ローカル/Notebook で **数十〜200 wells 相当**の推論時間を測る
- 特徴生成の並列化・キャッシュ・OOF 全再計算を提出パスから外す

## スコア向上への示唆

- 「動く提出」≠「hidden で 9h 内」— kernels-runbook に時間見積を残す
