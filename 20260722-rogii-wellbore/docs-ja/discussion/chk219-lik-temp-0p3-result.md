# CHK-219 結果 — tip-cv selector T=0.3

> date: 2026-07-26 · Kaggle GPU · **提出なし** · action **T2**  
> preds: `exp/work/wave20-upstream/chk219-t0p3-out/tip_train_preds_selector.csv`  
> score: [`chk219-score.json`](../../exp/work/wave20-upstream/chk219-score.json)

## 1 行

**PASS。** tip-cv hard20 selector **RMSE 30.827** · vs 211 **+2.351** · vs T0.5(205) **+1.449**。  
局所 218 の示唆が tip 面でも再現。次は **222（T=0.15）** と、承認後 **220（Best tip+T0.3）**。

## 数値

| 面 | RMSE | Δ vs 本ラン |
|---|---:|---:|
| CHK-211 T=1 | 33.178 | +2.351 |
| CHK-205 T=0.5 | 32.276 | +1.449 |
| **CHK-219 T=0.3** | **30.827** | 0 |

acceptance: ≤33.178−0.30 → **達成** · beats T0.5 → **達成**

## 判定

| 仮説 | 判定 |
|---|---|
| tip-cv で T=0.3 ≻ 211 | **PASS** |
| tip-cv で T=0.3 ≻ T0.5 | **PASS** |

## 次

1. **CHK-222** tip-cv T=0.15（running）— さらに下がるか  
2. **CHK-220** Best tip + LIK_TEMP=0.3 E2E — **ユーザー承認後**（提出は別）  
3. Final 仮への載せ替えは Public 確定後のみ

## 井別メモ

- 改善 14/20 井 · 最大 `86454a6f` **+18.4**（60.2→41.8）
- 悪化最大 `91db7070` −1.20 · 難井 `1b1eba53` はほぼ不変（−0.05）

## Explicit Stop

- 本スコアを Public 期待に直結させない（Trust CV）  
- F015 · 乱獲提出禁止
