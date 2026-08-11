# CHK-185 結果 — tip 候補天井監査（2026-07-25）

> 作業: [`exp/work/chk185-candidate-ceiling/`](../exp/work/chk185-candidate-ceiling/)  
> 計画: [`chk185-candidate-ceiling-plan.md`](chk185-candidate-ceiling-plan.md)  
> intel: [`20260725-alt-lineage-intel.md`](20260725-alt-lineage-intel.md)

## 1 行結論

**ディスク上の tip 家系候補では「選択」では伸びず、天井は generator 不足。**  
SOFT をラベルで最適に選んでも pooled は **8.33→8.18（+0.15）** 止まり。**4.8 帯には届かない。**

---

## 何を測ったか（限定）

| プール | 候補 | 目的 |
|---|---|---|
| **A** | tip T2 / T3 seed123 / T3 seed2026 | シード多様性 |
| **B** | tip + gated/SOFT/farvol（既存 graft） | 同家系の選択余地 |
| **C2** | hard20 tip / BH / NW_N-BH（SP45除外） | tip 内部ノブ |

除外（F・別面）: NCC · chk040/070/081 · Sunny · 近傍コピー

範囲: tip T2 allowlist **80井** · hard20 **20井**

---

## 数値

| プール | selected | oracle | gap | gap≥0.5 井 | oracle>6 井 | 読み |
|---|---:|---:|---:|---:|---:|---|
| A seeds | 8.330 | 8.330 | **0** | 0 | 23 | シード CSV **完全同一** |
| B tip+soft | 8.330 | **8.175** | **+0.155** | **3/80** | **23/80** | tip が既に最良 **64/80** |
| C2 hard20 | 14.870 | 14.870 | **0** | 0 | **20/20** | BH/方位ノブは tip 未越え |

B の oracle 選出: tip 64 · portable 8 · selfdev8 7 · gated_s05 1

ギャップ最大でも **~0.95ft**（難井）で、その井の oracle 自体はなお **14〜20ft**。

---

## Kaggler 解釈

1. **選択ボトルネックではない**  
   Discussion（S2）の「候補 oracle≈4.5」は、**もっと豊かな候補生成**を前提にしている。手元 tip+SOFT 集合では該当しない。

2. **generator 不足が支配的（S3）**  
   ラベル付き最良でも 23/80 井が RMSE>6、hard20 は全滅。公開 tip 沼の天井と一致。

3. **1位 4.859 との差**  
   ディスク上の後処理・シード・BH ノブの選択では説明不能。別 generator（未所持）か Public 特化か。

4. **次にやってよいこと**  
   - Final2（枠1 tip Trust / 枠2 Public Best）  
   - CHK-184 は **+0.15 級の残差**として任意（大勝負ではない）  
   - **やらない:** F011–F020 言い換え · 学習 ranker · 近傍/方位の再掘り

---

## 成果物

- [`chk185-report.json`](../exp/work/chk185-candidate-ceiling/chk185-report.json)
- per-well CSV: `chk185-per-well-A/B/C*.csv`
