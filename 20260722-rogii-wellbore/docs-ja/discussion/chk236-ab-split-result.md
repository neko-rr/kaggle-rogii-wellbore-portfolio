# CHK-236 — hard20 (A)/(B) 分割（2026-07-27）

> action: T4 診断（Force · T4 streak 回避）· 提出なし · tip GPU なし  
> 作業: [`exp/work/wave21-upstream-mid/`](../../exp/work/wave21-upstream-mid/)  
> 入力: CHK-186 · CHK-205b · hard20 allowlist

## 方針1行

**(B)優勢 n_B=14 >= n_A=6（hit_ok=0）→ 上流を厚く（CHK-246 → 232 → 233…）。中間は後回し。**

## 定義

| ラベル | 条件 |
|---|---|
| hit | `hit_le_4_5 == 1` |
| **(A)** | hit かつ（`gap_pf3 >= 0.5` または `ll_rank_of_best > 1`） |
| **(B)** | hit なし |
| hit_ok | hit かつ非 A |
| 優勢 | `n_B >= n_A` → B、否则 A |

## 件数

| 項目 | 値 |
|---|---:|
| hard20 | 20 |
| **(A)** | **6** |
| **(B)** | **14** |
| hit_ok | 0 |
| frac_hit≤4.5 | 0.30 |

## 井一覧

**(A)** `25050f63` · `43e16325` · `a959858c` · `ba48188d` · `c8d9680c` · `f88ddb26`

**(B)** `1b1eba53` · `206b6193` · `2fd68f7b` · `389ae58f` · `4c2208f5` · `57f05c51` · `5f4d2a52` · `7e721392` · `86454a6f` · `91db7070` · `94d813a4` · `f6d009f4` · `fb03ae90` · `fef8af96`

CSV: [`chk236-ab-per-well.csv`](../../exp/work/wave21-upstream-mid/chk236-ab-per-well.csv) · JSON: [`chk236-ab-report.json`](../../exp/work/wave21-upstream-mid/chk236-ab-report.json)

## 含意

- hard20 の **7割が候補不足（B）**。Wave-21 は上流（二峰 init · 多様性 · 多峰）を主戦場にする。
- (A) 6井は尤度ランクずれが残る → 中間 CHK（249/250/237）は副として残す。
- 次診断: **CHK-255**（MD vs TST）→ 本実験先頭 **CHK-246**。
