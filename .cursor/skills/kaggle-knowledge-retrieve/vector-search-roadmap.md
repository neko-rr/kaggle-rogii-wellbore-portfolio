# ベクトル検索ロードマップ（将来用）

## 導入条件

次を両方満たすまで実装しない。

- `knowledge/cards/` の承認済みカードが50件以上
- taxonomy＋文字列検索で関連知見の取りこぼしが実測された
- `concept_key`による重複候補の確認とalias整理が完了している
- provenance・license・秘密情報auditがPASSしている

## 事前に保存する項目

各カードは現在から次を持つ。

- `search_document`: title・機構・結果・兆候・施策・タグを連結した検索本文
- `taxonomy`: hard filter用の共通語彙
- `embedding.status/model/dimensions/vector_ref`: 将来の生成状態

ベクトル本体はカードへ埋め込まず、`knowledge/vectors/<model-id>/` に置く。

## 将来の検索順

1. taxonomyでコンペ型・制約をhard filter
2. 文字列検索とベクトル類似度を併用
3. 証拠レベル・再現コンペ数でrerank
4. 通常検索ではcandidateを除外
5. 上位結果の根拠と適用禁止条件を必ず表示

## 安全・再現性

- 既定はローカルembedding。外部API送信はユーザー明示許可がある場合のみ
- データセット、秘密情報、Notebook全文をembedding対象にしない
- `model-id`、モデル版、次元数、正規化方式、生成日をmanifestへ保存
- モデル変更時は別indexを作り、旧indexを上書きしない
- ベクトルindexはPrivateな `knowledge/` 内だけに保存する

## 品質ゲート

- 代表的な検索質問と期待カードを評価セット化
- taxonomyのみ、文字列のみ、hybridのRecall@Kを比較
- hybridが改善しない場合は導入しない
- 類似度だけでRule化・CHK化・昇格しない
