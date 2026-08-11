# CHK-290 結果 — ESS resample + MCMC rejuvenation（2026-07-30）

> action: **T3** · Kaggle GPU Ver1 COMPLETE · **提出なし**  
> kernel: [`kazeneko77/chk290-ess-mcmc-gpu`](https://www.kaggle.com/code/kazeneko77/chk290-ess-mcmc-gpu)  
> harvest: [`chk290-kaggle-harvest/`](../../exp/work/wave24-generator-redesign/chk290-kaggle-harvest/)  
> JSON: [`chk290-report.json`](../../exp/work/wave24-generator-redesign/chk290-kaggle-harvest/chk290-report.json)  
> 前提: 2h継続指示 · Force+allowlist · ≠F030

## 1行方針

**生成中 ESS連動 resample + 局所 MCMC は tip soft 未達（最良 Δ−0.51）。** Wave-24 B（proposal/SMC）は全滅。観測系（284–286）も PASS なし → **OPS-FINAL2 防衛へ。**

## 主結果（hard20 · tip soft s5@T0.15）

| 項目 | 値 |
|---|---:|
| pooled tip soft（base） | **17.24** |
| 最良 variant | `ess05_m2` |
| 最良 pooled | **17.74** |
| Δ vs tip soft | **−0.51** |
| 改善井割合（最良） | 35% |
| acceptance | **FAIL**（要 ≥+0.30） |

### variant 一覧（Δ = tip − variant · 正=改善）

| variant | Δ pooled | mean ESS | frac↑ |
|---|---:|---:|---:|
| ess03 | −3.76 | 304 | 0.60 |
| ess07 | −1.15 | 428 | 0.40 |
| ess05_m2 | **−0.51** | 371 | 0.35 |
| ess05_m4 | −2.51 | 370 | 0.35 |
| ess03_m2 | −2.52 | 302 | 0.55 |
| ess07_m2 | −2.85 | 428 | 0.35 |

（base mean ESS ≈ 372）

## 解釈

- ESS を上げた設定（ess07）でも tip は悪化 → **粒子枯渇対策≠tip面改善**。
- MCMC 追加は最良でも tip soft 未達。288/289 より害は小さいが採択不可。
- Wave-24 A/B の hard20 物差しでは生成器作り替えの PASS なし。

## 判定

| 項目 | 値 |
|---|---|
| verdict | **NO-GO** |
| ledger | **F035**（in-gen ESS resample + MCMC） |
| next | **OPS-FINAL2**（枠1=SUB-14 · 枠2=Public1）· 291–296 は前提PASSなしで skip |

## Explicit Stop

- ESS閾値×MCMC歩数の言い換え再スイープ禁止
- F030 後段焼なまし刈り込みへの回帰禁止
- F033/F034 proposal 系への逃げ禁止
