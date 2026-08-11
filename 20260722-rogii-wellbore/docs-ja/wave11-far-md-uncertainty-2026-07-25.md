# Wave-11 — tip 遠MD 自己線 damp（CHK-150/151 · 2026-07-25）

> ローカル CPU screen · Kaggle GPU smoke · **SUB-8 提出済（PENDING）**  
> 作業: [`exp/work/chk150-far-md-uncertainty/`](../exp/work/chk150-far-md-uncertainty/)  
> NB: `kazeneko77/tip-soft-selfline-f33s08` Ver1

## 1 行

**hard20 では tip 自己線が効くが、T2 sample を必ず悪化させる。** 厳格ゲートは空（**F020**）。弱い SOFT `f33-s08` のみ診断提出（SUB-8）· **枠1自動差し替え禁止**。

## 仮説と禁止帯

| 回避 | 内容 |
|---|---|
| F006 | last_known / CF への blend なし |
| F013 | 離散プロファイル切替なし |
| F019 | heel 既知区間の直線外挿なし（**tip 予測の自己線**のみ） |
| F020 | strength≥0.15 / sample 非悪化無視の再スイープ禁止 |

## 結果

| 段階 | 判定 | 要点 |
|---|---|---|
| hard20 screen | **PASS** | 最良攻撃的設定 far=0.50 s=0.25 · Δ**+1.11**（sample は別問題） |
| shrink / damp / md_ramp | **全滅** | 近MD平均への shrink は一貫悪化 |
| T2 厳格 | **NO-GO** | pooled+≥0.05 と sample 非悪化を両立できない |
| T2 SOFT `f33-s08` | **SOFT-PASS** | pool **8.261**（+0.069）· hard +0.194 · sample **−0.076** |
| CHK-151 Kaggle | **GO_SMOKE** | Ver1 COMPLETE · ≡local soft |
| SUB-8 | **PENDING** | ref **54970975** · Public 待ち |

## 採否（Final）

| 項目 | 判断 |
|---|---|
| 枠1 | **tip Trust CV のまま**（SOFT は診断） |
| 枠2 | **Public Best 6.524** |
| SOFT 昇格 | Public が出て tip(6.569) を明確に上回る場合のみ再検討 · 既定は不採用 |

## 次

1. SUB-8 Public 確定 → forecast / exp-infer 更新（OPS-SUB8-LB）
2. **OPS-FINAL2**（締切前 UI）
