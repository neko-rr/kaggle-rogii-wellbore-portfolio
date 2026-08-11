# 文献・公開データ調査 — rogii-wellbore

> surveyed: 2026-07-23  
> purpose: ネット上の論文・公開データを、本コンペ（TVT RMSE · Notebook · Internet OFF）向けに評価する  
> 英語ソース一覧: [`../docs-en/literature-survey.md`](../docs-en/literature-survey.md)  
> 反映先: `exp/exp-intel.md` · checklist は **仮説化してから** Active へ（本ファイルは intel）

---

## 初学者向け（まずここだけ読めばよい）

### このコンペでやっていること（たとえ）

水平に掘った井戸の途中から先は、「いま地層のどの高さにいるか（**TVT**）」が隠されています。  
手元にある手がかりはだいたい次の2つです。

1. **水平井戸のガンマ線（GR）** … 掘りながら測った「岩石の指紋」の時系列  
2. **Typewell（垂直の参照井戸）の GR** … 「地層の見本帳」

やることは、**見本帳と指紋をずらしながら重ねて、「ここが何フィート目か」を当てる**イメージです。  
採点は当てた TVT と正解の差の二乗平均（**RMSE**）。小さいほど良いです。

### 論文が言っていること（かんたん訳）

| 論文のキーワード | かんたん訳 | このコンペでは？ |
|---|---|---|
| **Particle Filter（粒子フィルタ）** | 「いまの位置候補」をたくさん持っておき、GR が合う候補を残す・増やす | すでに上位ノートでよく使われている。**正しい方向** |
| **Bayesian / 多峰** | 答えが1つに決まらない（上に15ft・下に15ftなど）ことがある | **真ん中を取る・両方混ぜる（hedge）**が RMSE に効きやすい |
| **DTW** | 波形を伸ばしたり縮めたりして無理やり合わせる | **何も制約なしだと失敗しやすい**。既に分かっている区間（heel）を固定してから使うなら検討可 |
| **強化学習（RL）** | 「どっちに曲がって掘るか」を学習する | コンペは「掘る方向」ではなく **TVT の数値当て** → **ほとんど使わない** |
| **有料の地質データベース** | お金を払う地下データ | Rules 上あぶない · Host も未回答 → **使わない** |

### 覚えておく結論（3行）

1. 専門家も「**GR と Typewell を確率的に合わせる**」のが本命、と言っている。  
2. だから **いま使っている tip / PF 系は筋が良い**。論文を読んで新アーキを一から作る必要は薄い。  
3. **別の油田の公開ログを学習に足す・有料DB・RL本命**は、今はやらない。

### 用語ミニ辞書

| 用語 | 意味 |
|---|---|
| GR | Gamma Ray。自然放射能の強さ。頁岩は高く、きれいな砂は低いことが多い |
| Typewell | 近くの垂直井戸の「お手本ログ」 |
| TVT | 地層の柱の上での位置（深さの一種）。このコンペの答え |
| heel | 井戸の序盤で、答え（TVT）がまだ分かっている区間 |
| RMSE | 予測と正解のズレの大きさ（小さいほど良い） |

---

## 要約（優秀な Kaggler としての結論）

1. **学術の本流は「GR ↔ type/offset log を確率的に合わせ、層位置（境界距離 / TST / TVT 相当）を推定する」**であり、公開 dual-track（PF + beam + hedge）と一致する。論文は **方針の正当性**を補強するが、Kaggle の即効スコア源にはなりにくい。
2. **RL / 掘進意思決定**論文は多いが、本コンペの評価は **解釈 TVT の RMSE**であり、舵取り最適化そのものではない → **直接移植は低優先**（PF 部分だけが有用）。
3. **使える公開データ**は、ほぼ **Geosteering World Cup 系（ラベル雑音・専門家分散）**。**有料地下 DB・他盆地 well log を学習に混ぜるのは Rules / ドメインずれリスク大**（Host 未回答の有料 DB は引き続き禁止）。
4. 自チームへの最短接続: 既存 CHK（ruler · heel 校正 · 二峰 hedge · 物理 PF · 近傍）を論文語彙で裏打ちし、**新しい Active CHK は「制約付き DTW / 多峰 posterior の明示」程度に限定**。

---

## コンペとの対応表（必須）

| コンペ要素 | 論文・手法の対応 | 採用判断 |
|---|---|---|
| 予測対象 TVT（層内位置） | PF / Bayesian の境界距離・TST / RSD 推定 | **高**（既に公開 NB 実装あり） |
| Typewell GR | offset / type log matching | **高** |
| RMSE | 単一 MAP より **事後分布の中点・hedge** が有利な場合あり | **高**（二峰 Discussion と一致） |
| 行単位 tabular | 文献でも「ログをそのまま回帰」より系列整合が主 | **本命にしない**（既存 Stop） |
| RL で舵を切る | reservoir contact 最大化 | **低**（評価とタスク不一致） |
| 3D 地震・有料 DB | 構造モデル更新 | **禁止/保留**（Rules · Host 未回答） |

---

## 論文・手法カード

### P1 — Particle Filter + GR（最重要クラス）

| 項目 | 内容 |
|---|---|
| 代表 | Akkam Veettil & Clark, *Bayesian Geosteering Using Sequential Monte Carlo* (SPWLA 2020) · Alyaev 系 RL+PF (arXiv:2402.06377, Comp. Geosci. 2025) · SPE/ICCS 系 Dual-DRL+PF |
| 手法 | 粒子で「層境界位置 / オフセット」を保持。観測 GR と **参照 type log をシフト合わせた予測 GR** の尤度で重み更新。非線形・多峰に強い（Kalman より適） |
| コンペ効用 | Sunny 物理 PF・公開 dual-track の Track B と **同族**。論文は「単一点推定より分布」を強調 → **lik-weighted ensemble / 複数 seed** の根拠 |
| 自チーム | CHK-030（物理 PF）・既存 PF の **尤度スケール・init_spread・GR 補間**を自 CV で触る。**新規アーキより校正** |
| 優先 | **高（概念）** / 実装は既にあるので **中（新規コード）** |

### P2 — 多峰・曖昧解釈（Viterbi / Bayesian state space）

| 項目 | 内容 |
|---|---|
| 代表 | SPE-212544（Bayesian state space + Viterbi · ノイズと解釈曖昧性） |
| 手法 | 単一最適相関ではなく **状態空間の尤度行列 + 遷移**から最尤経路。合成試験で距離誤差を報告 |
| コンペ効用 | Discussion の **±15 ft 二峰**・beam/selector と整合。RMSE では **中点 hedge** が有利（既知） |
| 自チーム | CHK-023（bimodal hedge 自CV）。単一モード強制を避ける（Stop 済み） |
| 優先 | **高** |

### P3 — DTW / ログ自動相関（制約付き）

| 項目 | 内容 |
|---|---|
| 代表 | Samant et al. 2025（DTW + stratigraphic constraints, AGU）· IDTW / semblance（Interpretation 2021）· MDPI 2025 geology-informed DL correlation |
| 手法 | 生 DTW は波形差で破綻しやすい。**tie points（マーカー）・沈降速度窓・step pattern**で地質制約を入れる |
| コンペ効用 | Host/Discussion は **素朴 DTW 単体に否定的**。**heel 既知区間を anchor にした制約 DTW / NCC**は B2 に接続可 |
| 自チーム | Active に載せるなら「heel 固定 + 窓付き DTW/NCC が CF を超えるか」1 CHK。**無制約 DTW は Stop** |
| 優先 | **中**（制約付きのみ） |

### P4 — ログ整合 + 3D horizon（参考）

| 項目 | 内容 |
|---|---|
| 代表 | Geosciences 2024（PF log interpretation + 3D horizon tracking） |
| 手法 | PF で RSD/TST 等を推定し、地震由来境界と融合 |
| コンペ効用 | **地震ボリュームは公式データに無い**。手順のうち **DTW で affine 校正 → PF** だけが移植候補 |
| 優先 | **低〜中**（校正手順のみ） |

### P5 — RL / DISTINGUISH / GAN 地質生成

| 項目 | 内容 |
|---|---|
| 代表 | DISTINGUISH（arXiv:2503.08509）· Decision-Driven Geosteering（arXiv:2606.17331）· GAN-geosteering（github.com/geosteering-no） |
| 手法 | 不確実地質を生成モデルで表現し、掘進意思決定を最適化 |
| コンペ効用 | **舵取り報酬 ≠ TVT RMSE**。学習コスト・Internet OFF・時間制約と相性が悪い |
| 優先 | **低**（読んでも提出本流にしない） |

### P6 — GR→距離制約で表面モデル更新（SPE-227995 等）

| 項目 | 内容 |
|---|---|
| 手法 | GR をゾーン上下面までの距離制約に変換し、アンサンブル表面を更新。非層準ノイズ区間を RF で除外 |
| コンペ効用 | 「悪い GR 区間をマッチから外す」は有用。全面モデル更新はデータ不足 |
| 優先 | **中（GR 区間フィルタの発想のみ）** |

---

## 公開データカード（Rules 観点）

| ID | データ | 入手 | ライセンス目安 | 学習に混ぜる？ | 使い方 |
|---|---|---|---|---|---|
| D1 | **GWC 2021 interpretations**（~10k） | [Zenodo 15190744](https://zenodo.org/records/15190744) · [GitHub geosteering-no/…](https://github.com/geosteering-no/10000-geosteering-interpretations-and-decisions) | オープン（論文・リポジトリ記載を確認） | **否**（別シミュレーション） | 人間解釈のばらつき · **median vs mean**（Georgy NB と同系） |
| D2 | **GWC 2020 typelog**（正規化 GR） | [DataverseNO 10.18710/20VIVT](https://dataverse.no/dataset.xhtml?persistentId=doi:10.18710/20VIVT) | DataverseNO 利用規約 | **否**（合成 typelog） | PF/RL 論文の再現実験用 |
| D3 | Georgy tidy GWC on Kaggle | `georgymamarin/geosteering-world-cup-2021-…` | CC BY 4.0（NB 記載） | **否** | 既分析済み · ledger T015 |
| D4 | Teapot Dome / Geolink / Taranaki well logs | Zenodo imputation benchmark 等 | CC / NOLD 等 | **原則否** | 盆地・サンプリングが違い、TVT タスクに直結しない。研究用のみ |
| D5 | USGS Texas historical logs | USGS data release | パブリックドメイン系 | **否** | スキャン PDF 中心 · 本コンペ非適合 |
| D6 | 有料 Enverus / IHS 等 | 商用 | — | **禁止** | Host 未回答（728022） |

**Rules 再確認:** External Data は全員が無償同等アクセス、または Reasonableness。有料・地理制限は失格リスク。**Competition Data の再配布禁止**は別問題（自 `dataset/` は Git に載せない）。

---

## コミュニティ実装（論文ではないが同ドメイン）

| 名前 | URL | メモ |
|---|---|---|
| mycarta / rogii-geosteering-toolkit | [GitHub](https://github.com/mycarta/rogii-geosteering-toolkit) | **本コンペ向け** · 方位 StratifiedGroupKFold · multi-scale NCC · offset prior。**ライセンス確認のうえ**概念参照（丸写し提出は独自性・Tier 注意） |
| tom99763 / rogii-viewer | [GitHub](https://github.com/tom99763/rogii-viewer) | 予測 CSV の per-well RMSE 可視化 · デバッグ用 |
| geosteering-no org | [GitHub](https://github.com/geosteering-no) | NORCE 公開コード · GAN / GWC データ |

---

## 自チームへのアクション（CHK との接続）

| 優先 | アクション | 既存 CHK / Bet | 実施状況（2026-07-23） |
|---|---|---|---|
| 1 | PF は「点推定」より **事後・多 seed 加重**を自 CV で固定 | CHK-010 · CHK-030b | **裏打ち済** · 030b Final2 |
| 2 | 二峰 / Viterbi 的曖昧性 → **midpoint hedge** を自 CV | CHK-023 → **CHK-041** | 023 退化 rejected · **041 Active 追加** |
| 3 | DTW は **heel anchor + 窓**のみ試す（素朴 DTW 禁止） | **CHK-040** | **Active 追加**（無制約は Stop） |
| 4 | GWC は **学習特徴に混ぜない** · Final blend の median 根拠 | CHK-032 | 高相関で rejected · 方針は維持 |
| 5 | 他盆地公開 well log・有料 DB は **使わない** | Stop | 維持 |
| 6 | mycarta の **方位 Stratified GroupKFold / NCC** は B1・031 と突合 | CHK-020 · CHK-031 | 020 in-progress · 031 は 040 と排他 |

**文献由来の接続（2026-07-27 更新）:** 初期の CHK-040/041 は閉鎖済。Wave-21 では **CHK-246–255** が EDA×文献×現場の上流/中間仮説（詳細は [`exp/experiment-checklist.md`](../exp/experiment-checklist.md)）。

---

## 効きそう / 効かなさそう

### 効きそう（論文×コンペ）

- GR–type log の **確率的マッチ（PF / Bayesian）**
- **多峰を潰さない**（hedge · median ensemble）
- **heel / 既知区間で校正**してからマッチ
- 近傍構造の利用（論文の offset well · コンペの &lt;150 ft）

### 効かなさそう / 危険

- RL で「掘る方向」を学習して RMSE を狙う
- 無制約 DTW を全面採用
- 他油田の公開ログで転移学習（分布ずれ · Rules 説明コスト）
- 有料 DB・地震ボリューム前提の手法

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-07-27 | EDA/文献/現場 → checklist **CHK-246–255**（候補二峰 · Buda lik · jitter · 扇状 · ESS · TST診断等）。新規 Active は上流/中間のみ · FINAL hedge 再開なし |
| 2026-07-23 | Web 調査初版 · 論文6系統 + 公開データ6 + コミュニティ3 · Rules 付き採用判定 |
