# CHK-FINAL-T2 all773 — Trust A/B/C/D 分析（優秀 Kaggler 視点）

> **date:** 2026-08-05  
> **lane:** Trust CV · full train allowlist **773** · **提出禁止**  
> **run:** `20260804-115307` · faces: [`../work/colab-final-t2/runs/20260804-115307/`](../work/colab-final-t2/runs/20260804-115307/)  
> **入口:** [`CURRENT-ALL773-FACES.md`](../work/colab-final-t2/CURRENT-ALL773-FACES.md)  
> **採点:** `score_final_trust_abc.py` · report [`all773-abc-report.json`](../work/colab-final-t2/runs/20260804-115307/all773-abc-report.json)  
> **≠** T2/T3 residual カタログ faces `041247`（物差し・mid 幾何が別）

---

## 1. 何を測ったか（混同しない）

| 項目 | 本 run（all773） | 対照 T2/T3（`041247`） |
|---|---|---|
| 井 | **773** train allowlist | **80** hard20_balanced |
| 行 | **3,783,989** | 約 0.4M 帯 |
| 面 | tip / mid_before_hedge / learned（同一 Colab run） | tip / mid residual 材料 / L · 別 dump |
| tipdist(mid, tip) | **0.201** | residual 帯 **~1.7–3.3**（例 666=1.985） |
| A tip pooled | **10.839** | catalog tip **17.030**（T2）· residual T3 別尺度 |
| ゲート方針 | A/B/C/D tip⊕(mid) · L=agree ゲートのみ（F015） | residual α 合成 · T3-B 三点 |

**読み方:** all773 は「**全 train 人口での tip 床 + tip⊕mid が効くか**」のフル定規。  
**666 の Trust 頭（pool≈10.09 on T3 residual）を置き換えない。** mid が tip に張り付いているため、ここで mid 注入ゲインを期待するのは誤り。

---

## 2. 結果表（Final Trust A/B/C/D）

| policy | pooled RMSE | frac inject mid | hard20 mean | Δ vs A |
|---|---:|---:|---:|---:|
| **A** tip alone | **10.8388** | 0 | **26.8294** | 0 |
| **B** tip ⊕ row(mid) | **10.8307** | 0.0249 | 26.8210 | **−0.0081** |
| **C** tip ⊕ (agree∧row) | **10.8307** | 0.0249 | 26.8210 | **−0.0081** |
| **D** tip ⊕ agree-only | **10.8351** | **1.0** | 26.8210 | −0.0037 |

- **winner pooled = B**（C と **同一数値** · Δ_C−B = 0）  
- hard_mean ほぼ不動（26.829 → 26.821 · **−0.008**）  
- **tipdist mid/L:** mid **0.201** · L **0.268**（どちらも tip 近傍）

### 井単位の要約

| 統計 | A tip | D mid全注入 |
|---|---:|---:|
| 井 mean RMSE | 8.51 | 8.50 |
| median | 6.50 | 6.49 |
| p90 / p95 / p99 | 16.3 / 21.5 / 31.6 | 同型 |
| max | **60.23**（`1b1eba53`） | 同 |

**B vs A（井 RMSE）:** help **≈1.9%** · hurt **≈0.9%** · 最大 help `00bbac68` **−1.55** · 最大 hurt `9d3ec64c` **+0.29**  
→ フル集合では **ほぼ押し引きゼロ**。

### hard20 / 最悪尾

- hard20 平均 **≈26.83** が一貫して残り、pooled 10.8 と乖離 → **easy 井が pooled を希釈**  
- tip 最悪帯の例: `1b1eba53` 60.2 · `5f4d2a52` 48.1 · `91b301ce` 44.6 · `708caea9` 40.7 …（既知 hard 系）

---

## 3. 「773 だから分かった」知見（T2 80 では擬似的にしか見えない）

（詳細は [`all773-stage-well-group-2026-08-05.md`](all773-stage-well-group-2026-08-05.md)）

1. **誤差はほぼべき分布:** top100 井が tip SSE **≈62%** · hard20 だけで **≈20%**（2.6% 井）。pool 10.84 は「みんなが中くらい」ではない。  
2. **T2 mid win77 は full tip-cv mid に複製不可:** label **win25 / hurt21 / タイ727** · tipdist ほぼ 0 · **面ごとに物語を切断**する。  
3. **tip は bulk で既に強い**（非 hard mean **≈8.0**）· hard mean 26.8 が別問題 · S0 再設計 ROI 低。  
4. **hard 群で tipdist 最小** → hard は tip に張り付き mid ブレンド未到達 · 突破は **L/resid 学習**のみ。  
5. **非 hard 内 Q4e mean tip≈15.6**「半 hard」層 → weight を hard20 だけにしない（802/804 型が妥当）。  
6. **B≡C / sign_agree≈1** · agree ゲートはフル人口で追加情報なし · Public agree 再発明の動機が薄い。  
7. tip⊕ の mid 注入対象が人口の **~3% しか「差がある」井がない**（tipdist>0.05 の井≈5.3%）。

---

## 4. Kaggler 読み（GO / NO-GO）

### 4.1 確定 GO（運用）

1. **all773 dump 完了 · SHA 検証済 · PC 分析可能** · Private DS `kazeneko77/rogii-final-t2-faces-20260804-115307`  
2. **フル train で tip 床 = pool 10.84 · hard 26.83** を SSOT 化（hard20 スクリーンと並べて読む物差しが増えた）  
3. **tip⊕mid は full CV では天井** — Δpool ≪ 0.01 · **提出・Final 差替の根拠にしない**  
4. **B≡C** → 本 learned 面では agree ゲートが **row 以外の追加情報ゼロ**  
5. **D を 100% mid にしても tip と区別ほぼ不能** → mid_before_hedge（本 run）は **「T2 で mid が tip を −4.7 した mid」ではない**

### 4.2 確定 NO-GO / 禁止

| 禁止 | 理由 |
|---|---|
| 本 face の **生 tip/mid/L を FINAL** | **F015** |
| all773 で tip⊕ を再発明・再提出 | Public 既に tip⊕群閉鎖 · 本計測で Trust も動かない |
| all773 mid で **T2 mid win77 を再主張** | tipdist 0.20 で幾何が別 · **041247 residual 面の読みを壊す** |
| hard_mean 未動で L1 成功とみなす | 尾 **26.8** が本命 · tip⊕ 無関係 |

### 4.3 戦略への接続

| 既存方針 | all773 の寄与 |
|---|---|
| Trust 枠1 = **666 系 · residual α · Trust only** | **不変**（別 faces · residual 梯子は 041247） |
| Public 枠2 = **farvol** | **不変** |
| 本命 = **L 質（761/804… dual）** | **強化** — full CV でも hard_mean は tip⊕ で動かない → **残すレバーは L（と L 後 residual）のみ** |
| F043 residual-α 閉 | **維持** |
| T2 faces `041247` を residual catalog SSOT | **維持** · all773 は **フル人口 tip 尺**として併記 |

---

## 5. 対比（なぜ T2 mid 注入が「勝った」のに all773 で死ぬか）

```text
T2 mid (catalog): tip 17.0 → mid 12.3   tipdist 大 · inject が効く土台
all773 mid (本):  tip 10.8 → mid≈tip     tipdist 0.20 · inject が残渣しか生まない
```

**結論:** tip⊕ 勝ちは **「mid が tip から十分離れている面」** が前提。  
本 all773 dump の mid_before_hedge は **tip 近傍ブレンド完了面**であり、**T3 residual の代替ではない**。

---

## 6. 次アクション（実験）

| 優先 | 行動 | 根拠 |
|---|---|---|
| 1 | **L retrain dual 継続**（761/782 → 804…） | hard_mean 26.8 不動 |
| 2 | residual T3 は **041247 / 666 尺** 維持 | all773 mid で residual 再評価しない |
| 3 | all773 tip を **フル baseline** として dual 報告に併記可 | pool 10.84 / hard 26.83 |
| 4 | **提出=ユーザー明示のみ** · 本 face 提出なし | F015 · tip⊕ NOGO |

---

## 6. ファイル索引

| 用途 | パス |
|---|---|
| faces | `exp/work/colab-final-t2/runs/20260804-115307/faces/` |
| ABC JSON | `.../all773-abc-report.json` |
| per-well | `.../all773-abc-report-per-well.csv` |
| pointer | `exp/work/colab-final-t2/CURRENT-ALL773-FACES.md` |
| Private DS | `kazeneko77/rogii-final-t2-faces-20260804-115307` |
| T2 対照 | `CURRENT-T2-FACES.md` · run `20260804-041247` |
