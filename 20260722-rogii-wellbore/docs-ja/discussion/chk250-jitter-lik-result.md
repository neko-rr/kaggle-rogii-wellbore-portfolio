# CHK-250 結果 — jitter/低信頼 GR 区間の lik ダウンウェイト

> date: 2026-07-28 · local mid-bank · **提出なし** · ≠F018 CF切替

## 判定

**NO-GO**（GPU tip-cv へ進めない）

横坑 GR rolling-std が高い区間の照合重みを下げ、`lik += α·z(-stable_rmse)`。

| face | Δ vs T0.15 |
|---|---:|
| α1 · win31 · p2 | **−0.190** |
| α1 · win63 | −0.257 |
| α2+ | −0.88〜−1.29 |

## 含意

- 低信頼区間の後段ダウンウェイトは tip soft を悪化。
- 本波では閉じる（PF 内部への移植もしない）。

出典: `exp/work/wave21-upstream-mid/chk250-jitter-lik-report.json`
