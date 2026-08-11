# How much should we trust the LB score?

> Topic ID: **704273**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/704273  
> 投稿者: （OP）· **2026/06/04** UTC · 票 18  
> 原文: `docs-en/discussion/704273-raw.md`

## 要約

train↔test シフトで CV–Public 差が最大 ~2。**向きは手法依存**:

- 空間・offset well: CV &lt; LB（Public が厳しい）  
- PF 系: CV &gt; LB（Public が甘い）  

OP / Tucker: 773 vs ~52 なので **健全な CV を優先**。大きなパイプライン変更のたびに CV–LB 相関は「リセット」される。

## 示唆

- tip/PF 系は Public が甘く見えやすい → Public 追い禁止と整合  
- 近傍・空間系は Public が厳しく出やすい → 悪化しても即破棄しない（CV を見る）
