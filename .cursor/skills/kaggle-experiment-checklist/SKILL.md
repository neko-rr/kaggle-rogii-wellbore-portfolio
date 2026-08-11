---
name: kaggle-experiment-checklist
description: >-
  Kaggle コンペの実験を「チェックリスト作成 → 1項目ずつ実験ループ」で進める汎用 Skill。
  Discussion・他者 NB・自チーム結果から **効果あり/なしの仮説** を列挙し、hyperparameter-table と突合して
  無駄な繰り返しを防ぐ。fork 自体は禁止ではないが、checklist には仮説のみ（fork 先は intel/my-notebook）。
  進捗報告だけでターンを終了しない。
  実験ループ、checklist、重複防止、自律実験、Mania 流と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| checklist 関連脚本（短時間） | — | — | exp/ · hyperparameter-table.md | exp/experiment-checklist.md · exp-index.md |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Experiment Checklist

[ml-mania-2026](https://github.com/ledmaster/ml-mania-2026) 由来の **2段構え** を Kaggle 汎用化する。

| フェーズ | やること | 出力 |
|---|---|---|
| **Phase 1: Plan** | 候補収集・重複排除・チェックリスト化 | `exp/experiment-checklist.md` |
| **Phase 2: Execute** | pending を **1項目ずつ** 実験 → 記録 → 次 | `exp-*` + `hyperparameter-table.md` |

要約・Discussion 取得は別 Skill に任せる（本 Skill は **実験の進め方** 専用）。

## fork と checklist の関係（必読）

**fork 自体は禁止ではない。** 他者 Notebook の fork は、多くのコンペで **材料取得・実行環境** として普通に使う（Skill: `kaggle-kernels-runbook` · `kaggle-notebook-folders` · `my-notebook/`）。

| レイヤ | 何を書く | 置き場 |
|---|---|---|
| **intel / 作業** | どの NB を fork するか・優先度 | `exp-intel.md` · `others-notebook-index.md` · `my-notebook/{name}/` |
| **checklist（CHK）** | **何のために fork するか＝検証する仮説** | `experiment-checklist.md` |
| **提出結果** | LB・SUB 履歴 | `exp-infer.md` |

- CHK の **主語は仮説**（手法 × 期待効果）。fork は **材料・前提** として `source:` や acceptance に書いてよい
- ❌ CHK にしない: 「〇〇を fork する」「Run All して提出」**だけ**（検証する主張が無い）
- ✅ CHK にする: 「URAD 7243 fork をベースに task205 graft → official +0.5pt」（fork は手段、graft が仮説）

## 関連 Skill

| Skill | 役割 |
|---|---|
| `experiment-management` | 記録先の判断 |
| `experiment-result-management` | LB/CV 報告時の更新 |
| `notebook-analysis` / `discussion-summary` | 他者情報の入力源 |
| `kaggle-cli-fetch` | Discussion 原文取得 |

---

## Phase 1: チェックリスト作成（Plan）

**いきなり実験しない。** 先に `exp/experiment-checklist.md` を作るか更新する。

### Step 1: 必ず読む

**前提ゲート:** `exp/pre-strategy-gate.md` — PASS まで戦略CHK禁止。  
**CV 前提:** `docs-ja/cv-design.md` の **cv_unit** 宣言（Skill `kaggle-cv-design`）。無ければ Phase 1 で先に作る。  
**knowledge:** prior の axis **A（CV）** を cv-design に突合してから primary CHK を増やす。

1. `docs-ja/comp-strategy.md`（Goal / Bets / Stop — **CHK は Bets と整合**）
2. `exp/exp-index.md` → **`exp/latest/manifest.md`**
3. `exp/exp-intel.md`
4. `exp/hyperparameter-table.md`
5. `exp/exp-train.md` / `exp/exp-infer.md`（直近の rejected 理由）
6. あれば `docs-ja/discussion/`、`docs-ja/others-notebook/`

### Step 2: 候補を収集

| ソース | 取るもの | checklist への書き方 |
|---|---|---|
| `exp-intel.md` | 他者の手法・ablation・効いた/効かなかった | `source: intel` + 参照リンク |
| Discussion | ホスト・上位者の示唆 | `source: discussion/{file}` |
| others-notebook 要約 | 再現候補の抽象化（写経禁止） | `source: notebook/{name}` |
| 自チーム rejected | hyperparameter-table / exp-train | `status: rejected` に移し **retry 禁止** |
| 弱点分析 | カテゴリ別・metric 別の gap | `source: self` |

**抽象化ルール:** 「kienngx の notebook をそのまま」ではなく **1仮説1項目**（例: 「symbol 特化 240 step 短 SFT」「`\boxed{}` 末尾指示の CoT テンプレ追加」）。

### チェックリストに載せないもの（必須 · 誤解防止）

`experiment-checklist.md` は **いま試す仮説の作業キュー（薄い Active）**。fork 禁止ではないが、以下は **CHK 行として載せない**:

| 載せない例（CHK の主語にしてはいけない） | 正しい置き場 |
|---|---|
| `fork uradkr/7243-08` **だけ** · `7243.21 を提出` **だけ** | intel · `my-notebook/` README · `exp-infer.md`（提出時） |
| 提出済み SUB の羅列 · **Best / LB スコア · tip 名の再掲** | **`exp/exp-index.md`（現在地 SSOT）** · 提出詳細は `exp-infer.md` |
| G1/G2 ベースライン確立のみ（改善仮説なし） | **`exp/latest/`** · INF-xxx |
| 他者 NB の DL・要約だけ | **intel 作業** — 要約後に仮説を CHK 化 |
| 「より高い他人 zip を取る」だけ | **仮説ではない** — 取り込み後に patch/blend 等を CHK 化 |
| 終わった Wave の全表 | **`exp/checklist-archive.md`**（または `exp/archive/checklist-*.md`） |

**SSOT / 肥大防止（Rule `kaggle-exp-ssot`）:**

- ヘッダは `exp-index` へのリンクのみ（スコア再掲禁止）
- Active 目安: **〜120 行 · pending 〜15**。超えたら archive へ移す
- ユーザーが checklist を見て指示する場合も、**読む主画面は Active**。Best が必要なら index を開く
- ずれ検知: `scripts/check-exp-ssot.ps1 -CompRoot <root>`

**CHK の `hypothesis` は必ず「手法 × 期待効果」形式。さらに `lane:` 必須。primary は shippable acceptance:**

- ✅ `lane:primary` + acceptance: shippable OOF（cv_unit=…）で改善 · **oracle を引用しない**
- ✅ `lane:diagnostic` + acceptance: 診断完了のみ · **提出 GO に使わない**（oracle/ceiling 可）
- ✅ `lane:diagnostic` **CHK-00S** shape smoke（id/列/短 run）· 性能は見ない · **性能 CHK より前**
- ✅ `lane:public` Public 指標のみ · primary の代替にしない
- ❌ unit 未宣言の CV 改善を Best 採用
- ❌ oracle/ceiling だけで Final / primary GO
- ❌ lane 無しで「LB が落ちたから全部止める」

**定型文 SSOT:** `_shared/CV-DESIGN.md` §2 · Skill `kaggle-cv-design` · `docs-ja/cv-design.md`  
**レーン:** `_shared/LANES-AND-FINAL-SLOTS.md`

**他者 notebook から checklist へ入れる手順:** notebook 要約 → **抽象化した仮説** → dedupe → CHK。notebook 名は `source:` にのみ書く。

### Step 3: 重複排除（必須）

新規項目を追加する前に、次と **意味が同じ** でないか確認する:

| 参照 | 確認内容 |
|---|---|
| `hyperparameter-table.md` | 同一設定・同一 notebook・同一 adapter パス |
| checklist `done` / `rejected` · **archive** | 同一 `hypothesis` または同一 `item-id` 系 |
| `exp-train.md` / `exp-infer.md` | 同じ experiment ID の結論 |

重複なら **新規行を作らない**。必要なら既存行に `note:` を追記。

**rejected の再登録:** 仮説が ** materially 変わった** 場合のみ（新 item-id、旧 ID への `supersedes:` 参照）。

### Step 4: チェックリストファイルを書く

テンプレート: [checklist-template.md](checklist-template.md) · archive: `comp/exp/checklist-archive.md.template`

Phase 1 完了条件:

- [ ] pending が `comp-strategy.md` の **Stop · compass** と矛盾していない
- [ ] 全 pending に `hypothesis` / `source` / `acceptance` / **`lane`** が書いてある
- [ ] primary の acceptance が **shippable** 定型（oracle 非引用）である / diagnostic は diagnostic 定型
- [ ] **CHK-00S shape smoke** が性能 primary より前（または N/A 理由）
- [ ] `docs-ja/cv-design.md` の **cv_unit** と矛盾しない
- [ ] knowledge axis A を cv-design に突合した（またはカード無し明記）
- [ ] rejected に載っているものが Active pending に混ざっていない
- [ ] `exp-index.md` の「次アクション」に checklist Active へのリンク
- [ ] checklist ヘッダに Best/LB スコアを書いていない
- [ ] Final 前チェック節がある（N は timeline · 推測しない）

---

## Phase 2: 実験ループ（Execute）

### Agent 行動規則（必須）

0. **仮説禁止ゲート（汎用）** — 重い実験の前に  
   `.\scripts\run-hypothesis-ban-gate.ps1 -ChkId CHK-xxx -ActionType T0|T1|T2|T3|T4 -Hypothesis "..." -Phase pre`  
   （T3 は `-Mechanism` 必須）。**exit 0 のときだけ**本実験へ。Rule: `kaggle-hypothesis-ban-ledger`  
   結果後: `-Phase post -Verdict GO|NOGO`。台帳: `exp/improvement-loop-failures.json`（開始時は空）  
0b. **CV unit** — primary 本実験前に `docs-ja/cv-design.md` の unit と矛盾しないか確認（Skill `kaggle-cv-design`）  
0c. **shape smoke** — 未 PASS なら性能 primary を in-progress にしない（CHK-00S または validator）  
0d. **static-check（コードあり CHK）** — Agent が `.py`/`.ipynb` を書いたら  
    `.\scripts\run-static-checks.ps1 -Path <触ったファイル…>` が **exit 0** するまで本実験・kernels 禁止  
    （**Cursor Ruff 拡張は代替不可** · Skill `kaggle-static-check` · SA-8）
1. **1項目ずつ** — Active の先頭（または priority 最高）から **1 仮説**。着手前に **lane** を確認し、判定は **当該 lane の acceptance のみ**
2. **記録してから次** — 項目完了時に必ず更新:
   - **必須:** `exp/experiment-checklist.md`（当該 Active 行の status）
   - **必須:** `exp/hyperparameter-table.md`（実験 ID）
   - **必須:** `exp/exp-train.md` または `exp/exp-infer.md`
   - **条件付き:** `exp/exp-index.md` — **Best 更新・方針転換・次アクション変更時のみ**（毎 CHK でスコアを書き直さない）
3. **done を Active に残さない** — 完了行は早めに `checklist-archive.md` へ移す（Wave 終了時は一括で可）
4. **partial progress でターン終了禁止** — 状況報告だけで止めない。次の **実行可能ステップ**（コード編集・Metric 実行・checklist 更新）まで進める
5. **validation-only デフォルト** — ルーティン実験はローカル CV / Metric のみ。LB 提出・大容量 artifact 保存は **accept 時またはユーザー明示時**（提出は **Notebook 紐づけ** · `NOTEBOOK-LINKED-SUBMIT.md`）
6. **同一仮説の量産禁止** — 1項目内で微差 200 個より、**意味のあるバリエーション少数**（コンペに応じ 3〜10 本）。acceptance を満たさなければ `rejected`  
   抽象失敗が確定したら `improvement-loop-failures.json` に **`id: Fnnn`**（禁止）と keywords を追記する。  
   **F ≠ 知見。** 学びは LES / harvest→KGL（`_shared/EXPERIMENT-ID-NAMESPACES.md`）

### 1項目の実行手順

```
1. checklist Active で CHK-xxx を in-progress に
2. コードを書いた・直したら `.\scripts\run-static-checks.ps1` → **PASS 必須**
3. 実験実行（train / infer / Metric / CV）
4. acceptance 判定
5. 当該行 + table + train/infer 更新（index は Best/次アクション変化時のみ）
6. in-progress → done または rejected（できれば直後に archive へ）
7. pending が残れば 1 に戻る（ユーザーが停止指示するまで）
```


### 改善ループゲート（コンペ固有がある場合のみ）

汎用は **`run-hypothesis-ban-gate.ps1`**（空の failures 台帳から開始）。  
**本コンペに** Rule `kaggle-local-improvement-loop` や固有ゲート脚本がある場合だけ、その SSOT に従う（テンプレ標準ではない）。

| 段 | 脚本 | 条件 |
|---|---|---|
| pre | `run-hypothesis-ban-gate.ps1 -Phase pre` | 台帳非一致 · T3 なら mechanism 必須 |
| post | `-Phase post -Verdict GO\|NOGO` | streak 更新 |

SSOT: `exp/improvement-loop-failures.json` · Rule `kaggle-hypothesis-ban-ledger`

### 敵対的検証（高コスト判定 · SA-7）

**毎 CHK では起動しない。** 詳細: `_shared/ADVERSARIAL-REVIEW.md` · Skill `kaggle-adversarial-review`

| 直前の作業 | mode |
|---|---|
| primary Bet / Wave 方針の大きな変更 | `pre-bet` |
| Final / 有効枠の決定 · 入替 | `pre-final` |
| 他者 · 外部の本採用（T1） | `pre-adopt` |
| cv_unit / fold 固定 | `pre-cv-lock` |
| knowledge harvest で横断カード量産 | `pre-harvest` |

親は `/kaggle-adversarial-review` を起動し **Verdict** を読む。KILL/CHALLENGE なら仮説を直す。GO は親+ユーザー。  
代替: 同一 kill-list を親が自問して埋める（ログに `adversarial: self-check`）。

### acceptance（コンペごとに checklist 行に明記）

汎用例:

| 条件 | 例 |
|---|---|
| メトリクス改善 | CV +0.5pt、または LB Best 更新 |
| サブセット非悪化 | 弱点カテゴリが -X pt 以内 |
| 再現性 | 同一 seed / 同一 Metric パラメータ |
| 提出ゲート | extract/verify QA ≥ 99%（推論コンペ） |

**mean だけ改善** でサブセットが壊れる場合は `rejected`（Mania の 4/5 fold ルールと同型）。

---

## チェックリスト項目 ID · 名前空間

**横断 SSOT:** `_shared/EXPERIMENT-ID-NAMESPACES.md` · Rule `kaggle-experiment-id-namespaces`

| 接頭 | 意味 | 置き場 |
|---|---|---|
| **CHK-nnn** | **仮説検証チケット**（Active の行） | `experiment-checklist.md` |
| **Fnnn** | **禁止確定のみ**（Failure）。知見ではない | `improvement-loop-failures.json` |
| **T0–T4** | 実験の型 | ban gate |
| **LES-** | コンペ内の学び（任意） | retro / latest — F にしない |
| **KGL-** | 横断知見カード | `knowledge/` |

形式: `CHK-{3桁}`（例: `CHK-001`）。  
型失敗が確定したら **CHK の rejected だけでは不十分** → **Fnnn を failures に追記**（`source_chk: "CHK-xxx"`）。

| フィールド | 必須 | 説明 |
|---|---|---|
| `hypothesis` | Yes | 1文の仮説（手法 × 期待効果） |
| `source` | Yes | intel / discussion / notebook / self |
| `priority` | Yes | high / medium / low |
| `acceptance` | Yes | 採用条件（数値またはチェックリスト） |
| `dup-check` | Yes | 照合した table ID または「新規」 |
| `action_type` | Yes（重い実験） | T0〜T4（仮説禁止ゲート用） |
| **`lane`** | **Yes** | **primary / public / diagnostic**（別名は strategy） |
| `status` | Yes | pending / in-progress / done / rejected |

**禁止:** CHK 行 ID を `F001` にする · F を Finding と呼ぶ · 学びを F 台帳に載せる · **lane 無し GO/NO-GO** · **他レーン悪化だけで全体停止**。

---

## ユーザー依頼別フロー

| 依頼 | フェーズ |
|---|---|
| 「次に何を試すべき？」 | Phase 1（checklist 無ければ作成）→ **Active** pending 上位を提示 |
| 「チェックリストを作って / 更新して」 | Active 行の更新が主。Best は触らず `exp-index` を指す。done の山は archive へ |
| 「実験を回して」 / 「ループして」 | Phase 2（checklist 必須。無ければ Phase 1 から） |
| 「Discussion から候補を足して」 | Phase 1 更新（intel 取込後に dedupe） |

---

## 品質チェック

- [ ] **Final / 枠決めの直前に SA-7**（`pre-final`）または同 kill-list 自問
- [ ] 全完了 CHK に **lane** があり、他レーン小差だけで止めていない
- [ ] rejected 項目をそのまま再実行していない
- [ ] 型失敗確定分は **Fnnn** が failures にある（CHK rejected だけで終わっていない）
- [ ] F を Finding / 知見として使っていない
- [ ] hyperparameter-table と checklist の experiment ID が対応している
- [ ] 他者手法は **抽象化** され写経項目になっていない
- [ ] **fork / 提出 / DL だけを CHK の主語にしていない**（仮説＋acceptance がある。fork は材料として可）
- [ ] 1ターンで複数 CHK を in-progress にしていない
- [ ] 項目完了前に Active 行と exp 記録を更新した
- [ ] checklist ヘッダに Best/LB を再掲していない（任意: `check-exp-ssot.ps1`）

---

## 追加リソース

- テンプレート: `%USERPROFILE%\.cursor\kaggle-template\comp\exp\experiment-checklist.md.template`（**唯一の本文正本**）
- Skill 内 [checklist-template.md](checklist-template.md) は **正本へのリンクのみ**（二重管理禁止）
- archive テンプレ: `%USERPROFILE%\.cursor\kaggle-template\comp\exp\checklist-archive.md.template`
- Phase 1 用プロンプト断片: [checklist-plan-prompt.md](checklist-plan-prompt.md)
- 判定地図: `_shared/DECISION-FLOW.md`
- ずれ検知: `%USERPROFILE%\.cursor\kaggle-template\root\scripts\check-exp-ssot.ps1`