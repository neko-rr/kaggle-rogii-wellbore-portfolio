# CHK-222 結果 — tip-cv selector T=0.15

> date: 2026-07-26 · Kaggle GPU · **提出なし** · action **T2**  
> preds: `exp/work/wave20-upstream/chk222-t0p15-out/tip_train_preds_selector.csv`  
> score: [`chk222-score.json`](../../exp/work/wave20-upstream/chk222-score.json)

## 1 行

**PASS_best。** tip-cv hard20 **29.899** · vs 219(T0.3) **+0.928** · vs T0.5 **+2.377** · vs 211 **+3.279**。  
**tip 面の温度既定候補は T=0.15。** 次は承認後 Best tip + T=0.15 E2E。

## 数値

| 面 | RMSE | Δ vs 222 |
|---|---:|---:|
| CHK-211 T=1 | 33.178 | +3.279 |
| CHK-205 T=0.5 | 32.276 | +2.377 |
| CHK-219 T=0.3 | 30.827 | +0.928 |
| **CHK-222 T=0.15** | **29.899** | 0 |

## 判定

| 仮説 | 判定 |
|---|---|
| T=0.15 ≻ 211 / T0.5 / T0.3 | **PASS_best** |

## 次

1. **CHK-220b** Best tip + **LIK_TEMP=0.15** E2E（ユーザー承認 · 提出は別）  
2. T=0.10 など更なる冷却は **1 ノブだけ**・余裕時（過鋭化リスク）  
3. topk5 tip 改変は後段

## Explicit Stop

- Public 乱獲 · F015 · phys 14.87
