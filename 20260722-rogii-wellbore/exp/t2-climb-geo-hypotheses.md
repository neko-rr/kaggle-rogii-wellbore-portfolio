# T2 CV 向上仮説 — 地質・Host視点（2026-08-04）

> **物差し:** T2≈80井 **pooled RMSE**（↓が改善）· Trust 代理 · 提出禁止既定  
> **実験事実:** [`t2-catalog-report.md`](work/colab-final-t2/t2-catalog-report.md) · [`t2-stage-well-map`](latest/t2-stage-well-map-2026-08-04.md) · 641 residual GO  
> **Host / Discussion:**  
> - [698825 How Geologists Interpret Wells](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/698825) · 全文 [`../docs-en/discussion/698825-host-geologist-tips-full.md`](../docs-en/discussion/698825-host-geologist-tips-full.md)  
> - [719235 Typewell 不一致](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/719235) · [`../docs-en/discussion/719235-geologists-analysis-full.md`](../docs-en/discussion/719235-geologists-analysis-full.md)  
> 先行本線（重複登録しない）: [`t2-climb`](t2-climb-hypotheses.md) **620–626** · [`t2-stage`](t2-climb-stage-hypotheses.md) **640–645**

---

## 1. 優秀なKaggler読み（T2 × 地質）

| 帯 | T2 / 工程の事実 | 地質的な意味 |
|---|---|---|
| **勝ちの大半** | tip 17.03 → mid **12.28**（Δ−4.75）· win **77**/80 | Pack/mid は「typewell 照合 + 粒子ジオステア」の本流。ほとんどの井で **層位座標の揺れ** を取りこぼしている tip より中間面が正しい |
| **絞ると悪化** | HD **13.89** · frac↓ | 地質的に「怪しい行だけ差し戻す」と、**一致が取れている区間まで捨てる** → Host の「信頼性一定ではない」とは別問題で、**一律 frac 節約が誤る** |
| **hurt 3井のみ** | `70925e23` / `ab3ced07` / `19871e7f` · tip がわずかに勝つ | mid 過剰補正（薄い井戸帯・既によく乗っている heel）。天井 **Δ0.062**（642）なので **切替R&Dは終了**、地質仮説は **面の作り方** へ |
| **診断天井** | learned 6.81 · mid+α(L−m) **10.31**（641） | 残差方向に真値。**α&lt;1 の合成面は F015 自動禁止ではない**（§7）· 危ないのは **α=1 の L 生昇格** と **F042 帯の mid 全面寄り提出** |
| **未検証の本命A** | soft_diag hard20 19.54 · **T2未dump** | soft は「別の地層候補面」。620 は本線維持 |

**Host の 3 点（698825）を T2 作戦に直訳する:**

1. **Formation dip は近傍井で似る** → 絶対 TVT の空間コピー（F002 死亡）ではなく、**傾き prior** を残差に効かせる  
2. **PS 前の lateral GR は typewell より分解が良い** · かつ **TVT が PS から負方向**（上り / 負dTVT）なら lateral 自己相関の方が typewell より効く  
3. **Lateral GR は自 corr** → typewell が死んでいる井（719235: `000d7d20`）では **heel lateral を第2参照ログ** にする

**David（719235）:** Typewell 不一致は実在 · **既知 TVT で typewell を少し補正できる**が、完全説明ではない → 「照合スコアで分岐」と「prefix TVT ワープ」は両方試す価値がある。

---

## 2. 新規仮説（CHK-650– · T2 重視）

| ID | hypothesis（手法 × 期待効果） | priority | acceptance | dup-check | action | status |
|---|---|---|---|---|---|---|
| **CHK-657** | T2 80井に **label-free typewell match score**（PS前 GR↔typewell NCC / peak鋭さ）を付与し、mid-win vs mid-hurt 3井で match が分かれるなら、層別注入の根拠になる | high | 報告1枚 · mid-hurt が低match側に偏る/しないを明記 · 提出なし | T4診断 · ≠620実行 | T4 | **pending · 先にこれ** |
| **CHK-650** | match **低**井は tip 固定、**高**井は mid 全面（または mid+薄残差）にすると T2 < **12.279** | high | T2&lt;12.279 · help≥hurt · HD再発明でない | **≠HD/frac** · **≠640固定3井** · 642切替STOPと矛盾しない（スコア規準が match） | T3 | **pending**（657後） |
| **CHK-652** | tip/mid の **PS→先での dTVT 累積が負**（Host: TVT domain negative）の区間だけ、typewell 照合を **PS前 lateral GR 自己相関** に切替える注入面を作ると、その井帯で mid を更新 | high | 当該帯 RMSE改善 · 他帯非悪化 · Soft/L FINAL禁止 | ≠F013 tipプロファイル · ≠251 dip-PF state | T3 | **pending** |
| **CHK-651** | 既知 `TVT_input` 区間だけで **typewell TVT 軸をわずかに warp**（stretch/offset · heel fit）→ その参照で mid 再生成し、T2 が mid495 を抜く | high | T2 mid_warp &lt; 12.279 · heel only label · 評価区間ラベル未使用 | David 719235 · ≠gold_prefix だけの FINAL 載せ替え · ≠F015 生 mid FINAL | T3 | **pending** |
| **CHK-653** | match 低井で **lateral-self lag 面**を tip⊕gate 注入（frac を match で制御）すると T2 改善 | medium | T2&lt;12.279 or vs 650改善 · anti-promote | Host self-corr · ≠遠井コピー F002 | T3 | **pending**（650後） |
| **CHK-654** | 空間 kNN の **formation dip（dTVT/dMD）prior** を残差 walk に弱く混ぜると T2 が 641/mid を更新 | medium | T2改善 · **絶対TVT近傍コピー禁止** · sample非悪化 | Host dip · ≠F002 · ≠727537 kriging level · ≠251 | T3 | **pending** |
| **CHK-655** | 641 型 `mid+α(L−m)` を **match 高井のみ**・α格子は **井外**（T2全体固定α）にすると、全井 α より T2 が良く **hurt が減る** | high | T2 ≤ 641全井α · hurt≤3 · **α=1 禁止** | 641 の地質層別 · ≠αをラベル井最適化 | T3 | **pending** |
| **CHK-656** | soft_diag 注入（620）を **match 低井優先** にすると、全面 soft より T2 が改善または同等で sample 安全 | medium | T2 ≤ 620全面 · Soft FINAL禁止 | **620 GO後** · 636 Public方針と別 · Trust用 | T3 | **blocked_until_620** |

### 既存本線との役割（新規にしない）

| 既存 | ここでの位置づけ |
|---|---|
| **621→620** | **注入面の本命A**（soft）· geo層とは並走。620 を待つ |
| **641 residual** | 数学的方向は勝ち · 地質では **655 で層別** を足す |
| **642/645** | tip\|mid 微差・HD救済は **停止維持** |
| **640 3井 tip** | 固定井リスト · **650 は match スコア** で一般化 |

---

## 3. やらない（地質ネタでの言い換え防止）

| 禁止 | 理由 |
|---|---|
| 近傍井の **TVT レベル**コピー / 空間 kriging 主体 | F002 · 727537 dead-end |
| typewell 無しの heel affine / gs スイープ | F001 |
| unguarded GR matching 「どこでも探索」 | 717445 · 721549 |
| fault/teleport / tip Soft・PF 言い換え | F026 近傍 · F022–F040 |
| mid / learned / soft **生 FINAL 提出** | F015 / F041 / F042 |
| match を **H-D と同じ frac 節約**に矮小化 | T2 で HD 敗北済み |

---

## 4. 実行順（T2 CV · geo レーン）

1. **657** match スコア診断（短 · T4）  
2. **650** match層別 tip|mid（657が GO 方向なら）  
3. **652** 負dTVT → lateral-GR correlator  
4. **651** known-TVT typewell warp  
5. **655** 641 の match 層別残差  
6. **653 / 654** 余力  
7. **656** は **620 後**  
8. 並走本線: **621→620** は geo と独立に優先維持

---

## 5. 成功時の読み方

| 結果 | 読み |
|---|---|
| 657 で mid-hurt ≠ 低match | Host 物語は T2 では弱い · **650 スキップ** · 652/651 へ |
| 650 だけ Δ≪0.05 | 642と同型 · 切替系は諦め **面（620/651）** |
| 651/652 で mid 帯更新 | **ジオステア材料の質**が本命 · Pack差し替え方向（≠ゲート） |
| 655 が全井αより良い | residual は **一致している層**にだけ寄せるのが地質的に正しい |
| どれも 12.28 不動 | soft / 新 mid（620·626）以外に T2 の穴は無い |

---

## 6. 過去実験との重複（2026-08-04 監査）

| 新規 ID | 似た過去 | **同じか** | 判定 |
|---|---|---|---|
| **657** match×mid-win/hurt | ESS peaky **602** · soft残差ゲート **600** · warp検出 **354** | 機構が違う（typewell **照合品質スコアを T2 面に載せる診断**は未了） | **未実施** |
| **650** match層別 tip\|mid | **640** 固定3井 · **592** \|L−tip\| · H-D 絞り | 640は leaky oracle 井名簿 · match スコア一般化は未 | **未実施**（640と近いが入口が違う） |
| **652** 負dTVT→lateral GR | gold_prefix / selfline / **364** PS連続 | self_verified・PS連続は別 · Host条件付き correlator 切替は未 | **未実施** |
| **651** known-TVT typewell warp | gold_prefix · **354** warp候補 · heel NCC **040/031** | 「heel TVTで typewell 軸 warp→mid 再生成」を T2 で通した記録なし | **未実施**（近縁はあり） |
| **653** lateral-self lag 注入 | NCC 単独モデル **F007/F008/031** | 失敗は *tip置換の tabular/NCC*。**mid差し替え用 self-lag 面**としては未 | **未実施**（形だけ似て禁止内容は別） |
| **654** 近傍 dip prior | **251** dip PF state · 空間kriging dead · F002 TVTコピー | Host は **傾き**共有 · 251 は PF state · 別機構 | **未実施**（251言い換えにしないこと） |
| **655** match層別残差 | **641** 全井 mid+α(L−m) | 641は全井一律α · 層別は未 | **未実施** |
| **656** match低へ soft | **618/620** soft_diag | 面は同じ候補 · match 優先付けは **620後** | **未実施** |

**要旨:** 「地質の話は過去に全部やった」ではない。**似たキーワードの NO-GO / 別機構**が多数あるので、入口の **657 診断**で重複を潰してから本体に進む。

---

## 7. F015 / 「10.31 提出不可」は誤解か（優秀Kaggler再審査）

### 7.1 F015 が本当に禁止するもの（SSOT）

| 禁止 | 実例 | Public |
|---|---|---|
| 中間面を **そのまま** submission にする（`*-only` · raw promote） | SUB-4–7 mpkg/pre-BH · **SUB-18 learned_trajectory** | 6.6〜**7.7** |
| （別ID）全面 mid≠tip の mid残存 FINAL | **CHK-458 / F042** | **7.78** |

**禁止しない:** tip⊕ゲート差し替え · S1/S2 改善 · **合成面の構築と Trust 採点**。  
詳細: [`docs-ja/f015-f013-correct-reading.md`](../docs-ja/f015-f013-correct-reading.md)

### 7.2 mid+α(L−m)=10.31 は何か

```
pred = mid + α · (learned − mid)   # α=0.30 が best
```

| α | 意味 | F015? |
|---:|---|---|
| 0 | ≡ mid 全面 | F042リスク帯（Publicは 458 で崩壊実績） |
| **0.3** | midとLの **新規合成** · **L単独ではない** | **自動F015ではない** |
| 1 | ≡ learned 全面 | **F015 そのもの**（SUB-18） |

- T2 格子: **641 GO**（10.309）
- E2E **診断提出済**（ref **55223002** · tipdist≈1.74 · pure L FINAL **False**）  
  → 「CV禁止」「F015自動禁止」ではない。**再提出だけ**禁止

### 7.3 どこで誤解が混ざったか

| 言い回し | 妥当性 |
|---|---|
| 「L を **そのまま FINAL** にするな」 | ✅ **正しい**（SUB-18） |
| 「mid+α で T2 が良い＝残差方向が有望」 | ✅ **正しい**（641） |
| 「だから 10.31 は **F015で提出不可**」 | ❌ **過剰** · F015の核は raw promote |
| 「learned 方向 residual は **一切触るな**」 | ❌ **539/641 を殺す誤解** |
| 「mid 系統 FINAL は Public で壊れやすい」 | ✅ **F042/458 として妥当** · 枠2主策にしない / tipdist 監視 |
| CHK-539「F015 risk → promote 禁止」 | ⚠️ ラベル粗い · ゲート上 tip+α(L−tip) は **504型に近い合法候補** |

### 7.4 レーン別規律

| レーン | mid+α(L−m) / residual | 根拠 |
|---|---|---|
| **T2 / Trust 枠1** | **積極的に使える** · 641 系は主候補 | pooled 10.3 · F015違反ではない |
| **Public 枠2 / 診断** | tipdist・形で選別 · 自動差替なし · 641 は **1回** 着弾待ち | 458/18 は遠い mid/L が 7.x |
| **α=1 L だけ / mpkg-only** | **禁止維持** | F015 実証 |
| **tip⊕薄いゲート** | **Public 向き**（541/558b） | tipdist 小 |

### 7.5 1行結論

**F015 自体は妥当。**  
**「残差ブレンド = F015 だから不可」は過大解釈。**  

1. **L/mid/soft の生のみ FINAL** → 禁止（F015/F041/F042）  
2. **合成 residual · tip⊕注入** → 許可（Trust 主、Public は tipdist と実績で判定）  
3. **641 型は T2 合法・診断提出済** · 再提出だけ禁止

