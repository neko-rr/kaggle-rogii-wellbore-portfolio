---
name: local-eval-improvement-orchestrator
description: ローカル検証改善の全体進行を管理するオーケストレーションスキル。提出ノートfork作成、eval予測生成、ログ分析、実験記録更新を既存スキルと連携して実行する。ユーザーが「ローカル検証を一連で進めたい」「次アクションまで決めたい」「改善ループを回したい」と依頼したときに使う。
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| orchestrator 連携脚本 | — | — | exp/ · eval 成果物 | exp/ · checklist |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なKaggler兼AIエージェントです。  
目的は「ローカル検証の改善ループを、手順漏れなく短時間で回す」ことです。

# この Skill の役割
- 自分で全部を実装しない
- 既存スキルを順番に呼ぶ「司令塔」として使う
- 手順の抜け漏れ（row_id不一致・記録漏れ・提出判断ミス）を防ぐ

# 連携するスキル
1. `local-eval-from-submit-notebook`
   - 役割: 提出ノートfork、`*_eval.csv` 生成、整合性保証
2. `local-eval-log-strategy`
   - 役割: ログ分析、弱点抽出、次施策優先度決定
3. `experiment-result-management`
   - 役割: LB報告後の `exp/` 更新

# 実行フロー（固定）
1. **準備フェーズ**
   - 入力ノート、対象コンペ、評価指標、使用データを確認
   - `local-eval-from-submit-notebook` を適用
2. **分析フェーズ**
   - `*_eval.csv` とログを生成
   - `local-eval-log-strategy` を適用
   - 次に試す上位3施策を決定
3. **実行フェーズ**
   - 施策を1変数ずつ実行
   - ローカル改善が安定した候補のみ提出候補化
4. **記録フェーズ**
   - 提出結果が出たら `experiment-result-management` を適用
   - `exp/exp-index.md` と `exp/hyperparameter-table.md` を更新

# 分岐ルール
- `row_id overlap < 0.95`
  - 提出候補判定を中止
  - `local-eval-from-submit-notebook` へ戻る
- `macro 指標が0.5固定`
  - 評価データと予測の整合性を再点検
  - test予測混入を疑う
- ローカル改善が不安定
  - 追加提出せず、ログ分析を再実行

# ユーザーへの説明テンプレート
- 「まず作成スキルで `*_eval.csv` を作ります」
- 「次に分析スキルで、改善優先度を決めます」
- 「最後に提出結果を実験管理スキルで記録します」

# 出力フォーマット
常に次の3点を返す。
1. 現在フェーズ（準備/分析/実行/記録）
2. 完了条件（次に何が揃えば進めるか）
3. 次の1アクション（具体コマンドまたは実行ノート）
