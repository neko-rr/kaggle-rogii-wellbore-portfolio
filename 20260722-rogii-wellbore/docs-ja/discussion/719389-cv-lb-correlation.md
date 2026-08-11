# Does CV correlate with LB?

> Topic ID: **719389**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/719389  
> 投稿者: **yuanzhe zhou** · **2026/07/04** UTC · 票 20  
> 重要コメント最終: **2026/07/08** UTC  
> 原文: `docs-en/discussion/719389-does-CV-correlate-with-LB.md`  
> **注意:** Georgy 長文は CLI 途中欠落あり

## 要約

公開高スコア NB は CV≈10 なのに LB≈7、という疑問。編集後の結論: **まず CV を目指す**。

## 重要コメント

| 日時 UTC | 誰 | 内容 |
|---|---|---|
| 2026/07/07 | **yu4u** [+18] | **trust-your-CV コンペ**。5fold×5seed 平均で改善だけ採用 |
| 2026/07/05 | **k256.dev** [+8] | 773 wells は **ある規則で2群**。LB は片方とよく相関。seed で 0.2–0.3 揺れ |
| 2026/07/05 | **Tucker** [+4] | CV が **6 未満**になると CV–LB 相関がほぼ消えた。それ以前はそこそこ |
| 2026/07/08 | Rishikesh | ~5.8 付近で同様 |
| 2026/07/04 | tennogh | LB はノイズ大（**~50 wells** vs CV 773）。公開 NB は LB 過適合気味 |
| 2026/07/05 | Georgy [+-14] | CV と Public LB は **異なる well 集合**。Public は hidden ~200 の友好スライス ~50（詳細 CLI 欠落） |

## スコア向上への示唆

1. 採用基準は **安定 CV**（multi-seed）  
2. LB 乱打より CV&lt;6 帯の手法改善  
3. CV–LB 乖離は「失敗」ではなく **Public が薄い**可能性  
4. k256 の「2群」は方位分割仮説（726465）と整合しうる  

## 効果が薄かった取り組み

- 公開 NB の CV≈10 / LB≈7 を真似た LB チューニング
