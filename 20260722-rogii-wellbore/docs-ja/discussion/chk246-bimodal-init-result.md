# CHK-246 — ±15ft 二峰 init screen（2026-07-27）

> action: T3 · ローカル PF screen · **GPU tip-cv なし**（early-kill）· 提出なし  
> 作業: [`run_chk246_bimodal_init_screen.py`](../../exp/work/wave21-upstream-mid/run_chk246_bimodal_init_screen.py)

## 判定

**NO-GO** — 候補に ±15ft 二峰を載せると tip 代理面（s8@T0.15）が大幅悪化。命中も下がる。

## 結果

| 指標 | baseline | bimodal ±15 | Δ（+改善） |
|---|---:|---:|---:|
| pooled oracle | 12.881 | 12.864 | +0.017 |
| frac_hit≤4.5 | 0.30 | 0.25 | −0.05 |
| pooled s8@T0.15 | **17.588** | **21.393** | **−3.805** |

- early-kill 条件: T0.15 悪化 ≥1.0 → **成立** → GPU tip-cv スキップ
- oracle ほぼフラットだが selector 代理が壊れる（P2: oracle≠tip と同型）

## 方針1行

±15ft 二峰 **候補 init** は tip 面を壊す → **rejected**。FINAL hedge（F013）とは別経路だが結論は同方向。次は CHK-232（spr12以外の多様性）へ。

JSON: [`chk246-bimodal-screen-report.json`](../../exp/work/wave21-upstream-mid/chk246-bimodal-screen-report.json)
