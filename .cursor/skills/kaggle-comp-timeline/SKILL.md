---
name: kaggle-comp-timeline
description: >-
  Kaggle コンペの締切・フェーズ・提出制限・Private LB 枠を 1 ファイルに集約し、
  残り日数を更新する。コンペ概要作成時に最初に作り、Discussion 等の新情報で更新する。
  タイムライン、締切、Entry、Merger、提出上限、評価継続期間、Private LB 枠と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | —（任意 kaggle-cli-fetch） | — | docs-ja/comp-timeline.md | docs-ja/comp-timeline.md |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Comp Timeline

**全コンペ共通。** 締切とフェーズの **唯一の正（SSOT）** は `docs-ja/comp-timeline.md`。

`AGENTS.md`・`exp/exp-index.md` に締切を **重複記載しない** — リンクと現フェーズ 1 行のみ。

---

## 出力ファイル

```
{comp-inner}/docs-ja/comp-timeline.md    # ★ タイムライン本体（日本語）
{comp-inner}/docs-en/comp-timeline.md    # 原文メモ（任意・英語のまま可）
```

bootstrap 時にテンプレから `docs-ja/comp-timeline.md` を自動生成する。

---

## いつ使うか

| タイミング | 動作 |
|---|---|
| **コンペ概要作成時（最初）** | `competition-conditions` / `create-agent-file` と **同時に** 初版を作成 |
| Discussion 要約後 | 締切・ルール変更があれば更新 |
| ホスト告知・Rules 改定 | 即更新 + changelog 追記 |
| 作業開始時（週次でも可） | **残り日数** を再計算して更新 |
| ユーザー「締切は？」 | 本ファイルを読んで回答 |

---

## 初回作成ワークフロー

### 入力

1. Kaggle コンペ Overview / Rules / Evaluation タブ
2. ユーザー貼り付け
3. `kaggle-cli-fetch` で取得した Competition Host トピック（任意）

### Step 1: マイルストーンを抽出

最低限そろえる項目（該当なしは `—`）:

| id | イベント | 典型例 |
|---|---|---|
| `start` | コンペ開始 | Overview の Start |
| `entry` | Entry / ルール同意締切 | Join Competition 期限 |
| `merger` | Team Merger 締切 | |
| `final-submit` | 最終提出締切 | |
| `post-eval-end` | 提出後の評価終了 | シミュレーションで対戦継続 |
| `private-select` | Private LB 枠選択締切 | 2 枠まで等 |
| `writeup` | Write-up / 公開 kernel 締切 | 賞金対象コンペ |

**時刻:** 明記がなければ **その日 23:59 UTC**（公式: *All deadlines are at 11:59 PM UTC … unless otherwise noted*）。  
notes に「公式デフォルト UTC」と書く。**チャット・要約も UTC**。JST はユーザー依頼時のみ併記。  
詳細: `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md` §4

### Step 2: 提出ルールを抽出

**他コンペの数字を転記しない。** Overview / Rules に無い項目は `要確認`。

| カテゴリ | 記録例（≠既定） |
|---|---|
| 提出形式 | CSV / zip / main.py / LoRA adapter |
| 1日あたり上限 | **当該 Overview の値**（5 とは限らない） |
| 有効提出数 / LB 反映 | Final **2** 選択 · または sim **最新 2 件のみ**（混同禁止） |
| チーム提出上限 | コンペによる |
| Private LB / Final 枠 | 枠数はコンペ固有 |
| 賞金・メダル | medals 対象か · write-up 要件 |
| メダル計算用 N | 参考チーム数（LB）— Skill `kaggle-competition-constraints` |

### Step 2b: メダル帯（参考節）

`## メダル帯（参考）` を timeline に置き、**N と計算式**を書く（断定は N 更新時に再計算）:

```markdown
## メダル帯（参考）
- 出典: https://www.kaggle.com/progression/competitions
- medals 対象: はい / いいえ / 要確認
- チーム数 N（時点）: …
- バンド: 0–99 / 100–249 / 250–999 / 1000+
- Gold / Silver / Bronze の rank 上限: （floor 計算を併記）
```

### Step 3: `docs-ja/comp-timeline.md` を書く

テンプレ: `kaggle-template/comp/docs-ja/comp-timeline.md.template`

### Step 4: 他ファイルへリンク（重複禁止）

- `AGENTS.md` — コンペ期間は **1 行 + リンク** のみ
- `docs-ja/conditions.md` — 期間セクションは「詳細は comp-timeline 参照」
- `docs-ja/comp-strategy.md` — 初版（Goal / Stop の骨格。Bets は intel 後に更新可）
- `exp/exp-index.md` — 「まず読む」に `comp-strategy` と `comp-timeline` を追加

---

## 更新ワークフロー（Discussion 等）

### トリガー

- Skill `discussion-summary` 完了後
- Host / Staff トピックに timeline 関連情報
- Rules タブの変更
- ユーザー「締切が延びた」等の報告

### 手順

1. 現行 `docs-ja/comp-timeline.md` を読む
2. 新情報と **差分** を特定（推測で書かない）
3. マイルストーン表・提出ルールを更新
4. **更新履歴（changelog）** に append:

   | updated_utc | source | 変更内容 |

5. **残り日数** を全未終了マイルストーンで再計算
6. `exp/exp-intel.md` に戦略影響がある場合のみ 1〜3 行追記（締切の生データは comp-timeline に置く）

### 日次更新（提出・実行戦略）

作業開始時または 1 run 完了後:

0. **`docs-ja/comp-strategy.md`** を読み、今日の行動が Bets / Stop と矛盾しないか確認
1. `## 提出・実行戦略（今日）` の **更新日 UTC**・本日提出済み・GPU 予算を更新
2. `次の run 候補` の `verdict` を見直す（`go` のみ実行、`defer` は締切・枠を理由に notes）
3. 実行した run の時間・コスト・metric は **`exp/run-ledger.md`** に追記（本 Skill は意思決定のみ）
4. pretrain-gate で `reject` した候補は `verdict: reject` にし、run-ledger へは見積のみ残す可

### Discussion 連携

`discussion-summary` が以下を検出したら **必ず** 本 Skill で comp-timeline を更新する:

- 締切延長・短縮
- 提出上限・評価方式の変更
- Private LB / 枠選択の告知
- 提出後評価期間の変更

---

## 残り日数の計算

- 基準: **作業時点の UTC 日付**
- 表示: `残り N 日`（当日締切 = `残り 0 日（本日締切）`、過ぎた = `終了`）
- 時刻付き締切は UTC で比較し、同日 23:59 UTC までをその日の締切とする
- `## 現在のフェーズ` を毎回更新:

```markdown
## 現在のフェーズ

**フェーズ:** 最終提出前 / 提出後評価中 / 終了 等  
**次の締切:** {イベント名} — yyyy/mm/dd UTC（残り N 日）  
**注意:** {提出上限・枠選択など直近で効くルール 1 行}
```

---

## コンペ型別の記入例

### シミュレーション（Orbit Wars 型）

```markdown
| final-submit | 2026/06/23 23:59 UTC | 未達 | 残り 6 日 | 追加提出ロック |
| post-eval-end | 2026/07/08 頃 UTC | 未達 | — | 対戦継続・LB 収束まで |

### 提出ルール
- 1 日最大 5 agents
- LB に効くのは **最新 2 提出のみ**
- 各 bot はコンペ終了まで対戦継続
```

### LoRA / 特殊提出（Nemotron 型）

```markdown
| final-submit | 2026/06/15 23:59 UTC | 終了 | — | submission.zip |
| private-select | （コンペ終了後） | — | — | **2 枠まで**選択可 |

### 提出ルール
- LoRA rank ≤ 32
- Private LB 枠: 最大 2 件を最終順位に使用
```

### タブラー（典型）

```markdown
| merger | yyyy/mm/dd UTC | ... |
| final-submit | yyyy/mm/dd UTC | ... |
```

---

## Agent 規則

1. **SSOT は comp-timeline のみ** — AGENTS / exp-index に締切一覧や「1日5回」をコピーしない
2. **確定情報のみ** — Discussion の噂は notes に「未確認」、Host 確認後に昇格
3. 更新のたび **changelog append** + **残り日数再計算（UTC）**
4. コンペ概要初回作成時は **conditions と同時に** comp-timeline を必ず作成
5. partial progress 禁止 — 更新後は index / AGENTS のリンク整合を確認
6. **日次** — `提出・実行戦略` を更新し、run 詳細は `run-ledger` へ分離する
7. **提出上限・有効枠を口頭で言う前**に本ファイルを読む。無記入なら Overview を読んで埋める（Skill `kaggle-competition-constraints`）
8. **メダル帯**は N 依存。N なしに「メダル圏」と断定しない
9. 締切の表示は **UTC**。日本時間だけの回答にしない

---

## ユーザー依頼別

| 依頼 | 動作 |
|---|---|
| 「コンペ概要を作って」 | conditions + **comp-timeline 初版** + AGENTS |
| 「締切を更新して」 | comp-timeline 更新 + changelog |
| 「あと何日？」 | 現フェーズ + 次締切の残り日数 |
| 「提出ルールは？」 | 提出ルール節を回答（数値は本ファイルのみ） |
| 「メダル圏？」「金銀銅」 | `kaggle-competition-constraints` で N から再計算 |
| 「今日何回出せる？」 | 1 日上限を本ファイルから。無ければ Overview 確認後に記入 |
| 「今日何をすべき？」 | **comp-strategy** + 提出・実行戦略節 + run-ledger を読んで提案 |
| 「方針を立てたい」 | Cursor Plan → 結果を **`comp-strategy.md`** に固定 |
| 「Discussion 要約して」 | discussion-summary 後、timeline 関連なら更新 |

---

## 他 Skill との分担

| Skill | 役割 |
|---|---|
| **本 Skill** | 締切・フェーズ・提出制限・**提出・実行戦略（今日）** の SSOT |
| `experiment-management` | `exp/run-ledger.md`（時間・コスト・metric の詳細） |
| `competition-conditions` | 概要・評価指標（期間・制約は timeline へ） |
| `kaggle-competition-constraints` | メダル再計算 · 制約誤認ガード · UTC |
| **`docs-ja/comp-strategy.md`** | **Goal / Bets / Stop（週次・Plan 結果の SSOT）** |
| `create-agent-file` | AGENTS.md（timeline へリンク） |
| `discussion-summary` | Discussion 要約 → timeline 更新トリガー |
| `kaggle-comp-bootstrap` | テンプレ生成 |
| `kaggle-simulation-tracker` | LB / 公開 NB 推移（締切とは別） |

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\docs-ja\comp-timeline.md.template`
