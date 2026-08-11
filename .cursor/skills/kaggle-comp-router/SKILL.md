---
name: kaggle-comp-router
description: >-
  コンペ型が未確定、または「どのSkillを使うか」迷うときに、
  comp-profile.md を基準に次に使う Skill を1つ選ぶメタ Skill。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | docs-ja/comp-profile.md · AGENTS.md · _shared/SUBAGENT-BRIEF.md | —（ルーティング提案のみ） |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Comp Router

コンペ型を判定し、**`docs-ja/comp-profile.md` を唯一のマトリクス**として参照する。

---

## 使い方

1. `AGENTS.md` の `comp-type` を確認（未設定なら判定）
2. **`docs-ja/comp-profile.md`** の **`comp-phase`**（`active` / `post-comp`）を確認
3. **迷いのとき先に** `_shared/DECISION-FLOW.md`（フェーズ × 次 Skill）
4. **`docs-ja/folder-map.md`** を読む（置き場所 SSOT）
5. `comp-phase` に応じた **タスク別ルーティング** 節だけを読む（全文読まない）
6. ユーザー依頼に対して、次に使う Skill を **1つ** 提示
7. 広域探索・長時間 shell → **`/kaggle-subagent-delegate`**（明示依頼時）  
   高コスト判定（Bet · Final · 本採用 · CV 固定 · harvest）→ **SA-7** / Skill **`kaggle-adversarial-review`**

**休眠 Skill**（`comp-profile.md` § 休眠）を post-comp で選ばない。

---

## ルーターが返すべき内容

- `comp-type`（必要なら更新提案）
- 次に使う Skill 名（1つ）
- 参照先 SSOT（`comp-profile.md` / `comp-timeline.md` など）

未作成 Skill（例: `metric-local-repro`, `agent-debug`）は、`comp-profile.md` の代替手段（**`metric-repro.md`** / **`agent-debug.md`** 等）を案内する。

---

## Agent 規則

1. 型固有 Skill の前に `comp-type` を確定する
2. マトリクスを Skill 本文に再掲しない（`comp-profile.md` のみ）
3. dataset ダウンロードはユーザー指示時のみ

---

## よく使う Skill（早見 · 詳細は comp-profile）

| comp-phase | 参照 |
|---|---|
| **post-comp** | `comp-profile.md` § post-comp マトリクス |
| **active** | `comp-profile.md` § active マトリクス |
| infra / 委譲 | `/cursor-agent-infra` · `/kaggle-subagent-delegate`（明示 `/` 呼び出し） |

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\docs-ja\comp-profile.md.template`
