---
name: create-agent-file
description: AGENTS.mdの作成・編集
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | AGENTS.md テンプレ | AGENTS.md |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。

# 出力ファイル形式
- 「ルート」フォルダに、マークダウン形式で、「AGENTS.md」ファイルを作成・現在の内容で更新する

# 最低限必要な出力フォーマット
- コンペのURL
- コンペ名
- コンペ概要
- 評価指標
- コンペ期間（**1行要約 + `docs-ja/comp-timeline.md` へのリンク**。締切一覧は AGENTS に書かない。**時刻は UTC**）
- 提出制約は AGENTS に長く書かない → `comp-timeline`（1 日上限・有効枠は **当該 Overview** · Skill `kaggle-competition-constraints`）
- pretrain-profile / submission-profile（tabular|lora|simulation|ensemble / lora|csv|simulation 等）
- 制限事項

- 現在のベスト記録（パブリックLB）
- メダル: 必要なら `comp-timeline` のメダル帯（N 依存）へリンク。順位帯を % だけで短絡しない
- 重要：評価機能の修正
- 実験を評価する方法（CV ≠ LB）
```md
#  開発ワークフロー
##  トレーニング環境：Google Colab
- Cursorはトレーニングスクリプトをローカルで実行してはいけません
- お使いのマシン上で環境設定は不要です。
- トレーニングはColabのクラウドインフラストラクチャ上で実行されます。
## 推論環境：Kaggleノートブック
- 推論スクリプトは、Kaggleの提出環境で実行されるように設計されています。
- Kaggleの制約（実行時間9時間以内、インターネット接続不要）を遵守する必要があります。
# 実験結果管理
- 重要：実験後は `exp/exp-index.md` を更新し、内容は `exp-train.md` / `exp-infer.md` / `exp-intel.md` に分ける
- skills\experiment-result-management\SKILL.mdを使用
# 実験管理
- skills\experiment-management\SKILL.mdを使用
# yyyymmdd-コンペ名/  # 締切日 yyyymmdd + コンペ名（kebab-case）
├─ dataset/            # 公式データ置き場（開始時に空・**ユーザーが手動 DL**）
│  ├─ README.md        # 手順（Agent は勝手に DL しない）
│  └─ derived/         # 自前加工（Git 除外）
├─ my-submitted-notebook/  # 提出済み（編集禁止）
├─ my-notebook/            # WIP（Cursor が編集）
│  └─ planned/             # 作成済み・未実行・実行後回し
├─ my-local-eval-notebook/ # 検証専用（提出しない）
├─ my-ran-notebook/        # 実行済み・未提出
├─ others-notebook/
├─ exp/
│  ├─ exp-index.md
│  ├─ exp-train.md
│  ├─ exp-infer.md
│  ├─ exp-intel.md
│  └─ hyperparameter-table.md
├─ docs-ja/
│  ├─ others-notebook/
│  ├─ discussion/
│  ├─ dataset.md
│  ├─ conditions.md
│  ├─ comp-profile.md
│  ├─ comp-timeline.md
│  ├─ pretrain-acceptance.md
│  ├─ kernels-runbook.md
│  └─ submission-rules.md
└─ docs-en/
   ├─ others-notebook/
   ├─ discussion/
   └─ comp-timeline.md

# コンペ SSOT（概要作成時に初版）
- Skill `kaggle-comp-router` — `comp-profile.md` + `AGENTS.md` の `comp-type`
- Skill `kaggle-comp-timeline` — `comp-timeline.md`
- Skill `kaggle-pretrain-gate` — `pretrain-acceptance.md`
- Skill `kaggle-kernels-runbook` — `kernels-runbook.md`
- Skill `kaggle-submission-validator` — `submission-rules.md`

# 3段ゲート
① pretrain-gate → ② kernels-runbook → ③ submission-validator → my-submitted-notebook/
Kaggle 完走は提出前提にしない。

# コンペ終了後（retro/）
- Skill `post-comp-retro-setup` で `retro/` を新設
- 自チーム Private 振り返り: Skill `post-comp-private-retrospective` → `retro/retro-private.md`

# Git / GitHub
- ルート `.gitignore` — **dataset/ は載せない**
- Skill `kaggle-git-security` / `scripts/install-git-hooks.ps1`

# Notebook フォルダ
- Skill `kaggle-notebook-folders` — `planned/`=未実行 / `my-ran-notebook/`=実行済み

# シミュレーション系コンペ（Games / 日次 LB）のみ
- Skill `kaggle-simulation-tracker` — `sim-track/` に公開 NB 一覧推移 + public score 時系列
```
