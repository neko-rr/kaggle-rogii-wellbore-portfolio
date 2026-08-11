# Problem Breakdown

> Topic ID: **708367**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/708367  
> 投稿者: **Tabish Shah Mohsin**（元 zacchaeus）· **2026/06/15** UTC · 票 **37**  
> 原文: `docs-en/discussion/708367-problem-breakdown.md`

## 要約

ジオステアリング入門スレ（水平井 = L プロファイル、TVT 一定を維持、Typewell = GR↔TVT ルックアップ）。

## 実務に効くコメント

| 日時 UTC | 誰 | 内容 |
|---|---|---|
| 2026/06/17 | Tabish [+3] | **最後の既知 TVT を提出 → Public LB 15.883**（anchor-hold 公式相当） |
| 2026/06/17 | **Shrey** [+6] | **GR センサが回転**している |
| 2026/06/19 | MY0705 / Tabish | FFT で低周波に回転成分。**denoise レバー**（のち Georgy が検証） |
| 2026/06/16 | Tabish | データ不整合リスト（急変 TVT · 空 Typewell 等）。**4c2208f5** 等 |
| 2026/06/15 | Tabish | Typewell は **単一 master の部分列グループ** |
| 2026/06/18 | Tabish [+4] | `|ASTNL|+TVT-|Z|` が well 内で一定 → グループ鍵 |
| 2026/06/21 | Patrick [+3] | TVT は層厚というより **参照地質境界までの垂直距離** |
| 2026/06/30 | Georgy | 誤差を heel オフセット + piecewise dip に分けてからモデル化 |

## スコア向上への示唆

1. ベースラインは **15.883** を必ず超える  
2. GR 回転 denoise を特徴/前処理候補に  
3. Typewell 共有構造をクラスタ特徴に  

## 関連

- 726751 anchor-hold ≈16.1 OOF
