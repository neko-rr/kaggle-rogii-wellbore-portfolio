# ROGII Wellbore Geology Prediction — Public Leaderboard 分析

**分析日:** 2026/08/06（追記 · フル統計は 2026/08/05 · 初版 2026/07/23）  
**コンペ:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
**評価指標:** RMSE（低いほど良い）  
**最終提出日:** 2026-08-05（**締切済** · Private 未公開）  
**データソース:**  
- **フル行:** CLI `leaderboard -d` → `docs-en/leaderboard/publicleaderboard-2026-08-05.csv`（**08-06 は zip 0B で失敗** · 再取得せず）  
- **08-06 show:** `docs-en/leaderboard/leaderboard-show-20260806.txt`（上位のみ · 順位公式確定用ではない）  
- 要約 JSON: `docs-en/leaderboard/lb-summary-20260805.json`  
- Top 抜粋: `docs-en/leaderboard/show-top50-20260805.csv` · `show-cli-20260805.txt`  
- 自提出 CLI 覗き: `exp/submissions-cli-20260806-peek.txt`  
- 旧: `publicleaderboard-2026-08-04.csv` · `…2026-07-25.csv`

### 追記（2026-08-06 · show のみ）

| 項目 | 08-05 フル | 08-06 show（抜粋） |
|---|---|---|
| 1位 | 4.608 shu01 | **4.608** 維持 |
| 2–3位 | Yannan 4.902 · N&A 4.908 | **N&A 4.901** · Yannan **4.902** |
| その他 | David 5.133 帯 | David **5.017** 浮上（show） |
| チーム数 / 自順 | 6,140 / **#127 @6.190** | 全件未更新 · **スコア 6.190 のみ確定**（自提出 COMPLETE） |
| Private | 未 | 未 · 一部提出 **PENDING**（Final 不可 · [732947](discussion/732947-final2-requires-public-score.md)） |

※ show の入れ替えを medal 予測や Final 差替根拠にしない。

### 公式 Leaderboard 分割（規定）

> This leaderboard is calculated with approximately **26%** of the test data.  
> The final results will be based on the other **74%**, so the final standings may be different.

本ファイルの数値・順位はすべて **Public（≈26%）**。最終順位は **Private（≈74%）**。関係論: [`cv-lb-private-relation.md`](cv-lb-private-relation.md) · 規定本文: [`conditions.md`](conditions.md)  
コミュニティ終盤議論: [`731550`](discussion/731550-final-two-submissions-shakeup.md) · [`732455`](discussion/732455-leaderboard-thoughts.md)

---

## 要約

- Public LB は **6,140 チーム**（08-04 の 6,118 から +22）。  
- **1位 4.608**（shu01）維持。Top10 圏 **≤5.205**。  
- **密集帯 6.0–6.5 に 1,434 チーム**（前日 1,391 · +43）。公開 fork 追随が続く。  
- **Kazeneko: Public Best 6.190 · 公式 Rank #127**（前日 #122 · **スコア不変** · 密集帯の順位滑りのみ）。  
  現 Public では **Silver 概算帯内**（上位5% 閾値 ≈6.353 / Rank≈307）。最終は **Private**。  
- 上位勢（Tucker/Pavel 等 Discussion）でも **CV 5 前後でも Public は 6 帯ノイズ**と報告。  
  **Public 順位だけを Final2 差替根拠にしない**（Rule `kaggle-public-lb-bias-stop`）。

---

## Leaderboard 概況（2026-08-05）

| 項目 | 値 |
|---|---|
| Teams（Public CSV 行数） | **6,140** |
| 1位 Public | **4.608**（shu01 · sub 21） |
| Top 5 圏 | ≤ **5.078** |
| Top 10 圏 | ≤ **5.205** |
| Top 25 圏 | ≤ **5.570** |
| Top 50 圏 | ≤ **5.865** |
| Top 100 圏 | ≤ **6.104** |
| 中央値（全） | **8.075** |
| 中央値（Score&lt;100） | **7.806** |
| Private | **未公開** |

### メダル閾値（概算 · チーム数 ≥1000 の Featured 慣習）

終了後は **Private** で確定。Kaggle Progression（大規模）の目安:

| 帯 | ルール目安 | 現 Public 換算 Rank ≤ | 現 Public Score ≤ |
|---|---|---|---|
| **Gold** | **上位 10 チーム** | **10** | **5.205** |
| **Silver** | **上位 5%** | **307** | **6.353** |
| **Bronze** | **上位 10%** | **614** | **6.402** |

※ 公式の端数・「+10」等の細則は [Progression](https://www.kaggle.com/progression) を最終確認。

---

## 上位順位とスコア差（Public）

| 順位帯 | Public score | 1位との差 | コメント |
|---|---|---|---|
| 1位 | 4.608 | — | shu01（提出 21） |
| 2位 | 4.902 | +0.294 | Yannan Chen（提出 153） |
| 3位 | 4.908 | +0.300 | N & A & O & A & A（提出 344） |
| Top 5 | 5.078 | +0.470 | Tucker / tremors 同点帯 |
| Top 10 | 5.205 | +0.597 | yu4u |
| Top 25 | 5.570 | +0.962 | |
| **Kazeneko** | **6.190** | **+1.582** | **#127** |
| Silver 概算 | 6.353 | +1.745 | Rank ~307（上位5%） |
| Bronze 概算 | 6.402 | +1.794 | Rank ~614（上位10%） |
| Gold 概算 | 5.205 | +0.597 | Rank ≤10 |

### Top 15（2026-08-05）

| Rank | Score | Team | Submissions |
|---|---|---|---|
| 1 | 4.608 | shu01 | 21 |
| 2 | 4.902 | Yannan Chen | 153 |
| 3 | 4.908 | N & A & O & A & A | 344 |
| 4 | 5.078 | Tucker Arrants | 172 |
| 5 | 5.078 | tremors | 168 |
| 6 | 5.080 | SaintLouis | 268 |
| 7 | 5.081 | Shrey Gandhi | 192 |
| 8 | 5.133 | David Rouyre | 39 |
| 9 | 5.204 | Rishikesh Jani | 156 |
| 10 | 5.205 | yu4u | 88 |
| 11 | 5.308 | L & J & A & A | 428 |
| 12 | 5.315 | Hit Imai | 242 |
| 13 | 5.326 | monkey | 144 |
| 14 | 5.327 | Ryo Takaki | 337 |
| 15 | 5.336 | tennogh | 87 |

### vs 旧スナップショット

| 項目 | 07-23/25 | 08-04 | **08-05** |
|---|---|---|---|
| Teams | ~5.5–5.7k | 6,118 | **6,140** |
| 1位 | 4.859 | 4.608 | **4.608** |
| Top10 | ~5.51 | 5.205 | **5.205** |
| 密集 6.0–6.5 | （当時は 6.5–7.0 最大） | 1,391 | **1,434** |
| Kazeneko | 6.644 #444 級 | 6.190 #122 | **6.190 #127** |

---

## スコア分布（Public · 08-05）

| 帯 (RMSE) | チーム数 | 解釈 |
|---|---|---|
| ≤5.0 | 3 | 先頭わずか |
| 5.0–5.5 | 18 | 賞金・上位争い |
| 5.5–6.0 | 49 | 強い独自系候補帯 |
| **6.0–6.5** | **1,434** | **現・公開スタック密集帯**（Kazeneko 含む） |
| 6.5–7.0 | 509 | 旧密集の残滓 |
| 7.0–8.0 | 1,036 | （7.0–7.5 + 7.5–8.0 合算近似 · 詳細は CSV） |
| 中央値 | 8.075 | |

---

## Public / Private Shake-up

- **安定性:** **低**（Discussion 720701 Chris · Host Working Note · Private outlier 再採点 707695 · **[732455](discussion/732455-leaderboard-thoughts.md)**）  
- **密集帯の意味:** 6.0–6.5 = **clone / tip 過適合の主戦場**（Michael 予測: Private ≈9.5–10 へ crumble）  
- **上位実測（731550 08-05）:** CV を 5 前後まで改善しても Public は 6 帯ノイズ · **0.07 級 LB 差を信じない**  
- **精密 vs バイアス（728477）:** Public ~52 wells は **固定** → 同一スライス比較は高精度 · **絶対 Public ≠ Private 推定**  
- **実験運用の正:** [`cv-lb-private-relation.md`](cv-lb-private-relation.md)

---

## Kazeneko 現在地

> **数値の正:** [`exp/exp-index.md`](../exp/exp-index.md)。本節は LB 文脈メモ。

| 項目 | 値 |
|---|---|
| Team | Kazeneko（`kazeneko77`） |
| Public Best（公式） | **6.190**（farvol · Rank **#127**） |
| 直近診断（枠固定） | 618c **6.231** · 558b **6.238** · 541 **6.256** · tip **6.269** · 641 **6.472 NO-GO** |
| 08-05 CLI | 711 / 710ssot / 702 ほか residual **PENDING**（採点待ち · 個別再提出禁止） |
| Silver 概算帯 | 現 Public では **帯内**（閾値 6.353 / #307） · **Private は別ゲーム** |
| Final 仮 | 枠1=Trust CV · 枠2=farvol（Public1）· SSOT `exp-index` · **提出=ユーザー明示のみ** |

6.0–6.5 密集帯の **上層**。順位 #122→#127 はスコア不変での滑り。**戦略変更の根拠にしない**。

---

## 自チームへの示唆（08-05）

| する | しない |
|---|---|
| Trust CV と L 質を本命 | Public 順位だけで Final2 差替 |
| farvol 枠2 維持 | tip / Hellbore / 空 NB を提出 |
| σ≈0.03 · ≲0.08 で GO 確定しない | PENDING 診断提出の個別リトライ |

詳細 refresh: [`discussion/20260805-refresh.md`](discussion/20260805-refresh.md)
