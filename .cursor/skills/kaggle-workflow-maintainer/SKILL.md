---
name: kaggle-workflow-maintainer
description: >-
  Kaggle 用テンプレ同期 · bootstrap · Skill 総数管理。
  Skills/Rules/Hooks/Subagents の作成・改善は **cursor-agent-infra** を先に使う。
  テンプレ同期、Skill 再編成と言ったときに使う。
disable-model-invocation: true
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| scripts/* · sync-project-infra-from-template.ps1 | — | — | kaggle-template/ · .cursor/ | .cursor/skills/ · rules · scripts テンプレ |

**要ユーザー明示 OK:** 新 Skill 追加 · テンプレ同期（ユーザー承認）

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Workflow Maintainer

**Kaggle インフラ専用メタ Skill。** コンペ本番（LB・学習）ではなく、**テンプレ同期 · bootstrap · Skill 総数管理** に使う。

**Cursor 製品機能（Skills / Rules / Hooks / Subagents）の作成・改善** → 先に Skill **`cursor-agent-infra`**。

詳細: [reference.md](reference.md)

---

## 鉄則（最初に確認）

| 置く | 置かない |
|---|---|
| `kaggle-template/` = **SSOT マスター** | `~/.cursor/skills/` に **Kaggle 系 Skill** |
| 各コンペ `<comp-root>/.cursor/skills/` | Web プロジェクトに Kaggle Skill / Rules |
| 各コンペ `<comp-root>/.cursor/rules/` | `Kaggle.code-workspace` |
| 軽量 **Rules** + 厚い **SSOT md テンプレ** | Skill 本文への長文 SSOT 二重化 |

**Web 開発** と **Kaggle** は **別 ROOT・別 Profile（Kaggle-Light）** で開く。

---

## 何を作るか（判断順）

```
1. 既存 Skill + docs-ja/*.md テンプレで足りないか？
2. scripts/*.ps1 に落とせないか？（L0-L1 検証など）
3. .cursor/rules/*.mdc に 1〜5 行リマインドで足りないか？
4. 上記すべて NO → 新 Skill（+1 はユーザー承認後）
```

| 追加したいもの | 第一候補 | 例 |
|---|---|---|
| 常時リマインド | **Rules** `.mdc` | `kaggle-three-gates.mdc` |
| 手順・チェックリスト | **SSOT テンプレ** | `license-ledger.md`, `metric-repro.md` |
| 機械的検証 | **script** | `validate-submission.ps1` |
| トリガー付きワークフロー | **Skill**（薄型） | `kaggle-pretrain-gate` |

---

## 編集フロー（SSOT → 反映）

1. **考察をユーザーに説明し承認**（複雑な変更時）
2. **マスター編集:** `%USERPROFILE%\.cursor\kaggle-template\`
   - Skill → `root/.cursor/skills/<name>/`
   - Rule → `root/.cursor/rules/<name>.mdc`
   - hook → `root/.githooks/` + `root/scripts/`
   - コンペ doc テンプレ → `comp/docs-ja/*.template`, `comp/sim-track/` 等
3. **既存コンペへ反映**
4. **`cursor.md` 変更メモ**（重要判断のみ）

### 反映コマンド

```powershell
# infra 一括同期（並行コンペ向け・推奨）
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA", "<DESKTOP>/OrbitWars"

# Skills のみ（軽量）
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-skills-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA"

# git 利用中なら hooks 再インストールも
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
  -CompRoot "<DESKTOP>/NVIDIA" -InstallGitHooks

# 誤ってグローバルに Kaggle Skill がある場合（退避）
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\archive-global-kaggle-skills.ps1"
```

**上書き対象:** `.cursor/skills/`, `.cursor/rules/`, `scripts/*.ps1`, `scripts/templates/`, `.githooks/`  
**配置（`-InstallCursorInfra`）:** `.cursor/hooks.json`, `.cursor/hooks/`, `.cursor/agents/`  
**上書きしない:** `AGENTS.md`, `cursor.md`, `{date}-{slug}/` 内のコンペデータ

---

## レイヤー早見

| レイヤー | SSOT パス | コンペへの反映 |
|---|---|---|
| **Skills** | `kaggle-template/root/.cursor/skills/` | `sync-project-infra-from-template.ps1`（または skills のみ script） |
| **Rules** | `kaggle-template/root/.cursor/rules/` | **`sync-project-infra-from-template.ps1`** |
| **Git hooks** | `root/.githooks/`, `scripts/install-git-hooks.ps1` | **`sync-project-infra-from-template.ps1`** + `-InstallGitHooks` |
| **Scripts** | `root/scripts/` | **`sync-project-infra-from-template.ps1`** |
| **doc テンプレ** | `comp/docs-ja/`, `comp/sim-track/`, `comp/exp/` | bootstrap 時展開 / 既存は手動 |
| **Profile** | `root/.vscode/` Kaggle-Light | PC ごと Import（1 回） |

---

## Skill 作成時

- 汎用 Cursor 形式 → グローバル Skill **`create-skill`**（形式のみ参照）
- **配置・命名・同期** → 本 Skill + `reference.md`
- `description`: **WHAT + WHEN**、60 行以内、`comp-profile.md` へルーティングを寄せる
- ネスト `skill/skill/` 禁止（sync スクリプトが除去するが作らない）
- **Permissions 表（必須）:** `_shared/PERMISSIONS.md` → `scripts/skill-permissions-map.json` に追記 → `.\scripts\sync-skill-permissions.ps1` で全 Skill へ反映

## Permissions 同期（新 Skill / 権限変更）

| 手順 | ファイル |
|---|---|
| 1. 列定義・共通禁止の確認 | `.cursor/skills/_shared/PERMISSIONS.md` |
| 2. Skill ごとの shell / network / env / file_* / user_ok | `scripts/skill-permissions-map.json` |
| 3. 全 `SKILL.md` へ表を挿入・更新 | `.\scripts\sync-skill-permissions.ps1`（`-WhatIf` で差分確認可） |

**要ユーザー OK** は Rules（`kaggle-three-gates` · `kaggle-cli-venv`）と `kaggle-submission-validator` に分散。各 Skill 表は **その Skill 内で触ってよい境界** のみ宣言する。

## Rule 作成時

- 形式 → グローバル **`create-rule`**
- **alwaysApply は最小**（3段ゲート程度）。長文は Skill / SSOT へ
- Kaggle Rule は **コンペ ROOT の `.cursor/rules/` のみ**

## hook 作成時

- **先に `cursor-agent-infra`** — https://cursor.com/ja/docs/hooks
- Skill **`kaggle-git-security`** と整合
- `dataset/`・秘匿・大容量を block — **緩和提案しない**

---

## Agent 規則

1. **Kaggle Skill を `~/.cursor/skills/` に作らない・コピーしない**
2. マスター無しで **コンペ ROOT だけ** に Skill を増やさない（ドrift）
3. Skill 総数を増やす前に **テンプレ / script / rule** を検討
4. 改修後は **template → `sync-project-infra-from-template.ps1`**（並行コンペは CompRoot 複数指定）
5. コンペ固有の変更は `docs-ja/comp-profile.md` の「使わない Skill」で休眠明示

---

## 関連 Skill

| Skill | 役割 |
|---|---|
| **`cursor-agent-infra`** | Skills / Rules / Hooks / Subagents（公式 URL 必読） |
| `kaggle-comp-bootstrap` | 新コンペ生成・フォルダ儀式 |
| `create-agent-file` | `AGENTS.md` |
| `create-skill` / `create-rule`（**グローバル**） | Cursor 一般形式のみ |
| `.cursor/skills/README.md` | Skill 配置の SSOT 1 ページ |
