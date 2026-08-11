---
name: post-comp-private-retrospective
description: >-
  終了済み Kaggle コンペで自チームの Private LB・提出枠選択・Public/Private shake-up を分析し、
  exp/ の実験記録と突合して教訓をまとめる。Private スコア共有、自チーム振り返り、提出枠の振り返り、
  Public Private 順位変動の解釈と言ったときに使う。出力先は retro/retro-private.md。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | exp/ · Private LB（ユーザー提供） | retro/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Post-Comp Private Retrospective

**自チーム（A）** の Private LB 振り返り専用。コンペ全体 LB は `leaderboard-analysis`、上位解法は `solution-analysis` に任せる。

## 使う場面

- ユーザーが Private LB・順位・提出枠の結果を報告したとき
- 「提出枠1・枠2の選択は正しかったか」「Public 0.86 → Private は？」を整理したいとき
- コンペ終了後に自チームの当たり・外れを `exp/` と突合したいとき

## 事前準備

1. `retro/` が無ければ Skill `post-comp-retro-setup` で作成する
2. 次を読む:
   - `retro/retro-index.md`
   - `exp/exp-index.md`
   - `exp/exp-infer.md`
   - `exp/hyperparameter-table.md`
   - 必要なら `exp/exp-train.md`（学習起因の外れ分析時）

**読まない / 上書きしない:** `exp/exp-intel.md`（コンペ中の他者仮説は参照のみ）

## 入力（ユーザーから取得）

### 必須

- Private LB スコアと順位（各提出枠）
- Public LB スコアと順位（比較用）
- 選択した提出枠（枠1・枠2）とその根拠

### 可能なら

- Kaggle の提出一覧スクリーンショット / CSV
- メダル圏との差（Gold / Silver / Bronze 閾値）
- ローカル CV との差分メモ

不足時は作業前に確認する。Private 未公開なら Public ベースの暫定メモにし、`retro-index.md` に「Private 未確定」と明記する。

## 分析手順

### Step 1: 事実の整理

`exp-infer.md` と `hyperparameter-table.md` から提出履歴を表にまとめる。

| 提出ID | 枠 | Public | Private | 順位変動 | Notebook / Adapter | 備考 |
|---|---|---|---|---|---|---|

### Step 1b: メダル判定（公式帯）

チーム数 **N** と最終 rank から Gold / Silver / Bronze / なしを判定する。  
表と計算法: `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md` · Skill `kaggle-competition-constraints`  
（% は floor · N≥250 の Gold は `10+floor(0.002×N)` · N を書かずに「メダル圏」と言わない）

### Step 2: 提出枠の評価

各枠について判定する:

- **選択は妥当だったか**（当時の情報で）
- **より良い選択肢があったか**（事後）
- **枠を使わなかった提出に価値はあったか**

### Step 3: shake-up 解釈

- Public → Private の順位・スコア変動
- 自チームの変動がコンペ全体の傾向と一致するか
- 過学習・CV 不一致・Public 依存の有無

### Step 4: exp との突合

| 観点 | 参照 | 問い |
|---|---|---|
| 推論・提出 | `exp-infer.md` | Best Public の仮説は Private で成立したか |
| 学習 | `exp-train.md` | 学習方針の当たり・外れ |
| 実験ログ | `hyperparameter-table.md` | 提出ごとの設定差は説明になるか |

**当たり / 外れ** は仮説ではなく、Private 確定後の事実として書く。

### Step 5: 教訓の抽出

`retro-lessons.md` に一般則を **3〜5 個** 追記する。コンペ固有と汎用を分ける。  
汎用はさらに **`### A. CV・物差し`** と **`### B. 解法`**（必要なら **`### C. 運用`**）に分け、**混ぜない**。

## 出力ファイル

| ファイル | 操作 |
|---|---|
| `retro/retro-private.md` | 主出力（新規 or 更新） |
| `retro/retro-index.md` | Best Private・順位・更新日を更新 |
| `retro/retro-lessons.md` | 教訓セクションを追記 |
| `exp/exp-infer.md` | Private 確定値のみ事実として追記可 |

## `retro-private.md` テンプレート

```markdown
# [コンペ名] 自チーム Private 振り返り

**分析日:** yyyy/mm/dd  
**参加者:** [名前]  
**コンペ:** [URL]  
**データソース:** Kaggle Private LB / ユーザー報告 / exp-infer / hyperparameter-table

---

## 要約

- [Private Best と順位を1〜3行]
- [提出枠選択の結論]
- [最重要の当たり・外れ]

---

## Private / Public 結果

| 項目 | Public | Private | コメント |
|---|---|---|---|
| Best スコア | | | |
| Best 順位 | | | |
| メダル | | | |

---

## 提出枠の振り返り

| 枠 | 選択提出 | Public | Private | 当時の根拠 | 事後評価 |
|---|---|---|---|---|---|
| 枠1 | | | | | |
| 枠2 | | | | | |

### 枠選択の結論

- [妥当だった点]
- [改善できた点]
- [使わなかった提出の評価]

---

## Public → Private shake-up

- **自チームの変動:** [順位・スコア]
- **解釈:** [Public 依存 / CV 一致 / 過学習 等]
- **コンペ全体との比較:** [分かる範囲]

---

## exp との突合

### 当たっていたこと

1. [施策] — 根拠: [exp-infer / exp-train の参照]

### 外れていたこと

1. [施策] — 根拠: [同上]

### 検証できなかったこと

- [Private 公開前の仮説で未確定のもの]

---

## 次コンペへの示唆（このコンペ固有）

1. [具体的な教訓]
2. [具体的な教訓]
3. [具体的な教訓]

---

## 未確認・追加で見るべきこと

- [上位解法との比較 → retro-solutions]
- [LB 全体 → retro-leaderboard]
```

## 品質チェック

- [ ] Public と Private を混同していない
- [ ] 提出枠の「当時の根拠」と「事後評価」を分けている
- [ ] `exp-intel.md` の仮説を確定事実のように書いていない
- [ ] 教訓が `retro-lessons.md` にも反映されている
- [ ] 数値の出典（Kaggle / ユーザー / exp）が分かる

## 関連 Skill

- フォルダ新設: `post-comp-retro-setup`
- コンペ全体 LB: `leaderboard-analysis` → `retro-leaderboard.md`
- 上位解法: `solution-analysis` → `retro-solutions.md`
