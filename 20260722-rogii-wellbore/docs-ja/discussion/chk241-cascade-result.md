# CHK-241 — 粗→細 2段 generator（2026-07-28）

> action: T3 · ローカル · GPU なし · 提出なし  
> JSON: [`chk241-cascade-report.json`](../../exp/work/wave21-upstream-mid/chk241-cascade-report.json)

## 判定

**NO-GO** — cascade は **oracle を大きく改善**（top2: 12.88→**8.44**）するが tip 代理面は悪化。P2 の典型例。

## 結果

| 設定 | oracle | hit | s8@T0.15 | vs tip |
|---|---:|---:|---:|---:|
| baseline | 12.881 | 0.30 | **17.588** | 0 |
| concat 64@9+64@1.5（tip最良） | 12.337 | 0.35 | 19.651 | **−2.06** |
| cascade_top3 | 10.257 | 0.35 | 19.726 | −2.14 |
| cascade_top2（oracle最良） | **8.437** | 0.35 | 20.554 | −2.97 |

## 方針1行

粗→細は **候補集合の天井を上げる**が、現行 T0.15 soft-lik では拾えない。上流単独採用は不可。中間の選択改善（244/245/237）が前提。次は中間バッチへ。
