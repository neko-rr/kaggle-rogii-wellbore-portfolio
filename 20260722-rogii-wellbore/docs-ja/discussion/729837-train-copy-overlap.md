# Train-copy override — hidden に train 重複井はあるか？（729837）

> Topic ID: **729837**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/729837  
> 投稿者: **Vaibhav_486**  
> 投稿日時: **2026/07/26** UTC  
> 最新コメント: **PC Jimmmy · 2026/07/26 22:27** UTC  
> 原文: `docs-en/discussion/729837-refresh-20260727-raw.md`

## 要約

公開パイプライン多数に、**test 井 ID が train にもあるとき train ラベルをそのまま埋める postprocessor（train-copy override）** がある。発動すると予測ではなくラベル再生になる。質問: hidden に本当に train 重複があるか、Rules 上許容か。公開スコアの意味が歪む、と指摘。

## コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Tucker Arrants** | 2026/07/26 19:07 | **No, there is no overlap.** dummy test の動きを LLM が誤解した提案が、公開 fork 連鎖で継承された可能性が高い |
| **steubk** | 2026/07/26 19:07 | Data ページ参照 — 手元 `test/` は少数の example のみ（採点時は差し替え） |
| **PC Jimmmy** | 2026/07/26 22:27 | LLM は dummy test に弱い。ローカル train→predict 検証でも混同しやすい |

## スコア向上にとって重要か

| 判断 | 内容 |
|---|---|
| **高（否定証拠）** | hidden で train-copy は **効かない**（重複なし）。Public/手元で「当たった」経路を LB 本命と読まない |
| 既存整合 | Georgy 712037 の訂正（board は3井 train-copy ではない）· EDA #4 · wave10 CHK-141 警告と同型 |
| Active CHK | **不要**（既知リスクの再確認） |

## 効果が薄い／注意

- 公開 tip 家系に `run_guarded_overlap_override` / `has_train_copy` 監査があるのは事実。**手元3井では発火しうるが hidden では無意味**
- 「override を消して LB が動くか」は Public 26% チューニングになりやすい → Final 本命にしない
