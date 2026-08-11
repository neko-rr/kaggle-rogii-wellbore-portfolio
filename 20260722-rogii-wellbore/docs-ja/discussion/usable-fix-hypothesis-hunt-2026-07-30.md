# 「提出に使える直し方」仮説ハント（2026-07-30）

> purpose: Wave-27 の「天井はあるがラベル無し実装が無い」を受け、**他者NB・GitHub・文献**から提出可能な直し方の仮説だけを集める  
> 前提: F038（平行移動）· F039（天井依存形修正 / median寄せ）は再開しない  
> 数値の正: [`exp/exp-index.md`](../../exp/exp-index.md) · Wave-27: [`wave27-twist-close-2026-07-30.md`](wave27-twist-close-2026-07-30.md)

---

## 初学者向け（3行）

1. **直せそう（天井）** と **提出で直せる（ラベル無し）** は別物。Wave-27 は後者が無いと結論した。  
2. ネット/他者NBが出してくる「直し方」の多くは、すでに自チームで **F00x 閉鎖**済みか、**別モデルを一から作る**話。  
3. まだ試す価値があるのは「soft曲線をこねる」より、**GRでラグを測る・PSだけつなぐ・別スタックを多様性に使う**あたり。

---

## なぜ「softを形修正」が提出で死ぬのか（再確認）

| Wave-27 事実 | 提出への意味 |
|---|---|
| 欠測/スパイクの説明力は高い | 正解を知れば直せるが、どの区間かはラベル無しで当てられない（353 FAIL） |
| piecewise/warp の天井は大きい | 検出は一応できるが、median寄せは悪化（360 FAIL · F039） |
| 位相/振幅は弱い | 「全体ラグ合わせ」本命にはならない |

→ 探すべきは **F038/F039 の言い換えではない** 仮説。

---

## 外部ソース → 仮説（抽象化）

### A. 公開 NB / GitHub（コンペ直結）

| 出典 | 借りるアイデア（抽象） | 提出向き？ | 自チームとの衝突 | 仮説ID |
|---|---|---|---|---|
| **mycarta** [rogii-geosteering-toolkit](https://github.com/mycarta/rogii-geosteering-toolkit) | **multi-scale NCC + heel自己相関**で整合特徴 → LightGBM が residual/dTVT を予測。`dcor_sliding` は NCC が拾えない非線形合わせ | **中**（別スタック or ラグ検出器） | 絶対TVTの NCC+木は **F007/F008/F011**。**drift目標+自己相関ラグ検出**は未試行の余地 | **H-A1 · H-A2** |
| **Mitch** drift-targeting-NCC（既存要約） | 目標を absolute TVT ではなく **drift（−last_anchor）** | 低（LB帯旧 · F007系） | **F007/F008** | （再実行禁止 · 目標設計の教訓のみ） |
| **dalloliogm** TCN starter | 系列モデルが **last known TVT 基準の残差**を予測 | **低〜中**（Final2多様性） | 行/系列MLは CV 帯が tip より悪い実績多い · tip置換は非推奨 | **H-A3** |
| **vamseeachanta** Phase5 設計 | **eval開始点が heel 最終 TVT_input と連続**する per-well bias | **中**（局所のみなら F038と区別可） | 全域バイアスは F038/F019 寄り。**PS近傍だけ**なら新規 | **H-A4** |
| **Sunny / Karnak** 物理+PF | formation top + Z から物理 TVT · 非 tip | 低（**F004** Public大敗） | Final禁止 | （経路の叙述のみ） |
| **Connor** dTVT≈−dZ+drift | 幾何の天井〜10ft · LOO | 提出コードにしない | 教育 | （構造事実） |
| tip 同家系 Frontier / GeoAnchor / GBDT gate | 定数パッチ · 井単位 residual | Final不可 | **F015/F016** · 同家系 | 監視のみ |

### B. 文献・ドメイン（ネット）

| 出典 | 借りるアイデア | 提出向き？ | 衝突 | 仮説ID |
|---|---|---|---|---|
| PF + GR ↔ type log（SPWLA/SPE 系 · 自 `literature-survey`） | 粒子の **局所シフト合わせ尤度**で重み更新（形そのものを後から曲げない） | **中**（生成/尤度側） | 観測尤度の手改修は Wave-24 **F033–F035** 付近で全滅済み。**窓付き自己相関ラグを提案分布に入れる**は未試行の細い隙 | **H-B1** |
| DTW + PF（SPE-230765 等） | ライブGRと参照の DTW で境界検出 | 低 | **F017** 無制約/heel-DTW 閉鎖。制約付きでも実装コスト高 · 締切近 | 原則 skip |
| CVAE residual around ridge（Research Square 2026） | 確率的補正ネットワーク | 低 | 新学習 · ライセンス · 9h · 締切 | skip |
| 3D horizon + PF（Geosciences 2024） | 地震面拘束 | **不可** | コンペに地震なし · 外部DB禁止 | skip |
| Within-well TVT–Z decoupling（mycarta方法論） | 横坑内では Z と TVT はほぼ独立 → **傾き/dip 由来の rate prior** | **中** | 定数平行ではない。rate clip 系は F037 一部と近いので **弱い prior のみ** | **H-B2** |

---

## 仮説カード（実験にするならこの形）

> **checklist 反映済（2026-07-30）:** CHK-363=H-A1 · 364=H-A4 · 365=H-A2 · 366=H-A3 · 367=H-B2 · 368=H-B1 · hypothesis-ban · F038/F039 衝突チェック必須。

### H-A1 — heel自己相関ラグ検出 → 未知区間だけ位相補正（ラベル無し）

- **手法:** 既知 heel の GR を typewell に multi-scale NCC（または dcor）で合わせ、**ラグの信頼度（ピーク鋭さ）**を測る。信頼度が高い井だけ、未知区間の soft/粒子に **同じラグ族**を適用（全域定数TVTシフトではない）。  
- **期待:** Wave-27 で「位相説明力は弱い」一方、**検出可能な位相井**だけなら +0.30 級が取れるか。欠測優勢井には適用しない。  
- **提出性:** ラベル不要 · E2E可能。  
- **≠:** F038（全粒子同量）· F039（median寄せ）· F017（無制約DTW）· F011（NCC+木で絶対TVT）。  
- **リスク:** 位相ファミリー自体が soft−oracle では弱かった → **天井probeを先に**（heelラグ教師 vs 真値）。

### H-A2 — mycarta型「整合特徴 → residual GBDT」別スタック（tip置換ではなく Final2）

- **手法:** NCC / self-corr / landing-zone / tortuosity 特徴で **dTVT or residual** を GroupKFold 学習。tip と **低相関**なら枠2候補。  
- **期待:** tip と同面にならない多様性。  
- **提出性:** あり（学習は train のみ）。  
- **≠:** F007（NCC+木が tip 高相関で敗北）— **成功条件を「tip pearson≪0.99 かつ hard20 で CF超え」**に置く。未達なら即打ち切り。  
- **リスク:** 過去 tabular/NCC は Final2 条件未達が多い。

### H-A3 — 系列 residual（TCN）を tip に薄ブレンドしない / 単独 Final2 診断

- **手法:** dalloliogm 型 TCN で last-anchor residual。  
- **期待:** 多様性のみ。  
- **Stop:** tip への薄混ぜは Wave-19 系で弱い実績 · **単独 hard20 screen が tip に大敗なら即NO-GO**。

### H-A4 — Prediction Start 連続拘束（局所のみ）

- **手法:** 評価区間の先頭数 ft〜数十 ft だけ、予測を `last TVT_input` に連続接続（以降は tip のまま or 線形に減衰）。  
- **期待:** 境界の形破れ（欠測/区分の一種）をラベル無しで抑える。  
- **≠:** F038 全域平行 · F019 遠MD直線。  
- **リスク:** tip が既に連続なら Δ≈0（F025型の無駄提出に注意）。

### H-B1 — GR窓自己相関を PF 提案に入れる（後処理禁止）

- **手法:** 形の後処理ではなく、生成中に **短いMD窓の GR–typewell ラグ**を提案に混ぜる。  
- **期待:** スパイク区間の粒子が生き残る。  
- **衝突:** F026/F033–F037 と近いので **薄い screen + pretrain-gate** 必須。締切近なら優先度下。

### H-B2 — 傾き由来 rate prior（弱い）

- **手法:** within-well では TVT 変化≈相対 dip。inclination / dZ から **弱い rate 正則**（定数シフトではない）。  
- **衝突:** F037 rate clip 言い換えに注意。**正則の強さを極小**にし tip soft 非悪化を門番に。

---

## 優先順位（優秀な Kaggler としての推奨）

| 順 | 仮説 | 理由 |
|---|---|---|
| **1** | **H-A1** | Wave-27 の穴（検出）に直結 · ラベル無し · F038/F039と明確に違う |
| **2** | **H-A4** | 実装が軽い · 連続性はドメイン常識 · 失敗しても Δ0 で終わりやすい |
| **3** | **H-A2** | Final2 多様性の最後の別面候補 · ただし過去 NCC/木は厳しい |
| **4** | H-B2 / H-B1 | 締切近 · 失敗台帳と近い |
| **×** | 天井だけの欠測マスク · median区分寄せ · 無制約DTW · tip同家系パッチ | F039/F017/F015 |

**並行必須:** OPS-FINAL2（枠確定）は仮説ハントと独立に進める。

---

## やらないリスト（検索で出てくるが今回は捨てる）

- 有料地下DB / 他盆地ログ学習（Rules · Host未回答）  
- RL で舵取り最適化（評価が TVT RMSE と不一致）  
- 地震 horizon 追跡（データ無し）  
- Frontier / tip 中間面の再提出（F015）  
- 「oracle天井が大きいから形修正を厚くする」（F039）

---

## 次アクション提案

1. **checklist 反映済:** Wave-28 · **CHK-363–368**（H-A1〜H-B2）+ OPS-FINAL2 · [`experiment-checklist.md`](../../exp/experiment-checklist.md)  
2. 実行はユーザー許可後 · 優先順は CHK-363 → 364 → 365 → 366 → 367 → 368（T4 screen から）。  
3. 詳細ソース: mycarta toolkit · dalloliogm TCN · vamsee Phase5 · 自 `literature-survey.md` · `non-tip-lineage-references.md`
