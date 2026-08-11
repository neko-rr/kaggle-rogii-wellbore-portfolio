# OPS-LB-89 — SUB-8/9 Public 確定（2026-07-26）

> CLI: `competitions submissions` · COMPLETE

## 実測

| ID | ref | Public | tip 6.569 比 | Best旧 6.524 比 | 判断 |
|---|---|---:|---:|---:|---|
| **SUB-9 gated** `self_dev>8` f33-s08 | **54972467** | **6.484** | **−0.085** | **−0.040** | **新 Public Best** · 継続 GO |
| **SUB-8 SOFT** 全井 f33-s08 | **54970975** | **6.582** | **+0.013** | +0.058 | **診断打ち切り** · 全井 SOFT 再強化禁止（F020 強化） |

## 読み（優秀な Kaggler）

1. **ゲート仮説は Public でも正しい。** Trust CV（sample 悪化が SOFT より小）と Public の向きが一致。  
2. **全井 SOFT は Public でも微悪化。** CV の sample 警告どおり。再提出・強化しない。  
3. **Public Best 更新:** 6.524 → **6.484（SUB-9）**。旧 Best は多様性保険候補。  
4. **枠1（Trust CV）:** gated T2 **8.246** ≺ tip **8.33** → CV も gated 優位。枠1を tip 固定のままにしない根拠が揃った（ただし Private 26%/74% で揺れあり）。  
5. **Wave-13 A portable**（複合ゲート+s05）は未提出。SUB-9 より sample 安全側の候補 → CHK-184/172/178 で上積みを狙う価値あり。  
6. **CHK-188/189** は引き続き触らない（generator EV 小）。

## Final2 仮（更新）

| 枠 | 仮候補 | 理由 |
|---|---|---|
| **枠1 Trust** | **SUB-9 gated**（または portable 改良後に差替え） | T2 8.246 · Public も最良 |
| **枠2 Public / 保険** | **SUB-9** を主 · 第2に旧 Best **6.524**（別 CSV） | 同一提出を二重選択しても意味薄い → 揺れ保険 |

UI 確定はユーザー（OPS-FINAL2）。Agent は自動差し替えしない。

## 次

1. forecast / exp-index / exp-infer / checklist 同期（本ターン）  
2. **CHK-184**（farvol除外本採点）→ 承認後 **CHK-172/178**  
3. OPS-FINAL2 UI（締切前）
