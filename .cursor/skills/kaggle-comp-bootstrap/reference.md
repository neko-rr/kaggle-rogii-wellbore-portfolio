# Kaggle Bootstrap リファレンス

## テンプレート配置

```
%USERPROFILE%\.cursor\
├─ kaggle-template\
│   ├─ root\
│   │   └─ .cursor\skills\     # ★ Kaggle Skill マスター（SSOT）
│   ├─ comp\
│   └─ scripts\
│       ├─ new-kaggle-comp.ps1
│       ├─ archive-global-kaggle-skills.ps1
│       ├─ sync-project-skills-from-template.ps1
│       ├─ sync-project-infra-from-template.ps1   # skills + rules + scripts + templates + githooks
│       └─ push-infra-to-kaggle-template.ps1      # マスターへ反映（orbit-wars 等から）
└─ skills-archive\kaggle\      # グローバル退避先（任意）
```

**`~/.cursor/skills/` に Kaggle Skill を置かない**（Web 開発と分離）。各コンペは `<comp-root>/.cursor/skills/` のみ。

## new-kaggle-comp.ps1 パラメータ

| パラメータ | 必須 | 既定値 | 説明 |
|---|---|---|---|
| `-Name` | Yes | — | コンペスラッグ（例: `titanic-2026`） |
| `-Parent` | No | Desktop | 親フォルダ |
| `-Url` | No | 空 | Kaggle コンペ URL |
| `-Deadline` | No | TBD | 締切表示 |
| `-CompDate` | No | 今日 | `YYYYMMDD` |
| `-Participant` | No | Kazeneko | AGENTS.md 用 |
| `-Participant` | No | Kazeneko | AGENTS.md 用 |
| `-NoOpen` | No | — | Cursor を自動起動しない |
| `-InitGit` | No | — | `git init` + pre-commit フックをインストール |

## Cursor Agent インフラ（新コンペ必須）

| 項目 | 配置 |
|---|---|
| Hooks | `.cursor/hooks.json` + `.cursor/hooks/` |
| Subagents | `.cursor/agents/`（4 カスタム SA） |
| テンプレ SSOT | `scripts/templates/cursor-hooks/` · `cursor-agents/` |
| 一括インストール | `scripts/install-cursor-infra.ps1` |
| テスト | `scripts/test-cursor-hooks.ps1`（8 cases PASS） |

**新リポ生成:** `new-kaggle-comp.ps1` が `install-cursor-infra.ps1` を自動実行。  
**既存リポ更新:** `sync-project-infra-from-template.ps1 -InstallCursorInfra`  
**マスター反映:** orbit-wars 等から `push-infra-to-kaggle-template.ps1`

配置後 **Cursor: Reload Window** 必須。

## Git / GitHub セキュリティ

| ファイル | 役割 |
|---|---|
| `.gitignore` | `dataset/`、`.env`、`kaggle.json`、大容量成果物を除外 |
| `.githooks/pre-commit` | コミット前フック |
| `scripts/check-staged-secrets.ps1` | staged 検査 |
| `scripts/install-git-hooks.ps1` | フック設置 |

Skill: `kaggle-git-security`

**dataset/ は GitHub に載せない** — コンペライセンス上のリスク。`dataset/README.md` に手順のみ。**Agent は dataset を勝手にダウンロードしない**（ユーザー指示時のみ）。

## コンペ Router

| ファイル | 役割 |
|---|---|
| `docs-ja/comp-profile.md` | comp-type・Skill マップ SSOT（Skill: `kaggle-comp-router`） |

概要作成時に comp-type を確定。Agent は型固有 Skill の前に Router を読む。

## コンペタイムライン

| ファイル | 役割 |
|---|---|
| `docs-ja/comp-timeline.md` | 締切・フェーズ・提出制限 SSOT（Skill: `kaggle-comp-timeline`） |

bootstrap 時にテンプレ生成。`conditions.md` と同時に初版作成。

## 3段ゲート

| Skill | ファイル |
|---|---|
| `kaggle-pretrain-gate` | `pretrain-acceptance.md`, `pretrain-gates/` |
| `kaggle-license-compliance` | `license-ledger.md`, `license-audits/` |
| `kaggle-kernels-runbook` | `kernels-runbook.md`, `my-ran-notebook/.../run-log.md` |
| `kaggle-submission-validator` | `submission-rules.md`, `submission-validations/` |

## Notebook フォルダ（コンペ内）

| フォルダ | 役割 |
|---|---|
| `dataset/` | **コンペ開始時に作成**。公式データの手動 DL 先（`README.md` + `derived/`） |
| `my-notebook/` | Cursor が編集する WIP |
| `my-notebook/planned/` | 作成済み・**未実行**・実行後回し |
| `my-local-eval-notebook/` | 検証専用 fork |
| `my-ran-notebook/` | 実行済み（完走不要）・`run-log.md` |
| `my-submitted-notebook/` | validator PASS 後のみ凍結 |

Skill: `kaggle-notebook-folders` / `kaggle-experiment-checklist`

## シミュレーション系（任意）

Skill **`kaggle-simulation-tracker`** — `sim-track/` に (1) 公開 NB 一覧推移 (2) public score 時系列

## Kaggle.code-workspace が不要な理由

| 開き方 | チャット | Profile 紐付け |
|---|---|---|
| フォルダ | 一貫 | `Kaggle-Light` に設定済み |
| `.code-workspace` | **別セッション** | Default のままになりやすい |

自動化では `cursor --profile "Kaggle-Light" "<folder>"` が再現性が高い。

## EXP標準4ファイル（`exp/` 配下）

| ファイル | 役割 |
|---|---|
| `exp-index.md` | 索引・現在地・Best・次アクション |
| `exp-train.md` | 学習実験、CV、fold、データ、モデル、loss、特徴量 |
| `exp-infer.md` | 推論、後処理、提出、LB、submission notebook |
| `exp-intel.md` | 他者Notebook、Discussion、上位解法、外部知見 |
| `experiment-checklist.md` | **仮説検証** CHK ループ（fork 羅列ではない · fork 自体は `my-notebook/` で可） |

`hyperparameter-table.md` は、学習・推論の詳細な表形式ログとして併用する。

自律実験: Skill **`kaggle-experiment-checklist`** — **仮説** を Plan → Execute。fork は手段（intel / my-notebook）、CHK は目的。

## レイアウト初期化（init-comp-layout.ps1）

| パラメータ | 説明 |
|---|---|
| `-CompRoot` | `{YYYYMMDD}-{slug}` フォルダパス（必須） |
| `-CompType` | `auto`（既定）· `simulation` · `tabular` 等 |
| `-Force` | 既存ファイル上書き |
| `-WhatIf` | ドライラン |

```powershell
.\scripts\init-comp-layout.ps1 -CompRoot "20260701-my-comp" -CompType simulation
```

テンプレ: `scripts/templates/`（repo 内 SSOT。`kaggle-template` へは `kaggle-workflow-maintainer` で同期）

## 置き場所 SSOT（Agent 向け）

| ファイル | 役割 |
|---|---|
| `docs-ja/folder-map.md` | ダウンロード先 · 4 層 · 二索引 |
| `docs-ja/comp-start-checklist.md` | 開始日タスク |
| `lifecycle-manifest.md` | コード成果物 |
| `exp/latest/manifest.md` | 分析 MD |

## 命名規則（統一）

**フォルダ名・ファイル名は同じ法則: 小文字 + ハイフン（kebab-case）**

| 種別 | 例 |
|---|---|
| フォルダ | `my-notebook/`, `docs-ja/`, `exp/` |
| ファイル | `exp-train.md`, `conditions.md`, `open-kaggle-light.ps1` |
| 例外 | `AGENTS.md`, `SKILL.md` のみ大文字 |

コンペ内部フォルダ名: `{YYYYMMDD}-{slug}`（アンダースコアではなくハイフン）

## Kaggle-Light 拡張（有効）

- Jupyter 一式, Python, Ruff, debugpy
- Google Colab, Rainbow CSV
- Markdown All in One, Spell Checker
- Git Graph, **vscode-icons**（ファイルアイコン）

## 初回 PC セットアップチェックリスト

- [ ] `Kaggle-Light.code-profile` を Import
- [ ] `new-kaggle-comp.ps1` でテストコンペを1つ作成
- [ ] Extension Host メモリが軽いことを確認
- [ ] 古い `anthropic.claude-code` 重複フォルダを削除

## トラブルシュート

| 症状 | 対処 |
|---|---|
| Profile が効かない | `open-kaggle-light.ps1` で起動 |
| チャットが消えた | フォルダで開き直す（workspace ファイルを使わない） |
| テンプレが見つからない | `%USERPROFILE%\.cursor\kaggle-template` を確認 |
| フォルダが既にある | `-Name` を変えるか手動削除 |
