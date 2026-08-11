# rogii-wellbore 自チーム Private 振り返り

**分析日:** 2026-08-06  
**参加者:** Kazeneko（teamId **16347969**）  
**コンペ:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
**データソース:** Kaggle CLI 2026-08-08 · `exp/work/post-comp-lb-20260808/`（および初回 `post-comp-lb/`）  
**分析日:** 2026-08-06 · **LB 再確定:** 2026-08-08

---

## 要約

- **Private 最終:** **9.142 · #594 / 6125**（CLI 2026-08-08 · Final2 最良 = **666**）。Public **6.190 · #143** から **約 451 位落下**。
- **枠選択は正当だった:** 枠1 Trust **666（priv 9.142）** ≻ 枠2 Public **farvol（priv 9.453）**。
- **Public Best は Private で弱い:** farvol 単独は大幅悪化帯。
- メダル帯（N=6125 · **1000+**）: Gold ≤**#22** · Silver ≤**#306** · Bronze ≤**#612** → **#594 は Bronze**（top10%≠Gold。公式 UI 確認推奨）。
- 事後最良の未選択面: **702 priv 8.986** · **641 priv 9.101**（Public 悪化帯）。

---

## Private / Public 結果

| 項目 | Public | Private | コメント |
|---|---|---|---|
| **チーム Best（Final 採用）** | **6.190**（farvol） | **9.142**（666） | Private は Final2 の min RMSE |
| **順位** | **#143** / **6125** | **#594** / **6125** | CLI **2026-08-08** |
| 順位変動 | — | **−451** | Public 頭 → Private 中位寄り |
| メダル | — | **Bronze**（#594 ≤ 612） | UI で公式確認 |

**注意:** `leaderboard -d` が落とす zip は **publicleaderboard** のみ。終了後の順位表は **`leaderboard -s` の方が Private**。

---

## 提出枠の振り返り

| 枠 | 選択提出 | Public | Private | 当時の根拠 | 事後評価 |
|---|---|---|---|---|---|
| **1 Trust** | **666** mid+α0.35 residual（ref **55247672**） | 6.509 | **9.142** | residual Trust 頭 · Public は NO-GO 帯でも Trust レーン | **正選択** · Final 採用 · **#594** |
| **2 Public** | **farvol** tip×thin 0.95/0.05（ref **55148128**） | **6.190** | **9.453** | Public Best · 多様性 tipdist_AB 1.95 | **Public 用としては妥当** · Private 単独なら ~#1395 で弱い |

### 枠選択の結論

- **妥当:** 二レーン分離。Private では Trust 枠が勝ち、単一 Public 枠だけなら順位が大きく悪化していた。
- **改善余地（事後）:** 自提出中で Private がさらに良いのは **702（8.986）· 641（9.101）· 710（9.122）**。いずれも Public 6.4–7.4 帯で当時の Public 枠には載せにくく、**Trust 枠を 641/710 に差し替え可能だったか** は当時の dual/残差根拠とトレードオフ。
- **使わなかった Public 近傍:** 618c 9.456 · 558b 9.419 — farvol より更に Private 悪化 or 同程度。枠2 を替える価値は薄かった。

---

## 主要提出の Public → Private

| 面 | ref | Public | Private | Δ(priv−pub) | Private 順位目安* |
|---|---|---:|---:|---:|---:|
| **Final 採用 666** | 55247672 | 6.509 | **9.142** | +2.633 | **#596** |
| Final 枠2 farvol | 55148128 | **6.190** | 9.453 | +3.263 | ~#1395 |
| 641 residual | 55223002 | 6.472 | **9.101** | +2.629 | ~#560 |
| 710ssot residual | 55252402 | 6.613 | 9.122 | +2.509 | ~#581 |
| **702 residual** | 55252403 | 7.394 | **8.986** | +1.592 | ~#498 |
| 660 residual+agree | 55248920 | 6.239 | 9.400 | +3.161 | — |
| 618c | 55222561 | 6.231 | 9.456 | +3.225 | ~#1439 |
| 558b | 55221471 | 6.238 | 9.419 | +3.181 | ~#1061 |
| 711 tip γ | 55251125 | 6.359 | 9.295 | +2.936 | — |

\*自提出 Private を Private LB 全チームと照合した近似順位（同点処理なし）。

### shake-up 解釈

- **自チーム:** Public 好スコア帯（~6.2）の tip/blend 系は Private で **+3 前後**に跳ねる。residual 系は Public 悪化でも Private の悪化幅が相対的に小さい。
- **解釈:** Public≈26% への tip 過適合仮説と整合。Trust residual を枠1に置いた運用は結果で裏付け。
- **全体:** Private 頭は ~5.64（Ruby）。Public 頭 ~4.61 とは順位表が別物。

---

## exp との突合

### 当たっていたこと

1. **Trust ≠ Public レーン分離** — 根拠: Final 採用が 666、farvol 単独なら ~800 位悪化。
2. **residual は Public 禁止・Trust 専用**（641 Public NO-GO）— Private では residual 群が tip 系を上回る。
3. **L retrain dual 全敗**で新 L を Final に載せなかった — スコア未改善のまま締切は合理的。

### 外れていたこと

1. **Public Best = Private の近似** — farvol は Private 中位以下。
2. **「Public 6.19 帯を守れば順位も守れる」** — #144 → #596。
3. **702 の Private 最良**を未認識のまま Final 外 — OOF/Public が悪く当時採用困難だが、Private 順位目安では最上。

### 検証できなかったこと

- 公式メダル表示（**Bronze** 目安 · Progression 表準拠 · UI 最終確認）。
- 上位解法が residual / tip のどちら寄りか → `retro-solutions.md`。

---

## 次コンペへの示唆（このコンペ固有）

1. Final2 は **必ず Trust 物差しの1本を含める**（Public 2本は危険）。
2. Private 公開後は CLI `submissions` の `privateScore` で **全提出ヒストグラム** を即取る（今回 702 がヒスト上最良）。
3. Public 密集帯（~6.2）の薄い勝ちを **Private 保険にしない**。

汎用化: [`retro-lessons.md`](retro-lessons.md)

---

## 未確認・追加で見るべきこと

- [x] Private スコア・順位（CLI）
- [ ] 公式メダル UI 確認
- [ ] LB 全体分布の精読 → `retro-leaderboard.md`
- [ ] 上位解法 → `retro-solutions.md`
