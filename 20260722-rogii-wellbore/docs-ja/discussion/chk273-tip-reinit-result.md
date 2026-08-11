# CHK-273 結果 — cascade→tip PF 再初期化（2026-07-29）

> action: **T3** · Kaggle CPU Ver1 · **提出なし**  
> kernel: [`kazeneko77/chk273-tip-reinit-cpu`](https://www.kaggle.com/code/kazeneko77/chk273-tip-reinit-cpu)  
> harvest: [`chk273-kaggle-harvest/`](../../exp/work/wave23-ceiling-bridge/chk273-kaggle-harvest/)  
> JSON: [`chk273-report.json`](../../exp/work/wave23-ceiling-bridge/chk273-report.json)

## 1行方針

**NO-GO。** cascade モードの `ls_offset` で tip PF を再初期化しても tip soft は改善しない（最良 Δ **−1.04**）。tip-cv へ進めない。

## 集計（hard20 · tip soft s5@T0.15 基準 = 17.236）

| variant | pooled | Δ vs tip | 改善井率 |
|---|---:|---:|---:|
| reinit_maxll_pick（最良） | 18.272 | **−1.04** | 0.40 |
| reinit_top1 | 18.275 | −1.04 | 0.40 |
| reinit_top3 | 19.823 | −2.59 | 0.30 |
| reinit_off_blend | 20.595 | −3.36 | 0.20 |
| reinit_top2 | 21.033 | −3.80 | 0.35 |
| cascade_soft（F027対照） | 20.528 | −3.29 | 0.40 |

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** |
| tip-cv | 不可 |
| 含意 | 天井モード位置へ tip を寄せても選ぶ人/生成器の断絶は解けない |
| 次 | **CHK-274**（バンク専用校正）または **OPS-FINAL2**（打ち切り検討） |

## Explicit Stop

- cascade `ls_offset` → tip PF 再初期化の言い換え再スイープ禁止（**F028**）
- cascade soft を tip 面に載せる再実行禁止（F027）
