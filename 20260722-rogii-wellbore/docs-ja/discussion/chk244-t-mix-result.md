# CHK-244 結果 — T0.15×T0.5 soft mix（同一候補バンク）

> date: 2026-07-28 · local mid-bank · **提出なし**

## 判定

**NO-GO**（GPU tip-cv へ進めない）

| face | pooled RMSE | Δ vs T0.15 |
|---|---:|---:|
| T0.15（基準） | 17.588 | 0.000 |
| T0.5 | 19.017 | −1.429 |
| mix 0.7@0.15 + 0.3@0.5 | 17.887 | −0.299 |
| mix 0.5 / 0.5 | 18.150 | −0.562 |

最良でも **−0.30**。採択閾値（screen +0.15 / tip-cv +0.30）未達。

## 含意

- 同一バンク上の温度混合は tip 面を悪化させる（P1 の T=0.15 単体が正）。
- FINAL 同士ブレンド禁止（Explicit Stop）とも整合。再試行しない。

出典: `exp/work/wave21-upstream-mid/chk-mid-batch-report.json`
