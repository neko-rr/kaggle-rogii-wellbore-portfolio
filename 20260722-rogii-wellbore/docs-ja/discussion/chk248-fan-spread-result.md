# CHK-248 結果 — 扇状提案分散（spr 4.5+8 結合）

> date: 2026-07-28 · local hard20 · **提出なし** · ≠243

## 判定

**NO-GO**

| spec | s5@T0.15 | Δ tip | oracle Δ |
|---|---:|---:|---:|
| baseline | 17.236 | 0 | 0 |
| fan 64@4.5 + 64@8 | 19.500 | **−2.26** | −1.21 |

## 含意

- 扇状 spr 拡大は tip・oracle とも悪化（232 mix と同系）。
- 本波の扇状 init は閉じる。

出典: `chk248-partial-summaries.json`
