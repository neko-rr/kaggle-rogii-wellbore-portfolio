# Subagent Brief — SSOT

> **親 Agent の入口:** Skill **`kaggle-subagent-delegate`**（本ファイルは詳細 SSOT）  
> 判定地図: **`_shared/DECISION-FLOW.md`**  
> カスタム定義の**編集正本:** `scripts/templates/cursor-agents/`（`.cursor/agents/` は生成物）  
> 親 Skill: **`kaggle-subagent-delegate`** · ルーター: **`kaggle-comp-router`**

---

## 原則

| 層 | 担当 |
|---|---|
| **rules + hooks** | CLI / dataset / submit の機械的ゲート |
| **親 Agent + Skill** | 判断 · exp 更新 · 提出可否 |
| **サブエージェント** | 重い **読取** · **shell 実行** · **diff/CI** · **敵対的審査（SA-7）** のみ |

- **AGENTS.md はセッション開始時に毎回読む**（親 Agent の定番。省略しない）
- サブエージェントは **Skill の置き換えではない**
- サブの返却は **構造化サマリのみ**（ファイル全文・ログ全文を親チャットに載せない）
- 詳細は `exp/` · `run-log.md` · `docs-ja/` に書き、親が索引だけ読む

---

## カスタム vs 組み込み（公式）

| 種類 | 場所 | 本 repo の使い方 |
|---|---|---|
| **組み込み** | 設定不要 | `explore` · `bash` · `browser` — 汎用 fallback |
| **カスタム** | `scripts/templates/cursor-agents/` → install → `.cursor/agents/` | **Kaggle 制約込み · 生成 · 直編集禁止** |
| **Task 型** | Agent ツール | `bugbot` · `ci-investigator`（SA-5/6 · 明示時） |

再配置: `.\scripts\install-cursor-agents.ps1`

| SA | カスタム agent | 呼び出し |
|---|---|---|
| SA-1 | `kaggle-repo-explore.md` | `/kaggle-repo-explore` |
| SA-2 | `kaggle-nb-scout.md` | `/kaggle-nb-scout` |
| SA-3 | `kaggle-discussion-scout.md` | `/kaggle-discussion-scout` |
| SA-4 | `kaggle-eval-runner.md` | `/kaggle-eval-runner` |
| SA-5 | — | Task `bugbot` |
| SA-6 | — | Task `ci-investigator` |
| SA-7 | `kaggle-adversarial-review.md` | `/kaggle-adversarial-review` |
| SA-8 | `kaggle-static-check.md` | `/kaggle-static-check` |

---

| ID | 用途 | サブエージェント | 親が残す仕事 | 依頼例 |
|---|---|---|---|---|
| **SA-1** | リポジトリ広域探索 | **`/kaggle-repo-explore`**（`.cursor/agents/`） | 解釈 → `exp-intel` / 次 Skill 選定（`kaggle-comp-router`） | 「main.py の seed 参照箇所を全部列挙」 |
| **SA-2** | 他者 NB 深掘り | **`/kaggle-nb-scout`** → 親が `notebook-analysis` | 要約フォーマット · 採用可否 · `docs-ja/others-notebook/` 出力 | 「sim-track の NB X のエントリポイントだけ」 |
| **SA-3** | Discussion 原文当たり | **`/kaggle-discussion-scout`** | `discussion-summary` で要約 · timeline/license 連携 | 「topic 123 の新規コメント有無」 |
| **SA-4** | 長時間・反復 shell | **`/kaggle-eval-runner`**（background） | `kaggle-pretrain-gate` PASS · `kaggle-kernels-runbook` · 成果を `exp/` に記録 | 「20 seed ローカル eval を回して表にまとめる」 |
| **SA-5** | diff レビュー | `bugbot`（**ユーザー明示依頼時のみ**） | `kaggle-submission-validator` + 提出判断 | 「未コミット diff をレビュー」 |
| **SA-6** | CI 失敗 1 件 | `ci-investigator` | 修正方針 · `exp/` 記録 | 「PR の failed check を 1 行で原因特定」 |
| **SA-7** | 敵対的検証（高コスト判定） | **`/kaggle-adversarial-review`** · SSOT `_shared/ADVERSARIAL-REVIEW.md` | GO は親 · Kill/Challenge なら修正 | 「Final 枠を red-team して」「Bet を敵対レビュー」 |
| **SA-8** | 静的検査（実行前） | **`/kaggle-static-check`** · `run-static-checks.ps1` | FAIL なら本実験禁止 · 親が修正 | 「書いたノートを static-check」 |

**SA-7 発火:** Bet / Final / T1 本採用 / cv_unit 固定 / harvest 直前。**毎 CHK 禁止。**  
**SA-8 発火:** Agent が `.py`/`.ipynb` を書いた直後 · train/eval 前。**エディタ Ruff は代替不可。**

---

## 返却フォーマット（全 SA 共通・必須）

サブエージェントの Task プロンプト末尾に必ず付ける:

```markdown
## Return format (mandatory)
Return ONLY this structure — no file dumps, no full logs:

### Answer
(1-2 sentences)

### Files
- path (max 15 paths)

### Findings
- bullet (max 8)

### Blockers
- or "none"

### Suggested next step
(one line — which parent Skill to use)
```

---

## Task プロンプト雛形

### SA-1 リポジトリ広域探索

```
subagent_type: explore
thoroughness: medium

Task: {ユーザーの探索依頼}
Scope: repo root {comp-root} only unless stated.
Do NOT edit files. Do NOT run competitions submit or raw kaggle.
Prefer grep/glob over reading entire trees.

{Return format}
Parent follow-up: kaggle-comp-router → experiment-result-management (exp-intel) if intel-related.
```

### SA-2 他者 NB 深掘り

```
subagent_type: explore
thoroughness: medium

Task: Locate and summarize entry points for notebook "{NB name/id}" under sim-track/ or others-notebook/.
Output: agent() / main / inference entry, key imports, config paths only.

{Return format}
Parent follow-up: notebook-analysis (full Japanese summary to docs-ja/others-notebook/).
```

### SA-3 Discussion 原文当たり

```
subagent_type: explore
thoroughness: quick

Task: Check docs-en/discussion/ for topic {id or slug}. Report whether new content exists vs docs-ja/discussion/ counterpart.
If docs-en missing, say "fetch needed" — do NOT kaggle-cli download without user OK.

{Return format}
Parent follow-up: discussion-summary (+ kaggle-cli-fetch if fetch needed).
```

### SA-4 長時間・反復 shell

```
subagent_type: shell

Task: {eval command batch — e.g. 20 seeds local eval}
Constraints:
- Use .\scripts\kaggle-cli.ps1 only (no raw kaggle)
- Write summary table to {path e.g. exp/work/YYYY-MM-DD/eval-summary.md}
- Full logs to run-log or exp/replay — not in chat return
- Stop and report if pretrain-gate would FAIL (OOM, path error)

{Return format}
Parent follow-up: kaggle-pretrain-gate (if not yet PASS) · experiment-result-management · kaggle-kernels-runbook.
```

### SA-5 diff レビュー（明示依頼時）

```
subagent_type: bugbot
readonly: true

Task: Review {branch changes | uncommitted changes}.
Focus: submission safety, secrets, dataset/ writes, agent(obs) timeout risks.

{Return format}
Parent follow-up: kaggle-submission-validator before any submit.
```

### SA-6 CI 失敗 1 件

```
subagent_type: ci-investigator

Task: Investigate failed check "{check name}" on PR {url or branch}.
Return root cause in one line + file/line if applicable.

{Return format}
Parent follow-up: fix + experiment-result-management if eval-related.
```

### SA-7 敵対的検証（高コスト判定前）

```
Prefer custom agent: /kaggle-adversarial-review
(or Task generalPurpose / explore with agent constraints from .cursor/agents/kaggle-adversarial-review.md)

You are SA-7 kaggle-adversarial-review (readonly).
Mode: {pre-bet|pre-final|pre-adopt|pre-cv-lock|pre-harvest}
Target: {CHK-id | Bet name | Final slots | pipeline path}
Hypothesis (one line): …
Must read (if exist): exp/exp-index.md, exp/experiment-checklist.md,
  docs-ja/comp-strategy.md, docs-ja/cv-design.md, exp/improvement-loop-failures.json
Do NOT edit files. Do NOT submit. Do NOT invent daily submit caps or Final N=2.
Use kill-list Q1–Q10 from _shared/ADVERSARIAL-REVIEW.md.
Return SA-7 format (Verdict, Kill shots, Checklist hits, …) only.

Parent follow-up: kaggle-experiment-checklist | kaggle-lanes-final-strategy |
  kaggle-cv-design | kaggle-knowledge-harvest | kaggle-submission-validator
  (one Skill). Parent decides GO — SA-7 does not.
```

### SA-8 静的検査（コード変更後・本実験前）

```
Prefer custom agent: /kaggle-static-check
(or shell: .\scripts\run-static-checks.ps1)

Task: Run static preflight for Agent-written code.
Paths: {changed files or CompRoot}
Editor Ruff extension does NOT count — only script exit 0.
If FAIL: list errors; do not start train/eval.
If ruff-missing WARN: tell parent to setup-kaggle-venv.ps1

Parent follow-up: fix code + re-run, or ban-gate / pretrain on PASS.
```

---

## サブエージェントを使わない（親が直接）

| 条件 | 理由 |
|---|---|
| 1 ファイル · 既知パス | Task 起動コスト > Read |
| `experiment-checklist` 1 項目ループ（通常 CHK） | 連続判断が必要 · **SA-7 も毎 CHK 禁止** |
| `submission-validator` / submit 判断 | ゲートは親 + Skill（SA-7 は代替不可） |
| `license-ledger` 更新 | Tier R は親が記録 |
| 既に `exp-index` に答えがある | 再探索不要 |

---

## 並列の可否

| OK（並列） | NG（直列） |
|---|---|
| SA-1 + SA-3 独立探索 | explore → 設計 → shell（親が中間判断） |
| 2 つの SA-1（別ディレクトリ） | SA-5 bugbot → submit（validator 必須） |
| （低優先）探索と無関係な資料集め | **SA-7 → 本実験 / Final 確定**（審査後に続行） |

---

## hooks との関係

- サブ `shell` も **beforeShellExecution** の対象（生 kaggle · submit · download 禁止）
- サブ `explore` の Write は **preToolUse** の対象（dataset/ 禁止）
- サブが failClosed で止まったら親が `kaggle-cli.ps1` 経由で再指示
