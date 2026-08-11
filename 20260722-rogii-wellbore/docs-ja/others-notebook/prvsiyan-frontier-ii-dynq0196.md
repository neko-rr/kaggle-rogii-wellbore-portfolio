# prvsiyan Frontier II VISUALS — 日本語分析（DYNQ0196）

> analyzed: 2026-07-27  
> source: [`prvsiyan/rogii-public-score-frontier-ii-visuals`](https://www.kaggle.com/code/prvsiyan/rogii-public-score-frontier-ii-visuals)  
> 原文: `others-notebook/public-useful-refresh-20260727/prvsiyan-frontier-ii-visuals/`  
> 関連: [DYNQ0130](prvsiyan-frontier-blend-visuals-dynq0130.md) · [evansussex Q0522](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md)

## 1 行結論

**Contact-Gated 同家系**の Frontier 変種。DYNQ0130（+0.130）の次世代で、PF branch report 由来の **符号付き +0.196 ft（DYNQ0196）**。井 ID / SHA ハードコード無し · hidden sample 順追従を主張。  
公開コード帯の監視対象だが **別予測面ではない** → Final 本命・Active CHK 化しない。

## 使用するデータ

tip / evansussex と同型 artifact DS（koolbox · fleongg · ravaghi · nina2025 等）。メタ上 **CPU only**（accelerator OFF · pretrained cache 必須）。GPU メタフラグが ON でも scoring パスは CPU 前提。

## 前処理 / パイプライン

1. tip 同型 Contact-Gated（`SUBMISSION_PROFILE='vp_balanced_modelpkg_005'` 等）  
2. **DYNQ0196:** run-local `pf_seed_branch_hedge_report` の applied 方向に **0.196 ft** を追加  
3. ランタイム余裕のため **visible_prefix_calibration / model_package_correction を noop 化**（メタ `disabled_runtime_layers`）  
4. VISUALS 付録は CSV 後・読取専用（GS1.30+DYNQ0196 ラベル）

## モデルの定義

新規学習なし。公開スタック + 動的 branch 延長のみ。

## 学習の設定

提出モード。重い CV OFF。

## 進化比較

| 項目 | evansussex Q0522 | DYNQ0130 | **DYNQ0196（本 NB）** |
|---|---|---|---|
| 追加量 | +0.522（特定井 · 合計2.522） | +0.130（applied 全井） | **+0.196**（applied 全井） |
| 井指定 | ハードコード + SHA | レポート動的 | レポート動的 |
| 家系 | Contact-Gated | 同 | **同** |
| 採用 | Final 不可 | Final 不可 | **Final 不可** |

## 自チーム

- **監視のみ**（公開 Frontier の定数延長レース）  
- tip / gated への移植は Public 追い → Private 非推奨  
- checklist Active 化しない · license **T032**
