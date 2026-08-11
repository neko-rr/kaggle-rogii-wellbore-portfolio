# experiment-checklist — rogii-wellbore

> phase: **COMP CLOSED · 実験停止 · 振り返りは retro/** · updated: 2026-08-06  
> **現在地:** [`exp-index.md`](exp-index.md) ← Best / Final2 / dual 梯子はここだけ  
> **終了後分析:** [`../retro/retro-index.md`](../retro/retro-index.md)  
> **終了 CHK:** [`checklist-archive.md`](checklist-archive.md)  
> **L 法則:** [`latest/l-improvement-laws-2026-08-05.md`](latest/l-improvement-laws-2026-08-05.md)  
> **工程内比較:** [`within-stage-comparisons.md`](within-stage-comparisons.md)  
> participant: Kazeneko · metric: **RMSE（低）**

---

## 実行制約（凍結）

| 項目 | 方針 |
|---|---|
| **実験** | **停止** · 新規 CHK / GPU train / dual 追加なし |
| **提出** | **なし** · Final UI = **666 + farvol** のみ |
| Final2 | **LOCK** 枠1=666 · 枠2=farvol |
| L 帯 | **F044 weight** · **F046 residual-path 781** · **F045 Huber 784** · α **F043** · 生 mid/L **F015** |

---

## Active（空）

> コンペ終了。作業キューは **なし**。結果は archive + exp-index。

| 優先 | ID | 状態 | メモ |
|---|---|---|---|
| — | — | — | （empty） |

---

## 終了時サマリ（再掲禁止 · リンクのみ）

| 区分 | 結果 | ref |
|---|---|---|
| Final2 | **666 + farvol** | [exp-index](exp-index.md) · [final2-ops](latest/final2-ops-20260805.md) |
| Public Best | farvol **6.190** | exp-index |
| Trust residual 頭 | faces **041247** · 666 α**0.35** pool **10.094** | within-stage |
| L1 dual 全敗梯子 | 781≺688≺804≺802≺782≺761≺**784** | [laws](latest/l-improvement-laws-2026-08-05.md) · archive |
| 777 reg↑ | body 作成済 · dual **未実施 · 締切停止** | [ops-777](latest/ops-chk777-regup-colab-2026-08-05.md) |

---

## all773 / GR

- GR 本命特徴 **禁止**（機器制限）  
- all773 CV: [chk-final-t2-all773-cv](latest/chk-final-t2-all773-cv-2026-08-05.md)
