# AGENTS.md — rogii-wellbore （legacy ops map）

> **Portfolio 入口はリポジトリ根の [README.md](README.md) です。**  
> 本ファイルはコンペ中のエージェント運用地図（厚い）です。公開 A では後続 Wave で短縮または退避予定。  
> Private 全史: GitHub `neko-rr/kaggle-rogii-wellbore-geology-prediction`（Private）。

---

## コンペ基本情報

| 項目 | 内容 |
|---|---|
| **コンペ名** | ROGII - Wellbore Geology Prediction（rogii-wellbore） |
| **URL** | https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction |
| **comp-type** | **tabular**（Code Competition · 副タグ: well-group-cv） |
| **締切** | 最終提出 2026-08-05（詳細: `docs-ja/comp-timeline.md`） |
| **提出形式** | Notebook → **`submission.csv`**（`id,tvt`） |
| **pretrain-profile** | **tabular** |
| **submission-profile** | **csv** |

### コンペ概要

水平坑井の軌道・検層と垂直参照ログ（Typewell）から、評価区間の **TVT（True Vertical Thickness）** を予測し、ジオステアリング自動化に寄与する Featured Code Competition。詳細: `docs-ja/conditions.md` · `docs-ja/dataset.md`

### 評価指標

**RMSE**（行単位の `tvt`）。提出列は `id,tvt`。

### Public / Private Leaderboard（公式）

> This leaderboard is calculated with approximately **26%** of the test data.  
> The final results will be based on the other **74%**, so the final standings may be different.

- **Public** ≈ テストの 26%（進行中に見える）· **Private** ≈ 74%（最終順位）
- 詳細: `20260722-rogii-wellbore/docs-ja/conditions.md` · `docs-ja/cv-lb-private-relation.md`

### コンペタイムライン / 提出制約 / メダル

締切・提出上限・有効枠の **SSOT**: `20260722-rogii-wellbore/docs-ja/comp-timeline.md`  
Skill: **`kaggle-comp-timeline`** · **`kaggle-competition-constraints`**  
常時 Rule: **`kaggle-comp-constraints`** · `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md`  
**現フェーズ要約:** **コンペ終了**（最終提出 2026-08-05 23:59 **UTC** 済）。実験停止。  
終了後分析: `20260722-rogii-wellbore/retro/`（Skill `post-comp-retro-setup`）。  
Private **#594 / 6125** → **Bronze**（Gold≤22 · Silver≤306 · Bronze≤612）。1日上限はこのコンペでは **5/day**（Overview · 他コンペ既定ではない）。

### 3段ゲート（軽量）

常時ルール: `.cursor/rules/kaggle-three-gates.mdc`  
詳細 SSOT: `docs-ja/pretrain-acceptance.md`, `kernels-runbook.md`, `submission-rules.md`

**F013/F015（過大禁止注意）:** 生中間の FINAL 昇格と tip プロファイル切替のみ禁止。S1/S2 工程改善・ゲートは可。  
SSOT: `20260722-rogii-wellbore/docs-ja/f015-f013-correct-reading.md` · Rule `kaggle-f015-f013-mid-stage` · 仮説 `exp/s1-s2-hypothesis-backlog.md`

---

## 現在のベスト記録（Kazeneko）

| 項目 | 値 |
|---|---|
| **Public LB** | （SSOT: `exp/exp-index.md` · 詳細 `docs-ja/leaderboard.md`） |
| **順位** | （SSOT: `exp/exp-index.md`） |
| **提出回数** | （SSOT: `exp/exp-index.md`） |
| **Private LB** | **9.142 · #594 / 6125**（[`retro/retro-private.md`](20260722-rogii-wellbore/retro/retro-private.md)） |

### コンペ型ルーティング

Skill: **`kaggle-comp-router`** — 型判定と Skill 選択。詳細: `docs-ja/comp-profile.md`

---

## 開発ワークフロー

### トレーニング環境

- **自作 Kaggle 資産は常に Private**（Rule `kaggle-private-assets.mdc` · `assert-kaggle-private.ps1`）
- **Kaggle/Colab 起動はユーザー許可 + 対象ジョブ指示の両方が必要**。Kaggle は CPU最大5枠 / GPU最大2枠を並列実行可能だが、未指示ジョブで空きを埋めない
- **CLI 書込は固定手順:** preflight → metadata/path → Private assert → `kaggle-cli.ps1`。生の `kaggle` とパス省略 push は禁止

- 重い学習は **Kaggle Notebook / Google Colab / クラウド GPU**
- Cursor はローカルで **Notebook 編集・実験記録・Agent 支援**

### 推論・提出環境

- Kaggle Notebook またはコンペ指定の提出形式に従う
- **提出はできるだけ Notebook 紐づけ**（UI「Submit to Competition」または CLI `-k` / `-v` · **自 kernel のみ**）
- ローカル zip/csv の **`-f` のみは非推奨**（Kaggle 上で提出コードが見れなくなる）
- SSOT: `.cursor/skills/_shared/NOTEBOOK-LINKED-SUBMIT.md` · **403 時 zip-only 禁止**
- Agent は `competitions submit` を実行しない（ユーザー操作）

### Cursor 起動

```powershell
.\scripts\open-kaggle-light.ps1
```

Profile: `Kaggle-Light`（`Kaggle.code-workspace` は使わない）

**Kaggle Skill は `<comp-root>/.cursor/skills/` のみ。** `~/.cursor/skills/` には置かない（Web 開発と分離）。

### Kaggle CLI

- Skill: `kaggle-cli-fetch`（Discussion 取得 → `docs-en/discussion/` → `discussion-summary` で要約）
- セットアップ: `%USERPROFILE%\.cursor\skills\kaggle-cli-fetch\setup.md`
- **dataset のダウンロードはユーザー指示時のみ**（Agent は勝手に実行しない）

---

## プロジェクト構成

```
rogii-wellbore/
├─ AGENTS.md
├─ .gitignore               # dataset / 秘匿情報除外（GitHub 公開想定）
├─ .vscode/
├─ scripts/
├─ cursor.md
└─ 20260722-rogii-wellbore/
    ├─ dataset/                 # 公式データ（編集禁止・手動 DL 先・Git 除外）
    │  ├─ README.md
    │  └─ derived/              # 自前加工（Git 除外）
    ├─ exp/                     # 実験結果（コンペ中 · 終了後は凍結）
    ├─ retro/                   # 終了後振り返り（索引: retro-index.md）
    │  └─ archive/              # 解法 · 他者 NB セット保管
    ├─ my-notebook/                 # WIP（Cursor が編集）
    │  └─ planned/                # 作成済み・未実行・実行後回し
    ├─ my-local-eval-notebook/      # 検証専用（提出しない）
    ├─ my-ran-notebook/            # 実行済み・未提出
    ├─ my-submitted-notebook/      # 提出済み（編集禁止）
    ├─ others-notebook/
    ├─ docs-ja/
    │  ├─ comp-profile.md         # コンペ型・Skill マップ SSOT
    │  ├─ comp-timeline.md
    │  ├─ metric-repro.md          # Metric ローカル再現
    │  ├─ agent-debug.md           # simulation 失敗解析（他型は inactive）
    │  ├─ pretrain-acceptance.md
    │  ├─ kernels-runbook.md
    │  ├─ submission-rules.md
    │  ├─ pretrain-gates/
    │  └─ submission-validations/
    ├─ sim-track/                  # simulation メタ追跡（休眠可）
    └─ docs-en/
```

---

## 命名規則

**フォルダ名・ファイル名は同じ法則: 小文字 + ハイフン（kebab-case）**

| 例 | ルール |
|---|---|
| `exp/exp-index.md` | 小文字 + ハイフン |
| `my-notebook/` | 小文字 + ハイフン |
| `hyperparameter-table.md` | 小文字 + ハイフン |

例外（ツール固定）: `AGENTS.md`, `SKILL.md` のみ大文字。

---

## 実験結果管理

実験管理Markdownは **4ファイル構成** にする。

| ファイル | 役割 |
|---|---|
| `20260722-rogii-wellbore/exp/exp-index.md` | 索引・現在地・Best・次アクション |
| `20260722-rogii-wellbore/exp/exp-train.md` | 学習、CV、fold、データ、モデル、loss、特徴量 |
| `20260722-rogii-wellbore/exp/exp-infer.md` | 推論、後処理、提出、LB、submission notebook |
| `20260722-rogii-wellbore/exp/exp-intel.md` | 他者Notebook、Discussion、上位解法、外部知見 |
| `20260722-rogii-wellbore/exp/experiment-checklist.md` | **仮説検証** CHK ループ（fork は `my-notebook/` で可 · CHK は目的） |
| `20260722-rogii-wellbore/exp/within-stage-comparisons.md` | **工程内比較グラフ**（恒常 · Canvas `within-stage-comparisons`） |

- Agent は最初に `exp-index.md` を読む
- 学習結果は `exp-train.md`、推論・提出結果は `exp-infer.md` に分ける
- 他者由来の知見は `exp-intel.md` に置き、自チーム実測と混ぜない
- ハイパラ・提出ログの表は `exp/hyperparameter-table.md` に集約
- **実験候補・ループ** は `exp/experiment-checklist.md`（**仮説の検証リスト** · fork 自体は `my-notebook/` で可）+ Skill **`kaggle-experiment-checklist`**
- **工程内比較** は `exp/within-stage-comparisons.md` + Canvas（更新:「工程内比較グラフを更新して」· Rule `kaggle-within-stage-graph`）

**コンペ終了済:** 終了後分析は `20260722-rogii-wellbore/retro/`（Skill: `post-comp-retro-setup` · 索引 [`retro-index.md`](20260722-rogii-wellbore/retro/retro-index.md)）。`exp/` は凍結（Private 確定値の `exp-infer` 追記のみ可）。`retro/archive/` に他者 NB と解法をセット保管。

| ファイル | 役割 | Skill |
|---|---|---|
| `retro/retro-index.md` | 終了後分析の索引・キュー | `post-comp-retro-setup` |
| `retro/retro-private.md` | 自チーム Private / 枠選択 / shake-up | `post-comp-private-retrospective` |
| `retro/retro-leaderboard.md` | コンペ全体 LB | `leaderboard-analysis` |
| `retro/retro-solutions.md` | 上位解法の統合分析 | `solution-analysis` |
| `retro/retro-lessons.md` | 次コンペへの教訓 | + `kaggle-knowledge-harvest` |

### 横断知見・インフラ（Private Git）

| 資産 | 正本 | ローカル |
|---|---|---|
| **知見** | Private [`neko-rr/kaggle-knowledge-store`](https://github.com/neko-rr/kaggle-knowledge-store) | ワークスペース根の `knowledge/`（nested git · outer `.gitignore` 除外） |
| **Skills / rules マスター** | Private [`neko-rr/kaggle-infra`](https://github.com/neko-rr/kaggle-infra) | `%USERPROFILE%\.cursor\kaggle-template\` |

- **新しいコンペの Agent は knowledge clone/pull があれば足りる**（rogii 本体を GitHub に置く必要はない）
- harvest / promote 後は **knowledge-store へ push**（audit PASS 後）
- 手順 SSOT: [`.cursor/skills/_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`](.cursor/skills/_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md)
- Rule: `kaggle-knowledge-isolation` · Skills: `kaggle-knowledge-retrieve` / `harvest` / `sync` / `promote`

---

## エージェント向け禁止事項

- `dataset/` 内の公式データを編集しない
- **`dataset/` へのダウンロードを Agent が勝手に行わない**（ユーザー明示指示時のみ。容量超過に注意）
- **`dataset/` および派生データを Git / GitHub にコミット・push しない**（ライセンスリスク）
- **`knowledge/` を outer Public リポや knowledge-store 以外の public へ載せない**（Private 専用）
- 秘匿情報（API キー、`kaggle.json`、`.env`）を Notebook や Git に含めない
- コミット前: Skill **`kaggle-git-security`** / `scripts/check-staged-secrets.ps1`
- 自律実験: Skill **`kaggle-experiment-checklist`** — checklist 無しで実験ループを開始しない
- **長時間学習前:** Skill **`kaggle-pretrain-gate`** PASS 必須
- **提出前:** Skill **`kaggle-submission-validator`** PASS 必須。validator 無しで `my-submitted-notebook/` を凍結しない

