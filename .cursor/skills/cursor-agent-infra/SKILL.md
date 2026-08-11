---
name: cursor-agent-infra
description: >-
  Cursor の Skills / Rules / Hooks / サブエージェント (.cursor/agents/) の
  作成・改善。公式ドキュメントを参照してから実装する。
  hooks 追加、Skill 作成、subagent 定義、rules.mdc、混同修正、
  install-cursor-hooks、install-cursor-agents と言ったときに使う。
disable-model-invocation: true
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| install-cursor-hooks.ps1 · install-cursor-agents.ps1 · test-cursor-hooks.ps1 · sync-skill-permissions.ps1 | cursor.com docs HTTPS（改善前必須 WebFetch） | — | .cursor/ · scripts/templates/cursor-* · reference.md | .cursor/skills/ · rules · hooks · agents · templates · skill-permissions-map.json |

**要ユーザー明示 OK:** 新 Skill 大量追加 · failClosed hook 追加 · kaggle-template 同期

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Cursor Agent Infra

**Cursor 製品機能専用メタ Skill。** Kaggle コンペ本番（LB・学習・提出）ではなく、**Skills · Rules · Hooks · Subagents** の設計・改修時に使う。

詳細: [reference.md](reference.md)

---

## 公式ドキュメント（改善前に必ず参照）

| 機能 | URL |
|---|---|
| **Subagents** | https://cursor.com/ja/docs/subagents |
| **Skills** | https://cursor.com/ja/docs/skills |
| **Rules** | https://cursor.com/ja/docs/rules |
| **Hooks** | https://cursor.com/ja/docs/hooks |

### 必須 Step 0（省略禁止）

改善・新規作成の **最初** に:

1. 対象 URL を **WebFetch**（またはユーザー提供の最新 export）で読む
2. 触るレイヤーを 1 つ特定（Skill / Rule / Hook / Subagent）
3. [reference.md](reference.md) の混同表と照合
4. **考察をユーザーに説明し承認**（複雑な変更時 · ユーザールール）
5. 実装 → 検証（下記）

**公式と矛盾する既存実装**を見つけたら、推測で直さず URL の該当節を引用して修正方針を示す。

---

## 4 レイヤー（1 行定義）

| レイヤー | 置き場 | 使うとき |
|---|---|---|
| **Skill** | `.cursor/skills/<name>/SKILL.md` | 親 Agent の判断・手順・ゲートフロー |
| **Rule** | `.cursor/rules/*.mdc` | 短い常時リマインド |
| **Hook** | `.cursor/hooks.json` + scripts | 機械的 allow/deny · 監査 |
| **Subagent** | `.cursor/agents/*.md` | 重い探索/shell の委譲（専用コンテキスト） |

組み込み subagent（`explore` · `bash` · `browser`）は設定不要 — [subagents 公式](https://cursor.com/ja/docs/subagents)。

---

## 実装フロー（種別別）

### Skill

- 形式: [skills 公式](https://cursor.com/ja/docs/skills) · グローバル `create-skill`（形式のみ）
- Permissions: `_shared/PERMISSIONS.md` → `skill-permissions-map.json` → `sync-skill-permissions.ps1`
- Kaggle 配置: コンペ ROOT の `.cursor/skills/` のみ

### Rule

- **`.mdc` のみ** — [rules 公式](https://cursor.com/ja/docs/rules)
- `alwaysApply: true` は最小限（例: `kaggle-three-gates.mdc`）

### Hook

- テンプレ: `scripts/templates/cursor-hooks/` → `install-cursor-hooks.ps1`
- 脚本は **常に valid JSON** · PS 5.1 · ASCII メッセージ推奨
- テスト: `test-cursor-hooks.ps1` · Reload 後 Settings → Hooks
- schema: [hooks 公式](https://cursor.com/ja/docs/hooks)（`permission` · `failClosed` · matcher）

### Subagent（カスタム）

- テンプレ: `scripts/templates/cursor-agents/` → `install-cursor-agents.ps1`
- 形式: [subagents 公式](https://cursor.com/ja/docs/subagents)（frontmatter + 簡潔 prompt）
- 委譲規約: `_shared/SUBAGENT-BRIEF.md` · 親 Skill `kaggle-subagent-delegate`
- **2〜4 個に絞る** — 汎用 helper 乱立禁止

---

## 検証チェックリスト

| 種別 | PASS 条件 |
|---|---|
| Hook | `test-cursor-hooks.ps1` 全 PASS · 空 stdout なし |
| Subagent | `.cursor/agents/` にファイル · `/name` または description で委譲 |
| Skill | `name` = フォルダ名 · permissions 同期済み |
| Rule | `.mdc` · alwaysApply 過多でない |

---

## 関連 Skill

| Skill | 役割 |
|---|---|
| **`kaggle-workflow-maintainer`** | テンプレ同期 · bootstrap · Skill 総数管理 |
| **`kaggle-subagent-delegate`** | 親 Agent の subagent オーケストレーション |
| **`kaggle-adversarial-review`** | 高コスト判定の red-team（SA-7） |
| **`kaggle-git-security`** | Git hook · 秘匿 |
| **グローバル `create-hook` / `create-skill` / `create-rule`** | Cursor 一般形式（配置は本 repo 規約優先） |

---

## Agent 規則

1. **Step 0 公式 URL 必読** — 推測で hooks.json / agents 形式を invent しない
2. **レイヤー混同禁止** — reference.md 早見表を毎回確認
3. **AGENTS.md** — セッション開始用。内容を Rule に丸写ししない
4. マスター同期が必要なら **`kaggle-workflow-maintainer`** に引き継ぎ
5. 変更後 `cursor.md` に 1 行（重要判断のみ）
