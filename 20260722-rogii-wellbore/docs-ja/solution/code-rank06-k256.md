# [6th / k256.dev] コード要約 — PF bagging notebook

**分析日:** 2026-08-08  
**順位:** Private **#6 / 5.984** · Public ~20th  
**作者:** k256.dev (@k256net)  
**公開コード:** [PF bagging NB](https://www.kaggle.com/code/k256net/public20th-private6th-pf-pf-pf-pf-and-bagging)  
**ローカル:** `retro/archive/others-notebook/post-comp-top-20260808/rank06-k256net-public20th-private6th-pf-bagging/`  
**writeup:** [733226](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733226)  
**GitHub:** writeup 時点で「later」（2026-08-08 未確認）

---

## 要約

- **モノリス提出 notebook**: `%%writefile` で **18 本の .py をその場生成**し、artifact dataset（`rogii-artifact-v103-final` 等）の checkpoint + `blend_final.json` と結合して推論。  
- 思想（writeup と一致）: **多数 PF パラメータ / 前処理系統**を特徴化し、**行単位 NN で bag**。さらに **GR 非使用の geometric anchor**（FormationPlane / κ / GRU）系統も同梱。  
- 提出は `SUBMIT_MODE` **A/B を2回**回して Final2 相当を作る設計。

---

## 構成（コード上）

| 要素 | 内容 |
|---|---|
| 入口 | 先頭 env: `DATA` / `DSPATH=final_submit_dataset` / `blend_final.json` 必須 |
| 生成モジュール | `pf_banks_v95/v97.py`, `features_*`, `create_*`, `nn_emission_*`, `submit_v103/v104/final.py`… |
| NN | `Net`, `Enc1D`, `_SeqNet`, `_SelfAttn` など 1D 系列ネット |
| 物理/補助 | `FormationPlaneKNN`, `DenseANCCImputer`, GR-free anchor 5-fold 平均 |
| 統計 | `def` ~**192** · `class` ~16 · code ~350k 文字 |

### 典型フロー（概念）

```
artifact (ckpt, pf_banks_config, blend_final.json)
        +
live recompute (PF banks / anchors / features on hidden test)
        ↓
row-level NN / multiple decoders (v103/v104/dec10…)
        ↓
blend_final / submit_final → submission.csv
```

環境変数例: `NN_SEEDS=5`, `N_SPLITS=5`, `PF_NGPU`, `V103_L5_CONFIGS`, `SUBMIT_MODE`.

---

## writeup とコードの対応

| writeup 主張 | コードでの表れ |
|---|---|
| 91 PF → NN bag | `pf_banks_*` · `n_pf` 多用 · bank_param |
| Optuna で PF 散布 | writeup 主 · NB は fixed banks + artifact config |
| Pub overfit 回避 | geometric GR-free 経路 · multi seed folds |
| T4×2 注意 | GPU 数検出 `PF_NGPU` |

---

## 再現性

| 項目 | 評価 | メモ |
|---|---|---|
| コード | **高（infer 一式）** | 巨大 NB 1本 |
| artifact DS | **必須** | metadata の dataset_sources が空文字でも、実行時は `k256net/rogii-artifact-v103-final` を探索 |
| 複雑度 | **極高** | 改造より「部品カタログ」として読むのが現実的 |
| 学習再現 | 低–中 | 重みは artifact · 学習 script は分散 |

---

## 改造・学習ポイント

1. **PF を1本に固定しない** — パラメータ多様化 → 候補特徴 + 行融合。  
2. **GR 非使用 anchor** で層ロックを避ける並列系統。  
3. **提出オーケストレータ**（モード A/B · 環境検出 · multi-gpu）を運用資産として分離。  
4. tip residual 単独より **候補工場 × bagging** のほうが本戦上位帯に直結。

---

## 未確認

- [ ] GitHub 本体公開後の diff  
- [ ] `blend_final.json` の正確な 91 次元定義（artifact 要 DL）
