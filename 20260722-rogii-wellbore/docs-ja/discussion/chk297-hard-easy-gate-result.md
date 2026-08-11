# CHK-297 結果 — ラベル無し hard/easy ゲート（2026-07-30）

> action: **T4** · LOO · **提出なし**  
> 作業: [`exp/work/wave25-hardwell-lane/run_chk297_hard_easy_gate.py`](../../exp/work/wave25-hardwell-lane/run_chk297_hard_easy_gate.py)  
> JSON: [`chk297-report.json`](../../exp/work/wave25-hardwell-lane/chk297-report.json) · 凍結: [`chk297-gate-frozen.json`](../../exp/work/wave25-hardwell-lane/chk297-gate-frozen.json)

## 1行方針

**hard/easy 本番スイッチは固定可能（PASS）。** 279断絶 subtype のラベル無し再現は不可 → subtype 別ノブは診断地図のみ。

## 集計（panel = hard20 ∪ Wave-14 easy shape · n=65）

| 項目 | 値 |
|---|---:|
| LOO hard recall | **0.950**（19/20） |
| LOO easy FPR | **0.022**（1/45） |
| AUC | **0.986** |
| acceptance | recall≥0.75 · FPR≤0.20 · AUC≥0.80 → **PASS** |

誤分類: easy `4f3eb9e9`（過検知）· hard `fb03ae90`（取りこぼし）。

## 主な手がかり（特徴 AUC）

| 特徴 | best AUC |
|---|---:|
| `tip_std_prox` | 0.983 |
| `tip_std_eval` | 0.973 |
| `tip_far_self_dev` | 0.869 |

単特徴 `tip_std_prox` 閾値だけでも recall0.85 / FPR0.022。ridge 多特徴で取りこぼしをさらに減らした。

## 断絶 subtype（CHK-279 · hard20 内）

| 項目 | 値 |
|---|---:|
| LOO disc recall | 0.44 |
| AUC | 0.44 |
| portable? | **No** |

→ 本番で ranking_fail / post_destroy を分けてスイッチしない（地図は CHK-299 診断用）。

## 含意

- Wave-25 介入対象ゲート = **凍結 ridge（`chk297-gate-frozen.json`）**
- 次: **CHK-298** easy 非回帰 harness → **CHK-299** 難井地図（subtype は診断ラベル）

## Explicit Stop

- oracle gap / tip_rmse を推論特徴にしない
- 断絶 subtype をラベル無しゲートとみなして本実験に使わない
