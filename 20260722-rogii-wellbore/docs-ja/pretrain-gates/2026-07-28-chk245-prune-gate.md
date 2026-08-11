# pretrain-gate — CHK-245 diversity prune tip-cv GPU

> skill: kaggle-pretrain-gate  
> date: 2026-07-28  
> chk: CHK-245  
> profile: tabular  
> lane: Kaggle GPU（ユーザー: Wave-21 tip-cv · 2h 継続指示）

## Tier 0

- [x] tip-cv ベース `tip-cv-sel-face-temp0p15-h20` を fork（Private · GPU · Internet OFF）
- [x] `dataset_sources` を元 tip-cv からコピー（koolbox 等）
- [x] prune graft: `CHK245_DIVERSITY_PRUNE=True` · keep=16 · rad=1.5 · soft T=0.15
- [x] ローカル mid-bank grid: keep16/rad1.5 **Δ≈+0.317** ≥ 0.30（screen PASS）
- [x] 提出なし · tip-cv 採択のみ

## Tier 1

- [x] 同一バンク上の soft-lik 再評価（`run_chk_mid_bank_batch` / prune grid）で即死なし
- [x] builder 検証: flag=1 · helper=1 · fn=1

## Tier 2

- [x] acceptance: tip-cv hard20 ≤ 29.599（vs 凍結 29.899 で ≥+0.30）
- [x] ≠224 top-k · FINAL ブレンド禁止

## Verdict

**PASS** → `tip-cv-gpu-prune16-r1p5-h20` push / GPU 実行可
