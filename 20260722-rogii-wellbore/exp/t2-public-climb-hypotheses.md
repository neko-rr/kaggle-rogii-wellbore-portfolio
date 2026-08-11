# T2→Public上昇仮説 — 2026-08-04（Kaggler読み）

> source: CHK-FINAL-T2 `20260803-114917` · [`t2-catalog-report.md`](work/colab-final-t2/t2-catalog-report.md)  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> 姉妹（Trust）: [`t2-climb-hypotheses.md`](t2-climb-hypotheses.md)（620–626）  
> 既存 Public代理: [`private-proxy-public-hypotheses.md`](private-proxy-public-hypotheses.md)（610–617）  
> **最終目標=Private** · Public↑は保証なき代理 · σ≈0.03 · |Δ|≲0.08はノイズ

---

## T2結果の Public 読み（戦略前提）

| T2事実 | Public含意 |
|---|---|
| tip 単独 **最悪 17.03** だが Public **6.269** | **T2勝ち ≠ Public勝ち**。agree-only/Pack をそのまま枠2にしない |
| agree-only **12.279**（≡Pack · frac1.0） | Trust本命。Publicは TEST frac **0.127** の薄い差分として別評価 |
| 579/541/row **T2完全タイ 12.331** | Trustでは区別不能 → **Public着弾と tipdist が分岐軸** |
| TEST tipdist: 541 **0.278** ≪ 558b **0.382** ≪ 579 **0.907** ≪ 618c **11.9** | Public上昇希望は **tipに近い面**（541→558b）。遠面は振れ大 |
| HD / learned_signed **13.8台**（T2悪化） | 514 Public **6.335** と同型 → **Publicレーンから HD 除外** |
| soft α0.50/0.10 **14–16台** | Softブレンドは Trustも負ける → **Public提出に Soft/α全面を載せない** |
| farvol / OPS-C / mid468 **skip** | 枠2既知強者は T2未採点 · farvolは触らない · パートナーは α薄い診断のみ |
| 515 Public **6.249≈tip** · 514 **NO-GO** | 「薄い載荷で≈tip」は生存、「強いゲート」は死亡 |

**1行戦略:** Publicを上げにいくなら **tip土台＋小さな tipdist（frac≲0.15帯）**。T2最良の全面 mid / soft_diag遠面 / HD は枠2に使わない。

---

## A. 本命（着弾後・薄い差分）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-630** | 579着弾後、T2同点クラスタの次の Public診断1回は **541（tipdist最小）優先**（558bは第二 · 618cは除外）すると情報効率が最大 | critical | ユーザー明示1提出 · 再提出禁止 · 615分岐と整合 | 596の具体化 · ≠618c | T4 | **ready**（579=6.277 ≈tip · 次は541） |
| **CHK-631** | 579が tip悪化なら、row系連打せず **541へ1回だけ**切替（T2同点・tipdist小）が Public回復の最短 | critical | 615悪化枝に541を明記 · farvol枠2維持 | 597/615拡張 | T4 | **done_policy**（≈tip微悪 · row STOP） |
| **CHK-632** | Public候補は **frac≲0.15 の tip⊕gate**（558b型）に限り、T2全面mid（frac1）や Pack生は枠2に載せない | high | Stop/Final2メモ更新 · 無断提出なし | 613 GO_confirm | T4 | **done_policy** · 579は非候補 |
| **CHK-633** | tip×**非farvolパートナー**（OPS-C / 515面）α**0.05のみ**1点が Publicを tipより明確に動かす（|Δ|≳0.15） | high | ユーザー1提出 · Trust報告 · farvol非再提出 | 612表は済 · LB未 | T2 | **pending** |

## B. 材料・穴埋め（期待は中）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-634** | mid468 face を T2 採点し、「Public≈tip の 515型」が T2 で tip を大きく壊さないことを確認してから α0.05 材料にする | medium | T2表 · tip非破壊 · 提出は633経由 | ≠624（Trust上位化）· 目的=Public材料 | T3 | **pending** |
| **CHK-635** | farvol/OPS-C の **train face** を揃えると、T2同一物差しで「枠2候補の Trust副作用」を事前に読める | low | face有 · T2副作用表 · farvol提出なし | catalog skip埋め | T4 | **pending** |

## C. 明示除外（Public上昇策にしない）

| ID | hypothesis（棄却） | 扱い |
|---|---|---|
| **CHK-636** | 618c / soft_diag（tipdist≈12）を Public上昇の主策にする | **NO-GO方針** · Trust専用 · 診断はユーザー明示時のみ |
| — | HD / learned_signed ゲートを Public再提出 | T2悪化+514反証 · **Stop** |
| — | tip×soft α 全面ブレンドを Public提出 | T2敗北+F041 · **Stop** |
| — | agree-only≡Pack 全面を枠2に昇格 | T2最良だが Public未検証かつ F015境界 · **禁止** |

---

## 既存CHKとの役割分担

| 既存 | 本表 |
|---|---|
| **579 / 615** | 着弾スイッチ → **630/631** が次手を具体化 |
| **595/596** | 診断ルール → **630** が「541優先」を固定 |
| **612** | tipdist表 done → **633** が α0.05 の **実LB1点** |
| **613** | frac安全 done → **632** が枠2選定ルール化 |
| **610/611/616/617** | rejected · 再開しない |
| **620–626** | Trust T2上位化 · Public同時狙わない |
| **618c** | Trust候補 · **636** で Public主策から除外 |

---

## 実行順

1. **579着弾済** Public **6.277** · 615≈tip · [`ops-lb`](latest/ops-lb-chk579-public-2026-08-04.md)  
2. **630** 次診断=**541**（ユーザー明示時のみ1回）  
3. 枠余裕時 **633**（α0.05 · 1点）  
4. 余力 **634** · **635**  
5. **636** 方針固定  
6. Trust本線（620）は **分離**  

---

## 成功時の読み方

| 結果 | 意味 |
|---|---|
| 541診断が tip より明確改善 | 枠2候補に541系 · farvolとのFinal選定はユーザー |
| 541/579とも ≈tip（σ内） | 枠2=farvol維持 · 追加Public実験停止 |
| 633 α0.05 が動く | 薄ブレンド枠2の残弾あり |
| どれも σ内 | Public上昇余地は小さい · Trust（620）へリソース集中 |
