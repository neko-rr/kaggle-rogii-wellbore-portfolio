# CHK-278 結果 — 温→冷焼なまし選択（2026-07-29）

> action: **T2** · Kaggle CPU Ver1 · **提出なし**  
> kernel: [`kazeneko77/chk278-anneal-select-cpu`](https://www.kaggle.com/code/kazeneko77/chk278-anneal-select-cpu)  
> harvest: [`chk278-kaggle-harvest/`](../../exp/work/wave23-ceiling-bridge/chk278-kaggle-harvest/)  
> JSON: [`chk278-report.json`](../../exp/work/wave23-ceiling-bridge/chk278-report.json)

## 1行方針

**NO-GO。** cascade 上の温→冷・段階刈り込みでも tip soft を超えられない（最良 Δ **−1.25**）。F027 対照（単発 T0.15）より改善もしない。

## 集計（hard20 · tip = 17.236）

| bank | schedule | pooled | Δ vs tip |
|---|---|---:|---:|
| near | anneal_frac（最良） | 18.484 | **−1.25** |
| near | F027 対照 T0.15 | 18.418 | −1.18 |
| full | anneal_* | ≈20.53–20.57 | ≈−3.3 |
| full | F027 対照 | 20.528 | −3.29 |

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** |
| tip-cv | 不可 |
| 含意 | 選び方を温冷スケジュールに変えても天井バンク→tip 面の断絶は解けない |
| 次 | **CHK-276**（hedge 前確定）または **OPS-FINAL2** 打ち切り |

## Explicit Stop

- cascade 温→冷焼なまし＋刈り込みの言い換え禁止（**F030**）
- 単発 T0.15（F027）· 単一点 (T,scale) フィット（F029）も継続禁止
