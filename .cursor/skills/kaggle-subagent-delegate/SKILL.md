---
name: kaggle-subagent-delegate
description: >-
  重い探索・shell・レビューを Cursor サブエージェント（Task）に委譲し、
  親 Agent は Skill 判断と exp 更新に集中する。広域探索、NB 深掘り、
  Discussion 当たり、長時間 eval、bugbot、CI 調査、敵対的検証（SA-7）と言ったときに使う。
  サブエージェント、Task、explore、コンテキスト削減と言ったときに使う。
disable-model-invocation: true
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| Task 起動（SA-4 本体は subagent shell） | サブに委譲 | — | _shared/SUBAGENT-BRIEF.md · AGENTS.md · exp-index | —（follow-up Skill が記録） |

**要ユーザー明示 OK:** bugbot · 長時間 shell/GPU · submit（親のみ）

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Subagent Delegate

**親 Agent のオーケストレーション Skill。** サブエージェント委譲時は **親が本 Skill だけ読めば足りる**（`SUBAGENT-BRIEF.md` · `.cursor/agents/README.md` は本 Skill から参照）。

詳細 SSOT: [**`_shared/SUBAGENT-BRIEF.md`**](../_shared/SUBAGENT-BRIEF.md)  
敵対的検証: [**`_shared/ADVERSARIAL-REVIEW.md`**](../_shared/ADVERSARIAL-REVIEW.md) · Skill **`kaggle-adversarial-review`**

---

## 使い方（固定 4 ステップ）

1. **AGENTS.md を読んだ上で** 依頼を SA-1〜7 に分類（`_shared/SUBAGENT-BRIEF.md` マトリクス）
2. **カスタムサブエージェント**を起動 — SA-1〜4 · **SA-7** · **SA-8** は `.cursor/agents/` の `/kaggle-*` を優先（正本は `scripts/templates/cursor-agents/`）。SA-5/6 は Task `bugbot` / `ci-investigator`
3. サブの **Answer / Findings / Suggested next step** のみ受け取る（ファイル全文は読まない）。SA-7 は **Verdict · Kill shots** も必須。SA-8 は **static verdict**
4. **親** が follow-up Skill を **1 つ** 実行し、必要なら `exp/` · `docs-ja/` に記録

---

## SA → follow-up Skill

| ID | サブ | 親 follow-up |
|---|---|---|
| SA-1 | `/kaggle-repo-explore` | `kaggle-comp-router` → `experiment-result-management` |
| SA-2 | `/kaggle-nb-scout` | `notebook-analysis` |
| SA-3 | `/kaggle-discussion-scout` | `discussion-summary`（必要なら `kaggle-cli-fetch`） |
| SA-4 | `/kaggle-eval-runner` | `kaggle-pretrain-gate` · `kaggle-kernels-runbook` · `experiment-result-management` |
| SA-5 | bugbot（Task） | `kaggle-submission-validator` |
| SA-6 | ci-investigator（Task） | 修正 + `experiment-result-management`（該当時） |
| SA-7 | `/kaggle-adversarial-review` | 判定後: checklist · lanes · cv-design · harvest · validator の **1 つ**（GO は親） |
| SA-8 | `/kaggle-static-check` | FAIL→修正+再検 · PASS→ ban / smoke / pretrain |

---

## Agent 規則

1. **Skill の置き換えにしない** — validator · pretrain-gate · checklist は必ず親 + 該当 Skill  
   SA-7 も ban-gate / validator の代替にしない
2. **小さい探索は親** — 1 ファイル · 既知パスは Read / Grep（SA-1 不要）
3. **並列** — 独立した SA-1 / SA-3 のみ。**SA-7 → 本実験は直列**
4. **CLI** — サブ shell 指示は `.\scripts\kaggle-cli.ps1` のみ
5. **記録** — サブは summary ファイル可 · 確定版は親が `exp/latest/` へ
6. **SA-7** — Bet / Final / T1 本採用 / cv 固定 / harvest 直前のみ。**毎 CHK 禁止**

---

## ユーザー依頼の言い方（例）

| 依頼 | SA |
|---|---|
| main.py の seed 参照を全部 | SA-1 |
| sim-track の NB X エントリポイントだけ | SA-2 |
| topic 123 新規コメントある？ | SA-3 |
| 20 seed ローカル eval 表にまとめて | SA-4 |
| 未コミット diff をレビュー | SA-5 |
| PR の failed check 原因 1 行 | SA-6 |
| Final 枠 / Bet を敵対レビュー | SA-7 |
| harvest 前に教訓を red-team | SA-7 mode=pre-harvest |
| 書いたコードを実行前に static | SA-8 |
