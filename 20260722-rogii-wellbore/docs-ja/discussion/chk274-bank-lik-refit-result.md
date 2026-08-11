# CHK-274 結果 — cascade バンク専用 soft(T,scale) 再フィット（2026-07-29）

> action: **T3** · Kaggle CPU Ver1 · **提出なし**  
> kernel: [`kazeneko77/chk274-bank-lik-refit-cpu`](https://www.kaggle.com/code/kazeneko77/chk274-bank-lik-refit-cpu)  
> harvest: [`chk274-kaggle-harvest/`](../../exp/work/wave23-ceiling-bridge/chk274-kaggle-harvest/)  
> JSON: [`chk274-report.json`](../../exp/work/wave23-ceiling-bridge/chk274-report.json)

## 1行方針

**NO-GO。** cascade バンク専用に (scale, T) を LOO 再フィットしても tip soft を超えられない（最良 LOO Δ **−1.39**）。≠F022（tip weight）・≠F027（固定 T0.15）でも効果なし。

## 集計（hard20 · tip = 17.236）

| bank | 指標 | pooled | Δ vs tip |
|---|---|---:|---:|
| near | LOO（主判定） | 18.627 | **−1.39** |
| near | in-sample 最良 s12·T2 | 18.326 | −1.09 |
| near | F027 対照 T0.15 | 18.418 | −1.18 |
| full | LOO | 20.850 | −3.61 |
| full | in-sample 最良 s5·T0.5 | 20.361 | −3.13 |

格子 32 点（scale∈{3,5,8,12} × T∈{0.05…2}）のいずれも tip 未達。

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** |
| tip-cv | 不可 |
| 次 | **CHK-278**（焼なまし）または **OPS-FINAL2**（Wave-23 大半 NO-GO） |

## Explicit Stop

- cascade バンク上の soft(T,scale) 再フィット言い換え禁止（**F029**）
- tip 既定 weight スイープは引き続き F022
- 固定 T0.15 を cascade に掛けるのは F027
