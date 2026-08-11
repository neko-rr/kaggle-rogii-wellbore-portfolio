---
name: post-comp-retro-setup
description: >-
  終了済み Kaggle コンペで retro/ フォルダを新設し、コンペ中の exp/ と終了後の振り返りを分離する。
  コンペ終了、Private LB 公開、post-comp、振り返りフォルダ作成、RETRO 初期化と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | exp/ | retro/ 初期 tree |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Post-Comp Retro Setup

コンペ終了後に **`retro/`** を新設し、コンペ中の **`exp/`**（次の提出改善）と終了後の振り返り（確定事実）を分離する。

## 使う場面

- コンペ締切後、Private LB 公開前後
- ユーザーが「振り返りフォルダを作って」「retro を初期化して」「コンペ終了後の整理」と依頼したとき
- `exp-summary.md` が肥大化し、コンペ中ログと終了後分析が混ざっているとき

## 既存 Skill との分担

| Skill | 担当 | 主な出力先 |
|---|---|---|
| **本 Skill** | `retro/` の新設・索引・フェーズ移行 | `retro/retro-index.md` |
| `post-comp-private-retrospective` | **自チーム** Private 振り返り | `retro/retro-private.md` |
| `leaderboard-analysis` | **コンペ全体** LB 分析 | `retro/retro-leaderboard.md` |
| `solution-analysis` | **上位チーム** 解法分析 | `retro/retro-solutions.md` |

`exp-intel.md` はコンペ中のスナップショットとして残す。終了後に上書きしない。

## 前提確認（作業前）

1. コンペフォルダパス（`yyyymmdd-コンペ名/`）を特定する
2. `exp/exp-index.md` が存在するか確認する
3. `retro/` が既にある場合は **新規作成ではなく更新** とする

## セットアップ手順

### Step 1: `retro/` を作成

コンペフォルダ直下に次を作る。テンプレートは `%USERPROFILE%\.cursor\kaggle-template\comp\retro\` を参照。

```text
yyyymmdd-コンペ名/
└─ retro/
   ├─ retro-index.md        # 終了後分析の索引（50行以内を目標）
   ├─ retro-private.md      # 自チーム Private / 枠選択 / shake-up
   ├─ retro-leaderboard.md  # コンペ全体 LB 要約
   ├─ retro-solutions.md    # 上位解法の統合分析
   ├─ retro-lessons.md      # 次コンペへ持つ一般則
   └─ archive/              # 他者 NB + 解法セット（Skill: kaggle-notebook-folders）
```

テンプレート変数: `{{COMP_NAME}}`, `{{PARTICIPANT}}`, `{{COMP_URL}}`, `{{COMP_DEADLINE}}`

### Step 2: `retro-index.md` を埋める

最低限記録する項目:

| 項目 | 内容 |
|---|---|
| コンペ終了日 | 締切 UTC |
| Private LB 公開日 | 分かる範囲 |
| 自チーム Best Public | `exp/exp-infer.md` から転記 |
| 自チーム Best Private | 未確定なら「未公開」 |
| 参照する exp ファイル | `exp-index`, `exp-infer`, `exp-train` 等 |
| 次に読む retro ファイル | ユーザーの依頼に応じて1つ指定 |

### Step 3: `exp/` のフェーズ移行

| ルール | 内容 |
|---|---|
| **フリーズ** | `exp-train.md`, `exp-intel.md` は原則追記しない |
| **例外** | Private 確定値のみ `exp-infer.md` に事実として追記可 |
| **新規分析** | 終了後の考察は `retro/` に書く |
| **索引** | `exp-index.md` 末尾に「コンペ終了 → 振り返りは `retro/`」リンクを1行追加 |

### Step 4: 関連ドキュメントを更新

- ルート `AGENTS.md` のプロジェクト構成に `retro/` を追記
- `cursor.md` に終了日・振り返り開始日を1行追記（存在する場合）

### Step 5: 次コンペ用の知見候補を収穫

1. failures · 自チーム · 上位解法から、`retro-lessons.md` に **A/B/C + apply/avoid/origin/domain** で最低3件  
2. Skill `kaggle-knowledge-harvest`（validate · audit）  
3. **Private knowledge-store へ push**（`cd knowledge; git pull; commit; push`）  
   → 詳細 `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action harvest -CompRoot "./<competition>"
./scripts/run-kaggle-knowledge.ps1 -Action validate
./scripts/run-kaggle-knowledge.ps1 -Action audit
cd knowledge
git pull origin main
git add -A
git commit -m "harvest: <competition>"
git push origin main
```

候補は自動 promote しない。昇格は `kaggle-knowledge-promote` + ユーザー承認。

## `exp/` と `retro/` の違い

| 観点 | `exp/`（コンペ中） | `retro/`（終了後） |
|---|---|---|
| 目的 | 次の提出を改善 | 学習・振り返り |
| 更新頻度 | 頻繁 | 終了後に数回で完了 |
| 内容 | 仮説・未確定が多い | 確定事実が多い |
| Agent の読み方 | 「次に何をする？」 | 「何を学んだ？」 |

## フェーズ別の読み方

| ユーザー依頼 | 読む順 |
|---|---|
| Private スコアを報告 | `retro-index` → `retro-private` → `exp-infer`（参照） |
| LB 全体を分析 | `retro-index` → `retro-leaderboard` + Skill `leaderboard-analysis` |
| 上位解法を分析 | `retro-index` → `retro-solutions` + Skill `solution-analysis` |
| 次コンペの準備 | `retro-lessons` のみでも可 |

## 品質チェック

- [ ] `retro/` が kebab-case で作成されている
- [ ] `exp-intel.md` を終了後分析で上書きしていない
- [ ] `retro-index.md` が50行以内で、次に読むファイルが明記されている
- [ ] 各 retro ファイルの役割が重複していない
- [ ] `retro-lessons.md` の汎用教訓が最低3件あり、根拠参照がある
- [ ] 汎用が **A（CV）/ B（解法）/ C（運用）** に分かれており、1 項目に混在していない
- [ ] knowledge harvest / validate / **audit** PASS  
- [ ] **`knowledge/` を Private store へ push 済み**（他コンペが古い候補を見ない）  
- [ ] 候補は未承認のまま Rule 化されていない

## 追加リソース

- テンプレート: `%USERPROFILE%\.cursor\kaggle-template\comp\retro\`
- 自チーム振り返り: Skill `post-comp-private-retrospective`
