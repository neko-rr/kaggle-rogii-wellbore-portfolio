# CHK-207 結果 — PF generator ノブ画面（hard20 seed-oracle）

> 作業: [`exp/work/wave20-upstream/`](../../exp/work/wave20-upstream/)  
> 目標: generator 候補集合の命中改善（tip FINAL は触らない）  
> 実行: ローカル CPU · 提出なし

## 1 行

**PASS。** 最良は **`init_spr=9.0`**（既定 4.5）で hard20 seed-oracle pooled **12.88 → 11.94**（Δ **+0.94**）。  
次点 **`seeds_256`**（Δ **+0.53**）。粒子増・`gs` 縮小・PN 増は悪化。

## 数値（hard20 · n=20）

| config | pooled seed-oracle | Δ vs baseline | hit≤6 |
|---|---:|---:|---:|
| baseline 128×500 gs×1.3 | **12.881** | 0 | 0.40 |
| particles_1500 | 13.420 | −0.54 | 0.35 |
| **seeds_256** | **12.350** | **+0.53** | 0.40 |
| gs_mult_1.0 | 21.892 | −9.01 | 0.45 |
| gs_mult_1.6 | 12.733 | +0.15 | 0.30 |
| pn_0.015 | 14.255 | −1.37 | 0.40 |
| **init_spr_9** | **11.936** | **+0.94** | 0.40 |

Acceptance: Δpool≥0.30 → **PASS**（init_spr_9 · seeds_256）

## 読み

1. **初期散らし `init_spr` を広げる**と難井の oracle が改善（generator 多様性が効く）。  
2. シード数 256 も同方向だが init_spr より弱い。  
3. 粒子 1500 / PN↑ / gs↓ は本格子では **命中を壊す**。  
4. hard oracle 11.9 でも 4.8 帯には遠い → 期待は「難井の候補品質」改善であり、銀帯への一発ではない。

## 次

- **CHK-206:** tip `lik_pf` / `run_particle_filter` の `init_spr` **4.5→9.0** を tip-cv hard20 full E2E で tip FINAL を確認（sample 非悪化）。  
- 副: seeds_256 は 206 が GO なら二次候補。  
- CHK-203 dump は解釈併用（進行中）。
