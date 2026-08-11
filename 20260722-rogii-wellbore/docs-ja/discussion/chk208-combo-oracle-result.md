# CHK-208 結果 — init_spr=9 × seeds=256（seed-oracle）

> 作業: [`exp/work/wave20-upstream/`](../../exp/work/wave20-upstream/) · ローカル CPU · 提出なし

## 1 行

**PASS。** 結合 **init_spr9×seeds256** で hard20 seed-oracle **12.88 → 11.63**（Δ **+1.25**）。  
単独最良 init_spr9（+0.94）を **+0.30** 上回る。

## 数値

| config | pooled oracle | Δ vs baseline |
|---|---:|---:|
| baseline 128×500 | 12.881 | 0 |
| init_spr_9 | 11.936 | +0.945 |
| seeds_256 | 12.350 | +0.531 |
| **init_spr9_seeds256** | **11.633** | **+1.248** |

## 次

tip CFG へ combo を載せる screen は、**CHK-206 の発見（下記）**を踏まえ **selector 面強制**で行う（phys 面では init_spr が原理的に見えない）。
