---
name: kaggle-competition-constraints
description: >-
  Kaggle コンペの提出上限・有効 LB 件数・Private/Final 枠・メダル帯（チーム数依存）・締切 UTC を
  確認・再計算する。1日提出回数・シミュレーションの最新N件・メダル範囲・日本時間 vs UTC
  で会話が噛み合わないとき、Overview 照合、comp-timeline 更新時に使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | 任意 Overview | — | Overview · Rules · docs-ja/comp-timeline.md | docs-ja/comp-timeline.md |

**共通禁止:** competitions submit · 他コンペの数値の流用 · 未確認の提出上限の断定

---

# Kaggle Competition Constraints

横断ノーマ（メダル表・UTC・禁止）:

**`_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md`**  
公式: [Competition Medals / Progression](https://www.kaggle.com/progression/competitions)

当該コンペの **実数の SSOT** は `docs-ja/comp-timeline.md`。

---

## いつ使うか

| トリガー | 動作 |
|---|---|
| 「今日何回出せる？」「まだ提出枠ある？」 | timeline の 1 日上限を読んで回答。無ければ Overview へ |
| 「メダル圏？」「金・銀・銅は？」 | **チーム数 N** を確認 → バンド表で cutoff を計算して回答 |
| 「Private 2 枠」「最新 2 つ」 | 提出形式（tabular Final vs sim 最新 N）を区別して説明 |
| 「締切は日本時間で？」 | **UTC を正**、JST は併記のみ |
| コンペ概要 / Day0 | conditions + timeline と同時に制約を初期記入 |
| 他コンペ経験の数字が出そうなとき | **本 Skill を先に開く** |

---

## Step 0 — 読み取り禁止事項

次を **記憶や他コンペから言わない**:

- 1 日あたり提出上限（5 / 10 / 20…）
- Final / Private 選択件数（必ずしも 2）
- simulation の「ランクに効く件数」（最新 1・2・K）
- メダル % や「上位○○なら銅」

未確認時の返答テンプレ:

```text
comp-timeline の提出ルールが未記入/不確実です。
Overview の Submission Limits を確認してから数字を言います。
仮置きしません。
```

---

## Step 1 — 提出・枠（comp 固有）

Overview / Rules から抜き出し、`comp-timeline.md` の **提出ルール** を埋める:

| 項目 | 例（≠既定） |
|---|---|
| 1 日あたり上限 | 5 / day · または別値 |
| 有効提出 / LB 反映 | Final 2 選択 · **最新 2 件のみ**（sim 典型） |
| チーム提出総量 / Merger | 合算ルール |
| Private / Final 枠 | 最大 2 Final Submissions 等 |
| 提出形式 | CSV · notebook · main.py |
| 実行制約 | 9h · Internet OFF 等 |

### simulation の取り違え防止

| 意味 | よくある実体 |
|---|---|
| 「最新 K 件が LB に載る」 | 提出のたびに古い eng が押し出される。**選抜 UI ではない** |
| 「Final 2 を選ぶ」 | tabular / 一部 の **最終提出選択**。sim とは別物 |

混同して「選択戦略」として語らない。

---

## Step 2 — 締切 UTC

- 時刻の明記がなければ **その日の 23:59 UTC**（公式デフォルト）
- チャット・要約は **`yyyy-mm-dd 23:59 UTC`**
- JST はユーザーが求めたときだけ併記（`23:59 UTC` = 翌日 `08:59 JST`）
- 残り日数は UTC 基準（Skill `kaggle-comp-timeline`）

---

## Step 3 — メダル帯（チーム数 N）

1. **N** を得る（Public LB チーム数 · 終了後は最終 N。会話では N を先に言う）
2. バンド:

| N | Bronze | Silver | Gold |
|---:|---|---|---|
| 0–99 | Top 40% | Top 20% | Top 10% |
| 100–249 | Top 40% | Top 20% | **Top 10** |
| 250–999 | **Top 100** | **Top 50** | **10 + floor(0.2%×N)** |
| 1000+ | Top 10% | Top 5% | **10 + floor(0.2%×N)** |

3. 割合は **floor**。9 チームなら Gold `floor(0.9)=0` → 金なし（公式例）
4. Gold（N≥250）: `10 + floor(0.002 × N)`
5. 自分の rank と比較し **Gold / Silver / Bronze / なし** を明示
6. medals 非対象コンペなら「付与なし」と書く

回答例:

```text
N=6125 → 1000+ バンド
Gold rank ≤ 10+floor(12.25)=22
Silver ≤ floor(5%)=306
Bronze ≤ floor(10%)=612
Private #594 → 銅帯外（無メダル）
```

---

## Step 4 — ファイル更新

差分があれば `docs-ja/comp-timeline.md` を更新し changelog に source（Overview URL / Rules §）を残す。  
`AGENTS.md` に提出上限の表を **コピーしない**（リンクのみ）。

---

## 他 Skill

| Skill | 分担 |
|---|---|
| **本 Skill** | 制約確認・メダル再計算・誤認ガード |
| `competition-conditions` | 概要 + 制約スロット初版 |
| `kaggle-comp-timeline` | 締切・提出ルール SSOT |
| `post-comp-private-retrospective` | 自チーム最終 rank とメダル判定 |
| `kaggle-simulation-tracker` | sim 日次スコア（上限は timeline） |
