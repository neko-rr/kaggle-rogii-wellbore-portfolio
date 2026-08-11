# Kaggle Workflow Maintainer — Reference

> SSOT 詳細。Skill 本文は判断フローのみ — パス・チェックリストは本ファイル。

---

## 1. 配置ポリシー（グローバル vs プロジェクト）

### グローバル `~/.cursor/skills/` — Kaggle 禁止

| 理由 | 説明 |
|---|---|
| Web 開発と混在 | 同一 Agent が Kaggle Skill を誤起動 |
| 二重管理 | プロジェクト `.cursor/skills/` と競合 |
| 退避済み | `~/.cursor/skills-archive/kaggle/` に旧 13 件 |

**グローバルに置いてよい例:** `gcp-*`, `dbt-*`, `building-data-apps`, **`create-skill`**, **`create-rule`**

### プロジェクト `<comp-root>/`

| パス | 内容 |
|---|---|
| `.cursor/skills/` | 全 Kaggle Skill（bootstrap / sync 由来） |
| `.cursor/rules/` | 常時リマインド（例: `kaggle-three-gates.mdc`） |
| `.cursor/hooks.json` + `.cursor/hooks/` | Cursor Agent hooks（CLI/submit/dataset ゲート） |
| `.cursor/agents/` | カスタムサブエージェント |
| `.cursor/skills/cursor-agent-infra/` | **Cursor インフラ改善 Skill（公式 URL 必読）** |
| `.cursor/skills/_shared/SUBAGENT-BRIEF.md` | サブエージェント併用 SSOT |
| `.githooks/` | pre-commit 等 |
| `scripts/` | validate-submission, install-git-hooks, install-cursor-hooks, open-kaggle-light |
| `scripts/templates/cursor-hooks/` | hooks テンプレ SSOT |
| `{date}-{slug}/docs-ja/` | コンペ SSOT（実行時に Agent が読む） |

### マスター `~/.cursor/kaggle-template/`

```
kaggle-template/
├─ root/                    # コンペ ROOT に展開（AGENTS.md, .cursor/, scripts/）
│  ├─ .cursor/skills/       # ★ Skill SSOT
│  ├─ .cursor/rules/
│  ├─ .githooks/
│  └─ scripts/
├─ comp/                    # {date}-{slug}/ 内側
│  ├─ docs-ja/*.template
│  ├─ sim-track/
│  └─ exp/
└─ scripts/
   ├─ new-kaggle-comp.ps1
   ├─ sync-project-skills-from-template.ps1
   └─ archive-global-kaggle-skills.ps1
```

---

## 2. 新規 Skill 要否チェックリスト

- [ ] 既存 Skill の **1 節追記** で足りないか？
- [ ] `comp/docs-ja/*.md.template` に SSOT として書けるか？
- [ ] `scripts/*.ps1` で L0-L1 自動化できるか？
- [ ] `.cursor/rules/*.mdc` に 1〜5 行で常時化できるか？
- [ ] `comp-profile.md.template` のルーティング表に 1 行追加で足りないか？
- [ ] **+1 承認** をユーザーから得たか？
- [ ] `description` が他 Skill と重複していないか？

**過去の方針例（独立 Skill にしなかった）:** cost-tracker → `run-ledger.md`、writeup-prep → retro テンプレ

---

## 3. 改修タイプ別手順

### A. 既存 Skill 改修

1. `kaggle-template/root/.cursor/skills/<name>/SKILL.md` を編集
2. `sync-project-skills-from-template.ps1 -CompRoot ...`
3. ルーティング変更なら `comp/docs-ja/comp-profile.md.template` も更新
4. 関連 SSOT テンプレがあれば `comp/` 側も更新

### B. 新 Skill 追加

1. 上記要否チェック + ユーザー承認
2. `kaggle-template/root/.cursor/skills/<kebab-name>/SKILL.md` 作成
3. 必要なら `reference.md` または `comp/*.template`
4. `comp-profile.md.template` マトリクスに 1 行
5. `kaggle-comp-bootstrap/reference.md` に SSOT 対応表追記
6. sync 全コンペ

### C. Rule（.mdc）追加・改修

1. `kaggle-template/root/.cursor/rules/<name>.mdc`
2. frontmatter: `description`, `alwaysApply`（原則 false 推奨、three-gates のみ true）
3. **5〜15 行** — 詳細は Skill へリンク
4. 既存コンペ: `<comp-root>/.cursor/rules/` へ手動コピー

### D. Git hook / scripts

1. `root/.githooks/` + `root/scripts/check-*.ps1`
2. `kaggle-git-security` Skill に 1 行追記
3. 既存コンペ: `scripts/` と `.githooks/` を手動同期
4. ユーザー環境: `git init` 済みなら `install-git-hooks.ps1` 再実行を案内

### E. docs-ja テンプレ（SSOT）

1. `comp/docs-ja/<name>.md.template` または `comp/sim-track/`
2. 初版生成 Skill（例: `competition-conditions`, `kaggle-license-compliance`）に参照 1 行
3. **既存コンペの `docs-ja/` は手動マージ**（bootstrap は新規のみ）

---

## 4. 同期（並行コンペ）

### 推奨: infra 一括

```powershell
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA", "<DESKTOP>/OrbitWars"

# ドライラン
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA" -WhatIf

# git リポジトリあり → git hooks 再インストール
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA" -InstallGitHooks

# Cursor hooks + agents 再配置 + テスト
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA" -InstallCursorInfra
```

| 対象 | sync |
|---|---|
| `.cursor/skills/` | **あり** |
| `.cursor/rules/` | **あり** |
| `scripts/*.ps1` | **あり** |
| `scripts/templates/` | **あり**（cursor-hooks · cursor-agents · comp テンプレ） |
| `.githooks/` | **あり** |
| `.cursor/hooks.json` · `.cursor/hooks/` · `.cursor/agents/` | **`-InstallCursorInfra` で配置**（テンプレから生成） |
| `comp/docs-ja/` テンプレ | **なし**（新コンペ bootstrap のみ / 手動マージ） |
| `AGENTS.md`, `cursor.md` | **上書きしない** |

### Skills のみ（軽量）

`sync-project-skills-from-template.ps1` — infra スクリプトは内部でこれを呼ぶ。

### いつ実行するか

| タイミング | コマンド |
|---|---|
| マスターで Skill / Rule / script / hook を直した直後 | `sync-project-infra` を **全 CompRoot** に |
| 新コンペ bootstrap 直後 | 不要（`new-kaggle-comp.ps1` が root 一式コピー済み） |
| 1 コンペだけ Skill だけ更新 | `sync-project-skills` でも可 |

改修後チェック:

```powershell
# Skill 件数一致
(Get-ChildItem "$env:USERPROFILE\.cursor\kaggle-template\root\.cursor\skills" -Directory).Count
(Get-ChildItem "<comp-root>\.cursor\skills" -Directory).Count

# グローバルに kaggle-* が無いこと
Get-ChildItem "$env:USERPROFILE\.cursor\skills" -Directory | Where-Object Name -like 'kaggle-*'
```

---

## 5. description / コンテキスト肥大化防止

- Router（`kaggle-comp-router`）と `comp-profile.md` に **マトリクス集約**
- 各 Skill `description` は **トリガー語のみ**（「全コンペ共通」連発禁止）
- 3段ゲート長表は **Rules + comp-profile** — 各 Skill は SSOT リンク

---

## 6. コンペ型別の infra 差

| comp-type | 追加 infra |
|---|---|
| tabular | `local-eval-*`, `metric-repro.md` |
| lora-llm | `validate-submission.ps1 -Profile lora`, `license-ledger.md` |
| simulation | `kaggle-simulation-tracker`, `sim-track/`, `agent-debug.md` |
| 終了後 | `retro/`, post-comp-* Skills |

`comp-profile.md` の「使わない Skill」で inactive を明示。

---

## 7. 変更記録

| 重要度 | 書く場所 |
|---|---|
| インフラ方針・Skill 追加 | `<comp-root>/cursor.md` 変更メモ |
| コンペ中の実験 | `exp/`（infra と混ぜない） |
| テンプレ README | `.cursor/skills/README.md`（配置ポリシーのみ） |

---

## 8. 禁止事項（再掲）

- Kaggle Skill / Kaggle Rule を **グローバル** に置く
- `dataset/` を Git / hook 緩和で載せる
- Skill 本文に Router マトリクス全文をコピー
- コンペ ROOT だけ改変して **template を更新しない**（ドリフト）
- `Others_notebook/` / `my-submitted-notebook/` を提出用として改変
