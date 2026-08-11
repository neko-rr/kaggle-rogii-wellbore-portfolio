# CHK-289 結果 — learned conditional proposal（2026-07-30）

> action: **T3** · Kaggle GPU Ver1 COMPLETE · **提出なし**  
> kernel: [`kazeneko77/chk289-learned-proposal-gpu`](https://www.kaggle.com/code/kazeneko77/chk289-learned-proposal-gpu)  
> harvest: [`chk289-kaggle-harvest/`](../../exp/work/wave24-generator-redesign/chk289-kaggle-harvest/)  
> JSON: [`chk289-report.json`](../../exp/work/wave24-generator-redesign/chk289-kaggle-harvest/chk289-report.json)  
> 前提: 2h継続指示 · Force+allowlist · ≠F033

## 1行方針

**train井 ridge で学習した ΔTVT を PF rate に混ぜると tip soft が悪化（最良でも Δ−12.8）。** 学習済み conditional proposal（本実装）は閉鎖。CHK-290（ESS+MCMC）の結果待ち。

## 主結果（hard20 · tip soft s5@T0.15）

| 項目 | 値 |
|---|---:|
| pooled tip soft（base） | **17.24** |
| n_train wells / rows | 80 / 32000 |
| 最良 variant | `a0p15`（α=0.15） |
| 最良 pooled | **30.01** |
| Δ vs tip soft | **−12.77** |
| 改善井割合（最良） | 45% |
| acceptance | **FAIL** |

### variant 一覧（Δ = tip − variant · 正=改善）

| variant | α | Δ pooled | frac↑ |
|---|---:|---:|---:|
| a0p15 | 0.15 | **−12.8** | 0.45 |
| a0p30 | 0.30 | −118.9 | 0.05 |
| a0p50 | 0.50 | −562.6 | 0.00 |

## 解釈

- α を上げるほど壊滅 → 学習 ΔTVT が tip 面で系統的に誤方向。
- 井の45%は微改善するが pooled は壊れる（難井悪化が支配）。
- F033（Newton 手設計）とは別機構だが、**提案分布を tip 近傍から外す系は同型の害**。

## 判定

| 項目 | 値 |
|---|---|
| verdict | **NO-GO** |
| ledger | **F034**（learned ridge ΔTVT → PF rate mix） |
| next | CHK-290 harvest · 全滅なら OPS-FINAL2 |

## Explicit Stop

- ridge/線形の ΔTVT→PF rate αスイープ言い換え禁止
- α を小さくするだけの再実行禁止
- F033 Newton / F026 spr への逃げ禁止
