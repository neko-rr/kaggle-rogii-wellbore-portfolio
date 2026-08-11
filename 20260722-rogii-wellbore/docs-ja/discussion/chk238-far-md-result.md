# CHK-238 — 遠MD 提案密度強化（2026-07-28）

> action: T3 · ローカル PF · **GPU tip-cv なし** · 提出なし  
> 作業: [`run_chk238_far_md_screen.py`](../../exp/work/wave21-upstream-mid/run_chk238_far_md_screen.py)  
> JSON: [`chk238-far-md-report.json`](../../exp/work/wave21-upstream-mid/chk238-far-md-report.json)

## 判定

**NO-GO** — 遠半区間の PN 増強は tip 代理面を大幅悪化。遠MD層の微改善では足りない。

## 結果

| 設定 | oracle | hit | s8@T0.15 | far RMSE | vs tip |
|---|---:|---:|---:|---:|---:|
| **baseline** | 12.881 | 0.30 | **17.588** | 14.324 | 0 |
| far_pn×1.5 | 13.728 | 0.30 | 21.223 | 15.948 | **−3.64** |
| far_pn×2（最良） | 12.654 | 0.35 | 20.818 | **13.951** | **−3.23** |
| far_vn / both | — | — | — | — | **cancelled** |

## 方針1行

遠MDで PN を厚くすると tip 面が壊れる。F019/F020 とは別経路だが上流の「遠だけノイズ増」は閉じる。次は **CHK-241（粗→細 2段）** または中間 **249**。

## Explicit Stop

- 遠MD PN/VN 倍率の tip 面再スイープ禁止（238）
