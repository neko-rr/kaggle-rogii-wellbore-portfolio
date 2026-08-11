# Welcome to ROGII - Wellbore Geology Prediction!

> Topic ID: **697416**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/697416  
> 投稿者: **Igor Kuvaev**（Competition Host）  
> 投稿日時: **2026/05/06** UTC  
> 重要コメント最終: **2026/07/24** UTC（Antek）/ 実質重要: **2026/07/13** BIT_Guber · Host 主要返信 **2026/06/09**  
> 票: 36 · コメント: 17  
> 原文: `docs-en/discussion/Competition-Host_697416-Welcome-to-ROGII.md`

## 要約

- データは現代の水平掘削の典型（軌道 + GR）。熟練者なら解釈可能
- **データ同梱 PPTX を強く推奨**（水平井解釈の要点）
- 手動ジオステアリング動画あり（リンクは一時 private → Host が **2026/06/09** 更新）

## Host 回答（重要）

| 日時 UTC | 質問 | Host 回答 |
|---|---|---|
| 2026/06/09 | StarSteer ソフト利用可？ | **No**。人手解釈で GR を TVT に投影するだけ。train で自作可能 |
| 2026/06/09 | PS 点以降の Typewell GR→TVT は DTW？ | **それがコンペの目的**（手法は教えない） |
| 2026/05/26 | チーム一部が賞金非適格 | María Cruz: 理由次第。制裁国ならその人除外し残りで分割、等 |

## 参加者メモ

- PatrickAIForFun（2026/05/27）: 手元 test は train の一部。真の hidden は提出後のみ — 周知確認
- **BIT_Guber（2026/07/13）**: 上位公開 NB が位置特徴に依存しがち、と指摘。位置のみで ~10.5 / 位置無し ~13 の自己報告。PPTX の位置開示への懸念（Host 未返答）
- Sharmi Nisha（2026/07/23）: full-well DTW vs PS 以降のみ — lateral 制限は期待に反して悪化した例。他者確認を募集（Host 未返答）
- Antek（2026/07/24）: 感謝のみ（戦略情報なし）

## スコア向上への示唆

- PPTX + png 断面を EDA の第一優先に
- StarSteer 依存は不要（Rules/Host とも整合）
- **位置のみパイプラインは Final 本命にしない**（BIT_Guber 報告 · Private リスク）
- 素朴 DTW の区間切りも盲信しない（Sharmi · 自チーム Stop 無制約 DTW と整合）
