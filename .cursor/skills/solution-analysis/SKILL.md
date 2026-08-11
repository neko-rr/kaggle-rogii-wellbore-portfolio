---
name: solution-analysis
description: 終了済みKaggleコンペで公表される上位解法・Solution・writeup・Working Note・公開Notebookを優秀なKaggler視点で分析し、再現性、勝因、失敗要因、次に試す実験案を日本語で要約する。Use when the user asks to analyze post-competition solutions, winning approaches, Kaggle solution writeups, or lessons from top teams.
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | intel/ · retro/ · 公開 writeup | docs-ja/solution/ · retro/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Solution Analysis

終了済み Kaggle コンペで公開される上位解法を分析し、次の実験・再現・改善に使える形で要約する。

## 使う場面

- ユーザーが「解法を分析して」「上位 Solution をまとめて」「終了後の writeup を読んで」「勝因を整理して」と依頼したとき。
- Kaggle の Solution、Discussion、Working Note、公開 Notebook、GitHub、arXiv/CEUR 論文を読み、実験方針へ落とし込みたいとき。
- 1 本の解法だけでなく、Top 1 / Top 5 / Top 10 など複数解法を比較したいとき。

## 入力

以下のいずれかを使う。

- Kaggle Solution / Discussion / Notebook / Leaderboard URL
- Working Note / paper / GitHub / README URL
- ユーザーが貼り付けた解法本文、スクリーンショット、コード断片
- 既存の `leaderboard.md`、`conditions.md`、`dataset.md`

情報が不足している場合は作業前に確認する。特に「どの順位の解法か」「どのコンペに保存するか」「再現まで必要か」は確認する。

## 収集する情報

### 必須

- コンペ名、URL、順位、Public/Private score
- チーム名、作者、Solution / Notebook / Paper の URL
- 使用データ（公式、外部、未ラベル、pseudo label、追加収集）
- CV 設計（split、fold、group、OOF、LB との相関）
- モデル構成（backbone、事前学習、head、損失、学習設定）
- 推論構成（TTA、ensemble、postprocess、制約対応）
- 効いた施策、効かなかった施策、ablation
- 再現に必要なファイル、計算資源、依存関係

### 可能なら収集

- Public と Private の順位差、およびその理由の仮説
- 解法同士の共通点・相違点
- 上位解法が共通して避けたこと
- 著者が明言した「最重要ポイント」
- そのコンペ固有の trick と、他コンペへ転用できる一般則

## 分析観点

優秀な Kaggler として、コードや手法をそのまま列挙せず「なぜ効いたか」「自分の実験にどう使うか」を重視する。

1. **勝因の分解（2軸）**
   - **CV・物差し:** 何を測ったか · Final に何を残したか · CV と Public の衝突時ルール。
   - **解法本体:** データ表現 · モデル · 候補/融合 · pretrain · 後処理。
   - **混ぜない:** 「GroupKFold した」と「U-Net 整列した」は別の学習にする。

2. **CV の信頼性**
   - Public/Private と CV が一致したか。
   - leak、domain shift、group split、time split、site split、fold leakage を確認する。
   - **CV が測っていた対象**（tip か出荷全体か）を明記する。

3. **再現性**
   - そのまま再現可能か、外部データ・非公開重み・計算量で難しいかを分類する。
   - Notebook 提出制約、CPU/GPU、Internet OFF、実行時間を確認する。

4. **実験優先度**
   - 今すぐ試す価値が高いもの、条件付きで試すもの、避けるものに分ける。
   - 各案に **軸（A/B）** を付ける（物差し変更 vs 手法変更）。
   - 期待効果、実装コスト、リスクを明記する。

5. **複数解法比較**
   - Top solution だけを信じず、複数チームで共通する施策を重視する。
   - 1 チームだけの trick は、再現性と汎用性を慎重に評価する。

## 出力ファイル

コンペフォルダがある場合は以下に作成する。

**`retro/` が存在する場合（コンペ終了後・推奨）:**

```text
yyyymmdd-コンペ名/
└─ retro/
   └─ retro-solutions.md    # 複数解法の統合分析
```

個別解法の詳細は任意で `docs-ja/solution/` にも保存できる。

**`retro/` が無い場合（従来）:**

```text
yyyymmdd-コンペ名/
├─ docs-ja/
│  └─ solution/
│     ├─ README.md
│     ├─ rank01-team-name.md
│     └─ solution-summary.md
└─ docs-en/
   └─ solution/
      ├─ rank01-team-name.md
      └─ solution-summary.md
```

`retro/` があるときは `retro-solutions.md` を統合要約の主出力とする。Skill `post-comp-retro-setup` で `retro/` を新設できる。

コンペフォルダが無い場合は、既存 skill 規約に合わせて `yyyymmdd-コンペ名/` を提案し、作成前にユーザー確認を取る。

## 単一解法テンプレート

```markdown
# [順位] [Team名] Solution 分析

**分析日:** yyyy/mm/dd  
**コンペ:** [URL]  
**順位:** Private [rank] / Public [rank]  
**Score:** Private [score] / Public [score]  
**作者:** [team / members]  
**ソース:** [Solution URL / Notebook URL / Paper URL]

---

## 要約

- [この解法の結論]
- [最も効いた要素]
- [再現・転用で注意する点]

---

## 解法の全体像

| 観点 | 内容 |
|------|------|
| 使用データ | |
| CV | |
| モデル | |
| 学習 | |
| 推論 | |
| 後処理 | |
| Ensemble | |
| 外部データ/事前学習 | |

---

## 勝因

1. [勝因]
2. [勝因]
3. [勝因]

## 効かなかった/危険だった施策

1. [施策]
2. [施策]

---

## CV と LB の関係

- CV:
- Public:
- Private:
- 解釈:

---

## 再現性

| 項目 | 評価 | メモ |
|------|------|------|
| データ入手性 | 高/中/低 | |
| コード公開 | 高/中/低 | |
| 計算資源 | 高/中/低 | |
| 提出制約適合 | 高/中/低 | |
| 再現難易度 | 高/中/低 | |

---

## 自分の実験への転用

### すぐ試す

- [実験案]

### 条件付きで試す

- [条件と実験案]

### 避ける

- [理由]

---

## 未確認事項

- [追加で読むべき URL / コード / ablation]
```

## 複数解法まとめテンプレート

```markdown
# [コンペ名] 公開 Solution 総合分析

**分析日:** yyyy/mm/dd  
**対象:** Top [N] Solutions / Working Notes / Notebooks  
**関連:** [`leaderboard.md`](../leaderboard.md)

---

## 結論

- [複数解法に共通する勝ち筋]
- [Private で強かった要因]
- [次に試すべき最優先実験]

---

## 解法比較表

| Rank | Team | Score | CV | Data | Model | Ensemble | Postprocess | 再現性 |
|------|------|-------|----|------|-------|----------|-------------|--------|
| 1 | | | | | | | | |

---

## 共通する勝ち筋

### A. CV・物差し（転用時はまずここ）

1. [複数チームで共通 · 物差し/ split / Final]
2. [複数チームで共通]

### B. 解法・モデリング

1. [複数チームで共通 · 表現/候補/fusion/pretrain]
2. [複数チームで共通]

## チーム固有の trick

| Team | 軸(A/B) | Trick | 汎用性 | リスク |
|------|---------|-------|--------|--------|
| | | | | |

---

## 汎用 lessons への書き戻し（必須）

`retro/retro-lessons.md` の `## 汎用` に追記するとき:

- **A.** CV・物差し・提出判断 ← 本節の「A」からのみ
- **B.** 解法・モデリング本体 ← 本節の「B」からのみ
- **C.** 運用 ← CLI/保管/提出衛生のみ

混ぜて1項目にしない。収穫は Skill `kaggle-knowledge-harvest`。

---

## 実験ロードマップ

| 優先度 | 軸 | 実験 | 期待効果 | コスト | リスク |
|--------|----|------|----------|--------|--------|
| 高 | A/B | | | | |
| 中 | | | | | |
| 低 | | | | | |
```

## 保存・更新ルール

- 個別解法は `rankXX-team-name.md` に保存する。
- 複数解法の横断まとめは `solution-summary.md` に保存する。
- 既存ファイルがある場合は新規作成ではなく更新し、「更新日」と「追加情報」を明記する。
- 原文やコード抜粋は `docs-en/solution/` 側に保存する。日本語ファイルには要約と判断を中心に書く。
- Notebook のコード抽出が主目的なら `notebook-analysis` を併用する。
- Leaderboard の順位・スコア分析が主目的なら `leaderboard-analysis` を併用する。

## 品質チェック

作成後に確認する。

- 解法の「何をしたか」だけでなく「なぜ効いたか」が書かれている。
- CV と Private LB の関係を評価している。
- 再現性、計算コスト、データ入手性を明記している。
- すぐ試す実験案が具体的で、期待効果とリスクが分かる。
- コンペ固有の trick と汎用的な学びを分けている。
- **CV・物差し（A）と解法本体（B）を別節で書き、`retro-lessons` でも混ぜていない。**
