# Artifact Lifecycle — SSOT

> 成果物（Notebook / `main.py` ツリー / zip）の **置き場所** と **状態遷移**。  
> 索引: **`{comp-root}/lifecycle-manifest.md`**（`exp/latest/manifest.md` と同型）。  
> 運用 Skill: **`kaggle-notebook-folders`**。移動トリガー: **`kaggle-kernels-runbook`** · **`kaggle-submission-validator`** · **`local-eval-from-submit-notebook`**。

---

## comp-type 別の成果物単位

| comp-type | 成果物単位 | 典型パス | 備考 |
|---|---|---|---|
| **tabular / notebook-output** | `.ipynb` 1 本 | `my-notebook/foo.ipynb` | Kaggle/Colab 実行後に移動 |
| **simulation / csv / lora** | ディレクトリ（`main.py` または提出 zip 展開） | `my-notebook/the-bot/` | ルートまたは `bot/` に `agent(obs)` |
| **csv / lora** | zip / csv ファイル | WIP は `my-notebook/` 配下 | validator PASS 後に凍結コピー |

`AGENTS.md` の `submission-profile` と `docs-ja/comp-profile.md` の `comp-type` で判定する。

---

## フォルダ ↔ 状態

| 状態 ID | フォルダ | 意味 |
|---|---|---|
| `wip` | `my-notebook/` | 編集中・実行直前 |
| `planned` | `my-notebook/planned/` | **未実行** のみ（ipynb または bot ツリー） |
| `local-eval` | `my-local-eval-notebook/{name}/` | 検証専用 fork（**提出しない**） |
| `ran` | `my-ran-notebook/{name}/` | 実行済み・未提出（または提出保留） |
| `submitted` | `my-submitted-notebook/{name}/` | LB 提出済み **凍結** |

---

## 遷移（Agent は **移動 + manifest 更新** をセットで行う）

```
wip ──後回し──► planned ──実行準備──► wip
wip / planned ──実行完走 or ローカル run 記録──► ran (+ run-log.md)
提出 NB から fork ──► local-eval（my-local-eval-notebook/ のみ）
ran / wip ──validator PASS──► submitted（コピー・凍結）
```

**禁止:** 実行済みを `planned/` に戻す · `my-submitted-notebook/` を編集 · local-eval を `my-notebook/` に残す。

---

## lifecycle-manifest.md（comp-root 直下）

### 役割

- 全成果物の **現在状態・物理パス・提出 ref** を 1 表に集約
- `exp/latest/manifest.md` が **分析 MD** の索引なら、本ファイルは **コード成果物** の索引

### 列（テンプレ）

| name | state | folder | path | artifact | submit_ref | updated | note |
|---|---|---|---|---|---|---|---|

- **state:** `wip` · `planned` · `local-eval` · `ran` · `submitted`
- **artifact:** `ipynb` · `main.py-dir` · `zip` · `csv` 等
- **submit_ref:** Kaggle submission id（未提出は `—`）

### 更新タイミング

| イベント | 更新者 |
|---|---|
| bootstrap 初回 | `kaggle-comp-bootstrap`（空テンプレ配置） |
| Kaggle/Colab 実行後 | `kaggle-kernels-runbook` Step |
| local-eval fork 作成 | `local-eval-from-submit-notebook` Step |
| validator PASS → 凍結 | `kaggle-submission-validator` Step |
| LB 報告・μ 確定 | `experiment-result-management`（`submit_ref` · note） |

---

## テンプレート配置

| ファイル | 用途 |
|---|---|
| `scripts/templates/lifecycle-manifest.md.template` | comp-root |
| `scripts/templates/folder-map.md.template` | **置き場所 SSOT** → `docs-ja/folder-map.md` |
| `scripts/templates/comp-start-checklist.md.template` | Day 0 チェックリスト |
| `scripts/templates/my-*-notebook-README.md.template` | 各フォルダ README |
| `scripts/init-comp-layout.ps1` | 上記を comp-root へ一括配置 |

グローバル `%USERPROFILE%\.cursor\kaggle-template\comp\` へ同期する場合は Skill **`kaggle-workflow-maintainer`** の手順に従う。
