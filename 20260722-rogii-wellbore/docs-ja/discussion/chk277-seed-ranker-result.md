# CHK-277 結果 — シード・ランカー（ridge LOO）（2026-07-29）

> action: **T3** · Kaggle CPU Ver1 · **提出なし**（CHK-276 と同一 kernel）  
> kernel: [`kazeneko77/chk276-277-joint-cpu`](https://www.kaggle.com/code/kazeneko77/chk276-277-joint-cpu)  
> harvest: [`kernels-output-chk276-277/`](../../exp/work/wave23-ceiling-bridge/kernels-output-chk276-277/)  
> JSON: [`chk277-report.json`](../../exp/work/wave23-ceiling-bridge/chk277-report.json)

## 1行方針

**NO-GO。** tip-bank シード特徴→ridge LOO でも tip soft 未達。最良は単純 **argmax_ll**（Δ **−1.16**）で、ランカー（top1/topk5/score-soft）はそれより悪い。

## 集計（hard20 · tip = 17.236）

| rule | pooled | Δ vs tip | frac_improved |
|---|---:|---:|---:|
| argmax_ll（最良） | 18.396 | **−1.16** | 0.35 |
| ranker_score_soft | 18.569 | −1.33 | 0.45 |
| ranker_top1 | 18.804 | −1.57 | 0.35 |
| ranker_topk5_mean | 19.151 | −1.92 | 0.30 |

- mean score↔oracle corr ≈ **0.38**（弱い）
- frac_pick_oracle（top1 が oracle）: **0.05**
- tip-cv / 昇格: **不可** · sample60 未実施（hard20 全滅のため不要）

## 判定

| 項目 | 値 |
|---|---|
| policy | **NO-GO** |
| 含意 | ラベル無し特徴の簡易ランカーでは順位付け失敗（CHK-279）を解けない |
| 次 | **OPS-FINAL2** · CHK-281（spr12 同型）も見込み薄 |

## Explicit Stop

- tip-bank シード特徴 → ridge/LOO ランカーで tip soft 置換の言い換え禁止（**F032**）
- argmax_ll / soft 混ぜの再スイープは F027/F023 継続
