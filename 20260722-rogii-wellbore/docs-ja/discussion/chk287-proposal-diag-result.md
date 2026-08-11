# CHK-287 結果 — proposal innovation 診断（2026-07-29）

> action: **T4** · ローカル（chk284-packs 再利用）· **提出なし**  
> 作業: [`run_chk287_proposal_diag.py`](../../exp/work/wave24-generator-redesign/run_chk287_proposal_diag.py)  
> JSON: [`chk287-report.json`](../../exp/work/wave24-generator-redesign/chk287-report.json)

## 1行方針

**単一の scale/方向バイアスは弱い。改修方向は `innovation_guided_residual_proposal`（CHK-288）に固定。**

## 集計（RF 11井中心）

| 指標 | 値 |
|---|---:|
| 遠MD bias（soft−oracle） | **+0.0017**（符号一貫 73%） |
| 近MD bias | −0.0026 |
| 全体 scale 比中央値 | **0.99** |
| 遠MD scale 比中央値 | **0.99** |
| innovation 符号一致率 | **81%** |

## 改修方向（1つ）

| 項目 | 値 |
|---|---|
| fix_direction | **innovation_guided_residual_proposal** |
| 意味 | 残差・局所勾配から次状態を提案（CHK-288）。PN/spr の無制約拡大はしない（F026） |

## 判定

| 項目 | 値 |
|---|---|
| verdict | **PASS** |
| next | **CHK-288** GPU-B（要 T3 gate · 現状 T3 streak=44 で要ユーザー Force または方針転換） |

## Explicit Stop

- spr/粒子数だけの拡散拡大に逃げない（F026）
- 観測後段いじり（284/285）へ戻らない
