# OPS-FINAL2 準備メモ（提出操作はユーザー）

> 更新: 2026-08-02 · **468 E2E GO（提出禁止）** · tip-cv 472/475 実行中 · 枠維持 · Agent は **competitions submit / 枠自動差替しない**  
> SSOT: [`exp-index`](../exp/exp-index.md) · [`comp-strategy`](comp-strategy.md) §Final2 · [`farvol-α`](../exp/latest/ops-lb-wave31-farvol-alpha-public-2026-08-01.md) · [`421`](../exp/work/wave31-nonssoft-blend/chk421-farvol-candidate-2026-08-01.md)  
> **別面門番注意:** [`gate-pearson-caveat`](gate-pearson-caveat.md)（生Pearson単独で切らない）  
> **コミュニティ追認（2026-08-02）:** Discussion [731550](discussion/731550-final-two-submissions-shakeup.md) — Tucker: Trust CV · 多数派: **best CV + best Public**（自チームと同型）

## 選抜ルール（Wave-30 閉鎖後）

| 枠 | 基準 | 差替ルール |
|---|---|---|
| **枠1** | **CV 1位**（Trust · tip-cv selector 面 / 自前 well-group） | CV 1位が変わったときだけ見直し · 現行 **SUB-14** 防衛 |
| **枠2** | **Public 1位**（表示） | Public1 追従はユーザー判断 · Soft-Preserve再学習による自動差替はしない（F041） |

B7/B8/B9 の言い換え再探索はしない（**F041**）。farvol 中間α（0.12–0.15）は Public NO-GO。

**別面 / 新FINAL を再検討する場合の門番（CHK-395以降）:**  
CF超え · sample非壊滅 · tip-cv改善 · **かつ** 生Pearsonだけでなく **誤差Pearson / 井中心化** を記録（[`gate-pearson-caveat`](gate-pearson-caveat.md)）。E2E自kernel（F005）· soft中間面提出禁止（F015）。

## 現時点の割当（候補メモ · 差替はユーザー）

| 枠 | 候補 | 根拠 |
|---|---|---|
| **枠1 CV1位** | **SUB-14** `55006677`（T=0.15） | tip-cv selector **29.899**（CHK-222 凍結） |
| **枠2 第1** | **farvol 0.95/0.05** `55148128` | 表示Public1 **6.190** · Δ≈1.2σ · [`farvol-α`](../exp/latest/ops-lb-wave31-farvol-alpha-public-2026-08-01.md) |
| **枠2 第2** | **farvol 0.80/0.20** `55148294` | Public **6.197** · 端のもう一方 |
| **枠2 旧** | OPS-C `55094041` / farvol 0.90 `55118587` | 6.237 / 6.226 · 降格候補 |
| **診断·枠外** | CHK-458 `55161873`/`55161881` | Public **7.78** · **F042** · mid残存壊滅 |
| **CV候補・未採点** | CHK-468 FINAL / tip×468 α0.05–0.10 | E2E mid残存GO · **提出禁止** · Trust tip-cv（472）待ち |

## 閉じたもの（再提出禁止）

| ID | Public | 扱い |
|---|---|---|
| **CHK-458 / 460 / 461 同型 mid FINAL** | **7.78** | **F042** · 追加提出禁止 |
| farvol α 0.88/0.12 · 0.85/0.15 | 6.273 / 6.314 | **枠外** · 中間α毒 · 追加α連打禁止 |
| SUB-8 / 10 / 11 / 12 | 6.53–6.58 帯 | 枠外 · F020 / OPS-LB-101112 |
| SUB-16 T0.3 | 6.385 | 枠外 · F025 |
| SUB-18 learned E2E | 7.705 | **禁止** · F015追認 |
| SUB-19 blend | 6.277 | 枠外 |
| OPS-A / B / D | 6.323 / 6.274 / 6.276 | **枠外** · A/B同面ノイズ · DはC未満 |
| T∈{0.10,0.15,0.2,0.3} 最終≡再提出 | — | **F025** |
| topk / spr12 tip | — | 223–229 · 214 · **NO** |
| 55001822（T0.5 重複） | 6.530 | 同kernel劣側 · **使わない** |
| F038–**F041** 言い換え成果物 | — | **禁止**（Soft-Preserve再学習含む） |

## UI チェックリスト（締切前 · ユーザー実行）

- [ ] Competition → Final 選択
- [ ] 枠1 = SUB-14
- [ ] 枠2 = farvol `55148128`（または `55148294` / 旧 OPS-C · ユーザー判断）
- [ ] 提出前 validator / Code Comp 規則確認
