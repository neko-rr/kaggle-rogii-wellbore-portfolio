# CHK-285 結果 — heteroscedastic / 難井ゲート screen（2026-07-29）

> action: **T4**（screen · T3 連続 NO-GO 上限のため型を T4 に修正）· **提出なし**  
> 作業: [`run_chk285_hetero_lik_screen.py`](../../exp/work/wave24-generator-redesign/run_chk285_hetero_lik_screen.py)  
> JSON: [`chk285-report.json`](../../exp/work/wave24-generator-redesign/chk285-report.json)  
> 前提: CHK-284 NO-GO（全井 robust 置換禁止）

## 1行方針

**難井ゲート付き pf_ll×late_het 混合でも RF 改善率 27% で未達。** 観測尤度の後段いじりは Wave-24 A screen として打ち切り、**CHK-287（proposal 診断）** へ。

## 主結果

| 項目 | 値 |
|---|---:|
| RF 井 | 11 |
| RF 改善率 | **27.3%**（要≥60%） |
| pooled Δ | **+0.032**（非悪化は満たす） |
| gated 井 | 7 / 20 |
| 284 非依存 | true（ungated α=1 より良い） |
| acceptance | **FAIL** |

## 判定

| 項目 | 値 |
|---|---|
| verdict | **NO-GO** |
| next | **CHK-287** proposal innovation 診断 |

## Explicit Stop

- 後段 soft の難井ゲート言い換え再スイープ禁止（本結果で閉じる）
- GPU-A（286）は 284/285 PASS なしでは起動しない
