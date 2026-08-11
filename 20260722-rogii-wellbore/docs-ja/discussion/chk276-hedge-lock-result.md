# CHK-276 結果 — hedge 前確定／後差替（2026-07-29）

> action: **T3** · Kaggle CPU Ver1 · **提出なし**  
> kernel: [`kazeneko77/chk276-277-joint-cpu`](https://www.kaggle.com/code/kazeneko77/chk276-277-joint-cpu)  
> harvest: [`kernels-output-chk276-277/`](../../exp/work/wave23-ceiling-bridge/kernels-output-chk276-277/)  
> JSON: [`chk276-report.json`](../../exp/work/wave23-ceiling-bridge/chk276-report.json)

## 1行方針

**NO-GO。** 天井面（tip_nearest / cas_argmax）を hedge 前に確定しても tip soft を超えられない。hedge（h=0.35）はさらに悪化。最良は tip soft そのもの（Δ **0.00**）のみ。

## 前提

- 272/275 skipped → PASS 天井セレクタ無し
- 診断面: `tip_nearest` · `cas_argmax` · tip soft lock · attractor hedge
- ≠259（temp-diversity のみの attractor）

## 集計（hard20 · tip soft = 17.236）

| face | pooled | Δ vs tip |
|---|---:|---:|
| tip_soft_lock（最良） | 17.236 | **0.00** |
| tip_nearest_lock | 17.592 | −0.36 |
| hedge_then_swap_nearest | 17.592 | −0.36 |
| tip_soft_then_hedge | 19.159 | −1.92 |
| cas_soft_lock | 20.528 | −3.29 |
| cas_argmax_lock | 20.938 | −3.70 |
| cas_argmax_then_hedge | 21.756 | −4.52 |

- adopt 候補（tip 超え）: **0**
- tip-cv / 昇格: **不可**

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** |
| 含意 | hedge の前後で天井面を固定しても断絶は解けない。hedge 自体が tip 面を壊す |
| 次 | **OPS-FINAL2**（Wave-23 橋渡し打ち切り） |

## Explicit Stop

- ceiling face × attractor hedge lock/swap の言い換え再スイープ禁止（**F031**）
- ≠259 は維持（本 CHK は lock/swap 構造の失敗）
