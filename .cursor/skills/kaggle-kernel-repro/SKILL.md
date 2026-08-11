---
name: kaggle-kernel-repro
description: >-
  tabular / notebook 提出コンペ向け。公開 Kaggle kernel + input をローカル workspace に再現。
  setup-kernel-workspace、kernels pull、notebook 再現、others-notebook/workspaces と言ったときに使う。
  simulation コンペでは使わない。eval CSV fork は local-eval-from-submit-notebook に任せる。
  dataset 一括 DL はユーザー明示 OK 後のみ。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| setup-kernel-workspace.ps1 · kaggle-cli.ps1 | Kaggle HTTPS · kernels pull | 読取のみ。token/.env をログ・Git 禁止 | comp-root | others-notebook/workspaces/（編集は my-notebook/ へコピー後） |

**要ユーザー明示 OK:** -DownloadInputs · competition/dataset 一括 DL

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Kernel Repro

**tabular / notebook-output / lora 専用。** NVIDIA [kernel-setup](https://github.com/NVIDIA/nvidia-kaggle/blob/main/skills/nvidia-kaggle-skill/kernel-setup.md) 相当。

## 使わない comp-type

| comp-type | 理由 | 代わり |
|---|---|---|
| **simulation** | 提出 = `main.py` / tar.gz | `agent-debug.md` · `kaggle_environments` |
| agent / Games | 同上 | `kaggle-simulation-tracker` |

`comp-profile.md` で `comp-type` を確認してから使う。

## 役割分担

| Skill | 担当 |
|---|---|
| **本 Skill** | kernel pull · metadata · 任意 input DL · workspace |
| `kaggle-cli-ops` | venv · OAuth preflight |
| `kaggle-notebook-folders` | `others-notebook/workspaces/` 配置規約 |
| `notebook-analysis` | 再現後の **日本語要約** → `docs-ja/others-notebook/` |
| `local-eval-from-submit-notebook` | **自チーム提出 NB** の eval CSV fork |
| `local-eval-improvement-orchestrator` | eval 改善ループ全体 |

## 前提

- `setup-kaggle-venv.ps1`（**cli** profile）
- OAuth 済み
- **Agent:** `--download-inputs` は **ユーザー明示 OK 後のみ**（容量 · ルール同意）
- **DL 前:** Skill `kaggle-cli-ops` **ダウンロード前チェック** 表を必ず通す（部分 workspace · archive 失敗で止める）

## Phase 1 — kernel のみ（軽量 · Agent 可）

```powershell
cd <repo-root>
.\scripts\setup-kernel-workspace.ps1 `
  -Kernel "https://www.kaggle.com/code/owner/kernel-slug" `
  -Competition <comp-slug>
```

出力: `<comp-root>/others-notebook/workspaces/<owner>-<slug>/`

| パス | 内容 |
|---|---|
| `working/` | `.ipynb` / script |
| `tmp/kernel-metadata.json` | input ソース一覧 |
| `manifest.json` | 機械可読索引 |
| `README.md` | 人間向け手順 |
| `create_symlinks.sh` | `/kaggle/input/` マップ（検出時） |

## Phase 2 — input ダウンロード（ユーザー OK 後）

```powershell
.\scripts\setup-kernel-workspace.ps1 `
  -Kernel "owner/kernel-slug" `
  -Competition <comp-slug> `
  -DownloadInputs
# competition data 不要なら
.\scripts\setup-kernel-workspace.ps1 ... -DownloadInputs -SkipCompetition
```

`kernel-metadata.json` の:

- `competition_sources`
- `dataset_sources`
- `kernel_sources`

を `input/` 以下に取得。

## Phase 3 — ローカル eval（自チーム NB のとき）

他人 NB を **参考** にするだけなら Phase 1–2 で足りる。  
**自チーム提出 NB** を検証する場合 → Skill **`local-eval-from-submit-notebook`**（`my-local-eval-notebook/`）。

## ワークスペース構造（NVIDIA 互換）

```text
others-notebook/workspaces/{owner}-{slug}/
├── input/
├── working/
├── tmp/
├── scripts/
│   └── __init__.py
├── manifest.json
├── README.md
└── create_symlinks.sh
```

## 収集後

1. 要約が必要 → `notebook-analysis`（`docs-ja/others-notebook/`）
2. intel 追記 → `exp/exp-intel.md`（事実のみ）
3. **編集は `others-notebook/` 直接禁止** — `my-notebook/` にコピーしてから（`kaggle-notebook-folders`）

## トラブルシュート

| 症状 | 対処 |
|---|---|
| 403 competition DL | Kaggle で Rules 同意 → 再実行 |
| 403 dataset | metadata の owner/slug を `kaggle datasets list -s` で確認 |
| paths が合わない | `README.md` · `create_symlinks.sh` · 手動マップ |
| disk 不足 | `-DownloadInputs` 中止 · 必要 source だけ手動 DL |

## 関連

- NVIDIA kernel-setup: https://github.com/NVIDIA/nvidia-kaggle/blob/main/skills/nvidia-kaggle-skill/kernel-setup.md
- `kaggle-cli-ops` · 公式 CLI: https://pypi.org/project/kaggle/#description
