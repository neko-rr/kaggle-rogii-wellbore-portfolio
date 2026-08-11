# OPS-LB — CHK-579 Public（tip⊕row P-495）

> date: 2026-08-04 · diagnostic once · **Final2 差替なし** · **再提出禁止**  
> ref: **55206184** · σ≈**0.03** · tip SUB-14 **6.269** · farvol0.95 **6.190**  
> branch SSOT: [`../work/wave31-neural-proposal/out-615-branch-table/chk615-579-branch.md`](../work/wave31-neural-proposal/out-615-branch-table/chk615-579-branch.md)

---

## 着弾

| ID | ref | Public | tipdist（TEST） | Trust hard20 | 判断 |
|---|---|---:|---:|---:|---|
| **579 tip⊕row495** | **55206184** | **6.277** | **0.907** | **26.768** | **枠2 NO-GO** · tip+0.008（σ内） |
| 515 tip⊕row468 | 55195981 | 6.249 | ≈2.12 | 28.901 | ≈tip · 改善主張なし |
| tip SUB-14 | 55006677 | **6.269** | 0 | 29.899 | Trust/Public基準 |
| farvol 0.95 | 55148128 | **6.190** | — | — | **枠2維持** |
| 514 H-D468 | 55195968 | 6.335 | ≈0.73 | 28.283 | Public NO-GO（既存） |

---

## 615 分岐適用

| 記号 | 値 |
|---|---:|
| `P579` | **6.277** |
| `Ptip` | 6.269 |
| `Pfar` | 6.190 |
| **Δ = P579 − Ptip** | **+0.008** |

```
|Δ| = 0.008 ≤ 0.08  →  ≈tip（ノイズ帯）枝
```

| 枝の指令 | 適用 |
|---|---|
| 枠2 = farvol 固定 | **YES**（599） |
| row495 Public 連打 STOP | **YES**（597） |
| Trust枠 558b/541/T2 継続 | **YES**（Trust≠Public で止めない） |
| Final2 自動差替 | **なし** |
| 再提出 | **禁止** |

---

## 判定（Kaggler）

| 仮説 | Public 結果 | 結論 |
|---|---|---|
| row P-495 が tip を明確に抜く（|Δ|≳0.15） | +0.008 | **反証 · 枠2候補にしない** |
| Trust 改善（26.768 ≪ tip 29.9）が Public に転移 | 6.277 ≳ 6.269 | **転移せず**（Trust≠Public） |
| tipdist 0.907 は 515 より薄いので安全 | tip より微悪 | tipdist 小≠Public勝ち（514教訓と整合） |
| 579 を枠2に差替 | farvol 6.190 に −0.087 | **禁止** |

### レーン別 verdict

| レーン | 主物差し | verdict |
|---|---|---|
| **Public 診断** | Public 6.277 | **≈tip ノイズ** · 改善なし · 枠2不適 |
| **Trust** | hard20 26.768 | **継続価値あり** · Public微悪で破棄しない |
| **Final2** | 枠2 farvol | **変更なし** |

---

## 読み（次手）

1. **row495 単独ゲートは Public で勝ちにならない** — 515（6.249）と同型の「壊さない程度」。P-495載荷でも Public 本命にはなれず。  
2. **630/631 適用** — 次の Public 診断1回があるなら **541（tipdist 0.278）優先**。row 連打しない。558b は第二候補。**618c は Public 主策にしない（636）**。  
3. **Trust 本線は分離** — 618c / T2 soft_diag（620）は Trust。Public 同時Paretoしない。  
4. **σ帯を採用根拠にしない** — +0.008 は「少し悪化したから Trust 全体 STOP」でも「ほぼ tip だから Final」でもない。

---

## 禁止（本結果で固定）

- 579 再提出・row495系 Public 連打  
- 579 を Final2 枠2へ自動差替  
- Public 微差で Trust 実験全体を停止  
- 618c を「579が惜しいから遠面で振りにいく」理由に Public へ載せること  

## 許可

- ユーザー明示時: **541（または 596 ルールの 558b）診断1回**  
- Trust: FINAL-T2 / soft_diag T2 / 618c 候補保持  

## SSOT

- [`exp-index.md`](../exp-index.md) · [`exp-infer.md`](../exp-infer.md) · [`experiment-checklist.md`](../experiment-checklist.md)  
- [`../docs-ja/cv-public-private-forecast.md`](../../docs-ja/cv-public-private-forecast.md)  
- 提出ログ: [`../../docs-ja/submission-validations/2026-08-03-chk579-submit.md`](../../docs-ja/submission-validations/2026-08-03-chk579-submit.md)
