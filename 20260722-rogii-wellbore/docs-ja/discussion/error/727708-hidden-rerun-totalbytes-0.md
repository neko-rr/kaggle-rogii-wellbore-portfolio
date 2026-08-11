# Hidden rerun fails with totalBytes=0

> Topic ID: **727708**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/727708  
> 投稿者: Sailor Ren  
> 投稿日時: **2026/07/20** UTC  
> 原文: `docs-en/discussion/error/727708-hidden-rerun-totalBytes-0.md`

## 要約

- Save Version（可視 test）成功 · `submission.csv` 14151 行 · 形式 OK
- 軽い last-value 制御は Public **15.883** で成功
- 重い Pipeline（大容量外部 DS · 多モデル · 全 train 特徴 materialize · 提出前フル OOF）は hidden rerun で **totalBytes=0** / unhandled error

推定: **OOM** または少数 well 前提の edge（既知 TVT_input 行数・typewell 欠落）。

## 対策

- 提出パスは推論のみ・メモリピークを hidden 規模で検証
- 外部巨大 artifact 依存を見直す
- last-value 等の最小提出で経路確認してから本提出

## 効果が薄かった構成

- 提出時にフル OOF + 巨大特徴表を同時に載せる
