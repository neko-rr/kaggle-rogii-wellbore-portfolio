---
name: discussion-summary
description: KaggleコンペのDiscussionの要約。入力はユーザー貼り付け、docs-en/discussion/ の原文、または Skill kaggle-cli-fetch で取得した CLI 出力。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | docs-en/discussion/ | docs-ja/discussion/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

入力のDiscussionを日本語で要約して下さい。
その上で何がスコア向上にとって重要か、また、効果的ではなかった取り組みについてもまとめて下さい。

## 入力の優先順位

1. ユーザーがチャットに貼り付けた本文
2. `docs-en/discussion/` に保存済みの原文（Skill `kaggle-cli-fetch` で取得した CLI 出力を含む）
3. 未保存の場合 → 先に Skill `kaggle-cli-fetch` で取得を提案する

CLI 取得分は画像・Notebook カードが欠けることがある。Notes にその旨があれば要約に「要手動確認」と明記する。

# 出力時注意点

- UTCの時間表記で、yyyy/mm/dd形式で統一してください
  - 投稿日時を意識して、要約してください。最新情報で判断するために必要です。
  - 最新コメント日時は必須（重要なコメントは、コメント日時を明記）
- 誰が書いた意見かと内容を重視してください
  - Competition HostやKaggle rank上位者の意見は、有効な可能性があります
  - コメント者名とコンペ順位を記載してください
- 過去に作成された同じdiscussionが無いかを確認してください。もし、存在する場合は、新規情報があれば、追記してください
- **締切・提出上限・Private LB 枠・評価継続期間** に触れる内容があれば、要約後に Skill **`kaggle-comp-timeline`** で `docs-ja/comp-timeline.md` を更新する（changelog + 残り日数再計算 **UTC**）
- 提出上限の数字は **Discussion より Overview/Rules を優先**。他コンペの「1日5回」等で埋めない（`kaggle-competition-constraints`）
- メダル・順位帯を論じるときは **チーム数 N** を明示（Progression バンド）
- **LB 信頼性 · shake · Public 比率 · Final 本数 · CV vs LB** に触れたら要約後に Skill **`kaggle-lanes-final-strategy`** で `docs-ja/comp-strategy.md` の  
  `public_scope` / `shake_risk` / `improvement_compass` / Final スロットを更新する（道しるべ）
- **Competition Host / CPMP / Kaggle Staff が外部データ・モデル・ツールの使用を明示許可・推奨** した場合、要約後に Skill **`kaggle-license-compliance` Tier R** で `docs-ja/license-ledger.md` の「主催者明示許可」表と BOM を更新する

## 出力ファイル形式

### 命名規則（必須）

| 対象 | 形式 | 例 |
|---|---|---|
| **一般トピック（既定）** | `{topicId}-{短い題名}.md` | `693088-onnx-runtime-compatibility.md` |
| **Competition Host がトピック主** | `Competition-Host_{topicId}-{短い題名}.md` | `Competition-Host_724226-two-submissions.md` |
| **Kaggle Staff がトピック主** | `Kaggle-Staff_{topicId}-{短い題名}.md` | `Kaggle-Staff_691446-how-to-get-started.md` |
| **エラー主題** | 上記と同じファイル名で `discussion/error/` 配下 | `docs-ja/discussion/error/693088-....md` |

ルール:

1. **`topicId` は日本語要約（`docs-ja`）にも必ず入れる**（原文 `docs-en` と突合できるようにする）
2. **一般参加者の投稿者名はファイル名に入れない**（`Ali_...` / `Ryuhki-Kimura_...` のような命名は禁止）
3. 投稿者名プレフィックスは **Competition Host / Kaggle Staff のみ**（例外）。本文中の「誰が書いたか」は要約本文に書く
4. 短い題名は kebab-case（英数字・ハイフン）。日本語題名でも可だが空白はハイフン化
5. topicId 不明（貼り付けのみ等）のときは先に ID を確認。取れない場合のみ仮名 `unknown-{短い題名}.md` とし、本文先頭に `Topic ID: 不明` と書く

### 保存先

- 日本語要約: `yyyymmdd-コンペ名/docs-ja/discussion/`（本 Skill の主出力）
- 原文が未保存なら Skill `kaggle-cli-fetch` で `docs-en/discussion/` へ。en も **同じ `{topicId}-...` 規則**に合わせる
- 同一 topicId の既存ファイルがあれば **新規作成せず追記**する

---

## サブエージェント連携（SA-3）

1. 親が **`kaggle-subagent-delegate`** → Task `explore` で `docs-en/discussion/` を当たり、新規有無のみ確認
2. 未保存なら `kaggle-cli-fetch` を提案（ユーザー OK 後）
3. **本 Skill** で日本語要約 · timeline / license 連携
