# Score Without Tabular Models

> Topic ID: **717573**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/717573  
> 投稿者: **k256.dev** · **2026/07/02** UTC · 票 18  
> 最新重要: **2026/07/17–18**（Angus Chang 物理モデル）  
> 原文: `docs-en/discussion/717573-score-without-tabular-models.md`

## 要約

公開 NB は tabular ベースが多い。k256: 非tabular 単体 **7.098**、tabular ベスト **6.798**（当時）。のち両方 **CV 5.x** 到達と報告。詳細は非開示。強調: **入力特徴そのもの**が本体。

## 重要コメント

| 日時 UTC | 誰 | 内容 |
|---|---|---|
| 2026/07/17 | **Angus Chang** [+7] | 初提出・**純物理**単体: **CV 6.85 / LB 6.577**。詳細非公開。CV は well-group · 隠れ suffix 再現 · per-point RMSE |
| 2026/07/02 | **Tucker** [+4] | 非tabular で CV **5台**可 |
| 2026/07/05 | **k256** [+9] | tabular でもさらに良くなる実験結果に驚き。**特徴が仕事をする** |
| 2026/07/10 | k256 | tabular 上限感: LB≈6.0（CV7.0）言及。非tabular でも LB&lt;6 可 |
| 2026/07/13 | radiant-allomancer | 上位への粗い質問（多くは downvote） |

## スコア向上への示唆

- tabular / 物理 / 系列 NN いずれも天井候補 — **表現と検証**が勝負  
- 物理単体でも LB 6.5 台は到達例あり（初提出）  
- 公開 tabular フォークの複製だけでは足りない  

## 効果が薄かった取り組み

- 公開 NB 複製の乱造（投稿者も指摘）
