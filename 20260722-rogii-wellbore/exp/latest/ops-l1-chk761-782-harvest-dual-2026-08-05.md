# OPS — Kaggle GPU harvest · CHK-761 / CHK-782 L1 dual

> date: 2026-08-05 · kernels **COMPLETE** · dual local α**0.35** · faces **20260804-041247**  
> **提出禁止** · Final2 不変 · Kaggle GPU 枠 **空き（提出温存）**

---

## 回収

| CHK | kernel | status | harvest | learned rows |
|---|---|---|---|---:|
| **761** | `kazeneko77/tip-cv-chk761-weighted-h20` | COMPLETE | [`harvest-761`](../work/out-t3-cpu-harvest/watch-v2-20260805/harvest-761/) | 107478（hard20 のみ） |
| **782** | `kazeneko77/tip-cv-chk782-resid-drag-h20` | COMPLETE | [`harvest-782`](../work/out-t3-cpu-harvest/watch-v2-20260805/harvest-782/) | 107478 |
| 804 Kaggle | `tip-cv-chk804-known-q4-h20` | **CANCEL_ACK** | 実験は **Colab 本線**（Kaggle L1 push 停止方針どおり） | — |

### 実行設定（ログ）

| CHK | config | weight |
|---|---|---|
| 761 | `v2_fold_driver` · sample_weight max=2 · hard20 | fold-driver 20 wells（**disk v2b midhurt 保護は未反映の可能性**） |
| 782 | `v1_resid_drag` · n_weighted **41** · FAST N_SPLITS=3 | resid>L drag · mean w=1.03 max=2 |

dual: [`run_l_residual_local_dual.py`](../work/out-t3-scratch/run_l_residual_local_dual.py) · tag `CHK-761-harvest` / `CHK-782-harvest`

---

## Dual 結果（Trust residual · 新旧 L）

基準 SSOT residual mid+α0.35: pool **10.094** · mean_worst **11.905**

| run | hard Δpool | hybrid Δpool | Q4 d | 688hurt d | drag d | SSE50 d | 815 \|L−mid\| d | L1 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **688**（参照） | **+0.52** | **+0.23** | +0.36 | — | — | — | — | **NOGO** |
| **782** | **+3.81** | **+1.71** | **+2.16** | **+4.18** | **+2.13** | **+2.16** | **−7.93** | **NOGO_L1** |
| **761** | **+4.01** | **+1.81** | **+2.29** | **+4.36** | **+2.25** | **+2.28** | **−7.93** | **NOGO_L1** |

- cover = **hard20 only**（non_hard / midhurt3 / Q4e d=0 は fillna 旧 L · 監査対象外）  
- **815 unlock = True** だが d_resid 大幅悪化 → **L が mid に吸い寄せ（\|L−mid\| 崩壊）**  
- 報告: [761 dual](../work/out-t3-cpu-harvest/l-dual-CHK-761-harvest/report.md) · [782 dual](../work/out-t3-cpu-harvest/l-dual-CHK-782-harvest/report.md)

---

## 専門家読み

### 1. 両 L1 は「軽い NOGO」ではない

688 は hard +0.5 級。**761/782 は hard +3.8〜4.0 · hybrid +1.7〜1.8** で residual を壊した。  
weight の **fold-driver / resid-drag** は hard 面で **688 より悪い failure mode**。

### 2. 共通病理 = mid-collapse

両 run で hard の mean \|L−mid\| が **~11.0 → ~3.05**（d≈−7.93）。  
学習が mid に張り付き residual の「L レバー」を殺す。  
→ **sample_weight を hard/drag に盛るだけ**では L1 GO にならない（地図は残すが、同型再学習は無駄）。

### 3. 帯内順位（この2本）

782 わずかに 761 よりマシ（hard 3.81 vs 4.01）だが **GO 閾値とは無関係**。  
oracle 地図 **804 ≳ 803 ≳ 802 ≫ 761** を **live dual で再確認**（761 最弱帯確定）。

### 4. 次アクション

| する | しない |
|---|---|
| **Colab 804 v1c** L1（known×Q4 · 別機構） | 761/782 **再 GPU** · 同型 weight 言い換え |
| dual 810/812/**813/815** を 804 でも | Kaggle 新規 L1 push（提出温存） |
| weight **3 NOGO なら 808→781**（688+761+782= L 帯 NOGO 累積 · **804 は別機構なので 1 回試す**） | 生 L FINAL / residual Public |
| 804 dual 失敗時: 802/809 または **781 residual-path** | 761 v2b 再 push 期待値低 |

### 5. レーン

- Trust L1: **761 NOGO · 782 NOGO** · 本命頭はなお **666 α0.35**  
- Public / Final2: **不変**（farvol / 666）  
- Kaggle GPU: **空** · 提出・提出 kernel 用に温存

---

## 記録先

- dual reports 上記  
- harvest paths 上記  
- SSOT: `exp-index` · `experiment-checklist` · `hyperparameter-table` · `exp-train` · `within-stage-comparisons` · session-bridge
