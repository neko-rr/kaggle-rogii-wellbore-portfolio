# CHK-239 T4 診断 — 1b1eba53（216型）観測破綻?

> date: 2026-07-28 · **提出なし**

## 結論（修正）

**heel GR 観測は壊れていない。** corr≈0.83 · heel_gr_rmse は hard20 中央値付近。  
主因は **候補不足（oracle≈41.7）** と遠区間悪化（early soft 26.9 → late 43.8）。lik も最良シードを 57 位にしか置けないが、そもそも最良でも 41。

| 指標 | 1b1eba53 | 含意 |
|---|---:|---|
| heel_gr_corr | 0.83 | 観測 OK |
| oracle | 41.7 | hit 無 · B |
| soft−oracle | +3.5 | 選択より候補 |
| late/early soft | 43.8 / 26.9 | 遠MD崩壊 |

→ 「接触・heel 観測モデル直し」単独は期待薄。**井内 geometry / stretch / 接触 MD オフセット**の上流寄りが次。全体強制禁止。

出典: `chk239-obs-break-report.json`
