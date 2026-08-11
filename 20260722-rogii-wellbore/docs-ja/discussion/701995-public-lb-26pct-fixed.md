# Is the public LB test set (26%) fixed?

> Topic ID: **701995**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/701995  
> 投稿者: **Alhasan Abdellatif** · **2026/05/20** UTC · 票 9  
> 原文: `docs-en/discussion/701995-raw.md`

## 要約

同一 Notebook 再提出で **~0.5 ft** 差が出る疑問。結論:

| 誰 | 内容 |
|---|---|
| **Chris Deotte** | **test データは変わらない**。スコア差は特徴生成等の確率性 |
| 複数 | Public 26% は固定。GPU/並列でも非決定性が残る |

公開 NB コピーでも提出者ごとに 9.7〜10.1 などばらつく報告あり。

## 示唆

- Public 揺れ ≠ スライス変更  
- seed 固定・同一 NB 2 提出でバンド測定（728477 と直結）
