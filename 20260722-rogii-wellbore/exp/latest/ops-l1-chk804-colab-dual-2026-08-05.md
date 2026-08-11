# ops — CHK-804 Colab L1 dual（2026-08-05）

> 提出禁止 · Kaggle GPU 新規 L1 禁止  
> SSOT face harvest Desktop: `exp/work/out-t3-cpu-harvest/chk804-colab-face-20260805/`  
> Drive run: `…/colab-final-t2/runs/20260805-073247-chk804-l1-hard20/`  
> **法則 SSOT:** [`l-improvement-laws-2026-08-05.md`](l-improvement-laws-2026-08-05.md)

---

## 1. L1 学習（Colab L4）

| 項目 | 値 |
|---|---|
| run_id | **`20260805-073247-chk804-l1-hard20`** |
| weight | **v1c known×Q4** · n_boost **43** · FORCE_RETRAIN · STOP_AFTER_LEARNED |
| FAST | 3-split · GPU |
| OOF (stack) | lgb ≈9.77 · cb ≈9.85 · ridge-stack **9.701** · tip-cv pooled TVT **9.131** |
| learned face | 107478 rows（hard20 retrain カバー） · sha256 `8ead74a2…a3cc` · **3.5MB** |
| WORK_DIR | Drive `runs/…/work`（揮発 `/content` 禁止） |
| 事故 | post-learned SystemExit 吸収後 cell 続行 · cell60 `FACES` NameError（**face は既に Drive コピー済 · dual 影響なし**） |

**注意:** TVT-OOF **9.13** は見た目強いが **L1 採否の根拠にしない**（下節 dual）。

---

## 2. dual（local · Desktop · α0.35 · faces 041247）

path: [`l-dual-CHK-804-colab`](../work/out-t3-cpu-harvest/l-dual-CHK-804-colab/report.md) · `summary.json`

| 物差し | 結果 |
|---|---|
| **L1_pass** | **False** · **NOGO_L1** |
| hard Δpool | **+0.7395**（悪化） |
| hard Δworst3 | **+0.833** |
| hybrid Δpool | **+0.325**（10.094 → **10.419**） |
| hybrid Δworst3 | **+0.409**（11.905 → **12.315**） |
| 812 Q4 | **+0.417** ok=False · midhurt3 **0.000** ok |
| 813 SSE top50/100 | **+0.410 / +0.325** · 両 ok=False |
| 815 unlock | moved=**True** · d_resid **+0.74** · d\|L−mid\| **−1.433** |
| non_hard / Q4e / Q1e | d_resid **0**（新 L は hard 行のみ） |
| 688hurt 15 | d_resid **+0.934**（hard より悪い帯） |

### タイプ別（810 · 要所）

| slice | d_resid | 読み |
|---|---:|---|
| A_hard20 | **+0.74** | 本戦場で悪化 |
| D_688_hurt | **+0.93** | retrain 毒が残る |
| B_Q4_rows | **+0.42** | Q4 も悪化（known×Q4 の意図が住まない） |
| C_drag | **+0.41** | 拖帯も悪化 |
| E_mid_hurt3 | 0 | カバー外 |
| non_hard | 0 | fillna 旧 L |

---

## 3. 専門家読み（Kaggler）

### 3.1 Verdict

**NOGO_L1 · 言い換え再学習禁止（v1d 等）。**  
Trust 頭はなお **666 α0.35**（旧 L）。Final2 不変。

### 3.2 病理 = mild mid-collapse

- hard mean \|L−mid\|: **10.99 → 9.55**（d **−1.43**）  
- residual 同時悪化 → 815: **unlock しても GO にしない** テンプレ再確認。  
- 761/782 の \|L−mid\| d≈**−7.93** より軽いが **同じ符号・同じ失敗族**。

### 3.3 oracle ≠ live

| 期待（CPU-C / v1c map） | 実測 |
|---|---|
| offline d_pool 負（knee ≈ −0.55） | live hard **+0.74** |
| oracle 804 ≳ 802 ≫ 761 | **壊れ方** 804≪761 のみ一致 |
| known×Q4 で Q4 改善 | Q4 **+0.42** 悪化 |

**結論:** weight map + TVT retrain は residual 面では **誤った最適化**。OOF は L-TVT を良くしても residual 方向に揃っていない。

### 3.4 梯子内位置

```text
壊れにくさ:  688 (+0.52)  ≺  804 (+0.74)  ≺  782 (+3.8)  ≺  761 (+4.0)
機構:        無 weight     known×Q4      drag       fold-driver
```

- **「weight を賢く」する路線は 804 で実用上限が判明**（それでも NOGO）。  
- 次は **機構変更（loss / path）**（781 · 807）が本命。  
- MD-Q4 **行** 802 は別機構として **1 本だけ**残してよい（F044 の「sample_weight 系」再試ではないかを dual で判定）。

### 3.5 808 カウント

| 勘定 | 扱い |
|---|---|
| 688 | baseline · **3 本目にしない** |
| 761 · 782 | **近親 weight 毒** · closed |
| **804** | known×Q4 · **1 本済 · 閉** |
| 802 | MD-Q4 **行** · 別機構 1 本（任意）後 → JUMP 判定 |
| JUMP | weight 帯失敗連鎖 → **781(+805)** |

---

## 4. 次

```text
DONE: 688 · 761 · 782 · 804  = L1 NOGO（weight/retrain 帯）
NOW:  Colab **802 MD-Q4** 1 本（軽い確認）→ dual 810/812/813/815
        or 方針ジャンプなら直接 **781 residual-path**
THEN: 809 protect · 806∩688 監査（低優先）· 808→781
STOP: 804 言い換え · 761/782 再 · residual α · tip⊕ · Kaggle 新 L1 · GR · 提出=明示
```

---

## 5. 記録先

| 用途 | パス |
|---|---|
| dual | `exp/work/out-t3-cpu-harvest/l-dual-CHK-804-colab/` |
| face | `exp/work/out-t3-cpu-harvest/chk804-colab-face-20260805/` |
| 法則 | [`l-improvement-laws-2026-08-05.md`](l-improvement-laws-2026-08-05.md) |
| F044 | `exp/improvement-loop-failures.json` |
| table | `exp/hyperparameter-table.md` |
| train | `exp/exp-train.md` |

updated: 2026-08-05 夜（分析確定 · F044 · 法則）
