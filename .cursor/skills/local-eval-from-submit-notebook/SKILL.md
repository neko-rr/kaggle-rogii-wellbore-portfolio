---
name: local-eval-from-submit-notebook
description: 提出用ノートを安全に fork してローカル検証用パイプラインを作る汎用スキル。コンペやノートブック名に依存せず、trainラベルに対応する eval 予測CSVを生成し、row_id一致率・種別AUC・弱点分析まで実施する。ユーザーが「ローカル検証コードを作って」「提出ノートを評価用に変えて」「eval csvを作って」と依頼したときに使う。
---
## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| —（fork 編集中心） | Kaggle Notebook 実行（ユーザー） | — | my-submitted-notebook/ · my-local-eval-notebook/ · lifecycle-manifest.md | my-local-eval-notebook/ · lifecycle-manifest.md · local_eval_preds manifest |

**要ユーザー明示 OK:** Kaggle 上 Dataset 公開

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

あなたは優秀なKagglerです。  
目的は「提出用ノートを壊さずに、ローカル検証可能な評価用パイプラインを作る」ことです。

# この Skill を使うタイミング
- ユーザーが提出ノートからローカル検証用を作りたいとき
- 提出CSVとtrainラベルの `row_id` 不一致で困っているとき
- `macro_auc=0.5 固定` など、評価が明らかに壊れているとき

# 必須方針（最重要）
1. **提出用ノートと評価用ノートを分離**する（同一ノートで混ぜない）。
2. **row_id 一致率チェック**を必ず入れる（最低 0.95）。
3. test 予測 CSV（提出用）を train ラベル評価に流用しない。
4. 失敗時は「何が足りないか」をファイル名付きで明示する。

# 実装手順
1. 任意の提出ノートから local-eval fork を作る。
   - `MODE="submit"` -> `MODE="train"`（または `eval_local`）
   - 出力ファイル名はモデル数に応じて `*_eval.csv` に変更
2. **移動必須:** 評価専用 fork は **`my-local-eval-notebook/{name}/` のみ** に置く（`my-notebook/` に `-local-eval` を残さない）。**`lifecycle-manifest.md` を `local-eval` に更新**（Skill: `kaggle-notebook-folders`）。
   - 生成ノート（`*_generator.ipynb`）または simulation bot ツリー
   - バンドル/検証ノート（`*_input_builder.ipynb`）
   - 手順書（README, CHECKLIST）
3. 生成物を `/kaggle/working/local_eval_preds/` に出力する。
4. `manifest.json` に source と output を記録する。
5. 評価ノートでは `MODEL_SOURCE_OVERRIDES` で `*_eval.csv` を読む。

# 実行順・実行場所（ユーザー説明必須）
ユーザーへは必ず、以下の順で説明する。

1. **ローカル（Cursor）**
   - 提出ノートから local-eval fork を作成
   - 変更内容を保存（`*_eval.csv` を出力する設定）
2. **Kaggle（GPU推奨）**
   - local-eval fork ノートを実行して `*_eval.csv` を生成
   - 出力は `/kaggle/working/local_eval_preds/` に保存
3. **Kaggle（CPUでも可）**
   - `local_eval_preds/` を Dataset 化（New Dataset）
4. **Kaggle（評価ノート実行）**
   - 評価ノートに上記 Dataset を Input 追加
   - `MODEL_SOURCE_OVERRIDES` を `*_eval.csv` のパスで設定して実行

# Input 追加の説明テンプレート（ユーザー向け）
必ず下記を説明すること。

1. 右ペイン `Add Input` を開く
2. `Datasets` で `local_eval_preds`（作成した Dataset）を追加
3. ノート内でパスを確認
   - 例: `/kaggle/input/<dataset-slug>/subm_22_eval.csv`
4. `MODEL_SOURCE_OVERRIDES` を設定

```python
MODEL_SOURCE_OVERRIDES = {
    'Model_22': '/kaggle/input/<dataset-slug>/subm_22_eval.csv',
    'Model_51p': '/kaggle/input/<dataset-slug>/subm_51p_eval.csv',
    'Model_74': '/kaggle/input/<dataset-slug>/subm_74_eval.csv',
}
AUTO_BUILD_SUBM_FROM_EOS9 = False
```

5. `row_id overlap` のログを確認し、`>= 0.95` を満たすことを確認

# チェックリスト
- [ ] すべての `*_eval.csv` が存在
- [ ] 3ファイルすべて `row_id` 列あり
- [ ] trainラベル row_id との overlap >= 0.95
- [ ] `macro_auc` が 0.5 固定になっていない

# 失敗時の標準エラーメッセージ
- source 不足:
  - `Need either pred_model*.npz (eval row_id aligned) or *_eval.csv`
- row_id 不一致:
  - `row_id overlap too low ... Likely using test submission for train labels`

# 実務の流れ
提出ノートをコピーして検証用 fork を作る
検証用で *_eval.csv（train row_id）を出す
その結果で種別AUCや弱点分析をする
良かった変更だけ提出ノートに戻す

# なぜこれが強いか
提出の安定性を壊さない
検証結果が「本当に使える数字」になる
改善の判断が速くなる

# ユーザーへの説明テンプレート（短文）
- 「提出用と評価用は別ノートに分けます」
- 「まず *_eval.csv を作ってから eval ノートで読みます」
- 「Kaggleでは 生成→Dataset化→評価ノートの順で実行します」

# ログ設計を含めるかの方針
- この Skill は「提出ノートを評価可能にするワークフロー」に集中する。
- 「評価を上げるためのログ設計（AUC分解、ablation、弱点分析ルール）」は別スキルに分離するのを推奨。
- ただし小規模プロジェクトでは、この Skill の末尾に最小ログ項目（`per_species`, `metric_by_group`, `ablation`）だけ同居してもよい。

# 連携スキル
- 本 Skill 完了後、ログ分析は `local-eval-log-strategy` を使用する。
- 一連フロー（作成→分析→記録）をまとめて進める場合は `local-eval-improvement-orchestrator` を使用する。
