# CHK-320 / OPS-FINAL2 — Wave-25 mid-session note（2026-07-30）

> 自動提出しない。ユーザー起床後の判断用。

## 現時点の事実

| レーン | 状態 |
|---|---|
| A 定義/契約/地図 | **PASS**（297–299） |
| B 観測 + D 選択/後工程 | **全滅** · **F036** · oracle T 天井 Δ+0.14≪0.30 |
| C 動力学 GPU | **実行中** · `chk306-309-dynamics-gpu` · `chk310-segment-pf-gpu` |

## Final 枠（変更なし推奨 · C全滅時）

| 枠 | 中身 |
|---|---|
| 枠1 | **SUB-14**（CV1 · tip T0.15） |
| 枠2 | Public1（表示 SUB-20 ≡ SUB-14 SHA） |

詳細: [`ops-final2-prep`](../ops-final2-prep-2026-07-26.md)

## 分岐（C完了後）

| 結果 | 行動 |
|---|---|
| 306–310 いずれか tip soft ≥+0.30 | 305/311統合 → 318 tip-cv → 320 |
| Cも全滅 | **Wave-25 レーン縮小** · OPS-FINAL2 のみ · 実験停止 |
| 微小改善のみ（+0.05〜0.15） | tip-cvは見送り · Final差替しない |

## SHA / 提出

- F025: T∈{0.10,0.15,0.2,0.3} 最終CSV再提出禁止
- Agent は competitions submit しない
