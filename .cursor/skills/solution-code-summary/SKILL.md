---
name: solution-code-summary
description: 終了済みKaggleコンペにおける1チーム/1人分の公開解法とコード自体を深掘りし、パイプライン、主要関数、入出力、設定、再現手順、改造ポイントを日本語で要約する。Use when summarizing one competitor's solution plus its actual code, notebooks, scripts, repository, or implementation details after a competition ends.
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | 公開 repo · notebook コード | docs-ja/solution/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Solution Code Summary

終了済み Kaggle コンペの **1チーム/1人分の解法とコード**を読み、実装を再利用・改造できる粒度で要約する。

## 使う場面

- ユーザーが「この人の解法とコードを要約して」「Solution と notebook の中身を読んで」「コード自体を説明して」と依頼したとき。
- 公開 Solution、Notebook、GitHub、script、config、weight 構成を 1 チーム分まとめたいとき。
- 複数解法の横断比較ではなく、**単一解法の実装理解**が目的のとき。

## 他 skill との使い分け

| skill | 使う場面 |
|-------|----------|
| `leaderboard-analysis` | 順位・スコア差・shake-up を分析する |
| `solution-analysis` | 複数解法や上位解法の勝因・再現性・実験案を比較する |
| `notebook-analysis` | Kaggle Notebook 単体を簡潔に要約し、コードを `.py` 保存する |
| `solution-code-summary` | **1人の解法 + コード全体**を実装レベルで深掘りする |

## 入力

以下のいずれかを使う。

- Kaggle Solution URL
- Kaggle Notebook URL / `.ipynb`
- GitHub repository / scripts / config
- Working Note / README
- ユーザーが貼り付けた解法本文・コード断片

情報が不足している場合は作業前に確認する。特に「順位・チーム名」「対象コードの場所」「保存先コンペフォルダ」「再現まで必要か」を確認する。

## 分析手順

1. **メタ情報を確認**
   - コンペ名、順位、Public/Private score、作者、URL、コード形式を確認する。

2. **コード全体の入口を探す**
   - Notebook ならセル構成、script なら `main` / config / inference entrypoint を特定する。
   - 依存関係、input dataset、weight、output file を確認する。

3. **パイプラインを分解**
   - data loading
   - preprocessing / feature extraction
   - model definition
   - training
   - validation / CV
   - inference
   - postprocess
   - ensemble / blending
   - submission 作成

4. **主要コードを読む**
   - 重要な class / function / config を一覧化する。
   - 入力、出力、副作用、重要パラメータを説明する。
   - trick、hard-coded 値、リーク懸念、再現に必要な外部ファイルを記録する。

5. **再現性と改造ポイントを評価**
   - そのまま動くか、Kaggle/Colab/ローカルで何が必要かを整理する。
   - 自分の実験へ移植するなら、どの関数・設定を変えるべきかを明記する。

## 出力ファイル

コンペフォルダがある場合は以下に作成する。

```text
yyyymmdd-コンペ名/
├─ docs-ja/
│  └─ solution-code/
│     └─ rankXX-team-name-code-summary.md
└─ docs-en/
   └─ solution-code/
      └─ rankXX-team-name-source-notes.md
```

Notebook のコード抽出 `.py` も保存する場合は、既存の `docs-en/others-notebook/` または `docs-en/solution-code/` のどちらに置くかをユーザーに確認する。既存プロジェクト規約がある場合はそれに従う。

## 日本語要約テンプレート

```markdown
# [Rank] [Team / Author] 解法・コード要約

**分析日:** yyyy/mm/dd  
**コンペ:** [URL]  
**順位:** Private [rank] / Public [rank]  
**Score:** Private [score] / Public [score]  
**作者:** [team / members]  
**対象:** [Solution URL / Notebook URL / GitHub URL]  
**コード形式:** Notebook / scripts / repository / mixed

---

## 1. 要約

- [この解法の一言要約]
- [コード上の中心アイデア]
- [再現・移植で最も重要な注意点]

---

## 2. ファイル構成・入口

| ファイル/セル | 役割 |
|---------------|------|
| | |

**実行入口:**  
**入力:**  
**出力:**  
**必要な外部ファイル/重み:**  

---

## 3. パイプライン全体

1. [data loading]
2. [preprocessing]
3. [model]
4. [training / validation]
5. [inference]
6. [postprocess]
7. [submission]

---

## 4. 使用データ・特徴量

| データ | 用途 | 注意点 |
|--------|------|--------|
| 公式データ | | |
| 外部データ | | |
| pseudo label | | |

---

## 5. モデル・学習

| 項目 | 内容 |
|------|------|
| backbone | |
| head | |
| loss | |
| optimizer/scheduler | |
| augmentation | |
| fold/CV | |
| checkpoint | |

---

## 6. 推論・後処理

| 項目 | 内容 |
|------|------|
| inference input | |
| TTA | |
| ensemble | |
| postprocess | |
| submission | |
| runtime | |

---

## 7. 主要関数・クラス

| 関数/クラス | 役割 | 入力 | 出力 | 重要パラメータ |
|-------------|------|------|------|----------------|
| | | | | |

---

## 8. コード上の重要ポイント

1. [実装 trick]
2. [hard-coded 値]
3. [性能に効きそうな箇所]
4. [壊れやすい箇所]

---

## 9. 再現手順

1. [必要データを用意]
2. [依存関係]
3. [学習/推論コマンドまたは Notebook 実行順]
4. [出力確認]

**再現難易度:** 高/中/低  
**不足しているもの:** [非公開 weight / config / seed / 外部データなど]

---

## 10. 自分の実験への移植案

### そのまま使える

- [関数/設定/後処理]

### 改造して使う

- [変更点]

### 使わない方がよい

- [理由]

---

## 11. 未確認事項

- [追加で読むべきコード/URL]
```

## 英語・原文メモ

`docs-en/solution-code/` には以下を保存する。

- 原文 Solution の要点
- コード構成のメモ
- URL、取得日時
- 必要なら重要コード断片

日本語ファイルには判断・解釈・移植案を中心に書く。

## 品質チェック

作成後に確認する。

- コードの入口、入力、出力が明確。
- パイプラインが実行順に読める。
- 主要関数・クラスの役割が分かる。
- 再現に必要な外部ファイル・重み・config が明記されている。
- 「何がすごいか」だけでなく「どこを変えれば自分の実験に使えるか」が書かれている。
- 解法本文の主張とコード実装が矛盾していないか確認している。
