# cv and lb correlations .....

> Topic ID: **701691**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/701691  
> 投稿者: **Gaurav Rawat** · **2026/05/19** UTC · 票 16 · コメント 16  
> 原文: `docs-en/discussion/701691-raw.md`

## 要約

早期の GroupKFold 表では CV 改善と LB 改善がおおむね同方向（例: CV 31→10 台、LB 35→9 台）。後半は逆転例が増える。

| 誰 | 日時 UTC | 内容 |
|---|---|---|
| **Tucker** | 2026/05/19 | GBDT: CV≈11 · LB≈9.6。ギャップ大だが **CV↑→LB↑ が安定** |
| **Tucker** | 2026/06/08 | LB ノイズ。CV +0.7 でも LB 悪化あり。CV≈8 で LB 6.6 のラッキー提出も |
| **Ruby** | 2026/06/08 | CV 6.74→LB 6.48 · CV 6.22→LB **7.18**（悪井支配の疑い） |

## 示唆

- 粗い改善期は CV–LB 同方向を期待してよい  
- 上位帯（CV&lt;7）では逆転を織り込み **Trust CV**  
- 詳細統合: [`../cv-lb-private-relation.md`](../cv-lb-private-relation.md)
