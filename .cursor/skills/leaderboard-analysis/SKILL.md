---
name: leaderboard-analysis
description: 終了済みKaggleコンペのLeaderboardを優秀なKaggler視点で分析し、日本語の要約ファイルを作成する。Use when the user asks to analyze a finished competition leaderboard, summarize rankings, compare Public/Private LB, review top teams/solutions, or extract lessons for future Kaggle competitions.
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | LB CSV/スクショ · retro/ | retro/ · docs-ja/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Leaderboard Analysis

終了済み Kaggle コンペの Leaderboard を分析し、次のコンペ・実験設計に使える形で要約する。

## 使う場面

- ユーザーが「終了したコンペのリーダーボードを分析して」「Leaderboard を要約して」「上位解法や順位変動を整理して」と依頼したとき。
- Kaggle の Public/Private Leaderboard、Solutions、Discussion、Working Notes を見て、実験方針に落とし込みたいとき。
- 特定コンペだけでなく、任意の Kaggle コンペに適用する。

## 入力

以下のいずれかを使う。

- Kaggle Leaderboard URL
- Kaggle コンペ URL
- Leaderboard のスクリーンショット、CSV、HTML、またはユーザー貼り付けテキスト
- 上位 Solution / Discussion / Working Note の URL

必要な情報が不足している場合は、作業前に確認する。特に Private LB が見えない場合は、Public LB のみで分析するか、ユーザーにスクリーンショット・CSV の提供を依頼する。

## 収集する情報

### 必須

- コンペ名、URL、終了日、評価指標
- チーム数、参加者数、提出数（取得できる場合）
- 1位、Top 5、Top 10、Top 25、**公式メダル帯**のスコア
- Public LB と Private LB の差、順位変動、shake-up の有無
- **チーム数 N** と Progression バンドに基づく Gold / Silver / Bronze の **rank 上限**  
  （Skill `kaggle-competition-constraints` · `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md`）  
  **禁止:** 小コンペの % 表を大規模に転用 · top10%=Gold 短絡（N≥1000 の top10% は **Bronze**）
- 上位チーム名、解法リンク、Notebook / Discussion / Working Note の有無
- 評価指標上、スコア差がどの程度意味を持つか

### 可能なら収集

- 1位と各順位帯のスコア差（Top 1 vs Top 5 / 10 / 25 / **medal cutoff**）
- メダル閾値（**floor 計算を表に書く**）、同点・小数丸めによる順位密集
- Public と Private の相関が弱い兆候
- 上位解法の共通パターン（データ、モデル、CV、後処理、アンサンブル、外部データ）
- 失敗しやすい方針（LB overfit、CV 不一致、リーク疑い、時間制約違反になりやすい構成）

## 分析観点

優秀な Kaggler として、単なる順位表ではなく「なぜその leaderboard になったか」を分析する。

1. **スコア分布**
   - 上位が密集しているか、1位が抜けているか。
   - metric の性質上、小さい差が実務上どれほど大きいかを説明する。

2. **Public/Private の安定性**
   - Public と Private の差、順位の入れ替わり、shake-up を確認する。
   - Public LB に依存しすぎた可能性があるかを見る。

3. **上位解法の共通点**
   - データ活用、外部データ、事前学習、CV、モデル、アンサンブル、後処理を整理する。
   - 再現可能性、計算コスト、提出制約への適合も見る。

4. **CV と LB の関係**
   - 上位 Solution がどのような CV を使ったか。
   - Public LB と CV の乖離、Private で効いた検証設計を重視する。

5. **次回コンペへの示唆**
   - そのコンペ固有の話と、他コンペにも転用できる一般則を分ける。
   - 「今すぐ試す価値が高いこと」「条件付きで試すこと」「避けること」を明確にする。

## 出力ファイル

コンペフォルダがある場合は以下に作成する。

**`retro/` が存在する場合（コンペ終了後・推奨）:**

```text
yyyymmdd-コンペ名/
└─ retro/
   └─ retro-leaderboard.md
```

**`retro/` が無い場合（従来）:**

```text
yyyymmdd-コンペ名/
├─ docs-ja/
│  └─ leaderboard.md
└─ docs-en/
   └─ leaderboard.md
```

`retro/` があるときは `retro-leaderboard.md` を優先する。Skill `post-comp-retro-setup` で `retro/` を新設できる。

既存の `docs-ja/leaderboard.md` がある場合は、新規作成ではなく更新する。更新時は「更新日」と「追加した情報」を明記する。

コンペフォルダがまだ無い場合は、既存 skill の規約に合わせて `yyyymmdd-コンペ名/` を提案し、作成前にユーザー確認を取る。

## 日本語要約テンプレート

```markdown
# [コンペ名] Leaderboard 分析

**分析日:** yyyy/mm/dd  
**コンペ:** [URL]  
**評価指標:** [metric]  
**最終提出日:** yyyy/mm/dd  
**データソース:** Kaggle Leaderboard / Solutions / Discussion / Working Notes / ユーザー提供資料

---

## 要約

- [1-3行で leaderboard の結論]
- [Public/Private の安定性、上位密集、勝ち筋]
- [次の実験・コンペに転用すべき最重要ポイント]

---

## Leaderboard 概況

| 項目 | 値 |
|------|-----|
| Teams | |
| Participants | |
| Submissions | |
| 1位 Private | |
| 1位 Public | |
| Top 10 圏 | |
| Top 25 圏 | |
| メダル閾値 | |

---

## 上位順位とスコア差

| 順位帯 | Private score | 1位との差 | コメント |
|--------|---------------|-----------|----------|
| 1位 | | | |
| Top 5 | | | |
| Top 10 | | | |
| Top 25 | | | |
| Medal cutoff | | | |

---

## Public / Private Shake-up

- **安定性:** [高/中/低]
- **主な順位変動:** [分かる範囲で記載]
- **解釈:** [Public LB overfit の有無、分布差、metric の不安定性]

---

## 上位解法の共通点

| 観点 | 共通パターン | 重要度 |
|------|--------------|--------|
| データ | | |
| CV | | |
| モデル | | |
| 外部データ/事前学習 | | |
| アンサンブル | | |
| 後処理 | | |
| 推論制約対応 | | |

---

## 効いた可能性が高い施策

1. [施策]
2. [施策]
3. [施策]

## 効果が限定的・危険だった施策

1. [施策]
2. [施策]
3. [施策]

---

## 次回コンペへの示唆

### すぐ試す価値が高い

- [具体的な実験案]

### 条件付きで試す

- [条件と実験案]

### 避ける

- [避ける理由]

---

## 未確認・追加で見るべき資料

- [Solution URL]
- [Discussion URL]
- [Working Note URL]
```

## 英語ファイルの扱い

`docs-en/leaderboard.md` には、以下のどちらかを保存する。

- Kaggle Leaderboard / Solution の原文抜粋
- 分析に使った英語メモ、URL、表、取得日時

英語原文が無い場合は無理に作成しない。日本語要約だけで足りる場合は、最終回答でその旨を説明する。

## 品質チェック

作成後に確認する。

- 数値が Kaggle 表示、論文、Solution のどれ由来か分かる。
- Public と Private を混同していない。
- 「スコアが高い」だけでなく、差分・安定性・再現性を説明している。
- コンペ固有の示唆と汎用的な示唆を分けている。
- 次に読むべき Solution / Discussion が明記されている。
