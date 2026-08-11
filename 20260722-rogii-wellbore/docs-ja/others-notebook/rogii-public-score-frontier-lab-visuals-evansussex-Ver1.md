# rogii-public-score-frontier-lab-visuals — 日本語分析（evansussex · Public **6.390** V1）

> analyzed: 2026-07-26  
> source: [`evansussex/rogii-public-score-frontier-lab-visuals`](https://www.kaggle.com/code/evansussex/rogii-public-score-frontier-lab-visuals?scriptVersionId=337186797)  
> scriptVersionId: **337186797** · 作者表記 Best Score **6.390 V1**  
> 原文フォルダ: `others-notebook/rogii-public-score-frontier-lab-visuals-evansussex/`  
> コード抽出: `docs-en/others-notebook/rogii-public-score-frontier-lab-visuals-evansussex-Ver1.py`  
> 自チーム現在地（参考）: [`exp/exp-index.md`](../../exp/exp-index.md)（自 Best は別物）  
> 後継監視: [`prvsiyan-frontier-blend-visuals-dynq0130.md`](prvsiyan-frontier-blend-visuals-dynq0130.md)（+0.130 動的 · Final不可）

---

## 1 行結論（優秀な Kaggler）

**Contact-Gated 同家系**に、公開帯で効きやすい **(1) PF `gs`×1.3** と **(2) 特定1井への定数シフト Q0522（+0.522 ft）** を載せた Frontier Lab。  
作者 Public **6.390** は公開コード帯では最右寄りだが、**別予測面ではない**。Q0522 は `sample_submission` 整列・固定 SHA・井 `00e12e8b` 前提の **Public 狙い1井パッチ** → Private / Final 本命には向かない。丸写し・Final2 差し替えは禁止。

---

## 使用するデータ

| 種別 | 内容 |
|---|---|
| コンペ | `rogii-wellbore-geology-prediction` |
| 外部 DS（metadata） | koolbox-offline · rogii-03 · pilkwang model-package · v10-fresh-artifacts · fleongg claude-models · tabicl-mirror · ravaghi artifacts |
| GPU | **ON** · Internet OFF · Public NB |

自 tip（luck / Contact-Gated）と同系統の artifact スタック。

---

## 前処理 / パイプライン

見出しどおり **Contact-Gated Stratigraphic Alignment**:

1. Ridge / residual ensemble + PF → SP45 selector アンカー  
2. U=T+Z 投影（`SP45_PROJECTION_DEGREE = 3`）+ learned blend  
3. Guarded same-well contact override（EGFDU 優先 · prefix RMSE ガード）  
4. Visible-prefix calibration（profile: `vp_balanced_modelpkg_005`）  
5. Model-package 弱ゲート（`max_w≈0.00425`）  
6. PF seed-branch midpoint hedge（`_BH_STRENGTH=0.60` · sep 4–40）  
7. **差分層:** PF GR noise `gs = clip(...) * 1.3`  
8. **差分層 Q0522:** 既に hedge 適用された **1井だけ** に追加 +0.522 ft（合計 2.522 ft）  
9. VISUALS 付録（図）は **submission を変えない**（変更したら RuntimeError）

既定プロファイル: **`SUBMISSION_PROFILE = 'vp_balanced_modelpkg_005'`**（自 tip と同名）。

---

## モデルの定義

- 新規学習アーキテクチャではない。公開 dual-track / Contact-Gated の再構成 + 公開 Frontier 介入。  
- PF: particles 500 · seeds 128 · SP45 ridge/selector 0.30/0.70。  
- 二峰 detector 系フラグはコード上残るが、本 profile では tip 同様「最終面の主役」ではない。

---

## 学習の設定

- `RUN_CV_REPORT = False` · 重い ablation OFF（提出モード）。  
- 本 NB の「改善」は学習ではなく **後段の固定シフト / noise scale**。

---

## その他 — tip / 自チームとの差分

| 項目 | 本 NB（evansussex V1） | 自 tip（luck 系） | 含意 |
|---|---|---|---|
| 家系 | Contact-Gated | 同 | Final「別面」にならない |
| profile | `vp_balanced_modelpkg_005` | 同 | — |
| `_BH_*` | 0.60 / sep 4–40 / cap 2 | 同 | — |
| `gs*1.3` | **あり** | **あり**（既確認） | 728712 吸収済 |
| **Q0522** | 井 `00e12e8b` に **+0.522 ft**（BH 2.0 の上） | **なし** | **本 NB の主差分** |
| projection degree | 3 | 3（抽出 tip も 3） | 実質同 |
| 作者 Public | **6.390** | tip smoke 6.569 帯 | 公開コード最右寄り（作者主張） |
| 旧 VISUALS（他作者） | — | 自提出参考 **6.581** | 本 NB の方が良い主張 |

### Q0522 の実装上の注意（重要）

コードは次を **同時に要求**する:

- `submission.csv` が **`sample_submission.csv` と同一 id 順**  
- 行数・統計が固定（**rows=14151**）または固定 **file SHA**  
- branch hedge が **ちょうど1井** `00e12e8b` に **shift=2.0 · moved_rows=4301**  
- その井の行にだけ **+0.522**

これは「汎用アルゴリズム」ではなく、**特定アーティファクト前提の1井定数パッチ**。  
Code Comp の hidden 再実行で sample 行数が変わる／SHA がずれると **RuntimeError** しうる。Public 6.390 が取れているなら、その Version では条件が通った（または同等の固定条件が揃った）と読む。**Private 74% への一般化は期待しない。**

---

## 自チームへの使い方（採用可否）

| 判断 | 内容 |
|---|---|
| Final 枠にそのまま載せる | **不可**（同家系 · 1井 Public パッチ · EDA #8 / checklist VISUALS Stop） |
| tip に Q0522 を移植 | **非推奨**。Public 密な定数シフトは Private shake-up の典型。井 ID 固定は再現も脆い |
| `gs*1.3` | tip に **既実装** → 追加作業なし |
| 学ぶ点 | 「公開最右は **同スタック + 細い Public 介入**」であり、別メカニズムではない |
| checklist | Active 化しない。既存 Stop（pfcfg / Frontier VISUALS 乱獲）を維持。必要なら **intel のみ** |

**数値比較メモ（混同禁止）:**  
作者公開コード Best **6.390** ≠ 自チーム `exp-index` の Public Best（現時点は自提出系）。関係論は [`cv-lb-private-relation.md`](../cv-lb-private-relation.md)（Public≈26%）。

---

## ライセンス

公開 Kaggle Code 慣行 · Tier R → [`license-ledger.md`](../license-ledger.md) **T030**。提出にコードを載せる前に台帳確認。
