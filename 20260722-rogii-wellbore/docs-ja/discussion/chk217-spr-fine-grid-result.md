# CHK-217 結果 — init_spr 細格子 {10,11,13,14}

> date: 2026-07-26 · ローカル CPU · **提出なし**  
> 数値: [`chk217-report.json`](../../exp/work/wave20-upstream/chk217-report.json)  
> 基準: CHK-213 spr12 oracle **10.383**

## 1 行

**NO-GO · spr12 固定。** 細格子はいずれも spr12 に ≥0.30 で勝てず、ピークは **12 鋭峰**。

## ランキング（vs spr12）

| 設定 | oracle | vs spr12 |
|---|---:|---:|
| init_spr=13 | 12.108 | **−1.72** |
| init_spr=14 | 12.381 | −2.00 |
| init_spr=10 | 12.658 | −2.27 |
| init_spr=11 | 12.825 | −2.44 |
| **spr12（213）** | **10.383** | 0 |

## 判定

| 仮説 | 判定 |
|---|---|
| {10,11,13,14} が spr12 を ≥+0.30 | **NO-GO** |
| spr 軸の続き | **打ち切り（12 固定）** |

## Explicit Stop

- seeds384 / 細格子の再スイープ禁止
- tip CFG への spr 変更は 214 NO-GO で既に閉鎖
