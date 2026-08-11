# 工程別 × 井別 有効化マップ

> **可視化（Canvas）:** [`pipeline-stage-well-effects.canvas.tsx`](<cursor-workspace>/canvases/pipeline-stage-well-effects.canvas.tsx)  
> **updated:** 2026-08-04 午後（**residual / Public 着弾 / 643 dump** を追記 · hard20・T2 本体は維持）  
> 意図: **上流→下流で何がどの井に効いたか**  
> **面を混ぜない:** hard20 = CHK-517（507 tip/mid）· T2 = run `20260803-114917` · Public = 診断提出スコア

---

## いまの工程ポジション（2026-08-04 セッション）

| 順 | 工程 | 状態 | メモ |
|---|---|---|---|
| S0 tip | 凍結 | Trust/Public 土台 · SUB-14 |
| S1–S2 | 規律 | 生 L/soft FINAL 禁止 · **合法残差のみ** |
| S3–S6 | **dump 中** | **CHK-643 Ver2 RUNNING** → harvest → **673 1工程** |
| S9 mid≡agree | actionable T2 **12.279** | 生 mid FINAL 禁止 · win77/hurt3 |
| S9 ゲート | HD/row 絞り | T2 では微害〜悪化 · Trust 枠で連打 STOP |
| S9 residual | **666 GO_e2e** | T2 **9.998** · tipdist **1.985** · help77 · 提出禁止（明示のみ） |
| B0 Public | **farvol 6.190** | 641 **6.472 NO-GO** · 664 完了 · 618c/558b/541 枠2NO |

グラフ・梯子: [`within-stage-comparisons.md`](../within-stage-comparisons.md)

---

## A. hard20（CHK-517 · 旧面）

| 順 | 工程 | 誰に効く | 指標 | 扱い |
|---|---|---|---:|---|
| 1 | **S0 tip** | 全井の土台 | Trust 29.899 | 防衛 |
| 2 | **S0+ selector** | pack / 易井信号 | pack ~23.5 | 信号 |
| — | S1–S2 | ゲート材料 | — | 生FINAL禁止 |
| 3 | **S3–S8 mid** | **11井**大改善 · **5井**悪化 · 4井≡tip | mid ~28.9 | 材料面 |
| 4 | **S9 row** | 行単位 | 28.901 | 対照（旧） |
| 5 | **S9 H-D** | 悪化井を tip 維持 | **28.283** | 当時の本命 · **Public 514 NO-GO** |
| 別 | **B0 SE** | Trust微改善 | 29.19 | Public無効 |

**mid 悪化 → H-D が tip 維持:** `7e721392` · `f88ddb26` · `fef8af96` · `2fd68f7b` · `94d813a4`  
**mid≡tip:** `57f05c51` · `206b6193` · `86454a6f` · `ba48188d`  
生データ: `exp/work/wave31-neural-proposal/out-517-wellslice-hg/chk517-per-well.csv`

---

## B. T2≈80井（run `20260803-114917`）

| 工程相当 | pooled | hard20平均（同面） | win/flat/hurt vs tip |
|---|---:|---:|---|
| S0 tip | **17.030** | 26.829 | — |
| S9 mid（≡agree） | **12.279** | 18.521 | **77 / 0 / 3** |
| S9 row / agree∧row | **12.331** | 18.538 | 74 / 2 / 4 |
| S9 H-D | **13.887** | 21.453 | 38 / 40 / 2 |
| S1 learned（診断·F015） | **6.806** | 7.640 | 77 / 0 / 3 |

**カバー注意:** S2–S6 個別面は **643 dump 待ち**。mid = before_hedge スタック代理。

### mid が効く井（Δ tip−mid 上位）

`5f4d2a52` · `1b1eba53` · `b3388334` · `f88ddb26` · `fef8af96` · `91db7070` · `206b6193` · `3e011332` · `86454a6f` · `389ae58f` …

### mid が悪化する井（T2 · 3井のみ · いずれも sample）

| well | tip | mid | Δ |
|---|---:|---:|---:|
| `70925e23` | 8.00 | 12.00 | −4.00 |
| `ab3ced07` | 5.82 | 7.59 | −1.77 |
| `19871e7f` | 1.82 | 3.01 | −1.19 |

詳細: [`t2-stage-well-map-2026-08-04.md`](t2-stage-well-map-2026-08-04.md)

---

## C. 合法残差 · tip⊕gate · Public（セッション · 面別）

> ここは **全井ヒートではない**（TEST 全体 / T2 pooled の工程読み）。井分解は 643 ladder 後に再投入。

| 工程 | 物差し | 数値 | 井に効くイメージ | 扱い |
|---|---|---|---|---|
| tip⊕agree∧row **541** | Public / tipdist | **6.256** / 0.278 | tip 近 · 薄い mid 注入 | 枠2NO · 再提出禁止 |
| tip⊕agree-only **558b** | Public / tipdist | **6.238** / 0.382 | 541より少し広い | 枠2NO · 再提出禁止 |
| tip⊕row **579** | Public | **6.277** | agree 無し → 悪化 | row STOP |
| tip⊕soft_diag **618c** | Public / tipdist | **6.231** / **11.9** | agree 行のみ soft · 距離大 | 枠2NO · Soft FINAL禁止 |
| mid+α0.30 L **641** | T2 / Public / tipdist | 10.309 / **6.472** / 1.743 | residual · T2 help77 | **Public NO-GO** · 再提出禁止 |
| mid+α0.35 L **666** | T2 / tipdist E2E | **9.998** / **1.985** | residual help77 | **GO_e2e** · 提出禁止 |
| mid+αL+βsoft **668** | T2 / tipdist | 10.206 / 2.552 | L+薄 soft · help71 **hurt9** | map dual · 提出禁止 |
| soft→mid **620** | T2 | **12.907** | mid を壊す | **NOGO 閉鎖** |
| farvol **B0** | Public | **6.190** | tip 薄 blend | **枠2 固定** |

**読み（工程×効果が「誰に」分かるか）**

1. **T2 mid** が井の勝ち分本体（B の 77井）。  
2. **ゲート絞り**は T2 で勝ち分を削る（HD）。  
3. **残差（L 方向）**は T2 で help **77/3** · Public は **641=6.472 で明確悪化** → Trust 専用。  
4. **668 soft 足し**は hurt **9** 井まで増える。  
5. **Public 薄い注入**は tip 近い agree が小さく効くが farvol 未達。  
6. **soft_diag Public 良い**は tipdist 大 → Private 禁止帯。  

**埋め済:** residual help/hurt · 641 Public · 拡張 Public 梯子（485/514等）  
**未埋め:** residual 井 id 別 RMSE（row faces 要）· S3–S6 井別（643 後）

---

## 関連

| 目的 | パス |
|---|---|
| 工程内比較 | [`../within-stage-comparisons.md`](../within-stage-comparisons.md) |
| 全実験マップ | [`full-pipeline-experiment-map-2026-08-03.md`](full-pipeline-experiment-map-2026-08-03.md) |
| T2 per-well 詳細 | [`t2-stage-well-map-2026-08-04.md`](t2-stage-well-map-2026-08-04.md) |
| checklist | [`../experiment-checklist.md`](../experiment-checklist.md) |
| | residual-t2井効果 | [`residual-t2-well-effects-2026-08-04.md`](residual-t2-well-effects-2026-08-04.md) |
| canvas | `pipeline-stage-well-effects` |
