# フォルダマップ — rogii-wellbore

> **Agent / 人間の最初の1枚。** 「何をどこに置くか」の SSOT。  
> comp-type: **tabular** · submission-profile: **csv**  
> 関連: [`lifecycle-manifest.md`](../lifecycle-manifest.md) · [`comp-start-checklist.md`](comp-start-checklist.md) · Skill `kaggle-notebook-folders`

---

## 二つの索引（混同禁止）

| 索引 | パス | 対象 |
|---|---|---|
| **成果物（コード）** | `{comp-root}/lifecycle-manifest.md` | bot / ipynb / zip の **今どこにあるか** |
| **分析 MD** | `exp/latest/manifest.md` | replay 解析 · 強みゲート等 **確定分析** |

---

## comp-root 全体

```text
{comp-root}/
├─ lifecycle-manifest.md       # 索引A — コード成果物
├─ dataset/                    # 公式 Data（手動 DL · Git 除外）
│  └─ derived/                 # competitions download 先
├─ my-notebook/                # WIP（編集中 bot / ipynb）
│  └─ planned/                 # 未実行のみ
├─ my-local-eval-notebook/     # 検証 fork のみ
├─ my-ran-notebook/            # 実行済み + run-log.md
├─ my-submitted-notebook/      # 提出凍結（編集禁止）
├─ others-notebook/            # 他者原版（編集禁止）
│  ├─ eda/                     # EDA 専用原文
│  ├─ eda-ja/                  # EDA 日本語注釈版
│  ├─ public-useful/           # 有用公開NB混合
│  └─ train-scout/             # 学習スカウト
├─ exp/                        # 実験 SSOT + 分析（→ exp/README.md）
├─ sim-track/                  # simulation のみ — LB · 公開 NB メタ
└─ docs-ja/
   ├─ folder-map.md             # 本ファイル
   ├─ comp-start-checklist.md  # 開始日チェックリスト
   └─ comp-profile.md          # comp-type · Skill マップ
```

---

## ダウンロード先（種類別）

| 取得するもの | 置き場 | いつ · 誰が | Skill |
|---|---|---|---|
| 公式 Starter Kit | `dataset/derived/` | **ユーザー明示 OK** のみ | `dataset-summary` · `kaggle-cli-fetch` |
| 自チーム提出 tar / output | `my-submitted-notebook/{ref}-{name}/output/` | validator **PASS** 後 | `kaggle-submission-validator` |
| replay JSON | `exp/replay/{用途}/` | ユーザー指示 · intel 用 | `kaggle-cli-fetch` |
| episode ログ | `exp/replay/.../logs/` | デバッグ時 | `agent-debug.md` |
| Discussion 原文 | `docs-en/discussion/` | CLI fetch | `kaggle-cli-fetch` |
| LB · 公開 NB スコア | `sim-track/`（**メタのみ**） | 貼り付け or 軽量 CLI | `kaggle-simulation-tracker` |
| 他者 kernel（tabular · **コンペ中**） | `others-notebook/workspaces/` · `public-useful-*` | ユーザー OK 後 | `kaggle-kernel-repro` |
| 他者 kernel（**終了後** · 上位公開） | `retro/archive/others-notebook/post-comp-top-YYYYMMDD/rankNN-…/` | post-comp 振り返り | `post-comp-retro-setup` · `solution-code-summary` |

**禁止（指示なし）:** `competitions download` の乱用 · replay 大量 DL · `dataset/` を Git に載せる。

---

## comp-type: tabular

### 成果物単位

| comp-type | 1 成果物 = | WIP 例 |
|---|---|---|
| **simulation** | `main.py` ディレクトリ | `my-notebook/my-bot-v1/` |
| **tabular / notebook-output** | `.ipynb` 1 本 | `my-notebook/train-v3.ipynb` |
| **csv / lora** | zip / csv | `my-notebook/submission.zip` |

### ライフサイクル（共通）

```
wip →（実行）→ ran →（validator PASS）→ submitted
提出元から fork → local-eval（my-local-eval-notebook/ のみ）
```

**状態が変わったら:** 物理移動 + **`lifecycle-manifest.md` 1 行更新**（同ターン必須）。

---

## simulation 向け補足

| データ | 置く場所 | 置かない場所 |
|---|---|---|
| bot ソース | `my-*-notebook/` | `sim-track/` · `dataset/` |
| LB 順位 · μ | `sim-track/leaderboard-log.md` | `dataset/` |
| 公開 NB 一覧 | `sim-track/public-notebook-catalog.md` | `exp/` root |
| 対戦 JSON | `exp/replay/` | `sim-track/` |
| 他者 bot コード一括 | —（replay 中心） | `others-notebook/workspaces/` |

Skill: `kaggle-simulation-tracker` · **`kaggle-kernel-repro` は使わない**。

---

## tabular / notebook-output 向け補足

| データ | 置く場所 |
|---|---|
| 学習 csv | `dataset/derived/`（ユーザー DL） |
| eval fork ipynb | `my-local-eval-notebook/` |
| 他者 kernel 再現（コンペ中） | `others-notebook/workspaces/` → 要約 `docs-ja/others-notebook/` |
| 上位解法コード（終了後） | `retro/archive/others-notebook/post-comp-top-*/` · 学習リポは `retro/archive/solutions/code/` |

Skill: `local-eval-from-submit-notebook` · `kaggle-kernel-repro`

---

## exp/ 4 層（分析 MD）

| 層 | パス | 用途 |
|---|---|---|
| root SSOT | `exp/exp-index.md` 等 7 ファイル | 意思決定 · Best |
| protocol | `exp/protocol/` | ローカル検証手順 |
| latest | `exp/latest/` + `manifest.md` | **索引B** — 確定分析 |
| work | `exp/work/YYYY-MM-DD/` | 日次 WIP |
| archive | `exp/archive/history|superseded/` | 旧版 · reject |
| replay データ | `exp/replay/` | JSON のみ（MD は載せない） |

Skill: `experiment-management` · `experiment-result-management`

---

## Agent 読み順（毎セッション）

1. `AGENTS.md` · `docs-ja/comp-profile.md`
2. **`lifecycle-manifest.md`**（触る成果物があるとき）
3. `exp/exp-index.md` → **`exp/latest/manifest.md`**
4. タスク別 Skill（Router: `kaggle-comp-router`）

---

## 更新

comp-type 変更 · 新フォルダ追加時は本ファイルと `ARTIFACT-LIFECYCLE.md` を同期。  
テンプレ: `scripts/templates/folder-map.md.template`
