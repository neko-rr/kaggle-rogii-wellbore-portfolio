# Write-UP: Anchors, GR Alignment, and Guarded Geosteering

> Topic ID: **717445** · **FOYSAL** · **2026/07/01** · 票 7  
> Writeup: https://www.kaggle.com/writeups/foysalemonshanto/rogii-wellbore-prediction-anchors-gr-alignment  
> 原文: `docs-en/discussion/717445-writeup-anchors-GR-alignment-guarded.md`

## 要約

Working Note: last-known TVT アンカーの強さ、GR/typewell 整合の効く場所、素朴 slope 外挿・無ガード GR matching の失敗、**guarded** contact/geosteering。

| 誰 | 内容 |
|---|---|
| Georgy | guarded 境界が測定側と一致。ガード幅を「どこでも探索」にしない |
| FOYSAL | ガード幅は train-tail EDA 制約（詳細は writeup） |

## 示唆

無制限マッチ禁止。探索幅に物理/EDA ガードを置く（B2/B3 と整合）。
