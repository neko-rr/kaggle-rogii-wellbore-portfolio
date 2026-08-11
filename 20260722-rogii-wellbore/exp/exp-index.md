# exp-index — rogii-wellbore

> type: experiment-index  
> updated: 2026-08-06（**Private 確定 · 振り返りは `retro/`**）  
> participant: Kazeneko

**SSOT:** 本ファイルの「現在地」が Best / 主成果物 / 次アクションの **唯一の正**（コンペ中ログ）。  
**コンペ終了 → 終了後の分析は [`../retro/retro-index.md`](../retro/retro-index.md)** · 自チーム詳細 [`../retro/retro-private.md`](../retro/retro-private.md)。  
`experiment-checklist.md`・`AGENTS.md`·`cursor.md` にスコアを再掲しない（リンクのみ）。Rule: `kaggle-exp-ssot`。  
**GPU↔CPU:** [`latest/session-bridge-cpu-to-gpu-2026-08-05.md`](latest/session-bridge-cpu-to-gpu-2026-08-05.md)。  
**L 法則:** [`latest/l-improvement-laws-2026-08-05.md`](latest/l-improvement-laws-2026-08-05.md)。  
**終了 CHK 保管:** [`checklist-archive.md`](checklist-archive.md)。

---

## 現在地

| 項目 | 値 |
|---|---|
| Public LB Best | **6.190**（farvol · **#143**）· 618c 6.231 · 558b 6.238 · **660 6.239** · tip 6.269 · **711 6.359 NO** · **641 6.472** · **666 6.509** · **710ssot 6.613** · **702 7.394** |
| Private LB | **9.142 · #594 / 6125**（666 · CLI 2026-08-08）· [`../retro/retro-private.md`](../retro/retro-private.md) |
| 主成果物 | **Final2:** 枠1 Trust **666**（priv 9.142）· 枠2 Public **farvol**（priv 9.453） |
| 主戦略 | **締切済** · 新規 submit なし · F043–F046 閉 · L retrain dual **全 NOGO** |
| 次アクション | **実験停止** · 終了後分析 [`../retro/retro-index.md`](../retro/retro-index.md) · 任意で解法分析 |

---

## Final2（凍結）

| 枠 | 提出面 | Public | Private | ref |
|---|---|---:|---:|---|
| **1 Trust** | **666** mid+α0.35 residual | 6.509 | **9.142**（Final 採用） | 55247672 |
| **2 Public** | **farvol** tip×thin | **6.190** | 9.453 | 55148128 |
| pair | tipdist_AB **1.950** · OK_diverse | — | — | [final2-ops](latest/final2-ops-20260805.md) |

---

## L1 dual 梯子（終了 · hard Δpool 正=悪化）

| rank | CHK | 機構 | hard Δ | 状態 |
|---:|---|---|---:|---|
| 1 最良失敗 | **781** | residual-path soft L\* | **+0.44** | NOGO · F046 · [report](work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md) |
| 2 | **688** | baseline retrain | **+0.52** | NOGO |
| 3 | **804** | known×Q4 weight | **+0.74** | NOGO · F044 |
| 4 | **802** | MD-Q4 行 weight | **+1.79** | NOGO · E2E ABORT · F044 |
| 5 | **782** | resid-drag weight | **+3.81** | NOGO · F044 |
| 6 | **761** | fold-driver weight | **+4.01** | NOGO · F044 |
| 7 最悪 | **784** | Huber loss FAST2 | **+6.27** | NOGO · F045 · [ops](latest/ops-chk784-dual-nogo-2026-08-05.md) |

Trust residual 頭は **faces 041247 / 666 α0.35**（pool **10.094**）。新 L で抜いて dual GO した面は **0**。

---

## まず読む（主要のみ）

| 目的 | ファイル |
|---|---|
| **終了後の正（分析）** | [`../retro/retro-index.md`](../retro/retro-index.md) |
| **L dual 法則** | [`latest/l-improvement-laws-2026-08-05.md`](latest/l-improvement-laws-2026-08-05.md) |
| **工程内比較** | [`within-stage-comparisons.md`](within-stage-comparisons.md) |
| **終了 CHK archive** | [`checklist-archive.md`](checklist-archive.md) |
| **学習 / 推論 / 表** | `exp-train.md` · `exp-infer.md` · `hyperparameter-table.md` |
| **Final2** | [`latest/final2-ops-20260805.md`](latest/final2-ops-20260805.md) |
| faces residual SSOT | `work/colab-final-t2/runs/20260804-041247/faces/` |

---

## 直近の重要メモ

- 2026-08-06 **コンペ終了:** 実験更新のみ · 新規 train/submit **なし**
- 2026-08-05/06 **L1 最終:** 781 path **NOGO** hard+0.44 · 784 Huber **NOGO** hard+6.27 · 777 reg↑ **未 dual / 締切停止**
- 2026-08-05 **F044 weight** · **F043 α** · **F015 生 mid/L** · tip⊕ 強 すべて閉
- Final2: **666 + farvol** · 自動差替なし · [deadline](latest/ops-deadline-submit-gate-2026-08-05.md)

---

## 次アクション

- [x] Final2 LOCK 666×farvol
- [x] L1 dual 系（688/761/782/804/802/781/784）**NOGO 記録完了**
- [x] 提出ゲート 新規 0
- [x] **post-comp:** `retro/` 本格起動
- [x] **Private CLI:** #596 / 9.142（666）
- [x] **上位解法:** [`../retro/retro-solutions.md`](../retro/retro-solutions.md)（**08-10 追記済**）
- [ ] （任意）公式メダル UI · knowledge promote · weight DS

### exp フェーズ移行（終了後）

| ルール | 内容 |
|---|---|
| **フリーズ** | `exp-train.md` · `exp-intel.md` は原則追記しない |
| **例外** | Private 確定値のみ `exp-infer.md` に事実として追記可 |
| **新規分析** | 考察・shake-up·上位解法はすべて `retro/` |
