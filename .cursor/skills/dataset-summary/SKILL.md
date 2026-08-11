---
name: dataset-summary
description: Kaggleコンペのデータセットの要約
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | dataset/README.md（Git 外） | docs-ja/dataset.md |

**要ユーザー明示 OK:** dataset/ への Agent DL

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なデータサイエンティスト兼Kagglerです。
入力はKaggleのデータセットページです。
以下のフォーマットに従って、日本語で要約して下さい：

# 出力フォーマット
データの概要：
各ファイルの詳細な説明：

## 出力ファイル形式
- 「yyyymmdd-コンペ名/docs-ja/」フォルダに、マークダウン形式で、「dataset.md」ファイルに日本語要約を作成する
- 「「yyyymmdd-コンペ名/docs-en/」フォルダに、原文をマークダウン形式で、「dataset.md」ファイルとして格納する

# 入力
チャットに記述する等
