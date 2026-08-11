# 候補生成・学習 穴潰しバックログ — 2026-08-04

> **用途:** 別セッションが **1 CHK ずつ** 実行できる網羅キュー  
> **CVの正:** **T2≈80 pooled**（faces `20260803-114917` 系）· dual **671** · sample3 非悪化 · help/hurt  
> **非尺子:** Public（residual は **679 禁止**）· tipdist 単独  
> **実行 2026-08-04 night:** 697 E2E tipdist 3.298 GO_map · 702 E2E tipdist 4.223 NOGO vs 666 ·
> **実行 2026-08-04 late:** 697b tipdist **3.705 NOGO** · 711 **0.327 GO_map_only** · 730 wave ·
> **実行 2026-08-04 eve:** 695/704/712 **NOGO** · 688 ceiling OPEN gap~5 ·
>
> **実行 2026-08-04:** 643 ladder GO · 診断A GO · 697 w0.50 GO · 702 sample NOGO · 710 GO
>
> **親戦略:** [`t2-upstream-cv-strategy-2026-08-04.md`](t2-upstream-cv-strategy-2026-08-04.md) · Active: [`experiment-checklist.md`](experiment-checklist.md)  
> **L 再学習専用 SSOT（別セッション推奨）:** [`l-relearn-session-guide.md`](l-relearn-session-guide.md)（**CHK-767–780** + 688/761 手順）  
> **S1/S2 既存:** [`s1-s2-hypothesis-backlog.md`](s1-s2-hypothesis-backlog.md)（519–570 と **dup**）  
> **失敗台帳:** [`improvement-loop-failures.json`](improvement-loop-failures.json) **F015 · F033–F035 · F041 · F043 · 620**

---

## 0. 別セッション手順（必ず）

1. 本 MD の **pending 最小優先 P** を1つ取る（同 P なら表の上から）  
2. `run-hypothesis-ban-gate.ps1` **pre**（T3 は `-Mechanism`）  
3. 本尺子 T2 dual · sample3 · hard20 は補助 · residual 成果は **Public 提出しない**  
4. GO/NO-GO を hyperparameter-table + 本 MD status 更新 · checklist Active は要約行のみ  
5. 失敗キーワード確定なら failures に1件（言い換え再実行禁止）

| 項目 | 値 |
|---|---|
| action_type | 診断=T4 · 機構1点=T3 · 外部面=T1 · ブレンドのみ=T2 |
| 提出 | ユーザー明示のみ · residual 既定 **出さない** |
| GPU/Kaggle | ユーザー許可 + 指示ジョブのみ |

---

## 1. 閉鎖（このキューでは **再実行しない**）

| 帯 | 内容 | 参照 |
|---|---|---|
| **C0** | Soft/L/mid **生 FINAL** | F015 · SUB-18 |
| **C1** | GR residual Newton **guided proposal** | **F033** |
| **C2** | ridge ΔTVT → PF rate α混合 | **F034** |
| **C3** | hard専用 tip PF 再生成言い換え · ESS+MCMC 厚化連打 | **F035** 周辺 |
| **C4** | soft→mid 注入 | **620** · 622/623 |
| **C5** | tip\|mid 切替 · 下流 agree/row/HD 微スイープ本命化 | Δ0.062 · 541/558b 梯子済 |
| **C6** | residual **Public 本命** | 641 · **679** |
| **C7** | 真・薄い別面 S1a/S1b 門番再挑戦 | **F041** |
| **C8** | RL 舵切り formal（World Cup 論文直訳） | 提出定義≠操縦 |
| **C9** | 579/541/558b/618c/641/farvol 再提出 | Explicit Stop |
| **C10** | match/heel を 643 より先に再優先 | 650 系 NOGO 多数 |

---

## 2. 穴マップ（工程 × 学習）

```text
[観測尤度 / GR モデル] ── 704–706 · ≠F033
        │
[S0 tip PF 骨格] ── 固定 680 · 厚化は C3
        │
[S1 learned 生成] ── 688–693 · 既知帯教師 · 面のみ
        │
[S2 SP45 / 投影] ── 694–696 · ≡468 ならスキップ
        │
[S3–S8 mid スタック] ── 643→677→673 · 697–701
        │
[載せ方 residual / tip⊕] ── 676 · 709–712 · Public禁止
        │
[別系統・全面] ── 719–720 · コスト最大 · 後回し
```

---

## 3. CHK 表（網羅キュー）

凡例 status: `pending` · `blocked_X` · `applied_rule` · `closed_C*` · `dup_s1s2`

### A. セッション規律（適用済み）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **681** | 0 | **applied_rule** | candgen/learn は **1機構または1学習面**のみ。載荷・ゲート・Public を同ジョブに混ぜない | ジョブ境界メモ1行 | T4 | — |
| **682** | 0 | **applied_rule** | 実行前に **C0–C10** と `improvement-loop-failures` を照合。一致したら即停止 | gate pre PASS または SKIP理由 | T4 | — |

### B. 診断天井・信号位置（T4 · 先行可）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **683** | 0 | **GO** | TRAIN/T2 既知帯で **oracle residual**（真 mid 上で最適 α·方向）と現行 666 の差を測ると、まだ L/mid どちら側の天井か分かる | 天井表1枚 · α\*/方向 | T4 | faces |
| **684** | 0 | **GO** | 井別 **L–tip / L–mid RMSE** と residual **help** の交差で、L改善すべき井 cluster が取れる | 井表 + cluster | T4 | L面 |
| **685** | 0 | **GO_lock** | 643 ladder の **主因1段 + tip_collapse** を固定し、697 以降の改修対象をロックする | harvest JSON · primary_stage | T4 | **643** |
| **686** | 1 | **GO** | tip+oracle-soft 天井（185系）と residual 天井を **同一 T2 faces** で並べ、次に触る生成器が mid / soft材料 / L かを決める | 3ウェイ表 | T4 | soft面 |
| **687** | 1 | **GO** | 既知帯のみ **L vs 真TVT** の MD-quartile 誤差を出し、未知帯ゲートの事前（549更新）にする | quartile 表 | T4 | L面 |
| **722** | 1 | **GO** | residual help/hurt を **井ID RMSE** まで落とし（count だけではなく）676 後比較用 SSOT にする | well RMSE CSV | T4 | 666面 |
| **723** | 2 | **applied_rule** | F033–F035 / 620 を **closed 確定**として本キューに再掲しない（実装禁止・メモのみ） | 本節 §1 | T4 | — |

### C. S1 learned 生成品質（面のみ · 生FINAL禁止）

> **実行手順・L0/L1/L2・新 CHK 詳細は [`l-relearn-session-guide.md`](l-relearn-session-guide.md) のみ**（ここは番号索引）。

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **688** | 0 | **GPU RUNNING v1** | L 再学習で residual が 666 を超える | local dual + 762 · F015 なし | T3 | pretrain-gate · **F043後必須** |
| **761** | 0 | **weights v2 ready** | worst-fold ドライバ井 sample_weight → mean_worst 先下げ | dual vs 一様 688 | T3 | 749 · l-relearn |
| **767** | 0 | **nb_ready** | L0/L1 FAST 雛形で即死を 30 分内に潰す | [`tip-cv-l-fast-h20`](../my-notebook/tip-cv-l-fast-h20/) | T3 ops | l-relearn |
| **769** | 0 | **pending** | LGB-only FAST で方向が見える | L1 dual 方向 = フル方向 | T3 | 767 |
| **771** | 0 | **pending** | 既知帯行のみ強重み | residual dual | T3 | 767 |
| **770** | 1 | **pending** | early-stop + 木 1/3 でも dual 維持 | dual Δ&lt;0.1 | T3 | L1 |
| **772** | 1 | **pending** | 学習ターゲット = **(y−mid)** residual | dual vs 直接 TVT | T3 | L1 |
| **689** | 1 | **pending** | **well-group / pad** CV で偶然井記憶が減る | group-CV 既知RMSE | T3 | 688設計 |
| **690** | 1 | **pending** | loss MAE / rate(ΔTVT) で横断井の L が residual に乗る | residual help↑ / worst↓ | T3 | L1 |
| **773** | 1 | **pending** | hard20 GO 後 balanced80 再学習で一般化 | dual on 80 | T3 | L2 |
| **779** | 1 | **pending after 761** | 761 L1 GO → L2 フル+weights 1 本 | L2 dual + tipdist | T3 | 761 |
| **691** | 2 | **pending** | multi-scale NCC · tortuosity · signed az · landing を **1 群だけ** | dual · tipdist map | T3 | post-761 |
| **774–777** | 2 | **pending** | 2-seed / MD重み / LGB\|CB 単系統 / reg↑ | dual | T3 | L1–L2 |
| **778** | 3 | **pending low** | soft_diag を **特徴**（≠注入） | dual · 620 維持 | T3 | L1 |
| **692** | 1 | **pending after 688** | **再 dump** TRAIN+T2+TEST faces · 676 入口更新 | 面整合 · tipdist | T3 | 688 |
| **693** | 1 | **pending after 692** | 新 L + **旧 mid** residual で **L単独寄与**分離 | residual dual · Public禁止 | T2 | 692 |
| **768 · 780** | 0/2 | **pending** | 3 NOGO で帯切替 · 探索順序 | 運用ログ | T4 | ops |
| **781** | 0 | **pending** | Trust residual-path loss（固定α0.35） | dual vs pure-TVT 学習 | T3 | 666 FINAL 定義 |
| **782** | 0 | **pending** | resid>L 拖井 sample_weight | dual mean_worst | T3 | 766 |
| **783–788** | 1–2 | **pending** | hard∩749 · Huber · field-CV · 未知除外 · multi-task · soft-label | dual | T3 | l-relearn §5.3b |
| **dup** | — | **dup_s1s2** | 524–570 ゲート/注入の再スイープは **しない**（s1-s2 済） | — | — | 519–570 |

### D. S2 SP45 / 投影

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **694** | 2 | **GO_non_equiv** | SP45 が mid468 と **非≡**なら品質 dump が材料になる（≡なら **スキップ**） | ≡判定 · tipdist | T4 | faces |
| **695** | 2 | **NOGO_tipdist** | SP45 soft residual `mid+α(L−m)+β(S−m)` が 666 tipdist を超えない | tipdist≥2.82 ≫1.985 | T2 | 694非≡ |
| **704** | 2 | **NOGO_Trust** | GR **相関雑音**を σ のみに入れると residual が改善する（proposal 非変更） | tipdist↓ map · T2↑（悪化） | T3 | ban F033 |
| **712** | 2 | **NOGO_tipdist_E2E** | Ridge residual 材料を TEST redeploy すると dual で 666 を超える | train OOF甘い · tipdist **4.42** | T3 | ban F015 |
| **696** | 3 | **pending** | SP45 が壊す井だけ mid で ignore する選別が 560 の T2 版で効く | 壊し井リスト + T2 | T4 | 694 |

### E. mid スタック機構（643 主因 · 本命）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **697** | 0 | **GO_t2_e2e_map** | 主工程 **1機構のみ**改修（677 固定）すると mid T2 &lt; 12.279 または tip⊕ 改善 | dual T2 · sample非悪化 | T3 | 643·**677**·≡**673** |
| **698** | 1 | **blocked_697GO** | 主工程 GO 後、**次点 ladder 段だけ**を 1 機構改修（同時2段禁止） | 追加 ΔT2 · 累積 | T3 | 697GO |
| **699** | 1 | **blocked_697** | 主因が **S1–S2** のとき 697= **L/blend 則**に閉じ、S3–S8 を触らない | スコープ監査 + T2 | T3 | 677=S1S2 |
| **700** | 1 | **blocked_697** | 主因が **S3–S8** のとき contact / hedge / scale など **ラベルされた1ノブ**のみ | T2 mid | T3 | 677=mid |
| **701** | 2 | **pending** | 新 mid を SSOT faces 化（672）し、旧 mid と dual 比較ログを1枚にする | faces path + 表 | T4 | 697GO |
| **702** | 2 | **NOGO_sample_and_tipdist_E2E** | 新 mid 上で **676 residual 再格子**（本戦略） | residual T2&lt;9.998 · Public禁止 | T2/T3 | 701 |
| **703** | 3 | **blocked_697NOGO** | 1機構2敗なら **626 全面 mid 再生成**条件を満たすか判定して分岐 | GO定義メモ | T4 | 697/698 NOGO |

### F. 観測尤度・相関モデル（≠ F033 Newton）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **704** | 2 | **NOGO_Trust** | GR **相関雑音**を σ のみに入れると residual が改善する（proposal 非変更） | tipdist↓ map · T2悪化 | T3 | ban F033 |
| **705** | 2 | **pending** | typewell vs 水平 GR の **局所スケール重み**を尤度に入れると接触帯の particle 勝率が上がる | stage ladder 再測 or mid T2 | T3 | 704後可 |
| **706** | 3 | **pending** | 既存 pf_scale の **再重み（mean）**だけで mid 入力が改善する（粒子再生成なし） | mid proxy T2 | T2 | 軽量 |
| **707** | 3 | **closed_C1C2** | 新規 **学習 proposal を PF rate に直接混合**は F033/F034 禁止 · ユーザー Force 時のみ再設計 | Force 文書 | T3 | **原則禁止** |

### G. 粒子力学・ビーム（厚化禁止との境界）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **708** | 3 | **pending** | **beam / top-k 経路（601）**が 643 で主因なら、再オープンして mid T2 を狙う（厚化 seed 連打ではない） | primary=beam · T2 | T3 | 643·≠F035 |
| **709b** | 3 | **closed_C3** | PN スケジュール・区間独立 PF・seed 予算の言い換えは **F035 閉鎖** | — | — | — |

### H. residual 載荷の高度化（mid/L 更新後）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **709** | 1 | **pending_after_676** | **井適応 α**（LOO 井 or trust proxy）が固定 α0.35 を T2 で超える · Public禁止 | T2&lt;676best · hurt非増 | T3 | 676 |
| **710** | 1 | **GO_local** | residual を **hurtリスク高井で α↓** すると sample/hurt が守られ T2 ほぼ維持 | hurt↓ · T2劣化≤ε | T3 | 722 |
| **711** | 2 | **GO_map_only** | residual Trust 面と **tip 薄ブレンド**の dual が 666 単体より tipdist 安全 | tipdist **0.327** · Trust 非本命 | T2 | 676 |
| **712** | 2 | **NOGO_tipdist_E2E** | Ridge residual TEST redeploy が dual で 666 を超える | train OOF甘い · tipdist **4.42** | T3 | ban F015 |
| **713** | 3 | **pending** | 近傍井 TVT prior を **residual 特徴**にだけ使い、T2 screen で寄与を見る（pad CV） | T2 screen · leakage注意 | T4/T3 | pad設計 |
| **714** | 3 | **pending** | 713 を **leave-pad-out** で学習し group 泄漏を潰すと LOO が落ちない | pad-CV 表 | T3 | 713 |

### I. soft / 診断材料（注入禁止）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **715** | 2 | **pending** | soft **品質スコア**をゲート特徴のみに使い（mid注入なし）tip⊕ 診断が 618c より tipdist 安全になる | tipdist &lt; 618c · T2非本命 | T4 | 621面 |
| **716** | 3 | **pending** | soft 方向 residual 単独は 667 NOGO だが、**新 mid 上**で再 screen すると再評価価値がある | T2 vs 667 · Public禁止 | T4 | 701 |
| **717** | 2 | **closed_C4** | soft→mid 再注入は **禁止** | — | — | 620 |

### J. 別系統・全面再設計（後回し）

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **718** | 3 | **pending** | **独立第2生成器**（別 lik スタック）の mid が tip と低相関なら blend 材料になる（F041 薄い別面 ≠） | 相関·T2 dual · 門番 | T3 | コスト大 |
| **719** | 2 | **pending** | **626 全面 mid 再生成**が 703 条件 or 673 2敗後に T2 を更新する | mid T2&lt;12.279 | T3 | 703 |
| **720** | 3 | **applied_rule** | **RL ジオステア formal** は本コンペ提出に使わない（文献は信念推定の参考のみ） | キュー非実行 | T4 | C8 |
| **721** | 0 | **applied_rule** | candgen/learn の GO は **必ず dual 671/672** · 片方雰囲気 GO 禁止 | report dual 必須 | T4 | 671 |

### K. 評価・ops 穴

| ID | P | status | hypothesis | acceptance | type | 依存 |
|---|---|---|---|---|---|---|
| **724** | 1 | **pending** | 新 L/mid 面の **anti-promote CI**（570）を通さないと submission パイプラインに載せない | CI PASS | T4 | 面GO |
| **725** | 2 | **LOCK** | Trust 候補の **Final2 枠1比較表**（tip / 666 / mid材料）を1枚に固定する | farvol+666+697 · 自動差替なし | T4 | 676 |
| **726** | 2 | **pending** | hard20 order flip が起きる面は sample 再監査（678 実行ログ） | flip 有無記録 | T4 | 678 |

---

## 4. 別セッションの「入口」早見

| セッション種別 | 最初の CHK | 終了条件 |
|---|---|---|
| **診断のみ（GPUなし）** | 683 → 684 → 686 → 687 → 722 | 天井表 + 次手1行 |
| **643 harvest後** | 685 → 677 → **697(=673)** | mid T2 GO or 703 |
| **L 再学習** | **[`l-relearn`](l-relearn-session-guide.md)** · 688 → 761/769/771 → 779 → 756 | local dual L1 · 762 · residual（新L後のみ） |
| **残差再格子** | 701 → **702(=676)** → 709/710 | Trust 候補更新 · **Public禁止** |
| **尤度1点** | 704 → （GOなら）700 連鎖か 706 | dual T2 · F033照合 |
| **全面再設計** | 703 → 719 | mid &lt; 12.28 |
| **禁止帯確認** | 682 のみ | 実行しない |

**本命シリアル（Trust）:**  
`643 → 685 → 677 → 697 → 701 → 702 → (709/710) → 725`

**並行可（本命を奪わない）:**  
`683–687 · 694 · 712 screen · 715`

---

## 5. 論文・外部仮説 → CHK 対応

| 外部 | 写像 CHK | しないこと |
|---|---|---|
| PF + GR 尤度（SPE/C&G） | 704–706 · 697 mid | RL 舵切り formal |
| Ridge + residual learning preprint | 712 · residual 系 | 生 residual FINAL 無断 Public |
| mycarta NCC/tortuosity/az | 691 · 特徴 | 単独 LGBM で tip 置換幻想 |
| 近傍井 prior | 713–714 | pad 泄漏 CV |
| soft tip⊕ 診断 | 715 · 618c 済 | 620 注入 |
| GPU PF 移植 | 加速のみ · 新規 CHK 不要 | 別手法と誤認 |

---

## 6. 状態更新ルール

- GO/NOGO は **本表 status + hyperparameter-table 1行**  
- Active checklist は **帯要約**のみ増減（全文コピー禁止）  
- 新規穴を見つけたら **次番 727+** を本 MD に追加し checklist レーン行を1行更新  

---

## 7. 参照

| 内容 | パス |
|---|---|
| checklist Active | [`experiment-checklist.md`](experiment-checklist.md) |
| **L 再学習フロー** | [`l-relearn-session-guide.md`](l-relearn-session-guide.md) |
| 上流 CV | [`t2-upstream-cv-strategy-2026-08-04.md`](t2-upstream-cv-strategy-2026-08-04.md) |
| S1/S2 済 | [`s1-s2-hypothesis-backlog.md`](s1-s2-hypothesis-backlog.md) |
| failures | [`improvement-loop-failures.json`](improvement-loop-failures.json) |
| residual Public | [`latest/ops-lb-chk641-public-2026-08-04.md`](latest/ops-lb-chk641-public-2026-08-04.md) |
