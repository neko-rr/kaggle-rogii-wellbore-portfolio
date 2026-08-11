# カスケード / S0 不足仮説バックログ — rogii-wellbore

> updated: 2026-08-03 · 工程内比較・カスケード再整理で気づいた不足  
> SSOT: [`pipeline-cascade-retest.md`](work/wave31-selector-replace/pipeline-cascade-retest.md) §6 · §8.5  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> S1/S2 は別表: [`s1-s2-hypothesis-backlog.md`](s1-s2-hypothesis-backlog.md)（519–570）

**共通制約**

- Pack 改善だけでは枠1にしない（Trust tip-cv 必須 · G1）  
- 全面 mid FINAL 禁止（F042）· 生中間昇格禁止（F015）  
- 親を混ぜない（G4）· P-495 カスケードは §6.1 有望順  
- 既定 action_type: T4 → 良いものだけ T3

---

## A. S0 Pack 載荷（最優先ギャップ）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-571 | **492b/495** 面の Trust tip-cv hard20 を数値化すると、Pack Best が tip 29.899 を抜くか判定できる | cascade G5 · 492b | critical | Trust 数値 + tip比較 · 提出なし | ≠packだけで枠1 | T3 | **done GO** · Trust **26.761** · [`571`](work/wave31-neural-proposal/out-571-492b-trust/tipcv-trust-report.md) |
| CHK-572 | P-495 の **S0′** 段差分で、勝ち分がどの段まで残るか分かる（456の466と同型） | cascade §6.1 | critical | 段ごと tipdist 表 | 466対照 | T4 | **done GO** · mid残→FINAL≡tip · [`572`](work/wave31-neural-proposal/out-572-495-s0prime/report.md) |
| CHK-573 | P-495 親で **S3 w** ①0.60②0.55③0.50 を screen すると 0.60 が再び勝ち残る | cascade | high | w 採用表 | 467同型・新親 | T4 | **done GO** · **w0.50** tipdist最大 · [`573`](work/wave31-neural-proposal/out-573-p495-w-screen/report.md) |
| CHK-574 | P-495 親で **S4 α** ①0.75②0.50③1.0 が勝ち分を残しつつ proxy を改善する | cascade | high | α 採用 · 提出禁止 | 468同型・新親 | T4→T3 | **GO_screen** · α=1 inject最良 · soft劣る · [`574`](work/wave31-neural-proposal/out-574-p495-alpha/report.md) |
| CHK-575 | P-495 親で **S5 self_v** が profile より mid を残す | cascade | medium | 面差分 | 469同型 | T4 | **GO_screen** · tipdist · [`575-576`](work/wave31-neural-proposal/out-575-576-p495-self-s8) |
| CHK-576 | P-495 親で **S8 OFF** が ON より FINAL を壊さない | cascade | medium | OFF採用 | 470同型 | T4 | **GO_screen** · 同上 |
| CHK-577 | P-495 の最良 α×SL **2×2** が一次元勝ち残りを更新する | G8 | medium | 2×2表 | 471同型 | T4 | **GO_screen** · soft≪α1 row · [`577`](work/wave31-neural-proposal/out-577-p495-2x2/report.md) |
| CHK-578 | P-495 に **row/H-D** を載せると tip⊕ゲート Trust が H-D(468) 28.283 を更新する | S9-g | critical | Trust &lt; 28.283 または tip-cv | 512対照・新親 | T4→T3 | **done GO** · row **26.768** · HD **27.577** · [`578`](work/wave31-neural-proposal/out-578-p495-hd-trust/report.md) · **row優先** |
| CHK-579 | P-495⊕**row** FINAL の **tip-cv / E2E** が tip を抜く（生495提出禁止） | S9-cv | critical | tip-cv &lt; 29.899 · 診断提出はユーザー | 504対照 | T3 | **done GO** · tipdist 0.907 · Trust 26.768 · Public未 · [`579`](work/wave31-neural-proposal/out-579-e2e-harvest/chk579-report.md) |
| CHK-580 | P-495 FINAL×tip の **B0** α0.10/0.05 が Trust を微改善する（farvol枠2は触らない） | B0 · G7 | medium | Trust Δ · sample | 473同型 | T4 | **NOGO** · B0悪化 · [`580`](work/wave31-neural-proposal/out-580-p495-b0/report.md) |

## B. 現行 P-468 / 計測穴

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-581 | **504** H-D tip-cv が tip を抜けば、ゲート本命の Trust 根拠が立つ | final-board | critical | tip-cv 数値 | 既存504と同一·完了待ち | T3 | **done GO_local** · Trust **28.283**≡HD468 · tip-cv Ver5 ERROR停止 · Public514 NOGO · [`504-close`](work/wave31-neural-proposal/out-504-local-close/report.md) |
| CHK-582 | 504b: tip-cv 設定の対照（seed/allowlist）で 504 が再現する | 504 | high | 再現帯 | 504後 | T3 | pending |
| CHK-583 | P-468 の **S0′ 再計測**（521拡張）で 501b 以降の消失点が更新される | cascade · 521 | high | 段差分表 | 521と統合可 | T4 | **GO** · 521と統合 · [`521`](work/wave31-neural-proposal/out-521-583-s0prime/report.md) |
| CHK-584 | 514/515 Public が Trust 順位と同方向なら、H-D/行の採用根拠が強化される | ops | high | Public 着弾メモ | 提出済·待 | T4 | **514 NO-GO 6.335** · **515 6.249** ≈SUB-14 · [`514-LB`](latest/ops-lb-chk514-public-2026-08-03.md) |

## C. 物差し・監査（やり過ぎ防止）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-585 | Pack / Trust / Public の **3層を1枚に固定**すると、pack勝ちを枠1に誤用しなくなる | G1 | high | 1枚 SSOT 更新 | 新規 | T4 | **done GO** · [`ruler`](latest/three-layer-ruler-2026-08-03.md) |
| CHK-586 | S9 前に **外井・別seedの軽い確認**（G6）を1回入れるとゲート楽観を減らせる | G6 | medium | メモ1回 | 新規 | T4 | **GO_screen** · LOO · [`586`](work/wave31-neural-proposal/out-586-loo-light/report.md) |
| CHK-587 | P-495 勝ち分の **井スライス**（方位/遠MD）を取ると、全面採用を避けられる | G3 | medium | 井別表 | 517型・新親 | T4 | **done GO** · 18/20 · [`587`](work/wave31-neural-proposal/out-587-p495-wellslice/report.md) |

## D. S0 表記ギャップ（低優先）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-588 | **beam** の短T4（既存フラグON/OFF1回）で Pack/Trust が動くか分かる。動かなければ表記削除候補 | S0-beam | low | Δ報告 · 長GPU禁止 | **→601** | T4 | **superseded→601** |
| CHK-589 | Soft 面を **ゲート特徴のみ**（提出なし）に使うと F041 を避けつつ信号が取れるか（557と同型・S0側） | F041境界 | low | 特徴寄与 · 提出なし | **→600/607** | T4 | **superseded→600** |

## E. HOLD（条件付き · 新IDなし）

| 既存ID | 条件 |
|---|---|
| CHK-471 / 474 / 476 | 504 または 579 が tip を明確に抜いたとき |
| CHK-492 | ERROR · **571/492b 経路を優先**（ess1.2は二の次） |

---

## 実行順（推奨 · 2026-08-03更新）

1. ~~571~~ · ~~578~~ · **579 tip-cv（P-495⊕row）** ← いまここ  
2. 504 Ver4 / 515 Public（並行・Final触らない）  
3. 572 → 573–577 → 580（579後）  
4. 583 · 585–587 監査  
5. 588 beam は余力のみ · S1/S2 は learned train dump 後

> 合計新規: **CHK-571–589**（19件）· HOLD は既存IDのまま
