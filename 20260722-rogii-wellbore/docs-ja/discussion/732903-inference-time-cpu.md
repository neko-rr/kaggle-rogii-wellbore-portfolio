# 推論時間のばらつき（CPU プラットフォーム）— 732903

> Topic ID: **732903**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732903  
> 投稿者: **Andrey Chankin**  
> 投稿日時: **2026/08/05 02:21** UTC  
> 最新コメント: **Andrey · 2026/08/05 14:44** UTC  
> 票/コメ: **3 / 5**  
> 原文: `docs-en/discussion/732903-refresh-20260806-raw.md`  
> 関連: [732422 9h=全 test](error/732422-private-lb-9h-runtime.md)

## 要約

同じコード（**3 井**スモーク）で runtime が **X → 1.8X → 再実行で X → 1.6X** と揺れる。CPU 種別の差？ と質問。  
**Private 200 井**見積もりに使えない、との訴え。

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Ryan Holbrook（Kaggle Staff）** | 2026/08/05 13:13 | 公式: 通常 NB の **CPU プラットフォーム（Skylake/Broadwell/AMD 等）は可変**。**提出/Code Comp 実行は別扱い**（CLI 途中切れ · 原文 Doc 参照） |
| ImperfectKitto | 2026/08/05 03:27 | LB probing 対策では、との推測 |
| Tiago Soares | 2026/08/05 11:24 | Private 200 井 · 学習中も glitch で落ちる報告 |

## 示唆

| 判断 | 内容 |
|---|---|
| **高（運用）** | 通常 run の壁時計だけで **9h 安全マージンを切らない**（Staff 確認） |
| 既存 | [732422](error/732422-private-lb-9h-runtime.md): 9h は **public+private 全 test** 前提 |
| Active | **不要** |
