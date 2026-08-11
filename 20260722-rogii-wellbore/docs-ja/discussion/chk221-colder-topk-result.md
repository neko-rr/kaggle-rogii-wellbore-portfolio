# CHK-221 結果 — colder T / top-k / scale（局所 PF）

> date: 2026-07-26 · ローカル CPU · **提出なし** · action **T2**  
> 数値: [`chk221-report.json`](../../exp/work/wave20-upstream/chk221-report.json)

## 1 行

**3軸とも PASS（≥+0.30 vs soft T0.3）。** 最良は **topk5（17.13）** ≈ **sc2@T0.3（17.21）** ≈ **T=0.15（17.24）**。  
tip 面への最短追試は既存ノブ **LIK_TEMP=0.15**（CHK-222）。topk はコード改変が要るため後段。

## pooled s5（hard20 · tip同型 PF spr4.5）

| 条件 | RMSE | vs T0.3 |
|---|---:|---:|
| **topk5** | **17.135** | **+0.713** |
| sc2 @ T0.3 | 17.206 | +0.642 |
| **T=0.15** | **17.236** | **+0.612** |
| T=0.20 | 17.406 | +0.441 |
| T=0.25 | 17.633 | +0.214 |
| T=0.30（ref） | 17.847 | 0 |
| T=0.50 | 18.405 | −0.558 |
| topk1（argmax） | 18.396 | −0.548 |

## 判定

| 仮説 | 判定 |
|---|---|
| T&lt;0.3 が ≥+0.30 | **PASS（T=0.15）** |
| top-k | **PASS（k=5）** · k=1 は悪化 |
| scale↓ @T0.3 | **PASS（sc2）** · tip面は主に scale8 経路なので **T 追試を優先** |

## 次

1. **CHK-219** tip-cv T=0.3 harvest（実行中）  
2. **CHK-222** tip-cv **T=0.15**（GPU 枠空き次第 · vs 211 / vs T0.5 / vs 219）  
3. topk5 は tip 改変が要る → 222 後に検討  

## Explicit Stop

- 局所 17.x を tip-cv 33 と混同しない  
- seeds384 再スイープ禁止（plan）  
- entropy / tip_std 温度ゲート再発明禁止  
