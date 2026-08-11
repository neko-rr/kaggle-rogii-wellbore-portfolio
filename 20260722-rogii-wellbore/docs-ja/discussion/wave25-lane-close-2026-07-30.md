# Wave-25 閉鎖 — 難井専用レーン（2026-07-30）

## 結論

**難井専用レーンは A（定義）以外全滅。実験を止め OPS-FINAL2 に集中する。**

| 帯 | 結果 |
|---|---|
| A 297–299 | **PASS**（ゲート・契約・地図） |
| B 300–305 | **F036** · 既存バンク再スコア壊滅 |
| D 312–315 | NO-GO · 温度 oracle 天井 +0.14≪0.30 |
| C 306–310 | **全滅** · 最良Δ0 · [`306`](chk306-309-dynamics-result.md) · [`310`](chk310-segment-pf-result.md) |
| E 316–320 | **skipped**（upstream無し）· 320=Final維持文書のみ |

## Final（変更なし）

| 枠 | 中身 |
|---|---|
| 枠1 | **SUB-14** |
| 枠2 | Public1（SUB-20≡14） |

UI操作はユーザー。Agent は提出しない。

## 残す資産

- `chk297-gate-frozen.json` · `chk298-contract.json` · `chk299-hardwell-map.csv`
- F036（バンク再スコア禁止）

## やらない

- F036/F033–F035 言い換え
- 全体平均だけの「微改善」で tip-cv / 提出
