# CHK-232 — spr12以外 generator 多様性（2026-07-27）

> action: T3 · ローカル PF T0.15 screen · **GPU tip-cv なし** · 提出なし  
> 作業: [`run_chk232_diversity_screen.py`](../../exp/work/wave21-upstream-mid/run_chk232_diversity_screen.py)  
> JSON: [`chk232-diversity-screen-report.json`](../../exp/work/wave21-upstream-mid/chk232-diversity-screen-report.json)

## 判定

**NO-GO** — spr12 以外の多様性ノブは oracle/hit を少し上げても **tip 代理面（s8@T0.15）を悪化**させる。GPU tip-cv に進まない。

## 結果（hard20 · vs baseline spr4.5）

| 設定 | oracle | hit≤4.5 | s8@T0.15 | vs base T0.15 |
|---|---:|---:|---:|---:|
| **baseline spr4.5** | 12.881 | 0.30 | **17.588** | 0 |
| spr8（最良候補） | 11.922 | 0.35 | 18.100 | **−0.51** |
| mix 64@4.5+64@9 | 12.862 | 0.35 | 19.178 | −1.59 |
| spr9 | 11.936 | 0.35 | 21.211 | −3.62 |
| mix128 / dualseed | — | — | — | **cancelled**（既に経路なし） |

## 方針1行

spr8/9/mix は **命中↑・tip面↓**（P2 再確認）。上流の「散布幅いじり」は tip 面では閉じる。次は **CHK-233**（heel 錨定/多峰 init）または遠MD（238）/粗細2段（241）。

## Explicit Stop 追記

- spr8/9 を tip CFG に載せない（232）
- mix(4.5+9) の tip 面再スイープ禁止（232）
- spr12 は従来どおり禁止（214/217）
