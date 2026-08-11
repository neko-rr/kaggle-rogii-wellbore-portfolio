# CHK-253 — fault-jump / teleport screen（NO-GO）

> date: 2026-07-28  
> layer: 上流 · mid-bank hard20 proxy  
> baseline soft@T0.15 ≈ **17.236** · oracle ≈ **12.881**

## 結果

| spec | soft Δ | oracle Δ | frac_hit | 判定 |
|---|---:|---:|---:|---|
| jump_pn05（112@pn0.005 + 16@pn0.05） | **−0.12** | +0.01 | 0.30→0.35 | tip未達 |
| jump_pn02 | **−0.15** | +0.17 | 0.30 | tip未達 |
| teleport_sparse（±20/±40 ls） | **−4.38** | **+3.30** | 0.30 | **P2**（oracle↑ tip↓） |

## 判定

**rejected** · tip soft ≥+0.15 なし · tip-cv GPU **skip**  
teleport は典型 P2（1b1eba53 oracle 改善でも tip 悪化）。

## 成果物

- `exp/work/wave21-upstream-mid/run_chk253_fault_jump_screen.py`
- `chk253-partial-summaries.json`
