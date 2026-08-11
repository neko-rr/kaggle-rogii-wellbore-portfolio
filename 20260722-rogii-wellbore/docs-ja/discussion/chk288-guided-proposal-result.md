# CHK-288 結果 — innovation-guided proposal（2026-07-29）

> action: **T3** · Kaggle GPU Ver1 COMPLETE · **提出なし**  
> kernel: [`kazeneko77/chk288-guided-proposal-gpu`](https://www.kaggle.com/code/kazeneko77/chk288-guided-proposal-gpu)  
> harvest: [`chk288-kaggle-harvest/`](../../exp/work/wave24-generator-redesign/chk288-kaggle-harvest/)  
> JSON: [`chk288-report.json`](../../exp/work/wave24-generator-redesign/chk288-report.json)  
> 前提: CHK-287 fix=`innovation_guided_residual_proposal` · Force+allowlist

## 1行方針

**GR残差の Newton 風ガイドを PF に入れると tip soft が壊滅（最良でも Δ−23.9）。** Wave-24 B の手設計 guided proposal は閉鎖。Final防衛を優先し、289/290 は別機構の明示承認があるときだけ。

## 主結果（hard20 · tip soft s5@T0.15）

| 項目 | 値 |
|---|---:|
| pooled tip soft（base） | **17.24** |
| 最良 variant | `g0p50_m5` |
| 最良 pooled | **41.11** |
| Δ vs tip soft | **−23.87** |
| 改善井割合（最良） | 15% |
| pass 候補 | **0** |

### variant 一覧（Δ = tip − variant · 正=改善）

| variant | Δ pooled | frac↑ |
|---|---:|---:|
| g0p10_m2 | −31.3 | 0.15 |
| g0p25_m2 | −33.1 | 0.05 |
| g0p50_m2 | −28.0 | 0.10 |
| g0p25_m5 | −26.3 | 0.15 |
| g0p50_m5 | **−23.9** | 0.15 |
| g0p25_m2_clip3 | −31.5 | 0.05 |
| g0p50_m2_clip3 | −24.2 | 0.20 |

## 解釈

- 287 の「残差誘導」方向自体は診断として妥当だったが、**生成時 Newton ガイドの実装は tip 面を壊す**。
- tip 近傍クリップ（clip_k=3）でも救済できず。
- oracle 面も悪化（最良でも tip より −16）→ 天井すら下がる。

## 判定

| 項目 | 値 |
|---|---|
| verdict | **NO-GO** |
| ledger | **F033**（手設計 residual-Newton PF guide） |
| next | **OPS-FINAL2** · 289/290 は別機構の明示指示時のみ |

## Explicit Stop

- Newton / GR勾配ガイドの γ·gmax 言い換え再スイープ禁止
- F026（spr 拡散）への逃げ禁止
- 284/285 後段尤度置換への回帰禁止
