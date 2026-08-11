# 上流工程（予測生成）精度向上 — 2026-08-04

> 前提: 下流ゲートは天井が薄い · tip→mid Δ−4.75 は **面の勝ち**  
> Host: [698825](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/698825) · [719235](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/719235)  
> 重複登録しない実施本体: **621/620 · 643 · 650–657 · 651/652 · 626**  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)

---

## 1. 戦略読み（追加した理由）

| 判断 | 根拠 |
|---|---|
| **上流は難しい** | typewell 死井 · tip Soft/PF 天井 · S1/S2 長時間 · dump 不足 |
| **それでも本命** | T2 で mid≪tip · residual も mid 土台 · 下流 HD/agree は悪化側 |
| **効き方の単位** | ゲート微差ではなく **照合・粒子・Pack 内部の生成品質** |
| **載せ方** | 新面は **tip⊕gate または合成 residual** · 生 mid/L/soft FINAL 禁止 |

### 難易度マップ（実験用）

| 層 | 例 | 難易度 | T2 空気 |
|---|---|---|---|
| 下流ゲート | agree / row / HD | 相対易 · **閉じる** | 絞るほど悪化 · 642 |
| 既成 mid 載荷 | tip⊕mid | 中 | Δ−4.75 · 標準 |
| 合成 residual | 641 / 660 | 中 | 合法 · 面依存 |
| **上流の生成改善** | soft_diag · warp · self-GR · Pack内 | **高** · **本命** | 未完・ここしか伸びない |
| tip Soft/PF 再発明 | F022–F040 | 閉鎖 | ≡tip または悪化 |

---

## 2. 実行マップ（既存 CHK · 二重に本体を作らない）

| 上流の中身 | 実施 ID | 役割 |
|---|---|---|
| 別注入面 soft_diag | **621→620** | 本命A 面 |
| typewell 信頼度・層別 | **657→650** · **655** | 死井分岐 |
| known-TVT typewell warp | **651** | David/Host |
| 負 dTVT → lateral GR | **652** · **653** | Host self-corr |
| 近傍 dip prior | **654** | 傾きのみ · ≠TVTコピー |
| S2–S6 どこが Δ の主因 | **643** → 改修1点 | Pack 内部 |
| 新 mid 全面 | **626** | 620 系 FAIL 後 |
| 載せ方（下流） | tip⊕gate · **660–663** residual | 生 FINAL しない |

---

## 3. 新規（CHK-670– · 方針・測定・GO 基準）

本体実験は上表。ここは **上流レーンを止めない規律** と **誤った易しい実験への逃げ** を封じる。

| ID | hypothesis | priority | acceptance | dup-check | action | status |
|---|---|---|---|---|---|---|
| **CHK-670** | Final Push の Trust 本命を **「面（上流・中流生成）更新」** に固定し、agree/row/HD 微スイープを Active から **明示退場**すると、無駄実験が減る | critical | Explicit Stop とレーン表に「上流本命」追記 · 追加の微ゲート CHK 0件 | **645 の拡張** · ≠新規ゲート発明 | T4 | **applied** |
| **CHK-671** | 新しく生んだ面 X は必ず **(a) X単独 T2** と **(b) tip⊕gate(X) T2** の **二本採点**にし、(b) だけで GO 扱いしないと、生 FINAL 事故と過小評価を防ぐ | critical | 新規面 CHK の acceptance に dual-score 必須 | ≠F015 生昇格 · 620/651 等に適用 | T4 | **applied** |
| **CHK-672** | 上流 GO 定義: **X単独 &lt; mid 12.279** または **tip⊕X &lt; 12.279 かつ mid 注入より良く sample 非悪化** · 片方だけの「雰囲気 GO」を禁止 | high | GO 判定チェックリスト1行 · 621/651/652/626 に適用 | 測り方統一 | T4 | **applied** |
| **CHK-673** | **643** で tip→mid Δ の主工程が1つに決まったら、その工程だけ **1機構改修**（他工程同時いじり禁止）すると再現可能な改善になる | high | 主工程1 + 改修1 CHK · T2 前後比較 | 643後 · ≠全段同時 | T3 | **blocked_until_643** |
| **CHK-674** | 上流コスト高を前提に、優先順を **643 内部診断 → 673 1改修 → 676 residual 再格子 → 626**（地質 650 系は割り込ませない）に固定する | high | Active 「次」と一致 · 620 NOGO 後更新 | 2026-08-04 更新 | T4 | **applied** |
| **CHK-675** | 上流で得た良い面は **Trust レーン（枠1候補）**、Public は tip近い薄い載荷のみ · residual Public は 641 で閉じる | high | Final2 規律 · 679 | 598 · 636 | T4 | **applied** |
| **CHK-676** | residual は mid 従属 · **mid 更新後**に α 再格子すると T2 天井が上がる · Public 提出しない | critical | 新 mid T2&lt;12.279 · resid T2&lt;9.998 · sample OK · 提出禁止 | 641 Public NO-GO 後 | T3 | **pending_after_673** |
| **CHK-677** | 643 主工程ラベルに **改修スコープを縛る**（S1–2→L、S3–8→1段） | critical | ラベル一致 · T2 dual | 673 前必須 | T3 | **blocked_643** |
| **CHK-678–680** | flip 監査 · residual Public 禁止 · tip/farvol 固定 | high | Explicit Stop | セッション後 | T4 | **applied** |

詳細戦略: [`t2-upstream-cv-strategy-2026-08-04.md`](t2-upstream-cv-strategy-2026-08-04.md)

---

## 4. やらない（上流ネタでの逃げ）

| 禁止 | 理由 |
|---|---|
| 「上流は難しいから」と **HD/agree に戻る** | 既に T2 で敗北 · 645/642 |
| tip Soft / PF / 温度 の言い換えを **上流改善と呼ぶ** | F022–F040 · F013 |
| 新 mid/L を **そのまま提出** | F015 / F042 |
| 近傍 **TVT レベル**コピーを上流と呼ぶ | F002 |
| S1–S2 を全部同時にいじる | 再現不可 · 673 |

---

## 5. 実行順（上流レーン）

3. ~~**670/674** 方針を checklist に固定~~ → **applied**（checklist · Explicit Stop）  
4. **621→620**（本命面 · dual-score 671）  
5. **657→650 · 651 · 652**（地質参照）  
6. **643** → **673** 1工程改修  
7. **626** は面系全滅後  
8. 載せ方は **tip⊕gate / 660 系 residual** · 生 FINAL 禁止  
9. **675** Public と混ぜない

---

## 6. 1行

**上流は難しいが Trust の本命。** 易しいゲートに逃げず、面を dual-score で測り、tip⊕gate で運ぶ。
