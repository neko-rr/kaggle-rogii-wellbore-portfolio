# T2 上位化仮説 — 2026-08-04（Kaggler読み）

> source: CHK-FINAL-T2 run `20260803-114917` · [`t2-catalog-report.md`](work/colab-final-t2/t2-catalog-report.md)  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> 物差し: **T2≈80井 pooled RMSE**（低いほど良い）· 提出はユーザー明示時のみ  
> **最終目標=Private** · T2↑は Trust枠の代理 · Public同時Pareto狙わない（598）

---

## T2結果から読める構造（戦略前提）

| 事実 | 含意 |
|---|---|
| actionable 1位 **agree-only = Pack mid** · frac=1.0 · pooled **12.279** | T2上では **ゲートをいじっても mid495 全面を超えられない**（既に全面注入） |
| 579 / 541 / row は **12.331 完全タイ** | 部分ゲート（frac≈0.77）は全面 mid より **わずかに悪い** → 「賢い絞り込み＋mid」は T2 では逆効果側 |
| HD / learned_signed ゲートは **13.8台** | 注入量を減らすほど悪化 · mid が T2 で全域有利な証拠 |
| soft α0.50/0.10（全面寄りブレンド）は **14.6 / 16.5** | **Softをブレンド本体にすると負ける**（F041/F023 と整合） |
| F015診断 `learned_inject` **10.89** | mid より **~1.4** 下に天井がある · **生 learned FINALは禁止**だが、合法注入面の余地を示す |
| tip 単独 **17.03** | Pack載荷は T2 でも本命 · tip Soft再発明は不要 |
| mid468 / farvol face **skip** | カタログ穴 · 上位化本命ではないが再ランク欠測 |
| hard20 では **618c soft_diag=19.54 ≪ agree 26.63** | **抜け穴は「ゲート」ではなく「注入面=soft_diag」** · ただし soft_diag は現状 hard20寄り · **T2未採点** |

**1行戦略:** T2で12.279を抜くには **mid495より良い注入面**（第一候補 soft_diag）か **新しい mid**。agree/row/HD の再発明は閉鎖寄り。

---

## A. T2 pooled を直接更新（本命）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-621** | soft_diag を **T2 80井**に dump すれば、既存 tip/mid/learned と同尺で採点できる | critical | T2面 soft_diag CSV · n≈T2 rows · 提出なし | 618bは hard20のみ | T3 | **GO** · [`report`](work/colab-final-t2/out-t2-missing-cv-kaggle/report.md) |
| **CHK-620** | tip⊕**soft_diag** agree（≡618c機構）を T2 採点すると pooled **&lt; 12.279** | critical | T2 pooled &lt; agree-only · Soft FINALにしない · anti-promote | 618cは E2E/hard20 · ≠T2 | T3 | **NOGO** T2 **12.907** · hard20は改善 |
| **CHK-622** | 注入面を soft_diag 固定のまま、605/603系ゲート（soft−mid合意・softW）で絞ると T2 が更に下がる | high | T2 &lt; 620単体 · hurt井過多ならNOGO · ≠592 | 605/603は hard20 GO | T4→T3 | **rejected**（620 NOGO） |
| **CHK-623** | learned 診断天井(10.89)へ合法接近: **agree ∧ (soft_diagがmidより近い)** 行だけ soft_diag 注入すると T2 が 620 を更新 | high | T2 &lt; 620 · F015遵守（learned生注入禁止） · sample非悪化 | X_diag_learned はF015 | T3 | **rejected**（620 NOGO） |

## B. 穴埋め・保険（上位化期待は中〜低）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-624** | mid468 face を dump してカタログ再ランクすると、515/514系が T2 で mid495 を超える | medium | 再ランク表 · 超えなければ「468はT2でも劣位」確定 | face欠でskip済 | T3 | **pending** |
| **CHK-625** | T2 **井単位残差**（mid vs tip）で負け井だけ tip/soft_diag に戻すと pooled &lt; 12.279 | medium | T2改善 · help≥hurt · ≠602(ESS peaky) | →**640 で3井具体化** | T4→T3 | **pending→640** |
| **CHK-626** | **新しい mid 面**（Pack改·別ess/topk）が T2 で mid495 を抜く | low | T2 mid_alone &lt; 12.279 · 生FINAL禁止 | 620 FAIL後のみ（641はT2 GO済だが提出不可） | T3 | **blocked_until** |

> 工程分解後の追加仮説: [`t2-climb-stage-hypotheses.md`](t2-climb-stage-hypotheses.md)（**640–645**）

## C. 既存との役割分担（新規にしない）

| 既存 | 役割 | 本表との関係 |
|---|---|---|
| **CHK-FINAL-T2 all773** | 勝者の全井保険 | T2スコア更新ではない · 継続 |
| **CHK-594** | T2勝者が hard20 agree を更新するか | hard20軸 · T2上位化とは別 |
| **CHK-593** | true S1-skip | 上流 · 余力 |
| **CHK-618c** | soft_diag E2E機構GO | **T2未検証** → 620/621 が本線 |
| **CHK-592/600/602** | agree微調整・Softゲート・peaky | **rejected** · 言い換え再開禁止 |

## D. やらない（Explicit Stop と整合）

| 禁止 | 理由 |
|---|---|
| agree/row/HD の微差再スイープで T2 1位狙い | T2では全面 mid が既に最適 · 592型 |
| Soft / soft α を FINAL・採択本体にする | F041/F023 · T2でも softブレンドは敗北 |
| learned / mid 生 FINAL | F015 · 診断10.89は天井示唆のみ |
| tip Soft / PF 言い換え | F022–F040 |
| Public同時最適化スイープ | 598 |

---

## 実行順（2026-08-04 更新）

1. ~~621~~ **GO** · ~~620~~ **NOGO** · soft agree 注入は T2 で閉じる（hard20過大評価に注意）  
2. **T2本命:** **641 / 644 残差** · **626 新mid**  
3. 余力: soft_sign **11.815**（620の言い換えにしない）· 624 mid468  
4. 切替 **642 STOP** · [`640-642`](work/colab-final-t2/out-640-642-climb/report.md)  
5. all773 は **Colab別・触らない**

---

## 成功時の読み方

| 結果 | Final2への意味 |
|---|---|
| 620 T2 GO · tipdist 小 | Trust枠を 618c 方向へ寄せる根拠が強い |
| 620 T2 GO · tipdist 大（E2Eと同型） | Trust希望は残すが Public診断は明示1回のみ |
| 620 T2 NOGO | soft_diag は hard20楽観 · Finalは 558b/541 安全側 |
| 626のみ GO | Pack面更新が本命 · ゲート議論は打ち切り |
