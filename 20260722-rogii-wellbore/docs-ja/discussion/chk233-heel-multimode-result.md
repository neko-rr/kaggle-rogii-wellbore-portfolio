# CHK-233 — heel 錨定 / 多峰 init（2026-07-28）

> action: T3 · ローカル PF T0.15 screen（207 PF + ls_offset）· **GPU tip-cv なし** · 提出なし  
> 作業: [`run_chk233_v2.py`](../../exp/work/wave21-upstream-mid/run_chk233_v2.py)  
> JSON: [`chk233-heel-multimode-report.json`](../../exp/work/wave21-upstream-mid/chk233-heel-multimode-report.json)

## 判定

**NO-GO** — heel 緊密 init / ±5 三峰 / heel-scan 2mode はいずれも tip 代理面を悪化。命中はわずかに上がるが tip に載らない。

## 結果（hard20）

| 設定 | oracle | hit≤4.5 | s8@T0.15 | vs base |
|---|---:|---:|---:|---:|
| **baseline spr4.5** | **12.881** | 0.30 | **17.588** | 0 |
| heel_tight spr1.5（最良） | 13.094 | **0.40** | 19.188 | **−1.60** |
| heel_tight spr2.5 | 14.077 | 0.35 | 20.658 | −3.07 |
| trimodal ±5 | 15.770 | 0.35 | 20.742 | −3.15 |
| heel_scan 2mode | 14.395 | 0.35 | 21.550 | −3.96 |

## 方針1行

heel 錨定・小さな多峰は **hit↑ ≠ tip↑**（P2）。上流の init いじりは 232/246/233 で閉じた。次は **遠MD提案強化（238）** または **粗→細 2段（241）**。

## Explicit Stop

- heel_tight spr≤2.5 の tip 面再試行禁止（233）
- trimodal ±5 / heel-scan 2mode の tip 面再スイープ禁止（233）
- ±15 二峰は従来どおり禁止（246）
