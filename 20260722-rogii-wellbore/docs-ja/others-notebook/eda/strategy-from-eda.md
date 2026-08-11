# EDA → 戦略（2026-07-24）

> source: [`analysis.md`](analysis.md) · `others-notebook/eda(-ja)/`  
> **方針の正（Final2 · Bets）:** [`../../comp-strategy.md`](../../comp-strategy.md)  
> **実験キュー:** [`../../../exp/experiment-checklist.md`](../../../exp/experiment-checklist.md)  
> 現状メモ: B2=F011 · B3=F012 · 枠2=別面未成立 → 選抜は `comp-strategy` §Final2

---

## 1 行結論

EDA が示す「正しい問題設定」は確定。別予測面の探索（整合学習・ゲート近傍）は **F011/F012 で閉鎖**。  
以降の賭け方・Final 選抜は **`comp-strategy.md` のみ**を正とする（本ファイルは EDA 拘束条件の要約）。

---

## EDAが確定させた構造事実（仮説ではない）

| # | 事実 | 出典 NB | 戦略への拘束 |
|---|---|---|---|
| 1 | 評価区間 = `TVT_input` NaN の連続区間 | visual / Chris / walkthrough | マスク再現 CV 以外で採択しない |
| 2 | 6 tops ≈ 平行な **1面**（散らばり≈0） | walkthrough · tvt-identity | tops を6独立特徴・絶対アンカーにしない |
| 3 | `TVT = top − Z + b_well` は説明用。**U=TVT+Z 持ち越しは CF より大幅悪化** | tvt-identity | 構造面一定外挿は禁止。目標は **flat TVT アンカー残差** |
| 4 | 手元 `test/` 3井は train コピー | visual · tvt-identity | 検証・チューニング禁止 |
| 5 | Eagle Ford · **Buda 急崖**が GR 照合の背骨。着床は EGFDL 多数・Austin 少数 | decoding-eagle-ford | 全井同一層前提を捨てる |
| 6 | ~30% 井で ±15–30 ft **二峰**。中点が RMSE 最適。モード決め打ちネットは平均に敗北 | 15-ft-datum | 曖昧井への分類器投資は期待値マイナス |
| 7 | well-CV と field-CV の差≈0.3–0.4 = 近傍既知分 | tvt-identity | 空間特徴を入れるなら差を監視（CHK-072 再掲条件） |
| 8 | Public 急改善の一部は **train 双子マッチ** | visual-eda | Private 戦略にしない |
| 9 | 行 tabular ≪ flat/anchor | beginners | 行 ML Final 禁止（既存） |

---

## すでに閉じた経路（EDA + 自チーム）

| 経路 | 閉じた理由 |
|---|---|
| 行 tabular / 軌道残差学習 | EDA + F010 |
| 素朴 heel affine · 遠井コピー | F001 · F002 |
| tip 後処理の方位/BH | F006 · F009 |
| 二峰モード決め打ち · tip `_BH_` hedge | EDA 15ft · CHK-041 |
| heel+窓 NCC → drift 学習 | **F011** |
| ゲート付き近傍転写 | **F012**（hard20 空間疎 · tip 同面） |
| tip 離散プロファイル梯子 | **F013** |
| 学習内方位分割 | **F014** |
| tip 中間面昇格 | **F015** |
| tip×Best 井単位アービター | **F016** |
| heel 拘束 DTW | **F017** |
| 低整合→CF / 遠MD heel直線 | **F018 / F019** |
| 攻撃的 tip_self_line（sample 無視） | **F020**（SOFT 診断のみ） |
| Sunny 物理 | F004 |

→ 「同じ GR–typewell 情報を別取り出し」で別面を作る期待は捨てる。詳細は failures 台帳。

**Discussion 追記（2026/07/25）:** [728712](../../discussion/728712-gs-noise-scale-public-nb.md) の PF `gs`×≈1.3 は tip 公開コードに **既実装**（ultimate-pf / gs130 / luck 同一）。Final2 多様性にはならない。現行 Final（枠1 tip CV · 枠2 Public Best）を変えなくてよい。

**公開 NB refresh（2026/07/25）:** Connor `dz-dtvt-eda` が幾何天井〜10ft を定量化し、本表の構造事実（特に #3）を補強。geoanchor / A016 は同家系の叙述・ablation。総括: [`../public-useful-refresh-20260725.md`](../public-useful-refresh-20260725.md)

---

## 残る運用（新規 Bet ではない）

| 項目 | 内容 | 置き場 |
|---|---|---|
| 枠1防衛 | 曖昧井は尖らせない · tip 最終面を壊さない（F015）· SOFT 自動昇格禁止（F020） | `comp-strategy` · checklist Stop |
| 着床層別の誤差 | CHK-080 done（EGFDL やや悪いが単一戦略で足りる） | `exp/work/chk080-screen/` |
| 公開NB由来 Parked | **EDA監査（2026-07-25）:** 110 frozen · 111 score-hyp禁止 · 112 absorbed · **Active 昇格しない** | checklist |
| Final 選抜 | 枠1=Trust CV · 枠2=Public最良 · 必須は UI 選択のみ | **`comp-strategy` §Final2** |
| SUB-8/9 | SOFT / gated smoke PENDING · 診断 · Wave-13 で Public 後判断 | forecast · [`wave13-plan`](../../wave13-plan-2026-07-25.md) |

### EDA → checklist 仮説修正の判定（2026-07-25）

| 判定 | 内容 |
|---|---|
| Active を増やす？ | **不要**（構造事実は Stop 化済 · Bets 閉鎖済 · Wave-10/11 診断済） |
| 閉じた CHK を再開？ | **不要**（F011–F020 と EDA が一致） |
| Parked 110–112？ | **要修正** → 昇格期待を下げ凍結／吸収（上表） |
| 新 Bet？ | **提案しない**（締切近 · 別面未成立 · Public 26% 追い禁止） |

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-07-25 | Wave-10/11 · F018–F020 · SUB-8 診断を閉じた経路へ追記 |
| 2026-07-25 | **EDA×checklist 監査** · Parked 優先度改定 · Active再開なし |
| 2026-07-25 | 公開 NB refresh · Connor 幾何 · `gs*1.3` は tip 既実装と確認 |
| 2026-07-25 | Discussion 728712/728879 反映 · PF `gs`×1.3 は枠1微調整候補のみ |
| 2026-07-24 | 初版（F011 後 · 080/081） |
| 2026-07-24 | F012 反映 · Final/Bets は `comp-strategy` へ委譲 · 重複削減 |
