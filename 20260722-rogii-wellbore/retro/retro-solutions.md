# rogii-wellbore 上位解法 統合分析

**分析日:** 2026-08-10（**新規 writeup · Host recap を追記**）  
**前回:** 2026-08-08（Top1–7 + 公開コード） · 2026-08-06  
**Skill:** `solution-analysis`  
**関連:** [`retro-private.md`](retro-private.md) · [`retro-leaderboard.md`](retro-leaderboard.md)  
**原文:** [`docs-en/solution/`](../docs-en/solution/)（CLI **2026-08-10** 含む）  
**Discussion 差分:** [`docs-ja/discussion/20260810-refresh.md`](../docs-ja/discussion/20260810-refresh.md)

---

## 結論（更新）

1. **Private 上位の勝ち筋は「行回帰」ではなく次の三本柱:**  
   **(A) 2D 整列 / path 表現（UNet · registration / RAFT）** · **(B) Particle Filter / HMM の多様バンク** · **(C) 物理的に整合した合成データ**。
2. **#1–5 はすべて「曖昧な GR マッチ＝多峰パス」を正面から扱い、単一スカラー回帰に戻らない。**
3. **Public を信じて neighbor / 強い地形を切り捨てたチームと、CV を信じて押し通したチームが上位に並ぶ。** 1位は XY-neighbor で **Pub 悪化・CV 改善 → CV を採用**。**#20 は Pub と Priv が反相関すら示した。**
4. 自チーム差分の本質は変わらず: **lane 分離は正解だが、主戦場は tip residual ではなく path+PF+synth 本体**。
5. **08-10 追加:** silver 帯に **estimator 三重スタック（#17）** · **無相関 multi-path（#20）** · **fold-safe geology delta（3581→429）** が新しく公開。Host 内部 RMSE **≈8.0**。

**転用時の切り分け（必須）:**  
- **物差し（CV / Final / レーン）** → [`retro-lessons.md`](retro-lessons.md) の **### A**  
- **作り込み（path / PF / synth / gate）** → 同 **### B**  
- 混ぜて「U-Net したのに採点は tip dual」みたいな不一致を繰り返さない。

**必読 writeup（高票 · Top 順位）:**  
1st [733220](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) **votes160** · 2nd [733432](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733432) · 3rd [733319](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733319) · 4th [733480](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733480) · 5th [733522](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733522) · 6th [733226](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733226)

**08-10 必読（新規）:**  
17th [733860](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733860) · 20th/Pub3 [733845](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733845) · 25th [733598](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733598) · shake [733895](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733895) · Host wrap [733341](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733341)

---

## Private Top × 解法リンク（2026-08-08 LB · 08-10 で writeup 行を拡張）

| # | Team | Priv | Writeup（Discussion） | 一言 |
|---:|---|---:|---|---|
| 1 | **Ruby** | **5.639** | [733220](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) votes**149** | ConvNeXt U-Net 整列 + PF/XY ch · CE path · **CV で XY 採用** |
| 2 | **Bilzard** | 5.802 | [733432](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733432) | **P(dTVT\|TVT)** AnchorCNN + DP 復号 · 生成合成 |
| 3 | **tereka & Takoi** | 5.836 | [733319](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733319) | HMM+PF+2NN+SDF → **SoftMax Gate** · fold-safe 25ckpt |
| 4 | **L & J & A & A** | 5.870 | [733480](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733480) | 地形 tabular + vision offsets · UNet · PF · OOF ridge |
| 5 | **daimaru** | 5.940 | [733522](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733522) | Synth **25ep** → real **2ep** · TVT×MD CNN · 潜伏地質 GR |
| 6 | **k256.dev** | 5.984 | [733226](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733226) | **91 PF** を NN が row-level bag · Pub20→Priv6 |
| 7 | roglike | 6.057 | [733154](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733154) | HMM + 捏造 first-pass refine |
| 8 | 富士山 | 6.180 | [733281](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733281) 等 | PF ranker + synth U-Net（8th 系） |
| 9 | tremors | 6.251 | [733150](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733150) | AR + dual UNet + banded stack |
| 10 | Can | 6.269 | [733315](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733315) | 10th Compass（追記可） |
| **17** | Falcon | **6.376** | [733860](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733860) **new** | GBDT+slope CNN+seg error · **難易度帯 CV** |
| ≈20 | Yannan Chen | （Pub 強 / Priv gold 帯） | [733845](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733845) **new** | **RAFT grtx** + PF residual + geo · **無相関 blend** |
| 25 | Jin Niu | 6.599 | [733598](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733598) **new** | 66 cand soft path + multi-scale residual |
| 35 | pay | 6.826 | [733326](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733326) | HRNet matching map · CV≈Pub≈Priv |
| 429 | matcha110 | **8.861** | [733895](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733895) **new** | Pub 3581→Priv 429 · fold-safe delta |

高票だが順位がやや下: Tucker **26** [733136](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733136)（votes 73+）· YOLO agent 系 [733181](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) など。

---

## 解法比較表（#1–7 中心）

| Rank | Team | Priv/Pub | 表現 | 物理/候補 | 神経 | 合成 | 選択哲学 |
|---:|---|---|---|---|---|---|---|
| 1 | Ruby | 5.639 / ~6 | 2D 整列 U-Net CE | PF heatmap ch · **XY neighbor** | ConvNeXt-S U-Net | Z-shift / GR affine 等 | **CV>Pub**（XY は Pub 悪化） |
| 2 | Bilzard | 5.802 | 条件付き **P(dTVT\|TVT)** | identity dTVT=dz_layer−dz · DP 復号 | AnchorCNN | レイヤーケーキ生成 + residual bank | multi-modal 回避（点回帰禁止） |
| 3 | tereka | 5.836 / 6.043 | 5候補 + gate | HMM · PF | Last-PS NN · Delta NN · 1D SDF | — | **fold-safe** · SoftMax gate · 5×5 splits |
| 4 | LJA A | 5.870 / 5.452 | 画像 offsets · path | 地形 slope · PF | ConvNeXt V2 + Squeezeformer | 二段 synth → real | OOF ridge ensemble · 一部 Priv 弱脚も保持 |
| 5 | daimaru | 5.940 | TVT×MD 画像 | （PF 途中廃止） | multi-backbone CNN | **潜伏地質** 合成に全振り | CV 信頼＝synth 忠実性 |
| 6 | k256 | 5.984 / 5.626 | 91ch PF features | 大量 PF 設定 | row-level NN bag | — | PF を「特徴量工場」に |
| 7 | roglike | 6.057 | HMM path + refine | HMM | UNet refiner | 壊 first-pass 合成 | Pub 定規は Local に逆転 |

---

## 共通する勝ち筋（確定版・2026-08-08）

### A. 問題の立て方

| パターン | 内容 | 代表 |
|---|---|---|
| **Alignment / path** | 候補 TVT × MD の分布 or 確率マップ · CE+soft decode | 1,2,5,7,9 |
| **生成過程 identity** | dTVT = Δsurface − dZ。Z 既知 → 推定は平滑な surface | 2,4,3 の一部 |
| **多峰性を認め複候補** | 単点回帰の mode 平均を拒否 · PF/HMM バンク | 2,3,6,8 |
| **候補の動的融合** | SoftMax gate / NN row bag / ridge OOF | 3,6,4 |

### B. データ

| パターン | 内容 | 代表 |
|---|---|---|
| **合成 pretrain** | real 短 finetune · 本物過剰コピー禁止 | 1,2,5,26,7 |
| **合成の忠実性＝CV の信頼** | latent geology · residual bank · 物理 consistent z | 2,5 |
| **XY/近傍井戸** | 効くが Pub と戦う · CV 重視で残す or 品質ゲート | 1,4 |

### C. 検証・提出

| パターン | 内容 |
|---|---|
| GroupKFold by well · shippable OOF | 全員 |
| fold-safe / nested（gate・中間特徴リーク禁止） | 3 が最明示 |
| **Public 逆転を無視して CV を正とする** | 1（XY）· 7（local vs pub 順序）· 6 の shake-up 生存 |
| Pub 密集 clone を Final 主にしない | 全体 LB と反例 writeup |

### D. 前回（08-06）から追加で固まった点

1. **#1 は UNet 単独ではなく PF+XY チャンネルの複合**（PF 単独 CV~7.4）。  
2. **#2 の核心は確率的 path model + 物理整合合成**（単純 UNet コピーではない）。  
3. **#3 は「物理候補 × 異なる誤差の NN × ゲート」**が公式パターン化。  
4. **#6 は深層本家ではなく「PF 多様性 × 行融合」**でも gold 圏 — bank の幅が本体になりうる。  
5. 高票 26th Tucker の **cost volume + stacked UNet + synth** は依然重要教科書だが、**#1–6 はさらに PF 多様化と生成モデルを上乗せ**。

---

## 自チーム（Kazeneko #594 / 9.142）との差分（更新）

| 観点 | 上位 #1–6 | 自チーム |
|---|---|---|
| 主表現 | 整列確率・条件移動・PF バンク | tip 系 + mid residual α |
| 候補数 | 5–91 本を融合 | 実質 2 枠（666 / farvol） |
| 合成 | 主戦 pretrain | 本線なし |
| PF | 上位の多くで必須/特徴 | 非中核 |
| CV | 出荷本体の fold-safe OOF | tip-cv / residual dual |
| Final | 多くが CV 主（一部 Pub 監視） | Trust+Public 二レーン（枠は正解） |
| 到達 | Priv 5.6–6.0 | Priv **9.14** |

**当たった:** Trust≠Public · residual を Public 主にしない · farvol 単独より 666 採用。  
**足りなかった:** (1) path UNet 本体 (2) PF 多様バンク (3) 物理整合合成 (4) fold-safe ゲートまでの階層。

---

## 実験ロードマップ（更新）

| 優先 | 実験 | 期待 | コスト | 根拠 |
|---|---|---|---|---|
| **高** | cost-volume / alignment U-Net（CE path） | 大 | GPU | 1,5,9,26 |
| **高** | multi-PF バンク + ranker/row NN bag | 大 | CPU/GPU | 6,8,3 |
| **高** | 物理整合 synthetic → short real FT | 大 | 生成 | 2,5,1 |
| **高** | 候補 SoftMax/gate · fold-safe OOF | 中–大 | 中 | 3 |
| **高** | Final 選択を strict OOF 優先 | 順位 | 低 | 1,7,LB |
| 中 | XY/表面 prior（品質ゲート + CV 正） | 中 | 中 | 1,4 |
| 中 | 捏造 first-pass refine | 中 | 中 | 7 |
| 中 | 帯別 / specialist blend | 小–中 | 中 | 9 |
| 避 | Pub ノート重み最適化 alone | 悪化 | 低 | 733149 等 |
| 避 | tip 上 weight/loss 一機構だけ | 本戦外れ | 中 | 自 F044–045 |

---

## 個別メモ（新規 Top）

### 1st Ruby · 2D alignment ConvNeXt（[733220](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220)）

- Grid: 水平 345pos · typewell ±100ft@0.5ft · **CE + Huber path + 弱 GR penalty**。  
- Backbone: **ConvNeXt small** · LN→BN · BF16。  
- PF ch（standalone ~7.4）· **XY 線形表面 prior（~11.4）** · Pub は XY 有害 → **CV +0.3 を信じ残す**。  
- Ensemble 重みで XY 有無を分岐 · final **CV 4.627 / Priv 5.639**。

### 2nd Bilzard · AnchorCNN P(dTVT|TVT)（[733432](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733432)）

- 多峰マッチ → **回帰は mode 平均に潰れる**と診断。  
- 条件分布を並べ **DP で厳密に path 復号**。  
- 合成: master typewell 系 + 軌跡 mixup + residual bank · **z_layer で identity 保存**。  
- Pub 停滞でも **締切3h前まで学習**して Private 2位。

### 3rd tereka · 5候補 SoftMax Gate（[733319](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733319)）

- HMM 5.97 · PF 6.58 · Last-PS NN 5.47 · Delta NN 5.77 · SDF 9.54（単独弱）→ gate で **CV 5.29 / Priv 5.836**。  
- **fold-safe**: 中間特徴・ゲートも fold 内閉じ。  
- 5 分割パターン ×5 = **25 ckpt/ family**。

### 4th L&J&A&A · 三系統 ensemble（[733480](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733480)）

- James 地形→画像→**8 制御点オフセット**（主力 0.64）· Lightsource UNet（0.33, Priv 弱）· PF（0.03）。  
- OOF ridge · 一部弱脚も含め安定。  
- 強い地形は CV≫Pub のリスク → vision との組み合わせ慎重。

### 5th daimaru · synth 忠実性（[733522](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733522)）

- PF は途中まで · 最終は **latent geology 合成 + CNN 画像**に集中。  
- 「synth を良くする＝CV が信じられる」。  
- pretrain ~25 / finetune ~2。

### 6th k256 · 91 PF bag（[733226](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733226)）

- Pub 20 → Priv 6 大上昇。  
- 公開 NB の PF 未チューニングを指摘し **多様 PF + 行 NN 融合**。  
- 深層一本勝負ではない gold。

### 反例・学び系（高信号）

| Topic | 学び |
|---|---|
| 733153 Pub計器 | n_eff≈well · Pub 定数スタック崩壊 |
| 733149 | w_pub↑ → Pub↑ · CV/Priv↓ |
| 733282 | 35提出 corr(pub,priv)≈−0.04 |
| 733307 48→407 | 失敗回顧 |
| 733341 Host | Host 内部 **RMSE≈8.0** · 現場は trajectory+GR が主 |
| 733595 Staff | N=6125 · 161k 提出 · 失格整理済 |

---

## 08-10 追記メモ（新規 writeup）

### 17th Falcon · estimator 三重（[733860](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733860)）

- 最終: **Model1** GBDT（last_known 相対・264 非学習特徴）+ **Model2** slope CNN 積分（EfficientNet-B0 帯）+ **Model3** 600ft セグメント系統誤差 LGBM。  
- Priv **6.376** / Pub 5.853。PF only CV 11 → 三段で 6.32。  
- **井難易度4帯**（naive PF RMSE）で実験採否。総合 RMSE 単独は **catastrophic 少数が支配** → 「normal 帯を上げる」を必須条件に。  
- AI agent 共同: 実装は agent · **方向クローズ禁止は human**。  
- 日本語: [`docs-ja/discussion/733860-17th-place-solution.md`](../docs-ja/discussion/733860-17th-place-solution.md)

### 20th · Public 3rd Yannan · RAFT grtx（[733845](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733845)）

- **grtx**: shared stem + Transformer + cost volume CE + **1D-RAFT** 反復。sinh 状態グリッド。  
- 3 path: grtx · **GPU PF residual**（pfnet/pftree）· **geo**（ancc + geotx）。固定重み + 距離減衰。  
- **選択壁:** per-well ゲートは CV 良く LB 死。  
- Pub ≈50 井 **σ≈0.9** · 著者表で **corr(Pub,Priv) が負** · Final は **CV 優先 ensemble**。  
- データエンジン: anchor slide · whip/layer synth · forward GR sim。見た目リアル synth ≠ 良い CV。  
- 日本語: [`docs-ja/discussion/733845-20th-raft-grtx-matcher.md`](../docs-ja/discussion/733845-20th-raft-grtx-matcher.md)

### 25th Jin Niu · 66候補 path ensemble（[733598](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733598)）

- Physics は **候補・制約生成**、学習が **信頼度・soft 融合**。Priv **6.599** / Pub 6.420。  
- 66 cand → CRF/forward-backward 周辺 · TCN 位相 · bi-dir GR · LightGBM residual · geometry PF。  
- 固定 base 重み + multi-scale residual。#3 soft gate / #6 bag と同型の「候補工場」。

### 429 · 3581→429 fold-safe delta（[733895](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733895)）

- Pub **10.021 (#3581)** → Priv **8.861 (#429)**。  
- 終盤は **公開 NB 追従停止**。v16: **EGFDU anchor-delta** · 同一 fold 参照禁止 · 距離加重 · 格子重みのみ。  
- absolute 近傍コピー禁止。Pub 悪化でも OOF 改善を信じた。  
- 日本語: [`docs-ja/discussion/733895-3581-to-429-shakeup.md`](../docs-ja/discussion/733895-3581-to-429-shakeup.md)

### 自チーム比較への追加

| 観点 | 08-10 新規 | 自 #594 |
|---|---|---|
| registration/RAFT | #20 主軸 | なし |
| estimator 三重 + 難易度帯 | #17 | hard pack はあるが final 主戦場にならなかった |
| fold-safe 近傍 delta | #429 medal 帯 | farvol 系は薄い空間補正 |
| Pub 反相関の数値証拠 | #20 明示 | Rule 一般論のみ |

---

## 再現性

| 帯 | 再現難度 | メモ |
|---|---|---|
| #1–2 | 高 | 大 code + synth + 多シード |
| #3–6 | 中–高 | PF 多数 or ゲート · 記述豊富 |
| #7–26 | 中 | writeup が教科書級 |
| 純 physics DP | 中 | Ayo 75 等 · 天井あり |

---

## コード公開分（2026-08-08 pull + コード要約）

> 在庫: [`docs-ja/solution/code-inventory.md`](../docs-ja/solution/code-inventory.md)  
> **weights / コンペ DS は未 DL**（推論 notebook · train repo · script のみ）

| Place | Team | 公開物 | コード要約 | ローカル |
|---:|---|---|---|---|
| **1** | Ruby | Infer NB `w5833946/submit-reproduce` · 学習は 7 weight DS | [code-rank01-ruby](../docs-ja/solution/code-rank01-ruby.md) | `retro/archive/others-notebook/post-comp-top-20260808/rank01-…` |
| 2–5 | — | **フル訓練コード未公開**（writeup のみ） | — | — |
| **6** | k256 | 巨大 Infer NB + artifact DS 前提 · GitHub later | [code-rank06-k256](../docs-ja/solution/code-rank06-k256.md) | `…/rank06-k256net-…` |
| **14** | keithtyser | **GitHub 学習一式** + Construction A submit | [code-rank14-keith](../docs-ja/solution/code-rank14-keith.md) | `retro/archive/solutions/code/…` · `…/rank14-keithtyser-…` |
| **23** | jiweiliu | self-contained infer script ~3k 行 | [code-rank23-jiwei](../docs-ja/solution/code-rank23-jiwei.md) | `…/rank23-jiweiliu-…` |

### コードから補強された勝ち筋

1. **#1**: 井単位 **XY-safe 閾値**（5 指標 AND）で `xy_based` / `GR_only` の bag をハード切替。  
2. **#6**: `%%writefile` 18 本 · PF banks × row NN · GR-free anchor 並列 · `SUBMIT_MODE` A/B。  
3. **#14**: `U-Net bank` → XGB margin → **well gate** → 固定係数の **(W96−W48)** · W64 seed 方向。receipt 絶対主義。  
4. **#23**: writeup 三段が関数名に直結（`AlignmentUNet` · `c016_*` residual · `run4_select_route`）。

### 自チームへ（コード読了後）

| 公開コードにあった | 自チームに無かった / 弱かった |
|---|---|
| multi-ckpt · 条件 bag · direction stack | tip residual 主軸 |
| path U-Net / PF bank 工場 | PF を副次・中断 |
| fold 固定係数・seed roster | 実験スイープ中心 |
| Infer 領収書化（hardcode weights） | 運用資産化不足 |

---

## 未確認

- [ ] formal `/writeups/` の追加有無（2026-08-10 時点 Discussion のみ）  
- [x] 公開コードのコード級要約（#1 · #6 · #14 · #23）  
- [x] 08-10 新規 writeup（17 · 20 · 25 · 429 · Host/Staff）  
- [ ] weight / artifact dataset の pull（ユーザー許可後）  
- [ ] #2–5 · #6 GitHub の後追い公開チェック  
- [ ] #20 / #17 公開コードの有無再スキャン  

---

## 出典

| 用途 | パス |
|---|---|
| LB 確定 | `exp/work/post-comp-lb-20260808/private-leaderboard.csv` |
| トピック一覧 08-08 | `.../solution-topics.json` |
| トピック一覧 08-10 | `docs-en/discussion/topics-*-20260810.csv` |
| 本文 | `docs-en/solution/topic-*.txt` · `exp/work/post-comp-lb-20260810/solution-bodies/` |
| **公開コード（終了後）** | `retro/archive/others-notebook/post-comp-top-20260808/` · `retro/archive/solutions/code/` |
| **コード要約** | `docs-ja/solution/code-*.md` |
| Discussion 差分 | `docs-ja/discussion/20260810-refresh.md` |
| 自チーム | `retro-private.md` |
