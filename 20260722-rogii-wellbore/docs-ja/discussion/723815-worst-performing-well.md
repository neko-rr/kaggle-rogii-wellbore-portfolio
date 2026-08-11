# What is your worst performing well?

> Topic ID: **723815**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/723815  
> 投稿者: **Shrey Gandhi** · **2026/07/08** UTC · 票 16  
> 最新: **2026/07/16** UTC  
> 原文: `docs-en/discussion/723815-what-is-your-worst-performing-well.md`

## 要約

難井の RMSE 共有スレ。系列モデルは早期ドリフトが尾を引く。

## 共有された難井（抜粋）

| well | 報告 RMSE 例 | 誰 |
|---|---|---|
| **86454a6f** | 43.9 / 40.8 / 22.6 / 20.8 / 19 | 複数（頻出） |
| fb03ae90 | 38.3 / ~50 | k256 / Connor |
| 389ae58f | 31.8 / ~50 | k256 / Connor |
| 91db7070 | 29.3 | k256 |
| **4c2208f5** | 34.3 | Rishikesh（Shrey も悪い） |

## コメント要点

| 誰 | 内容 |
|---|---|
| Andrey | 大 TVT 動き井は単純手法がそこそこ。**前セグメント終端接続**は1ミスで井全体を壊し、平坦井にも波及 |
| Connor | 決定的解で ~50。GBT/UNet 残差はあまり効かず。**別アプローチの併用**が前進かも |
| Rishikesh | 大誤差井の **分類はできるが誤差の向きは未解決** |
| Shrey | 上位は NN 系の感触。自分は当面非学習ベース |

## スコア向上への示唆

1. 難井 ID を CV エラー分析の固定セットに  
2. 系列接続の失敗モード対策（リセット／ガード）  
3. 単一パイプラインで全井を無理に解かない（ルーティング）  

## 関連

- 711878 二峰 datum · 712037 ruler/wall
