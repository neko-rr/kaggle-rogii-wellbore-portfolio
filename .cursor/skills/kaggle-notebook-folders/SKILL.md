---
name: kaggle-notebook-folders
description: >-
  Kaggle コンペの Notebook / 提出成果物フォルダ役割と移動ルール。my-notebook、planned、
  my-local-eval-notebook、my-ran-notebook、my-submitted-notebook、others-notebook。
  lifecycle-manifest.md（comp-root）で状態索引。comp-type 別（simulation = main.py ディレクトリ）。
  Notebook の置き場所、提出済み、未実行、検証専用と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | my-*-notebook/ · others-notebook/ · lifecycle-manifest.md | lifecycle-manifest.md · my-*-notebook/ 移動（各 Skill Step 連携） |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Notebook Folders

成果物は **ライフサイクル** でフォルダを分ける。コンペ開始時に `kaggle-comp-bootstrap` で一式生成される。

**SSOT:** `.cursor/skills/_shared/ARTIFACT-LIFECYCLE.md` · **`docs-ja/folder-map.md`**（人間向け1枚）  
**索引:** `{comp-root}/lifecycle-manifest.md`（`exp/latest/manifest.md` と同型 — 成果物用）

---

## フォルダ一覧

```text
yyyymmdd-comp-name/
├─ lifecycle-manifest.md         # ★ 成果物状態索引（comp-root 直下）
├─ my-notebook/                  # Cursor が編集する WIP（いま触るもの）
│  └─ planned/                   # 作成済み・未実行・実行後回しキュー
├─ my-local-eval-notebook/        # 検証専用 fork（提出しない）
├─ my-ran-notebook/              # 実行済み・未提出
├─ my-submitted-notebook/       # 提出済みスナップショット（編集禁止）
├─ others-notebook/              # 他者 .ipynb 生コピー（コンペ中）
└─ retro/archive/                # コンペ終了後の NB アーカイブ
```

要約は `docs-ja/others-notebook/`（Skill: `notebook-analysis`）。

---

## comp-type 別：成果物単位

| comp-type | 成果物 | WIP の置き方 | 実行後 |
|---|---|---|---|
| **tabular / notebook-output** | `.ipynb` | `my-notebook/foo.ipynb` | `my-ran-notebook/foo/` |
| **simulation** | **`main.py` ディレクトリ** | `my-notebook/the-bot-v3/`（ルート or `bot/main.py`） | `my-ran-notebook/the-bot-v3/` |
| **csv / lora** | zip / csv | `my-notebook/` 配下 | validator 経由で `my-submitted-notebook/` |

simulation では **ipynb だけでなく bot ツリー全体** を 1 成果物として移動する。`-local-eval` サフィックスの bot を `my-notebook/` に残さない。

---

## 定義

| フォルダ | 状態 ID | Agent が編集 |
|---|---|---|
| `my-notebook/` | `wip` | ✅ |
| `my-notebook/planned/` | `planned` | △（未実行の整理のみ） |
| `my-local-eval-notebook/{name}/` | `local-eval` | ✅ |
| `my-ran-notebook/{name}/` | `ran` | △（ログ追記程度） |
| `my-submitted-notebook/{name}/` | `submitted` | ❌ |
| `others-notebook/` | — | ❌（`my-notebook/` にコピーしてから編集） |

### `planned/` の要点

- **未実行** のみ（ipynb または simulation bot ツリー）
- 実行した瞬間 → **`my-ran-notebook/{name}/`** へ移動（`planned/` に留めない）

---

## 移動フロー（tabular）

```
[設計] → my-notebook/ で作成
    ↓ 後回し・未実行のまま保留
my-notebook/planned/
    ↓ 実行する直前
my-notebook/（親）
    ↓ Kaggle/Colab 完走 or run 記録
my-ran-notebook/{name}/  +  lifecycle-manifest → ran
    ↓ validator PASS → LB 提出
my-submitted-notebook/{name}/（コピー・凍結） + manifest → submitted
```

## 移動フロー（simulation）

```
my-notebook/{bot-name}/     # main.py ツリー WIP
    ↓ ローカル sim / NB 実行記録
my-ran-notebook/{bot-name}/ + run-log.md
    ↓ 提出用に確定 · validator PASS
my-submitted-notebook/{submit-ref}-{bot-name}/

local-eval fork のみ:
my-submitted-notebook/…  ──fork──►  my-local-eval-notebook/{name}-local-eval/
（my-notebook/ に local-eval を置かない）
```

---

## lifecycle-manifest.md

comp-root 直下。Agent は **フォルダ移動と同ターンで必ず 1 行更新**する。

テンプレ: `scripts/templates/lifecycle-manifest.md.template`

| 列 | 内容 |
|---|---|
| name | 成果物名（bot 名 · nb 名） |
| state | wip · planned · local-eval · ran · submitted |
| folder | 上表のフォルダ |
| path | リポジトリ内相対パス |
| artifact | ipynb · main.py-dir · zip · csv |
| submit_ref | Kaggle submission id（未提出 `—`） |
| updated | YYYY-MM-DD |
| note | μ · 有効枠 · legacy 等 |

---

## Agent 必須（状態変更時）

1. **物理移動**（または submitted へのコピー）
2. **`lifecycle-manifest.md` 更新**
3. 該当 Skill の Step を完了として記録（run-log · exp-infer 等）

移動だけして manifest を更新しない — **混在の主因**。

---

## Agent 禁止

- `my-submitted-notebook/` を提出用として改変しない
- 実行済みを `planned/` に戻さない
- `others-notebook/` を直接編集しない
- 検証 NB / bot と提出 NB / bot を同一ディレクトリに混ぜない
- local-eval fork を `my-notebook/` に残す

---

## コンペ終了後

- 重要な他者 NB + 自チーム記録 → `retro/archive/`
- **終了後公開**の上位 kernel → `retro/archive/others-notebook/post-comp-top-YYYYMMDD/rankNN-…/`（コンペ中 `others-notebook/` と混ぜない）
- 解法要約 → `retro/retro-solutions.md`（Skill: `solution-analysis` · **CV 物差し vs 解法本体を分離**）
- 教訓 → `retro/retro-lessons.md` の `### A/B/C`（Skill: `kaggle-knowledge-harvest`）
- **retro 一括移動はユーザー指示時のみ**（終了コンペの legacy パスを勝手に整理しない）

---

## 連携 Skill（移動必須 Step）

| Skill | トリガー | 移動先 · manifest |
|---|---|---|
| `kaggle-kernels-runbook` | 実行後 | `ran` |
| `local-eval-from-submit-notebook` | fork 作成 | `local-eval`（`my-local-eval-notebook/` のみ） |
| `kaggle-submission-validator` | PASS | `submitted` |
| `experiment-result-management` | LB 報告 | `submit_ref` · note 更新 |

---

## テンプレート

| パス | 用途 |
|---|---|
| `scripts/templates/lifecycle-manifest.md.template` | comp-root |
| `scripts/templates/folder-map.md.template` | `docs-ja/folder-map.md` |
| `scripts/init-comp-layout.ps1` | 新コンペ一括配置 |
| `%USERPROFILE%\.cursor\kaggle-template\comp\` | グローバル同期先（任意） |
