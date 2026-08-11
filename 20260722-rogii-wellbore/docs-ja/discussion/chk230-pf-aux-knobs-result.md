# CHK-230 結果 — 局所 PF gs/pn/particles @ T=0.15

> date: 2026-07-27 · ローカル CPU · 提出なし · elapsed ≈2.3h

**NO-GO。** 全補助ノブが base（gs1.3 / pn0.005 / p500）より悪い。

| label | pooled s8@T0.15 | Δ vs base |
|---|---:|---:|
| **base_gs1p3_pn005_p500** | **17.588** | 0 |
| gs1p45 | 17.815 | −0.23 |
| pn003 | 18.632 | −1.04 |
| pn008 | 20.281 | −2.69 |
| p350 | 20.912 | −3.32 |
| p700 | 20.953 | −3.37 |
| gs1p15 | 23.134 | −5.55 |
| gs1p0 | 27.963 | −10.38 |

acceptance（≥+0.30）未達。`pass_ge_0_30=false` · report: `exp/work/wave20-upstream/chk230-report.json`

**結論:** tip 同型 PF の gs/pn/particles は T=0.15 固定では動かさない。spr/init_spr 同様 **閉じる**。
