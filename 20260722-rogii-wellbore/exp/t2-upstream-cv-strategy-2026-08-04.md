# 上流改善戦略（確かなCV基準）— 2026-08-04 セッション後

> **目的:** Trust を **上流の生成品質** から上げる経路だけ残す  
> **CVの正:** **T2≈80 well pooled RMSE**（run `20260803-114917` faces）が Trust 本尺子  
> **補助CV:** hard20 mean · sample3井非悪化 · help/hurt well count  
> **非Trust尺子:** Public（診断・枠2 farvol）· tipdist TEST  
> Active: [`experiment-checklist.md`](experiment-checklist.md) · 規律: [`t2-climb-upstream-geology.md`](t2-climb-upstream-geology.md)

---

## 1. 結果から確定した地図（誤解しない）

| 事実 | 数値 | 上流への意味 |
|---|---|---|
| tip→mid の勝ち分本体 | T2 17.03→**12.28**（Δ−4.75）· win77/hurt3 | **面（mid スタック）が主戦** · ゲートではない |
| ゲート絞り | row 12.33 · HD **13.89** | 下流で 12.28 は抜けない · **退場** |
| tip\|mid 切替天井 | Δ**0.062** | 切替 R&D STOP · **面更新必須** |
| soft→mid 注入 | **12.91 NOGO**（620） | soft を mid に載せるのは閉じた |
| soft tip⊕agree Public | 6.231 · tipdist 11.9 | Public 次点でも **Trust 本線にしない** · 面材料候補のみ |
| residual mid+α(L−m) | T2 **10.31→9.999** · help **77/3** | **mid 土台の上でしか効かない** · L 方向は有用 |
| residual **Public** | **641 = 6.472**（tip+0.203） | residual は **Trust only** · Public 主策禁止 |
| match/heel/lateral 層別 | 天井薄い · NOGO 多数 | **参照ギミック先**ではなく **Pack 内部（643）先** |

**1行:** 確かな T2 が言うのは「**mid を良くせよ**。載荷は residual / tip⊕。Public は farvol。ゲートに戻るな」。

---

## 2. 物差し（これ以外で GO を主張しない）

| 順 | 物差し | 用途 | 停止条件（NO） |
|---|---|---|---|
| 1 | **T2 pooled** | 上流 / residual / 新面 | 単独 T2 だけでは足りない → **dual 671** |
| 2 | **X 単独 + tip⊕gate(X)** dual | 新面 GO | 片方だけ「雰囲気 GO」禁止（672） |
| 3 | sample3 + hurt 井 | 安全 | sample 悪化 or hurt 拡大で NOGO |
| 4 | hard20 mean | 補助 · order flip 監視 | hard20 単独で採用禁止 |
| 5 | Public / tipdist | 枠2 · 診断 | Trust 採用/却下の主証拠にしない |

**actionable mid 基準:** 12.279。新 mid はこれ以下を狙う。residual は mid 改善の **後** に再格子。

---

## 3. 上流→中流→載荷の戦略（工程順）

```text
[S0 tip 凍結] ──防衛土台・公開枠の参照
      │
      ▼
[S1–S2 粒子 / learned 方向] ── 生 FINAL 禁止 · residual の L 供給源
      │         ↑ ここを「良くする」＝ 666 の天井を上げる
      ▼
[S3–S8 mid スタック] ── T2 本命 12.28 · 643 で主因工程特定
      │
      ▼
[載せ方] tip⊕gate 薄い ／ mid+α(L−m) residual（Trust）
      │
      ▼
[禁止出口] Soft/L/mid 生 FINAL · residual Public · ゲート連打
```

### 本命パス（Trust）

| 段 | 戦略 | 根拠 | 次 CHK |
|---|---|---|---|
| **U0 診断** | 643 ladder で tip→mid Δ の **主工程1つ** を特定 | dump 無しでは改修点不明 | **643→673** |
| **U1 1工程改修** | 主工程だけ機構変更 · 他段同時禁止 · T2 dual | 再現性 · 673 | **673** |
| **U2 新 mid 固定** | 改修後 mid 面を SSOT faces として保存 · 12.279 比較 | 672 GO | **626** if full regen |
| **U3 residual 再格子** | **新 mid 上**で α 格子 · T2 dual · Public に出さない既定 | residual は mid 従属 · 641 Public NO-GO | **676** |
| **U4 L 側品質** | residual を伸ばすなら **L 再学習/再 dump**（生 L 提出禁止） | L 方向は T2 有効 · 載荷は合成 | **677** |
| **U5 soft 面** | soft は **注入禁止のまま** · dump/診断材料のみ | 620 NOGO · 618c tipdist | 面材料のみ |

### やらないパス

| 逃げ | なぜ |
|---|---|
| α↑ のみ / Public residual | 641=6.472 · tipdist↑ |
| soft→mid 再注入 | 620 |
| agree/row/HD 微差 | T2 悪化 |
| tip\|mid 切替 | Δ0.062 |
| match 層別スイープ | 650 天井 |
| Public≈ Trust で同時 Pareto | レーン分離 · 641/618c |

---

## 4. 新規仮説（CHK-676– · checklist 投入）

| ID | hypothesis | CV acceptance | action | status |
|---|---|---|---|---|
| **CHK-676** | residual の T2 勝ちは **mid 土台の従属**なので、**mid を T2 で更新してから** α 再格子した方が、α だけスイープするより Trust 天井が上がる | 新 mid T2 &lt; 12.279 · その上 residual &lt; 旧 666(9.998) · sample 非悪化 · **Public は既定提出しない** | T3 | pending_after_673 |
| **CHK-677** | 643 主工程が S1–S2（粒子/L）なら、改修は **L 品質または blend 則**に閉じ、S3–S8 同時触り禁止。主工程が S3–S8 なら **スタック1段のみ**。誤段への Host 地質を詰め込まない | 主工程ラベル一致 · T2 dual · Δmid vs tip 改善 | T3 | blocked_643 |
| **CHK-678** | 新面 Trust 採用前に **T2 と hard20 の順位が大食い違いしない**こと（既に residual dual で order 安定）を確認し、flip があれば T2 優先でも **hurt 井・sample を再監査**する | dual 表1枚 · flip 時は NOGO or 限定 | T4 | applied_rule |
| **CHK-679** | 641 で residual **Public は Trust≠Public 確定**のため、Trust 候補 residual は **ユーザー明示提出まで Public 診断1回以上**を要求しない／禁止する方が枠浪費を防ぐ | Explicit Stop · 666 そのまま維持 | T4 | applied_rule |
| **CHK-680** | S0 tip・farvol は **触らず固定**したまま上流だけ動かす（枠2防衛）。上流 GO 面は Trust 枠1 候補のみに載せる | farvol/641 再提出 0 · 新面は checklist 670/675 準拠 | T4 | applied_rule |

**拡張:** 候補生成・学習の網羅キュー **CHK-681–726** は [`t2-candgen-learn-checklist-2026-08-04.md`](t2-candgen-learn-checklist-2026-08-04.md) が SSOT（**676≡702 · 673≡697**）。

---

## 5. 実行順（いま）

1. **（任意並列）診断 683–687 · 722**  
2. **643 COMPLETE → harvest → 685 → 677 → 697(=673)**  
3. dual T2（671/672）· sample3 · help/hurt  
4. 面 GO → **701 → 702(=676) residual**（Public 禁止）  
5. 並行可: **688–693** L 再学習  
6. 全面: **719 / 626**（703 条件後）  
7. residual **提出はユーザー明示のみ**（679）  

---

## 6. 参照

| 内容 | パス |
|---|---|
| candgen/learn 穴潰し | [`t2-candgen-learn-checklist-2026-08-04.md`](t2-candgen-learn-checklist-2026-08-04.md) |
| residual Public | [`latest/ops-lb-chk641-public-2026-08-04.md`](latest/ops-lb-chk641-public-2026-08-04.md) |
| residual 井 | [`latest/residual-t2-well-effects-2026-08-04.md`](latest/residual-t2-well-effects-2026-08-04.md) |
| T2 梯子 | [`within-stage-comparisons.md`](within-stage-comparisons.md) |
| 上流規律 | [`t2-climb-upstream-geology.md`](t2-climb-upstream-geology.md) |
