# CV Tier 体制 — rogii-wellbore

> updated: 2026-08-04  
> purpose: **用途別の検証階層**（壊れ検知 / 採用 / Final / 空間監査）  
> 数値の正: [`exp/exp-index.md`](../exp/exp-index.md)  
> Public/Private 関係: [`cv-lb-private-relation.md`](cv-lb-private-relation.md)  
> Metric 手順: [`metric-repro.md`](metric-repro.md) · tip 手順: [`submission-prep-cv.md`](submission-prep-cv.md)  
> faces T3 実測: [`exp/work/out-t3-cpu-harvest/`](../exp/work/out-t3-cpu-harvest/) · 工程内: [`exp/within-stage-comparisons.md`](../exp/within-stage-comparisons.md)

---

## 1 行方針

**主物差しの型は変えない**（well-GroupKFold · 評価区間のみ · pooled RMSE · CF 門番）。  
用途ごとに **井集合・seed 数**だけ段階を上げる。

---

## Tier 表

| Tier | 用途 | 井集合 | seed | 実行レーン | 状態 |
|---|---|---|---|---|---|
| **T0** 疎通 | 形式・壊れ検知 | hard20 | 1 | tip GPU 短時間 / ローカル CF | 既存 |
| **T1** ゲート | CF 比較 · graft 粗選別 | hard20 | 1 | tip GPU / `score_tip_cv.py` | 既存（CHK-014） |
| **T2** 採用 | graft / 手法の本採用判定 | **hard20 + 方位層化 sample60（計≈80井 · GPU ≈6h）** | 1 | tip GPU · allowlist `hard20_balanced` | **新設** |
| **T3** Final | Final 枠1/2 候補の確定 | T2 と同じ ≈80井 | **3 seed**（平均 + バンド幅） | **種別で時間帯が全く違う**（下節） | **新設** |
| **T4** 空間監査 | 近傍・空間特徴の楽観検出 | CF=773 ローカル / tip=T2 集合 | 1 | ローカル CPU（条件付き） | **CHK-072**（040 hard20 直後） |

ローカル CF / 代理系は **773 井フル GroupKFold** のまま。T2 以降の判定には **fold seed 3 種（42 / 123 / 2026）** を併記する。

> **T3 は「同一 ≈80 井 × 3 seed」**。T2 より **井を増やさない**。井を増やすと「より厚い ruler」になるが、それは本表の T3 定義ではない（任意の all773 / CF-773 等は別物差し）。

**CHK-060 実測（2026-07-24）:** 全fold合算の CF pooled OOF は seed によらず **15.91**（全井 SSE 同一のため）。安定幅は **worst_fold band ≈ 0.51** · fold_mean band ≈ 0.05（`cf-multiseed-report.json`）。

---

## CHK → Tier 対応

| CHK / 作業 | 最低 Tier | 備考 |
|---|---|---|
| CHK-014 tip smoke / 壊れ検知 | T0–T1 | 完了済 |
| CHK-020 方位 graft · CHK-041 多峰 hedge | **T2** | hard20 だけでは本採用しない |
| Final 枠1（Trust CV 最良） | **T3** | 選抜方針: [`comp-strategy`](comp-strategy.md) |
| Final 枠2（Public 最良） | 提出前に T1 以上で壊れなし | Public は選抜軸 · 採用根拠は CV（関係論） |
| 空間特徴を入れる CHK の直前 | **T4（CHK-072 再掲）** | 近傍系は F012 閉鎖 · 新空間仮説のみ |
| CF 門番安定幅（CHK-060） | ローカル multi-seed | CPU |

---

## 判定式（採用・Final）

### T2（本採用）

次をすべて満たす:

1. tip（または候補）**pooled RMSE** が、同井集合の CF pooled より **≥ 0.05 改善**
2. hard20 の well-mean RMSE 悪化 **≤ 0.1**（既存ゲート）
3. cover ≥ 0.99
4. （任意だが推奨）方位ビン別で **NW_N が悪化しすぎない**（CHK-020 切断面）

### T3（Final 枠1 確定）

T2 に加え:

1. **3 seed の tip pooled 平均**で T2 条件を満たす
2. 改善幅が **seed バンド（max−min）より大きい**（ノイズ扱いを避ける）

枠2は Public 最良選抜（[`comp-strategy`](comp-strategy.md)）。Public の微差（**≲0.08 · Georgy σ≈0.03**）を **枠1の採用根拠にしない**（[`cv-lb-private-relation.md`](cv-lb-private-relation.md) §Public評価）。

### T3 の2種 — 時間と信頼性（必読 · 2026-08-04）

現場では **「短い T3」** と **「表どおり GPU T3」** が混在する。**同じ T3 ラベルでも中身が違う。** 記録時は必ず種別を書く。

| 種別 | 何を回すか | 時間 | seed が効く場所 |
|---|---|---|---|
| **A. フル tip T3**（表の既定 T3） | tip（または upstream）を **seed×3 でほぼ再実行**し、各 seed の pooled / fold を取る | **≈ T2×3**（GPU 数時間帯） | **予測面そのもの** が seed で揺れる |
| **B. faces / residual T3**（カタログ・残差監査） | 既にダンプした **固定 faces**（mid / L / tip 等）上で α・mix を式適用し、train 評価区間 RMSE を multi-seed fold する | **数十秒〜数分 · CPU** | 面は固定。seed は **fold 分割**のみ |

#### なぜ B が短いのか

- 重い部分（selector / mid / learned の生成）は **既に1回で済んだ faces** を再利用する  
- 残差・薄ブレンドは **行列演算 + スコア**だけ（`mid + α(L−mid)` 等）  
- 再学習・tip 再推論をしない → **「T3 が速くなった」のではなく、コスト定義を落とした T3**

#### B は T2 より信頼できるか

| 観点 | 結論 |
|---|---|
| **上がる** | 同一 fixed face について、1 seed の最悪 fold だけで順位を決めない → **mean_worst / max_band** で 666 vs 641 vs tip⊕ 等の **安定順位**が付く（faces catalog 2026-08-04） |
| **上がらない** | **井数は T2 と同じ ≈80** · mid/L/tip の **再生成 seed 揺れは測らない** · tipdist / Public は **別物差し**（E2E · LB） |
| **pooled 注意** | fixed 残差では full **pooled は seed ほぼ不変** → T3 の本信号は **mean_worst_fold / max_band** 側 |

**読み分け:**

1. Trust 残差の格子・工程内梯子の監査 → **B（faces T3）で十分かつ推奨**（CPU · 提出禁止の診断を多用）  
2. tip 本体・上流を差し替える Final 級の「枠1確定」→ **A（フル tip T3）** または T2×E2E を要求；**B の短い数字だけで A を通過扱いしない**  
3. B で pooled が改善しても **F015 生 L 昇格・過激 α の Public** は別途禁止帯（[`cv-lb-private-relation.md`](cv-lb-private-relation.md) · residual Public 閉鎖）

実測 SSOT: [`exp/work/out-t3-cpu-harvest/report.md`](../exp/work/out-t3-cpu-harvest/report.md) · catalog [`catalog-graph-faces/`](../exp/work/out-t3-cpu-harvest/catalog-graph-faces/)

---

## T4 空間 leave-out — **CHK-072**

**CHK-040 hard20 PASS 直後（または近傍/空間特徴の本実験直前）に必須。** 仕様の正: checklist CHK-072 · [training-insights](discussion/training-insights.md) · Discussion 727570。

発動トリガ（いずれか）:

- Active で **近傍 TVT 転写 / 空間補間特徴 / leave-field 依存**の仮説を走らせる
- tip graft が **他井座標・距離**を学習特徴に入れる
- **CHK-040** が hard20 ゲートを通過した

最小仕様:

- 井の (X,Y) 先頭または平均で空間ブロック分割
- CF（または当該代理）で通常 GroupKFold pooled と leave-spatial-out pooled の差分を記録
- 差分が **楽観方向に大きい**（空間分割の方が悪い）なら、その特徴の採用を保留

**今やらないこと:** 773 井フル tip CV · Random CV · Public に合わせた分割歪め。

---

## 成果物パス

| 成果物 | パス |
|---|---|
| T2 allowlist | `exp/work/wave0-ruler/tip-cv-allowlist-balanced.json` |
| tip CV レポート | `exp/work/wave0-ruler/tip-cv-report.json`（T1）/ `tip-cv-report-t2.json` 等 |
| multi-seed tip | `score_tip_cv.py --multi` → `tip-cv-multi-seed.json` |
| CF multi-seed | `exp/work/wave0-ruler/cf-multiseed-report.json` |
| 生成スクリプト | `my-local-eval-notebook/wave0-ruler/build_tip_cv_allowlist.py` |

---

## GPU / CPU 実行メモ

- T2 ≈ 80井 × ~4.3分/井 ≈ **6h**（9h 制限内）
- **T3-A（フル tip）:** 同 allowlist · seed 違いを **順次**（GPU 最大2枠）· **≈ T2×3**
- **T3-B（faces residual）:** CPU で catalog / 単体・**秒〜分** · **A の代替ではない**（上節）
- 起動は **ユーザー許可 + 対象ジョブ指示**（Rule）。見積は `exp/run-ledger.md`

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-08-04 | **T3-A/B 注釈** · faces residual T3 の時間・信頼性 vs T2 · harvest リンク |
| 2026-07-24 | 初版 · T0–T4 · CHK 対応 · T4 発動条件のみ |
