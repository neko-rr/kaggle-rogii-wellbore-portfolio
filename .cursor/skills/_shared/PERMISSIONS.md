# Skill Permissions — SSOT

> NVIDIA [nvidia-kaggle-skill](https://github.com/NVIDIA/nvidia-kaggle/blob/main/skills/nvidia-kaggle-skill/SKILL.md) の permissions 表を自チーム向けに一般化。  
> 各 Skill 先頭に **5 行以内** の表を置く。更新時は本ファイル → `scripts/skill-permissions-map.json` → `scripts/sync-skill-permissions.ps1`。

## 列の意味

| 列 | 内容 |
|---|---|
| **shell** | 実行してよい `scripts/*.ps1` · `.venv` 内 python |
| **network** | Kaggle HTTPS / — |
| **env** | 環境変数。**`KAGGLE_*` · `KAGGLE_API_TOKEN` をログ・Git・チャットに出さない** |
| **file_read** | 読んでよいパス |
| **file_write** | 書いてよいパス（**`dataset/` 編集禁止** · 秘匿禁止） |

## 全 Skill 共通禁止

- `competitions submit` · `kernels push` · **public dataset 作成** → **ユーザー明示 OK まで Agent 実行禁止**
- `competitions download` / `datasets download` 一括 → **ユーザー明示 OK**
- グローバル `pip install kaggle` · 生 `kaggle` コマンド
- `.kaggle/` · `.env` · `kaggle.json` を Git にコミット

## プロファイル早見

| ID | shell | 要ユーザー OK |
|---|---|---|
| **P-doc** | — | — |
| **P-subagent** | Task explore/shell/bugbot/ci-investigator · SA-7 adversarial | bugbot · 長時間 shell |
| **P-infra** | `/cursor-agent-infra` · `/kaggle-workflow-maintainer` · `/kaggle-subagent-delegate` | 明示 `/` 呼び出し（`disable-model-invocation: true`） |
| **P-exp** | — | — |
| **P-cli-read** | `kaggle-cli.ps1` · fetch 系 | 大容量 DL |
| **P-cli-setup** | `setup-kaggle-venv.ps1` · `check-kaggle-cli.ps1` | — |
| **P-validate** | `validate-*.ps1` · `check-*.ps1` | **`competitions submit`** |
| **P-kernel** | `setup-kernel-workspace.ps1` | **`-DownloadInputs`** |
| **P-infra** | `scripts/*` · sync テンプレ | push 公開 repo |

## 点検チェックリスト

- [x] 各 Skill に `## Permissions（Agent 境界）` がある（33/33 — `sync-skill-permissions.ps1`）
- [x] submit / DL の要 OK が Skill 内容と矛盾しない（validator · cli-fetch · kernel-repro で明示）
- [x] simulation 専用 Skill が tabular 向け shell を許可していない（`kaggle-kernel-repro` は tabular、`comp-profile` 参照）

## 関連 SSOT

- 成果物ライフサイクル · `lifecycle-manifest.md`: `.cursor/skills/_shared/ARTIFACT-LIFECYCLE.md`
