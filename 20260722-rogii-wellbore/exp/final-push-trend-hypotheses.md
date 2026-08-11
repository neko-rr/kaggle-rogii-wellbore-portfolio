# Final Push 傾向仮説 — 2026-08-03（Kaggler読み後）

> source: 工程内比較更新後の傾向分析（Trust梯子 · 514反証 · 590/591 · S1/S2 digest）  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> 既存: FINAL-T2 · 579 · 558b/541 · 590/591 は重複登録せず **参照のみ**  
> 後継（Private希望·Public代理）: [`private-proxy-public-hypotheses.md`](private-proxy-public-hypotheses.md)（**610–617**）

**共通:** F015=生FINAL禁止 · Final自動差替なし · Trust/Pack/Public混ぜない · farvol枠2触らない · **最終目標=Private**

---

## A. Trust（CV）向上

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-FINAL-T2** | （既存）T2≈80で全カタログ再ランク→勝者773が hard20偏りを修正する | critical | T2順位表 · 提出はユーザー | 既存Active | T3 | **実行中** |
| **CHK-592** | agree系の微調整（例: agree∧\|L−tip\|≥3）が agree-only **26.629** を更新する（tipdist縮小は許容·Public同時狙いはしない） | high | Trust &lt; 26.629 · sample非悪化 · 提出なし | 591メモの26.621芽 | T4→T3 | **rejected** · 26.621だが hurt12 · [`592`](work/wave31-neural-proposal/out-592-agree-micro/report.md) |
| **CHK-593** | **true** S1-skip vs enable（534本番GPU）が before_hedge / agree-Trust を有意に動かす | high | tip-cvまたはE2E差分 · screenのproxy超え | 531/534 GO_screen | T3 | pending |
| **CHK-594** | FINAL-T2勝者が agree系（558b/541）を Trust で更新する | critical | T2 Trust &lt; 26.629 | FINAL-T2後 | T4 | pending |

## B. Public 向上（Trust仮説と分離）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-579** | （既存）tip⊕row495 の Public が tip 6.269 を明確に抜く／少なくとも壊さない | critical | Public着弾比較 | Active PENDING | T3 | **PENDING** |
| **CHK-595** | Public用ゲートは Trust用agreeと **別物**。579着弾後、row系がダメなら agree診断1回、agreeがダメなら行/多様性側を残す（同じagree連打しない） | high | 診断ルール1枚 · 提出≤1 | 590多様性 | T4 | pending |
| **CHK-596** | 診断提出するなら **558b↔579** の片方1回が 541↔558b より情報量が多い（tipdist 0.90 ≫ 0.26） | high | ユーザー明示時のみ1提出 · 再提出禁止 | 590 GO_screen | T4 | pending |
| **CHK-597** | 579 Public が tip悪化なら、row495系の Public連打を止め、Trust枠はagree/T2、Public枠はfarvol維持に固定する | medium | Stop更新 | 514反証と同型 | T4 | pending |

## C. 同時最適化は狙わない（規律）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-598** | Trust≤26.655 ∧ tipdist∈[0.4,0.9] の同時帯は空（591）。**同時Pareto探索の追加スイープはしない**（Final2両輪で代替） | high | Stopに固定 | 591 NOGO | T4 | pending→**即Stop化可** |
| **CHK-599** | farvol 0.95/0.05 枠2は触らず、Public改善は枠1診断または別パートナーのみ | high | farvol非再提出 | 既存Stop | T4 | **方針固定** |

## 実行順

1. **FINAL-T2**（A）∥ **579着弾**（B）  
2. **592** Trust微調整（CPU可）  
3. **595/596**（579後 · ユーザー提出判断）  
4. **593** true S1-skip（GPU余力）  
5. **594** T2勝者 vs agree  
6. **598/599** を Explicit Stop に反映

> 新規本登録: **CHK-592–599**（FINAL-T2/579は既存）
