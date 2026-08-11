# Kaggle — メダル・提出制約・UTC（横断 SSOT）

> Agent が **他コンペの記憶で上限やメダル帯をでっち上げない**ための共通真実。  
> コンペ固有の数は常に **そのコンペの Overview / Rules / `docs-ja/comp-timeline.md`** が正。  
> 公式 Progression: [Competition Medals](https://www.kaggle.com/progression/competitions)

---

## 1. コンペ制約はコンペごとに異なる（禁止事項）

| 禁止 | 正しい振る舞い |
|---|---|
| 「Kaggle は 1 日 5 提出」と決めつける | 当該コンペの **Daily Submission Limit** を Overview / `comp-timeline` で読む |
| 「Private は選べる 2 枠」を全コンペに適用 | **Final selection / scoring selection** の **N** をルールで確認（0・2・シミュ最新2 等） |
| シミュレーションなのに「提出枠を戦略選択」と誤解 | 多くの Games は **最新 N 件だけ LB に効く**（選択 UI とは別） |
| 他コンペの数字をそのまま言う | 未確認なら「`comp-timeline` 未記入 — Overview 確認が先」 |

**会話で提出回数・有効枠・締切を口にする前の手順（必須）:**

1. `docs-ja/comp-timeline.md` の **提出ルール** 節を読む  
2. 無ければ Overview / Rules から埋め、changelog に source を書く  
3. その数値だけを使う（記憶・他コンペ・噂禁止）

---

## 2. Competition Medals（順位帯はチーム数バンドで変わる）

### 前提

- **Award されるコンペのみ**（Featured / Research 等。Getting Started・一部 Community / playground は対象外）。Overview の medals 表記を確認。
- 最終順位（通常 **Private LB / 最終順位表**）に対して付与。
- **Percentage は切り捨て（floor）**。  
  例: 9 チームのコンペでは `floor(9 × 10%) = 0` のため **Gold 0 枚**（公式例）。
- 帯は **エントリー／最終のチーム数スケール**で変わる。会話中は **「いまのチーム数 N」** を明示してから計算する。  
  N が 249→250 や 999→1000 をまたぐと **帯の定義そのものが変わる**。
- 同一 % でも N が違うと **順位のカットオフ（絶対順位）が違う**。  
  例: 1000 チーム Top 10% bronze ≈ rank ≤ 100。  
  5000 チーム Top 10% bronze ≈ rank ≤ 500。

### 公式表（チーム数バンド）

| チーム数 N | Bronze | Silver | Gold |
|---:|---|---|---|
| **0 – 99** | Top **40%** | Top **20%** | Top **10%** |
| **100 – 249** | Top **40%** | Top **20%** | Top **10**（チーム） |
| **250 – 999** | Top **100** | Top **50** | **Top 10 + 0.2%** |
| **1000+** | Top **10%** | Top **5%** | **Top 10 + 0.2%** |

出典: [Kaggle Progression — Competitions](https://www.kaggle.com/progression/competitions)

### 計算ルール（Agent）

1. **バンド判定:** 上記 4 列から N の行を選ぶ（境界は inclusive: 99 は小、100 は中）。
2. **割合系:** `cutoff = floor(N × p)`。`cutoff < 1` ならその色は **0 枚**。
3. **絶対順位系（例 Top 100）:** rank ≤ K が範囲。
4. **Gold: Top 10 + 0.2%（N≥250）:**  
   `gold_slots = 10 + floor(0.002 × N)`  
   例: N=1000 → 10+2=12 · N=5000 → 10+10=20 · N=250 → 10+0=10
5. ユーザーに話すときは必ず形を揃える:

```text
N=5000（1000+ バンド · 架空例）:
  Gold  ≤ 10 + floor(0.002×5000) = 10+10 = rank 1–20
  Silver ≤ floor(0.05×5000) = rank 1–250
  Bronze ≤ floor(0.10×5000) = rank 1–500
  （例: Private #480 → Bronze · #240 → Silver）
```

### 会話での誤用パターン（避ける）

| 誤り | 理由 |
|---|---|
| 「上位 10% なら金」 | N バンドと Gold 定義（10+0.2% 等）を無視 |
| 小規模コンペの「金 10%」を大規模に流用 | 1000+ は Gold が **% ではなく 10+0.2%** |
| 「メダル圏 = Public の感覚」だけで断言 | 最終は Private。shake-up で帯をまたぐ |
| チーム数を聞かない / 更新しない | N が伸びると cutoff が動く |

---

## 3. 提出・LB・枠 — 型別の「あるある」と確認項目

**すべて「典型」であり既定値ではない。** 数字は Overview で上書き。

| 型 | よくある項目 | 誤認しやすい点 |
|---|---|---|
| **tabular / Code Comp** | 1 日 **N** 提出 · Final **2** selections | N は 5 とは限らない。Code Comp は notebook 出力制約 |
| **simulation / Games** | 1 日 **M** agents · **最新 K 件のみ**がランク対象 | 「戦略的に 2 枠を残す」選択制と混同しない。**最新**が自動で効くことが多い |
| **LoRA / 特殊提出** | rank 上限 · zip 形式 · Final 2 | 日次上限が低い／長い実行制限 |
| **全型** | Team size · Merger · External data · Internet · time limit | |

`comp-timeline.md` の提出ルール表は **最低限** 次を埋める:

- 1 日あたり上限（未確認なら `?` + source 要）
- 有効提出 / LB に効く件数（最新 K / Final selection N）
- Private / Final 枠
- 提出形式（csv / notebook / main.py）
- 時刻はすべて **UTC**

---

## 4. 時刻 — 既定は UTC（日本時間で話さない）

公式文言（Timeline 典型）:

> All deadlines are at **11:59 PM UTC** on the corresponding day unless otherwise noted.  
> The competition organizers reserve the right to update the contest timeline if they deem it necessary.

### Agent 規則

| する | しない |
|---|---|
| 締切・残り日数を **UTC** で書く（例: `2026-08-05 23:59 UTC`） | 根拠なく「8/6 深夜（日本）」だけにする |
| 公式に JST が無い限り、既定は **23:59 UTC** | 他コンペの延長を想定して勝手にずらす |
| ユーザーが JST を求めたときだけ **換算を併記**（UTC+9） | 要約時に UTC 表記を落とす |
| `comp-timeline` の日時列は `… UTC` と明示 | 日付だけ書いてタイムゾーンを曖昧にする |

**JST 換算（ユーザー依頼時のみ）:**  
`23:59 UTC` → 翌日 **08:59 JST**（夏時間なし）。

残り日数の計算基準は Skill `kaggle-comp-timeline` どおり **作業時点の UTC**。

---

## 5. 要約・回答チェックリスト

- [ ] 提出上限・有効枠を口にした → `comp-timeline` の数値と一致
- [ ] メダル・順位帯を口にした → **N チーム**とバンド・floor 計算を併記
- [ ] 締切を口にした → **日付 + 23:59 UTC**（注記なければ）
- [ ] simulation → 「最新 K」と「選択 2 枠」を取り違えていない
- [ ] 未記入項目 → 数値を作らず `要 Overview 確認` と返す

---

## 6. 関連

| 置き場 | 役割 |
|---|---|
| 本ファイル | 横断ノーマ（メダル表・禁止・UTC） |
| Rule `kaggle-comp-constraints` | 毎セッション注意 |
| Skill `competition-conditions` | conditions 初版に制約スロット |
| Skill `kaggle-comp-timeline` | 提出・締切 SSOT |
| Skill `kaggle-competition-constraints` | 確認・再計算専用 |
| `docs-ja/comp-timeline.md` | 当該コンペの実数 |
