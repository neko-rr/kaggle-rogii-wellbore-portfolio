# SUB-4–7 · VISUALS Public 確定分析（2026-07-25）

> purpose: tip 中間面昇格実験の LB 読み · Final2 への含意  
> 数値の正: [`exp/exp-index.md`](../exp/exp-index.md) · 台帳: [`cv-public-private-forecast.md`](cv-public-private-forecast.md)

---

## スコア一覧（有効提出 · 低いほど良い）

| 順位 | ID | Public | tip(6.569)比 | Best(6.524)比 | 面 |
|---|---|---|---|---|---|
| 1 | **Best top-repro** | **6.524** | −0.045 | — | Contact-Gated final |
| 2 | tip smoke | **6.569** | — | +0.045 | tip final（mpkg005+BH） |
| 3 | VISUALS Ver2 | **6.581** | +0.012 | +0.057 | 別NB（Frontier Lab） |
| 4 | SUB-2 BH-off | **6.599** | +0.030 | +0.075 | hedge OFF |
| 5 | SUB-6 gated_020 | **6.621** | +0.052 | +0.097 | modelpkg 昇格 0.020 |
| 6 | SUB-5 pre-BH | **6.653** | +0.084 | +0.129 | branch-hedge 前 |
| 7 | SUB-4 gated_010 | **6.718** | +0.149 | +0.194 | modelpkg 昇格 0.010 |
| — | SUB-7 mpkg-only | **20.067** | +13.5 | — | package 単体 · 壊滅 |
| — | SUB-3 mpkg020 copy | Scoring Error | — | — | F005 |

---

## 読み（Kaggler）

1. **Public Best は不動 6.524**。中間面昇格はいずれも tip final より悪化 → **枠2は Best 維持**。
2. **model-package を最終に寄せるほど悪い:** tip final ≪ gated_020(6.621) < gated_010(6.718) ≪ only(20.067)。  
   tip 既定の弱い package ブレンド（`*_005`）が Public に最適側。**パッケージ強化・単独化は禁止帯。**
3. **BH / hedge を外すと悪化:** pre-BH 6.653 · BH-off 6.599。SUB-2 と整合。hedge は残す。
4. **E2E 昇格は F005 回避として技術的に成功**したが、**LB 仮説としては全滅**（実験枠の価値は「最終面を触るな」の証拠）。
5. VISUALS 6.581 は tip 近傍で Best 未達。枠2候補にならない。

---

## Final 2（更新後）

| 枠 | 仮 | 根拠 |
|---|---|---|
| 枠1 | tip Trust CV（T2 **8.33**） | 自測 Trust 最良 · B1 F014 |
| 枠2 | **Best Public 6.524** | 全有効提出の最小 |

---

## 台帳

言い換え再提出禁止のため **F015**（tip 中間面 / mpkg 単独の最終化）を `improvement-loop-failures.json` に追記。
