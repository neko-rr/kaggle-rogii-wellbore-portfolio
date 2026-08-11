# CHK-802 FAST2 · final-day L1 screen (2026-08-05)

## 目的

最終日に間に合わせるため **train_stack を圧縮**して L1 判定速度を上げる。

| 項目 | 旧 FAST (804) | **FAST2 (802)** |
|---|---|---|
| folds | 3 | **2** |
| LGB models | 3 (n=600 / 1200 / 1200) | **1** (n_est **200**, lr 0.05) |
| CatBoost | 2 models | **skip** |
| early_stopping | 250 | **80** |
| 狙い wall | ~1.5–2h stack | **~15–25 min stack**（preamble除く） |

GO 疑義 / borderline のみ **L_FULL**（3fold · フルstack）再学習。  
画面結果が **mid-collapse 同型**なら weight 近親は打ち切り **808→781** へジャンプ。

## Status

- static preflight: **PASS**
- ban-gate pre T3: **PASS**
- train FAST2: **DONE** OOF **9.3765** · face harvest OK
- dual: **NOGO_L1** · [ops-dual](ops-chk802-dual-nogo-2026-08-05.md) · ban-gate post **NO-GO**
- residual 後工程 / 提出: **E2E ABORT** · [post-pipeline](ops-chk802-post-pipeline-2026-08-05.md)
- 次: **808→781**（weight 帯 **F044 全閉** · 802 含む）

## 禁止

- 提出（802 residual E2E 含む）· 804/761/782/802 weight 言い換え · residual α · tip⊕ · Kaggle 新規 weight L1
