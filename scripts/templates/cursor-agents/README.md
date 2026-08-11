# Cursor カスタムサブエージェント（テンプレ = SSOT）

> **編集してよい場所は本フォルダのみ**  
> `scripts/templates/cursor-agents/`  
> 配置先 `.cursor/agents/` は **`install-cursor-agents.ps1` の生成物**。直編集は禁止。

公式: [サブエージェント](https://cursor.com/ja/docs/subagents)  
併用: `_shared/SUBAGENT-BRIEF.md` · `_shared/DECISION-FLOW.md` · `_shared/STATIC-CHECKS.md`

## エージェント一覧

| ファイル | 呼び出し | SA | readonly |
|---|---|---|---|
| `kaggle-repo-explore.md` | `/kaggle-repo-explore` | SA-1 | yes |
| `kaggle-nb-scout.md` | `/kaggle-nb-scout` | SA-2 | yes |
| `kaggle-discussion-scout.md` | `/kaggle-discussion-scout` | SA-3 | yes |
| `kaggle-eval-runner.md` | `/kaggle-eval-runner` | SA-4 | no · background |
| `kaggle-adversarial-review.md` | `/kaggle-adversarial-review` | SA-7 | yes · red-team |
| `kaggle-static-check.md` | `/kaggle-static-check` | SA-8 | no · static script |

SA-5 bugbot · SA-6 ci-investigator は組み込み Task（明示依頼時）。

## 再インストール

```powershell
.\scripts\install-cursor-agents.ps1
# or
.\scripts\install-cursor-infra.ps1
```

## 親の流れ

1. AGENTS.md · DECISION-FLOW
2. コード編集後は **SA-8 / run-static-checks** が train より先
3. `/kaggle-*` 委譲 → 構造化サマリのみ
4. 親 Skill で exp 確定
