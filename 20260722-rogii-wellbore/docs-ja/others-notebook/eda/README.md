# EDA 公開 Notebook 索引（日本語）

> updated: 2026-07-24  
> 選定方針: **真のデータ探索・地質直感・構造事実**を優先。票の多い dual-track / 「VISUALS」LBクローンは除外  
> 原文: [`others-notebook/eda/`](../../../others-notebook/eda/)  
> **日本語注釈ノート:** [`others-notebook/eda-ja/`](../../../others-notebook/eda-ja/)（マークダウンを日本語化 · コードは原文）

---

## まず読む順番（推奨）

| 順 | 優先 | 日本語注釈ノート | 作者 | なぜ最適か |
|---|---|---|---|---|
| 1 | **S** | [`rogii-geosteering-for-beginners-7-visuals-ja`](../../../others-notebook/eda-ja/rogii-geosteering-for-beginners-7-visuals/) | n0Rollback | 公式 PNG の読み方 · TVT/GR/typewell の直感 |
| 2 | **S** | [`eda-starter-ja`](../../../others-notebook/eda-ja/eda-starter/) | Chris Deotte | 公式風の網羅 EDA · 方向性・近傍・欠損 |
| 3 | **S** | [`rogii-visual-eda-the-evaluation-zone-ja`](../../../others-notebook/eda-ja/rogii-visual-eda-the-evaluation-zone/) | n0Rollback | 評価区間の定義 · train/test 重なりの正直な注記 |
| 4 | **A** | [`rogii-wellbore-data-walkthrough-ja`](../../../others-notebook/eda-ja/rogii-wellbore-data-walkthrough/) | HarshitSama | 短い構造事実ツアー |
| 5 | **A** | [`decoding-eagle-ford-…-ja`](../../../others-notebook/eda-ja/decoding-eagle-ford-why-some-wells-are-hard/) | souldrive | Eagle Ford 層序 · 難井の地質理由 |
| 6 | **A** | [`the-15-ft-datum-…-ja`](../../../others-notebook/eda-ja/the-15-ft-datum-why-honest-cv-bottoms-out/) | souldrive | ±15 ft 二峰 · 中点最適 · モード決め打ち失敗 |
| 7 | **A** | [`rogii-tvt-identity-…-ja`](../../../others-notebook/eda-ja/rogii-tvt-identity-and-honest-cv-design/) | souldrive | 6tops=1面 · test identity · well/field-CV |
| 8 | **B** | [`is-your-target-data-limited-…-ja`](../../../others-notebook/eda-ja/is-your-target-data-limited-a-3-test-check/) | souldrive | データ限界 vs モデル限界の3テスト |
| 9 | **B** | [`well-prediction-eda-exploratory-ja`](../../../others-notebook/eda-ja/well-prediction-eda-exploratory/) | sghwr | 表形式の古典 EDA（補完） |
| 10 | **B** | [`rogii-eda-target-free-…-ja`](../../../others-notebook/eda-ja/rogii-eda-target-free-alignment-for-tvt/) | Pilkwang | 大型 · リーク方針・整合（第二読） |

**スキップ推奨:** `rogii-why-3000-teams-are-stuck-at-12`（説明なしコードのみ）· `rogii-wellbore-noobnote-…`（中身薄い）

**追加（2026-07-25 · public-useful refresh）:** Connor [`dz-dtvt-eda`](../dz-dtvt-eda-Ver-latest.md) — 純幾何の研究ログ（`dTVT≈−dZ+drift` · LOO）。`eda/` フォルダ外だが、構造事実の補強として souldrive trilogy の次に読む価値あり。

---

## フォルダ構成

```
others-notebook/
├─ eda/          # 原文（英語）· kernels pull / コピー
├─ eda-ja/       # 日本語注釈付き .ipynb（説明セルを日本語化）
├─ public-useful/  # 提出・物理・検証など混合（既存）
└─ train-scout/    # 学習系スカウト（既存）
```

---

## 横断で得た知見（分析サマリ）

| 知見 | 出典 | 自チームへの示唆 |
|---|---|---|
| TVT = 地層内垂直位置。水平 GR ↔ typewell 照合が中核 | beginners · Chris | 行 ML より整合 |
| 評価区間 = `TVT_input` NaN | visual-eda · walkthrough | マスク再現 CV |
| 6 formation tops ≈ 平行な1面 | walkthrough · tvt-identity | tops を6独立特徴にしない |
| 平坦 TVT 持ち越し ≫ 構造面 U=TVT+Z 持ち越し | tvt-identity | 残差ターゲットは flat anchor |
| 手元 `test/` は train コピー | visual · tvt-identity | 検証に使わない（CHK-072） |
| Eagle Ford / Buda 急崖が相関の背骨 | decoding-eagle-ford | GR denoise · 窓整合の直感 |
| ~30% 井で ±15 ft 二峰 · 中点が RMSE 最適 | 15-ft-datum | CHK-041 結果と整合 · モード決め打ち禁止 |
| well-CV と field-CV を併記（差≈0.3） | tvt-identity | **CHK-072** |
| Public 急改善の一部は train 双子マッチ | visual-eda | Private 耐性を別経路で |

詳細分析: [analysis.md](analysis.md) · **戦略:** [strategy-from-eda.md](strategy-from-eda.md)

---

## ライセンス

他者公開 Notebook の閲覧・学習用コピー。提出にコードを載せる場合は `docs-ja/license-ledger.md` Tier R。
