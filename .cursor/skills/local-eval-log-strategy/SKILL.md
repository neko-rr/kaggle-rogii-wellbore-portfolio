---
name: local-eval-log-strategy
description: ローカル検証ログを設計・分析して評価向上の次アクションを決める汎用スキル。コンペやモデル種類に依存せず、per-class/per-group/ablation/相関/データカバレッジを使って改善優先度を決定する。ユーザーが「どのログを見るべきか」「次に何を試すべきか」「評価を上げる分析をしたい」と依頼したときに使う。
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | — | — | exp/ · eval ログ | exp/ 分析メモ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なKaggler兼AIエージェントです。  
目的は「ローカル検証ログから、再現性のある改善アクションを選ぶ」ことです。

# この Skill を使うタイミング
- `*_eval.csv` や OOF が揃っていて、次の実験優先度を決めたいとき
- 指標はあるが、どのモデル/どのクラスが弱いか分からないとき
- 「提出すべきか」「学習すべきか」「後処理で十分か」を判断したいとき

# 前提
- 予測と正解の `row_id` は一致していること（overlap >= 0.95）
- 評価指標はコンペ公式に合わせる（例: macro ROC-AUC / logloss / AP）
- 提出結果だけでなくローカル検証ログを持っていること

# 必須ログ（汎用）
1. `per_target`（クラス/ラベル単位）
   - 例: `per_species.csv`, `per_class.csv`
   - 最低項目: `target`, `score`, `n_pos`, `n_neg`
2. `group_metrics`（カテゴリ階層単位）
   - 例: `metric_by_group.csv`（class/family/domain など）
3. `ablation`
   - モデル/特徴/後処理ごとの寄与比較
4. `model_diversity` / `model_correlation`
   - 補完性と冗長性を判定
5. `data_coverage`
   - 学習データ有無、正例不足、分布偏り

# 推奨ログ（精度向上向け）
- `hard_negative`（偽陽性多発ケース）
- `confusion_pairs`（混同しやすい組み合わせ）
- `transform_delta`（後処理前後の差分）
- `runtime_profile`（速度・コスト）
- `reproducibility`（seed, dataset version, config hash）

# 分析フロー（実務）
1. **全体スコア確認**
   - ベースラインとの差分、信頼区間、fold分散を確認
2. **弱点抽出**
   - `per_target` 下位群（例: worst 20）を抽出
   - 正例数が極端に少ない対象を分離
3. **原因切り分け**
   - `group_metrics` で系統偏りを見る
   - `model_diversity/correlation` でブレンド余地を判定
4. **施策選択**
   - 後処理で直せるか（閾値/平滑化/校正）
   - 学習が必要か（再学習/再サンプリング/損失重み）
5. **提出判定**
   - ローカル改善が安定（foldまたは複数条件）している場合のみ提出

# 施策マッピング（汎用ルール）
- 下位対象が広範囲に中程度で悪い
  - 優先: 後処理/校正/軽量ブレンド調整
- 特定グループのみ極端に悪い
  - 優先: グループ特化学習、重み付き損失、データ補強
- 単体モデルは弱いが補完性が高い
  - 優先: ブレンド候補として採用
- 単体強いが相関が高い
  - 優先度低（冗長）
- 変換後に下位群が悪化
  - 変換/後処理をロールバック

# 出力フォーマット（ユーザー向け）
1. **現状**
   - 全体指標、ベースライン差分、不確実性
2. **弱点**
   - 下位対象、グループ偏り、データ不足
3. **意思決定**
   - 次に試す上位3施策（理由付き）
4. **提出可否**
   - 提出/見送り、必要な追加検証

# local-eval-from-submit-notebook との連携
- 先に `local-eval-from-submit-notebook` で `*_eval.csv` と基本ログを生成
- 次に本 Skill でログを分析し、次実験と提出判断を決める
- 役割分離:
  - 前者: 作成・実行・整合性保証
  - 本スキル: 分析・優先度決定・改善戦略
- 全体進行を一連で管理したい場合は `local-eval-improvement-orchestrator` を使用する

# ユーザー説明テンプレート（短文）
- 「まずログを5種類に分けて、原因を分離します」
- 「補完性が高い変更だけを次の提出候補にします」
- 「学習が必要か、後処理で十分かを先に判定します」
