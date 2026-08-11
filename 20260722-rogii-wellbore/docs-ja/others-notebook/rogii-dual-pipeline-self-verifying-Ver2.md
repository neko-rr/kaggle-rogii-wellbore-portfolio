# rogii-dual-pipeline-self-verifying — Ver2（分析）

> kernel: `kazeneko77/rogii-dual-pipeline-self-verifying`  
> Public LB: **7.536**（2026-06-16 · Version 2）  
> GPU: **OFF**  
> コード: `docs-en/others-notebook/rogii-dual-pipeline-self-verifying-latest.py`

## 使用するデータ

- 公式 + `koolbox-offline` + `fleongg/rogii-claude-models-pub` + `ravaghi/...-artifacts`

## 前処理 / アーキテクチャ

公開ノートの典型 **Dual-Pipeline Blend**:

```
Pipeline A "ridge-sp45" (PF×128×scales + beam + LGBM/Cat + Ridge)
        \  blend w≈0.55
Pipeline B fleongg pretrained submission
        /
   Guarded physical override (formation contacts)
   — known prefix で自己検証して合格した well のみ上書き
```

## モデルの定義

- A: particle filter + tabular meta
- B: fleongg 事前学習出力を CSV として読み blend
- Override: `tvt_from_contacts` — **prefix RMSE で自己検証**、失敗なら blend 維持

## 学習の設定

- CPU · Internet OFF
- 最終: `submission_sp45_fleongg_w0.55.csv` 系

## その他（重要・正直な caveat）

ノート自身が明記:

> override は test が train と重なるときだけ効く。**完全 hidden（Private）では no-op**。残るのは dual-pipeline blend（~10.5 CV と自称）。

→ Public 改善に効いても Private では無効になりうる **危険なガード**。

## 採用可否

| 判断 | 理由 |
|---|---|
| **Final 主軸にしない** | LB 最悪帯 · Private で override 無効 |
| blend 思想は参考 | 相関の低い2系統の平均は有効だが、中身が両方公開系なら弱い |
| 学習用 | 「自己検証ガード」の設計パターンのみ抽出可 |
