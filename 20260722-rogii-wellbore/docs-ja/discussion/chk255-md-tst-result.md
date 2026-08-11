# CHK-255 — MD vs TST 軸 GR 照合（2026-07-27）

> action: T4 診断 · 提出なし · tip-cv なし  
> 作業: [`run_chk255_md_tst_screen.py`](../../exp/work/wave21-upstream-mid/run_chk255_md_tst_screen.py)

## 判定

**absorbed** — TST 風軸は tip の TVT 照合より大幅に悪い。lik graft / tip-cv しない。

## 方針1行

TST風 pooled GR-RMSE=35.860 ≫ TVT=14.499（better_wells=0 · 全20井 best=tvt）→ tip TVT 照合を維持し次へ（CHK-246）。

## 要約

| 軸 | pooled GR-RMSE（既知区間） |
|---|---:|
| **TVT（tip 現行）** | **14.499** |
| MD（線形写像） | 32.564 |
| TST 風（dMD·sin I 累積） | 35.860 |
| TVD（|ΔZ| 累積） | 36.675 |

- `best_axis_counts`: tvt=20 / 他=0
- `n_tst_better_by_abs05`: **0**

CSV: [`chk255-md-tst-per-well.csv`](../../exp/work/wave21-upstream-mid/chk255-md-tst-per-well.csv)  
JSON: [`chk255-md-tst-report.json`](../../exp/work/wave21-upstream-mid/chk255-md-tst-report.json)
