---
name: competition-conditions
description: >-
  Kaggleコンペの概要・評価指標・提出制約の要約。締切UTC・1日提出上限・
  有効LB件数・メダル（チーム数依存）を Overview から抜き出し conditions /
  comp-timeline に固定する。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | Kaggle Overview（ユーザー貼付/Web） | docs-ja/conditions.md · comp-timeline.md |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。
入力はKaggleのコンペ概要ページです。
以下のフォーマットに従って、日本語で要約して下さい。

**横断ノーマ（数字をでっち上げない）:**  
`_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md` · Skill `kaggle-competition-constraints` · Rule `kaggle-comp-constraints`

# 出力フォーマット

- コンペ背景：
- コンペ概要：
- 評価指標：
- コンペ期間：**UTC**（時刻未記載は 23:59 UTC。JST のみで書かない）→ 詳細リンク `comp-timeline.md`
- 賞金：
- **提出・LB 制約（Overview の数値のみ · 他コンペ流用禁止）:**
  - 1 日あたり提出上限:
  - 有効提出 / LB に効く件数:（Final **N** 選択 / sim **最新 K** · **N を勝手に2としない**）
  - Private / Final 枠:
  - 提出形式:
- **レーン仮置き:** primary / public の物差しを1行ずつ（詳細は strategy）
- **public_scope / shake の手がかり:** Host 文があれば（無ければ unknown）
- 制限事項：
- メダル: 付与されるか · 現時点チーム数 N が分かるなら帯の目安（算出は `kaggle-competition-constraints`）
- コンペのURL

**ライセンス・外部データ（Rules 抜粋）** — 別節として `docs-ja/license-ledger.md` に SSOT 化する:

- Competition Data ライセンス（例: CC BY 4.0）
- Winner License（賞金時に付与する OSS ライセンス）
- External Data / Models（Reasonableness・同等アクセス）
- AMLT / ツールの要件

`conditions.md` の制限事項に 1〜2 行要約 + `license-ledger.md` へのリンクを書く。

**コンペ期間・提出上限・有効枠の詳細は `docs-ja/comp-timeline.md` に記載する。**  
Skill `kaggle-comp-timeline` を `conditions.md` と同時に作成・更新する。  
`conditions.md` は提出制約を **箇条書きで短く** · 重複表は timeline 側。  
未確認の提出回数を「たぶん5」と書かない — `要確認` と source を残す。

## 出力ファイル形式

```
yyyymmdd-コンペ名/  # 締切日 yyyymmdd + コンペ名（kebab-case）
├─ lifecycle-manifest.md   # 成果物状態索引（comp-root）
├─ dataset/            # 公式データ（開始時に空で作成・手動 DL）
│  ├─ README.md
│  └─ derived/
├─ my-notebook/
├─ my-local-eval-notebook/
├─ my-ran-notebook/
├─ exp/                         # 実験 SSOT（Skill experiment-management）
│  ├─ README.md
│  ├─ exp-index.md              # root: 必須 7 ファイルのみ
│  ├─ protocol/                 # ローカル検証 SSOT
│  ├─ latest/manifest.md        # 最新分析索引
│  ├─ work/YYYY-MM-DD/          # 日次 WIP
│  ├─ archive/history|superseded/
│  ├─ replay/                   # episode JSON
│  └─ local-eval/
├─ docs-ja/
│  ├─ folder-map.md             # ★ 置き場所 SSOT（Agent 最初の1枚）
│  ├─ comp-start-checklist.md # Day 0（init-comp-layout.ps1）
│  ├─ others-notebook/
│  ├─ discussion/
│  ├─ comp-profile.md
│  ├─ conditions.md
│  ├─ comp-strategy.md          # Goal / Bets / Stop（comp-level 戦略）
│  ├─ comp-timeline.md
│  ├─ pretrain-acceptance.md
│  ├─ kernels-runbook.md
│  ├─ submission-rules.md
│  ├─ license-ledger.md          # ライセンス BOM + 主催者明示許可
│  └─ license-audits/
└─ docs-en/

**開始時:** `new-kaggle-comp.ps1` → **`scripts/init-comp-layout.ps1`**（Skill `kaggle-comp-bootstrap`）。  
simulation なら `-CompType simulation` で `sim-track/` 同時生成。
   ├─ others-notebook/
   ├─ discussion/
   ├─ conditions.md
   └─ comp-timeline.md    # 原文メモ（任意）

```

## 作成順序

0. Skill `kaggle-comp-router` — `comp-type` 判定 → `docs-ja/comp-profile.md`
1. `docs-ja/conditions.md`（本 Skill）
2. `docs-ja/comp-timeline.md`（Skill `kaggle-comp-timeline`）
3. `docs-ja/comp-strategy.md`（初版 — Goal / Stop 骨格。Plan 結果の SSOT）
4. `docs-ja/pretrain-acceptance.md`, `kernels-runbook.md`, `submission-rules.md`（3段ゲート初版）
5. `docs-ja/license-ledger.md`（Skill `kaggle-license-compliance` — Rules 抜粋 + BOM 初版）
6. `AGENTS.md`（`pretrain-profile` / `submission-profile` を記入）

# 入力

チャットに記述する等
