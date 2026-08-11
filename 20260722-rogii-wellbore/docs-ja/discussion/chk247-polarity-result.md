# CHK-247 結果 — Typewell GR 極性反転候補

> date: 2026-07-28 · local hard20 · **提出なし**

## 判定

**NO-GO**

| spec | s5@T0.15 | Δ tip | oracle Δ | frac_hit |
|---|---:|---:|---:|---:|
| baseline | 17.236 | 0 | 0 | 0.30 |
| flip_half（64+64） | 37.794 | **−20.56** | −0.03 | 0.30 |

## 含意

- 極性混在は tip soft を破壊（誤候補に質量が流れる）。oracle/hit はほぼ不変。
- stretch 変形は未試行だが、極性だけでも明確 NO-GO → 本 CHK 閉じる。

出典: `chk247-partial-summaries.json`
