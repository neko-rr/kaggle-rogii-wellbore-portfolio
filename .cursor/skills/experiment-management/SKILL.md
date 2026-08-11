---
name: experiment-management
description: Kaggle の実験管理方法。exp 4層レイアウト、学習/推論の実験ID、exp-index 等 SSOT への記録先を判断する
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| reorganize-exp-layout.ps1（ユーザー指示時） | — | — | exp/ · README.md | exp/ root SSOT · latest/ · work/ · archive/ · protocol/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。

# exp/ レイアウト（4 層）

> 地図: `<comp-root>/exp/README.md`

| 層 | パス | 用途 |
|---|---|---|
| **必須 SSOT** | `exp/*.md`（root 7 ファイルのみ） | Skill 定義の索引 · train · infer · intel · 表 · CHK · run-ledger |
| **protocol** | `exp/protocol/` | ローカル検証 SSOT（protocol v2 等） |
| **latest** | `exp/latest/` + **`manifest.md`** | 最新・有効な分析（1 トピック 1 本） |
| **work** | `exp/work/YYYY-MM-DD/` | 当日 WIP · compare メモ |
| **archive** | `exp/archive/history/` · `superseded/` | 置換済み / 方法論 reject |
| **replay** | `exp/replay/` | episode JSON のみ |
| **local-eval** | `exp/local-eval/` | protocol 実行 JSON · bots.yaml |

**Agent 禁止:** `exp/` root に分析 MD を新規作成しない。

# 記録ファイルの基本（root）

| ファイル | 記録する内容 |
|---|---|
| `exp/exp-index.md` | 現在地、Best、次アクション → **`latest/manifest.md` へリンク** |
| `exp/exp-train.md` | 学習、CV、fold、データ、モデル、loss、特徴量 |
| `exp/exp-infer.md` | 推論、後処理、提出、LB。**tabular:** § blend。**simulation:** § simulation 提出 |
| `exp/exp-intel.md` | 他者Notebook、Discussion、上位解法、外部知見 |
| `exp/run-ledger.md` | **1 run** の env / GPU 時間 / 概算コスト / metric / delta |
| `exp/hyperparameter-table.md` | 実験 ID 別表 |
| `exp/experiment-checklist.md` | **仮説検証** **CHK-** ループ（fork は手段 · Skill `kaggle-experiment-checklist`） |
| `exp/improvement-loop-failures.json` | **Fnnn 禁止**台帳のみ（知見ではない · `_shared/EXPERIMENT-ID-NAMESPACES.md`） |

# 分析 MD の置き場所

| 状態 | 置き場 | 操作 |
|---|---|---|
| 当日ドラフト | `work/YYYY-MM-DD/` | 自由に追加 |
| 判断確定 | `latest/` | `latest/manifest.md` 更新 · 旧版 → `archive/history/` |
| 方法論 reject | `archive/superseded/` | manifest から外す · `superseded/README.md` 参照 |
| 置換済み（正しい過去） | `archive/history/` | manifest の `replaces` に記載 |

# 命名規則

フォルダ名・ファイル名は **小文字 + ハイフン（kebab-case）**。

# 主要な実験（脚本の変更 · tabular）

1. 新しい実験ディレクトリ: `exp/exp{no}/`（例: `exp/exp000/`）— **simulation では未使用可**
2. 学習 → `exp-train.md`、提出 → `exp-infer.md`
3. 長時間 GPU → `run-ledger.md` + `comp-timeline` 戦略節

# 推論・提出だけの実験

1. `exp-infer.md` に記録
2. `hyperparameter-table.md` に `infer_###` / `submit_###`
3. 深い replay 分析 → `latest/`（manifest 更新）

# 他者分析・Discussion

`exp-intel.md` に記録（自チーム replay 分析は `latest/` と混ぜない）。

# Notebook フォルダ（Skill: `kaggle-notebook-folders`）

| フォルダ | 用途 |
|---|---|
| `my-notebook/` | 編集中 WIP |
| `my-notebook/planned/` | 未実行キュー |
| `my-local-eval-notebook/` | 検証 fork |
| `my-ran-notebook/` | 実行済み・未提出 |
| `my-submitted-notebook/` | 提出済み（参照のみ） |

取り込んだ仮説は **`kaggle-experiment-checklist`** で `experiment-checklist.md` に dedupe。
