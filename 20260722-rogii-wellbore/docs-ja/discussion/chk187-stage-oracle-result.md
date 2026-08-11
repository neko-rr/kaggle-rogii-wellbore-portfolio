# CHK-187 結果 — tip 段・中間面 oracle（2026-07-26）

> 作業: [`exp/work/chk187-stage-oracle/`](../../exp/work/chk187-stage-oracle/)  
> 計画: [`chk186-plan`](chk186-generator-ceiling-plan.md) §CHK-187  
> **F015:** 中間面の提出昇格は **禁止**（Public 済み）

## 1 行結論

**提出可能な「中間面 / SOFT」のラベル oracle は tip FINAL に対し +0.14 級のみ（CHK-185 と同型）。**  
大きな gap に見える数字は **PF seed-oracle 混入**であり、提出段ではない。  
→ **昇格しない** · **OPS-FINAL2** · CHK-188/189 は触らない。

---

## 何を測ったか

| プール | 内容 | ラベル |
|---|---|---|
| **A soft** | tip FINAL + Wave-13/14 soft grafts | T2 train |
| **A PF** | tip FINAL + CHK-186 seed-oracle / pf_scale_3 | T2 train |
| **B knobs** | tip hard20 + BH / NW_N-BH | hard20 |
| **C test** | tip-fork `before_*` / gold / mpkg vs FINAL | 無し（多様性のみ） |

---

## 数値

| プール | selected | oracle | gap | 読み |
|---|---:|---:|---:|---|
| **A soft-only** | ≈8.06* | ≈7.92* | **+0.14** | tip が最良 **64/80** |
| **A + PF seed** | ≈8.06* | ≈5.28* | +2.77 | seed-oracle が 32井で勝つ · **提出不可** |
| **B hard knobs** | 14.84* | 14.84* | **0** | BH ノブは tip 未越え（CHK-185 C2 再確認） |
| **B + PF seed** | 14.84* | 9.14* | +5.70 | 難井で PF 最良シードに余地 · それでも 4.8 帯外 |

\* eq-well pooled（井等重み）。行重みの tip T2 FINAL は 8.330（CHK-186 と一致）。

SOFT oracle 選出: tip 64 · portable 8 · selfdev8 7 · gated_s05 1（CHK-185 B と一致）。

---

## Kaggler 解釈

1. **中間面を最終にする余地はない（F015 再確認）**  
   Public: pre-BH 6.653 / mpkg 系悪化。ラベルでも soft gap +0.14 のみ。

2. **「oracle が大きい」は PF シードの話**  
   CHK-186 と同じ。ラベル付き最良シードは診断用であり、submission 面ではない。

3. **次**  
   - OPS-FINAL2（枠1 tip Trust / 枠2 Public Best）  
   - SUB-8/9 Public 待ち（OPS-LB-89）  
   - CHK-188/189 自動開始なし

---

## 成果物

- [`chk187-report.json`](../../exp/work/chk187-stage-oracle/chk187-report.json)
- `chk187-per-well-A_t2_stages.csv` · `chk187-per-well-B_hard20_stages.csv`
- **実測×oracle まとめ:** [`intermediate-improvement-ledger`](intermediate-improvement-ledger-2026-07-26.md) · [`actual-vs-oracle-table.json`](../../exp/work/chk187-stage-oracle/actual-vs-oracle-table.json)
