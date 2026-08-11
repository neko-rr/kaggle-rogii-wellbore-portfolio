# CHK-249 結果 — Buda/強ピーク照合の尤度 soft 重み

> date: 2026-07-28 · local mid-bank · **提出なし** · ≠F003 tops独立

## 判定

**NO-GO**（GPU tip-cv へ進めない）

typewell GR 高勾配（急崖）近傍の照合 RMSE を標準化し、`lik += α·bonus` のあと soft T=0.15。

| face | pooled RMSE | Δ vs T0.15 |
|---|---:|---:|
| T0.15（本スクリプト） | 17.236 | 0.000 |
| α=1 · p=2 | 17.323 | **−0.088** |
| α=1 · p=3 | 17.351 | −0.115 |
| α=2 · p=2 | 18.041 | −0.805 |
| α=3 · p=2 | 18.320 | −1.084 |

最良でも負。急崖強調は tip 面の選択を悪化させる。

## 含意

- EDA#5 の直感は残すが、**現行 PF lik への後段加算**では通らない。
- 再試行するなら PF 内部の区間重み（本 CHK の別実装）だが、本波では閉じる。

出典: `exp/work/wave21-upstream-mid/chk249-buda-lik-report.json`
