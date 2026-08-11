# prvsiyan Frontier Blend VISUALS — 日本語分析（DYNQ0130）

> analyzed: 2026-07-26  
> source: [`prvsiyan/rogii-public-frontier-blend-research-visuals`](https://www.kaggle.com/code/prvsiyan/rogii-public-frontier-blend-research-visuals)  
> 原文: `others-notebook/public-useful-refresh-20260726/prvsiyan-frontier-blend-visuals/`  
> 関連: [evansussex Q0522 6.390](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md)

## 1 行結論

**Contact-Gated 同家系**の Frontier 変種。evansussex の固定井 Q0522 に対し、**DYNQ0130** は PF branch report 上の **applied 井すべて**に符号付き **+0.130 ft** を足す（井 ID / SHA ハードコード無し · hidden sample 順に追従）。  
公開ホット（票74 · 07/26 run）だが **別予測面ではない**。Public 密な定数延長の進化形 → Final 本命・Active CHK 化はしない。

## 使用するデータ

evansussex / tip と同型 artifact DS（koolbox · model-package · ravaghi · fleongg 等）。**GPU OFF**（pretrained cache 必須と明記）。

## 前処理 / パイプライン

1. tip 同型 Contact-Gated（`vp_balanced_modelpkg_005` · `_BH_=0.60` · `gs*1.3` · projection degree 3）  
2. **DYNQ0130:** `pf_seed_branch_hedge_report.csv` の `reason=applied` 各井について、既存 shift の符号方向に **0.130 ft** を追加  
3. submission は hidden の `sample_submission` id 順と一致必須  
4. VISUALS 付録は CSV 不変（参照 Public **6.390** を図のラベルに使用）

## モデルの定義

新規学習なし。公開スタック + 動的 branch 延長のみ。

## 学習の設定

提出モード。重い CV OFF。

## その他（evansussex との比較）

| 項目 | evansussex Q0522 | prvsiyan DYNQ0130 |
|---|---|---|
| 追加量 | +0.522（特定井 · 合計2.522） | **+0.130**（applied 全井 · 符号付き） |
| 井指定 | ハードコード `00e12e8b` + SHA | **レポートから動的** |
| hidden 耐性 | sample 14151 / SHA 前提で脆い | sample 順追従を主張（より提出向き） |
| 家系 | Contact-Gated | 同 |
| 採用 | Final 不可 | **同じく Final 不可** |

## 自チーム

- **監視のみ**（公開 Frontier の次世代パッチ）  
- tip / gated への移植は **Public 追い定数シフト** → Private 非推奨（EDA #8 · F015 精神）  
- checklist Active 化しない
