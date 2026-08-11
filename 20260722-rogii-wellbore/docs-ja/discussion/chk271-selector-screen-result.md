# CHK-271 結果 — ラベル無し選択ルール screen（2026-07-29）

> action: **T4** · Kaggle CPU Ver1 · **提出なし**  
> kernel: [`kazeneko77/chk271-selector-screen-cpu`](https://www.kaggle.com/code/kazeneko77/chk271-selector-screen-cpu)  
> harvest: [`exp/work/wave23-ceiling-bridge/chk271-kaggle-harvest/`](../../exp/work/wave23-ceiling-bridge/chk271-kaggle-harvest/)  
> JSON: [`chk271-report.json`](../../exp/work/wave23-ceiling-bridge/chk271-report.json) · 順位: [`chk271-rule-rank.csv`](../../exp/work/wave23-ceiling-bridge/chk271-rule-rank.csv)

## 1行方針

**ルール全滅（tip 超え 0件）。** 選び方変更（272/275）は期待薄 → **CHK-273（cascade モード→tip PF 再初期化）を本命**。

## 集計（hard20 · tip soft s5@T0.15 = 17.236）

| bank | 最良ルール | pooled | Δ vs tip | tip超え件数 |
|---|---|---:|---:|---:|
| full cascade | tip_nearest | 17.592 | **−0.36** | **0** |
| near k=1.0 | tip_nearest | 17.592 | **−0.36** | **0** |

- cascade oracle は **8.44**（天井あり）だが、どのラベル無しルールも tip 面に落とせない。
- soft T0.15（F027 対照）は full **20.53**（Δ−3.29）· near **18.42**（Δ−1.18）。
- argmax_ll / topk / GR窓 / median も全て tip より悪い。

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** · `WEAK/NO-GO→CHK-273 thicken` |
| tip-cv | 進めない（局所すら未達 · F023） |
| 272/275 | **薄く / skip 可**（271 全滅） |
| 次 | **CHK-273** |

## Explicit Stop

- 本 screen の「最良=tip_nearest」を tip-cv 採択しない（Δ負）
- mid-bank 代理採択禁止（F023）
- 現行 soft T0.15 を cascade にそのまま掛ける再実行禁止（F027 再確認）
