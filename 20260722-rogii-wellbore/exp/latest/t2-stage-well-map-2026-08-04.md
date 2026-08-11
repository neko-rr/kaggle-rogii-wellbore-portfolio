# T2 工程×井マップ — 2026-08-04

> wells: **80** · rows: 397333 · run `20260803-114917` · **提出禁止**  
> 面: tip(S0) · learned(S1診断) · mid(S7/S9スタック) · S9ゲート。**S2–S6 個別面は CHK-643 Ver2 dump 中**（mid に内包）。  
> ε=0.05（|Δtip−stage|&lt;ε → flat）  
> **updated:** 2026-08-04 午後 · residual / Public は工程比較へ → [`pipeline-stage-well-map-2026-08-03.md`](pipeline-stage-well-map-2026-08-03.md) §C · [`within-stage-comparisons.md`](../within-stage-comparisons.md)

### セッション追記（井 count · Public 埋め）

| id | T2 pooled | tipdist E2E | help/hurt T2 | Public | メモ |
|---|---:|---:|---:|---:|---|
| mid≡agree | 12.279 | — | 77/3 | — | actionable · 生FINAL禁止 |
| 641 α0.30 | 10.309 | 1.743 | **77/3** | **6.472** | **Public NO-GO** |
| 668 α0.30+β0.05 | 10.206 | 2.552 | **71/9** | — | soft で hurt↑ |
| **666 α0.35** | **9.998** | **1.985** | **77/3** | 未提出 | **GO_e2e** · 提出禁止 |
| 620 soft inject | 12.907 | — | — | — | NOGO 閉鎖 |

詳細: [`residual-t2-well-effects-2026-08-04.md`](residual-t2-well-effects-2026-08-04.md) · [`ops-641`](ops-lb-chk641-public-2026-08-04.md)


## 工程相当 pooled RMSE（T2）

| 工程相当 | id | pooled | hard20平均 | frac_inject |
|---|---|---:|---:|---:|
| S0 tip | tip | 17.0297 | 26.8294 | 0 |
| S1 learned（診断·F015） | learned | 6.8061 | 7.6396 | 1 |
| S9 mid スタック | mid | 12.2789 | 18.5214 | 1 |
| S9 agree-only | agree | 12.2789 | 18.5214 | 1.0000 |
| S9 agree∧row | agree_row | 12.3313 | 18.5377 | 0.7693 |
| S9 row | row | 12.3313 | 18.5377 | 0.7693 |
| S9 H-D | hd | 13.8870 | 21.4525 | 0.4666 |

## tip→工程 の井カウント（80井）

| 工程 | win | flat | hurt |
|---|---:|---:|---:|
| S9 mid | 77 | 0 | 3 |
| S9 agree | 77 | 0 | 3 |
| S9 row | 74 | 2 | 4 |
| S9 H-D | 38 | 40 | 2 |
| S1 learned | 77 | 0 | 3 |

## mid が効く井（Δ tip−mid 大きい順 · 上位15）

| well | tip | mid | Δ | hard20? |
|---|---:|---:|---:|---|
| `5f4d2a52` | 48.11 | 31.03 | 17.08 | True |
| `1b1eba53` | 60.23 | 44.49 | 15.74 | True |
| `b3388334` | 29.94 | 19.01 | 10.93 | False |
| `f88ddb26` | 25.68 | 15.18 | 10.50 | True |
| `fef8af96` | 27.60 | 17.88 | 9.72 | True |
| `91db7070` | 38.12 | 29.07 | 9.05 | True |
| `206b6193` | 32.49 | 23.69 | 8.80 | True |
| `3e011332` | 22.77 | 14.03 | 8.74 | False |
| `86454a6f` | 32.64 | 23.94 | 8.70 | True |
| `389ae58f` | 18.83 | 10.25 | 8.58 | True |
| `fb03ae90` | 27.26 | 18.89 | 8.37 | True |
| `2fd68f7b` | 26.29 | 18.23 | 8.07 | True |
| `7e721392` | 24.48 | 16.71 | 7.76 | True |
| `4f3eb9e9` | 18.94 | 11.24 | 7.70 | False |
| `a959858c` | 19.27 | 11.61 | 7.65 | True |

## mid が悪化する井（Δ 小さい順 · 下位15）

| well | tip | mid | Δ | hard20? |
|---|---:|---:|---:|---|
| `70925e23` | 8.00 | 12.00 | -4.00 | False |
| `ab3ced07` | 5.82 | 7.59 | -1.77 | False |
| `19871e7f` | 1.82 | 3.01 | -1.19 | False |
| `89fdb2f2` | 2.00 | 1.83 | 0.17 | False |
| `b95e7121` | 1.88 | 1.66 | 0.22 | False |
| `44441e54` | 1.65 | 1.37 | 0.28 | False |
| `eb06a4e7` | 4.10 | 3.77 | 0.33 | False |
| `aaeffccb` | 3.32 | 2.89 | 0.42 | False |
| `398dce4b` | 2.89 | 2.43 | 0.46 | False |
| `c2717d4f` | 8.88 | 8.39 | 0.49 | False |
| `0dd99dc5` | 3.54 | 3.03 | 0.51 | False |
| `d217e0c5` | 4.65 | 4.14 | 0.52 | False |
| `fd3b4faa` | 4.60 | 4.02 | 0.58 | False |
| `9a8ae0d6` | 4.03 | 3.41 | 0.62 | False |
| `a4719920` | 3.04 | 2.41 | 0.63 | False |

## 読み（T2）

1. **S9 mid 全面**は tip より pooled **4.751** 良い（12.279 vs 17.030）。
2. **agree-only frac=1.000** → T2ではほぼ≡mid（カタログと同型）。
3. mid win **77** / flat **0** / hurt **3** 井。
4. **H-D** は mid より pooled 悪化（絞り込みで勝ち分を捨てる）→ Public 514 と同型の警告。
5. **learned 単独**は診断天井だが F015 · 生FINAL禁止。
6. S2–S6 は未 dump · 次の dump で細分化可能。

## 成果物

| ファイル | 役割 |
|---|---|
| `t2-stage-per-well.csv` | 井×工程 RMSE |
| `t2-stage-summary.json` | 集計 |
