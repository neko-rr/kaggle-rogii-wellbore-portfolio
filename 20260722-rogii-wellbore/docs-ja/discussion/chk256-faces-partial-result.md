# CHK-256 部分結果 — tip 内部面 tip-cv（2026-07-28）

> Ver1 GPU **ERROR**（mpkg が公式 sample と衝突）· 部分成果物で tip-cv 採点  
> Ver2: mpkg を tip-cv 下で disable → hedge/score まで再走中  
> 提出なし · F015

## 1 行（暫定）

**tip-cv hard20 @T0.15 では gold / sp45 / selector / submission（gold後）が完全同値（pool 30.089）。**  
learned は test-id で tip-cv 計測不能。→ **案C「内部面天井」は現時点で見えない** · 分岐は **A（261〜）厚め**。

## tip-cv 数値（eq-well RMSE · hard20 · Ver1 partial）

| 面 | pool | Δ vs selector | beat wells |
|---|---:|---:|---:|
| selector（FINAL 代理） | **30.089** | 0 | 0 |
| sp45 | 30.089 | 0 | 0 |
| gold_conservative/balanced/aggressive | 30.089 | 0 | 0 |
| submission（gold 後） | 30.089 | 0 | 0 |
| learned | — | — | unmeasurable |
| before_hedge / mpkg | — | — | Ver1 未達 · Ver2 待ち |

凍結 tip-cv 29.899 との差 ≈0.19 は集約定義差帯。**面間差は 0** が主結論。

ログ: gold `applied_wells=0` · `mean_abs_move=0`（全プロファイル同一 SHA）。

## test 多様性（ラベル無し · Best tip T0.15 E2E）

| 面 | RMSE vs FINAL |
|---|---:|
| before_hedge / gold / before_mpkg / before_selfline | **0.968**（相互≡） |
| mpkg_gated_010/020 | ≈0.97 |
| learned | 5.740 |
| mpkg_only | 16.69 |

→ Public 既知（pre-BH 6.653 · F015）と整合。tip-cv 上では gold が動かないため、**test 差分は hedge 以降の本番専用段**の可能性が高い。

## 分岐（checklist）

| 条件 | 次 |
|---|---|
| 256 で内部面 ≤ FINAL（暫定確定） | **C 薄く** · **A（261→268→267）厚く** |
| Ver2 で before_hedge が tip-cv 改善 | C を再検討 |

## 成果物

- `exp/work/wave22-candidates/chk256_partial_*.csv/json`
- `chk256_test_face_diversity_vs_final.csv`
- kernel: `kazeneko77/tip-cv-chk256-faces-h20` Ver1 ERROR · Ver2 RUNNING
