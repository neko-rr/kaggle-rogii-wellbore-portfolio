# Cursor Agent Infra — Reference

> 公式 SSOT（改善前に必ず WebFetch）:
> - [Subagents](https://cursor.com/ja/docs/subagents)
> - [Skills](https://cursor.com/ja/docs/skills)
> - [Rules](https://cursor.com/ja/docs/rules)
> - [Hooks](https://cursor.com/ja/docs/hooks)

---

## 1. 4 レイヤー早見（混同防止）

| レイヤー | 置き場 | ファイル形式 | 役割 | 公式 |
|---|---|---|---|---|
| **Skill** | `.cursor/skills/<name>/SKILL.md` | `name` · `description` · 本文 | 親 Agent の **判断・手順**（オンデマンド読込） | [skills](https://cursor.com/ja/docs/skills) |
| **Rule** | `.cursor/rules/*.mdc` | `alwaysApply` / `description` / `globs` | **常時・条件付き** リマインド（短い） | [rules](https://cursor.com/ja/docs/rules) |
| **Hook** | `.cursor/hooks.json` + `.cursor/hooks/*.ps1` | JSON · stdio JSON | **機械的** allow/deny · 監査 | [hooks](https://cursor.com/ja/docs/hooks) |
| **Subagent（カスタム）** | `.cursor/agents/*.md` | `name` · `description` · `readonly` 等 | **委譲先** 専用コンテキスト | [subagents](https://cursor.com/ja/docs/subagents) |

### よくある混同

| 誤り | 正しい |
|---|---|
| Skill で shell ゲート全部 | Hook（`beforeShellExecution`） |
| Hook で長い Kaggle 手順 | Skill + `docs-ja/` |
| Task `explore` = カスタム subagent 定義 | 組み込み。Kaggle 制約は `.cursor/agents/kaggle-*.md` |
| `.cursor/hooks/README.md` が Rule | **`.mdc` のみ** Rule。README は説明用 |
| `AGENTS.md` を Rule に複製 | AGENTS.md はセッション開始用。短い常時禁止は `.mdc` |
| 50 個の汎用 subagent | **焦点を絞った少数**（探索 SA-1〜4 + 審査 SA-7 程度。公式「2〜4」精神） |

---

## 2. 何を作るか（判断順 — 公式 + 本 repo）

```
1. 1 行リマインドで足りる？     → Rule (.mdc) または AGENTS.md 追記
2. 機械的に止めたい？           → Hook
3. 重い探索・shell を分離？     → Subagent (.cursor/agents/) + kaggle-subagent-delegate
4. 判断・記録・ゲート手順？     → Skill
5. 上記すべて NO → script (scripts/*.ps1) + Skill から参照
```

Kaggle コンペ本番（LB・提出）は **本 Skill の対象外** → 各 comp Skill。

---

## 3. Skill 作成チェック（[skills 公式](https://cursor.com/ja/docs/skills)）

| チェック | 内容 |
|---|---|
| 配置 | `<comp-root>/.cursor/skills/` のみ（グローバル Kaggle 禁止） |
| 名前 | フォルダ名 = frontmatter `name` |
| 本文 | 60 行目安 · SSOT は `reference.md` / `docs-ja/` へ |
| infra 3 本 | `disable-model-invocation: true`（cursor-agent-infra · workflow-maintainer · subagent-delegate） |
| Permissions | `_shared/PERMISSIONS.md` → `skill-permissions-map.json` → `sync-skill-permissions.ps1` |
| ルーティング | `comp-profile.md` **`comp-phase`** → `kaggle-comp-router` → Skill 1 つ |

---

## 4. Rule 作成チェック（[rules 公式](https://cursor.com/ja/docs/rules)）

| チェック | 内容 |
|---|---|
| 拡張子 | **`.mdc` のみ**（`.md` は Rule として無視） |
| alwaysApply | 3 段ゲート · CLI 禁止など **最小** のみ |
| 長文 | Skill / SSOT へ。Rule は 500 行以内 |
| 優先 | Team → Project → User（本 repo は Project） |

---

## 5. Hook 作成チェック（[hooks 公式](https://cursor.com/ja/docs/hooks)）

| チェック | 内容 |
|---|---|
| 配置 | `.cursor/hooks.json` · スクリプト `.cursor/hooks/` |
| 実行 cwd | **プロジェクトルート** — パスは `.cursor/hooks/foo.ps1` |
| 出力 | **必ず valid JSON** stdout · try/catch · インフラ障害時は allow 検討 |
| failClosed | セキュリティ系のみ `true` · 障害で Agent 全停止しない設計 |
| テンプレ | `scripts/templates/cursor-hooks/` → `install-cursor-hooks.ps1` |
| テスト | `test-cursor-hooks.ps1` |
| イベント選定 | 最小スコープ（`beforeShellExecution` vs `preToolUse` 等） |
| 新イベント | `subagentStart` / `subagentStop` は公式 schema 確認後 |

本 repo 現行 hooks:

| イベント | スクリプト |
|---|---|
| beforeShellExecution | CLI · submit · download · 破壊的 git |
| preToolUse | dataset/ 書込拒否 |
| afterShellExecution | validate-submission 監査 |

---

## 6. Subagent 作成チェック（[subagents 公式](https://cursor.com/ja/docs/subagents)）

| チェック | 内容 |
|---|---|
| カスタム | `.cursor/agents/<name>.md` + YAML frontmatter |
| 組み込み | `explore` · `bash` · `browser` — 設定不要 |
| 呼び出し | `/name` または description による自動委譲 |
| 本 repo | `kaggle-repo-explore` 等 4 本 · SSOT `SUBAGENT-BRIEF.md` |
| テンプレ | `scripts/templates/cursor-agents/` → `install-cursor-agents.ps1` |
| 親の役割 | Skill で exp 確定 · subagent はサマリのみ返す |
| readonly | 探索系は `true` · eval runner は `false` + `is_background: true` 可 |

---

## 7. 本 repo パス SSOT

| 種別 | SSOT | インストール |
|---|---|---|
| Hooks | `scripts/templates/cursor-hooks/` | `install-cursor-hooks.ps1` |
| Subagents | `scripts/templates/cursor-agents/` | `install-cursor-agents.ps1` |
| Skills | `.cursor/skills/`（マスター `kaggle-template`） | `sync-project-infra-from-template.ps1` |
| Rules | `.cursor/rules/` | 同上 |
| 委譲規約 | `_shared/SUBAGENT-BRIEF.md` | — |
| Permissions | `_shared/PERMISSIONS.md` | `sync-skill-permissions.ps1` |

---

## 8. 改善後の検証

| 種別 | 検証 |
|---|---|
| Hook | `test-cursor-hooks.ps1` · Reload Window · Settings → Hooks |
| Subagent | Settings / Agent ツール一覧 · `/kaggle-repo-explore` 試行 |
| Skill | `description` で意図した Skill が選ばれるか |
| Rule | alwaysApply 過多でコンテキスト膨張していないか |

---

## 9. kaggle-workflow-maintainer との分担

| 本 Skill | kaggle-workflow-maintainer |
|---|---|
| **Cursor 公式 4 機能**の設計・混同防止 | テンプレ同期 · 新コンペ bootstrap · Skill 総数管理 |
| 改善前の **公式 URL 必読** | マスター `kaggle-template` 編集フロー |
| hooks/agents インストール脚本 | `sync-project-infra-from-template.ps1` |
