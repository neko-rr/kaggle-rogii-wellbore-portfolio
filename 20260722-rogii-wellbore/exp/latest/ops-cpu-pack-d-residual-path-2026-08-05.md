# OPS — CPU Pack D · residual-path 設計探索（2026-08-05）

> **提出禁止** · T4 screen · Colab 並行可 · F044 weight retrain 禁止  
> **local:** [`work/out-t3-cpu-harvest/cpu-expert-pack-d-20260805/`](../work/out-t3-cpu-harvest/cpu-expert-pack-d-20260805/)  
> **Kaggle CPU×5:** 下表 · Private · Internet OFF

---

## 1. 何をやったか

Colab が 802/781 を回している間に、**L retrain なし**で 781/807/802/784 設計地図を拡張。

| ID | 内容 | 環境 |
|---|---|---|
| **D1** | live L face（688/761/782/**804**）residual dual 再掲 | local（harvest 要） |
| **D2** | residual-path β×mask 格子 L\* vs y | local + Kaggle |
| **D3** | collapse budget（hard \|L−mid\| を壊さない帯） | local |
| **D4** | protect（midhurt / hurt15 除外）path | local + Kaggle |
| **D5** | 807 stop: residual vs L rank | local + Kaggle |
| **D6** | MD-Q4 行 only path（802 理論） | local + Kaggle |
| **D7** | Huber 風 well-weight map（784 design · F044 非） | local + Kaggle |

gate pre: **CHK-CPU-D T4 PASS**

---

## 2. D1 再確認（live dual · hybrid80）

| face | hard Δ | hybrid Δ | hard d\|L−mid\| | 判定 |
|---|---:|---:|---:|---|
| 688 | +0.52 | +0.23 | −0.90 | NOGO |
| **804** | **+0.74** | **+0.33** | **−1.43** | NOGO mild collapse |
| 782 | +3.81 | +1.71 | −7.93 | NOGO |
| 761 | +4.01 | +1.81 | −7.93 | NOGO |

Weight face はすべて **\|L−mid\|↓ かつ residual↑**（F044）。

---

## 3. D2–D4 offline path 天井（L\* teacher · α0.35）

SSOT residual pool **10.094** · hard **16.304**

| 候補 | β | mask | d_pool | d_worst | hard_d | hard d\|L−mid\| |
|---|---:|---|---:|---:|---:|---:|
| all | 0.30 | all | **−3.03** | **−3.57** | −4.89 | **+10.7**（拡大＝non-collapse） |
| q34 | 0.30 | q34 | −2.34 | −2.89 | −3.97 | +7.8 |
| hard20 | 0.30 | hard | −2.02 | −2.41 | −4.89 | +10.7 |
| all protect excl midhurt | 0.30 | excl_mh | −2.88 | −3.35 | −4.89 | +10.7 · d_midhurt **0** |

**y teacher β0.30 all** は L\* より遥かに弱い（過去 781 sim どおり）。

**重要:** path は \|L−mid\| を **増やし** residual を下げる。  
weight retrain は \|L−mid\| を **減らし** residual を上げる。  
→ **781 residual-path loss の方向は offline で正しいレバー**。

---

## 4. D5 807

| 指標 | 値 |
|---|---:|
| resid_rmse vs path_benefit Spearman | **1.00** |
| top20 resid ∩ benefit | **1.00** |
| top20 L-TVT ∩ benefit | 0.85 |
| prefer_stop | **residual_rmse** |

TVT-OOF だけ early-stop は 804 と整合して不利。

---

## 5. D6 / D7

- **D6:** MD-Q4 行 L\* path でも hard d_pool 改善は残る（802 を weight にしないで path/loss 寄り設計可）  
- **D7:** `d7_chk784_huber_well_weights.json` · midhurt force 1.0 · **loss 地図のみ · F044 攻撃 weight 禁止**

---

## 6. Kaggle CPU kernels（Ver3 COMPLETE ≡ local 主結論）

| kernel | status | harvest |
|---|---|---|
| [cpu-cv-d-781-path-grid](https://www.kaggle.com/code/kazeneko77/cpu-cv-d-781-path-grid) | COMPLETE | `…/path-grid-v3/d2_path_grid.csv` |
| [cpu-cv-d-protect-path](https://www.kaggle.com/code/kazeneko77/cpu-cv-d-protect-path) | COMPLETE | `…/protect-v3/d4_protect_path.csv` |
| [cpu-cv-d-807-stop](https://www.kaggle.com/code/kazeneko77/cpu-cv-d-807-stop) | COMPLETE | `…/stop-v3/d5_807_stop_proxy.json` |
| [cpu-cv-d-mdq4-row](https://www.kaggle.com/code/kazeneko77/cpu-cv-d-mdq4-row) | COMPLETE | `…/mdq4-v3/d6_mdq4_row_path.csv` |
| [cpu-cv-d-huber-map](https://www.kaggle.com/code/kazeneko77/cpu-cv-d-huber-map) | COMPLETE | `…/huber-v3/d7_chk784_huber_well_weights.json` |

**修了:** `exp/work/out-t3-cpu-harvest/kaggle-cpu-pack-d-20260805/*-v3/`

| 失敗 Ver | 原因 | 修正 |
|---|---|---|
| Ver1 | `No kernel name found`（ipynb に kernelspec 無し） | metadata `kernelspec: python3` |
| Ver2 | `t3_worst() missing argument w` | 全呼び出し `t3_worst(pred,y,w)` |
| Ver3 | COMPLETE | — |

Kaggle 再実測の一致例: β0.30 all d_pool **−3.028** · D5 prefer **residual_rmse** · top20 resid cap **1.0**

---

## 7. 設計への落とし込み（Colab / 次 L1）

| 次 CHK | Pack D から |
|---|---|
| **781** | loss ≈ residual path toward L\* · apply 帯 **q34 ∪ hard · excl midhurt** · intensity offline 0.15–0.30 帯 |
| **807** | early-stop / selector = **residual RMSE 主** |
| **802** | weight retrain 最終 1 本でもよいが **path 設計を 781 に寄せる方が期待値高** |
| **784** | huber map は **loss sample_weight 記述**まで · 攻撃 upweight と同型にしない（F044） |

---

## 8. 禁止

- Pack D 結果の **提出**  
- D 地図を理由にした **weight retrain の再起動（F044）**  
- L\* を **教師ラベル反転**として学習（loss 方向のみ許可）

updated: 2026-08-05 · local COMPLETE · Kaggle Ver3 COMPLETE（≡ local 主結論）
