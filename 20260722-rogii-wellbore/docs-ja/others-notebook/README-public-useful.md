# 公開有用 Notebook 分析 — 索引

> analyzed: 2026-07-23 UTC · **refresh: 2026-08-06（締切翌日）** · **公開最右監視: 継続**  
> 選定方針: **票数ランキングの dual-track クローンを避け**、Discussion / Working Note と整合する **多様性・検証・物理・教育** を優先  
> 生データ: `others-notebook/public-useful/<slug>/`  
> コード抽出: `docs-en/others-notebook/<slug>-Ver-latest.py`  
> スキャン: `docs-en/others-notebook/kernels-*-20260806.txt` · pull `others-notebook/public-useful-refresh-20260806/`  
> 既分析の自提出コピー: [README-kazeneko-v2.md](README-kazeneko-v2.md)（本一覧から除外）

**同家系以外の参考（上流・中間・部分借り）:** [`non-tip-lineage-references.md`](non-tip-lineage-references.md) ← **「無いのか？」への回答**  
**EDA 専用:** [`docs-ja/others-notebook/eda/README.md`](eda/README.md) · [strategy-from-eda](eda/strategy-from-eda.md) · 原文 `others-notebook/eda/` · 日本語注釈 `others-notebook/eda-ja/`  
**2026-07-25 refresh:** [`public-useful-refresh-20260725.md`](public-useful-refresh-20260725.md) · 原文 `others-notebook/public-useful-refresh-20260725/`  
**2026-07-29 診断必読:** [`georgy-noise-floor-lever-Ver.md`](georgy-noise-floor-lever-Ver.md)（無編集再提出 **σ≈0.03** · 提出不可）  
**2026-07-30 監視:** [`blacklions-final-hierarch-Ver.md`](blacklions-final-hierarch-Ver.md)（Q0522 lock + LB座標探索 · Final不可）  
**2026-07-26 公開コード最右:** [`rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md`](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md)（作者 Public **6.390** · **Final採用不可**）  
**Discussion refresh:** **[`../discussion/20260806-refresh.md`](../discussion/20260806-refresh.md)** · [08-05](../discussion/20260805-refresh.md)  
**Public LB:** [`../leaderboard.md`](../leaderboard.md)（**6.190 #127** · 08-05 フル）

### 監視追記（2026-08-06）— 締切翌日 · tip 量産 + CatBoost starter

| 追記 | 内容 |
|---|---|
| **Discussion 6本** | 732999 物理/HMM · 733015 天井 · 732947 Chris Final規則 · 732903 Staff CPU · [20260806-refresh](../discussion/20260806-refresh.md) |
| **Farhan best-score** | 11 profile tip · **捨て** · [分析](farhan-best-score-wellbore-Ver.md) |
| **Raunak Ultra Sub-6** | 1井 shape residual · 票119 · **Final不可** · [分析](raunak-ultra-sub-6-Ver.md) |
| **Sumit ROGIIv2** | koolbox gold · **捨て** · [分析](sumit-rogiiv2-Ver.md) |
| **Ayush Rogii_Ayush** | CatBoost starter · 教育のみ · [分析](ayush-rogii-ayush-Ver.md) |
| 票増加のみ | daniil **229** · Contact+U **93** · physics **724** |

### 監視追記（2026-08-05）— 締切日 · Hellbore 捨て · Anubhav

| 追記 | 内容 |
|---|---|
| **731550** | 終盤: CV 改善でも Public ノイズ · Final2=Trust CV · [要約](../discussion/731550-final-two-submissions-shakeup.md) |
| **Hellbore V.6** | 数式ポエム · 実装なし · **捨て** · [分析](hellbore-v6-Ver.md) |
| **Geologia V92** | pull 結果 **0 bytes** · 空 · 捨て |
| **Anubhav LGBM** | typewell+residual LightGBM starter · tip 外 · Active 不要 · [分析](anubhav-wellbore-lgbm-challenge-Ver.md) |
| tip 看板票 | daniil **199** · Contact+U **90** · AeroRidge **43** · physics v48 再 run |
| **Public LB** | 6,140 teams · 密集 6.0–6.5=**1,434** · Kazeneko **6.190 #127** |

### 監視追記（2026-08-04 eve）— AeroRidge 改題 · LB 6k チーム

| 追記 | 内容 |
|---|---|
| **AeroRidge v34** | タイトル偽装 · 中身=Contact/U · Q2522 Consensus · **Final不可** · [分析](yaroslav-aeroridge-v34-Ver.md) |
| **AkiiroLabs** | koolbox+fleongg PF stack · 票1 · 捨て · [分析](akiirolabs-tvt-Ver.md) |
| **732455** | Tucker: scale-up で gains · tip dense は崩落論維持 · [要約](../discussion/732455-leaderboard-thoughts.md) |
| **Public LB** | 6,118 teams · 密集 **6.0–6.5** · Kazeneko **6.190 #122** |
| Contact+U / daniil | 票 78 / 171（人気化のみ） |

### 監視追記（2026-08-04）— LB thoughts · tip 量産

| 追記 | 内容 |
|---|---|
| **732455** | Public 6.5–7.1 密集=clone 過適合 · shake-up 予測 · [要約](../discussion/732455-leaderboard-thoughts.md) |
| tip 量産 | robust-ensemble-v3 · best-score-roggi · gold-calibra fork · **Final不可** |
| daniil 6.390 | 票 68→145（人気化のみ） |
| 732296 | sample 行数 assert 罠 |

### 監視追記（2026-08-03）— 9h全test · daniil 6.390

| 追記 | 内容 |
|---|---|
| **732422** | Andrey: 9h=Public+Private 全 test · Privateは隠れだけ |
| daniil 6.390 Solution | Q0522/Contact-Gated 看板 · Final不可 · [分析](daniil-solution-6-390-Ver.md) |
| 732432 / 732443 | teammate ban · scoring 8h · 方針無影響 |

### 監視追記（2026-08-02）— Final2 スレ · Contact+U

| 追記 | 内容 |
|---|---|
| **731550** | Final2=Trust CV + Public1（コミュニティ）· 自方針と一致 |
| yaroslav Contact+U | Q0522 + score-space アフィン · Final不可 |
| 732296 / 730983 | Exception · 採点待ち5–7h |

### 監視追記（2026-07-30）— Final Hierarch · Forum静穏

| 追記 | 内容 |
|---|---|
| Discussion 新規 | **なし** |
| blacklions Final Hierarch | Q0522 **6.390 lock** + 井単位 LB 座標探索 · **Final不可** |
| my0705 6.391 | tip クローン改題 · 捨て |

### 監視追記（2026-07-29）— Georgy noise-floor + tip クローン

| 追記 | 内容 |
|---|---|
| Georgy noise-floor | 無編集再提出 **σ≈0.03** · lever 微差を信じない · **S 必読** |
| 728477 追記 | Georgy·souldrive · seed 帯サイズ付け |
| 730092 | format error · ハードパス禁止 |
| blacklions GBDT-gate / 「6.213」/ 6.520 | tip/Q0522 同家系 · Final不可 |

### 監視追記（2026-07-27）— Discussion + DYNQ0196

| 追記 | 内容 |
|---|---|
| 729837 train-copy | hidden に train 重複なし（Tucker）· override は dummy 混同の遺産 |
| 729554 追記 | `sample_submission` 依存は危険 · offset を3井から固定しない |
| prvsiyan Frontier II | **DYNQ0196 +0.196** · DYNQ0130 延長 · **Final不可** |
| タイトル紛らわし | romanrozen「beam-search」= Q0522 メタ · 別経路ではない |

### 監視追記（2026-07-26）— Discussion + Frontier 進化

| 追記 | 内容 |
|---|---|
| 729554 Exception | Submit 失敗ログは3偽井 · hidden≈200 · Final方針変更なし |
| prvsiyan DYNQ0130 | evansussex Q0522 の hidden 追従版 · **Final不可** · Active化しない |

### 監視追記（2026-07-26）— 公開コード Public 最右

| 追記 | 内容 |
|---|---|
| evansussex Frontier VISUALS V1 | 作者 **6.390** · Contact-Gated + `gs*1.3` + **Q0522**（井 `00e12e8b` に +0.522 ft） |
| 判定 | **同家系** · 1井定数パッチは Public 26% 向け · Private/Final 本命にしない · Active CHK 化しない |
| 詳細 | [rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md) |

## 選定（19本）と優先度

| 優先 | slug（作者） | なぜ有用か | 自チームへの使い方 |
|---|---|---|---|
| **S** | `fork-the-ruler-not-the-model`（Georgy） | oracle ladder · leave-field-out · 二峰 · 「モデルを fork するな」 | **必読** · CV/監査 CHK の型 |
| **S** | `what-is-the-precision-of-a-manual-interpretation`（Georgy） | ラベル=人間解釈 · GWC2021 · median 集約 | Final 多様化・hedge 根拠。**LBは上がらない**と明記 |
| **S** | `rogii-wellbore-tvt-physical-model`（Sunny） | 物理 TVT + PF128 · GR補間 · 非tabular 経路 | Discussion 717573 系 · Final 2 の候補 |
| **A** | `rogii-honest-carry-forward-baseline-groupkfold`（n0Rollback） | carry-forward ≫ 軌道 HGB · GroupKFold | ベースライン・否定実験の型 |
| **A** | `rogii-geosteering-for-beginners-7-visuals`（n0Rollback） | png 読み方 · GR↔typewell 直感 | オンボーディング · EDA 起点 |
| **A** | `eda-starter` / `xgb-starter-cv-15`（Chris） | 公式風 EDA · 行寄り XGB（CV~15） | 「tabular だけは天井」の証拠 |
| **A** | `drift-targeting-ncc-tree-based-…`（Mitch） | **drift 目標** · multi-scale NCC · 段階的 writeup | 特徴設計 CHK（LB 8.9 帯・旧世代） |
| **A** | `working-note-target-free-tvt-geosteering` / `rogii-eda-target-free-…`（Pilkwang） | target-free 整合の説明・EDA | heel/整合 B2 の参考（コードは dual-track 近縁） |
| **B** | `rogii-another-approach` / `…-2nd`（Yusuke） | 実験ログ付き · mha 系変種 | 「別アプローチ」名だが **同エコ系** — 差分だけ抽出 |
| **B** | `wellbore-geology-prediction-ridge`（Ravaghi） | artifacts + koolbox の祖先 | 家系の起点理解 |
| **B** | `physics-informed-baseline`（Karnak） | PF×GBM · Optuna PP | 初期物理系（現 Best より劣） |
| **B** | `rogii-geology-aware-ensembling-…`（Roman） | geology gate · fleongg blend | dual-pipeline 近縁 · Private 多様化には弱い |
| **B** | `rogii-pf-contact-gold-calibration-stack` / `experimental-notebook`（FOYSAL） | contact/gold · **実験で LB 悪化も開示** | Working Note 精神 · 盲目採用禁止 |
| **C** | `gr-features-outlier-detection-…`（Mitch） | GR/outlier 姉妹編 | drift 本編とセットで十分 |
| **C** | `rogii-visual-eda-the-evaluation-zone`（n0） | 評価区間 EDA | beginners で足りる場合多 |

## 家系メモ（公開エコシステム）

```
[教育・検証] Georgy ruler / GWC · n0 visuals · Chris EDA/XGB · Mitch NCC writeup
[物理]       Sunny physical · Karnak physics-informed
[公開スタック祖先] Ravaghi ridge/artifacts → Pilkwang dual-track → 大量 fork
[自提出 Ver2] 同一スタックのハイパラ差（既分析）
```

**優秀な Kaggler としての判断:**  
Public 票の多いノートの大半は **同一 dual-track / PF+GBM スタックの再掲**。残り日数では **(1) Georgy の ruler で自 CV を鍛える (2) Sunny 物理や Mitch NCC/drift など未取り込み経路で Final 多様性を取る** のが合理的。同スタックの追スイープは限界効用が薄い。

### スキャウト追記（2026-07-23）

| 追記 | 内容 |
|---|---|
| Yusuke 2nd | 差分は **A31 Mean-Preserving Toe Tilt** のみ → 提出 skip · ablation のみ可 |
| Mitch NCC | Final 多様性有力だが **offline 学習 NB が未同梱**（推論再現のみ） |
| FOYSAL experimental | 実行コードなし · Affine gs / multi-contact は **悪化ログ**（CHK 不要） |
| Pilkwang WN | Ver2 と同家系 → 全文移植せず **contact/gold 概念だけ** CHK 化 |

### refresh（2026-07-25）

| 追記 | 内容 |
|---|---|
| Connor `dz-dtvt-eda` | **S** · 純幾何梯子 · LOO · 幾何天井〜10ft → GR/整合の価値の証拠（提出コードではない） |
| lucifer19 `geoanchor` | **A** · Dual-Champion suffix arbiter · dual-track 同家系 · 概念のみ |
| A016 contact-guard OFF | **A** · ablation · submit-safe · tip の `gs*1.3` は無し |
| tip / ultimate-pf / gs130 | **コード SHA 同一** · `gs*1.3` は tip に既実装 → 728712 は「未移植微調整」ではない |
| pfcfg / VISUALS / shift / MHA | 未 DL（同家系乱獲） |

詳細: [public-useful-refresh-20260725.md](public-useful-refresh-20260725.md)

## 個別要約ファイル

| ファイル | 対象 |
|---|---|
| [public-validation-education-Ver.md](public-validation-education-Ver.md) | Georgy · n0 · Chris |
| [public-physical-alt-Ver.md](public-physical-alt-Ver.md) | Sunny · Karnak · Mitch · Yusuke · Ravaghi · Roman · FOYSAL |
| [public-pilkwang-working-note-Ver.md](public-pilkwang-working-note-Ver.md) | Pilkwang Working Note / EDA |
| [public-useful-refresh-20260725.md](public-useful-refresh-20260725.md) | 2026-07-25 再スキャン総括 |
| [dz-dtvt-eda-Ver-latest.md](dz-dtvt-eda-Ver-latest.md) | Connor 幾何研究ログ |
| [rogii-geoanchor-Ver-latest.md](rogii-geoanchor-Ver-latest.md) | Suffix Arbiter |
| [a016-true-no-contact-guard-ablation-Ver-latest.md](a016-true-no-contact-guard-ablation-Ver-latest.md) | contact guard ablation |
| [rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md) | 公開コード最右 6.390 · Q0522 |
| [prvsiyan-frontier-blend-visuals-dynq0130.md](prvsiyan-frontier-blend-visuals-dynq0130.md) | DYNQ0130 · +0.130 動的 branch |
| [non-tip-lineage-references.md](non-tip-lineage-references.md) | **同家系以外**の上流・中間参考一覧 |

## ライセンス（Tier R）

外部 DS 例: `georgymamarin/geosteering-world-cup-2021-…`（GWC · CC BY 4.0 記載あり）· ravaghi artifacts · koolbox · fleongg · Mitch models DS。  
採用して提出に載せる前に `docs-ja/license-ledger.md` を更新すること。
