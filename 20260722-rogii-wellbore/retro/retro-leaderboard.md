# rogii-wellbore Leaderboard 分析（コンペ全体）

> Skill: `leaderboard-analysis`  
> **分析日:** 2026-08-08（順位確定後 **再取得**）  
> データ: CLI `leaderboard -s`（Private）· `-d`（Public）  
> 生データ: `exp/work/post-comp-lb-20260808/`

---

## 要約

- Private 最終: **6125 teams** · 1位 **Ruby 5.639** · **1000+ バンド** Gold≤**#22** · Silver≤**#306** · Bronze≤**#612**（Progression · floor）。
- Public 1位 **shu01 4.608** と Private 頭 **Ruby** は別人 → **大 shake-up** が確定構造。
- 自チーム **Kazeneko**: Public **#143 / 6.190** → Private **#594 / 9.142**（Δ rank **−451**）。**Bronze**（594≤612 · 銀外）。
- 前回（08-06）比: チーム数 6191→**6125** · 自 Private 順位 596→**594** · スコア **9.142 不変**（採用面 666 のまま）。

---

## Leaderboard 概況（Private · 確定）

| 項目 | 値 |
|---|---|
| Teams | **6125** |
| 1位 | **Ruby · 5.639** |
| 2 | Bilzard · 5.802 |
| 3 | tereka & Takoi · 5.836 |
| 4 | L & J & A & A · 5.870 |
| 5 | daimaru · 5.940 |
| 6 | k256.dev · 5.984 |
| 7 | roglike · 6.057 |
| 8 | 富士山 · 6.180 |
| 9 | tremors · 6.251 |
| 10 | Can · 6.269 |
| #25 | ≈ **6.599**（Tucker Arrants 帯） |
| #50 | ≈ **7.017** |
| #100 | ≈ **7.667** |
| #22（Gold 端 · 10+0.2%） | （上位帯） |
| #306（Silver 端 · 5%） | （概算） |
| #612（Bronze 端 · 10%） | ≈ **9.164** |
| **Kazeneko** | **#594 · 9.142** → **Bronze** |

*Featured 公式は UI 準拠。**N≥1000 では top10%=Bronze**（Gold は 10+0.2% のみ）。0–99 チーム帯の % を転用しない。*

### Public（参考）

| 項目 | 値 |
|---|---|
| 1位 | shu01 **4.608** |
| Top5 | N&A&… 4.901 · Yannan 4.902 · David 5.017 · Tucker 5.078 |
| **Kazeneko** | **#143 · 6.190** |

---

## Public / Private Shake-up

| 観点 | 観察 |
|---|---|
| 頭の一致 | **しない**（Public 覇者と Private 覇者は別） |
| 密集帯 | Public 4.6–6.5 と Private 5.6–7.5 の並びが乖離 |
| 自チーム | #143 → #594 · スコア 6.19→9.14（採用 666 が Public farvol より良い Private） |
| 解釈 | 公開クローン / Pub 最適化は Private で崩落。clean CV と path/PF 系が上位に集中（→ solutions） |

### スコア帯の意味（RMSE 低が良い）

- 上位 1–10: **5.6–6.3**（本体が効いた帯）
- #50–100: **7.0–7.7**  
- #500–600: **~9.1–9.2**（自チーム帯 · tip residual / Pub 最適化の名残）
- 下位: 失敗/timeout 系が極端（最大 score は桁外れ）

---

## 自チーム位置の確定メモ

| | Public | Private |
|---|---|---|
| Score | **6.190**（farvol） | **9.142**（666 · Final 最良） |
| Rank | **#143** / 6125 | **#594** / 6125 |
| vs メダル | — | **Bronze**（Gold≤22 · Silver≤306 · Bronze≤612） |
| 枠2 単独 | farvol Private **9.453** ≒ ~#1300+ 帯 | Trust 枠なしなら大幅悪化 |

詳細: [`retro-private.md`](retro-private.md)

---

## 次回コンペへの示唆

### すぐ試す価値が高い

- Final は **Trust 物差し ×（任意）Public** の分離（本件で順位を守った）
- 終了直後に Private 全取得し、**履歴 privateScore ヒスト**を取る

### 避ける

- Public 頭の単一 Final  
- `leaderboard -d` を Private と誤認  

### 解法側（概要 → solutions 本編）

- 上位: **整列 UNet + PF バンク + 合成 + XY/表面事前** が主戦  
- 詳細: [`retro-solutions.md`](retro-solutions.md)

---

## 出典

| ファイル | 内容 |
|---|---|
| `exp/work/post-comp-lb-20260808/private-leaderboard.csv` | Private 全チーム |
| `exp/work/post-comp-lb-20260808/lb-public/*publicleaderboard*.csv` | Public |
| `exp/work/post-comp-lb-20260808/solution-topics.json` | Discussion writeup 索引 |

**CLI:** Private 表 = `leaderboard -s` · 自提出列 = `submissions`
