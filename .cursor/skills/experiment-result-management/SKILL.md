---
name: experiment-result-management
description: Kaggle の実験結果管理。exp-index、manifest、4ファイル SSOT、latest/archive への分析の読み書きと LB 報告更新
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | exp-index · latest/manifest · lifecycle-manifest.md · archive/ | root SSOT · latest/ · work/ · exp/latest/manifest.md · lifecycle-manifest.md（root 分析 MD 禁止） |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。

# 読み順（固定）

1. `exp/exp-index.md`（**現在地 SSOT** · Best / tip / 次アクション）
2. **`exp/experiment-checklist.md` の Active**（作業キュー · 実験指示の主画面）
3. **`exp/latest/manifest.md`**（分析 MD 索引）
4. **`lifecycle-manifest.md`**（comp-root · 成果物状態索引）
5. 目的別: `exp-infer.md` / `protocol/` / archive 等

**Rule:** `kaggle-exp-ssot` — checklist / AGENTS / cursor に Best スコアを再掲しない。ずれ検知: `scripts/check-exp-ssot.ps1`。

# 標準ファイル構成

| ファイル | 役割 | 主な更新タイミング |
|---|---|---|
| `exp/exp-index.md` | **現在地 SSOT** | Best 更新 · 方針転換 · 次アクション変更時 |
| `exp/latest/manifest.md` | **最新分析の索引** | 分析確定 · 昇格 · supersede 時 |
| `exp/exp-train.md` | 学習 · CV | 学習報告時 |
| `exp/exp-infer.md` | 提出 · LB | 提出 · LB 報告時 |
| `exp/exp-intel.md` | 他者 · Discussion | 調査時 |
| `exp/hyperparameter-table.md` | 実験 ID 表 | **各実験時（必須）** |
| `exp/experiment-checklist.md` | Active 作業キュー | **各実験時（当該行必須）** · ヘッダにスコア禁止 |
| `exp/checklist-archive.md` | 終了 CHK / 旧 Wave | Wave 終了 · 週次 |
| `exp/run-ledger.md` | GPU / コスト | 長時間 run 後 |

# サブフォルダ（分析）

| パス | 書き込み |
|---|---|
| `exp/work/YYYY-MM-DD/` | 当日 WIP |
| `exp/latest/` | 確定版のみ + manifest 更新 |
| `exp/archive/history/` | 置換された旧版 |
| `exp/archive/superseded/` | reject 確定（提出判断に使わない） |
| `exp/protocol/` | ローカル検証 SSOT |
| `exp/replay/` | JSON のみ（Agent は DL 脚本経由） |

# 読むファイルの判断

| ユーザー依頼 | 読むファイル |
|---|---|
| 現状 · 次アクション | `exp-index.md` → checklist **Active** → **`latest/manifest.md`** |
| LB · 提出結果 | `exp-index.md` → `exp-infer.md` → `hyperparameter-table.md` |
| 学習 · CV | `exp-index.md` → `exp-train.md` → `hyperparameter-table.md` |
| 次の打ち手 | checklist **Active**（主画面）→ `exp-index` で現在地確認 → train/infer/intel |
| 過去 CHK · 旧 Wave | `checklist-archive.md` / `archive/` |
| replay · slot 分析 | **`latest/manifest.md`** → リンク先 MD |
| ローカル検証 | `protocol/local-eval-protocol-v2.md` + `local-eval/runs/` |
| 過去 · reject 確認 | `archive/superseded/README.md` |

# LB 結果を報告された場合

1. **`exp-index.md` の現在地を更新**（Best / 提出 / 次アクション）— ここが SSOT
2. **`exp/work-protect.json` の `best_artifact` / `best_zip` を同じ Best に合わせる**（cleanup 保護 · Rule `kaggle-exp-work-cleanup`）
3. `exp-infer.md` · `hyperparameter-table.md` 更新
4. **移動必須（提出済みの場合）:** `lifecycle-manifest.md` の `submit_ref` · μ · note を更新（Skill `kaggle-notebook-folders`）
5. 該当 CHK 行を checklist Active で done に（スコアは checklist に書かない）
6. 任意: `scripts/check-exp-ssot.ps1`

# 学習 · CV 結果を報告された場合

1. `exp-train.md` · `hyperparameter-table.md` 更新
2. 提出候補なら `exp-infer.md` に反映
3. **次アクションや Best 見込みが変わったときだけ** `exp-index.md` 更新
4. checklist Active の当該行を更新
5. `prior-knowledge.md` のカードを根拠にした実験なら、Skill `kaggle-knowledge-feedback` でGO/NO-GOとsource_refを記録

# 新規分析 MD を書く場合

1. まず `work/YYYY-MM-DD/` に作成
2. 確定したら `latest/` へ移動 · **`manifest.md` 1 行更新**
3. 旧 current → `archive/history/`（manifest の `replaces` に記載）
4. 方法論 reject → `archive/superseded/`

# コンペ固有の生成物が root に出た場合

1. 可能なら発生元の出力先を `exp/work/<role>/` に変更する
2. 発生元を直せない場合、固有 pattern を **`exp/artifact-routing.json`** に追加する（Rule / 共通脚本には書かない）
3. `scripts/organize-generated-files.ps1 -ExpDir <exp>` でドライラン
4. 件数・容量・移動先を確認後、`-Apply` で移動する（削除なし · JSONL 履歴あり）

# 文書化基準

- 学習 → `exp-train.md`、提出 → `exp-infer.md`、他者 → `exp-intel.md`
- 自チーム replay 深掘り → `latest/`（`exp-infer` にはサマリ + リンクのみ）
- **simulation:** `sim-track/` → intel 時 peak-ui 注記（Skill `kaggle-simulation-tracker`）

---

## サブエージェント連携（SA-1 / SA-4 / SA-6 後）

- Task `explore` / `shell` / `ci-investigator` の **サマリのみ**を受け取り、本 Skill で `exp-intel.md` · `exp-infer.md` · `exp-index.md` に確定記録
- サブ返却の全文ログは `exp/work/` または `run-log.md` へ — チャットに再掲しない
- SSOT: `_shared/SUBAGENT-BRIEF.md`
