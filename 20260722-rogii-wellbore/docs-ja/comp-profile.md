# コンペプロファイル — rogii-wellbore

> skill: kaggle-comp-router  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-07-25 UTC

コンペ型と Skill ルーティングの **SSOT**。Agent は作業開始時に `AGENTS.md` と本ファイルを読む。

---

## コンペ型

| 項目 | 値 |
|---|---|
| **comp-type** | **tabular** |
| **副タグ** | code-competition, kaggle-9h-limit, no-internet-on-submit, well-group-cv, multimodal-logs |
| **提出形式** | Notebook 出力 → **`submission.csv`**（`id,tvt`） |
| **Public / Private** | Public ≈ テストの **26%** · 最終は残り **74%**（Private）。公式文は [`conditions.md`](conditions.md) |
| **comp-phase** | **active** |

### 判定メモ

- Overview: 行単位の連続値 **TVT** を **RMSE** で採点 → **tabular 回帰**
- Featured **Code Competition**（Notebook 必須・Internet OFF・≤9h）→ 副タグ `code-competition`
- Multimodal / Geology タグあり（軌道 CSV + GR + Typewell + png）だが提出は csv。simulation / LoRA ではない
- Leaderboard: Public 26% / Private 74% → 最終順位は shake-up しうる（[`cv-lb-private-relation.md`](cv-lb-private-relation.md)）

---

## Profile（3段ゲート）

| 項目 | 値 |
|---|---|
| pretrain-profile | **tabular** |
| submission-profile | **csv**（成果物）※提出経路は Notebook 紐づけ必須 |

---

## Skill マトリクス（このコンペ）

### 全コンペ共通

| フェーズ | Skill |
|---|---|
| 開始・構成 | `kaggle-comp-bootstrap` |
| 型判定 | `kaggle-comp-router` |
| 締切 | `kaggle-comp-timeline` |
| 実験ループ | `kaggle-experiment-checklist` |
| 学習前 | `kaggle-pretrain-gate` |
| 外部依存追加 | **`kaggle-license-compliance`（Tier R）** |
| 実行 | `kaggle-kernels-runbook` |
| 提出前 | `kaggle-submission-validator` |
| 記録 | `experiment-management`, `experiment-result-management` |
| Discussion | `kaggle-cli-fetch`, `discussion-summary` |

### 型固有（tabular）

| 主 Skill | 補助 |
|---|---|
| `local-eval-improvement-orchestrator`, `local-eval-log-strategy` | `metric-repro.md`（well 単位 holdout / LB 差）+ `dataset-summary` |

---

## タスク別ルーティング

| 依頼 | まず使う Skill |
|---|---|
| コンペ概要作成 | `competition-conditions` + `kaggle-comp-timeline` |
| 次に何を試す？ | `kaggle-experiment-checklist` Phase 1 |
| 学習していい？ | `kaggle-pretrain-gate` + `metric-repro.md` |
| 外部モデル/他者 NB | **`kaggle-license-compliance` Tier R** |
| ローカル CV / Metric | `metric-repro.md` → `local-eval-*` |
| Kaggle / Colab 実行 | `kaggle-kernels-runbook` |
| 提出していい？ | `kaggle-submission-validator`（列 `id,tvt`） |
| 今日何をすべき？ | `kaggle-comp-timeline` + **`comp-strategy.md`** |

---

## 実行環境方針

| 用途 | 場所 |
|---|---|
| EDA・短い CV | ローカル or Kaggle CPU |
| 長時間学習 | Kaggle GPU（≤9h）または Colab — **ユーザーが選択** |
| 提出 | Kaggle Notebook（Internet OFF）→ `submission.csv` |

---

## 使わない Skill（このコンペ）

- `kaggle-simulation-tracker`（休眠）
- `agent-debug.md`（**inactive** — simulation 専用）
- `kaggle-submission-strength-gate`（simulation 専用）
- LoRA 提出プロファイル関連

---

## 関連 SSOT

| ファイル | 内容 |
|---|---|
| `conditions.md` | 概要・評価指標 |
| `comp-strategy.md` | Goal / Bets / Stop |
| `metric-repro.md` | RMSE 再現・well holdout |
| `comp-timeline.md` | 締切・今日の戦略 |
| `pretrain-acceptance.md` | 学習前基準 |
| `kernels-runbook.md` | 実行手順 |
| `submission-rules.md` | 提出検証 L2 |
| `license-ledger.md` | ライセンス BOM |
