# 最近トピック短記（中優先）

## 718670 Top-kernel teardown（nvidia-kaggle）

> **2026/07/03** · Jiwei Liu · 票 27 · 原文 docs-en  
> 公開 NB の版ごと LB・コード差分・依存を機械集計。当時 Public 先頭 **5.262** は公開 NB より遥か下。粒子フィルタ系は同一コードでも **~0.4 RMSE** 揺れ。

## 721578 GP + Typewell warping

> **2026/07/06** · szknaoki · 票 4 · コメント 0  
> 全球 GP（形成深度）→ TVT_input 条件付け → 線形地質 → GR warping。物理解釈パイプラインの公開説明。

## 722236 Complex NNs（再取得 2026/07/24）

> **2026/07/06** · 最新コメント **2026/07/20** · コメント 5  
> steven: 複雑 NN より **表現・CV・学習安定**が決定要因。Shrey: 上位は NN 感（2提出で到達例）。DECEM: simple NN **CV 8.9 / LB 8.39** · matcher/ranker は未確定。→ 学習本命はアーキより整合特徴（training-insights）。

## 724669 Bad wells を外すか

> **2026/07/12** · Zejun_ · CV で RMSE20+ の井。学習除外するか未結論（過学習懸念）。Andrey: 「bad typewell」定義の確認のみ。

## 719235 Geologists' analysis

> **2026/07/04** · 票 20 · **コメント 0**  
> Typewell と合う井 / 全く合わない井（例 `000d7d20`）。地質解釈は常に信頼できるか — **Host 未回答**。

## 727537 Competition Analysis

> **2026/07/19** · Chris Deotte が図を評価。投稿者: **spatial kriging / multi-well surface は dead end**（ノイズ床未達）。

## 728712 PF `gs`×1.3（新規 2026/07/24 · 取得 07/25）

> suzu10 · 票 3 · コメント 0  
> 公開 `hjyact/ultimate-pf-config-…` で GR noise `gs`≈**1.3x** がスコア改善。Forum 共有は公平性のため。  
> **F001（heel affine gs）とは別。** tip 公開コードに `*1.3` **既実装**（ultimate-pf / gs130 / luck 同一）· 追加移植不要 · Final2 禁止。詳細: [728712-…](728712-gs-noise-scale-public-nb.md)

## 728879 Well Steerer（新規）

> Tabish · 票 1 · コメント 0 · 操舵体験ツール構想。スコア方針変更なし。

## 729554 Notebook Threw Exception（新規 2026/07/26）

> Angel · コメント1（PC Jimmmy）· sample 14151 は OK でも Submit 失敗。  
> **ログは3偽井のみ** · hidden≈200 の shape/mem が典型。詳細: [error/729554](error/729554-notebook-threw-exception.md)

## prvsiyan DYNQ0130（公開 NB · 2026/07/26）

> Frontier VISUALS ホット · evansussex Q0522 の **+0.130 動的 branch** 版 · tip 同家系 · Final不可。  
> [分析](../others-notebook/prvsiyan-frontier-blend-visuals-dynq0130.md) · 総括 [20260726-refresh](20260726-refresh.md)

> コメント **0** · Host 未回答 — **不使用**維持。

## 728256 AI コーディング支援（更新 2026/07/24）

> コメント **3** · Host 未回答。tennogh: Rules に LLM 記載あり→**可寄り**。詳細: [728256-ai-coding-assistant.md](728256-ai-coding-assistant.md)

## 727570 souldrive 追記（2026/07/23 → 反映 07/24）

> well-CV vs field-CV（≈+0.3）· worst field · `test/` は train コピーで検証不可。詳細: [727570-local-validation.md](727570-local-validation.md)
