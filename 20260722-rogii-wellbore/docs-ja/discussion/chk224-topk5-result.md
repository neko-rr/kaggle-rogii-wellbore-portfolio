# CHK-224 結果 — tip-cv T=0.15 + topk5

> date: 2026-07-27 · GPU · 提出なし

## 1 行

**NO-GO。** tip-cv **49.526**（vs 29.899 大幅悪化）。局所 PF の topk5 は tip selector 面に移植不可。

## 判定

topk 選択の tip 面再発明禁止。E2E 作らない。
