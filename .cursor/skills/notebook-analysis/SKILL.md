---
name: notebook-analysis
description: Kaggleコンペの他者Notebookの分析
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | others-notebook/ · docs-en/others-notebook/ | docs-ja/others-notebook/ · docs-en/others-notebook/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。
入力はKaggleのベースラインNotebookです。
以下のフォーマットに従って、Notebookでの実施要項を日本語で要約して下さい：

# 出力フォーマット
- 使用するデータ:
- 前処理:
- モデルの定義:
- 学習の設定:
- その他:

## 出力ファイル形式
- 「yyyymmdd-コンペ名/docs-ja/others-notebook/」フォルダに、マークダウン形式で、「Notebook名-Ver番号.md」ファイルに日本語要約を作成する
- 「yyyymmdd-コンペ名/docs-en/others-notebook/」フォルダに、原文のコードをPythonファイルで、「Notebook名-Ver番号」ファイルとして格納する

# 入力
チャットに記述する等

---

## サブエージェント連携（SA-2）

1. 親が **`kaggle-subagent-delegate`** → Task `explore` でエントリポイント・構造のみ取得（`_shared/SUBAGENT-BRIEF.md` § SA-2）
2. **本 Skill** で日本語要約 · 採用可否 · `docs-ja/others-notebook/` 出力
3. intel 反映は `experiment-result-management` → `exp/exp-intel.md`
