# Notebook Threw Exception（732296）

> Topic ID: **732296**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732296  
> 投稿者: **Mahboob Biswas**  
> 投稿日時: **2026/08/02** UTC  
> 最新コメント: **Tiago / Mahboob · 2026/08/03** UTC  
> 原文: `docs-en/discussion/732296-refresh-20260804-raw.md`

## 要約

提出ノートが連続で Exception。Kaggle メッセージどおり hidden は公開データとサイズ・内容が違う可能性あり。Host/Staff をメンション。

## コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **OzanM.** | 2026/08/02 12:01 | Submit は未知の test で遅いことがある · **GPU で提出 NB を使う**提案 |
| **Mahboob**（返信） | 2026/08/02 14:40 | GPU でも提出時のみ落ちる · 内部問題を疑う |
| **Ayush Khaire** | 2026/08/03 00:47 | 自分は **train フォルダだけ**を誤って使っていた · 直して治った、との自己報告 |
| **Tiago Soares** | 2026/08/03 11:08 | 同じ · private 側のエラーが見えない |
| **Mahboob**（続） | 2026/08/03 11:40 | **`assert len(sample_sub) == 14151` を submit 時に入れると落ちる**（sample 行数のハードコード） |
| **Tiago** | 2026/08/03 11:46 | それは未使用 · private run のエラーメッセージの見方を質問 |

## 自チームへの示唆

| 判断 | 内容 |
|---|---|
| 既知 | 729554 と同型（3偽井ログ ≠ hidden） |
| **運用強化** | sample 行数・`14151` の assert / 固定は **提出コード禁止**（hidden ≫ sample） |
| 関連 | [729554](729554-notebook-threw-exception.md) · 9h 全 test [732422](732422-private-lb-9h-runtime.md) |
| CHK | **不要** |
