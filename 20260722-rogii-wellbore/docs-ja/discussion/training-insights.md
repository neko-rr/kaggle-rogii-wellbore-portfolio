# Discussion 学習（Training）知見 — 分析

> updated: 2026-07-24 UTC  
> 目的: **どう学習するか**（特徴・目標・CV・禁止）だけを抽出。LB 哲学は [`cv-lb-private-relation.md`](../cv-lb-private-relation.md)  
> 反映先: [`exp/experiment-checklist.md`](../../exp/experiment-checklist.md) · [`cv-tiers.md`](../cv-tiers.md)

---

## 1 行結論

学習の「正しい形」（flat 残差 · ガード整合 · Trust CV）は確定。  
整合学習（040）· ゲート近傍（081）は **F011/F012 で閉鎖**。Final 選抜は [`comp-strategy`](../comp-strategy.md)。学習拘束の EDA 要約は [`strategy-from-eda`](../others-notebook/eda/strategy-from-eda.md)。

---

## 上位者・Host が言っている学習プロトコル

| 優先 | topic | 誰 · 日 | 学習への含意 | 自チーム状態 |
|---|---|---|---|---|
| **A** | [727149](727149-sub6-regime-alignment-cv.md) | Georgy · 07/22 | heel gain/offset + GR 回転 denoise 後の残りは **井ごと shape/dip**。無制約 DTW は洗流し。PF は信頼ゲート | → **CHK-040** |
| **B** | [712037](712037-fork-the-ruler.md) | Georgy · 06/22 | 誤差の核は **drift slope** だが合法特徴から **学習困難**（field R²≈0） | 横断 slope 回帰は本命禁止 |
| **C** | [726751](726751-beginners-map-rowwise-ml-fails.md) | n0Rollback · 07/16 | 行 LGBM 17.46 ≪ anchor-hold ~16.1 | 行 tabular **本命禁止**（Stop · F010） |
| **D** | [726465](726465-top-team-signal-below-line-oracle.md) | De DQ · 07/15 | **方位分割して学習**が楽。近傍&lt;150 は形状コピー向き。Tucker: per-well only でも CV&lt;5 | 方位は **学習条件**（tip 後処理は F006/F009） |
| **E** | [727570](727570-local-validation.md) | Tucker · souldrive 07/23 | 5×5 well-CV。**well vs field-CV ≈+0.3** · worst field · `test/` は identity | → **CHK-072** · Tier T4 |
| **F** | [719389](719389-cv-lb-correlation.md) · [723647](723647-lowest-cv.md) | yu4u · Tucker | Trust CV。CV&lt;~6 で LB 相関は分解能切れ | 採用=安定 CV（既存 Tier） |
| **G** | [711878](711878-pm15ft-bimodal-datum.md) | souldrive · 06/22 | ±15 二峰。モード当てより **中点/hedge** | CHK-041 NO-GO 済 · 040 では不確実性ゲート余地 |
| **H** | [727171](Competition-Host_727171-working-note-winners.md) | Host Igor · 07/18 | 高周波 wiggle は無料。壁は **低周波** | 目的=低周波 trend/shape |
| **I** | [717573](717573-score-without-tabular.md) | 複数 | 表現が天井。tabular/非tabular とも 5台可 | Final2 を GBDT 残差に固定しない |
| **J** | [717445](717445-writeup-anchors-guarded.md) | FOYSAL · Georgy | **ガード付き**整合。探索幅は train-tail EDA で制約 | 040 窓はガード必須（F008 回避） |
| **K** | [708367](708367-problem-breakdown.md) | 複数 | GR 回転 denoise · 誤差=heel+piecewise dip | 040 特徴前段に denoise |
| **L** | [726834](726834-six-architectures-same-blind-spot.md) · [718670](20260723-recent-short-notes.md) | OpPrime · Jiwei | 多アーキ同一盲点。公開の安い技=**last-known TVT からの残差** | 残差目標は last_anchor 基準 + 整合特徴（F010≠） |

### 補完取得（2026/07/24）

| topic | 要点 |
|---|---|
| **722236** | steven: 複雑 NN より **表現・CV・学習安定**。DECEM simple NN CV8.9/LB8.39。matcher vs ranker は未確定 |
| **721578** | GP + Typewell warping 説明のみ · コメント 0 · 学習 CHK 化は保留 |
| **717445** | FOYSAL: guard 幅は「どこでも探索」ではなく **train-tail の TVT 移動量**で制約 |

---

## 効果が薄い／禁止（学習）

| やらないこと | 根拠 |
|---|---|
| 行単位 ML 本命 | 726751 · F010 |
| Typewell 無し heel affine | F001 · 727149 |
| 遠井コピー · 薄い NCC+木 · soft-argmax · ゲート近傍 | F002 · F007 · F008 · **F012** |
| tip 後処理の方位 blend / BH だけ上げ | F006 · F009（De DQ の「分割学習」とは別物） |
| tops 絶対アンカー · 無制約 DTW · 有料 DB | 727149 · Stop |
| 他人の CV–LB ギャップで自分を校正 | 727570 souldrive |
| `test/` 3 wells で学習検証 | identity |
| 多アーキ平均で同一盲点を消す | 726834 |

---

## checklist への反映マップ

| 知見 | 反映 |
|---|---|
| heel+窓 → drift | **CHK-040 → F011 閉鎖** |
| ゲート近傍 | **CHK-081 → F012 閉鎖** |
| field-CV / worst-field | CHK-072 cancelled · 空間CHK前に再掲 |
| Trust CV / multi-seed | CHK-060–062 done |
| F001–F012 | failures + Explicit Stop |

**Active 乱増しない。** 次の CHK はユーザー承認後の新仮説のみ（[`experiment-checklist`](../../exp/experiment-checklist.md)）。
