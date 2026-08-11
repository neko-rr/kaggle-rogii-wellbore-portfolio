---
name: kaggle-comp-bootstrap
description: >-
  Kaggle コンペ開始時の標準構成を new-kaggle-comp.ps1 で生成する Skill。
  comp-type と 3段ゲート SSOT の初期化まで含める。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| new-kaggle-comp.ps1 · init-comp-layout.ps1 · sync 系（ユーザー指示時） | — | — | kaggle-template/ · scripts/templates/ | comp-root 初期 tree · docs-ja/ テンプレ |

**要ユーザー明示 OK:** git init · GitHub 公開

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle コンペ Bootstrap

優秀な Kaggler 視点で、**コンペ開始の儀式をスクリプト1本に固定**する。

## 前提

| 項目 | 内容 |
|---|---|
| Profile | `Kaggle-Light`（PC ごとに1回 Import） |
| テンプレート | `%USERPROFILE%\.cursor\kaggle-template\` |
| 起動方法 | **フォルダ + `--profile Kaggle-Light`**（推奨） |
| 命名規則 | **フォルダ・ファイルとも小文字 + ハイフン（kebab-case）** |
| `Kaggle.code-workspace` | **不要**（チャット履歴が分断されるため使わない） |

### Skill の置き場所（Web 開発との分離）

| 場所 | Kaggle Skill |
|---|---|
| **`~/.cursor/skills/`（グローバル）** | **置かない** — Web 開発時も Agent に載るため |
| **`kaggle-template/root/.cursor/skills/`** | **マスター** — Private **`kaggle-infra`** の clone 先 |
| **`<comp-root>/.cursor/skills/`** | `new-kaggle-comp.ps1` がテンプレからコピー |

**インフラ master（Private）:** `https://github.com/neko-rr/kaggle-infra`  
ローカル: `%USERPROFILE%\.cursor\kaggle-template\`  
並行コンペ同期: `scripts\sync-project-infra-from-template.ps1`

```powershell
# グローバルに Kaggle Skill が残っている場合（1回）
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\archive-global-kaggle-skills.ps1"

# マスター更新後、既存コンペへ反映（並行コンペは CompRoot を列挙）
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<comp-root1>", "<comp-root2>"
```

**Web 開発プロジェクト** には `kaggle-three-gates.mdc` も Kaggle Skill も置かない。  
**Kaggle 作業時** は `open-kaggle-light.ps1` でコンペ ROOT を開く。


### 新コンペ開始（最優先）

```powershell
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\new-kaggle-comp.ps1" `
  -Name "<comp-slug>" `
  -Url "https://www.kaggle.com/competitions/<slug>" `
  -Deadline "YYYY-MM-DD"
```

1. スクリプト実行前に `-Name` が既存フォルダと衝突しないか確認
2. 実行後 **`init-comp-layout.ps1`** で整理 SSOT を一括配置（下記「レイアウト初期化」）
3. **`new-kaggle-comp.ps1` は Cursor hooks + agents を自動配置**（`install-cursor-infra.ps1`）。未配置時は手動実行
4. 生成物を確認（`AGENTS.md`, `.gitignore`, `{日付}-{slug}/lifecycle-manifest.md`, `docs-ja/folder-map.md`, `docs-ja/comp-start-checklist.md`, `exp/exp-index.md`, `docs-ja/comp-profile.md`, **`.cursor/hooks.json`**, **`.cursor/agents/`**）
5. `dataset/` は **ユーザーが手動で** データを入れる（Agent は指示がない限りダウンロードしない）
6. `AGENTS.md` のコンペ概要・**comp-type**・評価指標をユーザー入力で追記（Skill: `kaggle-comp-router`）
7. **`docs-ja/comp-timeline.md`** を Skill `kaggle-comp-timeline` で初版（`conditions.md` と同時）  
   - **必須:** 1 日提出上限 · 有効 LB / Final 枠 · 締切 **UTC**  
   - **他コンペの数字を転記しない** · 未確認は `要確認`  
   - メダルは N が分かれば「メダル帯」節（Skill **`kaggle-competition-constraints`** · `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md`）  
   - Rule **`kaggle-comp-constraints`** が `.cursor/rules/` にあること（alwaysApply）
8. **`docs-ja/comp-strategy.md`** を初版（レーン · Final N · compass — Skill `kaggle-lanes-final-strategy`）  
8b. **`docs-ja/cv-design.md`** を初版（**cv_unit** · shippable · knowledge A · smoke — テンプレ `comp/docs-ja/cv-design.md.template` · Skill **`kaggle-cv-design`**）。  
    prior retrieve 後に axis A を突合して埋める
9. **`docs-ja/pretrain-acceptance.md`**, **`kernels-runbook.md`**（`comp/docs-ja/kernels-runbook.md.template`）, **`submission-rules.md`**（`scripts/templates/submission-rules.md.template` · **Notebook 紐づけ提出**は `_shared/NOTEBOOK-LINKED-SUBMIT.md` — 方式 2b `kernels push` 含む）, **`license-ledger.md`** を概要作成時に初版（3段ゲート + ライセンス BOM）
10. **Private 必須（Day 0）:** Rule **`kaggle-private-assets.mdc`** が `.cursor/rules/` にあること · `scripts/assert-kaggle-private.ps1` があること · 自作 Kernel/Dataset/Model は **常に Private**（`is_private` / `isPrivate: true`）。`datasets create --public` 禁止（`kaggle-cli.ps1`）
11. **`experiment-checklist.md`** に **§実行制約** を追記（ユーザー許可 + 対象ジョブ指示が必要 · Kaggle CPU最大5枠 / GPU最大2枠 · 全自作資産 Private）
12. **CPU / GPU / Colab:** Skill **`kaggle-kernels-runbook`** §実行レーンの承認 — 指示済みジョブだけを上限内で並列化し、未指示ジョブで空きを埋めない
13. **知見ストア（Private knowledge-store）:**  
    - repo ルートに `knowledge/store.json` が無ければ  
      `git clone https://github.com/neko-rr/kaggle-knowledge-store.git knowledge`  
      （`$env:KAGGLE_KNOWLEDGE_GIT_URL` で上書き可）。**空の `knowledge init` で新 store_id を作らない**  
    - 既にあるなら `cd knowledge; git pull`  
    - 代替: Skill `kaggle-knowledge-sync`（Git 無し peer · ドライラン→Apply）  
    - 詳細: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`
14. **過去知見:** `comp-profile.md` 確定後、Skill `kaggle-knowledge-retrieve`（開始直後は **`-IncludeCandidates`**）。  
    prior は domain → **A→C→B** → apply/avoid。自動 CHK 化しない
15. **戦略前ゲート:** 知見 retrieve の次に Skill `kaggle-pre-strategy-gate` — `exp/pre-strategy-gate.md` を comp-type で確定し、`scripts/check-pre-strategy-gate.ps1` **PASS まで戦略CHKを作らない**
16. **提出既定:** Notebook 紐づけ（`NOTEBOOK-LINKED-SUBMIT.md`）。zip/csv 直 `-f` のみは非推奨
17. **テンプレ差分:** 任意で `.\scripts\check-template-drift.ps1 -CompRoot .`（欠落検知）
18. **任意:** 工程分離が必要なコンペのみ `docs-ja/gpu-execution-split.md` を新設（手順の恒久 SSOT · Wave 結果は `exp/latest/handoff-*.md` に分離）
19. **`docs-ja/comp-start-checklist.md`** を上から `[x]`（Agent は未完了を報告 · **Private / GPU 方針**の項を含む）
20. 初回のみ PC で `Kaggle-Light` Profile Import 済みか確認
21. Git 利用時: `-InitGit` または `git init` → `scripts/install-git-hooks.ps1`（Skill: `kaggle-git-security` · pre-commit は secrets + **ps1 UTF-8 BOM**）
22. **PS1 BOM:** `.\scripts\check-ps1-utf8-bom.ps1` が PASS（Rule `kaggle-ps1-utf8-bom` · FAIL 時は `-Fix`）
23. **ローカル計算依存:** 内側 `requirements-local.txt` を編集 → `.\scripts\setup-comp-venv.ps1 -CompRoot <inner>`（Skill `kaggle-comp-deps` · CLI のみなら `setup-kaggle-venv` で足りる）
24. **Cursor: Developer → Reload Window**（hooks 初回配置後）

### レイアウト初期化（必須 · 混乱防止）

`new-kaggle-comp.ps1` の直後に **必ず** 実行:

```powershell
cd <repo-root>
.\scripts\init-comp-layout.ps1 `
  -CompRoot "<repo-root>\<YYYYMMDD>-<slug>" `
  -CompType auto   # comp-profile 確定後 simulation 等に合わせて再実行可
```

| 生成物 | 役割 |
|---|---|
| `lifecycle-manifest.md` | コード成果物索引 |
| `docs-ja/folder-map.md` | **置き場所 SSOT**（Agent 最初の1枚） |
| `docs-ja/comp-start-checklist.md` | Day 0 チェックリスト |
| `exp/README.md` · `exp/latest/manifest.md` | 分析 4 層 |
| 各 `my-*-notebook/README.md` | lifecycle ルール |
| `sim-track/`（`-CompType simulation` 時） | LB · 公開 NB メタ |

テンプレ SSOT: **`scripts/templates/`** · 状態遷移: **`.cursor/skills/_shared/ARTIFACT-LIFECYCLE.md`**

**Skill / Rules / hooks / テンプレ改修:** Skill **`kaggle-workflow-maintainer`** — Kaggle 系はグローバル `~/.cursor/skills/` に置かない。

**新 Skill 追加時:** `scripts/skill-permissions-map.json` に permissions 行を足し、`.\scripts\sync-skill-permissions.ps1` を実行（SSOT: `.cursor/skills/_shared/PERMISSIONS.md`）。

### 既存コンペフォルダを開く

```powershell
& "<comp-root>\scripts\open-kaggle-light.ps1"
```

`Kaggle.code-workspace` は開かない。

### Profile 未 Import の PC

1. `.vscode/profiles/Kaggle-Light.code-profile` を Import
2. フォルダを `open-kaggle-light.ps1` で開く

## 生成される標準構成

```
<comp-root>/
├─ AGENTS.md
├─ .gitignore                 # dataset / 秘匿 / 大容量成果物を除外
├─ .githooks/
│   └─ pre-commit
├─ cursor.md
├─ .cursor/
│   ├─ rules/                 # kaggle-three-gates.mdc · **kaggle-private-assets.mdc**
│   ├─ skills/                # ★ Kaggle Skill 一式（グローバルに置かない）
│   ├─ hooks.json             # Cursor Agent hooks 設定
│   ├─ hooks/                 # install-cursor-hooks.ps1 で配置
│   └─ agents/                # カスタムサブエージェント（install-cursor-agents.ps1）
├─ .vscode/
├─ scripts/
│   ├─ open-kaggle-light.ps1
│   ├─ install-git-hooks.ps1
│   ├─ install-cursor-infra.ps1   # hooks + agents 一括
│   ├─ install-cursor-hooks.ps1
│   ├─ install-cursor-agents.ps1
│   ├─ test-cursor-hooks.ps1
│   ├─ init-comp-layout.ps1
│   ├─ check-staged-secrets.ps1
│   └─ templates/
│       ├─ cursor-hooks/      # hooks SSOT
│       └─ cursor-agents/     # subagents SSOT
└─ {YYYYMMDD}-{slug}/
    ├─ lifecycle-manifest.md      # 成果物状態索引（scripts/templates/ から）
    ├─ dataset/                 # ★ コンペ開始時に空で作成（手動 DL 先）
    │  ├─ README.md             # ダウンロード手順
    │  └─ derived/              # 自前加工用（任意）
    ├─ exp/
    │  ├─ README.md
    │  ├─ exp-index.md
    │  ├─ latest/manifest.md
    │  ├─ protocol/ · work/ · archive/ · replay/ · local-eval/
    │  ├─ exp-train.md · exp-infer.md · exp-intel.md
    │  ├─ experiment-checklist.md
    │  └─ hyperparameter-table.md
    ├─ my-notebook/                # Cursor が編集する WIP
    │  └─ planned/                # 作成済み・未実行・実行後回しキュー
    ├─ my-local-eval-notebook/      # 検証専用（提出しない）
    ├─ my-ran-notebook/            # 実行済み・未提出
    ├─ my-submitted-notebook/      # 提出済み（編集禁止）
    ├─ others-notebook/
    ├─ sim-track/                 # simulation のみ（init-comp-layout）
    ├─ docs-ja/
    │  ├─ folder-map.md           # ★ 置き場所 SSOT
    │  ├─ comp-start-checklist.md # Day 0 チェックリスト
    │  ├─ comp-profile.md         # コンペ型・Skill マップ（bootstrap で生成）
    │  ├─ comp-timeline.md
    │  ├─ pretrain-acceptance.md
    │  ├─ kernels-runbook.md
    │  ├─ submission-rules.md
    │  ├─ pretrain-gates/
    │  └─ submission-validations/
    └─ docs-en/
```

コンペ終了後は Skill `post-comp-retro-setup` で `retro/` を追加する（開始時には作らない）。

```
    └─ retro/                # コンペ終了後に新設
       ├─ retro-index.md
       ├─ retro-private.md
       ├─ retro-leaderboard.md
       ├─ retro-solutions.md
       ├─ retro-lessons.md
       └─ archive/            # 他者 NB + 解法セット
```

## Notebook · 成果物ライフサイクル

Skill **`kaggle-notebook-folders`** — `planned/` = **未実行**のみ  
**`init-comp-layout.ps1`** — lifecycle-manifest · folder-map · README 一式  
SSOT: `.cursor/skills/_shared/ARTIFACT-LIFECYCLE.md`

## コンペ Router（全コンペ共通・最初に）

Skill **`kaggle-comp-router`** — `comp-type` 判定 → `docs-ja/comp-profile.md` に Skill マップ。  
作業開始時・概要作成時・「どの Skill？」のときに **最初に** 読む。

## コンペタイムライン · 提出制約 · メダル（全コンペ共通）

Skill **`kaggle-comp-timeline`** — `docs-ja/comp-timeline.md` に締切・提出制限・**UTC** を集約。  
Skill **`kaggle-competition-constraints`** — 1日上限 / 有効枠 / **メダル帯（チーム数 N）** の再計算・誤認防止。  
Rule **`kaggle-comp-constraints`** · SSOT `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md`  
bootstrap 時に timeline テンプレ生成。**他コンペの提出回数を流用しない。**

## 3段ゲート（全コンペ共通）

| 順 | Skill | SSOT |
|---|---|---|
| ① 学習前 | `kaggle-pretrain-gate` | `pretrain-acceptance.md`, `pretrain-gates/` |
| ①b 外部依存 | `kaggle-license-compliance` | `license-ledger.md`, `license-audits/` |
| ② 実行 | `kaggle-kernels-runbook` | `kernels-runbook.md`, `run-log.md` · **許可+指示後のみ** · CPU5/GPU2枠 · **自資産 Private** |
| ③ 提出前 | `kaggle-submission-validator` | `submission-rules.md`, `submission-validations/` |

### 提出（notebook-output · 必読）

SSOT: **`_shared/NOTEBOOK-LINKED-SUBMIT.md`**

| 方式 | 内容 |
|---|---|
| **1 UI** | Submit to Competition（実行含むことが多い） |
| **2 CLI** | `competitions submit -k/-v`（Version 済み · `-f` は出力名） |
| **2b CLI 完結** | `kernels push` → `status`/`files` → `competitions submit -k/-v` |
| **3 禁止標準** | zip-only `-f` ローカルパス |

| ルール | 内容 |
|---|---|
| **`-k` / `-v`** | **自アカウントの kernel のみ**（他者 slug → 403） |
| **403 時** | **zip-only 禁止** — 自 fork 更新 → Version 作成 → 再提出 |
| **他者 zip** | `kernels output` 後も embedded zip を **自 fork** に載せて notebook 紐づけ |
| **公式 CLI** | [kaggle-cli tutorials](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md) · 実行は `scripts/kaggle-cli.ps1` |

`submission-rules.md` · `kernels-runbook.md` 初版作成時に上記を含める（テンプレ `submission-rules.md.template` · `kernels-runbook.md.template` 参照）。

---

Games / エージェント提出 / 日次 LB では **`init-comp-layout.ps1 -CompType simulation`** で `sim-track/` を同時生成。Skill **`kaggle-simulation-tracker`** で運用。

- **公開 NB 一覧の推移** → `public-notebook-catalog.md` + `snapshots/catalog/`
- **パブリックスコアの時間推移** → `notebook-score-history.md`（append only）。Code タブ score は **peak-ui** — stale 注意は Skill 参照

**タブラー ML・LoRA コンペでは使わない。**

## 終了後フェーズ（retro/）

| Skill | 担当 |
|---|---|
| `post-comp-retro-setup` | `retro/` 新設・exp/ との分離 · **lessons は A/B/C 分離** |
| `post-comp-private-retrospective` | 自チーム Private 振り返り → lessons 軸付き追記 |
| `leaderboard-analysis` | コンペ全体 LB → `retro-leaderboard.md` |
| `solution-analysis` | 上位解法 → `retro-solutions.md`（**A CV vs B 解法 を別節**） |
| `kaggle-knowledge-harvest` | `retro-lessons` · failures → `knowledge/candidates/`（L0）· **Private push** |
| `kaggle-knowledge-retrieve` | **次コンペ開始** · prior（domain · **A→C→B** · apply/avoid） |
| `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md` | knowledge-store / kaggle-infra 運用 SSOT |

```
    └─ retro/
       ├─ retro-lessons.md   # ## 汎用 → ### A/B/C
       └─ archive/
          └─ others-notebook/post-comp-top-YYYYMMDD/  # 終了後公開 kernel
```

## 命名規則（統一）

| 対象 | ルール | 例 |
|---|---|---|
| フォルダ | 小文字 + ハイフン | `my-notebook/`, `exp/` |
| ファイル | 小文字 + ハイフン | `exp-index.md`, `hyperparameter-table.md` |
| 例外 | ツール固定のみ大文字 | `AGENTS.md`, `SKILL.md` |

フォルダとファイルで **別ルールにしない**。

## プレースホルダ

| タグ | 意味 |
|---|---|
| `{{COMP_NAME}}` | コンペ表示名 |
| `{{COMP_SLUG}}` | フォルダ用スラッグ |
| `{{COMP_URL}}` | Kaggle URL |
| `{{COMP_DEADLINE}}` | 締切 |
| `{{COMP_DATE}}` | 開始日 YYYYMMDD |
| `{{PARTICIPANT}}` | 参加者名（既定: Kazeneko） |

## 禁止事項

- `Kaggle.code-workspace` を新規コンペに含めない
- Default Profile をコピーして `Kaggle-Light` を作らない
- `dataset/` 内の公式データを編集しない
- **`dataset/` へのダウンロードを Agent が勝手に行わない**（容量超過の恐れ。ユーザー明示指示時のみ）
- **`dataset/` および派生データを Git / GitHub にコミット・push しない**（ライセンスリスク）
- 学習・推論・他者分析を1つの巨大な `EXP_SUMMARY.md` に混ぜない

## 詳細

テンプレート一覧・トラブルシュートは [reference.md](reference.md) を参照。

## Kaggle CLI

| Skill | 用途 |
|---|---|
| **`kaggle-cli-ops`** | venv bootstrap · preflight · **Notebook 紐づけ提出 CLI（方式 2b）** · 障害 |
| **`kaggle-comp-deps`** | コンペ `requirements-local.txt` · `setup-comp-venv` |
| **`kaggle-cli-fetch`** | Discussion・提出履歴取得 |

セットアップ: **`scripts/setup-kaggle-venv.ps1`**（CLI）· **`scripts/setup-comp-venv.ps1`**（計算）· 詳細 **`kaggle-cli-ops`** / **`kaggle-comp-deps`**  
提出 SSOT: **`_shared/NOTEBOOK-LINKED-SUBMIT.md`** · 公式: [Kaggle CLI tutorials](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md)

## Git / GitHub

Skill `kaggle-git-security` — `.gitignore` 同梱、`-InitGit` で pre-commit 設置

## 実験チェックリスト（Mania 流 2段構え）

Skill **`kaggle-experiment-checklist`** — Discussion · intel · 自チーム結果から **仮説** を列挙 → dedupe → 1項目ずつ検証。

| 概念 | 役割 |
|---|---|
| **fork** | **禁止ではない** — 材料取得・実行（`my-notebook/` · runbook · intel） |
| **checklist** | **何のために fork するか**＝検証する仮説（手法 × 期待効果） |
| **exp-infer** | 提出結果・SUB 履歴 |

bootstrap 時の `experiment-checklist.md` はテンプレから生成。Day 0 以降は Phase 1 で仮説を埋める。**§実行制約** に週次の GPU 方針（温存・ローカル CPU のみ等）を書く。工程分離手順は任意で `docs-ja/gpu-execution-split.md`（NeuroGolf 例: `kaggle-cpu-gpu-split.md`）。
